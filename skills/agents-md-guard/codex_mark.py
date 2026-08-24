#!/usr/bin/env python
"""Codex CLI: PostToolUse hook (matcher: "Bash|apply_patch|Edit|Write|read_file").

Codexは既定では専用のReadツールを持たず、シェル経由（cat/sed/head等）で
ファイルを読む。そのためBashコマンド文字列のヒューリスティック検知を主とし、
MCPのread_file等が導入されている場合はfile_path一致も併用する。
"""
import json
import sys

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
import _common  # noqa: E402


def main():
    try:
        payload = json.load(sys.stdin)
    except (ValueError, json.JSONDecodeError):
        return 0

    session_id = payload.get("session_id") or payload.get("turn_id") or ""
    tool_input = payload.get("tool_input") or {}

    file_path = tool_input.get("file_path") or tool_input.get("path") or ""
    command = tool_input.get("command") or ""

    if _common.path_targets_agents_md(file_path) or _common.command_reads_agents_md(command):
        _common.write_marker("codex", session_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
