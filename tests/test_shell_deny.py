"""共通ガードのシェル禁止パターン（AGENTS.md §7）の回帰テスト。

コマンド文字列だけを見る誤操作の歯止めであり、スクリプト内・別名・変数経由は対象外。
"""
from __future__ import annotations
import contextlib, io, json, pathlib, sys, tempfile, unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD = ROOT / "skills" / "agents-md-guard"
sys.path.insert(0, str(GUARD))
import _common

DENIED = [
    ("git filter-repo --force", "filter-repo"),
    ("git filter-branch --all", "filter-branch"),
    ("git reflog expire --expire=now --all", "reflog expire"),
    ("git gc --prune=now", "gc --prune"),
    ("git push --force", "--force"),
    ("git push -f origin master", "--force"),
    ("git push -fu origin master", "--force"),
    ("git push --force-with-lease", "--force"),
    ("git push origin +master", "+refspec"),
    ("git push origin :old-branch", ":ref"),
    ("git push --delete origin old", "--delete"),
    ("git push -d origin old", "--delete"),
    ("git commit --no-verify -m x", "--no-verify"),
    ("git push --no-verify", "--no-verify"),
    ("git -c core.hooksPath=x commit -m y", "core.hooksPath"),
    ("git config core.hooksPath hooks", "core.hooksPath"),
    ("git config --global core.hooksPath hooks", "core.hooksPath"),
    ("git -C sub push --force", "--force"),
    ("git --no-pager -C sub push -f", "--force"),
    ("/usr/bin/git push -f", "--force"),
    ("C:\\git\\cmd\\git.exe push -f", "--force"),
    ("GIT.EXE PUSH --FORCE", "--force"),
    ("git-filter-repo --force", "filter-repo"),
    # 連結・パイプ・環境変数・呼出し演算子
    ("git status; git push -f", "--force"),
    ("git add x && git push --force", "--force"),
    ("git fetch || git push -f", "--force"),
    ("echo a | git push -f", "--force"),
    ("FOO=1 git push -f", "--force"),
    ("& git push -f", "--force"),
    ("$env:X='1'; git push -f", "--force"),
    ("git log\ngit push --force", "--force"),
    # 別シェル経由
    ('pwsh -NoProfile -Command "git push --force"', "--force"),
    ('powershell.exe -Command "git filter-repo"', "filter-repo"),
    ("bash -lc 'git push -f'", "--force"),
    ('cmd /c "git push --force"', "--force"),
    ('pwsh -Command "git status; git push -f"', "--force"),
    ('bash -c "pwsh -Command \'git push -f\'"', "--force"),
]

ALLOWED = [
    "git status",
    "git push origin master",
    "git push -u origin master",
    "git push --set-upstream origin master",
    "git push --dry-run origin master",
    "git push --tags",
    "git push origin HEAD:refs/heads/work",
    "git fetch origin",
    "git log --grep=filter-repo",
    "git config user.name x",
    "git gc",
    "git reflog",
    "git reflog show",
    "git stash push -m x",
    'git commit -m "remove --no-verify use"',
    'git commit -m "git push --force note"',
    'echo "git push --force"',
    'grep "git push --force" README.md',
    "python -c \"print('git push -f')\"",
    "python scripts/check_links.py",
    "git commit -m \"$(cat <<'EOF'\n- deny: git filter-repo、filter-branch\nEOF\n)\"",
    "",
    "   ",
]


class DangerousCommandTests(unittest.TestCase):
    def test_denied_forms(self):
        for command, expected in DENIED:
            with self.subTest(command=command):
                label = _common.dangerous_git_command(command)
                self.assertIsNotNone(label)
                self.assertIn(expected, label)

    def test_allowed_forms(self):
        for command in ALLOWED:
            with self.subTest(command=command):
                self.assertIsNone(_common.dangerous_git_command(command))

    def test_unbalanced_quote_does_not_raise(self):
        self.assertIsNone(_common.dangerous_git_command('git commit -m "unterminated'))
        self.assertIsNotNone(_common.dangerous_git_command('git push -f "unterminated'))

    def test_deep_wrapper_nesting_is_bounded(self):
        command = "git push -f"
        for _ in range(6):
            command = 'bash -c "' + command.replace('"', "'") + '"'
        _common.dangerous_git_command(command)  # 無限再帰・例外にならないこと

    def test_shell_tools_and_argument_fields(self):
        cases = [
            ("claude", {"tool_name": "Bash", "tool_input": {"command": "git push -f"}}),
            ("claude", {"tool_name": "PowerShell", "tool_input": {"command": "git push -f"}}),
            ("codex", {"tool_name": "exec_command", "tool_input": {"cmd": "git push -f"}}),
            ("codex", {"tool_name": "shell_command", "tool_input": {"command": "git push -f"}}),
            ("gemini", {"tool_name": "run_shell_command", "tool_input": {"command": "git push -f"}}),
            ("cline", {"tool_name": "cline_tool:execute_command",
                       "parameters": {"command": "git push -f"}}),
        ]
        for tool, payload in cases:
            with self.subTest(tool=tool, name=payload["tool_name"]):
                reason = _common.shell_deny_reason(payload, tool)
                self.assertIn("AGENTS.md §7", reason)
                self.assertIn("--force", reason)

    def test_non_shell_tool_is_not_inspected(self):
        payload = {"tool_name": "Read", "tool_input": {"command": "git push -f"}}
        self.assertIsNone(_common.shell_deny_reason(payload, "claude"))

    def test_shell_tool_with_non_string_command_is_denied(self):
        for args in ({"command": None}, {"command": ["git", "push", "-f"]}, {"command": 1},
                     {"cmd": 1}):
            with self.subTest(args=args):
                payload = {"tool_name": "Bash", "tool_input": args}
                self.assertEqual(_common.shell_deny_reason(payload, "claude"),
                                 _common.SHELL_INVALID_MESSAGE)

    def test_shell_tool_without_command_text_has_nothing_to_inspect(self):
        for args in ({}, {"description": "no command"}):
            with self.subTest(args=args):
                payload = {"tool_name": "Bash", "tool_input": args}
                self.assertIsNone(_common.shell_deny_reason(payload, "claude"))


class GuardIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / "tests")
        self.root = pathlib.Path(self.tmp.name)
        self.contract = self.root / "AGENTS.md"
        self.contract.write_text("# Contract\n全文を読む。\n", encoding="utf-8")
        self.patches = [mock.patch.object(_common, "AGENTS_MD_PATH", str(self.contract)),
                        mock.patch.object(_common, "MARKER_ROOT", str(self.root / "markers"))]
        for patch in self.patches:
            patch.start()

    def tearDown(self):
        for patch in reversed(self.patches):
            patch.stop()
        self.tmp.cleanup()

    def payload(self, tool, command):
        if tool == "cline":
            return {"taskId": "test-1", "preToolUse": {
                "toolName": "execute_command", "parameters": {"command": command}}}
        names = {"claude": "Bash", "codex": "exec_command", "gemini": "run_shell_command"}
        args = {"cmd": command} if tool == "codex" else {"command": command}
        return {"session_id": "test-1", "hook_event_name": "PreToolUse",
                "tool_name": names[tool], "tool_input": args}

    def run_guard(self, tool, command):
        out = io.StringIO()
        raw = json.dumps(self.payload(tool, command))
        with mock.patch.object(sys, "stdin", io.StringIO(raw)), contextlib.redirect_stdout(out):
            code = _common.run_guard(tool)
        return code, (json.loads(out.getvalue()) if out.getvalue() else {})

    def denied(self, tool, out):
        if tool == "cline":
            return out.get("cancel") is True
        if tool == "gemini":
            return out.get("decision") == "deny"
        return out.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"

    def reason(self, tool, out):
        if tool == "cline":
            return out.get("errorMessage", "")
        if tool == "gemini":
            return out.get("reason", "")
        return out.get("hookSpecificOutput", {}).get("permissionDecisionReason", "")

    def test_marked_session_denies_forbidden_command_for_every_adapter(self):
        for tool in ("claude", "codex", "gemini", "cline"):
            with self.subTest(tool=tool):
                _common.write_marker(tool, "test-1")
                code, out = self.run_guard(tool, "git push --force origin master")
                self.assertEqual(code, 0)
                self.assertTrue(self.denied(tool, out))
                self.assertIn("AGENTS.md §7", self.reason(tool, out))

    def test_marked_session_passes_ordinary_command_to_host_permissions(self):
        for tool in ("claude", "codex", "gemini", "cline"):
            with self.subTest(tool=tool):
                _common.write_marker(tool, "test-1")
                code, out = self.run_guard(tool, "git push origin master")
                self.assertEqual(code, 0)
                self.assertFalse(self.denied(tool, out))
                self.assertNotIn("permissionDecision", json.dumps(out))  # 自動承認を返さない

    def test_unmarked_session_still_gets_the_contract_reason(self):
        for tool in ("claude", "codex", "gemini", "cline"):
            with self.subTest(tool=tool):
                _, out = self.run_guard(tool, "git status")
                self.assertTrue(self.denied(tool, out))
                self.assertEqual(self.reason(tool, out), _common.REASON_MESSAGE)

    def test_contract_read_exemption_is_unchanged(self):
        out = io.StringIO()
        raw = json.dumps({"session_id": "test-1", "tool_name": "Read",
                          "tool_input": {"file_path": str(self.contract)}})
        with mock.patch.object(sys, "stdin", io.StringIO(raw)), contextlib.redirect_stdout(out):
            _common.run_guard("claude")
        self.assertEqual(out.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
