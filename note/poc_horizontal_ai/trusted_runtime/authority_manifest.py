"""Signed attestation of the declared execution authority placement."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519
from .deployment_boundary import RuntimePlacement
from .role_verification import verify_role_signed_payload
from .trust_bundle import KeyRole, VerifiedTrustBundle


@dataclass(frozen=True, slots=True)
class AuthorityManifestQuorum:
    satisfied: bool
    manifest_id: str | None
    placement_sha256: str | None
    principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


def authority_placement_sha256(placement: RuntimePlacement) -> str:
    if placement.execution_authorization_database_path is None:
        raise ValueError("EXECUTION_AUTHORITY_PLACEMENT_NOT_APPLICABLE")
    data = {
        "execution_integrity_key_authority_domain": (
            placement.execution_integrity_key_authority_domain
        ),
        "execution_journal_authority_domain": (
            placement.execution_journal_authority_domain
        ),
        "execution_journal_path": str(
            placement.execution_authorization_database_path.resolve()
        ),
        "observer_trust_root_authority_domains": list(
            placement.observer_trust_root_authority_domains
        ),
        "schema_version": "execution-authority-placement/1.0",
    }
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def create_signed_authority_manifest_attestation(
    *,
    placement: RuntimePlacement,
    manifest_id: str,
    attestation_id: str,
    signing_key_id: str,
    signing_private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    attested_at: datetime,
    valid_until: datetime,
) -> str:
    if (
        not _identifier(manifest_id)
        or not _identifier(attestation_id)
        or attested_at.tzinfo is None
        or valid_until.tzinfo is None
        or valid_until <= attested_at
    ):
        raise ValueError("invalid authority manifest attestation")
    record = trust_bundle.record_for(signing_key_id)
    if (
        record is None
        or record.role is not KeyRole.AUTHORITY_ATTESTER
        or not record.active_at(attested_at)
        or public_key_fingerprint(record.public_key)
        != public_key_fingerprint(signing_private_key.public_key())
    ):
        raise ValueError("AUTHORITY_ATTESTER_ROLE_OR_KEY_MISMATCH")
    payload = _canonical_json(
        {
            "attestation_id": attestation_id,
            "attested_at": _time_text(attested_at),
            "manifest_id": manifest_id,
            "placement_sha256": authority_placement_sha256(placement),
            "schema_version": "execution-authority-manifest-attestation/1.0",
            "valid_until": _time_text(valid_until),
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=signing_key_id,
        private_key=signing_private_key,
        issued_at=attested_at,
        trust_bundle_generation=trust_bundle.generation,
        trust_bundle_sha256=trust_bundle.signed_bundle_sha256,
    )


def assess_authority_manifest_quorum(
    signed_attestations: tuple[str, ...],
    *,
    placement: RuntimePlacement,
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> AuthorityManifestQuorum:
    """Verify fresh attestations agreeing on one exact runtime placement.

    ``minimum_principals`` counts distinct trusted authority principals, not
    signatures. Invalid attestations are ignored but reported; any placement
    digest disagreement prevents quorum. ``now`` may provide a timezone-aware
    verification time. The function returns evidence only and performs no
    deployment or persistent-state update.
    """
    current = now or datetime.now(timezone.utc)
    if (
        current.tzinfo is None
        or not isinstance(signed_attestations, tuple)
        or not signed_attestations
        or not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
    ):
        return AuthorityManifestQuorum(False, None, None, (), ("AUTHORITY_MANIFEST_QUORUM_CONFIG_INVALID",))
    expected_digest = authority_placement_sha256(placement)
    principals = set()
    agreement = None
    invalid = False
    mismatch = False
    for signed in signed_attestations:
        verified = verify_role_signed_payload(
            signed,
            trust_bundle=trust_bundle,
            required_role=KeyRole.AUTHORITY_ATTESTER,
            signature_max_age=signature_max_age,
            require_trust_binding=True,
            now=current,
        )
        if verified.payload_json is None or verified.key_record is None:
            invalid = True
            continue
        try:
            data = json.loads(verified.payload_json, object_pairs_hook=_pairs_hook)
            if not isinstance(data, dict) or set(data) != {
                "attestation_id", "attested_at", "manifest_id",
                "placement_sha256", "schema_version", "valid_until",
            }:
                raise ValueError
            if data["schema_version"] != "execution-authority-manifest-attestation/1.0":
                raise ValueError
            _identifier(data["attestation_id"])
            manifest_id = _identifier(data["manifest_id"])
            placement_digest = _digest(data["placement_sha256"])
            attested_at = _time(data["attested_at"])
            valid_until = _time(data["valid_until"])
            if valid_until <= attested_at or current.astimezone(timezone.utc) >= valid_until:
                raise ValueError
        except (TypeError, ValueError, json.JSONDecodeError):
            invalid = True
            continue
        item_agreement = (manifest_id, placement_digest, valid_until)
        if placement_digest != expected_digest or (
            agreement is not None and item_agreement != agreement
        ):
            mismatch = True
            continue
        agreement = item_agreement
        principals.add(verified.key_record.principal_id)
    principal_ids = tuple(sorted(principals))
    if agreement is None or len(principal_ids) < minimum_principals:
        reasons = ["AUTHORITY_MANIFEST_QUORUM_NOT_REACHED"]
        if invalid:
            reasons.append("INVALID_AUTHORITY_MANIFEST_ATTESTATION_IGNORED")
        if mismatch:
            reasons.append("AUTHORITY_MANIFEST_PLACEMENT_MISMATCH")
        return AuthorityManifestQuorum(False, None, None, principal_ids, tuple(reasons))
    return AuthorityManifestQuorum(True, agreement[0], agreement[1], principal_ids, ())


def _identifier(value: object) -> str:
    if not isinstance(value, str) or not 0 < len(value) <= 128 or any(character.isspace() for character in value):
        raise ValueError
    return value


def _digest(value: object) -> str:
    if not isinstance(value, str) or len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError
    return value


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.astimezone(timezone.utc)


def _time_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError
        result[key] = value
    return result


def _canonical_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
