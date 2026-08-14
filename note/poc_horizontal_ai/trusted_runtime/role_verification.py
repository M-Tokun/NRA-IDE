"""Verify a signature only when its key is active for the required role."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from .asymmetric_auth import verify_signed_payload_ed25519
from .trust_bundle import KeyRole, TrustedKeyRecord, VerifiedTrustBundle


@dataclass(frozen=True, slots=True)
class RoleSignedPayloadResult:
    payload_json: str | None
    key_record: TrustedKeyRecord | None
    reason_codes: tuple[str, ...]


def verify_role_signed_payload(
    signed_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    required_role: KeyRole,
    signature_max_age: timedelta,
    require_trust_binding: bool = False,
    now: datetime | None = None,
) -> RoleSignedPayloadResult:
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        return RoleSignedPayloadResult(
            None,
            None,
            ("ROLE_VERIFIER_TIME_INVALID",),
        )
    active_keys = trust_bundle.active_public_keys(required_role, current)
    signed = verify_signed_payload_ed25519(
        signed_json,
        trusted_public_keys=active_keys,
        max_age=signature_max_age,
        now=current,
    )
    if signed.payload_json is None:
        reason_codes = signed.reason_codes
        if signed.key_id is not None:
            record = trust_bundle.record_for(signed.key_id)
            if record is not None and record.role is not required_role:
                reason_codes = tuple(
                    dict.fromkeys((*reason_codes, "SIGNATURE_ROLE_MISMATCH"))
                )
            elif record is not None and not record.active_at(current):
                reason_codes = tuple(
                    dict.fromkeys((*reason_codes, "SIGNATURE_KEY_NOT_ACTIVE"))
                )
        return RoleSignedPayloadResult(None, None, reason_codes)
    assert signed.key_id is not None
    record = trust_bundle.record_for(signed.key_id)
    if record is None or record.role is not required_role or not record.active_at(current):
        return RoleSignedPayloadResult(
            None,
            None,
            ("SIGNATURE_KEY_NOT_ACTIVE_FOR_ROLE",),
        )
    if require_trust_binding:
        if (
            signed.trust_bundle_generation is None
            or signed.trust_bundle_sha256 is None
        ):
            return RoleSignedPayloadResult(
                None,
                None,
                ("TRUST_STATE_BINDING_REQUIRED",),
            )
        if (
            signed.trust_bundle_generation != trust_bundle.generation
            or signed.trust_bundle_sha256 != trust_bundle.signed_bundle_sha256
        ):
            return RoleSignedPayloadResult(
                None,
                None,
                ("TRUST_STATE_BINDING_MISMATCH",),
            )
    return RoleSignedPayloadResult(signed.payload_json, record, ())
