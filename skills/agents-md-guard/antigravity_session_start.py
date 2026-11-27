#!/usr/bin/env python
"""Antigravity IDE SessionStart hook: AGENTS.md 全文注入・ハッシュ記録・旧承認消去。

stdin の JSON から conversationId を受け取り、AGENTS.md 全文を injectSteps.systemMessage で
出力した後に `.agent_state/agents_md_read/antigravity/<conversationId>` へ記録する。
あわせて保留中の承認・push 計画を消去する。
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common  # noqa: E402

LOG_PATH = pathlib.Path(_common._REPO_ROOT) / ".agent_state" / "hooks" / "session_start_antigravity.jsonl"


def _read_stdin() -> str:
    buffer = getattr(sys.stdin, "buffer", None)
    if buffer is None:
        return sys.stdin.read()
    return buffer.read().decode("utf-8")


def _log(**fields: object) -> None:
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {"at": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), **fields}
        with LOG_PATH.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:  # noqa: BLE001
        pass


def _emit_system(text: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"injectSteps": [{"systemMessage": {"systemMessage": text}}]},
                     ensure_ascii=False), flush=True)


def _emit_error(text: str) -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"injectSteps": [{"errorMessage": {"userMessage": text}}]},
                     ensure_ascii=False), flush=True)


def main() -> int:
    emitted = False
    conv_id: object = None
    try:
        payload = json.loads(_read_stdin() or "{}")
        if not isinstance(payload, dict):
            raise ValueError("Hook payload must be an object")
        conv_id = payload.get("conversationId")
        if not _common.valid_session_id(conv_id):
            raise ValueError("Missing or invalid conversationId")
        _common.invalidate_marker("antigravity", conv_id)
        content = _common.read_agents_md()
        too_long = _common.too_long_reason("antigravity", content)
        if too_long:
            _emit_error(too_long)
            _log(result="TOO_LONG", conversation_id=conv_id, chars=len(_common.CONTEXT_PREFIX + content))
            return 0
        context = _common.CONTEXT_PREFIX + content
        _emit_system(context)
        emitted = True
        _common.write_marker("antigravity", conv_id, content)
        try:
            _common.clear_pending_route_state()
        except OSError:
            print("SessionStart could not clear pending push/commit state", file=sys.stderr)
        _log(result="OK", conversation_id=conv_id, chars=len(context))
        return 0
    except Exception as exc:  # noqa: BLE001
        _log(result="ERROR", conversation_id=conv_id, error=type(exc).__name__)
        if emitted:
            print("SessionStart marker recording failed", file=sys.stderr)
            return 2
        reason = (_common.MISSING_REASON_MESSAGE
                  if isinstance(exc, (OSError, UnicodeError))
                  else _common.INVALID_PAYLOAD_MESSAGE)
        try:
            _emit_error(reason)
        except (OSError, UnicodeError):
            return 2
        return 0


if __name__ == "__main__":
    sys.exit(main())
