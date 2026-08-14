"""Process entry point for replay-resistant authenticated observation."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import timedelta
from pathlib import Path

from .nonce_store import PersistentNonceStore
from .observer_gateway import process_observation_request
from .auth import derive_subkey
from .secret_file import load_secret_key_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--observer-id", required=True)
    parser.add_argument("--nonce-database", required=True)
    parser.add_argument("--key-id", required=True)
    parser.add_argument("--key-file", required=True)
    parser.add_argument("--request-max-age-seconds", type=int, default=30)
    args = parser.parse_args(argv)
    try:
        master_key = load_secret_key_file(Path(args.key_file))
        authentication_key = derive_subkey(master_key, "observer-auth-v1")
        nonce_key = derive_subkey(master_key, "nonce-store-v1")
        with PersistentNonceStore(
            Path(args.nonce_database),
            nonce_key,
        ) as nonce_store:
            response = process_observation_request(
                sys.stdin.read(),
                repository_root=Path(args.repository_root),
                observer_id=args.observer_id,
                nonce_store=nonce_store,
                key_id=args.key_id,
                secret_key=authentication_key,
                request_max_age=timedelta(
                    seconds=args.request_max_age_seconds
                ),
            )
    except (OSError, ValueError) as error:
        sys.stdout.write(
            json.dumps(
                {
                    "error": type(error).__name__,
                    "schema_version": "trusted-runtime-error/1.0",
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2
    sys.stdout.write(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
