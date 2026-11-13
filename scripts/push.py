"""push の入口（固定経路）。設計：local_reports/push_route_design_2026-11-13/push_route_design.md

  python -B scripts/push.py prepare   10 PLAN → 20 ASK（提示して必ず終わる）
  python -B scripts/push.py run       30 PUSH → 40 VERIFY → 50 DONE（提示の直後の利用者の入力が git push のとき）
  python -B scripts/push.py decline   提示の直後の利用者の入力が git push 以外のとき（STOP 90 @20）

最後の1行だけを読む。言い換えない。
  NEXT 20 Y ASK      提示した。利用者の入力が git push なら run へ
  STOP 90 @<番号>    止まった。番号で場所が分かる（@40 は送信済み、@30 の TIMEOUT は不明）
  DONE 50            完了

分岐は1つだけ：20 の利用者の入力（git push か、それ以外か）。30 の時刻差を含め、それ以外の結果はすべて STOP 90。
STOP 90 の後に 10 へ自動で戻らない。やり直すときは、利用者の新しい入力で prepare から始める。
細かい理由と送信状態（send_state）は記録（local_reports/push_gate/push_route_log.jsonl）に残し、後から追う。
send_state：NOT_STARTED（送っていない）／UNKNOWN（送ったか不明）／COMMAND_SUCCEEDED_UNVERIFIED（push は成功、照合前）／VERIFIED。

この入口は push を許可する仕組みではない。利用者の確認（git push の入力）を機械的に確かめるのは段階2。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GATE_DIR = ROOT / "local_reports" / "push_gate"
STATE = GATE_DIR / "push_route_state.json"
LOG = GATE_DIR / "push_route_log.jsonl"
TIMEOUT = {"10": 240, "30": 600, "40": 60}  # 案（設計案 U-6：実測して決める）
# 名前・パスの長さの上限。送る側では通っても、受け取る側の clone で失敗するのを先に止める。
MAX_NAME_BYTES = 255   # 名前1つの UTF-8 バイト数（Linux・macOS のファイルシステムの上限）
MAX_PATH_CHARS = 200   # リポジトリ内パスの文字数（clone 先が60文字までなら Windows の260文字に収まる）
PREPARE_TIMEOUT_SECONDS = 180


def _run(args, timeout, env=None):
    """(終了コード, 出力) を返す。上限時間を超えたら終了コード None。"""
    try:
        done = subprocess.run(args, cwd=ROOT, capture_output=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None, ""
    text = (done.stdout or b"").decode("utf-8", "replace") + (done.stderr or b"").decode("utf-8", "replace")
    return done.returncode, text


RUN = _run  # 試験で差し替える


def _log(step, result, reason="", detail="", send_state="NOT_STARTED"):
    GATE_DIR.mkdir(parents=True, exist_ok=True)
    rec = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "step": step, "result": result, "reason": reason, "send_state": send_state}
    if detail:
        rec["detail"] = detail
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _stop(step, reason, detail="", send_state="NOT_STARTED"):
    _log(step, "STOP", reason, detail, send_state)
    if STATE.exists():
        STATE.unlink()
    print(f"STOP 90 @{step}")
    return 1


def _json_in(text):
    """出力の中の最初の { から最後の } までを JSON として読む。読めなければ {}。"""
    i, j = text.find("{"), text.rfind("}")
    if i < 0 or j < i:
        return {}
    try:
        return json.loads(text[i:j + 1])
    except ValueError:
        return {}


def _git(args, timeout):
    code, out = RUN(["git", *args], timeout)
    return code, out.strip()


def _new_plan_path():
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = GATE_DIR / f"plan_{stamp}.json"
    n = 2
    while path.exists():
        path = GATE_DIR / f"plan_{stamp}_{n}.json"
        n += 1
    return path


def _too_long_path(base, head):
    """送信範囲で追加・変更・名前変更されたパスのうち、上限を超える最初のものを返す。なければ ""。"""
    code, out = RUN(["git", "diff", "--name-only", "--diff-filter=AMR", "-z", base, head], TIMEOUT["10"])
    if code != 0:
        return "DIFF_FAILED"
    for path in (p for p in out.split("\0") if p.strip()):
        name = path.rsplit("/", 1)[-1]
        if len(name.encode("utf-8")) > MAX_NAME_BYTES or len(path) > MAX_PATH_CHARS:
            return path
    return ""


# ---- 10 PLAN ----------------------------------------------------------------
def step10(remote, branch):
    code, _ = _git(["fetch", "--quiet", remote], TIMEOUT["10"])
    if code != 0:
        return _stop("10", "TIMEOUT" if code is None else "FETCH_FAILED")
    plan = _new_plan_path()
    GATE_DIR.mkdir(parents=True, exist_ok=True)
    code, out = RUN([sys.executable, "-B", "scripts/push_gate.py", "prepare", "--remote", remote,
                     "--branch", f"refs/heads/{branch}", "--output", plan.relative_to(ROOT).as_posix(),
                     "--timeout-seconds", str(PREPARE_TIMEOUT_SECONDS)], TIMEOUT["10"])
    if code is None:
        return _stop("10", "TIMEOUT")
    data = _json_in(out)
    if code != 0 or "context" not in data:
        return _stop("10", data.get("reason", "PREPARATION_FAILED"))
    ctx = data["context"]
    if not ctx.get("outgoing"):
        return _stop("10", "NOTHING_TO_SEND")
    too_long = _too_long_path(ctx.get("base_oid") or ctx["remote_oid"], ctx["source_oid"])
    if too_long == "DIFF_FAILED":
        return _stop("10", "DIFF_FAILED")
    if too_long:
        return _stop("10", "PATH_TOO_LONG", too_long)
    STATE.write_text(json.dumps({"plan": plan.relative_to(ROOT).as_posix(), "remote": remote, "branch": branch,
                                 "head": ctx["source_oid"]}, ensure_ascii=False),
                     encoding="utf-8")
    _log("10", "PLAN", plan.name)
    return step20(remote, branch, ctx, plan)


# ---- 20 ASK -----------------------------------------------------------------
def step20(remote, branch, ctx, plan):
    print(f"送信先: {remote} refs/heads/{branch}")
    print(f"HEAD: {ctx['source_oid']}")
    print(f"送信先の現在: {ctx['remote_oid']}")
    print(f"送信コミット（{len(ctx['outgoing'])}件、古い順）:")
    for oid in ctx["outgoing"]:
        _, subject = _git(["log", "-1", "--format=%s", oid], TIMEOUT["10"])
        print(f"  {oid} {subject}")
    print("incoming: 0")
    print(f"plan: {plan.relative_to(ROOT).as_posix()}")
    _log("20", "ASK", plan.name)
    print("NEXT 20 Y ASK")
    return 0


# ---- 30 PUSH → 40 VERIFY → 50 DONE -------------------------------------------
def run():
    if not STATE.exists():
        return _stop("30", "NO_PREPARED_PLAN")
    st = json.loads(STATE.read_text(encoding="utf-8"))
    env = dict(os.environ, NRA_PUSH_PLAN=st["plan"])
    code, out = RUN(["git", "push", "--no-progress", st["remote"], st["branch"]], TIMEOUT["30"], env=env)
    if code is None:
        return _stop("30", "TIMEOUT", send_state="UNKNOWN")  # 送ったか不明
    if code != 0:
        # ゲートの判定（JSON の reason）があれば送る前の拒否。判定がなければ、送ったか確定できない。
        reason = _json_in(out).get("reason")
        if reason:
            return _stop("30", reason)  # 時刻差（PLAN_OR_RULES_CHANGED 等）も含め、10 へは戻らない
        return _stop("30", "PUSH_FAILED", send_state="UNKNOWN")
    _log("30", "PASS", send_state="COMMAND_SUCCEEDED_UNVERIFIED")
    return step40(st)


def step40(st):
    sent = "COMMAND_SUCCEEDED_UNVERIFIED"
    code, _ = _git(["fetch", "--quiet", st["remote"]], TIMEOUT["40"])
    if code != 0:
        return _stop("40", "TIMEOUT" if code is None else "FETCH_FAILED", send_state=sent)
    ref = f"{st['remote']}/{st['branch']}"
    code, remote_oid = _git(["rev-parse", ref], TIMEOUT["40"])
    if code != 0:
        return _stop("40", "TIMEOUT" if code is None else "OBSERVE_FAILED", send_state=sent)
    code, counts = _git(["rev-list", "--left-right", "--count", f"{ref}...HEAD"], TIMEOUT["40"])
    if code != 0:
        return _stop("40", "TIMEOUT" if code is None else "OBSERVE_FAILED", send_state=sent)
    if remote_oid != st["head"] or counts.split() != ["0", "0"]:
        return _stop("40", "MISMATCH", send_state=sent)
    _log("40", "VERIFY", send_state="VERIFIED")
    STATE.unlink()
    _log("50", "DONE", send_state="VERIFIED")
    print("DONE 50")
    return 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows のパイプ出力（cp932）で日本語が化けないように
    parser = argparse.ArgumentParser(description="push の入口（固定経路）")
    parser.add_argument("stage", choices=["prepare", "run", "decline"])
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--branch", default=None, help="既定は現在のブランチ")
    args = parser.parse_args(argv)
    if args.stage == "run":
        return run()
    if args.stage == "decline":
        return _stop("20", "DECLINED")
    branch = args.branch
    if not branch:
        code, branch = _git(["branch", "--show-current"], TIMEOUT["10"])
        if code != 0 or not branch:
            return _stop("10", "NO_CURRENT_BRANCH")
    return step10(args.remote, branch)


if __name__ == "__main__":
    sys.exit(main())
