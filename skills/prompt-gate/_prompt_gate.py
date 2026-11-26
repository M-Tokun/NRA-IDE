"""prompt_gate の共通判定（ホスト共通）。各ホストの hook は薄いラッパーで、これを呼ぶ。

AGENTS.md §7「合言葉の完全一致」を機械で判定する。AI は判定しない。
経路（番号はこのファイル内だけ）:

  10 入力の前後の空白（半角・全角。改行・タブを含む）を除く。GOTO 20
  20 IF 入力 == "git push" AND push 計画が保留中: 承認（push・plan）を書き、PUSH_RUN を注入。GOTO 99
  30 IF 入力 == "git push": 残りの承認を消し、PUSH_PREPARE を注入。GOTO 99
  40 IF 入力が ^commit[ 　]?まで$ に一致: 承認（commit）を書き、COMMIT_RUN を注入。GOTO 99
  50 IF push 計画が保留中: push.py decline を実行（状態を消し DECLINED を記録）。GOTO 60
  60 IF 入力に commit または push を含む（大小を区別しない）: NOT_EXACT を注入。GOTO 70
  70 残っている承認をすべて消す。GOTO 99
  99 終了。入力は止めない（承認の発行・取消と文脈の注入だけ）

判定結果 decide() は副作用のない関数。apply() が承認の書込み・消去と decline を行う。
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import approval  # noqa: E402

PUSH_STATE = ROOT / "local_reports" / "push_gate" / "push_route_state.json"
STRIP = " 　\t\r\n"
COMMIT_RE = re.compile(r"commit[ 　]?まで")

CONTEXT = {
    "PUSH_RUN": "prompt_gate: PUSH_RUN — 入力は「git push」と完全一致し、承認（push）を書いた。AGENTS.md 55 により scripts/push.py run を呼ぶ。",
    "PUSH_PREPARE": "prompt_gate: PUSH_PREPARE — 入力は「git push」と完全一致した。保留中の push 計画はない。AGENTS.md 57 の prepare の対象。",
    "COMMIT_RUN": "prompt_gate: COMMIT_RUN — 入力は「commit まで」と完全一致し、承認（commit）を書いた。AGENTS.md 58・59 で commit する。",
    "NOT_EXACT": "prompt_gate: NOT_EXACT — 入力は commit・push を含むが合言葉と完全一致しない。「完全一致していません」と返し、commit・push を実行しない。",
    "PUSH_DECLINED": "prompt_gate: PUSH_DECLINED — 保留中の push 計画を取り消した（push.py decline）。",
}


def normalize(prompt: str) -> str:
    return prompt.strip(STRIP)


def pending_plan() -> str:
    """保留中の push 計画のパス。なければ ""。"""
    try:
        return json.loads(PUSH_STATE.read_text(encoding="utf-8")).get("plan", "")
    except (OSError, ValueError):
        return ""


def decide(prompt: str, plan: str) -> dict:
    """入力と保留中の計画から、行う処理を決める（副作用なし）。

    戻り値: {"line": 経路番号, "write": 承認の種類 or "", "decline": bool, "clear": bool, "context": [語…]}
    """
    text = normalize(prompt)
    if text == "git push" and plan:
        return {"line": 20, "write": "push", "decline": False, "clear": False, "context": ["PUSH_RUN"]}
    if text == "git push":
        return {"line": 30, "write": "", "decline": False, "clear": True, "context": ["PUSH_PREPARE"]}
    if COMMIT_RE.fullmatch(text):
        return {"line": 40, "write": "commit", "decline": False, "clear": False, "context": ["COMMIT_RUN"]}
    context = []
    decline = bool(plan)
    if decline:
        context.append("PUSH_DECLINED")
    low = text.lower()
    if "commit" in low or "push" in low:
        context.append("NOT_EXACT")
    return {"line": 70, "write": "", "decline": decline, "clear": True, "context": context}


def _decline() -> None:
    subprocess.run([sys.executable, "-B", "scripts/push.py", "decline"], cwd=ROOT,
                   capture_output=True, timeout=8)


def apply(prompt: str) -> str:
    """判定して承認の書込み・消去・decline を行い、注入する文脈を返す。"""
    plan = pending_plan()
    result = decide(prompt, plan)
    if result["decline"]:
        _decline()
    if result["write"] == "push":
        approval.write("push", plan=plan)
    elif result["write"] == "commit":
        approval.write("commit")
    elif result["clear"]:
        approval.clear_all()
    return "\n".join(CONTEXT[word] for word in result["context"])
