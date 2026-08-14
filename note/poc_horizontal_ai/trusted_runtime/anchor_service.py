"""Process entry point that verifies and anchors one audit bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel import verify_audit_bundle

from .anchor_store import AuditAnchorStore
from .auth import derive_subkey
from .secret_file import load_secret_key_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchor-database", required=True)
    parser.add_argument("--anchor-id", required=True)
    parser.add_argument("--key-file", required=True)
    args = parser.parse_args(argv)
    try:
        bundle_json = sys.stdin.read()
        verification = verify_audit_bundle(bundle_json)
        if verification.events is None or verification.head_digest is None:
            raise ValueError("invalid audit bundle")
        master_key = load_secret_key_file(Path(args.key_file))
        anchor_key = derive_subkey(master_key, "audit-anchor-v1")
        with AuditAnchorStore(
            Path(args.anchor_database),
            anchor_key,
        ) as store:
            receipt = store.append(
                anchor_id=args.anchor_id,
                audit_head_digest=verification.head_digest,
                event_count=len(verification.events),
                bundle_sha256=hashlib.sha256(
                    bundle_json.encode("utf-8")
                ).hexdigest(),
                anchored_at=datetime.now(timezone.utc),
            )
        sys.stdout.write(
            json.dumps(
                {
                    **asdict(receipt),
                    "schema_version": "anchor-receipt/1.0",
                },
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 0
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


if __name__ == "__main__":
    raise SystemExit(main())
