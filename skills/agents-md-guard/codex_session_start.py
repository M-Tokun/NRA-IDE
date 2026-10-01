#!/usr/bin/env python
"""Codex SessionStart hook: load AGENTS.md before any guarded tool call."""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def _stop(reason):
    print(json.dumps({"continue": False, "stopReason": reason}))


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        _stop(_common.INVALID_PAYLOAD_MESSAGE)
        return 0

    session_id = payload.get("session_id") or ""
    if not session_id:
        _stop(_common.INVALID_PAYLOAD_MESSAGE)
        return 0

    try:
        content = _common.read_agents_md()
    except (OSError, UnicodeError, ValueError):
        _stop(_common.MISSING_REASON_MESSAGE)
        return 0

    output = {
        "systemMessage": "AGENTS.md loaded",
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": "AGENTS.md loaded\n\n" + content,
        },
    }
    try:
        print(json.dumps(output, ensure_ascii=False), flush=True)
        _common.write_marker("codex", session_id)
    except (BrokenPipeError, OSError, UnicodeError, ValueError):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
