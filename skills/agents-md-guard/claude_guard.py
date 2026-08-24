#!/usr/bin/env python
"""Claude Code: PreToolUse hook (matcher: Edit|Write|Bash|NotebookEdit)."""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        print(json.dumps({"continue": True}))
        return 0

    status = _common.agents_md_status()
    if status != "ok":
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": _common.MISSING_REASON_MESSAGE,
            }
        }
        print(json.dumps(output))
        return 0

    session_id = payload.get("session_id") or ""
    if not session_id or _common.is_marked("claude", session_id):
        print(json.dumps({"continue": True}))
        return 0

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": _common.REASON_MESSAGE,
        }
    }
    print(json.dumps(output))
    return 0


if __name__ == "__main__":
    sys.exit(main())
