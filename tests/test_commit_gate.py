"""scripts/commit.py（commit の固定入口）の試験。一時リポジトリで実行し、実リポジトリには触れない。"""
from __future__ import annotations

import contextlib
import io
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import approval  # noqa: E402
import commit  # noqa: E402

REPORT = """---
id: REPORT-FILEOP-20261126-1200
kind: report
created: 2026-11-26
title: test
---
{body}
"""


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


class CommitGateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = pathlib.Path(self.tmp.name).resolve()
        git(self.repo, "init", "-q", "-b", "master")
        git(self.repo, "config", "user.name", "t")
        git(self.repo, "config", "user.email", "t@example.invalid")
        git(self.repo, "config", "commit.gpgsign", "false")
        (self.repo / "a.txt").write_text("alpha\n", encoding="utf-8")
        (self.repo / "b.txt").write_text("beta\n", encoding="utf-8")
        (self.repo / "empty.txt").write_text("", encoding="utf-8")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "init")
        self.saved = (commit.ROOT, commit.LOG_DIR, approval.APPROVAL_DIR)
        commit.ROOT = self.repo
        commit.LOG_DIR = self.repo / "local_reports" / "commit_gate"
        approval.APPROVAL_DIR = self.repo / ".agent_state" / "approvals"
        self.msg = self.repo / "msg.txt"
        self.msg.write_text("test commit\n", encoding="utf-8")

    def tearDown(self):
        commit.ROOT, commit.LOG_DIR, approval.APPROVAL_DIR = self.saved
        self.tmp.cleanup()

    def run_commit(self, *paths):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = commit.main(["run", "--paths", *paths, "--message-file", str(self.msg)])
        lines = out.getvalue().strip().splitlines()
        return code, lines

    def head_count(self):
        return int(git(self.repo, "rev-list", "--count", "HEAD").decode().strip())

    def test_no_approval_stops_without_staging(self):
        (self.repo / "a.txt").write_text("changed\n", encoding="utf-8")
        code, lines = self.run_commit("a.txt")
        self.assertEqual((code, lines[-2:]), (1, ["reason: NO_APPROVAL", "STOP"]))
        self.assertEqual(git(self.repo, "diff", "--cached", "--name-only"), b"")

    def test_push_approval_does_not_allow_commit(self):
        approval.write("push", plan="p.json")
        (self.repo / "a.txt").write_text("changed\n", encoding="utf-8")
        code, lines = self.run_commit("a.txt")
        self.assertEqual(lines[-2], "reason: NO_APPROVAL")

    def test_normal_commit_and_single_use(self):
        approval.write("commit")
        (self.repo / "a.txt").write_text("changed\n", encoding="utf-8")
        code, lines = self.run_commit("a.txt")
        self.assertEqual((code, lines[-1]), (0, "DONE"))
        self.assertEqual(self.head_count(), 2)
        self.assertFalse((approval.APPROVAL_DIR / "commit.json").exists())
        (self.repo / "b.txt").write_text("changed\n", encoding="utf-8")
        code, lines = self.run_commit("b.txt")
        self.assertEqual(lines[-2], "reason: NO_APPROVAL")

    def test_extra_staged_file_stops(self):
        approval.write("commit")
        (self.repo / "a.txt").write_text("changed\n", encoding="utf-8")
        (self.repo / "b.txt").write_text("changed\n", encoding="utf-8")
        git(self.repo, "add", "b.txt")
        code, lines = self.run_commit("a.txt")
        self.assertEqual(lines[-2], "reason: CACHED_DIFFERS")
        self.assertEqual(self.head_count(), 1)

    def test_delete_without_report_stops(self):
        approval.write("commit")
        (self.repo / "b.txt").unlink()
        code, lines = self.run_commit("b.txt")
        self.assertEqual(lines[-2], "reason: FILEOP_REPORT_MISSING")

    def test_delete_with_report_passes(self):
        approval.write("commit")
        (self.repo / "b.txt").unlink()
        report = self.repo / "audit" / "file_operations" / "r.md"
        report.parent.mkdir(parents=True)
        report.write_text(REPORT.format(body="DEL NRA-IDE/b.txt"), encoding="utf-8")
        code, lines = self.run_commit("b.txt", "audit/file_operations/r.md")
        self.assertEqual((code, lines[-1]), (0, "DONE"))

    def test_report_without_frontmatter_stops(self):
        approval.write("commit")
        (self.repo / "b.txt").unlink()
        report = self.repo / "audit" / "file_operations" / "r.md"
        report.parent.mkdir(parents=True)
        report.write_text("DEL b.txt\n", encoding="utf-8")
        code, lines = self.run_commit("b.txt", "audit/file_operations/r.md")
        self.assertEqual(lines[-2], "reason: FILEOP_REPORT_MISSING")

    def test_restore_without_report_stops(self):
        git(self.repo, "rm", "-q", "b.txt")
        git(self.repo, "commit", "-q", "-m", "delete")
        approval.write("commit")
        (self.repo / "b.txt").write_text("beta\n", encoding="utf-8")
        code, lines = self.run_commit("b.txt")
        self.assertEqual(lines[-2], "reason: FILEOP_REPORT_MISSING")

    def test_copy_without_report_stops(self):
        approval.write("commit")
        (self.repo / "c.txt").write_text("alpha\n", encoding="utf-8")
        code, lines = self.run_commit("c.txt")
        self.assertEqual(lines[-2], "reason: FILEOP_REPORT_MISSING")

    def test_new_file_passes(self):
        approval.write("commit")
        (self.repo / "new.txt").write_text("brand new\n", encoding="utf-8")
        (self.repo / "new_empty.txt").write_text("", encoding="utf-8")
        code, lines = self.run_commit("new.txt", "new_empty.txt")
        self.assertEqual((code, lines[-1]), (0, "DONE"))

    def test_path_outside_repository_stops(self):
        approval.write("commit")
        code, lines = self.run_commit(str(self.repo.parent / "outside.txt"))
        self.assertEqual(lines[-2], "reason: BAD_ARGUMENTS")

    def test_last_line_vocabulary(self):
        code, lines = self.run_commit("a.txt")
        self.assertIn(lines[-1], {"STOP", "DONE"})


if __name__ == "__main__":
    unittest.main()
