"""One-request monotonic trust-checkpoint witness service."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .asymmetric_auth import load_ed25519_private_key, load_ed25519_public_key
from .checkpoint_attestation import CheckpointWitnessStateStore
from .trust_bundle import verify_signed_trust_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Witness one monotonic trust checkpoint read from stdin."
    )
    parser.add_argument(
        "--witness-database",
        required=True,
        help="SQLite path holding this witness's monotonic checkpoint state",
    )
    parser.add_argument(
        "--witness-principal-id",
        required=True,
        help="principal identity represented by this witness process",
    )
    parser.add_argument(
        "--witness-key-id",
        required=True,
        help="trust-bundle key identifier used to sign the attestation",
    )
    parser.add_argument(
        "--witness-private-key-file",
        required=True,
        help="Ed25519 private-key file for the witness key identifier",
    )
    parser.add_argument(
        "--pinned-root-key-id",
        required=True,
        help="identifier of the pinned primary trust root",
    )
    parser.add_argument(
        "--pinned-root-public-key-file",
        required=True,
        help="Ed25519 public-key file for the pinned primary trust root",
    )
    parser.add_argument(
        "--trust-bundle-max-age-seconds",
        type=int,
        default=300,
        help="maximum accepted trust-bundle signature age in seconds (default: 300)",
    )
    args = parser.parse_args(argv)
    try:
        current = datetime.now(timezone.utc)
        signed_bundle_json = sys.stdin.read(512 * 1024 + 1)
        if len(signed_bundle_json.encode("utf-8")) > 512 * 1024:
            raise ValueError("trust bundle input too large")
        root_public_key = load_ed25519_public_key(
            Path(args.pinned_root_public_key_file)
        )
        verification = verify_signed_trust_bundle(
            signed_bundle_json,
            pinned_root_keys={args.pinned_root_key_id: root_public_key},
            signature_max_age=timedelta(
                seconds=args.trust_bundle_max_age_seconds
            ),
            now=current,
        )
        if verification.bundle is None:
            raise ValueError(",".join(verification.reason_codes))
        private_key = load_ed25519_private_key(
            Path(args.witness_private_key_file)
        )
        with CheckpointWitnessStateStore(
            Path(args.witness_database),
            args.witness_principal_id,
        ) as store:
            signed = store.attest(
                verification.bundle,
                witness_key_id=args.witness_key_id,
                witness_private_key=private_key,
                witnessed_at=current,
            )
    except (OSError, sqlite3.DatabaseError, ValueError) as error:
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
    sys.stdout.write(signed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
