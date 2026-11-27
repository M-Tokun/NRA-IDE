"""Gemini CLI の BeforeAgent hook。共通判定 _prompt_gate.apply() を呼ぶ薄いラッパー。

入力（stdin の JSON）の "prompt" を判定し、注入する文脈があれば
hookSpecificOutput（hookEventName: "BeforeAgent", additionalContext）として返す。
注入する文脈がないとき、および判定できない入力（JSON でない等）は {} を返し、
入力自体は止めない（常に終了コード 0）。判定不能時は残りの承認をすべて消す（安全側）。

診断用として `.agent_state/hooks/prompt_gate_gemini.jsonl` に発火時刻・入力キー構造・
文字数・判定結果のみを追記する（入力の本文は記録しない）。
"""
from __future__ import annotations

import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _prompt_gate  # noqa: E402

LOG_PATH = _prompt_gate.ROOT / ".agent_state" / "hooks" / "prompt_gate_gemini.jsonl"


def _read_stdin() -> str:
    """hook の入力は UTF-8。Windows の既定（cp932）で読むと日本語が化けて一致しない。"""
    buffer = getattr(sys.stdin, "buffer", None)
    if buffer is None:  # 試験で StringIO に差し替えたとき
        return sys.stdin.read()
    return buffer.read().decode("utf-8")


def extract_prompt(payload: object) -> str:
    """入力 JSON から利用者の入力原文を取り出す。取り出せなければ ValueError。"""
    if isinstance(payload, dict):
        prompt = payload.get("prompt")
        if isinstance(prompt, str):
            return prompt
    raise ValueError("prompt is not a string")


def _keys(value: object) -> object:
    """入力の構造だけを記録するため、値は捨てて辞書のキーと型名だけを残す。"""
    if isinstance(value, dict):
        return {k: _keys(v) for k, v in value.items()}
    return type(value).__name__


def _log(**fields: object) -> None:
    """発火の有無と入力の形を `.agent_state/hooks/` に追記する（診断用。本文は記録しない）。"""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), **fields}
        with LOG_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - 記録の失敗で判定を止めない
        pass


def _emit(context: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if context:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "BeforeAgent",
                "additionalContext": context,
            }
        }
    else:
        output = {}
    print(json.dumps(output, ensure_ascii=False), flush=True)


def main() -> int:
    payload: object = None
    try:
        payload = json.loads(_read_stdin() or "{}")
        prompt = extract_prompt(payload)
        context = _prompt_gate.apply(prompt)
    except Exception as exc:  # noqa: BLE001 - 判定不能は承認なしへ倒す
        try:
            _prompt_gate.approval.clear_all()
        except Exception:  # noqa: BLE001
            pass
        _log(result="UNREADABLE", shape=_keys(payload), error=type(exc).__name__)
        _emit("")
        return 0
    _log(
        result="OK",
        shape=_keys(payload),
        prompt_chars=len(prompt),
        context=[w for w in ("PUSH_RUN", "PUSH_PREPARE", "COMMIT_RUN", "NOT_EXACT", "PUSH_DECLINED") if w in context],
    )
    _emit(context)
    return 0


if __name__ == "__main__":
    sys.exit(main())
