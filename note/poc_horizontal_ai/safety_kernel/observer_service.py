"""One-request stdin/stdout entry point for a separately launched observer."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .observer_protocol import serve_observation_request


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Observe one repository path request from stdin."
    )
    parser.add_argument(
        "--repository-root",
        required=True,
        help="repository root that bounds every observable path",
    )
    parser.add_argument(
        "--observer-id",
        required=True,
        help="stable identifier recorded in the returned evidence",
    )
    args = parser.parse_args(argv)
    request_json = sys.stdin.read()
    try:
        response = serve_observation_request(
            request_json,
            repository_root=Path(args.repository_root),
            observer_id=args.observer_id,
        )
    except (OSError, ValueError) as error:
        sys.stdout.write(
            json.dumps(
                {"error": type(error).__name__, "schema_version": "observer-error/1.0"},
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2
    sys.stdout.write(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
