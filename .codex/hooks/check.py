"""Observe PreToolUse delivery without changing tool permissions."""

import json
from datetime import datetime, timezone
from pathlib import Path
import sys


def main():
    # Separate manual probes from actual client delivery evidence.
    filename = (
        "pre_tool_use_self_test.jsonl"
        if "--self-test" in sys.argv[1:]
        else "pre_tool_use.jsonl"
    )
    try:
        payload = json.load(sys.stdin)
        tool_name = payload.get("tool_name") if isinstance(payload, dict) else None
        record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "tool_name": tool_name if isinstance(tool_name, str) else "<unavailable>",
        }
        # Resolve from this script, never from untrusted hook-input paths.
        log_path = Path(__file__).resolve().parents[2] / ".agent_state" / "hooks" / filename
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8", newline="\n") as log:
            log.write(json.dumps(record, ensure_ascii=True) + "\n")
    except (OSError, ValueError):
        # An observation failure must not become a permission decision.
        print("PreToolUse observation could not be recorded.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
