#!/usr/bin/env python
"""Cline: PostToolUse相当フックから呼び出される（未確認: イベント名は文献上の
推定であり、Cline公式リファレンスで明示的に確認できたのはPreToolUseのみ）。
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

    task_id = payload.get("taskId") or ""
    params = payload.get("parameters") or {}
    file_path = params.get("path") or params.get("file_path") or ""

    if _common.path_targets_agents_md(file_path):
        _common.write_marker("cline", task_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
