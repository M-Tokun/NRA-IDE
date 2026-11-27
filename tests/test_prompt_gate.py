"""skills/prompt-gate（合言葉の機械判定）と scripts/approval.py の試験。実リポジトリの承認ファイルには触れない。"""
from __future__ import annotations

import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "skills" / "prompt-gate"))
sys.path.insert(0, str(ROOT / "scripts"))
import _prompt_gate  # noqa: E402
import approval  # noqa: E402
import antigravity_prompt_gate  # noqa: E402
import claude_prompt_gate  # noqa: E402
import cline_prompt_gate  # noqa: E402
import gemini_prompt_gate  # noqa: E402


class DecideTest(unittest.TestCase):
    def check(self, prompt, plan, line, write, decline, context):
        r = _prompt_gate.decide(prompt, plan)
        self.assertEqual((r["line"], r["write"], r["decline"], r["context"]), (line, write, decline, context), prompt)

    def test_git_push_with_plan(self):
        self.check("git push", "p.json", 20, "push", False, ["PUSH_RUN"])

    def test_git_push_with_surrounding_spaces(self):
        self.check(" 　git push　\n", "p.json", 20, "push", False, ["PUSH_RUN"])

    def test_git_push_without_plan(self):
        self.check("git push", "", 30, "", False, ["PUSH_PREPARE"])

    def test_commit_made_forms(self):
        for text in ("commit まで", "commitまで", "commit　まで", "  commit まで  "):
            self.check(text, "", 40, "commit", False, ["COMMIT_RUN"])

    def test_commit_made_with_plan_does_not_decline_silently(self):
        # 「commit まで」は push の承認ではない。計画は残すが push 承認は書かない
        self.check("commit まで", "p.json", 40, "commit", False, ["COMMIT_RUN"])

    def test_not_exact(self):
        for text in ("commit  まで", "commitして下さい", "git push origin", "Git Push", "pushして"):
            self.check(text, "", 70, "", False, ["NOT_EXACT"])

    def test_other_input_with_plan_declines(self):
        self.check("こんにちは", "p.json", 70, "", True, ["PUSH_DECLINED"])
        self.check("pushして", "p.json", 70, "", True, ["PUSH_DECLINED", "NOT_EXACT"])

    def test_other_input_without_plan(self):
        self.check("こんにちは", "", 70, "", False, [])


class ApplyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = pathlib.Path(self.tmp.name)
        self.saved = (approval.APPROVAL_DIR, _prompt_gate.PUSH_STATE, _prompt_gate._decline,
                      cline_prompt_gate.LOG_PATH, gemini_prompt_gate.LOG_PATH,
                      antigravity_prompt_gate.LOG_PATH)
        cline_prompt_gate.LOG_PATH = base / "hooks" / "prompt_gate_cline.jsonl"
        gemini_prompt_gate.LOG_PATH = base / "hooks" / "prompt_gate_gemini.jsonl"
        antigravity_prompt_gate.LOG_PATH = base / "hooks" / "prompt_gate_antigravity.jsonl"
        approval.APPROVAL_DIR = base / "approvals"
        _prompt_gate.PUSH_STATE = base / "push_route_state.json"
        self.declined = []
        _prompt_gate._decline = lambda: (self.declined.append(1), _prompt_gate.PUSH_STATE.unlink(missing_ok=True))

    def tearDown(self):
        (approval.APPROVAL_DIR, _prompt_gate.PUSH_STATE, _prompt_gate._decline,
         cline_prompt_gate.LOG_PATH, gemini_prompt_gate.LOG_PATH,
         antigravity_prompt_gate.LOG_PATH) = self.saved
        self.tmp.cleanup()

    def files(self):
        d = approval.APPROVAL_DIR
        return sorted(p.name for p in d.iterdir()) if d.exists() else []

    def plan(self, path="local_reports/push_gate/plan_x.json"):
        _prompt_gate.PUSH_STATE.write_text(json.dumps({"plan": path}), encoding="utf-8")

    def test_push_approval_carries_plan_and_is_single_use(self):
        self.plan()
        _prompt_gate.apply("git push")
        self.assertEqual(self.files(), ["push.json"])
        self.assertEqual(approval.consume("push", plan="local_reports/push_gate/plan_x.json"), "")
        self.assertEqual(approval.consume("push", plan="local_reports/push_gate/plan_x.json"), "NO_APPROVAL")

    def test_plan_mismatch_is_rejected_and_consumed(self):
        self.plan("a.json")
        _prompt_gate.apply("git push")
        self.assertEqual(approval.consume("push", plan="b.json"), "APPROVAL_MISMATCH")
        self.assertEqual(self.files(), [])

    def test_other_input_clears_approvals_and_declines(self):
        self.plan()
        _prompt_gate.apply("commit まで")
        self.assertEqual(self.files(), ["commit.json"])
        context = _prompt_gate.apply("ありがとう")
        self.assertEqual(self.files(), [])
        self.assertEqual(self.declined, [1])
        self.assertIn("PUSH_DECLINED", context)

    def test_commit_then_push_keeps_only_latest(self):
        _prompt_gate.apply("commit まで")
        self.plan()
        _prompt_gate.apply("git push")
        self.assertEqual(self.files(), ["push.json"])

    def test_claude_wrapper_output_and_invalid_input(self):
        out = io.StringIO()
        sys.stdin = io.StringIO(json.dumps({"prompt": "commit まで"}))
        try:
            with contextlib.redirect_stdout(out):
                self.assertEqual(claude_prompt_gate.main(), 0)
        finally:
            sys.stdin = sys.__stdin__
        data = json.loads(out.getvalue())
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("COMMIT_RUN", data["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(self.files(), ["commit.json"])
        sys.stdin = io.StringIO("not json")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(claude_prompt_gate.main(), 0)
        finally:
            sys.stdin = sys.__stdin__
        self.assertEqual(self.files(), [])

    def test_claude_wrapper_reads_utf8_bytes(self):
        # 実機（Windows）では標準入力の既定が cp932。hook の入力は UTF-8 のバイト列で届く
        class Bytes:
            buffer = io.BytesIO(json.dumps({"prompt": "commitまで"}, ensure_ascii=False).encode("utf-8"))
        sys.stdin = Bytes()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(claude_prompt_gate.main(), 0)
        finally:
            sys.stdin = sys.__stdin__
        self.assertEqual(self.files(), ["commit.json"])

    def run_cline(self, stdin):
        out = io.StringIO()
        sys.stdin = stdin
        try:
            with contextlib.redirect_stdout(out):
                self.assertEqual(cline_prompt_gate.main(), 0)
        finally:
            sys.stdin = sys.__stdin__
        return json.loads(out.getvalue())

    def test_cline_wrapper_flat_and_nested_input(self):
        for payload in ({"prompt": "commit まで"}, {"taskId": "t", "userPromptSubmit": {"prompt": "commit まで"}}):
            approval.clear_all()
            data = self.run_cline(io.StringIO(json.dumps(payload)))
            self.assertEqual(data["cancel"], False)
            self.assertEqual(data["errorMessage"], "")
            self.assertIn("COMMIT_RUN", data["contextModification"])
            self.assertEqual(self.files(), ["commit.json"])

    def test_cline_wrapper_not_exact_and_other_input(self):
        self.run_cline(io.StringIO(json.dumps({"userPromptSubmit": {"prompt": "commit まで"}})))
        data = self.run_cline(io.StringIO(json.dumps({"userPromptSubmit": {"prompt": "commitして"}})))
        self.assertIn("NOT_EXACT", data["contextModification"])
        self.assertEqual(self.files(), [])

    def test_cline_wrapper_unreadable_input_clears_and_reports(self):
        approval.write("commit")
        for stdin in (io.StringIO("not json"), io.StringIO(json.dumps({"userPromptSubmit": {"prompt": 1}})),
                      io.StringIO(json.dumps({"other": "commit まで"}))):
            approval.write("commit")
            data = self.run_cline(stdin)
            self.assertEqual(data["cancel"], False)
            self.assertEqual(data["contextModification"], "")
            self.assertNotEqual(data["errorMessage"], "")
            self.assertEqual(self.files(), [])

    def test_cline_unwraps_user_input_tag(self):
        # 実機（Cline 4.1.22）の形：<user_input mode="act">commitまで</user_input>
        for mode in ("act", "plan"):
            approval.clear_all()
            prompt = f'<user_input mode="{mode}">commitまで</user_input>'
            data = self.run_cline(io.StringIO(json.dumps({"userPromptSubmit": {"prompt": prompt}})))
            self.assertIn("COMMIT_RUN", data["contextModification"])
            self.assertEqual(self.files(), ["commit.json"])

    def test_cline_unwrap_only_whole_wrapper(self):
        f = cline_prompt_gate.unwrap
        self.assertEqual(f('<user_input mode="act">commit まで</user_input>'), "commit まで")
        self.assertEqual(f('<user_input mode="act">x</user_input>'), "x")
        for raw in ('<user_input mode="other">commit まで</user_input>',
                    'commit まで<user_input mode="act">y</user_input>',
                    '<user_input mode="act">commit まで</user_input> 追記'):
            self.assertEqual(f(raw), raw)
            self.assertNotEqual(_prompt_gate.decide(f(raw), "")["write"], "commit")

    def test_cline_wrapper_logs_shape_without_prompt_text(self):
        self.run_cline(io.StringIO(json.dumps({"taskId": "t", "userPromptSubmit": {"prompt": "秘密の本文 commit まで"}})))
        self.run_cline(io.StringIO(json.dumps({"other": "x"})))
        lines = [json.loads(line) for line in cline_prompt_gate.LOG_PATH.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([r["result"] for r in lines], ["OK", "UNREADABLE"])
        self.assertEqual(lines[0]["shape"], {"taskId": "str", "userPromptSubmit": {"prompt": "str"}})
        self.assertEqual(lines[1]["shape"], {"other": "str"})
        self.assertNotIn("秘密の本文", cline_prompt_gate.LOG_PATH.read_text(encoding="utf-8"))

    def test_cline_wrapper_reads_utf8_bytes(self):
        class Bytes:
            buffer = io.BytesIO(json.dumps({"userPromptSubmit": {"prompt": "commitまで"}},
                                           ensure_ascii=False).encode("utf-8"))
        data = self.run_cline(Bytes())
        self.assertIn("COMMIT_RUN", data["contextModification"])
        self.assertEqual(self.files(), ["commit.json"])

    def run_gemini(self, stdin):
        out = io.StringIO()
        sys.stdin = stdin
        try:
            with contextlib.redirect_stdout(out):
                self.assertEqual(gemini_prompt_gate.main(), 0)
        finally:
            sys.stdin = sys.__stdin__
        return json.loads(out.getvalue())

    def test_gemini_wrapper_commit_and_not_exact_and_ordinary(self):
        data = self.run_gemini(io.StringIO(json.dumps({"prompt": "commit まで"})))
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "BeforeAgent")
        self.assertIn("COMMIT_RUN", data["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(self.files(), ["commit.json"])
        data = self.run_gemini(io.StringIO(json.dumps({"prompt": "commitして"})))
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "BeforeAgent")
        self.assertIn("NOT_EXACT", data["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(self.files(), [])
        data = self.run_gemini(io.StringIO(json.dumps({"prompt": "こんにちは"})))
        self.assertEqual(data, {})
        self.assertEqual(self.files(), [])

    def test_gemini_wrapper_unreadable_input_clears_and_returns_empty(self):
        for stdin in (io.StringIO("not json"), io.StringIO(json.dumps({"prompt": 1})),
                      io.StringIO(json.dumps({"other": "commit まで"}))):
            approval.write("commit")
            data = self.run_gemini(stdin)
            self.assertEqual(data, {})
            self.assertEqual(self.files(), [])

    def test_gemini_wrapper_logs_shape_without_prompt_text(self):
        self.run_gemini(io.StringIO(json.dumps({"session_id": "g1", "prompt": "秘密の本文 commit まで"})))
        self.run_gemini(io.StringIO(json.dumps({"other": "x"})))
        raw_log = gemini_prompt_gate.LOG_PATH.read_text(encoding="utf-8")
        lines = [json.loads(line) for line in raw_log.splitlines()]
        self.assertEqual([r["result"] for r in lines], ["OK", "UNREADABLE"])
        self.assertEqual(lines[0]["shape"], {"session_id": "str", "prompt": "str"})
        self.assertEqual(lines[1]["shape"], {"other": "str"})
        self.assertNotIn("秘密の本文", raw_log)

    def test_gemini_wrapper_reads_utf8_bytes(self):
        class Bytes:
            buffer = io.BytesIO(json.dumps({"prompt": "commitまで"}, ensure_ascii=False).encode("utf-8"))
        data = self.run_gemini(Bytes())
        self.assertEqual(data["hookSpecificOutput"]["hookEventName"], "BeforeAgent")
        self.assertIn("COMMIT_RUN", data["hookSpecificOutput"]["additionalContext"])
        self.assertEqual(self.files(), ["commit.json"])

    def run_antigravity(self, stdin):
        out = io.StringIO()
        sys.stdin = stdin
        try:
            with contextlib.redirect_stdout(out):
                self.assertEqual(antigravity_prompt_gate.main(), 0)
        finally:
            sys.stdin = sys.__stdin__
        return json.loads(out.getvalue())

    def test_antigravity_wrapper_commit_reinvocation_and_ordinary(self):
        # invocationNum == 0（実機確認済みの0起点）で承認を発行
        data = self.run_antigravity(io.StringIO(json.dumps({"invocationNum": 0, "lastUserInput": "commit まで"})))
        self.assertIn("COMMIT_RUN", data["injectSteps"][0]["systemMessage"]["systemMessage"])
        self.assertEqual(self.files(), ["commit.json"])
        # 承認を消費した後、同一ターン内の再呼び出し（invocationNum == 1）では再発行しない
        self.assertEqual(approval.consume("commit"), "")
        self.assertEqual(self.files(), [])
        data = self.run_antigravity(io.StringIO(json.dumps({"invocationNum": 1, "lastUserInput": "commit まで"})))
        self.assertEqual(data, {})
        self.assertEqual(self.files(), [])
        # 不一致・通常入力
        data = self.run_antigravity(io.StringIO(json.dumps({"invocationNum": 0, "lastUserInput": "commitして"})))
        self.assertIn("NOT_EXACT", data["injectSteps"][0]["systemMessage"]["systemMessage"])
        self.assertEqual(self.files(), [])
        data = self.run_antigravity(io.StringIO(json.dumps({"invocationNum": 0, "lastUserInput": "こんにちは"})))
        self.assertEqual(data, {})
        self.assertEqual(self.files(), [])

    def test_antigravity_wrapper_unreadable_input_clears_and_returns_empty(self):
        for stdin in (io.StringIO("not json"), io.StringIO(json.dumps({"invocationNum": 0})),
                      io.StringIO(json.dumps({"lastUserInput": "commit まで"}))):
            approval.write("commit")
            data = self.run_antigravity(stdin)
            self.assertEqual(data, {})
            self.assertEqual(self.files(), [])

    def test_antigravity_wrapper_logs_shape_without_prompt_text(self):
        self.run_antigravity(io.StringIO(json.dumps(
            {"conversationId": "c1", "invocationNum": 0, "lastUserInput": "秘密の本文 commit まで"})))
        self.run_antigravity(io.StringIO(json.dumps(
            {"conversationId": "c1", "invocationNum": 1, "lastUserInput": "秘密の本文 commit まで"})))
        self.run_antigravity(io.StringIO(json.dumps({"other": "x"})))
        raw_log = antigravity_prompt_gate.LOG_PATH.read_text(encoding="utf-8")
        lines = [json.loads(line) for line in raw_log.splitlines()]
        self.assertEqual([r["result"] for r in lines], ["OK", "SKIP_REINVOCATION", "UNREADABLE"])
        self.assertEqual(lines[0]["invocation_num"], 0)
        self.assertEqual(lines[1]["invocation_num"], 1)
        self.assertNotIn("秘密の本文", raw_log)

    def test_antigravity_wrapper_reads_utf8_bytes(self):
        class Bytes:
            buffer = io.BytesIO(json.dumps(
                {"invocationNum": 0, "lastUserInput": "commitまで"}, ensure_ascii=False).encode("utf-8"))
        data = self.run_antigravity(Bytes())
        self.assertIn("COMMIT_RUN", data["injectSteps"][0]["systemMessage"]["systemMessage"])
        self.assertEqual(self.files(), ["commit.json"])


if __name__ == "__main__":
    unittest.main()
