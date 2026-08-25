"""Apply role, validity, and revocation policy to observation and anchor checks."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

from note.poc_horizontal_ai.safety_kernel.observer_protocol import (
    ObservationRequest,
)

from .role_verification import verify_role_signed_payload
from .signed_boundary import (
    SignedAnchorReceiptResult,
    SignedObservationResult,
    _verify_signed_anchor_receipt,
    verify_signed_observation,
)
from .trust_bundle import KeyRole, VerifiedTrustBundle


def verify_trusted_observation(
    signed_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    request: ObservationRequest,
    repository_root: Path,
    expected_observer_id: str,
    signature_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> SignedObservationResult:
    """Verify an observer-role signature before validating observation content.

    The signature must be fresh, active for the observer role, and bound to the
    exact ``trust_bundle``. The decoded observation must then answer ``request``
    within ``repository_root``, observer identity, and observation-age bounds.
    Failure returns no evidence with reason codes; no trust state is changed.
    """
    current = now or datetime.now(timezone.utc)
    role = verify_role_signed_payload(
        signed_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.OBSERVER_SIGNER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=current,
    )
    if role.payload_json is None or role.key_record is None:
        return SignedObservationResult(None, role.reason_codes)
    return verify_signed_observation(
        signed_json,
        request=request,
        repository_root=repository_root,
        expected_observer_id=expected_observer_id,
        trusted_public_keys={role.key_record.key_id: role.key_record.public_key},
        signature_max_age=signature_max_age,
        observation_max_age=observation_max_age,
        now=current,
    )


def verify_trusted_anchor_receipt(
    signed_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    expected_bundle_json: str | None = None,
    now: datetime | None = None,
) -> SignedAnchorReceiptResult:
    """Verify an anchor-role signature and the enclosed anchor receipt.

    The signature must be fresh, active for the anchor role, and bound to the
    exact trust bundle. ``expected_bundle_json`` optionally requires the receipt
    to anchor that audit bundle. Failure returns no receipt with reason codes;
    verification does not append an anchor or alter the ledger.
    """
    current = now or datetime.now(timezone.utc)
    role = verify_role_signed_payload(
        signed_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.ANCHOR_SIGNER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=current,
    )
    if role.payload_json is None or role.key_record is None:
        return SignedAnchorReceiptResult(None, role.reason_codes)
    return _verify_signed_anchor_receipt(
        signed_json,
        trusted_public_keys={role.key_record.key_id: role.key_record.public_key},
        signature_max_age=signature_max_age,
        expected_bundle_json=expected_bundle_json,
        now=current,
    )
