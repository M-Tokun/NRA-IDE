#!/usr/bin/env python
"""Claude Code: PostToolUse hook (matcher: Read)."""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        return 0

    session_id = payload.get("session_id") or ""
    file_path = (payload.get("tool_input") or {}).get("file_path") or ""
    if _common.path_targets_agents_md(file_path):
        _common.write_marker("claude", session_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
