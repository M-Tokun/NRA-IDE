"""Collect policy-root rotation approvals with a previous-side gate."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Mapping, Sequence

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from .asymmetric_auth import load_ed25519_public_key, public_key_fingerprint
from .policy_witness_deployment import (
    RootPolicyWitnessProcess,
    policy_witness_deployment_sha256,
)
from .root_policy import (
    PinnedPolicyRoot,
    RootPolicyRotationEvidence,
    assess_root_policy_rotation_quorum,
    root_policy_configuration_sha256,
)
from .trust_bundle import VerifiedTrustBundle, verify_signed_trust_bundle


_MAX_WITNESS_RESPONSE_BYTES = 256 * 1024


def collect_root_policy_rotation_evidence(
    *,
    rotation_id: str,
    policy_id: str,
    previous_processes: Sequence[RootPolicyWitnessProcess],
    previous_policy_roots: Mapping[str, PinnedPolicyRoot],
    previous_minimum_principals: int,
    next_processes: Sequence[RootPolicyWitnessProcess],
    next_policy_roots: Mapping[str, PinnedPolicyRoot],
    next_minimum_principals: int,
    signed_trust_bundle_json: str,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    trust_bundle_signature_max_age: timedelta,
    approval_signature_max_age: timedelta,
    approval_validity: timedelta,
    process_timeout_seconds: float,
    admission_challenge: str,
    now: datetime | None = None,
) -> RootPolicyRotationEvidence:
    """Collect old approval quorum before contacting any new-side process.

    This function collects evidence only.  Applying the rotation to retained or
    newly bootstrapped witness state remains a separate operation.
    """

    current = now or datetime.now(timezone.utc)
    previous = _validate_process_set(
        previous_processes,
        previous_policy_roots,
        previous_minimum_principals,
        policy_id,
    )
    next_set = _validate_process_set(
        next_processes,
        next_policy_roots,
        next_minimum_principals,
        policy_id,
    )
    if (
        current.tzinfo is None
        or not isinstance(signed_trust_bundle_json, str)
        or not signed_trust_bundle_json
        or not isinstance(pinned_root_key_id, str)
        or not pinned_root_key_id
        or not isinstance(pinned_root_public_key_path, Path)
        or not pinned_root_public_key_path.is_file()
        or pinned_root_public_key_path.is_symlink()
        or not _positive_duration(trust_bundle_signature_max_age)
        or not _positive_duration(approval_signature_max_age)
        or not _positive_duration(approval_validity)
        or not isinstance(process_timeout_seconds, (int, float))
        or isinstance(process_timeout_seconds, bool)
        or not math.isfinite(process_timeout_seconds)
        or process_timeout_seconds <= 0
    ):
        raise ValueError("invalid root policy rotation collection")

    primary_root = load_ed25519_public_key(pinned_root_public_key_path)
    primary_root_keys: dict[str, Ed25519PublicKey] = {
        pinned_root_key_id: primary_root
    }
    verification = verify_signed_trust_bundle(
        signed_trust_bundle_json,
        pinned_root_keys=primary_root_keys,
        signature_max_age=trust_bundle_signature_max_age,
        now=current,
    )
    if verification.bundle is None:
        raise ValueError("ROOT_POLICY_ROTATION_TARGET_BUNDLE_INVALID")
    target_bundle = verification.bundle

    previous_configuration = root_policy_configuration_sha256(
        policy_id=policy_id,
        pinned_policy_roots=previous_policy_roots,
        minimum_principals=previous_minimum_principals,
    )
    next_configuration = root_policy_configuration_sha256(
        policy_id=policy_id,
        pinned_policy_roots=next_policy_roots,
        minimum_principals=next_minimum_principals,
    )
    if previous_configuration == next_configuration:
        raise ValueError("ROOT_POLICY_ROTATION_CONFIGURATION_UNCHANGED")

    common_request = {
        "admission_challenge": admission_challenge,
        "next_configuration_sha256": next_configuration,
        "policy_id": policy_id,
        "previous_configuration_sha256": previous_configuration,
        "rotation_id": rotation_id,
        "schema_version": "root-policy-rotation-approval-request/1.0",
        "signed_trust_bundle_json": signed_trust_bundle_json,
    }
    bundle_age_seconds = _duration_seconds(trust_bundle_signature_max_age)
    validity_seconds = _duration_seconds(approval_validity)

    previous_approvals = _collect_side(
        previous,
        policy_roots=previous_policy_roots,
        request={**common_request, "approval_side": "PREVIOUS"},
        pinned_root_key_id=pinned_root_key_id,
        pinned_root_public_key_path=pinned_root_public_key_path,
        bundle_age_seconds=bundle_age_seconds,
        approval_validity_seconds=validity_seconds,
        timeout_seconds=float(process_timeout_seconds),
    )
    if not previous_approvals:
        raise ValueError("ROOT_POLICY_PREVIOUS_ROTATION_QUORUM_NOT_REACHED")
    previous_assessment = assess_root_policy_rotation_quorum(
        previous_approvals,
        rotation_id=rotation_id,
        policy_id=policy_id,
        previous_policy_roots=previous_policy_roots,
        previous_minimum_principals=previous_minimum_principals,
        next_policy_roots=next_policy_roots,
        next_minimum_principals=next_minimum_principals,
        primary_root_keys=primary_root_keys,
        target_bundle=target_bundle,
        admission_challenge=admission_challenge,
        signature_max_age=approval_signature_max_age,
        now=max(current, datetime.now(timezone.utc)),
    )
    if len(previous_assessment.previous_principal_ids) < previous_minimum_principals:
        raise ValueError("ROOT_POLICY_PREVIOUS_ROTATION_QUORUM_NOT_REACHED")

    next_approvals = _collect_side(
        next_set,
        policy_roots=next_policy_roots,
        request={**common_request, "approval_side": "NEXT"},
        pinned_root_key_id=pinned_root_key_id,
        pinned_root_public_key_path=pinned_root_public_key_path,
        bundle_age_seconds=bundle_age_seconds,
        approval_validity_seconds=validity_seconds,
        timeout_seconds=float(process_timeout_seconds),
    )
    approvals = previous_approvals + next_approvals
    final = assess_root_policy_rotation_quorum(
        approvals,
        rotation_id=rotation_id,
        policy_id=policy_id,
        previous_policy_roots=previous_policy_roots,
        previous_minimum_principals=previous_minimum_principals,
        next_policy_roots=next_policy_roots,
        next_minimum_principals=next_minimum_principals,
        primary_root_keys=primary_root_keys,
        target_bundle=target_bundle,
        admission_challenge=admission_challenge,
        signature_max_age=approval_signature_max_age,
        now=max(current, datetime.now(timezone.utc)),
    )
    if not final.satisfied:
        raise ValueError(",".join(final.reason_codes))
    return RootPolicyRotationEvidence(
        signed_approvals=approvals,
        rotation_id=rotation_id,
        policy_id=policy_id,
        previous_policy_roots=dict(previous_policy_roots),
        previous_minimum_principals=previous_minimum_principals,
        next_policy_roots=dict(next_policy_roots),
        next_minimum_principals=next_minimum_principals,
        primary_root_keys=primary_root_keys,
        admission_challenge=admission_challenge,
        signature_max_age=approval_signature_max_age,
    )


def _validate_process_set(
    processes: Sequence[RootPolicyWitnessProcess],
    roots: Mapping[str, PinnedPolicyRoot],
    minimum_principals: int,
    policy_id: str,
) -> tuple[RootPolicyWitnessProcess, ...]:
    normalized = tuple(processes)
    policy_witness_deployment_sha256(normalized)
    root_policy_configuration_sha256(
        policy_id=policy_id,
        pinned_policy_roots=roots,
        minimum_principals=minimum_principals,
    )
    if {process.key_id for process in normalized} != set(roots):
        raise ValueError("incomplete root policy witness process set")
    for process in normalized:
        root = roots.get(process.key_id)
        if (
            root is None
            or root.principal_id != process.principal_id
            or not process.private_key_path.is_file()
            or process.private_key_path.is_symlink()
            or not process.database_path.parent.is_dir()
            or process.database_path.parent.is_symlink()
        ):
            raise ValueError("invalid root policy witness process set")
    return normalized


def _collect_side(
    processes: tuple[RootPolicyWitnessProcess, ...],
    *,
    policy_roots: Mapping[str, PinnedPolicyRoot],
    request: dict[str, object],
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    bundle_age_seconds: int,
    approval_validity_seconds: int,
    timeout_seconds: float,
) -> tuple[str, ...]:
    request_json = json.dumps(
        request,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    approvals = []
    for process in processes:
        try:
            approvals.append(
                _invoke_process(
                    process,
                    request_json=request_json,
                    policy_root_public_key_fingerprint=(
                        public_key_fingerprint(
                            policy_roots[process.key_id].public_key
                        )
                    ),
                    pinned_root_key_id=pinned_root_key_id,
                    pinned_root_public_key_path=pinned_root_public_key_path,
                    bundle_age_seconds=bundle_age_seconds,
                    approval_validity_seconds=approval_validity_seconds,
                    timeout_seconds=timeout_seconds,
                )
            )
        except ValueError:
            continue
    return tuple(approvals)


def _invoke_process(
    process: RootPolicyWitnessProcess,
    *,
    request_json: str,
    policy_root_public_key_fingerprint: str,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    bundle_age_seconds: int,
    approval_validity_seconds: int,
    timeout_seconds: float,
) -> str:
    try:
        completed = subprocess.run(
            (
                sys.executable,
                "-m",
                "note.poc_horizontal_ai.trusted_runtime."
                "root_policy_witness_service",
                "--witness-database",
                str(process.database_path),
                "--policy-root-principal-id",
                process.principal_id,
                "--policy-root-key-id",
                process.key_id,
                "--policy-root-private-key-file",
                str(process.private_key_path),
                "--policy-root-public-key-fingerprint",
                policy_root_public_key_fingerprint,
                "--pinned-root-key-id",
                pinned_root_key_id,
                "--pinned-root-public-key-file",
                str(pinned_root_public_key_path),
                "--trust-bundle-max-age-seconds",
                str(bundle_age_seconds),
                "--endorsement-validity-seconds",
                str(approval_validity_seconds),
            ),
            input=request_json,
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ValueError("ROOT_POLICY_WITNESS_SERVICE_FAILED") from error
    if (
        completed.returncode != 0
        or not completed.stdout
        or len(completed.stdout.encode("utf-8")) > _MAX_WITNESS_RESPONSE_BYTES
    ):
        raise ValueError("ROOT_POLICY_WITNESS_SERVICE_FAILED")
    return completed.stdout


def _positive_duration(value: object) -> bool:
    return isinstance(value, timedelta) and value > timedelta(0)


def _duration_seconds(value: timedelta) -> int:
    return max(1, math.ceil(value.total_seconds()))
