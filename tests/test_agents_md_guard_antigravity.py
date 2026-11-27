"""Antigravity IDE 用 SessionStart / PreToolUse（agents-md-guard・outside-root-guard）の単体テスト。"""
from __future__ import annotations

import contextlib
import io
import json
import os
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
GUARD_ROOT = REPO_ROOT / "skills" / "agents-md-guard"
OUTSIDE_ROOT = REPO_ROOT / "skills" / "outside-root-guard"
sys.path.insert(0, str(GUARD_ROOT))
sys.path.insert(0, str(OUTSIDE_ROOT))

import _common  # noqa: E402
import _outside  # noqa: E402
import antigravity_guard  # noqa: E402
import antigravity_outside  # noqa: E402
import antigravity_session_start  # noqa: E402


class AntigravityGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(dir=REPO_ROOT / "tests")
        self.root = pathlib.Path(self.tmp.name)
        self.contract = self.root / "AGENTS.md"
        self.contract.write_text("# Contract\n全文を読む。\n", encoding="utf-8")
        self.patches = [
            mock.patch.object(_common, "AGENTS_MD_PATH", str(self.contract)),
            mock.patch.object(_common, "MARKER_ROOT", str(self.root / "markers")),
            mock.patch.object(_common, "APPROVAL_DIR", str(self.root / "approvals")),
            mock.patch.object(_common, "PUSH_STATE_PATH", str(self.root / "push_route_state.json")),
            mock.patch.object(antigravity_session_start, "LOG_PATH", self.root / "session_start.jsonl"),
            mock.patch.object(_outside, "LOG_PATH", str(self.root / "outside_root.jsonl")),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self) -> None:
        for p in reversed(self.patches):
            p.stop()
        self.tmp.cleanup()

    def invoke(self, fn, payload: object | str) -> tuple[int, dict]:
        raw = payload if isinstance(payload, str) else json.dumps(payload, ensure_ascii=False)
        out = io.StringIO()
        with mock.patch.object(sys, "stdin", io.StringIO(raw)), contextlib.redirect_stdout(out):
            code = fn()
        return code, json.loads(out.getvalue())

    def tool_payload(self, name: str, args: dict, conv: str = "conv-1") -> dict:
        return {
            "conversationId": conv,
            "cwd": str(self.root),
            "toolCall": {"id": "t1", "name": name, "args": args},
        }

    def test_session_start_injects_contract_marks_and_clears_approvals(self) -> None:
        approvals = self.root / "approvals"
        approvals.mkdir()
        (approvals / "commit.json").write_text("{}", encoding="utf-8")
        code, out = self.invoke(antigravity_session_start.main, {"conversationId": "conv-1"})
        self.assertEqual(code, 0)
        msg = out["injectSteps"][0]["systemMessage"]["systemMessage"]
        self.assertIn("AGENTS.md loaded", msg)
        self.assertIn("# Contract", msg)
        self.assertTrue(_common.is_marked("antigravity", "conv-1"))
        self.assertFalse((approvals / "commit.json").exists())

    def test_session_start_rejects_too_long_contract(self) -> None:
        self.contract.write_text("x" * 10001, encoding="utf-8")
        code, out = self.invoke(antigravity_session_start.main, {"conversationId": "conv-2"})
        self.assertEqual(code, 0)
        self.assertIn("上限10000字", out["injectSteps"][0]["errorMessage"]["userMessage"])
        self.assertFalse(_common.is_marked("antigravity", "conv-2"))

    def test_pre_tool_use_unmarked_allows_only_full_contract_read(self) -> None:
        # 通常コマンドは未読拒否
        code, out = self.invoke(antigravity_guard.main,
                                self.tool_payload("run_command", {"CommandLine": "git status"}))
        self.assertEqual(code, 0)
        self.assertEqual(out["decision"], "deny")
        # 単独全文読取は通過（decision 必須のため ask。自動承認しない）
        code, out = self.invoke(antigravity_guard.main,
                                self.tool_payload("read_file", {"Path": str(self.contract)}))
        self.assertEqual(code, 0)
        self.assertEqual(out, {"decision": "ask"})
        # 部分読取（StartLine 付き）は拒否
        code, out = self.invoke(antigravity_guard.main,
                                self.tool_payload("read_file", {"Path": str(self.contract), "StartLine": 1}))
        self.assertEqual(code, 0)
        self.assertEqual(out["decision"], "deny")

    def test_pre_tool_use_marked_denies_git_and_approval_writes(self) -> None:
        _common.write_marker("antigravity", "conv-1")
        # 通常コマンドは ask（自動承認しない）
        _, out = self.invoke(antigravity_guard.main,
                             self.tool_payload("run_command", {"CommandLine": "git status"}))
        self.assertEqual(out, {"decision": "ask"})
        # 直接 git commit / git push / force push は拒否
        for cmd in ("git commit -m x", "git push origin master", "git push --force"):
            _, out = self.invoke(antigravity_guard.main,
                                 self.tool_payload("run_command", {"CommandLine": cmd}))
            self.assertEqual(out["decision"], "deny", cmd)
        # 承認ディレクトリ書込は拒否
        d = ".agent_state" + "/" + "approvals"
        _, out = self.invoke(antigravity_guard.main,
                             self.tool_payload("write_file", {"Path": str(self.root / d / "commit.json")}))
        self.assertEqual(out["decision"], "deny")

    def test_pre_tool_use_invalid_payload_denied(self) -> None:
        _, out = self.invoke(antigravity_guard.main, "{not json")
        self.assertEqual(out["decision"], "deny")

    def test_outside_root_guard_antigravity(self) -> None:
        inside = str(REPO_ROOT / "AGENTS.md")
        outside = "Z:\\nra_outside_test\\file.txt" if os.name == "nt" else "/nra_outside_test/file.txt"
        # ルート内は通過（ask。自動承認しない）
        _, out = self.invoke(antigravity_outside.main,
                             self.tool_payload("read_file", {"Path": inside}))
        self.assertEqual(out, {"decision": "ask"})
        # ルート外読取は force_ask + 警告文（Always Allow キャッシュを無視）
        _, out = self.invoke(antigravity_outside.main,
                             self.tool_payload("read_file", {"Path": outside}))
        self.assertEqual(out["decision"], "force_ask")
        self.assertIn("CAUTION!!アウトルート_OK!!!!!", out["reason"])
        # ログには共通判定の ask を残す
        lines = pathlib.Path(_outside.LOG_PATH).read_text(encoding="utf-8").splitlines()
        self.assertEqual(json.loads(lines[-1])["host"], "antigravity")
        # ルート外シェルコマンドは force_ask（リポジトリルート基準で ../../ はルート外）
        _, out = self.invoke(antigravity_outside.main, {
            "conversationId": "conv-1",
            "cwd": str(REPO_ROOT),
            "toolCall": {"id": "t1", "name": "run_command", "args": {"CommandLine": "cat ../../outside.txt"}},
        })
        self.assertEqual(out["decision"], "force_ask")
        # 許可リスト書込は deny
        allow_file = str(OUTSIDE_ROOT / "allow_default.txt")
        _, out = self.invoke(antigravity_outside.main,
                             self.tool_payload("write_file", {"Path": allow_file}))
        self.assertEqual(out["decision"], "deny")


if __name__ == "__main__":
    unittest.main()
