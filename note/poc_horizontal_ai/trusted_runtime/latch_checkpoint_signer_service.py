"""One-request signer for the verified local irreversible-latch chain."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .irreversible_latch_store import PersistentIrreversibleLatchStore
from .latch_witness import (
    create_signed_latch_checkpoint,
    create_signed_latch_genesis,
)
from .runtime_admission import admit_file_signer, load_bounded_text_file
from .secret_file import load_secret_key_file
from .trust_bundle import KeyRole


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sign the verified head of one local irreversible-latch chain."
    )
    parser.add_argument("--latch-database", required=True, help="SQLite path holding the irreversible-latch chain")
    parser.add_argument("--latch-store-id", required=True, help="stable identity bound to the latch chain")
    parser.add_argument("--latch-integrity-key-file", required=True, help="secret-key file protecting the local latch ledger")
    parser.add_argument("--signing-key-id", required=True, help="trusted LATCH_CHECKPOINT_SIGNER key identifier")
    parser.add_argument("--signing-key-file", required=True, help="Ed25519 private-key file for the signing key identifier")
    parser.add_argument("--trust-bundle-file", required=True, help="signed trust-bundle JSON file used for signer admission")
    parser.add_argument("--trust-checkpoint-database", required=True, help="SQLite path retaining the accepted trust-bundle chain")
    parser.add_argument("--pinned-root-key-id", required=True, help="identifier of the pinned primary trust root")
    parser.add_argument("--pinned-root-public-key-file", required=True, help="Ed25519 public-key file for the pinned primary trust root")
    parser.add_argument("--trust-bundle-max-age-seconds", type=int, default=300, help="maximum accepted trust-bundle age in seconds (default: 300)")
    parser.add_argument(
        "--trust-checkpoint-attestation-file",
        action="append",
        required=True,
        help="signed checkpoint-attestation file; repeat for distinct witnesses",
    )
    parser.add_argument(
        "--minimum-trust-checkpoint-witness-principals",
        type=int,
        default=2,
        help="minimum distinct trust-checkpoint witness principals (default: 2)",
    )
    parser.add_argument(
        "--trust-checkpoint-attestation-max-age-seconds",
        type=int,
        default=300,
        help="maximum trust-checkpoint attestation age in seconds (default: 300)",
    )
    args = parser.parse_args(argv)
    try:
        request = _read_request()
        current = datetime.now(timezone.utc)
        admitted_signer = admit_file_signer(
            signed_bundle_path=Path(args.trust_bundle_file),
            checkpoint_database_path=Path(args.trust_checkpoint_database),
            pinned_root_key_id=args.pinned_root_key_id,
            pinned_root_public_key_path=Path(args.pinned_root_public_key_file),
            signing_key_id=args.signing_key_id,
            signing_key_path=Path(args.signing_key_file),
            required_role=KeyRole.LATCH_CHECKPOINT_SIGNER,
            bundle_max_age=timedelta(
                seconds=args.trust_bundle_max_age_seconds
            ),
            signed_checkpoint_attestations=tuple(
                load_bounded_text_file(Path(path), 256 * 1024)
                for path in args.trust_checkpoint_attestation_file
            ),
            minimum_checkpoint_witness_principals=(
                args.minimum_trust_checkpoint_witness_principals
            ),
            checkpoint_attestation_max_age=timedelta(
                seconds=args.trust_checkpoint_attestation_max_age_seconds
            ),
            now=current,
        )
        integrity_key = load_secret_key_file(
            Path(args.latch_integrity_key_file)
        )
        with PersistentIrreversibleLatchStore(
            Path(args.latch_database),
            integrity_key,
        ) as latch_store:
            head = latch_store.head()
            if head is None:
                signed_checkpoints = (
                    create_signed_latch_genesis(
                        checkpoint_id=(
                            f"genesis-{request['admission_challenge'][:24]}"
                        ),
                        latch_store_id=args.latch_store_id,
                        signing_key_id=args.signing_key_id,
                        signing_private_key=admitted_signer.private_key,
                        trust_bundle=admitted_signer.trust_bundle,
                        checkpointed_at=current,
                    ),
                )
            else:
                checkpoints: list[str] = []
                for sequence in range(1, head.sequence + 1):
                    sequence_head = latch_store.head_at(sequence)
                    if sequence_head is None:
                        raise ValueError("IRREVERSIBLE_LATCH_CHAIN_INVALID")
                    checkpoints.append(
                        create_signed_latch_checkpoint(
                            sequence_head,
                            checkpoint_id=(
                                f"head-{sequence}-"
                                f"{request['admission_challenge'][:24]}"
                            ),
                            latch_store_id=args.latch_store_id,
                            signing_key_id=args.signing_key_id,
                            signing_private_key=admitted_signer.private_key,
                            trust_bundle=admitted_signer.trust_bundle,
                            checkpointed_at=current,
                        )
                    )
                signed_checkpoints = tuple(checkpoints)
        sys.stdout.write(
            json.dumps(
                {
                    "admission_challenge": request["admission_challenge"],
                    "schema_version": "signed-latch-checkpoint-set/1.0",
                    "signed_latch_checkpoints": signed_checkpoints,
                },
                ensure_ascii=False,
                allow_nan=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 0
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


def _read_request() -> dict[str, str]:
    raw = sys.stdin.read(4097)
    if len(raw.encode("utf-8")) > 4096:
        raise ValueError("checkpoint signer request too large")
    data = json.loads(raw, object_pairs_hook=_pairs_hook)
    if not isinstance(data, dict) or set(data) != {
        "admission_challenge",
        "schema_version",
    }:
        raise ValueError("invalid checkpoint signer request")
    challenge = data["admission_challenge"]
    if (
        data["schema_version"] != "latch-checkpoint-sign-request/1.0"
        or not isinstance(challenge, str)
        or len(challenge) != 64
        or any(character not in "0123456789abcdef" for character in challenge)
    ):
        raise ValueError("invalid checkpoint signer request")
    return {"admission_challenge": challenge}


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


if __name__ == "__main__":
    raise SystemExit(main())
