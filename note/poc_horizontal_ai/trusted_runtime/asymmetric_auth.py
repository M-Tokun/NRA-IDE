"""Ed25519 signing boundary with public-key-only verification."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)


_MAX_SIGNED_BYTES = 128 * 1024


@dataclass(frozen=True, slots=True)
class SignedPayloadResult:
    payload_json: str | None
    key_id: str | None
    public_key_fingerprint: str | None
    reason_codes: tuple[str, ...]
    trust_bundle_generation: int | None = None
    trust_bundle_sha256: str | None = None


def sign_payload_ed25519(
    payload_json: str,
    *,
    key_id: str,
    private_key: Ed25519PrivateKey,
    issued_at: datetime,
    trust_bundle_generation: int | None = None,
    trust_bundle_sha256: str | None = None,
) -> str:
    _validate_key_id(key_id)
    if not isinstance(private_key, Ed25519PrivateKey):
        raise ValueError("Ed25519 private key is required")
    if issued_at.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")
    public_key = private_key.public_key()
    trust_bound = (
        trust_bundle_generation is not None or trust_bundle_sha256 is not None
    )
    if trust_bound:
        if (
            not isinstance(trust_bundle_generation, int)
            or isinstance(trust_bundle_generation, bool)
            or trust_bundle_generation <= 0
            or not _is_sha256(trust_bundle_sha256)
        ):
            raise ValueError("invalid trust state binding")
    signed_fields: dict[str, object] = {
        "algorithm": "Ed25519",
        "issued_at": issued_at.astimezone(timezone.utc).isoformat(),
        "key_id": key_id,
        "payload_json": payload_json,
        "payload_sha256": _sha256(payload_json),
        "public_key_fingerprint": public_key_fingerprint(public_key),
        "schema_version": (
            "signed-payload/1.1" if trust_bound else "signed-payload/1.0"
        ),
    }
    if trust_bound:
        signed_fields["trust_bundle_generation"] = trust_bundle_generation
        signed_fields["trust_bundle_sha256"] = trust_bundle_sha256
    signature = private_key.sign(_canonical_json(signed_fields).encode("utf-8"))
    return _canonical_json(
        {
            **signed_fields,
            "signature_base64": base64.b64encode(signature).decode("ascii"),
        }
    )


def verify_signed_payload_ed25519(
    envelope_json: str,
    *,
    trusted_public_keys: Mapping[str, Ed25519PublicKey],
    max_age: timedelta | None,
    now: datetime | None = None,
) -> SignedPayloadResult:
    """Verify one strict Ed25519 envelope against the supplied trusted keys.

    ``trusted_public_keys`` maps accepted key identifiers to public keys.
    ``max_age`` limits signature age when non-None, and ``now`` must be
    timezone-aware when supplied. Schema, digest, fingerprint, signature, key,
    or time failures return no payload with reason codes. Version 1.1 trust
    binding fields are verified as signed data but interpreted by the caller.
    """
    current_time = now or datetime.now(timezone.utc)
    if (
        (max_age is not None and max_age <= timedelta(0))
        or current_time.tzinfo is None
    ):
        return SignedPayloadResult(
            None,
            None,
            None,
            ("SIGNATURE_VERIFIER_CONFIG_INVALID",),
        )
    try:
        data = _strict_object(envelope_json)
        base_fields = {
            "algorithm",
            "issued_at",
            "key_id",
            "payload_json",
            "payload_sha256",
            "public_key_fingerprint",
            "schema_version",
            "signature_base64",
        }
        schema_version = data.get("schema_version")
        trust_fields = {"trust_bundle_generation", "trust_bundle_sha256"}
        if schema_version == "signed-payload/1.0" and set(data) == base_fields:
            trust_generation = None
            trust_digest = None
        elif (
            schema_version == "signed-payload/1.1"
            and set(data) == base_fields | trust_fields
        ):
            trust_generation = data["trust_bundle_generation"]
            trust_digest = data["trust_bundle_sha256"]
            if (
                not isinstance(trust_generation, int)
                or isinstance(trust_generation, bool)
                or trust_generation <= 0
                or not _is_sha256(trust_digest)
            ):
                raise ValueError("invalid trust state binding")
        else:
            raise ValueError("unexpected signed fields")
        if data["algorithm"] != "Ed25519":
            raise ValueError("unsupported signature contract")
        key_id = _strict_str(data["key_id"])
        _validate_key_id(key_id)
        payload_json = _strict_str(data["payload_json"])
        payload_sha256 = _strict_str(data["payload_sha256"])
        fingerprint = _strict_str(data["public_key_fingerprint"])
        issued_at_text = _strict_str(data["issued_at"])
        issued_at = _parse_time(issued_at_text)
        signature = base64.b64decode(
            _strict_str(data["signature_base64"]),
            validate=True,
        )
    except (binascii.Error, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return SignedPayloadResult(
            None,
            None,
            None,
            ("SIGNATURE_ENVELOPE_INVALID",),
        )

    public_key = trusted_public_keys.get(key_id)
    if public_key is None:
        return SignedPayloadResult(
            None,
            key_id,
            fingerprint,
            ("SIGNATURE_KEY_UNKNOWN",),
        )
    reasons: list[str] = []
    if payload_sha256 != _sha256(payload_json):
        reasons.append("SIGNATURE_PAYLOAD_DIGEST_MISMATCH")
    if fingerprint != public_key_fingerprint(public_key):
        reasons.append("SIGNATURE_KEY_FINGERPRINT_MISMATCH")
    signed_fields = {
        "algorithm": "Ed25519",
        "issued_at": issued_at_text,
        "key_id": key_id,
        "payload_json": payload_json,
        "payload_sha256": payload_sha256,
        "public_key_fingerprint": fingerprint,
        "schema_version": schema_version,
    }
    if trust_generation is not None:
        signed_fields["trust_bundle_generation"] = trust_generation
        signed_fields["trust_bundle_sha256"] = trust_digest
    try:
        public_key.verify(
            signature,
            _canonical_json(signed_fields).encode("utf-8"),
        )
    except InvalidSignature:
        reasons.append("SIGNATURE_INVALID")
    current_time = current_time.astimezone(timezone.utc)
    if issued_at > current_time + timedelta(seconds=1):
        reasons.append("SIGNATURE_TIME_IN_FUTURE")
    if max_age is not None and current_time - issued_at > max_age:
        reasons.append("SIGNATURE_STALE")
    return SignedPayloadResult(
        payload_json if not reasons else None,
        key_id,
        fingerprint,
        tuple(reasons),
        trust_generation,
        trust_digest,
    )


def load_ed25519_private_key(path: Path) -> Ed25519PrivateKey:
    data = _load_bounded_regular_file(path, 16 * 1024)
    key = serialization.load_pem_private_key(data, password=None)
    if not isinstance(key, Ed25519PrivateKey):
        raise ValueError("private key is not Ed25519")
    return key


def load_ed25519_public_key(path: Path) -> Ed25519PublicKey:
    data = _load_bounded_regular_file(path, 16 * 1024)
    key = serialization.load_pem_public_key(data)
    if not isinstance(key, Ed25519PublicKey):
        raise ValueError("public key is not Ed25519")
    return key


def public_key_fingerprint(public_key: Ed25519PublicKey) -> str:
    if not isinstance(public_key, Ed25519PublicKey):
        raise ValueError("Ed25519 public key is required")
    raw = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return hashlib.sha256(raw).hexdigest()


def _load_bounded_regular_file(path: Path, maximum_bytes: int) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise ValueError("key path must be a regular non-symlink file")
    size = path.stat().st_size
    if size <= 0 or size > maximum_bytes:
        raise ValueError("key file size is outside the accepted range")
    data = path.read_bytes()
    if len(data) != size:
        raise ValueError("key file changed while reading")
    return data


def _validate_key_id(key_id: str) -> None:
    if not key_id or len(key_id) > 128:
        raise ValueError("invalid key_id")


def _strict_object(text: str) -> dict[str, object]:
    if len(text.encode("utf-8")) > _MAX_SIGNED_BYTES:
        raise ValueError("signed envelope too large")

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


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
