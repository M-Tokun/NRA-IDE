"""Antigravity IDE の PreInvocation hook。共通判定 _prompt_gate.apply() を呼ぶ薄いラッパー。

入力（stdin の JSON）の "lastUserInput" と "invocationNum" を受け取り、
ターン開始時（invocationNum == 0、2026-11-27 実機確認）のときだけ共通判定 _prompt_gate.apply() を実行する。
ツール実行後の再呼び出し（invocationNum != 0）では承認の再発行・消去を行わず {} を返す。

出力は Antigravity の PreInvocation 規約:
- 注入文脈あり: {"injectSteps": [{"systemMessage": {"systemMessage": context}}]}
- 注入文脈なし / 再呼び出し / 判定不能: {}（入力は止めない、常に終了コード 0）

診断用として `.agent_state/hooks/prompt_gate_antigravity.jsonl` に発火時刻・invocation_num・
入力キー構造・文字数・判定結果のみを追記する（入力の本文は記録しない）。
"""
from __future__ import annotations

import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import _prompt_gate  # noqa: E402

LOG_PATH = _prompt_gate.ROOT / ".agent_state" / "hooks" / "prompt_gate_antigravity.jsonl"


def _read_stdin() -> str:
    """hook の入力は UTF-8。Windows の既定（cp932）で読むと日本語が化けて一致しない。"""
    buffer = getattr(sys.stdin, "buffer", None)
    if buffer is None:  # 試験で StringIO に差し替えたとき
        return sys.stdin.read()
    return buffer.read().decode("utf-8")


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
            "injectSteps": [
                {
                    "systemMessage": {
                        "systemMessage": context,
                    }
                }
            ]
        }
    else:
        output = {}
    print(json.dumps(output, ensure_ascii=False), flush=True)


def main() -> int:
    payload: object = None
    inv_num: object = None
    try:
        payload = json.loads(_read_stdin() or "{}")
        if not isinstance(payload, dict):
            raise ValueError("payload is not an object")
        inv_num = payload.get("invocationNum")
        if not isinstance(inv_num, int) or isinstance(inv_num, bool):
            raise ValueError("invocationNum is not an integer")
        if inv_num != 0:
            _log(result="SKIP_REINVOCATION", invocation_num=inv_num, shape=_keys(payload))
            _emit("")
            return 0
        prompt = payload.get("lastUserInput")
        if not isinstance(prompt, str):
            raise ValueError("lastUserInput is not a string")
        context = _prompt_gate.apply(prompt)
    except Exception as exc:  # noqa: BLE001 - 判定不能は承認なしへ倒す
        try:
            _prompt_gate.approval.clear_all()
        except Exception:  # noqa: BLE001
            pass
        _log(result="UNREADABLE", invocation_num=inv_num, shape=_keys(payload), error=type(exc).__name__)
        _emit("")
        return 0
    _log(
        result="OK",
        invocation_num=inv_num,
        shape=_keys(payload),
        prompt_chars=len(prompt),
        context=[w for w in ("PUSH_RUN", "PUSH_PREPARE", "COMMIT_RUN", "NOT_EXACT", "PUSH_DECLINED") if w in context],
    )
    _emit(context)
    return 0


if __name__ == "__main__":
    sys.exit(main())
