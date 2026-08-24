#!/usr/bin/env python
"""Cline: PreToolUseフックから呼び出される。

出力形式はCline固有（{"cancel": bool, "errorMessage": str}）で、
Claude/Codex/Geminiのhookdecision形式とは異なる点に注意。
"""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        print(json.dumps({"cancel": False}))
        return 0

    status = _common.agents_md_status()
    if status != "ok":
        print(json.dumps({"cancel": True, "errorMessage": _common.MISSING_REASON_MESSAGE}))
        return 0

    task_id = payload.get("taskId") or ""
    if not task_id or _common.is_marked("cline", task_id):
        print(json.dumps({"cancel": False}))
        return 0

    print(json.dumps({"cancel": True, "errorMessage": _common.REASON_MESSAGE}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
