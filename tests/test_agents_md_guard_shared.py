from __future__ import annotations
import contextlib, io, json, os, pathlib, shutil, subprocess, sys, tempfile, unittest
from unittest import mock
ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD = ROOT / "skills" / "agents-md-guard"
sys.path.insert(0, str(GUARD))
import _common

class SharedGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / "tests")
        self.root = pathlib.Path(self.tmp.name)
        self.contract = self.root / "AGENTS.md"
        self.contract.write_text("# Contract\n全文を読む。\n", encoding="utf-8")
        self.patches = [mock.patch.object(_common, "AGENTS_MD_PATH", str(self.contract)),
                        mock.patch.object(_common, "MARKER_ROOT", str(self.root / "markers"))]
        for p in self.patches: p.start()
    def tearDown(self):
        for p in reversed(self.patches): p.stop()
        self.tmp.cleanup()
    def invoke(self, fn, raw):
        out = io.StringIO()
        raw = raw if isinstance(raw, str) else json.dumps(raw)
        with mock.patch.object(sys, "stdin", io.StringIO(raw)), contextlib.redirect_stdout(out):
            code = fn()
        return code, json.loads(out.getvalue()) if out.getvalue() else None
    def payload(self, tool, **kw):
        return {("taskId" if tool == "cline" else "session_id"): "test-1", **kw}
    def denied(self, tool, out):
        if tool == "cline": return out.get("cancel") is True
        if tool == "gemini": return out.get("decision") == "deny"
        return out.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"
    def test_bad_inputs_denied_for_every_adapter(self):
        for tool in ("claude", "codex", "gemini", "cline"):
            for raw in ("{", "[]", "null", "42", {}, self.payload(tool, tool_input=[]),
                        self.payload(tool, tool_name=[]), {("taskId" if tool == "cline" else "session_id"): "../escape"}):
                with self.subTest(tool=tool, raw=raw):
                    code, out = self.invoke(lambda: _common.run_guard(tool), raw)
                    self.assertEqual(code, 0); self.assertTrue(self.denied(tool, out))
    def test_unexpected_failure_denied(self):
        with mock.patch.object(_common, "guard_reason", side_effect=RuntimeError("test")):
            _, out = self.invoke(lambda: _common.run_guard("codex"), self.payload("codex"))
        self.assertTrue(self.denied("codex", out))
    def test_start_full_content_and_hash_invalidation(self):
        for tool in ("claude", "codex", "gemini"):
            with self.subTest(tool=tool):
                _, out = self.invoke(lambda: _common.run_session_start(tool), self.payload(tool))
                self.assertEqual(out["hookSpecificOutput"]["additionalContext"], "AGENTS.md loaded\n\n" + self.contract.read_text(encoding="utf-8"))
                self.assertTrue(_common.is_marked(tool, "test-1"))
                self.contract.write_text("# Changed " + tool + "\n", encoding="utf-8")
                self.assertFalse(_common.is_marked(tool, "test-1"))
    def test_old_marker_is_invalid(self):
        path = pathlib.Path(_common.marker_path("codex", "test-1"))
        path.parent.mkdir(parents=True); path.write_text("read\n", encoding="utf-8")
        self.assertFalse(_common.is_marked("codex", "test-1"))
    def test_failed_start_invalidates_previous_marker(self):
        for tool in ("claude", "codex", "gemini"):
            _common.write_marker(tool, "test-1")
            with mock.patch.object(_common, "read_agents_md", side_effect=OSError("test")):
                _, out = self.invoke(lambda: _common.run_session_start(tool), self.payload(tool))
            self.assertFalse(out["continue"]); self.assertFalse(_common.is_marked(tool, "test-1"))
    def test_context_truncation_is_not_marked(self):
        self.contract.write_text("x" * 12001, encoding="utf-8")
        for tool in ("claude", "codex", "gemini"):
            _, out = self.invoke(lambda: _common.run_session_start(tool), self.payload(tool))
            self.assertFalse(out["continue"]); self.assertFalse(_common.is_marked(tool, "test-1"))
    def test_marker_write_failure_emits_one_json(self):
        with mock.patch.object(_common, "write_marker", side_effect=OSError("test")), contextlib.redirect_stderr(io.StringIO()):
            code, out = self.invoke(lambda: _common.run_session_start("codex"), self.payload("codex"))
        self.assertEqual(code, 2); self.assertIn("hookSpecificOutput", out)
        self.assertFalse(_common.is_marked("codex", "test-1"))
    def test_read_exemption_and_unknown_mutation_coverage(self):
        for tool in ("claude", "codex", "gemini", "cline"):
            for name in ("Bash", "PowerShell", "Edit", "Write", "mcp__service__write", "future_tool"):
                _, out = self.invoke(lambda: _common.run_guard(tool), self.payload(tool, tool_name=name))
                self.assertTrue(self.denied(tool, out))
            args_key = "parameters" if tool == "cline" else "tool_input"
            _, out = self.invoke(lambda: _common.run_guard(tool), self.payload(tool, tool_name="Read", **{args_key:{"file_path":str(self.contract)}}))
            self.assertFalse(self.denied(tool, out or {}))
    def test_bootstrap_rejects_other_reads_and_missing_contract_for_all_hosts(self):
        for tool in ('claude','codex','gemini','cline'):
            args_key='parameters' if tool=='cline' else 'tool_input'
            for name,args in (('Read',{}),('Read',{'file_path':str(self.root/'other.md')}),
                              ('Read',{'file_path':str(self.contract),'limit':1}),
                              ('read_many_files',{'paths':[str(self.contract),'other.md']}),
                              ('read_many_files',{'paths':['*.md']}),('Glob',{'pattern':'*'}),
                              ('Grep',{'pattern':'contract'}),('WebFetch',{'url':'https://example.invalid'})):
                _,out=self.invoke(lambda:_common.run_guard(tool),self.payload(tool,tool_name=name,**{args_key:args}))
                self.assertTrue(self.denied(tool,out))
            for name,args in (('Read',{'file_path':str(self.contract)}),('read_file',{'path':'AGENTS.md'}),
                              ('read_many_files',{'paths':[str(self.contract)]})):
                _,out=self.invoke(lambda:_common.run_guard(tool),self.payload(tool,tool_name=name,**{args_key:args}))
                self.assertFalse(self.denied(tool,out or {}))
        self.contract.rename(self.root/'AGENTS.missing')
        for tool in ('claude','codex','gemini','cline'):
            args_key='parameters' if tool=='cline' else 'tool_input'
            _,out=self.invoke(lambda:_common.run_guard(tool),self.payload(tool,tool_name='Read',**{args_key:{'path':str(self.contract)}}))
            self.assertTrue(self.denied(tool,out))

    def test_marked_guard_leaves_host_permissions_intact(self):
        for tool in ("claude", "codex", "gemini", "cline"):
            _common.write_marker(tool, "test-1")
            _, out = self.invoke(lambda: _common.run_guard(tool), self.payload(tool, tool_name="Bash", tool_input={"command": "git push origin HEAD"}))
            self.assertEqual(out, {"cancel": False} if tool == "cline" else {} if tool == "gemini" else None)
    def test_full_read_required_in_legacy_adapter(self):
        text = self.contract.read_text(encoding="utf-8")
        for tool in ("claude", "codex", "gemini", "cline"):
            for name, args, response in (
                ("partial", {"file_path": str(self.contract), "limit": 1}, {"content": text}),
                ("error", {"file_path": str(self.contract)}, {"error": "failed", "content": text}),
                ("foreign", {"file_path": str(self.root / "other" / "NRA-IDE" / "AGENTS.md")}, {"content": text}),
                ("short", {"file_path": str(self.contract)}, {"content": "# Contract"}),
                ("full", {"file_path": str(self.contract)}, {"content": text})):
                payload = self.payload(tool, tool_response=response)
                payload["parameters" if tool == "cline" else "tool_input"] = args
                self.invoke(lambda: _common.mark_verified_read(tool), payload)
                self.assertEqual(_common.is_marked(tool, "test-1"), name == "full")
    def test_relative_path_matches_only_from_root(self):
        previous = os.getcwd()
        try:
            os.chdir(self.root)
            self.assertTrue(_common.path_targets_agents_md("AGENTS.md"))
        finally:
            os.chdir(previous)
        self.assertFalse(_common.command_reads_agents_md("cat AGENTS.md"))
    def test_configured_hooks_execute_from_nested_cwd(self):
        target = self.root / "skills" / "agents-md-guard"
        shutil.copytree(GUARD, target, ignore=shutil.ignore_patterns("__pycache__"))
        nested = self.root / "nested"; nested.mkdir()
        for tool, settings, event, variable in (
            ("claude", ".claude/settings.json", "PreToolUse", "CLAUDE_PROJECT_DIR"),
            ("gemini", ".gemini/settings.json", "BeforeTool", "GEMINI_PROJECT_DIR")):
            config = json.loads((ROOT / settings).read_text(encoding="utf-8"))
            self.assertEqual(config["hooks"][event][0]["matcher"], ".*")
            env = dict(os.environ); env[variable] = str(self.root); env["PYTHONDONTWRITEBYTECODE"] = "1"
            def run(event_name):
                command = config["hooks"][event_name][0]["hooks"][0]["command"]
                result = subprocess.run(command, shell=True, cwd=nested, env=env, input=json.dumps(self.payload(tool, tool_name="Bash")), text=True, capture_output=True, timeout=15)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout) if result.stdout else None
            self.assertTrue(self.denied(tool, run(event)))
            out = run("SessionStart"); self.assertIn("全文を読む", out["hookSpecificOutput"]["additionalContext"])
            self.assertFalse(self.denied(tool, run(event) or {}))
    def test_codex_matcher_covers_all_tools(self):
        config = json.loads((ROOT / ".codex/hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(config["hooks"]["PreToolUse"][0]["matcher"], ".*")

if __name__ == "__main__": unittest.main()
