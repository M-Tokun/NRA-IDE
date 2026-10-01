from __future__ import annotations

import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD_ROOT = REPO_ROOT / "skills" / "agents-md-guard"
sys.path.insert(0, str(GUARD_ROOT))

import _common
import codex_guard
import codex_session_start


class CodexAgentsMdGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests")
        self.root = pathlib.Path(self.temporary.name)
        self.agents_path = self.root / "AGENTS.md"
        self.agents_path.write_text("# Test contract\n\nRead completely.\n", encoding="utf-8")
        self.marker_root = self.root / "markers"
        self.patches = [
            mock.patch.object(_common, "AGENTS_MD_PATH", str(self.agents_path)),
            mock.patch.object(_common, "MARKER_ROOT", str(self.marker_root)),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self) -> None:
        for patcher in reversed(self.patches):
            patcher.stop()
        self.temporary.cleanup()

    def run_hook(self, function, payload: object | str) -> tuple[int, str]:
        raw = payload if isinstance(payload, str) else json.dumps(payload)
        output = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(raw)), contextlib.redirect_stdout(output):
            result = function()
        return result, output.getvalue()

    def test_session_start_loads_full_contract_then_marks_session(self) -> None:
        result, raw = self.run_hook(
            codex_session_start.main,
            {"session_id": "session-1", "hook_event_name": "SessionStart"},
        )
        payload = json.loads(raw)
        self.assertEqual(result, 0)
        self.assertEqual(payload["systemMessage"], "AGENTS.md loaded")
        self.assertIn("# Test contract", payload["hookSpecificOutput"]["additionalContext"])
        self.assertTrue(_common.is_marked("codex", "session-1"))

    def test_session_start_fails_closed_when_contract_is_missing(self) -> None:
        self.agents_path.unlink()
        result, raw = self.run_hook(
            codex_session_start.main,
            {"session_id": "session-2", "hook_event_name": "SessionStart"},
        )
        payload = json.loads(raw)
        self.assertEqual(result, 0)
        self.assertFalse(payload["continue"])
        self.assertFalse(_common.is_marked("codex", "session-2"))

    def test_pre_tool_use_denies_unmarked_session(self) -> None:
        result, raw = self.run_hook(codex_guard.main, {"session_id": "session-3"})
        payload = json.loads(raw)
        self.assertEqual(result, 0)
        self.assertEqual(
            payload["hookSpecificOutput"]["permissionDecision"], "deny"
        )

    def test_pre_tool_use_allows_marked_session_without_output(self) -> None:
        _common.write_marker("codex", "session-4")
        result, raw = self.run_hook(codex_guard.main, {"session_id": "session-4"})
        self.assertEqual(result, 0)
        self.assertEqual(raw, "")

    def test_malformed_payload_is_denied(self) -> None:
        result, raw = self.run_hook(codex_guard.main, "{")
        payload = json.loads(raw)
        self.assertEqual(result, 0)
        self.assertEqual(
            payload["hookSpecificOutput"]["permissionDecision"], "deny"
        )


if __name__ == "__main__":
    unittest.main()
