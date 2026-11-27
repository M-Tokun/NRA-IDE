#!/usr/bin/env python
"""Antigravity IDE PreToolUse hook: AGENTS.md 読込・危険Git・承認書込ガード。

Antigravity の toolCall 形式（conversationId, toolCall.{name, args}）を
`_common.guard_reason()` の共通形式へ正規化して判定する。
拒否時は {"decision": "deny", "reason": ...}、通過時は {"decision": "ask"} を返す。
Antigravity の PreToolUse は decision が必須で、{} は拒否として扱われる。
"allow" は自動承認になるため使わない。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402

_SHELL_NAMES = frozenset({"run_command"})
_READ_NAMES = frozenset({"read_file"})


def _read_stdin() -> str:
    buffer = getattr(sys.stdin, "buffer", None)
    if buffer is None:
        return sys.stdin.read()
    return buffer.read().decode("utf-8")


def normalize_payload(raw: object) -> dict:
    """Antigravity の PreToolUse JSON を _common 互換の辞書へ変換する。"""
    if not isinstance(raw, dict):
        raise ValueError("Hook payload must be an object")
    conv_id = raw.get("conversationId")
    if not _common.valid_session_id(conv_id):
        raise ValueError("Missing or invalid conversationId")
    tool_call = raw.get("toolCall")
    if not isinstance(tool_call, dict):
        raise ValueError("Missing or invalid toolCall")
    name = tool_call.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("Missing or invalid toolCall.name")
    args = tool_call.get("args", {})
    if args is None:
        args = {}
    if not isinstance(args, dict):
        raise ValueError("toolCall.args must be an object")

    mapped_name = "Bash" if name in _SHELL_NAMES else name
    mapped_args: dict = {}
    if name in _SHELL_NAMES:
        if "CommandLine" in args:
            mapped_args["command"] = args["CommandLine"]
        elif "command" in args:
            mapped_args["command"] = args["command"]
    elif name in _READ_NAMES:
        for key, value in args.items():
            if key == "Path":
                mapped_args["file_path"] = value
            else:
                mapped_args[key] = value
    else:
        for key, value in args.items():
            if key == "Path":
                mapped_args["file_path"] = value
            elif key == "CommandLine":
                mapped_args["command"] = value
            else:
                mapped_args[key] = value

    out = {
        "session_id": conv_id,
        "tool_name": mapped_name,
        "tool_input": mapped_args,
    }
    if isinstance(raw.get("cwd"), str):
        out["cwd"] = raw["cwd"]
    return out


def _emit(reason: str | None) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    output = {"decision": "deny", "reason": reason} if reason else {"decision": "ask"}
    print(json.dumps(output, ensure_ascii=False), flush=True)


def main() -> int:
    try:
        raw = json.loads(_read_stdin() or "{}")
        payload = normalize_payload(raw)
        reason = _common.guard_reason(payload, "antigravity")
    except Exception:  # noqa: BLE001
        reason = _common.INVALID_PAYLOAD_MESSAGE
    _emit(reason)
    return 0


if __name__ == "__main__":
    sys.exit(main())
