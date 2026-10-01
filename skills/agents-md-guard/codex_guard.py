#!/usr/bin/env python
"""Codex CLI: PreToolUse hook (matcher: "Bash|apply_patch|Edit|Write")."""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def _deny(reason):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        _deny(_common.INVALID_PAYLOAD_MESSAGE)
        return 0

    status = _common.agents_md_status()
    if status != "ok":
        _deny(_common.MISSING_REASON_MESSAGE)
        return 0

    session_id = payload.get("session_id") or ""
    if session_id and _common.is_marked("codex", session_id):
        # PreToolUseの許可時は、未対応フィールドを返さず無出力で成功する。
        return 0

    _deny(_common.REASON_MESSAGE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
