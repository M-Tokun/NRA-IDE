"""scripts/push.py の固定経路の試験。本物の git・ゲートは動かさず、模擬の出力で全経路を確かめる。

設計：local_reports/push_route_design_2026-11-13/push_route_design.md（T-2a・T-2b・S1〜S6）
"""
import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import push  # noqa: E402

HEAD = "a" * 40
BASE = "b" * 40


def ctx(outgoing=(HEAD,)):
    return {"plan_id": "x", "is_execution_permission": False,
            "context": {"source_oid": HEAD, "remote_oid": BASE, "outgoing": list(outgoing)}}


def gate_fail(reason):
    return 1, json.dumps({"status": "UNAVAILABLE", "reason": reason}) + "\nerror: failed to push some refs"


class FakeRunner:
    """コマンドの種類ごとに、用意した結果を順に返す。"""

    def __init__(self, **queues):
        self.queues = {k: list(v) for k, v in queues.items()}
        self.calls = []

    def __call__(self, args, timeout, env=None):
        self.calls.append((args, env))
        if args[:2] == ["git", "fetch"]:
            key = "fetch"
        elif "push_gate.py" in " ".join(args):
            key = "prepare"
        elif args[:2] == ["git", "push"]:
            key = "push"
        elif args[:2] == ["git", "rev-parse"]:
            key = "rev_parse"
        elif args[:2] == ["git", "rev-list"]:
            key = "rev_list"
        elif args[:2] == ["git", "diff"]:
            q = self.queues.get("diff")
            return q.pop(0) if q else (0, "")  # 既定：長すぎるパスなし
        elif args[:2] == ["git", "log"]:
            return 0, "subject"
        elif args[:2] == ["git", "branch"]:
            return 0, "master"
        else:
            raise AssertionError(f"unexpected command: {args}")
        q = self.queues.get(key)
        if not q:
            raise AssertionError(f"no prepared result for {key}: {args}")
        return q.pop(0)


class PushRouteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        gate = pathlib.Path(self.tmp.name)
        self.saved = (push.GATE_DIR, push.STATE, push.LOG, push.RUN, push.ROOT)
        push.ROOT = gate
        push.GATE_DIR = gate / "local_reports" / "push_gate"
        push.STATE = push.GATE_DIR / "push_route_state.json"
        push.LOG = push.GATE_DIR / "push_route_log.jsonl"

    def tearDown(self):
        push.GATE_DIR, push.STATE, push.LOG, push.RUN, push.ROOT = self.saved
        self.tmp.cleanup()

    def go(self, runner, *argv):
        push.RUN = runner
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = push.main(list(argv))
        lines = buf.getvalue().strip().splitlines()
        return code, lines[-1], lines

    def reasons(self):
        return [json.loads(l)["reason"] for l in push.LOG.read_text(encoding="utf-8").splitlines()
                if json.loads(l)["result"] in ("STOP", "RETRY")]

    def last_record(self):
        return json.loads(push.LOG.read_text(encoding="utf-8").splitlines()[-1])

    # S1 正常：prepare は 20 で必ず終わり、run で 50 まで進む
    def test_s1_normal(self):
        r = FakeRunner(fetch=[(0, ""), (0, "")], prepare=[(0, json.dumps(ctx()))], push=[(0, "a..b master -> master")],
                       rev_parse=[(0, HEAD)], rev_list=[(0, "0\t0")])
        code, last, lines = self.go(r, "prepare")
        self.assertEqual((code, last), (0, "NEXT 20 Y ASK"))
        self.assertTrue(any(l.startswith("plan: local_reports/push_gate/plan_") for l in lines))
        self.assertTrue(push.STATE.exists())
        code, last, _ = self.go(r, "run")
        self.assertEqual((code, last), (0, "DONE 50"))
        self.assertFalse(push.STATE.exists())
        push_env = [env for args, env in r.calls if args[:2] == ["git", "push"]][0]
        self.assertTrue(push_env["NRA_PUSH_PLAN"].startswith("local_reports"))

    # S2 @10：incoming・送るものなし・fetch 失敗・上限時間
    def test_s2_stop_at_10(self):
        for runner, why in [
            (FakeRunner(fetch=[(0, "")], prepare=[gate_fail("INCOMING_COMMITS_PRESENT")]), "INCOMING_COMMITS_PRESENT"),
            (FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx(outgoing=())))]), "NOTHING_TO_SEND"),
            (FakeRunner(fetch=[(128, "fatal")]), "FETCH_FAILED"),
            (FakeRunner(fetch=[(None, "")]), "TIMEOUT"),
        ]:
            with self.subTest(why=why):
                code, last, _ = self.go(runner, "prepare")
                self.assertEqual((code, last), (1, "STOP 90 @10"))
                self.assertEqual(self.reasons()[-1], why)
                self.assertFalse(push.STATE.exists())

    # S2′ @10：名前・パスが長すぎる（受け取る側の clone で失敗するのを先に止める）
    def test_s2_path_too_long(self):
        long_name = "あ" * 86 + ".md"            # 258 + 3 バイト > 255
        long_path = "d/" * 99 + "abc.md"          # 204 文字 > 200
        ok_name = "あ" * 83 + ".md"               # 252 バイト（上限内）
        for diff_out, want in [(f"note/{long_name}\0", "PATH_TOO_LONG"), (f"{long_path}\0", "PATH_TOO_LONG"),
                               ((1, "fatal"), "DIFF_FAILED")]:
            with self.subTest(want=want, diff=str(diff_out)[:20]):
                result = diff_out if isinstance(diff_out, tuple) else (0, diff_out)
                r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))], diff=[result])
                code, last, _ = self.go(r, "prepare")
                self.assertEqual((code, last), (1, "STOP 90 @10"))
                self.assertEqual(self.reasons()[-1], want)
                self.assertFalse(push.STATE.exists())
        r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))], diff=[(0, f"note/{ok_name}\0")])
        code, last, _ = self.go(r, "prepare")
        self.assertEqual((code, last), (0, "NEXT 20 Y ASK"))

    # S3 @20：提示の直後の入力が git push 以外 → decline。plan は消え、run しても送れない
    def test_s3_declined_at_20(self):
        r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))])
        self.go(r, "prepare")
        code, last, _ = self.go(r, "decline")
        self.assertEqual((code, last), (1, "STOP 90 @20"))
        self.assertEqual(self.reasons()[-1], "DECLINED")
        self.assertFalse(push.STATE.exists())
        code, last, _ = self.go(r, "run")
        self.assertEqual((code, last), (1, "STOP 90 @30"))
        self.assertFalse(any(args[:2] == ["git", "push"] for args, _ in r.calls))

    # 準備した plan がないのに run した（＝提示を経ていない）→ 送らずに止まる
    def test_run_without_prepare(self):
        code, last, _ = self.go(FakeRunner(), "run")
        self.assertEqual((code, last), (1, "STOP 90 @30"))
        self.assertEqual(self.reasons()[-1], "NO_PREPARED_PLAN")

    # S4 @30：ゲートの赤の結果・上限時間・表にない結果。送信状態：ゲートの判定あり＝送っていない、判定なし・TIMEOUT＝不明
    def test_s4_stop_at_30(self):
        for push_result, why, sent in [(gate_fail("MALWARE_OR_UNICODE_BLOCKED"), "MALWARE_OR_UNICODE_BLOCKED", "NOT_STARTED"),
                                       (gate_fail("SOMETHING_NEW_IN_FUTURE"), "SOMETHING_NEW_IN_FUTURE", "NOT_STARTED"),
                                       ((None, ""), "TIMEOUT", "UNKNOWN"),
                                       ((1, "no json at all"), "PUSH_FAILED", "UNKNOWN")]:
            with self.subTest(why=why):
                r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))], push=[push_result])
                self.go(r, "prepare")
                code, last, _ = self.go(r, "run")
                self.assertEqual((code, last), (1, "STOP 90 @30"))
                self.assertEqual(self.reasons()[-1], why)
                self.assertEqual(self.last_record()["send_state"], sent)

    # S5 時刻差：10 へ戻らず、すべて STOP 90 @30（2026-11-13 利用者決定：戻りの廃止）。prepare からやり直す
    def test_s5_time_difference_stops_without_return(self):
        for reason in ("PLAN_OR_RULES_CHANGED", "FETCH_EVIDENCE_MISSING"):
            with self.subTest(reason=reason):
                r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))], push=[gate_fail(reason)])
                self.go(r, "prepare")
                code, last, _ = self.go(r, "run")
                self.assertEqual((code, last), (1, "STOP 90 @30"))
                self.assertEqual(self.reasons()[-1], reason)
                self.assertEqual(self.last_record()["send_state"], "NOT_STARTED")
                self.assertFalse(push.STATE.exists())
                self.assertEqual(sum(1 for args, _ in r.calls if args[:2] == ["git", "fetch"]), 1)  # 10 へ戻っていない
                self.assertEqual(sum(1 for args, _ in r.calls if args[:2] == ["git", "push"]), 1)

    # S5′ 停止後に run をもう一度呼んでも、送らない（自動再開しない）
    def test_s5_run_after_stop_does_not_resend(self):
        r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))], push=[gate_fail("PLAN_OR_RULES_CHANGED")])
        self.go(r, "prepare")
        self.go(r, "run")
        code, last, _ = self.go(r, "run")
        self.assertEqual((code, last), (1, "STOP 90 @30"))
        self.assertEqual(self.reasons()[-1], "NO_PREPARED_PLAN")
        self.assertEqual(sum(1 for args, _ in r.calls if args[:2] == ["git", "push"]), 1)

    # S6 @40：送信後の照合が不一致（送信済み）
    def test_s6_mismatch_after_send(self):
        r = FakeRunner(fetch=[(0, ""), (0, "")], prepare=[(0, json.dumps(ctx()))], push=[(0, "ok")],
                       rev_parse=[(0, BASE)], rev_list=[(0, "1\t0")])
        self.go(r, "prepare")
        code, last, _ = self.go(r, "run")
        self.assertEqual((code, last), (1, "STOP 90 @40"))
        self.assertEqual(self.reasons()[-1], "MISMATCH")
        self.assertEqual(self.last_record()["send_state"], "COMMAND_SUCCEEDED_UNVERIFIED")

    # S6′ @40：照合の観測コマンド自体の失敗は、不一致と区別して止まる（終了コードを明示的に確認）
    def test_s6_observation_failure_is_not_a_match(self):
        for rev_parse, rev_list, want in [((128, "fatal: bad revision"), (0, "0\t0"), "OBSERVE_FAILED"),
                                          ((0, HEAD), (128, "fatal"), "OBSERVE_FAILED"),
                                          ((None, ""), (0, "0\t0"), "TIMEOUT"),
                                          ((0, HEAD), (None, ""), "TIMEOUT")]:
            with self.subTest(want=want, rev_parse=rev_parse[0], rev_list=rev_list[0]):
                r = FakeRunner(fetch=[(0, ""), (0, "")], prepare=[(0, json.dumps(ctx()))], push=[(0, "ok")],
                               rev_parse=[rev_parse], rev_list=[rev_list])
                self.go(r, "prepare")
                code, last, _ = self.go(r, "run")
                self.assertEqual((code, last), (1, "STOP 90 @40"))
                self.assertEqual(self.reasons()[-1], want)
                self.assertEqual(self.last_record()["send_state"], "COMMAND_SUCCEEDED_UNVERIFIED")

    # 完了時の送信状態は VERIFIED
    def test_done_records_verified(self):
        r = FakeRunner(fetch=[(0, ""), (0, "")], prepare=[(0, json.dumps(ctx()))], push=[(0, "ok")],
                       rev_parse=[(0, HEAD)], rev_list=[(0, "0\t0")])
        self.go(r, "prepare")
        self.go(r, "run")
        self.assertEqual(self.last_record()["send_state"], "VERIFIED")

    # 出力の最後の行は、決まった3種類だけ
    def test_last_line_vocabulary(self):
        allowed = {"NEXT 20 Y ASK", "DONE 50"} | {f"STOP 90 @{n}" for n in (10, 20, 30, 40)}
        r = FakeRunner(fetch=[(0, "")], prepare=[(0, json.dumps(ctx()))])
        _, last, _ = self.go(r, "prepare")
        self.assertIn(last, allowed)


if __name__ == "__main__":
    unittest.main()
