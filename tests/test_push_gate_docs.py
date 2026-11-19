"""The push documents must name exactly the gates that push_gate.py runs, and never a gate count."""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import push_gate  # noqa: E402

PROCEDURE = ROOT / "docs" / "PUSH_PROCEDURE.md"
ERROR_MANUAL = ROOT / "docs" / "ERROR_MANUAL.md"
GATE_LINE = re.compile(r"^- ゲートは (.+?)（正本は scripts/push_gate\.py の GATES）", re.M)
GATE_COUNT = re.compile(r"[0-9０-９一二三四五六七八九十]+\s*ゲート")


class PushGateDocsTests(unittest.TestCase):
    def test_procedure_lists_exactly_the_gates(self) -> None:
        matches = GATE_LINE.findall(PROCEDURE.read_text(encoding="utf-8"))
        self.assertEqual(len(matches), 1, "PUSH_PROCEDURE.md must list the gates in exactly one place")
        listed = tuple(name.strip() for name in matches[0].split("/"))
        self.assertEqual(listed, push_gate.GATES)

    def test_documents_do_not_state_a_gate_count(self) -> None:
        for path in (PROCEDURE, ERROR_MANUAL):
            with self.subTest(path=path.name):
                self.assertEqual(GATE_COUNT.findall(path.read_text(encoding="utf-8")), [])


if __name__ == "__main__":
    unittest.main()
