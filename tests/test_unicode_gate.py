from __future__ import annotations

import contextlib
import io
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


POLICY_PATH = REPO_ROOT / "unicode_gate_policy.json"


class UnicodeGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = unicode_gate.load_policy(POLICY_PATH)

    def scan(self, text: str, path: str = "sample.py") -> list[unicode_gate.Finding]:
        return unicode_gate.scan_bytes(path, text.encode("utf-8"), self.policy)

    def test_safe_ascii_and_japanese_pass(self) -> None:
        self.assertEqual(self.scan("value = 1\n# Japanese: \u5b89\u5168\u306a\u6587\u7ae0\n"), [])

    def test_bidi_override_is_fail_with_correct_bidi_class(self) -> None:
        findings = self.scan("abc" + chr(0x202E) + "def")
        bidi = [item for item in findings if item.rule == "BIDI_CONTROL"]
        self.assertEqual(len(bidi), 1)
        self.assertEqual(bidi[0].severity, "fail")
        self.assertEqual(bidi[0].codepoint, "U+202E")
        self.assertEqual(bidi[0].bidi_class, "RLO")
        self.assertNotIn(chr(0x202E), bidi[0].escaped_context or "")

    def test_zero_width_space_is_fail(self) -> None:
        findings = self.scan("abc" + chr(0x200B) + "def")
        self.assertIn("INVISIBLE_FORMAT", {item.rule for item in findings})

    def test_utf8_bom_is_fail(self) -> None:
        findings = unicode_gate.scan_bytes("sample.md", b"\xef\xbb\xbftext", self.policy)
        self.assertIn("BOM", {item.rule for item in findings})

    def test_invalid_utf8_is_fail(self) -> None:
        findings = unicode_gate.scan_bytes("sample.txt", b"abc\xffdef", self.policy)
        invalid = [item for item in findings if item.rule == "INVALID_UTF8"]
        self.assertEqual(len(invalid), 1)
        self.assertEqual(invalid[0].severity, "fail")

    def test_non_ascii_line_separator_is_fail(self) -> None:
        findings = self.scan("first" + chr(0x2028) + "second")
        self.assertIn("LINE_SEPARATOR", {item.rule for item in findings})

    def test_risky_mixed_script_identifier_warns(self) -> None:
        identifier = "p" + chr(0x0430) + "ypal"
        findings = self.scan(identifier + " = 1\n")
        mixed = [item for item in findings if item.rule == "MIXED_SCRIPT_IDENTIFIER"]
        self.assertEqual(len(mixed), 1)
        self.assertEqual(mixed[0].severity, "warn")

    def test_japanese_and_latin_are_not_risky_mixed_scripts(self) -> None:
        self.assertFalse(unicode_gate.risky_scripts("NRA_\u7406\u8ad6"))

    def test_greek_formula_identifier_is_deferred_to_uts39(self) -> None:
        identifier = chr(0x03C4) + "_dynamic"
        self.assertFalse(unicode_gate.risky_scripts(identifier))

    def test_binary_extension_skips_content_decode(self) -> None:
        findings = unicode_gate.scan_bytes("image.png", b"\x89PNG\xff", self.policy)
        self.assertEqual(findings, [])

    def test_path_control_is_fail_and_escaped(self) -> None:
        path = "safe" + chr(0x200B) + ".txt"
        findings = unicode_gate.scan_path(path, self.policy)
        control = [item for item in findings if item.rule == "PATH_CONTROL"]
        self.assertEqual(len(control), 1)
        self.assertEqual(control[0].severity, "fail")
        self.assertNotIn(chr(0x200B), control[0].path)

    def test_separate_path_components_are_not_mixed(self) -> None:
        path = "latin/" + chr(0x0430) + chr(0x0431) + ".txt"
        findings = unicode_gate.scan_path(path, self.policy)
        self.assertNotIn("PATH_MIXED_SCRIPT", {item.rule for item in findings})

    def test_json_output_is_ascii_only_and_round_trips(self) -> None:
        findings = self.scan("abc" + chr(0x202E) + "def", "\u5371\u967a.py")
        rendered = unicode_gate.render_json(findings, scanned=1)
        rendered.encode("ascii")
        payload = json.loads(rendered)
        self.assertEqual(payload["status"], "FAIL")
        self.assertEqual(payload["findings"][0]["path"], "\\u5371\\u967a.py")
        self.assertNotIn(chr(0x202E), rendered)

    def test_exact_baseline_suppresses_only_matching_fe0f_occurrence(self) -> None:
        raw = ("emoji" + chr(0xFE0F)).encode("utf-8")
        findings = unicode_gate.scan_bytes("sample.md", raw, self.policy)
        variation = next(item for item in findings if item.rule == "VARIATION_SELECTOR")
        fields = {
            "path": "sample.md",
            "file_sha256": unicode_gate.sha256_bytes(raw),
            "rule": variation.rule,
            "codepoint": variation.codepoint,
            "line": variation.line,
            "column": variation.column,
        }
        entry = unicode_gate.BaselineEntry(
            id=unicode_gate.baseline_entry_id(fields), **fields
        )
        active, matched = unicode_gate.apply_baseline(
            "sample.md", raw, findings, [entry]
        )
        self.assertEqual(active, [])
        self.assertEqual(matched, [entry.id])

        changed = ("prefix emoji" + chr(0xFE0F)).encode("utf-8")
        active, matched = unicode_gate.apply_baseline(
            "sample.md",
            changed,
            unicode_gate.scan_bytes("sample.md", changed, self.policy),
            [entry],
        )
        self.assertIn("VARIATION_SELECTOR", {item.rule for item in active})
        self.assertEqual(matched, [])

    def test_baseline_loader_accepts_only_explicit_approved_scope(self) -> None:
        allowed = [
            ("VARIATION_SELECTOR", "U+FE0F"),
            ("BOM", "U+FEFF"),
            ("INVISIBLE_FORMAT", "U+200D"),
        ]
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            root = pathlib.Path(directory)
            for index, (rule, codepoint) in enumerate(allowed):
                fields = {
                    "path": f"sample-{index}.txt",
                    "file_sha256": "0" * 64,
                    "rule": rule,
                    "codepoint": codepoint,
                    "line": 1,
                    "column": 1,
                }
                document = {
                    "schema_version": 1,
                    "entries": [{"id": unicode_gate.baseline_entry_id(fields), **fields}],
                }
                path = root / f"allowed-{index}.json"
                path.write_text(json.dumps(document), encoding="ascii")
                self.assertEqual(len(unicode_gate.load_baseline(path)), 1)

            fields["rule"] = "INVISIBLE_FORMAT"
            fields["codepoint"] = "U+200B"
            document = {
                "schema_version": 1,
                "entries": [{"id": unicode_gate.baseline_entry_id(fields), **fields}],
            }
            denied = root / "denied.json"
            denied.write_text(json.dumps(document), encoding="ascii")
            with self.assertRaisesRegex(ValueError, "outside approved scope"):
                unicode_gate.load_baseline(denied)

    def test_missing_input_fails_closed(self) -> None:
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            with contextlib.redirect_stderr(stderr):
                result = unicode_gate.main([
                    "--repo", directory,
                    "--policy", str(POLICY_PATH),
                    "--paths", "missing.txt",
                ])
        self.assertEqual(result, unicode_gate.EXIT_GATE_ERROR)
        stderr.getvalue().encode("ascii")
        self.assertIn("internal failure", stderr.getvalue())

    def test_directory_scope_scans_nested_files(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            root = pathlib.Path(directory)
            nested = root / "nested"
            nested.mkdir()
            (nested / "safe.txt").write_text("safe\n", encoding="utf-8")
            (nested / "unsafe.txt").write_text(
                "abc" + chr(0x202E) + "def", encoding="utf-8"
            )
            supplied = root.relative_to(REPO_ROOT).as_posix()
            inputs = list(unicode_gate.directory_inputs(REPO_ROOT, supplied))
        findings = [
            item
            for path, raw in inputs
            for item in unicode_gate.scan_bytes(path, raw, self.policy)
        ]
        self.assertEqual(len(inputs), 2)
        self.assertIn("BIDI_CONTROL", {item.rule for item in findings})

    def test_staged_scope_reads_index_blob_not_worktree(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            repo = pathlib.Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            source = repo / "sample.py"
            source.write_text("abc" + chr(0x202E) + "def", encoding="utf-8")
            subprocess.run(["git", "add", "sample.py"], cwd=repo, check=True)
            source.write_text("safe\n", encoding="utf-8")
            inputs = list(unicode_gate.staged_inputs(repo))
        self.assertEqual([path for path, _ in inputs], ["sample.py"])
        findings = unicode_gate.scan_bytes(inputs[0][0], inputs[0][1], self.policy)
        self.assertIn("BIDI_CONTROL", {item.rule for item in findings})

    def test_missing_policy_rule_fails_at_load_time(self) -> None:
        data = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        data["rules"].pop("BIDI_CONTROL")
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests") as directory:
            path = pathlib.Path(directory) / "broken-policy.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                unicode_gate.load_policy(path)


if __name__ == "__main__":
    unittest.main()
