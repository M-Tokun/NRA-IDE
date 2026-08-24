#!/usr/bin/env python
"""Gemini CLI: BeforeTool hook (matcher: "run_shell_command|write_file|edit|replace")."""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        print(json.dumps({"decision": "allow"}))
        return 0

    status = _common.agents_md_status()
    if status != "ok":
        print(json.dumps({"decision": "deny", "reason": _common.MISSING_REASON_MESSAGE}))
        return 0

    session_id = payload.get("session_id") or ""
    if not session_id or _common.is_marked("gemini", session_id):
        print(json.dumps({"decision": "allow"}))
        return 0

    print(json.dumps({"decision": "deny", "reason": _common.REASON_MESSAGE}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
