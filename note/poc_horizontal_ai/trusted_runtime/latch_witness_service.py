"""One-request, separate-process irreversible-latch witness service."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .asymmetric_auth import load_ed25519_private_key, load_ed25519_public_key
from .latch_witness import LatchCheckpointWitnessStateStore
from .trust_bundle import verify_signed_trust_bundle


_MAX_REQUEST_BYTES = 1024 * 1024


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--witness-database", required=True)
    parser.add_argument("--witness-principal-id", required=True)
    parser.add_argument("--latch-store-id", required=True)
    parser.add_argument("--witness-key-id", required=True)
    parser.add_argument("--witness-private-key-file", required=True)
    parser.add_argument("--pinned-root-key-id", required=True)
    parser.add_argument("--pinned-root-public-key-file", required=True)
    parser.add_argument("--trust-bundle-max-age-seconds", type=int, default=300)
    parser.add_argument(
        "--checkpoint-signature-max-age-seconds", type=int, default=300
    )
    args = parser.parse_args(argv)
    try:
        if (
            args.trust_bundle_max_age_seconds <= 0
            or args.checkpoint_signature_max_age_seconds <= 0
        ):
            raise ValueError("signature age limits must be positive")
        request = _read_request()
        current = datetime.now(timezone.utc)
        root_public_key = load_ed25519_public_key(
            Path(args.pinned_root_public_key_file)
        )
        verification = verify_signed_trust_bundle(
            request["signed_trust_bundle_json"],
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
        with LatchCheckpointWitnessStateStore(
            Path(args.witness_database),
            args.witness_principal_id,
            args.latch_store_id,
        ) as store:
            signed = store.attest(
                request["signed_latch_checkpoints"],
                trust_bundle=verification.bundle,
                checkpoint_signature_max_age=timedelta(
                    seconds=args.checkpoint_signature_max_age_seconds
                ),
                witness_key_id=args.witness_key_id,
                witness_private_key=private_key,
                witnessed_at=current,
                admission_challenge=request["admission_challenge"],
            )
    except (OSError, sqlite3.DatabaseError, ValueError, json.JSONDecodeError) as error:
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


def _read_request() -> dict[str, object]:
    raw = sys.stdin.read(_MAX_REQUEST_BYTES + 1)
    if len(raw.encode("utf-8")) > _MAX_REQUEST_BYTES:
        raise ValueError("latch witness request too large")
    data = json.loads(raw, object_pairs_hook=_pairs_hook)
    if not isinstance(data, dict) or set(data) != {
        "admission_challenge",
        "schema_version",
        "signed_latch_checkpoints",
        "signed_trust_bundle_json",
    }:
        raise ValueError("invalid latch witness request")
    checkpoints = data["signed_latch_checkpoints"]
    if (
        data["schema_version"] != "latch-witness-request/1.0"
        or not isinstance(data["admission_challenge"], str)
        or len(data["admission_challenge"]) != 64
        or any(
            character not in "0123456789abcdef"
            for character in data["admission_challenge"]
        )
        or not isinstance(data["signed_trust_bundle_json"], str)
        or not isinstance(checkpoints, list)
        or not checkpoints
        or len(checkpoints) > 1024
        or any(not isinstance(item, str) for item in checkpoints)
    ):
        raise ValueError("invalid latch witness request")
    return {
        "admission_challenge": data["admission_challenge"],
        "signed_trust_bundle_json": data["signed_trust_bundle_json"],
        "signed_latch_checkpoints": tuple(checkpoints),
    }


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


if __name__ == "__main__":
    raise SystemExit(main())
