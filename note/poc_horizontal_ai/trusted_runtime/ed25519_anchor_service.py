"""One-request audit anchor service returning an Ed25519 receipt."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import timedelta
from pathlib import Path

from .anchor_store import AuditAnchorStore
from .runtime_admission import admit_file_signer, load_bounded_text_file
from .secret_file import load_secret_key_file
from .signed_boundary import anchor_and_sign_bundle
from .trust_bundle import KeyRole


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchor-database", required=True)
    parser.add_argument("--anchor-id", required=True)
    parser.add_argument("--ledger-key-file", required=True)
    parser.add_argument("--signing-key-id", required=True)
    parser.add_argument("--signing-key-file", required=True)
    parser.add_argument("--trust-bundle-file", required=True)
    parser.add_argument("--trust-checkpoint-database", required=True)
    parser.add_argument("--pinned-root-key-id", required=True)
    parser.add_argument("--pinned-root-public-key-file", required=True)
    parser.add_argument("--trust-bundle-max-age-seconds", type=int, default=300)
    parser.add_argument(
        "--trust-checkpoint-attestation-file",
        action="append",
        required=True,
    )
    parser.add_argument(
        "--minimum-checkpoint-witness-principals",
        type=int,
        default=2,
    )
    parser.add_argument(
        "--checkpoint-attestation-max-age-seconds",
        type=int,
        default=300,
    )
    args = parser.parse_args(argv)
    try:
        ledger_key = load_secret_key_file(Path(args.ledger_key_file))
        admitted_signer = admit_file_signer(
            signed_bundle_path=Path(args.trust_bundle_file),
            checkpoint_database_path=Path(args.trust_checkpoint_database),
            pinned_root_key_id=args.pinned_root_key_id,
            pinned_root_public_key_path=Path(args.pinned_root_public_key_file),
            signing_key_id=args.signing_key_id,
            signing_key_path=Path(args.signing_key_file),
            required_role=KeyRole.ANCHOR_SIGNER,
            bundle_max_age=timedelta(
                seconds=args.trust_bundle_max_age_seconds
            ),
            signed_checkpoint_attestations=tuple(
                load_bounded_text_file(Path(path), 256 * 1024)
                for path in args.trust_checkpoint_attestation_file
            ),
            minimum_checkpoint_witness_principals=(
                args.minimum_checkpoint_witness_principals
            ),
            checkpoint_attestation_max_age=timedelta(
                seconds=args.checkpoint_attestation_max_age_seconds
            ),
        )
        with AuditAnchorStore(Path(args.anchor_database), ledger_key) as store:
            response = anchor_and_sign_bundle(
                sys.stdin.read(),
                anchor_id=args.anchor_id,
                anchor_store=store,
                signing_key_id=args.signing_key_id,
                signing_key=admitted_signer.private_key,
                admitted_signer=admitted_signer,
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
