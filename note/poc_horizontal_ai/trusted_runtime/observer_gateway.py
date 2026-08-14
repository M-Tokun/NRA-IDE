"""Authenticated, replay-resistant observer gateway composition."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Mapping

from note.poc_horizontal_ai.safety_kernel import AuthoritativeEvidence
from note.poc_horizontal_ai.safety_kernel.observer_protocol import (
    ObservationRequest,
    decode_observation_request,
    encode_observation_request,
    serve_observation_request,
    verify_observation_envelope,
)

from .auth import authenticate_payload, verify_authenticated_payload
from .nonce_store import PersistentNonceStore


@dataclass(frozen=True, slots=True)
class AuthenticatedObservationResult:
    evidence: AuthoritativeEvidence | None
    reason_codes: tuple[str, ...]


def process_observation_request(
    request_json: str,
    *,
    repository_root: Path,
    observer_id: str,
    nonce_store: PersistentNonceStore,
    key_id: str,
    secret_key: bytes,
    request_max_age: timedelta,
    now: datetime | None = None,
) -> str:
    current_time = now or datetime.now(timezone.utc)
    request = decode_observation_request(request_json)
    if current_time.tzinfo is None or request_max_age <= timedelta(0):
        raise ValueError("invalid gateway time configuration")
    current_time = current_time.astimezone(timezone.utc)
    issued_at = request.issued_at.astimezone(timezone.utc)
    if issued_at > current_time + timedelta(seconds=1):
        raise ValueError("request time is in the future")
    if current_time - issued_at > request_max_age:
        raise ValueError("request is stale")
    canonical_request = encode_observation_request(request)
    consume = nonce_store.consume(
        request_id=request.request_id,
        nonce=request.nonce,
        issued_at=request.issued_at,
        request_digest=hashlib.sha256(
            canonical_request.encode("utf-8")
        ).hexdigest(),
        consumed_at=current_time,
    )
    if not consume.accepted:
        raise ValueError(",".join(consume.reason_codes))
    payload = serve_observation_request(
        canonical_request,
        repository_root=repository_root,
        observer_id=observer_id,
    )
    return authenticate_payload(
        payload,
        key_id=key_id,
        secret_key=secret_key,
        issued_at=current_time,
    )


def verify_authenticated_observation(
    authenticated_json: str,
    *,
    request: ObservationRequest,
    repository_root: Path,
    expected_observer_id: str,
    trusted_keys: Mapping[str, bytes],
    authentication_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> AuthenticatedObservationResult:
    authenticated = verify_authenticated_payload(
        authenticated_json,
        trusted_keys=trusted_keys,
        max_age=authentication_max_age,
        now=now,
    )
    if authenticated.payload_json is None:
        return AuthenticatedObservationResult(None, authenticated.reason_codes)
    observation = verify_observation_envelope(
        authenticated.payload_json,
        request=request,
        repository_root=repository_root,
        expected_observer_id=expected_observer_id,
        max_age=observation_max_age,
        now=now,
    )
    return AuthenticatedObservationResult(
        observation.evidence,
        observation.reason_codes,
    )
