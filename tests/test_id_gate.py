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

import id_gate


POLICY_PATH = REPO_ROOT / "id_gate_policy.json"
VALID = '---\nid: EXP-TEST-20261022\nkind: idea\ncreated: 2026-10-22\ntitle: "t"\n---\n\nbody\n'


class IdGateRuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = id_gate.load_policy(POLICY_PATH)
        cls.empty = id_gate.Baseline(frozenset(), frozenset())

    def run_rules(self, files: dict[str, str], changed: list[str] | None = None, baseline=None):
        return id_gate.evaluate(changed or list(files), files, self.policy, baseline or self.empty)

    def rules(self, findings) -> set[str]:
        return {item.rule for item in findings}

    def test_valid_frontmatter_passes(self) -> None:
        self.assertEqual(self.run_rules({"note/a.md": VALID}), [])

    def test_missing_frontmatter_fails(self) -> None:
        self.assertEqual(self.rules(self.run_rules({"note/a.md": "# title\n"})), {"NO_FRONTMATTER"})

    def test_html_comment_before_frontmatter_is_not_frontmatter(self) -> None:
        text = "<!-- FILE: x -->\n\n" + VALID
        self.assertEqual(self.rules(self.run_rules({"note/a.md": text})), {"NO_FRONTMATTER"})

    def test_missing_and_empty_keys_fail(self) -> None:
        text = "---\nid:\nkind: idea\n---\n"
        self.assertEqual(self.rules(self.run_rules({"note/a.md": text})), {"EMPTY_ID", "MISSING_KEY"})

    def test_bad_id_format_fails(self) -> None:
        text = VALID.replace("EXP-TEST-20261022", "exp test")
        self.assertEqual(self.rules(self.run_rules({"note/a.md": text})), {"BAD_ID_FORMAT"})

    def test_existing_id_shapes_are_accepted(self) -> None:
        for identifier in ("EXP-00042", "EXP-GE01-04", "ESSAY-MAINT-20261020", "PAPER-DFNC-20261022"):
            text = VALID.replace("EXP-TEST-20261022", identifier)
            self.assertEqual(self.run_rules({"note/a.md": text}), [], identifier)

    def test_duplicate_id_is_reported_for_changed_file_only(self) -> None:
        files = {"note/a.md": VALID, "note/b.md": VALID}
        findings = self.run_rules(files, changed=["note/a.md"])
        self.assertEqual([(item.rule, item.path) for item in findings], [("DUPLICATE_ID", "note/a.md")])

    def test_unresolved_related_fails_unless_known(self) -> None:
        text = VALID.replace("---\n\nbody", "related: [EXP-NONE-1]\n---\n\nbody")
        self.assertEqual(self.rules(self.run_rules({"note/a.md": text})), {"UNRESOLVED_RELATED"})
        known = id_gate.Baseline(frozenset(), frozenset({"EXP-NONE-1"}))
        self.assertEqual(self.run_rules({"note/a.md": text}, baseline=known), [])

    def test_related_resolves_to_other_file(self) -> None:
        other = VALID.replace("EXP-TEST-20261022", "EXP-OTHER-20261022")
        text = VALID.replace("---\n\nbody", "related: [EXP-OTHER-20261022]\n---\n\nbody")
        self.assertEqual(self.run_rules({"note/a.md": text, "note/b.md": other}, changed=["note/a.md"]), [])

    def test_baseline_exempts_missing_frontmatter_only(self) -> None:
        baseline = id_gate.Baseline(frozenset({"note/a.md"}), frozenset())
        self.assertEqual(self.run_rules({"note/a.md": "# title\n"}, baseline=baseline), [])
        bad = VALID.replace("EXP-TEST-20261022", "exp test")
        self.assertEqual(self.rules(self.run_rules({"note/a.md": bad}, baseline=baseline)), {"BAD_ID_FORMAT"})

    def test_target_selection(self) -> None:
        self.assertTrue(id_gate.is_target("note/x/y.md", self.policy))
        self.assertFalse(id_gate.is_target("note/x/y.png", self.policy))
        self.assertFalse(id_gate.is_target("docs/y.md", self.policy))

    def test_comment_after_value_is_stripped(self) -> None:
        text = VALID.replace("EXP-TEST-20261022", "EXP-TEST-20261022   # memo")
        self.assertEqual(self.run_rules({"note/a.md": text}), [])


class IdGateGitTests(unittest.TestCase):
    def git(self, repo: pathlib.Path, *arguments: str) -> None:
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.com", *arguments],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_range_gate_blocks_new_file_without_id_and_passes_after_fix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = pathlib.Path(directory)
            self.git(repo, "init", "-q")
            (repo / "id_gate_policy.json").write_text(POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
            (repo / "note").mkdir()
            (repo / "note" / "old.md").write_text("# old\n", encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "base")
            (repo / "note" / "新規.md").write_text("# new\n", encoding="utf-8")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-q", "-m", "add")

            def run() -> int:
                with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    return id_gate.main(["--repo", str(repo), "--base", "HEAD~1", "--head", "HEAD"])

            self.assertEqual(run(), id_gate.EXIT_FINDINGS)
            (repo / "note" / "新規.md").write_text(VALID, encoding="utf-8")
            self.git(repo, "commit", "-q", "-am", "fix")
            self.assertEqual(
                id_gate.main(["--repo", str(repo), "--base", "HEAD~2", "--head", "HEAD"]),
                id_gate.EXIT_PASS,
            )

    def test_gate_error_when_base_is_missing(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(id_gate.main(["--repo", str(REPO_ROOT)]), id_gate.EXIT_GATE_ERROR)

    def test_repository_baseline_is_valid_json_with_known_keys(self) -> None:
        data = json.loads((REPO_ROOT / "id_gate_baseline.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], 1)
        self.assertIsInstance(data["exempt_paths"], list)


if __name__ == "__main__":
    unittest.main()
