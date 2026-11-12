"""push の入口（固定経路）。設計：local_reports/push_route_design_2026-11-13/push_route_design.md

  python -B scripts/push.py prepare   10 PLAN → 20 ASK（提示して必ず終わる）
  python -B scripts/push.py run       30 PUSH → 40 VERIFY → 50 DONE（提示の直後の利用者の入力が git push のとき）
  python -B scripts/push.py decline   提示の直後の利用者の入力が git push 以外のとき（STOP 90 @20）

最後の1行だけを読む。言い換えない。
  NEXT 20 Y ASK      提示した。利用者の入力が git push なら run へ
  STOP 90 @<番号>    止まった。番号で場所が分かる（@40 だけ送信済み）
  DONE 50            完了

分岐は2つだけ：20 の利用者の入力（git push か、それ以外か）と、30 の時刻差による戻り（10 へ1回まで）。
それ以外の結果はすべて STOP 90。細かい理由は記録（local_reports/push_gate/push_route_log.jsonl）に残し、後から追う。

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
RETRY_REASONS = {"PLAN_OR_RULES_CHANGED", "FETCH_EVIDENCE_MISSING"}  # 時刻差：10 へ1回だけ戻る
TIMEOUT = {"10": 240, "30": 600, "40": 60}  # 案（設計案 U-6：実測して決める）
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


def _log(step, result, reason=""):
    GATE_DIR.mkdir(parents=True, exist_ok=True)
    rec = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
           "step": step, "result": result, "reason": reason}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def _stop(step, reason):
    _log(step, "STOP", reason)
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


# ---- 10 PLAN ----------------------------------------------------------------
def step10(remote, branch, retries):
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
    STATE.write_text(json.dumps({"plan": plan.relative_to(ROOT).as_posix(), "remote": remote, "branch": branch,
                                 "head": ctx["source_oid"], "retries": retries}, ensure_ascii=False),
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
        return _stop("30", "TIMEOUT")
    if code != 0:
        reason = _json_in(out).get("reason", "PUSH_FAILED")
        if reason in RETRY_REASONS and st.get("retries", 0) == 0:
            _log("30", "RETRY", reason)
            return step10(st["remote"], st["branch"], retries=1)  # 毎回再提示（20 で止まる）
        return _stop("30", reason)
    _log("30", "PASS")
    return step40(st)


def step40(st):
    code, _ = _git(["fetch", "--quiet", st["remote"]], TIMEOUT["40"])
    if code != 0:
        return _stop("40", "TIMEOUT" if code is None else "FETCH_FAILED")
    _, remote_oid = _git(["rev-parse", f"{st['remote']}/{st['branch']}"], TIMEOUT["40"])
    _, counts = _git(["rev-list", "--left-right", "--count", f"{st['remote']}/{st['branch']}...HEAD"], TIMEOUT["40"])
    if remote_oid != st["head"] or counts.split() != ["0", "0"]:
        return _stop("40", "MISMATCH")
    _log("40", "VERIFY")
    STATE.unlink()
    _log("50", "DONE")
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
    return step10(args.remote, branch, retries=0)


if __name__ == "__main__":
    sys.exit(main())
