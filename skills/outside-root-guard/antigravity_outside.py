#!/usr/bin/env python
"""Antigravity IDE PreToolUse hook: 作業ルート外ガード（outside-root-guard）の薄い入口。

Antigravity の toolCall 形式（toolCall.{name, args}）を `_outside.decide()` 互換の形式へ
正規化して判定する。ルート外アクセスは decision: "force_ask"（Always Allow キャッシュを無視して
毎回確認）、許可リスト書込は decision: "deny"、ルート内・許可リスト内は {"decision": "ask"}
（Antigravity は decision 必須のため。自動許可しない）を返す。ログには _outside.decide() の判定を残す。
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _outside  # noqa: E402

_SHELL_NAMES = frozenset({"run_command"})
_WRITE_NAMES = frozenset({"write_file", "edit_file"})
_READ_NAMES = frozenset({"read_file"})


def _read_stdin() -> str:
    buffer = getattr(sys.stdin, "buffer", None)
    if buffer is None:
        return sys.stdin.read()
    return buffer.read().decode("utf-8")


def normalize_payload(raw: object) -> dict:
    if not isinstance(raw, dict):
        raise ValueError("payload must be an object")
    tool_call = raw.get("toolCall")
    if not isinstance(tool_call, dict):
        raise ValueError("toolCall must be an object")
    name = tool_call.get("name")
    if not isinstance(name, str) or not name:
        raise ValueError("toolCall.name must be a string")
    args = tool_call.get("args", {})
    if args is None:
        args = {}
    if not isinstance(args, dict):
        raise ValueError("toolCall.args must be an object")

    if name in _SHELL_NAMES:
        mapped_name = "Bash"
    elif name in _WRITE_NAMES:
        mapped_name = "Write"
    elif name in _READ_NAMES:
        mapped_name = "Read"
    else:
        mapped_name = name

    mapped_args: dict = {}
    for key, value in args.items():
        if key == "Path":
            mapped_args["file_path"] = value
        elif key == "CommandLine":
            mapped_args["command"] = value
        elif key == "Cwd":
            mapped_args["cwd"] = value
        else:
            mapped_args[key] = value

    out = {"tool_name": mapped_name, "tool_input": mapped_args}
    if isinstance(raw.get("cwd"), str):
        out["cwd"] = raw["cwd"]
    return out


def main() -> int:
    payload: dict = {}
    try:
        raw = json.loads(_read_stdin() or "{}")
        payload = normalize_payload(raw)
        # Antigravity の PreToolUse は "ask" / "deny" をサポートするため Claude と同じ確認判定を使う
        decision, reason = _outside.decide(payload, "claude")
    except Exception:  # noqa: BLE001
        decision = "ask"
        reason = "ルート外ガードが入力を確認できません。安全のため確認を求めます。"
    _outside.log("antigravity", payload, decision, reason)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if decision == "ask":
        output = {"decision": "force_ask", "reason": reason}
    elif decision:
        output = {"decision": decision, "reason": reason}
    else:
        output = {"decision": "ask"}
    print(json.dumps(output, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
