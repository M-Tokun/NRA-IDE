from __future__ import annotations

import contextlib
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

import fileop_gate


def report(paths: list[str], identifier: str = "REPORT-FILEOP-20261118-1600") -> str:
    body = "\n".join(f"- 削除: NRA-IDE/{path}" for path in paths)
    return (
        "---\n"
        f"id: {identifier}\n"
        "kind: report\n"
        "created: 2026-11-18\n"
        'title: "ファイル操作報告"\n'
        "---\n\n"
        "# ファイル操作報告\n\n"
        f"{body}\n"
    )


class FileopGateRuleTests(unittest.TestCase):
    def rules(self, findings) -> set[str]:
        return {item.rule for item in findings}

    def test_name_status_parses_delete(self) -> None:
        raw = b"D\0note/old.md\0"
        self.assertEqual(fileop_gate.parse_name_status(raw), (["note/old.md"], []))

    def test_name_status_parses_rename_pair(self) -> None:
        raw = b"R100\0note/old.md\0note/new.md\0"
        deleted, renamed = fileop_gate.parse_name_status(raw)
        self.assertEqual(deleted, [])
        self.assertEqual(renamed, [("note/old.md", "note/new.md")])

    def test_name_status_parses_mixed_entries(self) -> None:
        raw = b"D\0a.md\0R100\0b.md\0c.md\0D\0d.md\0"
        deleted, renamed = fileop_gate.parse_name_status(raw)
        self.assertEqual(deleted, ["a.md", "d.md"])
        self.assertEqual(renamed, [("b.md", "c.md")])

    def test_name_status_rejects_truncated_output(self) -> None:
        with self.assertRaises(fileop_gate.GateError):
            fileop_gate.parse_name_status(b"D\0")

    def test_mentions_accepts_either_separator(self) -> None:
        self.assertTrue(fileop_gate.mentions("NRA-IDE/note/a.md", "note/a.md"))
        self.assertTrue(fileop_gate.mentions("NRA-IDE\\note\\a.md", "note/a.md"))
        self.assertFalse(fileop_gate.mentions("NRA-IDE/note/b.md", "note/a.md"))

    def test_is_report_requires_prefix_and_extension(self) -> None:
        self.assertTrue(fileop_gate.is_report("audit/file_operations/x.md"))
        self.assertFalse(fileop_gate.is_report("audit/other/x.md"))
        self.assertFalse(fileop_gate.is_report("audit/file_operations/x.txt"))

    def test_valid_report_has_no_findings(self) -> None:
        reports = {"audit/file_operations/r.md": report(["note/a.md"])}
        self.assertEqual(fileop_gate.check_reports(reports), [])

    def test_report_without_frontmatter_fails(self) -> None:
        reports = {"audit/file_operations/r.md": "# report\n"}
        self.assertEqual(self.rules(fileop_gate.check_reports(reports)), {"NO_FRONTMATTER"})

    def test_report_missing_required_key_fails(self) -> None:
        text = report(["note/a.md"]).replace('title: "ファイル操作報告"\n', "")
        self.assertEqual(self.rules(fileop_gate.check_reports({"audit/file_operations/r.md": text})),
                         {"MISSING_KEY"})

    def test_report_with_wrong_id_shape_fails(self) -> None:
        text = report(["note/a.md"], identifier="REPORT-LRD-001-X-20261118")
        self.assertEqual(self.rules(fileop_gate.check_reports({"audit/file_operations/r.md": text})),
                         {"BAD_REPORT_ID"})


