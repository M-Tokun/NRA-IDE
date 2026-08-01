from __future__ import annotations

import contextlib
import io
import pathlib
import sys
import tempfile
import unittest


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
PARSER_ROOT = REPO_ROOT / "nra-tcm-parser"
sys.path.insert(0, str(PARSER_ROOT))

from nra_tcm import ExtractorConfig, TextExtractor, render_markdown
from nra_tcm.cli import EXIT_INPUT_ERROR, EXIT_OUTPUT_CONFLICT, main


class ExtractorConfigTests(unittest.TestCase):
    def test_threshold_must_be_bounded(self) -> None:
        for value in (-0.01, 1.01, float("nan"), float("inf")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    ExtractorConfig(threshold=value)

    def test_unknown_language_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ExtractorConfig(language="unknown")


class TextExtractorTests(unittest.TestCase):
    def test_empty_lines_are_not_candidates(self) -> None:
        result = TextExtractor().extract(["\n", "   \n"])
        self.assertEqual(result.total_lines, 2)
        self.assertEqual(result.nonempty_lines, 0)
        self.assertEqual(result.extracted, ())

    def test_short_markdown_heading_is_preserved(self) -> None:
        result = TextExtractor().extract(["# 概要\n"])
        self.assertEqual([item.line_number for item in result.extracted], [1])
        self.assertIn("markdown_heading", result.extracted[0].reasons)

    def test_indented_code_is_not_reclassified_as_heading(self) -> None:
        source = "    # Important code   "
        result = TextExtractor(ExtractorConfig(language="en")).extract([source + "\n"])
        self.assertEqual(len(result.extracted), 1)
        item = result.extracted[0]
        self.assertEqual(item.content, source)
        self.assertNotIn("markdown_heading", item.reasons)
        self.assertIn("indented_code", item.reasons)

    def test_fenced_code_is_not_reclassified_as_heading(self) -> None:
        result = TextExtractor(ExtractorConfig(language="en")).extract(
            ["```python\n", "# Important code\n", "```\n"]
        )
        self.assertEqual(len(result.extracted), 1)
        self.assertNotIn("markdown_heading", result.extracted[0].reasons)
        self.assertIn("fenced_code", result.extracted[0].reasons)

    def test_language_keywords_are_profile_specific(self) -> None:
        ja = TextExtractor(ExtractorConfig(language="ja")).score_line("重要")
        en = TextExtractor(ExtractorConfig(language="en")).score_line("重要")
        self.assertIn("profile_keyword", ja[1])
        self.assertNotIn("profile_keyword", en[1])

    def test_english_keywords_require_word_boundaries(self) -> None:
        extractor = TextExtractor(ExtractorConfig(language="en"))
        for text in ("terror management", "resultant vector", "éerror", "error_日本"):
            with self.subTest(text=text):
                self.assertNotIn("profile_keyword", extractor.score_line(text)[1])
        for text in ("error report", "the result", "IN SUMMARY, stop"):
            with self.subTest(text=text):
                self.assertIn("profile_keyword", extractor.score_line(text)[1])

    def test_higher_threshold_is_stricter(self) -> None:
        lines = ["abc\n", "これは十分な長さを持つ説明文です。\n", "重要\n", "# 概要\n"]
        previous = None
        for step in range(101):
            threshold = step / 100
            current = {
                item.line_number
                for item in TextExtractor(ExtractorConfig(threshold=threshold)).extract(lines).extracted
            }
            if previous is not None:
                self.assertTrue(current.issubset(previous), threshold)
            previous = current

    def test_source_order_and_line_numbers_are_preserved(self) -> None:
        result = TextExtractor(ExtractorConfig(threshold=0.0)).extract(
            ["first\n", "\n", "third\n"]
        )
        self.assertEqual([item.line_number for item in result.extracted], [1, 3])

    def test_score_is_bounded(self) -> None:
        score, _ = TextExtractor().score_line("# Important " + "x" * 1000, 1.0)
        self.assertEqual(score, 1.0)

    def test_report_is_deterministic_and_discloses_scope(self) -> None:
        config = ExtractorConfig()
        result = TextExtractor(config).extract(["# Important result\n"])
        first = render_markdown(result, source_name="sample.md", config=config)
        second = render_markdown(result, source_name="sample.md", config=config)
        self.assertEqual(first, second)
        self.assertIn("not a summary, structural measurement, or safety decision", first)
        self.assertIn("Line 1", first)

    def test_report_contains_untrusted_text_only_inside_code_fence(self) -> None:
        config = ExtractorConfig()
        result = TextExtractor(config).extract(["# <img src=x onerror=alert(1)> Important ```\n"])
        report = render_markdown(result, source_name="`sample`.md", config=config)
        self.assertIn("- Source: `` `sample`.md ``", report)
        self.assertIn("````text\n# <img src=x onerror=alert(1)> Important ```\n````", report)
        self.assertNotIn("> # <img", report)


class CliTests(unittest.TestCase):
    def test_creates_report_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as directory:
            root = pathlib.Path(directory)
            source = root / "input.md"
            output = root / "report.md"
            source.write_text("# Important result\n", encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(source), "-o", str(output)]), 0)
            original = output.read_text(encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(
                    main([str(source), "-o", str(output)]),
                    EXIT_OUTPUT_CONFLICT,
                )
            self.assertEqual(output.read_text(encoding="utf-8"), original)

    def test_force_explicitly_replaces_output(self) -> None:
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as directory:
            root = pathlib.Path(directory)
            source = root / "input.md"
            output = root / "report.md"
            source.write_text("# Important result\n", encoding="utf-8")
            output.write_text("old", encoding="utf-8")

            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main([str(source), "-o", str(output), "--force"]), 0)
            self.assertNotEqual(output.read_text(encoding="utf-8"), "old")

    def test_input_cannot_be_output(self) -> None:
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as directory:
            source = pathlib.Path(directory) / "input.md"
            source.write_text("content", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(source), "-o", str(source), "--force"])
            self.assertEqual(code, EXIT_OUTPUT_CONFLICT)
            self.assertEqual(source.read_text(encoding="utf-8"), "content")

    def test_invalid_utf8_is_reported(self) -> None:
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as directory:
            root = pathlib.Path(directory)
            source = root / "input.txt"
            source.write_bytes(b"\xff")
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(source)])
            self.assertEqual(code, EXIT_INPUT_ERROR)
            self.assertFalse((root / "input_extracted.md").exists())

    def test_missing_output_directory_is_reported(self) -> None:
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as directory:
            root = pathlib.Path(directory)
            source = root / "input.md"
            source.write_text("# Important result\n", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                code = main([str(source), "-o", str(root / "missing" / "report.md")])
            self.assertNotEqual(code, 0)

    def test_cp932_console_escapes_unrepresentable_filename(self) -> None:
        with tempfile.TemporaryDirectory(dir=pathlib.Path(__file__).parent) as directory:
            source = pathlib.Path(directory) / "input_\U0001f600.md"
            source.write_text("# Important result\n", encoding="utf-8")
            encoded = io.BytesIO()
            console = io.TextIOWrapper(encoded, encoding="cp932")
            with contextlib.redirect_stdout(console):
                code = main([str(source)])
            console.flush()
            message = encoded.getvalue().decode("cp932")
            self.assertEqual(code, 0)
            self.assertIn(r"\U0001f600", message)


class ReplacementTests(unittest.TestCase):
    def test_legacy_implementations_are_absent(self) -> None:
        self.assertFalse((PARSER_ROOT / "nra_crystallizer_JP_v3_1.py").exists())
        self.assertFalse((PARSER_ROOT / "nra_crystallizer_EN_v2.py").exists())
        self.assertFalse((PARSER_ROOT / "nra-crystallization-v33-full-fix").exists())

    def test_historical_note_identifies_removed_v33(self) -> None:
        note = (REPO_ROOT / "note" / "律環公理と内包性動力学.txt").read_text(encoding="utf-8")
        self.assertIn("旧v33実験系を説明する歴史記録", note)
        self.assertIn("現行ツリーから削除済み", note)


if __name__ == "__main__":
    unittest.main()
