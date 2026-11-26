"""Claude Code の UserPromptSubmit hook。共通判定 _prompt_gate.apply() を呼ぶ薄いラッパー。

入力（stdin の JSON）の "prompt" を判定し、注入する文脈があれば
hookSpecificOutput.additionalContext として返す。入力は止めない（常に終了コード 0）。
判定できない入力（JSON でない等）は承認を書かず、残りの承認を消す（安全側）。
"""
from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _prompt_gate  # noqa: E402


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        prompt = payload.get("prompt")
        if not isinstance(prompt, str):
            raise ValueError("prompt is not a string")
        context = _prompt_gate.apply(prompt)
    except Exception:  # noqa: BLE001 - 判定不能は承認なしへ倒す
        _prompt_gate.approval.clear_all()
        return 0
    if context:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                 "additionalContext": context}}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
