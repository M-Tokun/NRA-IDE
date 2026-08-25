"""Signed deployment manifest for the complete policy-root witness set."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
from typing import Sequence

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from .asymmetric_auth import public_key_fingerprint, sign_payload_ed25519
from .role_verification import verify_role_signed_payload
from .trust_bundle import KeyRole, VerifiedTrustBundle


@dataclass(frozen=True, slots=True)
class RootPolicyWitnessProcess:
    database_path: Path
    principal_id: str
    key_id: str
    private_key_path: Path
    host_identity: str
    os_identity: str
    key_authority_domain: str
    state_authority_domain: str


@dataclass(frozen=True, slots=True)
class PolicyWitnessDeploymentQuorum:
    satisfied: bool
    manifest_id: str | None
    deployment_sha256: str | None
    principal_ids: tuple[str, ...]
    reason_codes: tuple[str, ...]


def policy_witness_deployment_sha256(
    processes: Sequence[RootPolicyWitnessProcess],
) -> str:
    normalized = _validate_processes(processes)
    data = {
        "processes": [
            {
                "database_path": str(process.database_path.resolve()),
                "host_identity": process.host_identity,
                "key_authority_domain": process.key_authority_domain,
                "key_id": process.key_id,
                "os_identity": process.os_identity,
                "principal_id": process.principal_id,
                "private_key_path": str(process.private_key_path.resolve()),
                "state_authority_domain": process.state_authority_domain,
            }
            for process in normalized
        ],
        "schema_version": "policy-witness-deployment/1.0",
        "service_module": (
            "note.poc_horizontal_ai.trusted_runtime."
            "root_policy_witness_service"
        ),
    }
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()


def create_signed_policy_witness_deployment_attestation(
    *,
    processes: Sequence[RootPolicyWitnessProcess],
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
        raise ValueError("invalid policy witness deployment attestation")
    record = trust_bundle.record_for(signing_key_id)
    if (
        record is None
        or record.role is not KeyRole.AUTHORITY_ATTESTER
        or not record.active_at(attested_at)
        or public_key_fingerprint(record.public_key)
        != public_key_fingerprint(signing_private_key.public_key())
    ):
        raise ValueError("POLICY_WITNESS_DEPLOYMENT_ATTESTER_MISMATCH")
    payload = _canonical_json(
        {
            "attestation_id": attestation_id,
            "attested_at": _time_text(attested_at),
            "deployment_sha256": policy_witness_deployment_sha256(processes),
            "manifest_id": manifest_id,
            "schema_version": "policy-witness-deployment-attestation/1.0",
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


def assess_policy_witness_deployment_quorum(
    signed_attestations: tuple[str, ...],
    *,
    processes: Sequence[RootPolicyWitnessProcess],
    trust_bundle: VerifiedTrustBundle,
    minimum_principals: int,
    signature_max_age: timedelta,
    now: datetime | None = None,
) -> PolicyWitnessDeploymentQuorum:
    """Assess distinct-principal agreement on one witness deployment digest.

    ``processes`` defines the expected deployment and ``signed_attestations``
    supplies authority statements bound to the verified trust bundle.
    ``minimum_principals`` counts distinct principals; ``signature_max_age``
    and timezone-aware ``now`` bound freshness. Invalid or disagreeing evidence
    is reported and cannot satisfy quorum. No process is launched or changed.
    """
    current = now or datetime.now(timezone.utc)
    if (
        current.tzinfo is None
        or not isinstance(signed_attestations, tuple)
        or not signed_attestations
        or not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
        or not isinstance(signature_max_age, timedelta)
        or signature_max_age <= timedelta(0)
    ):
        return PolicyWitnessDeploymentQuorum(
            False,
            None,
            None,
            (),
            ("POLICY_WITNESS_DEPLOYMENT_QUORUM_CONFIG_INVALID",),
        )
    try:
        expected_digest = policy_witness_deployment_sha256(processes)
    except ValueError:
        return PolicyWitnessDeploymentQuorum(
            False,
            None,
            None,
            (),
            ("POLICY_WITNESS_DEPLOYMENT_INVALID",),
        )
    principals: set[str] = set()
    agreement: tuple[str, str] | None = None
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
            data = json.loads(
                verified.payload_json,
                object_pairs_hook=_pairs_hook,
            )
            if not isinstance(data, dict) or set(data) != {
                "attestation_id",
                "attested_at",
                "deployment_sha256",
                "manifest_id",
                "schema_version",
                "valid_until",
            }:
                raise ValueError
            if (
                data["schema_version"]
                != "policy-witness-deployment-attestation/1.0"
            ):
                raise ValueError
            _identifier(data["attestation_id"])
            manifest_id = _identifier(data["manifest_id"])
            deployment_digest = _digest(data["deployment_sha256"])
            attested_at = _time(data["attested_at"])
            valid_until = _time(data["valid_until"])
            if (
                valid_until <= attested_at
                or current.astimezone(timezone.utc) >= valid_until
            ):
                raise ValueError
        except (TypeError, ValueError, json.JSONDecodeError):
            invalid = True
            continue
        item_agreement = (manifest_id, deployment_digest)
        if deployment_digest != expected_digest or (
            agreement is not None and item_agreement != agreement
        ):
            mismatch = True
            continue
        agreement = item_agreement
        principals.add(verified.key_record.principal_id)
    principal_ids = tuple(sorted(principals))
    if agreement is None or len(principal_ids) < minimum_principals:
        reasons = ["POLICY_WITNESS_DEPLOYMENT_QUORUM_NOT_REACHED"]
        if invalid:
            reasons.append(
                "INVALID_POLICY_WITNESS_DEPLOYMENT_ATTESTATION_IGNORED"
            )
        if mismatch:
            reasons.append("POLICY_WITNESS_DEPLOYMENT_MISMATCH")
        return PolicyWitnessDeploymentQuorum(
            False,
            None,
            None,
            principal_ids,
            tuple(reasons),
        )
    return PolicyWitnessDeploymentQuorum(
        True,
        agreement[0],
        agreement[1],
        principal_ids,
        (),
    )


def _validate_processes(
    processes: Sequence[RootPolicyWitnessProcess],
) -> tuple[RootPolicyWitnessProcess, ...]:
    if isinstance(processes, (str, bytes)):
        raise ValueError("invalid policy witness deployment")
    normalized = tuple(processes)
    if len(normalized) < 2 or any(
        not isinstance(process, RootPolicyWitnessProcess)
        for process in normalized
    ):
        raise ValueError("invalid policy witness deployment")
    if any(
        not isinstance(process.database_path, Path)
        or not isinstance(process.private_key_path, Path)
        for process in normalized
    ):
        raise ValueError("invalid policy witness deployment path")
    identifier_fields = (
        tuple(process.key_id for process in normalized),
        tuple(process.principal_id for process in normalized),
        tuple(process.host_identity for process in normalized),
        tuple(process.os_identity for process in normalized),
        tuple(process.key_authority_domain for process in normalized),
        tuple(process.state_authority_domain for process in normalized),
    )
    if any(
        any(not _identifier(value) for value in values)
        or len(values) != len(set(values))
        for values in identifier_fields
    ):
        raise ValueError("policy witness identities are not separated")
    authority_domains = (
        *(process.key_authority_domain for process in normalized),
        *(process.state_authority_domain for process in normalized),
    )
    resolved_paths = (
        *(process.database_path.resolve() for process in normalized),
        *(process.private_key_path.resolve() for process in normalized),
    )
    if (
        len(authority_domains) != len(set(authority_domains))
        or len(resolved_paths) != len(set(resolved_paths))
    ):
        raise ValueError("policy witness authority or path overlap")
    return tuple(sorted(normalized, key=lambda process: process.key_id))


def _identifier(value: object) -> str:
    if (
        not isinstance(value, str)
        or not 0 < len(value) <= 128
        or any(character.isspace() for character in value)
    ):
        raise ValueError("invalid identifier")
    return value


def _digest(value: object) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise ValueError("invalid digest")
    return value


def _time(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("invalid time")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed.astimezone(timezone.utc)


def _time_text(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat()


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result


def _canonical_json(data: object) -> str:
    return json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
