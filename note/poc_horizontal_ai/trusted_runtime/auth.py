"""HMAC-authenticated transport envelope for the trusted-runtime PoC."""

from __future__ import annotations

import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Mapping


_MAX_AUTHENTICATED_BYTES = 128 * 1024


@dataclass(frozen=True, slots=True)
class AuthenticatedPayloadResult:
    payload_json: str | None
    key_id: str | None
    reason_codes: tuple[str, ...]


def derive_subkey(master_key: bytes, context: str) -> bytes:
    if not isinstance(master_key, bytes) or len(master_key) < 32:
        raise ValueError("master_key must contain at least 32 bytes")
    if not context or len(context) > 128:
        raise ValueError("invalid subkey context")
    return hmac.new(
        master_key,
        f"nra-trusted-runtime/{context}".encode("utf-8"),
        hashlib.sha256,
    ).digest()


def authenticate_payload(
    payload_json: str,
    *,
    key_id: str,
    secret_key: bytes,
    issued_at: datetime,
) -> str:
    _validate_key(key_id, secret_key)
    if issued_at.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    payload_digest = _sha256(payload_json)
    signed_fields = {
        "algorithm": "HMAC-SHA256",
        "issued_at": issued_at.astimezone(timezone.utc).isoformat(),
        "key_id": key_id,
        "payload_json": payload_json,
        "payload_sha256": payload_digest,
        "schema_version": "authenticated-payload/1.0",
    }
    mac = hmac.new(
        secret_key,
        _canonical_json(signed_fields).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return _canonical_json({**signed_fields, "mac": mac})


def verify_authenticated_payload(
    envelope_json: str,
    *,
    trusted_keys: Mapping[str, bytes],
    max_age: timedelta,
    now: datetime | None = None,
) -> AuthenticatedPayloadResult:
    """Verify one strict HMAC-SHA256 envelope and its freshness boundary.

    ``trusted_keys`` maps accepted key identifiers to secret keys,
    ``max_age`` must be positive, and ``now`` must be timezone-aware when
    supplied. Unknown keys, malformed envelopes, digest or MAC mismatches, and
    stale or future timestamps return no payload with reason codes. The input
    mapping and persistent state are not modified.
    """
    current_time = now or datetime.now(timezone.utc)
    if max_age <= timedelta(0) or current_time.tzinfo is None:
        return AuthenticatedPayloadResult(
            None,
            None,
            ("AUTH_VERIFIER_CONFIG_INVALID",),
        )
    try:
        data = _strict_object(envelope_json)
        if set(data) != {
            "algorithm",
            "issued_at",
            "key_id",
            "mac",
            "payload_json",
            "payload_sha256",
            "schema_version",
        }:
            raise ValueError("unexpected authenticated fields")
        if (
            data["schema_version"] != "authenticated-payload/1.0"
            or data["algorithm"] != "HMAC-SHA256"
        ):
            raise ValueError("unsupported authentication contract")
        key_id = _strict_str(data["key_id"])
        payload_json = _strict_str(data["payload_json"])
        payload_sha256 = _strict_str(data["payload_sha256"])
        provided_mac = _strict_str(data["mac"])
        issued_at_text = _strict_str(data["issued_at"])
        issued_at = _parse_time(issued_at_text)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return AuthenticatedPayloadResult(None, None, ("AUTH_ENVELOPE_INVALID",))

    secret_key = trusted_keys.get(key_id)
    if secret_key is None:
        return AuthenticatedPayloadResult(None, key_id, ("AUTH_KEY_UNKNOWN",))
    try:
        _validate_key(key_id, secret_key)
    except ValueError:
        return AuthenticatedPayloadResult(
            None,
            key_id,
            ("AUTH_KEY_CONFIGURATION_INVALID",),
        )
    reasons: list[str] = []
    if payload_sha256 != _sha256(payload_json):
        reasons.append("AUTH_PAYLOAD_DIGEST_MISMATCH")
    signed_fields = {
        "algorithm": "HMAC-SHA256",
        "issued_at": issued_at_text,
        "key_id": key_id,
        "payload_json": payload_json,
        "payload_sha256": payload_sha256,
        "schema_version": "authenticated-payload/1.0",
    }
    expected_mac = hmac.new(
        secret_key,
        _canonical_json(signed_fields).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(provided_mac, expected_mac):
        reasons.append("AUTH_MAC_MISMATCH")
    current_time = current_time.astimezone(timezone.utc)
    if issued_at > current_time + timedelta(seconds=1):
        reasons.append("AUTH_TIME_IN_FUTURE")
    if current_time - issued_at > max_age:
        reasons.append("AUTH_ENVELOPE_STALE")
    return AuthenticatedPayloadResult(
        payload_json if not reasons else None,
        key_id,
        tuple(reasons),
    )


def _validate_key(key_id: str, secret_key: bytes) -> None:
    if not key_id or len(key_id) > 128:
        raise ValueError("invalid key_id")
    if not isinstance(secret_key, bytes) or len(secret_key) < 32:
        raise ValueError("secret_key must contain at least 32 bytes")


def _strict_object(text: str) -> dict[str, object]:
    if len(text.encode("utf-8")) > _MAX_AUTHENTICATED_BYTES:
        raise ValueError("authenticated envelope too large")

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


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def _strict_str(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("string required")
    return value