class FileopGateGitTests(unittest.TestCase):
    def git(self, repo: pathlib.Path, *arguments: str) -> None:
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.com", *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"},
        )

    @contextlib.contextmanager
    def repository(self):
        """A repository whose first commit holds note/old.md and note/keep.md."""
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "local_reports") as directory:
            repo = pathlib.Path(directory)
            self.git(repo, "init", "-q")
            (repo / "note").mkdir()
            (repo / "note" / "old.md").write_text("# old\n", encoding="utf-8")
            (repo / "note" / "keep.md").write_text("# keep\n", encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "base")
            yield repo

    def add_report(self, repo: pathlib.Path, text: str, name: str = "r.md") -> None:
        folder = repo / "audit" / "file_operations"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text(text, encoding="utf-8")

    def run_gate(self, repo: pathlib.Path, base: str = "HEAD~1", head: str = "HEAD") -> int:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return fileop_gate.main(["--repo", str(repo), "--base", base, "--head", head])

    def run_json(self, repo: pathlib.Path, base: str = "HEAD~1", head: str = "HEAD"):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(io.StringIO()):
            code = fileop_gate.main(["--repo", str(repo), "--base", base, "--head", head, "--json"])
        return code, json.loads(stream.getvalue())

    def test_commit_without_deletion_passes(self) -> None:
        with self.repository() as repo:
            (repo / "note" / "added.md").write_text("# added\n", encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "add only")
            code, data = self.run_json(repo)
            self.assertEqual(code, fileop_gate.EXIT_PASS)
            self.assertEqual(data["status"], "PASS")
            self.assertEqual(data["scanned_files"], 0)

    def test_deletion_without_report_is_blocked(self) -> None:
        with self.repository() as repo:
            self.git(repo, "rm", "-q", "note/old.md")
            self.git(repo, "commit", "-q", "-m", "delete")
            code, data = self.run_json(repo)
            self.assertEqual(code, fileop_gate.EXIT_FINDINGS)
            self.assertEqual(data["status"], "FAIL")
            self.assertEqual({item["rule"] for item in data["findings"]}, {"MISSING_REPORT"})

    def test_deletion_with_report_naming_the_path_passes(self) -> None:
        with self.repository() as repo:
            self.git(repo, "rm", "-q", "note/old.md")
            self.add_report(repo, report(["note/old.md"]))
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "delete with report")
            self.assertEqual(self.run_gate(repo), fileop_gate.EXIT_PASS)

    def test_deletion_with_report_missing_the_path_is_blocked(self) -> None:
        with self.repository() as repo:
            self.git(repo, "rm", "-q", "note/old.md")
            self.add_report(repo, report(["note/unrelated.md"]))
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "delete with wrong report")
            code, data = self.run_json(repo)
            self.assertEqual(code, fileop_gate.EXIT_FINDINGS)
            self.assertEqual({item["rule"] for item in data["findings"]}, {"PATH_NOT_REPORTED"})
            self.assertEqual([item["path"] for item in data["findings"]], ["note/old.md"])

    def test_deletion_with_malformed_report_is_blocked(self) -> None:
        with self.repository() as repo:
            self.git(repo, "rm", "-q", "note/old.md")
            self.add_report(repo, "# 報告\n\n- 削除: NRA-IDE/note/old.md\n")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "delete with bare report")
            code, data = self.run_json(repo)
            self.assertEqual(code, fileop_gate.EXIT_FINDINGS)
            self.assertEqual({item["rule"] for item in data["findings"]}, {"NO_FRONTMATTER"})

    def test_rename_requires_both_sides_named(self) -> None:
        with self.repository() as repo:
            self.git(repo, "mv", "note/old.md", "note/moved.md")
            self.add_report(repo, report(["note/old.md", "note/moved.md"]))
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "move with report")
            self.assertEqual(self.run_gate(repo), fileop_gate.EXIT_PASS)

    def test_rename_without_any_report_is_blocked(self) -> None:
        with self.repository() as repo:
            self.git(repo, "mv", "note/old.md", "note/moved.md")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "move")
            self.assertEqual(self.run_gate(repo), fileop_gate.EXIT_FINDINGS)

    def test_deleting_a_past_report_also_needs_a_report(self) -> None:
        with self.repository() as repo:
            self.add_report(repo, report(["note/keep.md"]), name="old_report.md")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "first report")
            self.git(repo, "rm", "-q", "audit/file_operations/old_report.md")
            self.git(repo, "commit", "-q", "-m", "remove past report")
            self.assertEqual(self.run_gate(repo), fileop_gate.EXIT_FINDINGS)

    def test_json_result_carries_the_requested_range(self) -> None:
        with self.repository() as repo:
            self.git(repo, "rm", "-q", "note/old.md")
            self.git(repo, "commit", "-q", "-m", "delete")
            _, data = self.run_json(repo, base="HEAD~1", head="HEAD")
            self.assertEqual(data["schema_version"], 1)
            self.assertEqual(data["base"], "HEAD~1")
            self.assertEqual(data["head"], "HEAD")
            self.assertIsInstance(data["findings"], list)
            self.assertIsInstance(data["scanned_files"], int)

    def test_gate_error_when_base_is_missing(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(fileop_gate.main(["--repo", str(REPO_ROOT)]), fileop_gate.EXIT_GATE_ERROR)


class FileopGateWiringTests(unittest.TestCase):
    def test_push_gate_registers_the_fileop_gate(self) -> None:
        text = (REPO_ROOT / "scripts" / "push_gate.py").read_text(encoding="utf-8")
        self.assertIn("fileop", text)
        self.assertIn("scripts/fileop_gate.py", text)

    def test_skill_states_the_report_location(self) -> None:
        skill = REPO_ROOT / "skills" / "file-operation-report" / "SKILL.md"
        self.assertIn(fileop_gate.REPORT_PREFIX, skill.read_text(encoding="utf-8"))

    def test_agents_md_routes_to_the_skill(self) -> None:
        text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("skills/file-operation-report/SKILL.md", text)


if __name__ == "__main__":
    unittest.main()
