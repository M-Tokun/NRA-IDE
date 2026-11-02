"""Real Git fixtures; AV substitutions are explicitly local test doubles.

The Git-client test is dry-run only and checks the real hook's rejection.
It never sends changes to a shared remote or tests production Defender safety.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import malware_gate as mg
import unicode_gate as ug
import id_gate as ig
import check_dictionary as dg
import push_gate as pg

ENV = {**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1", "PYTHONDONTWRITEBYTECODE": "1"}
VALID = "---\nid: TEST-RECORD-1\nkind: dialog\ncreated: 2026-11-02\ntitle: t\n---\n"


class GitFixture(unittest.TestCase):
    def setUp(self):
        parent = ROOT / "local_reports"
        parent.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(prefix="gate-acceptance-", dir=parent)
        self.work = Path(self.tmp.name)
        assert parent.resolve() in self.work.resolve().parents
        self.addCleanup(self.tmp.cleanup)
        self.repo = self.work / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        for name in pg.RULE_FILES:
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, dest)
        for name in ["dictionary/" + p for p in dg.ALL] + ["dictionary/ids.json"]:
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, dest)
        self.put(".gitignore", "local_reports/\nplan*.json\n")
        self.put("base.txt", "base\n")
        self.commit("base")
        self.base = self.git("rev-parse", "HEAD")
        self.remote = self.work / "remote.git"
        subprocess.run(["git", "clone", "-q", "--bare", str(self.repo), str(self.remote)], env=ENV, check=True, capture_output=True)
        self.git("remote", "add", "origin", str(self.remote))
        self.git("fetch", "-q", "origin", "+refs/heads/main:refs/remotes/origin/main")
        self.git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        self.policy = ug.load_policy(self.repo / "unicode_gate_policy.json")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.repo), "-c", "user.name=Gate test", "-c", "user.email=gate@example.invalid", *args], env=ENV, stderr=subprocess.PIPE).decode().strip()

    def put(self, name, content):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content if isinstance(content, bytes) else content.encode())

    def commit(self, message="change"):
        self.git("add", ".")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def extraction(self):
        out = self.work / ("extract-" + next(tempfile._get_candidate_names()))
        # Materialization and manifest consumption remain inside one repository.
        out = self.repo / "local_reports" / out.name
        out.parent.mkdir(exist_ok=True)
        manifest = mg.materialize_outgoing_blobs(self.repo, self.base, "HEAD", out)
        return out, manifest

    def unicode_result(self):
        out, manifest = self.extraction()
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(io.StringIO()):
            code = ug.main(["--repo", str(self.repo), "--manifest", str(out / "manifest.json"), "--policy", str(self.repo / "unicode_gate_policy.json"), "--baseline", str(self.repo / "unicode_gate_baseline.json"), "--json"])
        return code, json.loads(captured.getvalue()) if code != 2 else None, out, manifest

    def plan(self, branch="refs/heads/main"):
        self.plan_path = self.repo / "plan-test.json"
        return pg.prepare(self.repo, "origin", branch, self.plan_path, 30)

    def line(self, target="refs/heads/main", old=None):
        return f"refs/heads/main {self.git('rev-parse','HEAD')} {target} {old or self.base}\n"

    def backend(self, repo, args, timeout):
        if args[0] != "pwsh":
            return pg.command(repo, args, timeout)
        code, payload, out, manifest = self.unicode_result()
        unicode = {"status": "UNAVAILABLE", "scanned_files": 0, "reason": "TEST_INPUT_UNAVAILABLE"}
        if code != 2:
            status = "FAIL" if code == 1 else "WARN" if payload["findings"] else "PASS"
            if not payload["scanned_files"]:
                status = "NOT_APPLICABLE"
            unicode = dict(status=status, scanned_files=payload["scanned_files"], expected_files=manifest["unicode_input_count"], findings=payload["findings"])
        malware = {"status": "NOT_RUN", "scanned_files": 0}
        if code == 0:
            n = manifest["av_blob_count"]
            malware = dict(status="PASS" if n else "NOT_APPLICABLE", scanned_files=n, expected_files=n, test_double=True)
        data = dict(schema_version=1, base=self.base, head=self.git("rev-parse", "HEAD"), exit_code=code, unicode=unicode, malware=malware)
        Path(args[args.index("-ResultPath") + 1]).write_text(json.dumps(data), encoding="utf-8")
        return subprocess.CompletedProcess(args, code, b"", b"")

    def check_with_test_av(self, text=None):
        native = pg.command
        def adapter(repo, args, timeout):
            if args[0] == "pwsh":
                return self.backend(repo, args, timeout)
            return native(repo, args, timeout)
        with patch.object(pg, "command", side_effect=adapter):
            return pg.check(self.repo, "origin", str(self.remote), text or self.line(), self.plan_path)


class OutgoingContractTests(GitFixture):
    def test_original_path_and_intermediate_blob_are_checked(self):
        self.put("intermediate.txt", "a\u202eb")
        self.commit()
        (self.repo / "intermediate.txt").unlink()
        self.commit("remove")
        code, payload, _, manifest = self.unicode_result()
        self.assertEqual(code, 1)
        self.assertTrue(any(f["path"] == "intermediate.txt" and f["rule"] == "BIDI_CONTROL" for f in payload["findings"]))
        self.assertEqual(manifest["outgoing_commit_count"], 2)

    def test_exact_baseline_survives_materialized_name(self):
        raw = b"\xef\xbb\xbfapproved\n"
        f = ug.scan_bytes("approved.csv", raw, self.policy)[0]
        fields = dict(path="approved.csv", file_sha256=hashlib.sha256(raw).hexdigest(), rule=f.rule, codepoint=f.codepoint, line=f.line, column=f.column)
        baseline = dict(schema_version=1, entries=[dict(id=ug.baseline_entry_id(fields), **fields)])
        self.put("unicode_gate_baseline.json", json.dumps(baseline))
        self.put("approved.csv", raw)
        self.commit()
        code, payload, _, _ = self.unicode_result()
        self.assertEqual(code, 0)
        self.assertEqual(payload["baselined_findings"], 1)
        self.put("approved.csv", raw + b"plain\n")
        self.commit()
        self.assertEqual(self.unicode_result()[0], 1)

    def test_existing_blob_binary_to_text_is_scanned_without_new_AV_blob(self):
        self.put("image.png", "a\u202eb")
        self.commit()
        self.base = self.git("rev-parse", "HEAD")
        self.git("mv", "image.png", "source.py")
        self.commit()
        code, _, _, manifest = self.unicode_result()
        self.assertEqual(code, 1)
        self.assertEqual(manifest["av_blob_count"], 0)

    def test_reused_blob_unsafe_name_is_checked(self):
        self.git("mv", "base.txt", "bad\u202ename.txt")
        self.commit()
        code, payload, _, manifest = self.unicode_result()
        self.assertEqual(code, 1)
        self.assertEqual(manifest["av_blob_count"], 0)
        self.assertIn("PATH_CONTROL", {f["rule"] for f in payload["findings"]})

    def test_mixed_suffix_content_and_unknown_binary(self):
        for name in ("image.png", "source.py"):
            self.put(name, "a\u202eb")
        self.commit()
        self.assertEqual(self.unicode_result()[0], 1)
        self.put("unknown.avif", b"\xff")
        self.commit()
        self.assertEqual(self.unicode_result()[0], 2)

    def test_manifest_tampering_is_rejected(self):
        self.put("safe.txt", "safe\n")
        self.commit()
        out, manifest = self.extraction()
        (out / manifest["blobs"][0]["materialized_name"]).write_bytes(b"evil\n")
        with self.assertRaisesRegex(ValueError, "mismatch"):
            list(ug.manifest_inputs(self.repo, out / "manifest.json", self.policy))

    def test_capacity_rejected_before_blob_read(self):
        self.put("large.bin", b"12345")
        self.commit()
        original = mg.run_git
        calls = []
        def observe(repo, args, input_bytes=None):
            if args[:2] == ["cat-file", "blob"]:
                calls.append(args)
            return original(repo, args, input_bytes)
        with patch.object(mg, "run_git", side_effect=observe), self.assertRaises(mg.GateError):
            mg.materialize_outgoing_blobs(self.repo, self.base, "HEAD", self.repo / "too-large", maximum_total_bytes=4)
        self.assertEqual(calls, [])

    def test_changed_gitlink_is_rejected_unchanged_is_not(self):
        self.git("update-index", "--add", "--cacheinfo", "160000," + self.base + ",module")
        self.git("commit", "-q", "-m", "gitlink")
        with self.assertRaisesRegex(mg.GateError, "gitlink"):
            self.extraction()
        self.base = self.git("rev-parse", "HEAD")
        self.put("safe.txt", "safe\n")
        self.commit()
        self.assertEqual(self.unicode_result()[0], 0)

    def test_id_removal_checks_unchanged_referrer(self):
        self.put("note/owner.md", VALID)
        self.put("note/ref.md", VALID.replace("TEST-RECORD-1", "TEST-REF-1").replace("title: t\n", "title: t\nrelated: [TEST-RECORD-1]\n"))
        self.commit()
        base = self.git("rev-parse", "HEAD")
        (self.repo / "note/owner.md").unlink()
        self.commit()
        _, _, findings = ig.evaluate_range(self.repo, base, "HEAD", ig.load_policy(self.repo / "id_gate_policy.json"), ig.Baseline(frozenset(), frozenset()))
        self.assertEqual([(f.rule, f.path) for f in findings], [("UNRESOLVED_RELATED", "note/ref.md")])

    def test_dictionary_reads_head_not_dirty_or_untracked_notes(self):
        self.put("safe.txt", "safe\n")
        self.commit()
        self.put("draft.md", "[draft](dictionary/NRA-IDE_Dictionary_JP.md#not-real)\n")
        self.put("dictionary/NRA-IDE_Dictionary_JP.md", "broken worktree\n")
        with contextlib.redirect_stdout(io.StringIO()):
            code = dg.main(["--repo", str(self.repo), "--head", "HEAD", "--json"])
        self.assertEqual(code, 0)


class PlanAndPipelineTests(GitFixture):
    def setUp(self):
        super().setUp()
        self.put("safe.txt", "safe\n")
        self.commit()

    def test_success_with_explicit_test_AV_and_unrelated_draft_change(self):
        self.plan()
        self.put("draft.md", "[draft](dictionary/NRA-IDE_Dictionary_JP.md#not-real)")
        report = self.check_with_test_av()
        self.assertEqual(report["status"], "PASS", report)
        self.assertFalse(report["is_execution_permission"])

    def test_warning_does_not_block(self):
        self.put("safe.txt", "text\ufe0f\n")
        self.commit()
        self.plan()
        self.assertEqual(self.check_with_test_av()["status"], "WARN")

    def test_source_and_rules_changes_invalidate_plan(self):
        plan = self.plan()
        self.put("unicode_gate_policy.json", (self.repo / "unicode_gate_policy.json").read_bytes() + b"\n")
        with self.assertRaisesRegex(pg.GateError, "CHANGED"):
            pg.unchanged(self.repo, plan)
        self.assertEqual(self.check_with_test_av()["status"], "UNAVAILABLE")

    def test_HEAD_change_invalidates_plan(self):
        plan = self.plan()
        self.put("more.txt", "more\n")
        self.commit()
        with self.assertRaises(pg.GateError):
            pg.unchanged(self.repo, plan)

    def test_missing_plan_and_multi_ref_and_non_HEAD_are_blocked(self):
        self.assertEqual(pg.check(self.repo, "origin", str(self.remote), self.line(), None)["status"], "UNAVAILABLE")
        self.plan()
        for lines in (self.line() * 2, self.line().replace(self.git("rev-parse", "HEAD"), self.base)):
            self.assertEqual(self.check_with_test_av(lines)["status"], "UNAVAILABLE")

    def test_multiple_destinations_are_blocked(self):
        self.git("remote", "set-url", "--add", "--push", "origin", "file:///first.git")
        self.git("remote", "set-url", "--add", "--push", "origin", "file:///second.git")
        with self.assertRaisesRegex(pg.GateError, "SINGLE_DESTINATION"):
            self.plan()

    def test_incoming_commits_are_blocked(self):
        tree = self.git("rev-parse", "HEAD^{tree}")
        remote_tip = self.git("commit-tree", tree, "-p", self.git("rev-parse", "HEAD"), "-m", "remote advanced")
        self.git("update-ref", "refs/remotes/origin/main", remote_tip)
        with self.assertRaisesRegex(pg.GateError, "INCOMING"):
            self.plan()

    def test_refetch_evidence_change_invalidates_plan(self):
        plan = self.plan()
        fetch = self.repo / ".git/FETCH_HEAD"
        fetch.write_bytes(fetch.read_bytes() + b"\n")
        with self.assertRaisesRegex(pg.GateError, "CHANGED"):
            pg.unchanged(self.repo, plan)

    def test_zero_count_success_receipt_is_rejected(self):
        self.plan()
        def empty_receipt(repo, args, timeout):
            item = dict(status="PASS", scanned_files=0, expected_files=0)
            data = dict(schema_version=1, base=self.base, head=self.git("rev-parse", "HEAD"), exit_code=0, unicode=item, malware=item)
            Path(args[args.index("-ResultPath") + 1]).write_text(json.dumps(data), encoding="utf-8")
            return subprocess.CompletedProcess(args, 0, b"", b"")
        with patch.object(pg, "command", side_effect=empty_receipt):
            report = pg.check(self.repo, "origin", str(self.remote), self.line(), self.plan_path)
        self.assertEqual(report["status"], "UNAVAILABLE")
        self.assertIn("ZERO_SCAN", report["reason"])

    def test_new_branch_plan_separate_from_approval_module(self):
        plan = self.plan("refs/heads/new-branch")
        self.assertEqual(plan["context"]["base_oid"], self.base)
        self.assertEqual(set(plan["context"]["remote_oid"]), {"0"})
        self.assertFalse(plan["is_execution_permission"])

    def test_invalid_or_malformed_receipt_is_not_success(self):
        self.plan()
        def no_receipt(repo, args, timeout):
            return subprocess.CompletedProcess(args, 0, b"", b"")
        with patch.object(pg, "command", side_effect=no_receipt):
            report = pg.check(self.repo, "origin", str(self.remote), self.line(), self.plan_path)
        self.assertEqual(report["status"], "UNAVAILABLE")

    def test_timeout_and_passing_exit_with_failure_payload(self):
        with self.assertRaisesRegex(pg.GateError, "TIMEOUT"):
            pg.command(self.repo, [sys.executable, "-c", "import time; time.sleep(1)"], 0.02)
        result = subprocess.CompletedProcess([], 0, json.dumps(dict(schema_version=1, head="h", status="PASS", scanned_files=1, findings=[{}])).encode(), b"")
        with self.assertRaises(pg.GateError):
            pg.payload_result(result, "h")

    def test_native_PowerShell_prepare_only_is_not_AV_permission(self):
        if not shutil.which("pwsh"):
            self.skipTest("PowerShell is unavailable")
        receipt = self.repo / "receipt.json"
        result = subprocess.run(["pwsh", "-NoProfile", "-File", str(self.repo / "scripts/malware_gate.ps1"), "-Repository", str(self.repo), "-Base", self.base, "-Head", self.git("rev-parse", "HEAD"), "-PrepareOnly", "-ResultPath", str(receipt)], capture_output=True, env=ENV, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr.decode(errors="replace"))
        data = json.loads(receipt.read_text(encoding="utf-8-sig"))
        self.assertEqual(data["unicode"]["status"], "PASS")
        self.assertEqual(data["malware"]["status"], "NOT_RUN")

    def test_real_Git_dry_run_hook_rejects_Unicode_failure(self):
        self.put("bad.txt", "x\u202ey")
        self.commit()
        self.plan()
        result = subprocess.run(["git", "-C", str(self.repo), "-c", "core.hooksPath=.githooks", "push", "--dry-run", "origin", "HEAD:refs/heads/main"], env={**ENV, "NRA_PUSH_PLAN": str(self.plan_path)}, capture_output=True, timeout=40)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"BIDI_CONTROL", result.stdout)
        remote_oid = subprocess.check_output(["git", "--git-dir", str(self.remote), "rev-parse", "HEAD"], env=ENV).decode().strip()
        self.assertEqual(remote_oid, self.base)


if __name__ == "__main__":
    unittest.main()
