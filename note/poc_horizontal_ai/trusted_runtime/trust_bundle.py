"""Offline-root-signed role registry with rotation and revocation semantics."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Mapping, Sequence

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from .asymmetric_auth import sign_payload_ed25519, verify_signed_payload_ed25519


class KeyRole(str, Enum):
    OBSERVER_SIGNER = "OBSERVER_SIGNER"
    ANCHOR_SIGNER = "ANCHOR_SIGNER"
    WITNESS_SIGNER = "WITNESS_SIGNER"


@dataclass(frozen=True, slots=True)
class TrustedKeySpec:
    key_id: str
    principal_id: str
    role: KeyRole
    public_key: Ed25519PublicKey
    valid_from: datetime
    valid_until: datetime
    revoked_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class TrustedKeyRecord:
    key_id: str
    principal_id: str
    role: KeyRole
    public_key: Ed25519PublicKey
    valid_from: datetime
    valid_until: datetime
    revoked_at: datetime | None

    def active_at(self, moment: datetime) -> bool:
        current = _utc(moment)
        return (
            self.valid_from <= current < self.valid_until
            and (self.revoked_at is None or current < self.revoked_at)
        )


@dataclass(frozen=True, slots=True)
class VerifiedTrustBundle:
    generation: int
    issued_at: datetime
    previous_bundle_sha256: str | None
    keys: tuple[TrustedKeyRecord, ...]
    signed_bundle_sha256: str

    def active_records(
        self,
        role: KeyRole,
        moment: datetime,
    ) -> tuple[TrustedKeyRecord, ...]:
        return tuple(
            record
            for record in self.keys
            if record.role is role and record.active_at(moment)
        )

    def active_public_keys(
        self,
        role: KeyRole,
        moment: datetime,
    ) -> dict[str, Ed25519PublicKey]:
        return {
            record.key_id: record.public_key
            for record in self.active_records(role, moment)
        }

    def record_for(self, key_id: str) -> TrustedKeyRecord | None:
        return next((record for record in self.keys if record.key_id == key_id), None)


@dataclass(frozen=True, slots=True)
class TrustBundleVerification:
    bundle: VerifiedTrustBundle | None
    reason_codes: tuple[str, ...]


def create_signed_trust_bundle(
    *,
    generation: int,
    keys: Sequence[TrustedKeySpec],
    root_key_id: str,
    root_private_key: Ed25519PrivateKey,
    issued_at: datetime,
    previous_signed_bundle_json: str | None = None,
) -> str:
    if not isinstance(generation, int) or isinstance(generation, bool) or generation <= 0:
        raise ValueError("generation must be a positive integer")
    if (generation == 1) != (previous_signed_bundle_json is None):
        raise ValueError("generation one alone must omit previous bundle")
    if not keys:
        raise ValueError("trust bundle must contain keys")
    key_payloads = [_encode_key_spec(spec) for spec in keys]
    key_ids = [payload["key_id"] for payload in key_payloads]
    if len(key_ids) != len(set(key_ids)):
        raise ValueError("duplicate trust key_id")
    public_keys = [payload["public_key_base64"] for payload in key_payloads]
    if len(public_keys) != len(set(public_keys)):
        raise ValueError("one public key cannot occupy multiple trust records")
    payload = _canonical_json(
        {
            "generation": generation,
            "issued_at": _utc(issued_at).isoformat(),
            "keys": key_payloads,
            "previous_bundle_sha256": (
                None
                if previous_signed_bundle_json is None
                else _sha256(previous_signed_bundle_json)
            ),
            "schema_version": "trust-bundle/1.0",
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=root_key_id,
        private_key=root_private_key,
        issued_at=issued_at,
    )


def verify_signed_trust_bundle(
    signed_bundle_json: str,
    *,
    pinned_root_keys: Mapping[str, Ed25519PublicKey],
    signature_max_age: timedelta | None,
    now: datetime | None = None,
) -> TrustBundleVerification:
    signed = verify_signed_payload_ed25519(
        signed_bundle_json,
        trusted_public_keys=pinned_root_keys,
        max_age=signature_max_age,
        now=now,
    )
    if signed.payload_json is None:
        return TrustBundleVerification(None, signed.reason_codes)
    try:
        data = _strict_object(signed.payload_json)
        if set(data) != {
            "generation",
            "issued_at",
            "keys",
            "previous_bundle_sha256",
            "schema_version",
        }:
            raise ValueError("unexpected trust bundle fields")
        if data["schema_version"] != "trust-bundle/1.0":
            raise ValueError("unsupported trust bundle schema")
        generation = _strict_positive_int(data["generation"])
        issued_at = _parse_time(data["issued_at"])
        previous = data["previous_bundle_sha256"]
        if previous is not None and not _is_sha256(previous):
            raise ValueError("invalid previous bundle digest")
        if generation == 1 and previous is not None:
            raise ValueError("generation one cannot have previous bundle")
        if generation > 1 and previous is None:
            raise ValueError("later generation requires previous bundle")
        key_data = data["keys"]
        if not isinstance(key_data, list) or not key_data:
            raise ValueError("keys must be a non-empty array")
        records = tuple(_decode_key_record(item) for item in key_data)
        if len({record.key_id for record in records}) != len(records):
            raise ValueError("duplicate trust key_id")
        fingerprints = tuple(
            record.public_key.public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
            for record in records
        )
        if len(set(fingerprints)) != len(fingerprints):
            raise ValueError("duplicate public key across trust records")
    except (binascii.Error, TypeError, ValueError, json.JSONDecodeError):
        return TrustBundleVerification(None, ("TRUST_BUNDLE_INVALID",))
    return TrustBundleVerification(
        VerifiedTrustBundle(
            generation,
            issued_at,
            previous,
            records,
            _sha256(signed_bundle_json),
        ),
        (),
    )


def _encode_key_spec(spec: TrustedKeySpec) -> dict[str, object]:
    if not spec.key_id or len(spec.key_id) > 128:
        raise ValueError("invalid key_id")
    if not spec.principal_id or len(spec.principal_id) > 128:
        raise ValueError("invalid principal_id")
    if not isinstance(spec.role, KeyRole):
        raise ValueError("invalid key role")
    valid_from = _utc(spec.valid_from)
    valid_until = _utc(spec.valid_until)
    revoked_at = None if spec.revoked_at is None else _utc(spec.revoked_at)
    if valid_from >= valid_until:
        raise ValueError("invalid key validity interval")
    if revoked_at is not None and not valid_from <= revoked_at <= valid_until:
        raise ValueError("revocation lies outside validity")
    raw = spec.public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return {
        "key_id": spec.key_id,
        "principal_id": spec.principal_id,
        "public_key_base64": base64.b64encode(raw).decode("ascii"),
        "revoked_at": None if revoked_at is None else revoked_at.isoformat(),
        "role": spec.role.value,
        "valid_from": valid_from.isoformat(),
        "valid_until": valid_until.isoformat(),
    }


def _decode_key_record(data: object) -> TrustedKeyRecord:
    if not isinstance(data, dict) or set(data) != {
        "key_id",
        "principal_id",
        "public_key_base64",
        "revoked_at",
        "role",
        "valid_from",
        "valid_until",
    }:
        raise ValueError("unexpected trust key fields")
    key_id = _strict_nonempty(data["key_id"])
    principal_id = _strict_nonempty(data["principal_id"])
    if len(key_id) > 128 or len(principal_id) > 128:
        raise ValueError("trust key identifier too long")
    raw = base64.b64decode(
        _strict_nonempty(data["public_key_base64"]),
        validate=True,
    )
    public_key = Ed25519PublicKey.from_public_bytes(raw)
    valid_from = _parse_time(data["valid_from"])
    valid_until = _parse_time(data["valid_until"])
    revoked_value = data["revoked_at"]
    revoked_at = None if revoked_value is None else _parse_time(revoked_value)
    if valid_from >= valid_until or (
        revoked_at is not None and not valid_from <= revoked_at <= valid_until
    ):
        raise ValueError("invalid trust key time interval")
    return TrustedKeyRecord(
        key_id,
        principal_id,
        KeyRole(_strict_nonempty(data["role"])),
        public_key,
        valid_from,
        valid_until,
        revoked_at,
    )


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


def _utc(value: datetime) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("timezone-aware datetime required")
    return value.astimezone(timezone.utc)


def _parse_time(value: object) -> datetime:
    text = _strict_nonempty(value)
    parsed = datetime.fromisoformat(text)
    return _utc(parsed)


def _strict_nonempty(value: object) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("non-empty string required")
    return value


def _strict_positive_int(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError("positive integer required")
    return value


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
