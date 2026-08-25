"""One-request, separate-process root-policy witness service."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .asymmetric_auth import (
    load_ed25519_private_key,
    load_ed25519_public_key,
    public_key_fingerprint,
)
from .root_policy import PinnedPolicyRoot, RootPolicyWitnessStateStore
from .trust_bundle import verify_signed_trust_bundle


_MAX_REQUEST_BYTES = 512 * 1024


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Witness and sign one root-policy endorsement request."
    )
    parser.add_argument("--witness-database", required=True, help="SQLite path holding this policy witness's monotonic state")
    parser.add_argument("--policy-root-principal-id", required=True, help="distinct policy-root principal represented by this witness")
    parser.add_argument("--policy-root-key-id", required=True, help="key identifier assigned to this pinned policy root")
    parser.add_argument("--policy-root-private-key-file", required=True, help="Ed25519 private-key file for the policy-root key identifier")
    parser.add_argument(
        "--policy-root-public-key-fingerprint",
        required=True,
        help="expected SHA-256 fingerprint of the policy-root public key",
    )
    parser.add_argument("--pinned-root-key-id", required=True, help="identifier of the pinned primary trust root")
    parser.add_argument("--pinned-root-public-key-file", required=True, help="Ed25519 public-key file for the pinned primary trust root")
    parser.add_argument("--trust-bundle-max-age-seconds", type=int, default=300, help="maximum accepted trust-bundle age in seconds (default: 300)")
    parser.add_argument("--endorsement-validity-seconds", type=int, default=300, help="validity interval placed on a new endorsement in seconds (default: 300)")
    args = parser.parse_args(argv)
    try:
        if (
            args.trust_bundle_max_age_seconds <= 0
            or args.endorsement_validity_seconds <= 0
        ):
            raise ValueError("time limits must be positive")
        request = _read_request()
        current = datetime.now(timezone.utc)
        primary_root = load_ed25519_public_key(
            Path(args.pinned_root_public_key_file)
        )
        verification = verify_signed_trust_bundle(
            request["signed_trust_bundle_json"],
            pinned_root_keys={args.pinned_root_key_id: primary_root},
            signature_max_age=timedelta(
                seconds=args.trust_bundle_max_age_seconds
            ),
            now=current,
        )
        if verification.bundle is None:
            raise ValueError(",".join(verification.reason_codes))
        private_key = load_ed25519_private_key(
            Path(args.policy_root_private_key_file)
        )
        if (
            public_key_fingerprint(private_key.public_key())
            != args.policy_root_public_key_fingerprint
        ):
            raise ValueError("POLICY_ROOT_PRIVATE_KEY_MISMATCH")
        policy_root = PinnedPolicyRoot(
            args.policy_root_key_id,
            args.policy_root_principal_id,
            private_key.public_key(),
        )
        challenge = request["admission_challenge"]
        with RootPolicyWitnessStateStore(
            Path(args.witness_database),
            policy_root,
        ) as store:
            if request["operation"] == "ENDORSE":
                signed = store.endorse(
                    policy_id=request["policy_id"],
                    policy_configuration_sha256=request[
                        "policy_configuration_sha256"
                    ],
                    endorsement_id=(
                        f"root-policy-g{verification.bundle.generation}-"
                        f"{challenge[:32]}"
                    ),
                    private_key=private_key,
                    trust_bundle=verification.bundle,
                    admission_challenge=challenge,
                    endorsed_at=current,
                    valid_until=current
                    + timedelta(seconds=args.endorsement_validity_seconds),
                )
            else:
                signed = store.approve_rotation(
                    rotation_id=request["rotation_id"],
                    approval_side=request["approval_side"],
                    policy_id=request["policy_id"],
                    previous_configuration_sha256=request[
                        "previous_configuration_sha256"
                    ],
                    next_configuration_sha256=request[
                        "next_configuration_sha256"
                    ],
                    private_key=private_key,
                    trust_bundle=verification.bundle,
                    admission_challenge=challenge,
                    approved_at=current,
                    valid_until=current
                    + timedelta(seconds=args.endorsement_validity_seconds),
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


def _read_request() -> dict[str, str]:
    raw = sys.stdin.read(_MAX_REQUEST_BYTES + 1)
    if len(raw.encode("utf-8")) > _MAX_REQUEST_BYTES:
        raise ValueError("root policy witness request too large")
    data = json.loads(raw, object_pairs_hook=_pairs_hook)
    if not isinstance(data, dict):
        raise ValueError("invalid root policy witness request")
    if data.get("schema_version") == "root-policy-witness-request/1.1":
        return _decode_endorsement_request(data)
    if data.get("schema_version") == "root-policy-rotation-approval-request/1.0":
        return _decode_rotation_approval_request(data)
    raise ValueError("invalid root policy witness request")


def _decode_endorsement_request(data: dict[str, object]) -> dict[str, str]:
    if set(data) != {
        "admission_challenge",
        "policy_configuration_sha256",
        "policy_id",
        "schema_version",
        "signed_trust_bundle_json",
    }:
        raise ValueError("invalid root policy witness request")
    challenge = data["admission_challenge"]
    policy_configuration = data["policy_configuration_sha256"]
    policy_id = data["policy_id"]
    signed_bundle = data["signed_trust_bundle_json"]
    if (
        data["schema_version"] != "root-policy-witness-request/1.1"
        or not isinstance(challenge, str)
        or len(challenge) != 64
        or any(character not in "0123456789abcdef" for character in challenge)
        or not isinstance(policy_configuration, str)
        or len(policy_configuration) != 64
        or any(
            character not in "0123456789abcdef"
            for character in policy_configuration
        )
        or not isinstance(policy_id, str)
        or not policy_id
        or len(policy_id) > 128
        or any(character.isspace() for character in policy_id)
        or not isinstance(signed_bundle, str)
        or not signed_bundle
    ):
        raise ValueError("invalid root policy witness request")
    return {
        "admission_challenge": challenge,
        "operation": "ENDORSE",
        "policy_configuration_sha256": policy_configuration,
        "policy_id": policy_id,
        "signed_trust_bundle_json": signed_bundle,
    }


def _decode_rotation_approval_request(data: dict[str, object]) -> dict[str, str]:
    if set(data) != {
        "admission_challenge",
        "approval_side",
        "next_configuration_sha256",
        "policy_id",
        "previous_configuration_sha256",
        "rotation_id",
        "schema_version",
        "signed_trust_bundle_json",
    }:
        raise ValueError("invalid root policy rotation approval request")
    result = {
        "admission_challenge": data["admission_challenge"],
        "approval_side": data["approval_side"],
        "next_configuration_sha256": data["next_configuration_sha256"],
        "operation": "ROTATION_APPROVAL",
        "policy_id": data["policy_id"],
        "previous_configuration_sha256": data[
            "previous_configuration_sha256"
        ],
        "rotation_id": data["rotation_id"],
        "signed_trust_bundle_json": data["signed_trust_bundle_json"],
    }
    if (
        result["approval_side"] not in {"PREVIOUS", "NEXT"}
        or any(
            not isinstance(result[key], str) or not result[key]
            for key in result
        )
        or any(
            len(result[key]) != 64
            or any(character not in "0123456789abcdef" for character in result[key])
            for key in (
                "admission_challenge",
                "previous_configuration_sha256",
                "next_configuration_sha256",
            )
        )
        or len(result["policy_id"]) > 128
        or any(character.isspace() for character in result["policy_id"])
        or len(result["rotation_id"]) > 128
        or any(character.isspace() for character in result["rotation_id"])
    ):
        raise ValueError("invalid root policy rotation approval request")
    return result


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


if __name__ == "__main__":
    raise SystemExit(main())
