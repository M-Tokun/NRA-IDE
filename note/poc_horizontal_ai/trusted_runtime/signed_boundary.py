"""Ed25519 observation and audit-anchor compositions."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Mapping

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from note.poc_horizontal_ai.safety_kernel import (
    AuthoritativeEvidence,
    verify_audit_bundle,
)
from note.poc_horizontal_ai.safety_kernel.observer_protocol import (
    ObservationRequest,
    decode_observation_request,
    encode_observation_request,
    serve_observation_request,
    verify_observation_envelope,
)

from .anchor_store import AnchorReceipt, AuditAnchorStore
from .asymmetric_auth import (
    public_key_fingerprint,
    sign_payload_ed25519,
    verify_signed_payload_ed25519,
)
from .nonce_store import PersistentNonceStore
from .runtime_admission import AdmittedSigner
from .trust_bundle import KeyRole


_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class SignedObservationResult:
    evidence: AuthoritativeEvidence | None
    reason_codes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SignedAnchorReceiptResult:
    receipt: AnchorReceipt | None
    reason_codes: tuple[str, ...]


def process_signed_observation_request(
    request_json: str,
    *,
    repository_root: Path,
    observer_id: str,
    nonce_store: PersistentNonceStore,
    signing_key_id: str,
    signing_key: Ed25519PrivateKey,
    admitted_signer: AdmittedSigner | None = None,
    request_max_age: timedelta,
    now: datetime | None = None,
) -> str:
    current_time = _current_utc(now)
    request = decode_observation_request(request_json)
    _validate_request_time(request, current_time, request_max_age)
    canonical_request = encode_observation_request(request)
    consumed = nonce_store.consume(
        request_id=request.request_id,
        nonce=request.nonce,
        issued_at=request.issued_at,
        request_digest=hashlib.sha256(
            canonical_request.encode("utf-8")
        ).hexdigest(),
        consumed_at=current_time,
    )
    if not consumed.accepted:
        raise ValueError(",".join(consumed.reason_codes))
    payload = serve_observation_request(
        canonical_request,
        repository_root=repository_root,
        observer_id=observer_id,
    )
    if admitted_signer is not None:
        if (
            admitted_signer.key_record.key_id != signing_key_id
            or admitted_signer.private_key is not signing_key
        ):
            raise ValueError("admitted signer does not match signing arguments")
        return admitted_signer.sign_payload(payload, issued_at=current_time)
    return sign_payload_ed25519(
        payload,
        key_id=signing_key_id,
        private_key=signing_key,
        issued_at=current_time,
    )


def verify_signed_observation(
    signed_json: str,
    *,
    request: ObservationRequest,
    repository_root: Path,
    expected_observer_id: str,
    trusted_public_keys: Mapping[str, Ed25519PublicKey],
    signature_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> SignedObservationResult:
    """Verify a signed observation and its exact request/path binding.

    ``trusted_public_keys`` defines accepted signers. Signature age and
    observation age are independent bounds; repository root, observer identity,
    request digest, resolved path, snapshot digest, and file hash are all
    checked. Any mismatch returns no observation with reason codes. The
    verifier is read-only and does not confer Cause-Side authority on output.
    """
    signed = verify_signed_payload_ed25519(
        signed_json,
        trusted_public_keys=trusted_public_keys,
        max_age=signature_max_age,
        now=now,
    )
    if signed.payload_json is None:
        return SignedObservationResult(None, signed.reason_codes)
    observation = verify_observation_envelope(
        signed.payload_json,
        request=request,
        repository_root=repository_root,
        expected_observer_id=expected_observer_id,
        max_age=observation_max_age,
        now=now,
    )
    return SignedObservationResult(
        observation.evidence,
        observation.reason_codes,
    )


def anchor_and_sign_bundle(
    bundle_json: str,
    *,
    anchor_id: str,
    anchor_store: AuditAnchorStore,
    admitted_signer: AdmittedSigner,
    now: datetime | None = None,
) -> str:
    current_time = _current_utc(now)
    verification = verify_audit_bundle(bundle_json)
    if verification.events is None or verification.head_digest is None:
        raise ValueError("invalid audit bundle")
    if not isinstance(admitted_signer, AdmittedSigner):
        raise ValueError("ANCHOR_SIGNER_ADMISSION_REQUIRED")
    record = admitted_signer.key_record
    if record.role is not KeyRole.ANCHOR_SIGNER:
        raise ValueError("ANCHOR_SIGNER_ROLE_MISMATCH")
    trusted_record = admitted_signer.trust_bundle.record_for(record.key_id)
    if (
        trusted_record is None
        or trusted_record.principal_id != record.principal_id
        or trusted_record.role is not record.role
        or trusted_record.valid_from != record.valid_from
        or trusted_record.valid_until != record.valid_until
        or trusted_record.revoked_at != record.revoked_at
        or public_key_fingerprint(trusted_record.public_key)
        != public_key_fingerprint(record.public_key)
    ):
        raise ValueError("ANCHOR_SIGNER_TRUST_RECORD_MISMATCH")
    if not trusted_record.active_at(current_time):
        raise ValueError("ANCHOR_SIGNER_KEY_NOT_ACTIVE")
    if public_key_fingerprint(admitted_signer.private_key.public_key()) != (
        public_key_fingerprint(trusted_record.public_key)
    ):
        raise ValueError("ANCHOR_SIGNER_PRIVATE_KEY_MISMATCH")

    def sign_receipt(receipt: AnchorReceipt) -> str:
        payload = _canonical_json(
            {
                **asdict(receipt),
                "schema_version": "anchor-receipt/2.0",
            }
        )
        return admitted_signer.sign_payload(
            payload,
            issued_at=current_time,
        )

    return anchor_store.append_finalized(
        anchor_id=anchor_id,
        audit_head_digest=verification.head_digest,
        event_count=len(verification.events),
        bundle_sha256=hashlib.sha256(bundle_json.encode("utf-8")).hexdigest(),
        anchored_at=current_time,
        finalizer=sign_receipt,
    )


def _verify_signed_anchor_receipt(
    signed_json: str,
    *,
    trusted_public_keys: Mapping[str, Ed25519PublicKey],
    signature_max_age: timedelta,
    expected_bundle_json: str | None = None,
    now: datetime | None = None,
) -> SignedAnchorReceiptResult:
    signed = verify_signed_payload_ed25519(
        signed_json,
        trusted_public_keys=trusted_public_keys,
        max_age=signature_max_age,
        now=now,
    )
    if signed.payload_json is None:
        return SignedAnchorReceiptResult(None, signed.reason_codes)
    try:
        data = _strict_object(signed.payload_json)
        if set(data) != {
            "anchor_id",
            "anchored_at",
            "audit_head_digest",
            "bundle_sha256",
            "event_count",
            "previous_receipt_mac",
            "receipt_mac",
            "schema_version",
            "sequence",
        }:
            raise ValueError("unexpected receipt fields")
        if data.pop("schema_version") != "anchor-receipt/2.0":
            raise ValueError("unsupported receipt schema")
        receipt = _decode_receipt(data)
    except (TypeError, ValueError, json.JSONDecodeError):
        return SignedAnchorReceiptResult(None, ("SIGNED_RECEIPT_INVALID",))
    reasons: list[str] = []
    if expected_bundle_json is not None:
        bundle = verify_audit_bundle(
            expected_bundle_json,
            expected_head_digest=receipt.audit_head_digest,
        )
        if bundle.events is None:
            reasons.append("SIGNED_RECEIPT_BUNDLE_MISMATCH")
        if receipt.bundle_sha256 != hashlib.sha256(
            expected_bundle_json.encode("utf-8")
        ).hexdigest():
            reasons.append("SIGNED_RECEIPT_BUNDLE_DIGEST_MISMATCH")
        if bundle.events is not None and receipt.event_count != len(bundle.events):
            reasons.append("SIGNED_RECEIPT_EVENT_COUNT_MISMATCH")
    return SignedAnchorReceiptResult(
        receipt if not reasons else None,
        tuple(dict.fromkeys(reasons)),
    )


def _validate_request_time(
    request: ObservationRequest,
    current_time: datetime,
    max_age: timedelta,
) -> None:
    if max_age <= timedelta(0):
        raise ValueError("invalid request max age")
    issued_at = request.issued_at.astimezone(timezone.utc)
    if issued_at > current_time + timedelta(seconds=1):
        raise ValueError("request time is in the future")
    if current_time - issued_at > max_age:
        raise ValueError("request is stale")


def _current_utc(value: datetime | None) -> datetime:
    current = value or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("current time must be timezone-aware")
    return current.astimezone(timezone.utc)


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


def _decode_receipt(data: dict[str, object]) -> AnchorReceipt:
    sequence = data["sequence"]
    event_count = data["event_count"]
    previous = data["previous_receipt_mac"]
    if (
        not isinstance(sequence, int)
        or isinstance(sequence, bool)
        or sequence <= 0
        or not isinstance(event_count, int)
        or isinstance(event_count, bool)
        or event_count <= 0
        or not isinstance(previous, (str, type(None)))
    ):
        raise ValueError("invalid receipt numeric or chain fields")
    strings = {
        name: data[name]
        for name in (
            "anchor_id",
            "anchored_at",
            "audit_head_digest",
            "bundle_sha256",
            "receipt_mac",
        )
    }
    if any(not isinstance(value, str) or not value for value in strings.values()):
        raise ValueError("invalid receipt string fields")
    if not _SHA256.fullmatch(strings["audit_head_digest"]):
        raise ValueError("invalid audit head digest")
    if not _SHA256.fullmatch(strings["bundle_sha256"]):
        raise ValueError("invalid bundle digest")
    if not _SHA256.fullmatch(strings["receipt_mac"]):
        raise ValueError("invalid receipt mac")
    if previous is not None and not _SHA256.fullmatch(previous):
        raise ValueError("invalid previous receipt mac")
    anchored_at = datetime.fromisoformat(strings["anchored_at"])
    if anchored_at.tzinfo is None:
        raise ValueError("receipt time requires timezone")
    return AnchorReceipt(
        sequence=sequence,
        anchor_id=strings["anchor_id"],
        audit_head_digest=strings["audit_head_digest"],
        event_count=event_count,
        bundle_sha256=strings["bundle_sha256"],
        anchored_at=strings["anchored_at"],
        previous_receipt_mac=previous,
        receipt_mac=strings["receipt_mac"],
    )
