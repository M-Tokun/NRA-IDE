from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_ROOT))

import unicode_gate
import unicode_review


POLICY_PATH = REPO_ROOT / "unicode_gate_policy.json"


class UnicodeReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = unicode_gate.load_policy(POLICY_PATH)

    def make_repo(self, root: pathlib.Path, text: str) -> pathlib.Path:
        repo = root / "repo"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        (repo / "sample.py").write_text(text, encoding="utf-8")
        subprocess.run(["git", "add", "sample.py"], cwd=repo, check=True)
        return repo

    def write_scan_report(self, repo: pathlib.Path) -> pathlib.Path:
        scanned, records = unicode_review.make_records(
            unicode_gate.tracked_worktree_inputs(repo), self.policy
        )
        report = repo / "local_reports" / "unicode_gate" / "list.list"
        unicode_review.write_report(
            report, unicode_review.report_lines(scanned, records), False
        )
        return report

    def approve_first(self, report: pathlib.Path, action: str = "REMOVE_CODEPOINT") -> None:
        documents = [json.loads(line) for line in report.read_text(encoding="ascii").splitlines()]
        documents[1]["decision"] = "APPROVED"
        documents[1]["action"] = action
        report.write_text(
            "\n".join(unicode_review.canonical_json(item) for item in documents) + "\n",
            encoding="ascii",
        )

    def test_report_is_ascii_json_lines_with_pending_decision(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            raw = report.read_bytes()
            raw.decode("ascii")
            header, finding = [json.loads(line) for line in raw.decode("ascii").splitlines()]
        self.assertEqual(header["finding_count"], 1)
        self.assertEqual(finding["decision"], "PENDING")
        self.assertEqual(finding["codepoint"], "U+202E")
        self.assertNotIn(chr(0x202E).encode("utf-8"), raw)

    def test_report_refuses_accidental_overwrite(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            report = pathlib.Path(directory) / "list.list"
            report.write_text("existing\n", encoding="ascii")
            with self.assertRaises(FileExistsError):
                unicode_review.write_report(report, ["replacement"], False)

    def test_apply_requires_an_approved_record(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            _, records = unicode_review.load_report(report)
            with self.assertRaisesRegex(ValueError, "no APPROVED"):
                unicode_review.apply_approved(repo, records, self.policy)

    def test_apply_refuses_changed_file_hash(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            self.approve_first(report)
            (repo / "sample.py").write_text("changed" + chr(0x202E), encoding="utf-8")
            _, records = unicode_review.load_report(report)
            with self.assertRaisesRegex(ValueError, "hash changed"):
                unicode_review.apply_approved(repo, records, self.policy)

    def test_approved_removal_changes_only_exact_codepoint(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), "abc" + chr(0x202E) + "def\n")
            report = self.write_scan_report(repo)
            self.approve_first(report)
            _, records = unicode_review.load_report(report)
            changed = unicode_review.apply_approved(repo, records, self.policy)
            result = (repo / "sample.py").read_text(encoding="utf-8")
        self.assertEqual(changed, ["sample.py"])
        self.assertEqual(result, "abcdef\n")

    def test_line_separator_uses_same_lf_only_location_as_scanner(self) -> None:
        suspicious = "first" + chr(0x2028) + "second\n"
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), suspicious)
            report = self.write_scan_report(repo)
            self.approve_first(report)
            _, records = unicode_review.load_report(report)
            unicode_review.apply_approved(repo, records, self.policy)
            result = (repo / "sample.py").read_text(encoding="utf-8")
        self.assertEqual(result, "firstsecond\n")

    def test_replacement_cannot_be_the_same_codepoint(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            self.approve_first(report, "REPLACE_CODEPOINT")
            documents = [json.loads(line) for line in report.read_text(encoding="ascii").splitlines()]
            documents[1]["replacement_codepoint"] = "U+202E"
            report.write_text(
                "\n".join(unicode_review.canonical_json(item) for item in documents) + "\n",
                encoding="ascii",
            )
            _, records = unicode_review.load_report(report)
            with self.assertRaisesRegex(ValueError, "must change"):
                unicode_review.apply_approved(repo, records, self.policy)

    def test_immutable_finding_edit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = self.make_repo(pathlib.Path(directory), "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            documents = [json.loads(line) for line in report.read_text(encoding="ascii").splitlines()]
            documents[1]["line"] = 99
            report.write_text(
                "\n".join(unicode_review.canonical_json(item) for item in documents) + "\n",
                encoding="ascii",
            )
            with self.assertRaisesRegex(ValueError, "immutable finding fields changed"):
                unicode_review.load_report(report)

    def test_backup_contains_verified_original_and_planned_hashes(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            root = pathlib.Path(directory)
            repo = self.make_repo(root, "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            self.approve_first(report)
            _, records = unicode_review.load_report(report)
            prepared = unicode_review.prepare_approved(repo, records, self.policy)
            backup = root / "backup"
            unicode_review.write_backup(backup, prepared)
            unicode_review.verify_backup(backup, prepared)
            manifest = json.loads((backup / "manifest.json").read_text(encoding="ascii"))
        self.assertEqual(len(manifest["files"]), 1)
        self.assertNotEqual(
            manifest["files"][0]["original_sha256"],
            manifest["files"][0]["planned_sha256"],
        )

    def test_apply_rejects_backup_for_different_plan(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            root = pathlib.Path(directory)
            repo = self.make_repo(root, "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            self.approve_first(report)
            _, records = unicode_review.load_report(report)
            prepared = unicode_review.prepare_approved(repo, records, self.policy)
            backup = root / "backup"
            unicode_review.write_backup(backup, prepared)
            manifest_path = backup / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="ascii"))
            manifest["files"][0]["planned_sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(manifest), encoding="ascii")
            with self.assertRaisesRegex(ValueError, "does not match"):
                unicode_review.apply_approved(repo, records, self.policy, backup)

    def test_baseline_document_selects_only_fe0f(self) -> None:
        inputs = [
            ("sample.md", ("emoji" + chr(0xFE0F) + chr(0x200B)).encode("utf-8"))
        ]
        _, records = unicode_review.make_records(inputs, self.policy)
        document = unicode_review.baseline_document(records)
        self.assertEqual(len(document["entries"]), 1)
        self.assertEqual(document["entries"][0]["codepoint"], "U+FE0F")
        baseline_path = None
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            baseline_path = pathlib.Path(directory) / "baseline.json"
            unicode_review.write_json_document(baseline_path, document, False)
            loaded = unicode_gate.load_baseline(baseline_path)
        self.assertEqual(len(loaded), 1)

    def test_decision_update_selects_only_requested_codepoints(self) -> None:
        inputs = [
            ("sample.md", (chr(0xFE0F) + chr(0x200B) + chr(0x200D)).encode("utf-8"))
        ]
        _, records = unicode_review.make_records(inputs, self.policy)
        header = json.loads(unicode_review.report_lines(1, records)[0])
        selected = unicode_review.update_decisions(
            header,
            records,
            frozenset({"U+200B"}),
            "APPROVED",
            "REMOVE_CODEPOINT",
        )
        self.assertEqual(selected, 1)
        decisions = {record["codepoint"]: record["decision"] for record in records}
        self.assertEqual(decisions["U+200B"], "APPROVED")
        self.assertEqual(decisions["U+200D"], "PENDING")
        self.assertEqual(decisions["U+FE0F"], "PENDING")

    def test_decision_update_can_be_limited_to_exact_path(self) -> None:
        inputs = [
            ("one.md", chr(0x200B).encode("utf-8")),
            ("two.md", chr(0x200B).encode("utf-8")),
        ]
        _, records = unicode_review.make_records(inputs, self.policy)
        header = json.loads(unicode_review.report_lines(2, records)[0])
        selected = unicode_review.update_decisions(
            header,
            records,
            frozenset({"U+200B"}),
            "APPROVED",
            "REPLACE_WITH_ESCAPE",
            frozenset({"two.md"}),
        )
        self.assertEqual(selected, 1)
        by_path = {record["path"]: record for record in records}
        self.assertEqual(by_path["one.md"]["decision"], "PENDING")
        self.assertEqual(by_path["two.md"]["action"], "REPLACE_WITH_ESCAPE")

    def test_escape_replacement_writes_ascii_codepoint_notation(self) -> None:
        inputs = [("sample.md", chr(0x200B).encode("utf-8"))]
        _, records = unicode_review.make_records(inputs, self.policy)
        records[0]["decision"] = "APPROVED"
        records[0]["action"] = "REPLACE_WITH_ESCAPE"
        self.assertEqual(unicode_review.replacement_character(records[0]), "\\u200B")

    def test_restore_requires_current_planned_hash(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            root = pathlib.Path(directory)
            repo = self.make_repo(root, "abc" + chr(0x202E) + "def")
            report = self.write_scan_report(repo)
            self.approve_first(report)
            _, records = unicode_review.load_report(report)
            prepared = unicode_review.prepare_approved(repo, records, self.policy)
            backup = root / "backup"
            unicode_review.write_backup(backup, prepared)
            unicode_review.apply_approved(repo, records, self.policy, backup)
            restored = unicode_review.restore_backup(repo, backup)
            self.assertEqual(restored, ["sample.py"])
            self.assertIn(chr(0x202E), (repo / "sample.py").read_text(encoding="utf-8"))

            (repo / "sample.py").write_text("unrelated", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "neither original nor planned"):
                unicode_review.restore_backup(repo, backup)


if __name__ == "__main__":
    unittest.main()
