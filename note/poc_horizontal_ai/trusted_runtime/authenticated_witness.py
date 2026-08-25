"""Witness-signed attestations counted by distinct trusted principals."""

from __future__ import annotations

import json
import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Sequence

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import sign_payload_ed25519
from .role_verification import verify_role_signed_payload
from .runtime_admission import AdmittedSigner
from .trust_bundle import KeyRole, VerifiedTrustBundle
from .witness_store import WitnessRecord


_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class VerifiedWitnessAttestation:
    attestation_id: str
    witness_principal_id: str
    witness_key_id: str
    witness_sequence: int
    audit_head_digest: str
    signed_receipt_sha256: str
    witnessed_at: datetime


@dataclass(frozen=True, slots=True)
class AuthenticatedWitnessQuorum:
    satisfied: bool
    principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


def create_signed_witness_attestation(
    record: WitnessRecord,
    *,
    attestation_id: str,
    witness_principal_id: str,
    witness_sequence: int,
    witness_key_id: str,
    witness_private_key: Ed25519PrivateKey,
    admitted_signer: AdmittedSigner | None = None,
    witnessed_at: datetime,
) -> str:
    """Sign one witness record with explicit principal and sequence binding.

    ``admitted_signer`` may additionally prove that the supplied private key is
    admitted for the witness role. Identifiers, sequence, key match, and the
    timezone-aware ``witnessed_at`` value are validated before signing. The
    function returns canonical signed JSON and performs no persistent write.
    """
    if not attestation_id or len(attestation_id) > 128:
        raise ValueError("invalid attestation_id")
    if witness_principal_id != record.witness_id:
        raise ValueError("record witness and principal mismatch")
    if (
        not isinstance(witness_sequence, int)
        or isinstance(witness_sequence, bool)
        or witness_sequence <= 0
    ):
        raise ValueError("witness_sequence must be positive")
    if witnessed_at.tzinfo is None:
        raise ValueError("witnessed_at must be timezone-aware")
    if (
        not record.record_path.is_file()
        or record.record_path.is_symlink()
        or hashlib.sha256(record.record_path.read_bytes()).hexdigest()
        != record.signed_receipt_sha256
    ):
        raise ValueError("witness record is missing or changed")
    payload = _canonical_json(
        {
            "attestation_id": attestation_id,
            "audit_head_digest": record.audit_head_digest,
            "schema_version": "witness-attestation/1.0",
            "signed_receipt_sha256": record.signed_receipt_sha256,
            "witness_principal_id": witness_principal_id,
            "witness_sequence": witness_sequence,
            "witnessed_at": witnessed_at.astimezone(timezone.utc).isoformat(),
        }
    )
    if admitted_signer is not None:
        if (
            admitted_signer.key_record.key_id != witness_key_id
            or admitted_signer.private_key is not witness_private_key
            or admitted_signer.key_record.principal_id
            != witness_principal_id
        ):
            raise ValueError("admitted witness does not match attestation")
        return admitted_signer.sign_payload(payload, issued_at=witnessed_at)
    return sign_payload_ed25519(
        payload,
        key_id=witness_key_id,
        private_key=witness_private_key,
        issued_at=witnessed_at,
    )


def verify_witness_attestation(
    signed_attestation_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedWitnessAttestation | None, tuple[str, ...]]:
    """Verify a fresh witness attestation against the active witness role.

    ``signature_max_age`` bounds the signed envelope and ``now`` supplies an
    optional timezone-aware verification time. Trust binding, schema, identity,
    sequence, and record fields must all validate. Failure returns ``None`` and
    stable reason codes without changing witness state.
    """
    verified = verify_role_signed_payload(
        signed_attestation_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.WITNESS_SIGNER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=now,
    )
    if verified.payload_json is None or verified.key_record is None:
        return None, verified.reason_codes
    try:
        data = _strict_object(verified.payload_json)
        if set(data) != {
            "attestation_id",
            "audit_head_digest",
            "schema_version",
            "signed_receipt_sha256",
            "witness_principal_id",
            "witness_sequence",
            "witnessed_at",
        }:
            raise ValueError("unexpected witness fields")
        if data["schema_version"] != "witness-attestation/1.0":
            raise ValueError("unsupported witness schema")
        attestation_id = _identifier(data["attestation_id"])
        principal_id = _identifier(data["witness_principal_id"])
        if principal_id != verified.key_record.principal_id:
            return None, ("WITNESS_PRINCIPAL_MISMATCH",)
        sequence = data["witness_sequence"]
        if (
            not isinstance(sequence, int)
            or isinstance(sequence, bool)
            or sequence <= 0
        ):
            raise ValueError("invalid witness sequence")
        head = _digest(data["audit_head_digest"])
        receipt_digest = _digest(data["signed_receipt_sha256"])
        witnessed_at = _time(data["witnessed_at"])
    except (TypeError, ValueError, json.JSONDecodeError):
        return None, ("WITNESS_ATTESTATION_INVALID",)
    return (
        VerifiedWitnessAttestation(
            attestation_id,
            principal_id,
            verified.key_record.key_id,
            sequence,
            head,
            receipt_digest,
            witnessed_at,
        ),
        (),
    )


def assess_authenticated_witness_quorum(
    signed_attestations: Sequence[str],
    *,
    trust_bundle: VerifiedTrustBundle,
    audit_head_digest: str,
    signed_receipt_sha256: str,
    minimum_principals: int,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> AuthenticatedWitnessQuorum:
    if minimum_principals < 2:
        return AuthenticatedWitnessQuorum(
            False,
            (),
            ("AUTHENTICATED_WITNESS_QUORUM_CONFIG_INVALID",),
        )
    principals: set[str] = set()
    invalid_seen = False
    for signed in signed_attestations:
        attestation, reasons = verify_witness_attestation(
            signed,
            trust_bundle=trust_bundle,
            signature_max_age=signature_max_age,
            now=now,
        )
        if attestation is None:
            invalid_seen = invalid_seen or bool(reasons)
            continue
        if (
            attestation.audit_head_digest == audit_head_digest
            and attestation.signed_receipt_sha256 == signed_receipt_sha256
        ):
            principals.add(attestation.witness_principal_id)
    principal_ids = tuple(sorted(principals))
    if len(principal_ids) < minimum_principals:
        reasons = ["AUTHENTICATED_WITNESS_QUORUM_NOT_REACHED"]
        if invalid_seen:
            reasons.append("INVALID_WITNESS_ATTESTATION_IGNORED")
        return AuthenticatedWitnessQuorum(False, principal_ids, tuple(reasons))
    return AuthenticatedWitnessQuorum(True, principal_ids, ())


def _strict_object(text: str) -> dict[str, object]:
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate field")
            result[key] = value
        return result

    data = json.loads(text, object_pairs_hook=pairs_hook)
    if not isinstance(data, dict):
        raise ValueError("object required")
    return data


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def _identifier(value: object) -> str:
    if not isinstance(value, str) or not value or len(value) > 128:
        raise ValueError("invalid identifier")
    return value


def _digest(value: object) -> str:
    if not isinstance(value, str) or not _SHA256.fullmatch(value):
        raise ValueError("invalid digest")
    return value


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("invalid time")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)
