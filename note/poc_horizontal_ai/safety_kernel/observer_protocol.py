"""Closed request/response protocol for an independently launched observer."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath

from .evidence import (
    AuthoritativeEvidence,
    EvidenceQuality,
    compute_snapshot_digest,
)
from .observer import TrustedFileObserver
from .states import (
    CommunicationChannelState,
    LoggingChannelState,
    ObservationChannelState,
)


_MAX_REQUEST_BYTES = 16 * 1024
_MAX_ENVELOPE_BYTES = 64 * 1024
_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class ObservationRequest:
    request_id: str
    nonce: str
    resource_path: str
    state_version: int
    issued_at: datetime


@dataclass(frozen=True, slots=True)
class ObservationEnvelopeResult:
    evidence: AuthoritativeEvidence | None
    reason_codes: tuple[str, ...]


def encode_observation_request(request: ObservationRequest) -> str:
    _validate_request(request)
    return _canonical_json(
        {
            "issued_at": _format_time(request.issued_at),
            "nonce": request.nonce,
            "request_id": request.request_id,
            "resource_path": request.resource_path,
            "schema_version": "observer-request/1.0",
            "state_version": request.state_version,
        }
    )


def serve_observation_request(
    request_json: str,
    *,
    repository_root: Path,
    observer_id: str,
) -> str:
    request = decode_observation_request(request_json)
    observation = TrustedFileObserver(repository_root, observer_id).observe(
        request.resource_path,
        request.state_version,
    )
    if observation.evidence is None:
        raise ValueError(",".join(observation.reason_codes))
    evidence = observation.evidence
    return _canonical_json(
        {
            "evidence": {
                "communication_state": evidence.communication_state.value,
                "current_sha256": evidence.current_sha256,
                "logging_state": evidence.logging_state.value,
                "observation_state": evidence.observation_state.value,
                "observed_at": evidence.observed_at,
                "observer_id": evidence.observer_id,
                "quality": evidence.quality.value,
                "resolved_path": str(evidence.resolved_path),
                "resource_path": evidence.resource_path,
                "snapshot_digest": evidence.snapshot_digest,
                "state_version": evidence.state_version,
                "target_exists": evidence.target_exists,
                "target_is_symlink": evidence.target_is_symlink,
            },
            "request_digest": _sha256(encode_observation_request(request)),
            "request_id": request.request_id,
            "schema_version": "observer-envelope/1.0",
        }
    )


def verify_observation_envelope(
    envelope_json: str,
    *,
    request: ObservationRequest,
    repository_root: Path,
    expected_observer_id: str,
    max_age: timedelta,
    now: datetime | None = None,
) -> ObservationEnvelopeResult:
    current_time = now or datetime.now(timezone.utc)
    if (
        max_age <= timedelta(0)
        or current_time.tzinfo is None
        or not expected_observer_id
    ):
        return ObservationEnvelopeResult(
            None,
            ("OBSERVER_VERIFIER_CONFIG_INVALID",),
        )
    reasons: list[str] = []
    try:
        envelope = _strict_object(envelope_json, _MAX_ENVELOPE_BYTES)
        if set(envelope) != {
            "evidence",
            "request_digest",
            "request_id",
            "schema_version",
        }:
            raise ValueError("unexpected envelope fields")
        if envelope["schema_version"] != "observer-envelope/1.0":
            raise ValueError("unsupported envelope schema")
        if envelope["request_id"] != request.request_id:
            reasons.append("OBSERVER_REQUEST_ID_MISMATCH")
        expected_request_json = encode_observation_request(request)
        if envelope["request_digest"] != _sha256(expected_request_json):
            reasons.append("OBSERVER_REQUEST_DIGEST_MISMATCH")
        evidence_data = envelope["evidence"]
        if not isinstance(evidence_data, dict) or set(evidence_data) != {
            "communication_state",
            "current_sha256",
            "logging_state",
            "observation_state",
            "observed_at",
            "observer_id",
            "quality",
            "resolved_path",
            "resource_path",
            "snapshot_digest",
            "state_version",
            "target_exists",
            "target_is_symlink",
        }:
            raise ValueError("unexpected evidence fields")
        evidence = AuthoritativeEvidence(
            quality=EvidenceQuality(evidence_data["quality"]),
            state_version=_strict_int(evidence_data["state_version"]),
            resource_path=_strict_str(evidence_data["resource_path"]),
            resolved_path=Path(_strict_str(evidence_data["resolved_path"])),
            target_exists=_strict_bool(evidence_data["target_exists"]),
            target_is_symlink=_strict_bool(evidence_data["target_is_symlink"]),
            current_sha256=_optional_str(evidence_data["current_sha256"]),
            observer_id=_strict_str(evidence_data["observer_id"]),
            observed_at=_strict_str(evidence_data["observed_at"]),
            snapshot_digest=_strict_str(evidence_data["snapshot_digest"]),
            observation_state=ObservationChannelState(
                evidence_data["observation_state"]
            ),
            logging_state=LoggingChannelState(evidence_data["logging_state"]),
            communication_state=CommunicationChannelState(
                evidence_data["communication_state"]
            ),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return ObservationEnvelopeResult(None, ("OBSERVER_ENVELOPE_INVALID",))

    if evidence.observer_id != expected_observer_id:
        reasons.append("OBSERVER_ID_MISMATCH")
    if evidence.resource_path != request.resource_path:
        reasons.append("OBSERVER_RESOURCE_MISMATCH")
    if evidence.state_version != request.state_version:
        reasons.append("OBSERVER_STATE_VERSION_MISMATCH")
    expected_path = (repository_root.resolve() / request.resource_path).resolve()
    if evidence.resolved_path.resolve() != expected_path:
        reasons.append("OBSERVER_RESOLVED_PATH_MISMATCH")
    if evidence.snapshot_digest != compute_snapshot_digest(evidence):
        reasons.append("OBSERVER_SNAPSHOT_DIGEST_MISMATCH")
    if evidence.target_exists:
        if evidence.current_sha256 is None or not _SHA256.fullmatch(
            evidence.current_sha256
        ):
            reasons.append("OBSERVER_FILE_HASH_INVALID")
    elif evidence.current_sha256 is not None:
        reasons.append("OBSERVER_ABSENT_TARGET_HAS_HASH")
    try:
        observed_at = _parse_time(evidence.observed_at)
        current_time = current_time.astimezone(timezone.utc)
        if observed_at > current_time + timedelta(seconds=1):
            reasons.append("OBSERVER_TIME_IN_FUTURE")
        if current_time - observed_at > max_age:
            reasons.append("OBSERVER_EVIDENCE_STALE")
        if observed_at < request.issued_at:
            reasons.append("OBSERVER_EVIDENCE_PRECEDES_REQUEST")
    except ValueError:
        reasons.append("OBSERVER_TIME_INVALID")
    return ObservationEnvelopeResult(
        evidence if not reasons else None,
        tuple(dict.fromkeys(reasons)),
    )


def decode_observation_request(request_json: str) -> ObservationRequest:
    data = _strict_object(request_json, _MAX_REQUEST_BYTES)
    if set(data) != {
        "issued_at",
        "nonce",
        "request_id",
        "resource_path",
        "schema_version",
        "state_version",
    }:
        raise ValueError("unexpected request fields")
    if data["schema_version"] != "observer-request/1.0":
        raise ValueError("unsupported request schema")
    request = ObservationRequest(
        request_id=_strict_str(data["request_id"]),
        nonce=_strict_str(data["nonce"]),
        resource_path=_strict_str(data["resource_path"]),
        state_version=_strict_int(data["state_version"]),
        issued_at=_parse_time(_strict_str(data["issued_at"])),
    )
    _validate_request(request)
    return request


def _validate_request(request: ObservationRequest) -> None:
    if not request.request_id or len(request.request_id) > 128:
        raise ValueError("invalid request_id")
    if len(request.nonce) < 16 or len(request.nonce) > 128:
        raise ValueError("invalid nonce")
    if not request.resource_path or len(request.resource_path) > 1024:
        raise ValueError("invalid resource_path")
    path = PurePosixPath(request.resource_path)
    if (
        path.is_absolute()
        or request.resource_path.startswith(("/", "\\"))
        or "\\" in request.resource_path
        or ":" in request.resource_path
        or any(part in {"", ".", ".."} for part in path.parts)
    ):
        raise ValueError("invalid resource_path")
    if (
        not isinstance(request.state_version, int)
        or isinstance(request.state_version, bool)
        or request.state_version < 0
    ):
        raise ValueError("invalid state_version")
    if request.issued_at.tzinfo is None:
        raise ValueError("issued_at must be timezone-aware")


def _strict_object(text: str, max_bytes: int) -> dict[str, object]:
    if len(text.encode("utf-8")) > max_bytes:
        raise ValueError("input too large")
    def pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate field")
            result[key] = value
        return result

    result = json.loads(text, object_pairs_hook=pairs_hook)
    if not isinstance(result, dict):
        raise ValueError("object required")
    return result


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


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _parse_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def _strict_str(value: object) -> str:
    if not isinstance(value, str):
        raise ValueError("string required")
    return value


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    return _strict_str(value)


def _strict_int(value: object) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("integer required")
    return value


def _strict_bool(value: object) -> bool:
    if not isinstance(value, bool):
        raise ValueError("boolean required")
    return value
