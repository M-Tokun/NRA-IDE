"""Cline の UserPromptSubmit hook。共通判定 _prompt_gate.apply() を呼ぶ薄いラッパー。

入力（stdin の JSON）から利用者の入力原文を取り出して判定し、承認の書込み・消去と文脈の注入を行う。
入力の形は2通りを受ける（実機での確認は README の「前提」を参照）:

  平坦      {"prompt": "…"}
  入れ子    {"userPromptSubmit": {"prompt": "…"}}   （preToolUse と同じ Cline の形）

出力は Cline の hook 規約 {"cancel", "contextModification", "errorMessage"}。入力は止めない（cancel は常に false）。
解釈できない入力は承認を書かず、残りの承認を消す（安全側）。そのとき errorMessage で利用者に知らせる。
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _prompt_gate  # noqa: E402

WRAPPER_RE = re.compile(r'<user_input mode="(?:act|plan)">(.*)</user_input>', re.DOTALL)
LOG_PATH =_prompt_gate.ROOT / ".agent_state" / "hooks" / "prompt_gate_cline.jsonl"
UNREADABLE ="prompt_gate: 入力の形を解釈できないため承認を作りませんでした（Cline の UserPromptSubmit 入力を確認してください）。"


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
        if prompt is None and isinstance(payload.get("userPromptSubmit"), dict):
            prompt = payload["userPromptSubmit"].get("prompt")
        if isinstance(prompt, str):
            return unwrap(prompt)
    raise ValueError("prompt is not a string")


def unwrap(prompt: str) -> str:
    """Cline は入力を <user_input mode="act|plan">…</user_input> で包んで渡す（2026-11-27 実機で確認）。

    全体がこの形のときだけ中身を返す。それ以外は手を加えない（合言葉と一致せず、承認は作られない）。
    """
    match = WRAPPER_RE.fullmatch(prompt.strip(_prompt_gate.STRIP))
    return match.group(1) if match else prompt


def _emit(context: str, error: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"cancel": False, "contextModification": context, "errorMessage": error},
                     ensure_ascii=False), flush=True)


def _keys(value: object) -> object:
    """入力の構造だけを記録するため、値は捨てて辞書のキーだけを残す。"""
    if isinstance(value, dict):
        return {k: _keys(v) for k, v in value.items()}
    return type(value).__name__


def _log(**fields: object) -> None:
    """発火の有無と入力の形を `.agent_state/hooks/` に追記する（診断用。入力の本文は記録しない）。"""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), **fields}
        with LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001 - 記録の失敗で判定を止めない
        pass


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
        _emit("", UNREADABLE)
        return 0
    _log(result="OK", shape=_keys(payload), prompt_chars=len(prompt),
         context=[w for w in ("PUSH_RUN", "PUSH_PREPARE", "COMMIT_RUN", "NOT_EXACT", "PUSH_DECLINED") if w in context])
    _emit(context, "")
    return 0


if __name__ == "__main__":
    sys.exit(main())
