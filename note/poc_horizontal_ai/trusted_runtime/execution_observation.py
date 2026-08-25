"""Signed execution-observation evidence; physical measurement stays external."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519
from .nonce_store import PersistentNonceStore
from .role_verification import verify_role_signed_payload
from .runtime_admission import AdmittedSigner
from .trust_bundle import KeyRole, VerifiedTrustBundle
from ..safety_kernel.observer import TrustedFileObserver


@dataclass(frozen=True, slots=True)
class VerifiedExecutionRealityObservation:
    observation_id: str
    attempt_id: str
    intent_id: str
    target_id: str
    observation_subject: str
    observation_field: str
    observed_value: str
    observer_principal_id: str
    observed_at: datetime
    observation_payload_sha256: str


@dataclass(frozen=True, slots=True)
class VerifiedExecutionRealityQuorum:
    attempt_id: str
    intent_id: str
    target_id: str
    observation_subject: str
    observation_field: str
    observed_value: str
    principal_ids: tuple[str, ...]
    observations: tuple[VerifiedExecutionRealityObservation, ...]
    minimum_principals: int


def create_signed_execution_reality_observation(
    *,
    observation_id: str,
    attempt_id: str,
    intent_id: str,
    target_id: str,
    observation_subject: str,
    observation_field: str,
    observed_value: str,
    signing_key_id: str,
    signing_private_key: Ed25519PrivateKey,
    trust_bundle: VerifiedTrustBundle,
    observed_at: datetime,
) -> str:
    """Sign observer-side measured input; no expected value is accepted here."""
    _validate_observation_fields(
        observation_id=observation_id,
        attempt_id=attempt_id,
        intent_id=intent_id,
        target_id=target_id,
        observation_subject=observation_subject,
        observation_field=observation_field,
        observed_value=observed_value,
        observed_at=observed_at,
    )
    if not isinstance(signing_private_key, Ed25519PrivateKey):
        raise ValueError("Ed25519 private key is required")
    record = trust_bundle.record_for(signing_key_id)
    if (
        record is None
        or record.role is not KeyRole.OBSERVER_SIGNER
        or not record.active_at(observed_at)
        or public_key_fingerprint(record.public_key)
        != public_key_fingerprint(signing_private_key.public_key())
    ):
        raise ValueError("EXECUTION_OBSERVER_ROLE_OR_KEY_MISMATCH")
    payload = _canonical_json(
        {
            "attempt_id": attempt_id,
            "observation_field": observation_field,
            "intent_id": intent_id,
            "observation_id": observation_id,
            "observation_subject": observation_subject,
            "observed_at": _format_time(observed_at),
            "observed_value": observed_value,
            "schema_version": "execution-reality-observation/1.2",
            "target_id": target_id,
        }
    )
    return sign_payload_ed25519(
        payload,
        key_id=signing_key_id,
        private_key=signing_private_key,
        issued_at=observed_at,
        trust_bundle_generation=trust_bundle.generation,
        trust_bundle_sha256=trust_bundle.signed_bundle_sha256,
    )


def verify_signed_execution_reality_observation(
    signed_observation_json: str,
    *,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedExecutionRealityObservation | None, tuple[str, ...]]:
    """Verify a signed execution-reality observation and both age bounds.

    ``signature_max_age`` limits the signed envelope while
    ``observation_max_age`` independently limits the observed event. The signer
    must have the active observer role and bind the exact trust bundle. Invalid
    identity, schema, digest, sequence, or time data returns ``None`` with
    reason codes and does not update the execution journal.
    """
    current = now or datetime.now(timezone.utc)
    if (
        current.tzinfo is None
        or not isinstance(observation_max_age, timedelta)
        or observation_max_age <= timedelta(0)
    ):
        return None, ("EXECUTION_OBSERVATION_POLICY_INVALID",)
    role = verify_role_signed_payload(
        signed_observation_json,
        trust_bundle=trust_bundle,
        required_role=KeyRole.OBSERVER_SIGNER,
        signature_max_age=signature_max_age,
        require_trust_binding=True,
        now=current,
    )
    if role.payload_json is None or role.key_record is None:
        return None, role.reason_codes
    try:
        data = json.loads(role.payload_json, object_pairs_hook=_pairs_hook)
        if not isinstance(data, dict) or set(data) != {
            "attempt_id",
            "observation_field",
            "intent_id",
            "observation_id",
            "observation_subject",
            "observed_at",
            "observed_value",
            "schema_version",
            "target_id",
        }:
            raise ValueError
        if data["schema_version"] != "execution-reality-observation/1.2":
            raise ValueError
        observed_at = _time(data["observed_at"])
        _validate_observation_fields(
            observation_id=data["observation_id"],
            attempt_id=data["attempt_id"],
            intent_id=data["intent_id"],
            target_id=data["target_id"],
            observation_subject=data["observation_subject"],
            observation_field=data["observation_field"],
            observed_value=data["observed_value"],
            observed_at=observed_at,
        )
        utc_now = current.astimezone(timezone.utc)
        if (
            observed_at > utc_now + timedelta(seconds=1)
            or utc_now - observed_at > observation_max_age
        ):
            return None, ("EXECUTION_OBSERVATION_STALE_OR_FUTURE",)
        return (
            VerifiedExecutionRealityObservation(
                observation_id=data["observation_id"],
                attempt_id=data["attempt_id"],
                intent_id=data["intent_id"],
                target_id=data["target_id"],
                observation_subject=data["observation_subject"],
                observation_field=data["observation_field"],
                observed_value=data["observed_value"],
                observer_principal_id=role.key_record.principal_id,
                observed_at=observed_at,
                observation_payload_sha256=hashlib.sha256(
                    role.payload_json.encode("utf-8")
                ).hexdigest(),
            ),
            (),
        )
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None, ("SIGNED_EXECUTION_OBSERVATION_INVALID",)


def assess_execution_reality_quorum(
    signed_observation_jsons: tuple[str, ...],
    *,
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedExecutionRealityQuorum | None, tuple[str, ...]]:
    if (
        not isinstance(signed_observation_jsons, tuple)
        or not signed_observation_jsons
        or not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
    ):
        return None, ("EXECUTION_OBSERVATION_QUORUM_CONFIG_INVALID",)
    observations = []
    reasons: list[str] = []
    for signed_json in signed_observation_jsons:
        observation, observation_reasons = (
            verify_signed_execution_reality_observation(
                signed_json,
                trust_bundle=trust_bundle,
                signature_max_age=signature_max_age,
                observation_max_age=observation_max_age,
                now=now,
            )
        )
        if observation is None:
            reasons.extend(observation_reasons)
        else:
            observations.append(observation)
    if reasons or not observations:
        return None, tuple(dict.fromkeys(reasons))
    first = observations[0]
    agreement = (
        first.attempt_id,
        first.intent_id,
        first.target_id,
        first.observation_subject,
        first.observation_field,
        first.observed_value,
    )
    if any(
        (
            item.attempt_id,
            item.intent_id,
            item.target_id,
            item.observation_subject,
            item.observation_field,
            item.observed_value,
        )
        != agreement
        for item in observations[1:]
    ):
        return None, ("EXECUTION_OBSERVATION_QUORUM_CONFLICT",)
    principal_ids = tuple(
        sorted({item.observer_principal_id for item in observations})
    )
    if len(principal_ids) < minimum_principals:
        return None, ("EXECUTION_OBSERVATION_QUORUM_NOT_REACHED",)
    return (
        VerifiedExecutionRealityQuorum(
            attempt_id=first.attempt_id,
            intent_id=first.intent_id,
            target_id=first.target_id,
            observation_subject=first.observation_subject,
            observation_field=first.observation_field,
            observed_value=first.observed_value,
            principal_ids=principal_ids,
            observations=tuple(observations),
            minimum_principals=minimum_principals,
        ),
        (),
    )


def _validate_observation_fields(
    *,
    observation_id: object,
    attempt_id: object,
    intent_id: object,
    target_id: object,
    observation_subject: object,
    observation_field: object,
    observed_value: object,
    observed_at: object,
) -> None:
    if (
        not _identifier(observation_id, 128)
        or not _sha256(attempt_id)
        or not _identifier(intent_id, 128)
        or not _identifier(target_id, 128)
        or not _subject(observation_subject)
        or not _identifier(observation_field, 128)
        or not isinstance(observed_value, str)
        or not 0 < len(observed_value) <= 4096
        or not isinstance(observed_at, datetime)
        or observed_at.tzinfo is None
    ):
        raise ValueError("invalid execution reality observation")


@dataclass(frozen=True, slots=True)
class ExecutionFileObservationRequest:
    observation_id: str
    request_id: str
    nonce: str
    attempt_id: str
    intent_id: str
    target_id: str
    observation_subject: str
    observation_field: str
    state_version: int
    issued_at: datetime


def encode_execution_file_observation_request(
    request: ExecutionFileObservationRequest,
) -> str:
    """Validate, observe, journal, and sign one execution-file request.

    ``repository_root`` bounds the observed path, ``nonce_store`` enforces
    replay resistance, and ``admitted_signer`` supplies the trusted observer
    key. ``request_max_age`` and timezone-aware ``now`` bound request freshness.
    Success records the nonce/observation before returning signed JSON; invalid
    input raises ``ValueError`` and must not be represented as an observation.
    """
    _validate_file_request(request)
    return _canonical_json(
        {
            "attempt_id": request.attempt_id,
            "intent_id": request.intent_id,
            "issued_at": _format_time(request.issued_at),
            "nonce": request.nonce,
            "observation_field": request.observation_field,
            "observation_id": request.observation_id,
            "observation_subject": request.observation_subject,
            "request_id": request.request_id,
            "schema_version": "execution-file-observation-request/1.0",
            "state_version": request.state_version,
            "target_id": request.target_id,
        }
    )


def decode_execution_file_observation_request(
    request_json: str,
) -> ExecutionFileObservationRequest:
    data = json.loads(request_json, object_pairs_hook=_pairs_hook)
    if not isinstance(data, dict) or set(data) != {
        "attempt_id",
        "intent_id",
        "issued_at",
        "nonce",
        "observation_field",
        "observation_id",
        "observation_subject",
        "request_id",
        "schema_version",
        "state_version",
        "target_id",
    }:
        raise ValueError("invalid execution file observation request")
    if data["schema_version"] != "execution-file-observation-request/1.0":
        raise ValueError("unsupported execution file observation request")
    request = ExecutionFileObservationRequest(
        observation_id=data["observation_id"],
        request_id=data["request_id"],
        nonce=data["nonce"],
        attempt_id=data["attempt_id"],
        intent_id=data["intent_id"],
        target_id=data["target_id"],
        observation_subject=data["observation_subject"],
        observation_field=data["observation_field"],
        state_version=data["state_version"],
        issued_at=_time(data["issued_at"]),
    )
    _validate_file_request(request)
    return request


def process_signed_execution_file_observation_request(
    request_json: str,
    *,
    repository_root: Path,
    observer_id: str,
    nonce_store: PersistentNonceStore,
    admitted_signer: AdmittedSigner,
    request_max_age: timedelta,
    now: datetime | None = None,
) -> str:
    current = now or datetime.now(timezone.utc)
    request = decode_execution_file_observation_request(request_json)
    if current.tzinfo is None or request_max_age <= timedelta(0):
        raise ValueError("invalid execution observer time policy")
    current = current.astimezone(timezone.utc)
    issued = request.issued_at.astimezone(timezone.utc)
    if issued > current + timedelta(seconds=1) or current - issued > request_max_age:
        raise ValueError("execution observation request is stale or future")
    canonical = encode_execution_file_observation_request(request)
    consumed = nonce_store.consume(
        request_id=request.request_id,
        nonce=request.nonce,
        issued_at=issued,
        request_digest=hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        consumed_at=current,
    )
    if not consumed.accepted:
        raise ValueError(",".join(consumed.reason_codes))
    observation = TrustedFileObserver(repository_root, observer_id).observe(
        request.observation_subject,
        request.state_version,
    )
    if observation.evidence is None:
        raise ValueError(",".join(observation.reason_codes))
    evidence = observation.evidence
    if request.observation_field == "current_sha256":
        if not evidence.target_exists or evidence.current_sha256 is None:
            raise ValueError("EXECUTION_OBSERVED_FILE_HASH_UNAVAILABLE")
        observed_value = evidence.current_sha256
    elif request.observation_field == "target_exists":
        observed_value = "true" if evidence.target_exists else "false"
    else:
        raise ValueError("EXECUTION_OBSERVATION_FIELD_UNSUPPORTED")
    return create_signed_execution_reality_observation(
        observation_id=request.observation_id,
        attempt_id=request.attempt_id,
        intent_id=request.intent_id,
        target_id=request.target_id,
        observation_subject=request.observation_subject,
        observation_field=request.observation_field,
        observed_value=observed_value,
        signing_key_id=admitted_signer.key_record.key_id,
        signing_private_key=admitted_signer.private_key,
        trust_bundle=admitted_signer.trust_bundle,
        observed_at=_time(evidence.observed_at),
    )


def verify_signed_execution_file_observation(
    signed_observation_json: str,
    *,
    request: ExecutionFileObservationRequest,
    trust_bundle: VerifiedTrustBundle,
    signature_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedExecutionRealityObservation | None, tuple[str, ...]]:
    """Verify that signed file evidence answers the exact observation request.

    Signature and observation ages are checked independently, then request id,
    challenge, attempt, path, expected hash, and trust binding are compared.
    Any mismatch returns ``None`` with reason codes. The verifier is read-only
    and does not reconcile or update the execution journal.
    """
    _validate_file_request(request)
    observation, reasons = verify_signed_execution_reality_observation(
        signed_observation_json,
        trust_bundle=trust_bundle,
        signature_max_age=signature_max_age,
        observation_max_age=observation_max_age,
        now=now,
    )
    if observation is None:
        return None, reasons
    mismatches = []
    for actual, expected, reason in (
        (observation.observation_id, request.observation_id, "ID"),
        (observation.attempt_id, request.attempt_id, "ATTEMPT_ID"),
        (observation.intent_id, request.intent_id, "INTENT_ID"),
        (observation.target_id, request.target_id, "TARGET_ID"),
        (
            observation.observation_subject,
            request.observation_subject,
            "SUBJECT",
        ),
        (
            observation.observation_field,
            request.observation_field,
            "FIELD",
        ),
    ):
        if actual != expected:
            mismatches.append(f"EXECUTION_OBSERVATION_{reason}_MISMATCH")
    if observation.observed_at < request.issued_at.astimezone(timezone.utc):
        mismatches.append("EXECUTION_OBSERVATION_PREDATES_REQUEST")
    return observation if not mismatches else None, tuple(mismatches)


def assess_execution_file_observation_quorum(
    requested_observations: tuple[
        tuple[ExecutionFileObservationRequest, str], ...
    ],
    *,
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    observation_max_age: timedelta,
    now: datetime | None = None,
) -> tuple[VerifiedExecutionRealityQuorum | None, tuple[str, ...]]:
    """Bind every observer response to its request before quorum assessment."""
    if (
        not isinstance(requested_observations, tuple)
        or not requested_observations
    ):
        return None, ("EXECUTION_FILE_OBSERVATION_QUORUM_CONFIG_INVALID",)
    signed_observations: list[str] = []
    reasons: list[str] = []
    for item in requested_observations:
        if (
            not isinstance(item, tuple)
            or len(item) != 2
            or not isinstance(item[1], str)
        ):
            reasons.append("EXECUTION_FILE_OBSERVATION_RESPONSE_INVALID")
            continue
        request, signed_observation = item
        try:
            observation, observation_reasons = (
                verify_signed_execution_file_observation(
                    signed_observation,
                    request=request,
                    trust_bundle=trust_bundle,
                    signature_max_age=signature_max_age,
                    observation_max_age=observation_max_age,
                    now=now,
                )
            )
        except ValueError:
            observation = None
            observation_reasons = (
                "EXECUTION_FILE_OBSERVATION_REQUEST_INVALID",
            )
        if observation is None:
            reasons.extend(observation_reasons)
        else:
            signed_observations.append(signed_observation)
    if reasons or not signed_observations:
        return None, tuple(dict.fromkeys(reasons))
    return assess_execution_reality_quorum(
        tuple(signed_observations),
        trust_bundle=trust_bundle,
        minimum_principals=minimum_principals,
        signature_max_age=signature_max_age,
        observation_max_age=observation_max_age,
        now=now,
    )


def _validate_file_request(request: object) -> None:
    if not isinstance(request, ExecutionFileObservationRequest):
        raise ValueError("invalid execution file observation request")
    if (
        not _identifier(request.observation_id, 128)
        or not _identifier(request.request_id, 128)
        or not isinstance(request.nonce, str)
        or not 16 <= len(request.nonce) <= 128
        or not _sha256(request.attempt_id)
        or not _identifier(request.intent_id, 128)
        or not _identifier(request.target_id, 128)
        or not _subject(request.observation_subject)
        or request.observation_field not in {"current_sha256", "target_exists"}
        or not isinstance(request.state_version, int)
        or isinstance(request.state_version, bool)
        or request.state_version < 0
        or request.issued_at.tzinfo is None
    ):
        raise ValueError("invalid execution file observation request")


def _subject(value: object) -> bool:
    if not isinstance(value, str) or not 0 < len(value) <= 1024:
        return False
    path = PurePosixPath(value)
    return not (
        path.is_absolute()
        or value.startswith(("/", "\\"))
        or "\\" in value
        or ":" in value
        or any(part in {"", ".", ".."} for part in path.parts)
    )


def _identifier(value: object, maximum: int) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= maximum
        and not any(character.isspace() for character in value)
    )


def _sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError
    return parsed.astimezone(timezone.utc)


def _format_time(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def _canonical_json(data: dict[str, object]) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
