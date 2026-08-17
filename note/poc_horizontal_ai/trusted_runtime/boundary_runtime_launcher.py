"""Trusted orchestration for challenge-bound boundary-runtime admission."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable, Sequence

from .asymmetric_auth import load_ed25519_public_key, public_key_fingerprint
from .boundary_runtime import (
    AdmittedBoundaryRuntime,
    ExternalLatchWitnessEvidence,
    admit_boundary_runtime,
    create_boundary_admission_challenge,
)
from .execution_gate import (
    BoundaryExecutionIntent,
    BoundaryExecutor,
    SimulationOutcome,
)
from .deployment_boundary import RuntimePlacement, assess_runtime_placement
from .irreversible_latch_store import PersistentIrreversibleLatchStore
from .latch_witness import (
    genesis_latch_head,
    verify_signed_latch_checkpoint,
)
from .policy_witness_deployment import (
    RootPolicyWitnessProcess,
    assess_policy_witness_deployment_quorum,
    policy_witness_deployment_sha256,
)
from .runtime_admission import load_bounded_text_file
from .root_policy import PinnedPolicyRoot, root_policy_configuration_sha256
from .trust_bundle import verify_signed_trust_bundle


_MAX_BUNDLE_BYTES = 512 * 1024
_MAX_CHECKPOINT_RESPONSE_BYTES = 1024 * 1024
_MAX_WITNESS_RESPONSE_BYTES = 256 * 1024


@dataclass(frozen=True, slots=True)
class LatchWitnessProcess:
    database_path: Path
    principal_id: str
    key_id: str
    private_key_path: Path


@dataclass(frozen=True, slots=True)
class LatchCheckpointSignerProcess:
    latch_integrity_key_path: Path
    signing_key_id: str
    signing_key_path: Path
    trust_bundle_path: Path
    trust_checkpoint_database_path: Path
    trust_checkpoint_attestation_paths: tuple[Path, ...]


def launch_boundary_runtime(
    *,
    placement: RuntimePlacement,
    latch_integrity_key: bytes,
    latch_store_id: str,
    checkpoint_signer_process: LatchCheckpointSignerProcess,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    witness_processes: Sequence[LatchWitnessProcess],
    minimum_witness_principals: int,
    minimum_trust_checkpoint_witness_principals: int,
    minimum_execution_authorizer_principals: int,
    signed_authority_manifest_attestations: tuple[str, ...],
    minimum_authority_attester_principals: int,
    pinned_policy_roots: dict[str, PinnedPolicyRoot],
    root_policy_id: str,
    root_policy_witness_processes: Sequence[RootPolicyWitnessProcess],
    signed_policy_witness_deployment_attestations: tuple[str, ...],
    minimum_policy_witness_deployment_attester_principals: int,
    policy_witness_deployment_signature_max_age: timedelta,
    minimum_policy_root_principals: int,
    root_policy_signature_max_age: timedelta,
    trust_bundle_max_age: timedelta,
    trust_checkpoint_attestation_max_age: timedelta,
    checkpoint_signature_max_age: timedelta,
    checkpoint_signer_process_timeout: timedelta,
    witness_process_timeout: timedelta,
    root_policy_witness_process_timeout: timedelta,
    execution_executor: BoundaryExecutor | None = None,
    hard_invariant_checker: (
        Callable[[BoundaryExecutionIntent, bytes], tuple[str, ...]] | None
    ) = None,
    simulator: (
        Callable[[BoundaryExecutionIntent, bytes], SimulationOutcome] | None
    ) = None,
    now: datetime | None = None,
) -> AdmittedBoundaryRuntime:
    """Perform the complete witness round and return only an admitted runtime."""
    if (
        not isinstance(latch_store_id, str)
        or not latch_store_id
        or len(latch_store_id) > 128
        or any(character.isspace() for character in latch_store_id)
    ):
        raise ValueError("invalid latch_store_id")
    _validate_checkpoint_signer_process(checkpoint_signer_process)
    current = now or datetime.now(timezone.utc)
    if current.tzinfo is None:
        raise ValueError("boundary launcher time must be timezone-aware")
    current = current.astimezone(timezone.utc)
    bundle_age_seconds = _whole_positive_seconds(
        trust_bundle_max_age,
        "trust bundle max age",
    )
    checkpoint_age_seconds = _whole_positive_seconds(
        checkpoint_signature_max_age,
        "checkpoint signature max age",
    )
    trust_checkpoint_age_seconds = _whole_positive_seconds(
        trust_checkpoint_attestation_max_age,
        "trust checkpoint attestation max age",
    )
    root_policy_age_seconds = _whole_positive_seconds(
        root_policy_signature_max_age,
        "root policy signature max age",
    )
    _whole_positive_seconds(
        policy_witness_deployment_signature_max_age,
        "policy witness deployment signature max age",
    )
    signer_timeout_seconds = checkpoint_signer_process_timeout.total_seconds()
    timeout_seconds = witness_process_timeout.total_seconds()
    root_policy_timeout_seconds = (
        root_policy_witness_process_timeout.total_seconds()
    )
    if (
        not 0 < signer_timeout_seconds <= 120
        or not 0 < timeout_seconds <= 120
        or not 0 < root_policy_timeout_seconds <= 120
    ):
        raise ValueError("invalid service process timeout")
    processes = tuple(witness_processes)
    if (
        not isinstance(minimum_witness_principals, int)
        or isinstance(minimum_witness_principals, bool)
        or minimum_witness_principals < 2
        or len(processes) < minimum_witness_principals
    ):
        raise ValueError("LATCH_WITNESS_QUORUM_CONFIG_INVALID")
    _validate_process_set(processes)
    policy_processes = tuple(root_policy_witness_processes)
    _validate_root_policy_process_set(
        policy_processes,
        pinned_policy_roots=pinned_policy_roots,
        minimum_principals=minimum_policy_root_principals,
        placement=placement,
    )
    if (
        not isinstance(root_policy_id, str)
        or not root_policy_id
        or len(root_policy_id) > 128
        or any(character.isspace() for character in root_policy_id)
    ):
        raise ValueError("ROOT_POLICY_ID_INVALID")
    if (
        not isinstance(minimum_trust_checkpoint_witness_principals, int)
        or isinstance(minimum_trust_checkpoint_witness_principals, bool)
        or minimum_trust_checkpoint_witness_principals < 2
        or len(checkpoint_signer_process.trust_checkpoint_attestation_paths)
        < minimum_trust_checkpoint_witness_principals
    ):
        raise ValueError("CHECKPOINT_WITNESS_QUORUM_CONFIG_INVALID")
    if (
        not isinstance(minimum_execution_authorizer_principals, int)
        or isinstance(minimum_execution_authorizer_principals, bool)
        or minimum_execution_authorizer_principals < 2
    ):
        raise ValueError("EXECUTION_AUTHORIZATION_QUORUM_CONFIG_INVALID")
    signed_trust_bundle_json = load_bounded_text_file(
        checkpoint_signer_process.trust_bundle_path,
        _MAX_BUNDLE_BYTES,
    )
    if len(signed_trust_bundle_json.encode("utf-8")) > _MAX_BUNDLE_BYTES:
        raise ValueError("trust bundle input too large")

    placement_assessment = assess_runtime_placement(placement)
    structural_reasons = tuple(
        reason
        for reason in placement_assessment.reason_codes
        if reason != "OS_IDENTITY_SEPARATION_NOT_ATTESTED"
    )
    if not placement_assessment.path_separated:
        raise ValueError(",".join(structural_reasons))
    _validate_checkpoint_signer_placement(
        checkpoint_signer_process,
        placement,
        processes,
        policy_processes,
    )

    pinned_root = load_ed25519_public_key(pinned_root_public_key_path)
    verification = verify_signed_trust_bundle(
        signed_trust_bundle_json,
        pinned_root_keys={pinned_root_key_id: pinned_root},
        signature_max_age=trust_bundle_max_age,
        now=current,
    )
    if verification.bundle is None:
        raise ValueError(",".join(verification.reason_codes))
    bundle = verification.bundle
    deployment_quorum = assess_policy_witness_deployment_quorum(
        signed_policy_witness_deployment_attestations,
        processes=policy_processes,
        trust_bundle=bundle,
        minimum_principals=(
            minimum_policy_witness_deployment_attester_principals
        ),
        signature_max_age=policy_witness_deployment_signature_max_age,
        now=current,
    )
    if not deployment_quorum.satisfied:
        raise ValueError(",".join(deployment_quorum.reason_codes))

    challenge = create_boundary_admission_challenge()
    policy_configuration_sha256 = root_policy_configuration_sha256(
        policy_id=root_policy_id,
        pinned_policy_roots=pinned_policy_roots,
        minimum_principals=minimum_policy_root_principals,
    )
    root_policy_request_json = json.dumps(
        {
            "admission_challenge": challenge.nonce,
            "policy_configuration_sha256": policy_configuration_sha256,
            "policy_id": root_policy_id,
            "schema_version": "root-policy-witness-request/1.1",
            "signed_trust_bundle_json": signed_trust_bundle_json,
        },
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    signed_root_policy_endorsements = tuple(
        _invoke_root_policy_witness_process(
            process,
            request_json=root_policy_request_json,
            policy_root_public_key_fingerprint=public_key_fingerprint(
                pinned_policy_roots[process.key_id].public_key
            ),
            pinned_root_key_id=pinned_root_key_id,
            pinned_root_public_key_path=pinned_root_public_key_path,
            bundle_age_seconds=bundle_age_seconds,
            endorsement_validity_seconds=root_policy_age_seconds,
            timeout_seconds=root_policy_timeout_seconds,
        )
        for process in policy_processes
    )
    signed_checkpoints = _invoke_checkpoint_signer_process(
        checkpoint_signer_process,
        placement=placement,
        latch_store_id=latch_store_id,
        admission_challenge=challenge.nonce,
        pinned_root_key_id=pinned_root_key_id,
        pinned_root_public_key_path=pinned_root_public_key_path,
        bundle_age_seconds=bundle_age_seconds,
        minimum_trust_checkpoint_witness_principals=(
            minimum_trust_checkpoint_witness_principals
        ),
        trust_checkpoint_age_seconds=trust_checkpoint_age_seconds,
        timeout_seconds=signer_timeout_seconds,
    )
    checkpoint_verification_time = max(current, datetime.now(timezone.utc))
    with PersistentIrreversibleLatchStore(
        placement.latch_database_path,
        latch_integrity_key,
    ) as latch_store:
        head = latch_store.head()
        if head is None:
            expected_heads = (genesis_latch_head(latch_store_id),)
        else:
            heads = []
            for sequence in range(1, head.sequence + 1):
                sequence_head = latch_store.head_at(sequence)
                if sequence_head is None:
                    raise ValueError("IRREVERSIBLE_LATCH_CHAIN_INVALID")
                heads.append(sequence_head)
            expected_heads = tuple(heads)
    if len(signed_checkpoints) != len(expected_heads):
        raise ValueError("LATCH_CHECKPOINT_SIGNER_STATE_MISMATCH")
    for signed_checkpoint, expected_head in zip(
        signed_checkpoints,
        expected_heads,
        strict=True,
    ):
        verified_checkpoint, reasons = verify_signed_latch_checkpoint(
            signed_checkpoint,
            trust_bundle=bundle,
            signature_max_age=checkpoint_signature_max_age,
            now=checkpoint_verification_time,
        )
        if verified_checkpoint is None:
            raise ValueError(",".join(reasons))
        if (
            verified_checkpoint.latch_store_id != latch_store_id
            or verified_checkpoint.head != expected_head
        ):
            raise ValueError("LATCH_CHECKPOINT_SIGNER_STATE_MISMATCH")

    request_json = json.dumps(
        {
            "admission_challenge": challenge.nonce,
            "schema_version": "latch-witness-request/1.0",
            "signed_latch_checkpoints": list(signed_checkpoints),
            "signed_trust_bundle_json": signed_trust_bundle_json,
        },
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    attestations = tuple(
        _invoke_witness_process(
            process,
            request_json=request_json,
            latch_store_id=latch_store_id,
            pinned_root_key_id=pinned_root_key_id,
            pinned_root_public_key_path=pinned_root_public_key_path,
            bundle_age_seconds=bundle_age_seconds,
            checkpoint_age_seconds=checkpoint_age_seconds,
            timeout_seconds=timeout_seconds,
        )
        for process in processes
    )
    evidence = ExternalLatchWitnessEvidence(
        signed_trust_bundle_json=signed_trust_bundle_json,
        signed_latch_checkpoint_json=signed_checkpoints[-1],
        signed_witness_attestations=attestations,
        minimum_principals=minimum_witness_principals,
        signature_max_age=checkpoint_signature_max_age,
        signed_authority_manifest_attestations=(
            signed_authority_manifest_attestations
        ),
        minimum_authority_attester_principals=(
            minimum_authority_attester_principals
        ),
        signed_root_policy_endorsements=signed_root_policy_endorsements,
    )
    admission_time = max(current, datetime.now(timezone.utc))
    return admit_boundary_runtime(
        placement=placement,
        latch_integrity_key=latch_integrity_key,
        latch_store_id=latch_store_id,
        admission_challenge=challenge,
        external_witness_evidence=evidence,
        pinned_root_keys={pinned_root_key_id: pinned_root},
        trust_bundle_signature_max_age=trust_bundle_max_age,
        now=admission_time,
        minimum_execution_authorizer_principals=(
            minimum_execution_authorizer_principals
        ),
        execution_executor=execution_executor,
        hard_invariant_checker=hard_invariant_checker,
        simulator=simulator,
        pinned_policy_roots=pinned_policy_roots,
        minimum_policy_root_principals=minimum_policy_root_principals,
        root_policy_signature_max_age=root_policy_signature_max_age,
    )


def _invoke_root_policy_witness_process(
    process: RootPolicyWitnessProcess,
    *,
    request_json: str,
    policy_root_public_key_fingerprint: str,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    bundle_age_seconds: int,
    endorsement_validity_seconds: int,
    timeout_seconds: float,
) -> str:
    if not isinstance(process, RootPolicyWitnessProcess):
        raise ValueError("invalid root policy witness process")
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
                str(endorsement_validity_seconds),
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


def _invoke_witness_process(
    process: LatchWitnessProcess,
    *,
    request_json: str,
    latch_store_id: str,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    bundle_age_seconds: int,
    checkpoint_age_seconds: int,
    timeout_seconds: float,
) -> str:
    if not isinstance(process, LatchWitnessProcess):
        raise ValueError("invalid latch witness process")
    try:
        completed = subprocess.run(
            (
                sys.executable,
                "-m",
                "note.poc_horizontal_ai.trusted_runtime.latch_witness_service",
                "--witness-database",
                str(process.database_path),
                "--witness-principal-id",
                process.principal_id,
                "--latch-store-id",
                latch_store_id,
                "--witness-key-id",
                process.key_id,
                "--witness-private-key-file",
                str(process.private_key_path),
                "--pinned-root-key-id",
                pinned_root_key_id,
                "--pinned-root-public-key-file",
                str(pinned_root_public_key_path),
                "--trust-bundle-max-age-seconds",
                str(bundle_age_seconds),
                "--checkpoint-signature-max-age-seconds",
                str(checkpoint_age_seconds),
            ),
            input=request_json,
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ValueError("LATCH_WITNESS_SERVICE_FAILED") from error
    if (
        completed.returncode != 0
        or not completed.stdout
        or len(completed.stdout.encode("utf-8")) > _MAX_WITNESS_RESPONSE_BYTES
    ):
        raise ValueError("LATCH_WITNESS_SERVICE_FAILED")
    return completed.stdout


def _invoke_checkpoint_signer_process(
    process: LatchCheckpointSignerProcess,
    *,
    placement: RuntimePlacement,
    latch_store_id: str,
    admission_challenge: str,
    pinned_root_key_id: str,
    pinned_root_public_key_path: Path,
    bundle_age_seconds: int,
    minimum_trust_checkpoint_witness_principals: int,
    trust_checkpoint_age_seconds: int,
    timeout_seconds: float,
) -> tuple[str, ...]:
    command = [
        sys.executable,
        "-m",
        "note.poc_horizontal_ai.trusted_runtime.latch_checkpoint_signer_service",
        "--latch-database",
        str(placement.latch_database_path),
        "--latch-store-id",
        latch_store_id,
        "--latch-integrity-key-file",
        str(process.latch_integrity_key_path),
        "--signing-key-id",
        process.signing_key_id,
        "--signing-key-file",
        str(process.signing_key_path),
        "--trust-bundle-file",
        str(process.trust_bundle_path),
        "--trust-checkpoint-database",
        str(process.trust_checkpoint_database_path),
        "--pinned-root-key-id",
        pinned_root_key_id,
        "--pinned-root-public-key-file",
        str(pinned_root_public_key_path),
        "--trust-bundle-max-age-seconds",
        str(bundle_age_seconds),
        "--minimum-trust-checkpoint-witness-principals",
        str(minimum_trust_checkpoint_witness_principals),
        "--trust-checkpoint-attestation-max-age-seconds",
        str(trust_checkpoint_age_seconds),
    ]
    for path in process.trust_checkpoint_attestation_paths:
        command.extend(("--trust-checkpoint-attestation-file", str(path)))
    try:
        completed = subprocess.run(
            tuple(command),
            input=json.dumps(
                {
                    "admission_challenge": admission_challenge,
                    "schema_version": "latch-checkpoint-sign-request/1.0",
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            capture_output=True,
            text=True,
            cwd=Path.cwd(),
            timeout=timeout_seconds,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise ValueError("LATCH_CHECKPOINT_SIGNER_SERVICE_FAILED") from error
    if (
        completed.returncode != 0
        or not completed.stdout
        or len(completed.stdout.encode("utf-8"))
        > _MAX_CHECKPOINT_RESPONSE_BYTES
    ):
        raise ValueError("LATCH_CHECKPOINT_SIGNER_SERVICE_FAILED")
    try:
        data = json.loads(completed.stdout, object_pairs_hook=_pairs_hook)
        if not isinstance(data, dict) or set(data) != {
            "admission_challenge",
            "schema_version",
            "signed_latch_checkpoints",
        }:
            raise ValueError
        checkpoints = data["signed_latch_checkpoints"]
        if (
            data["schema_version"]
            != "signed-latch-checkpoint-set/1.0"
            or data["admission_challenge"] != admission_challenge
            or not isinstance(checkpoints, list)
            or not checkpoints
            or len(checkpoints) > 1024
            or any(not isinstance(item, str) for item in checkpoints)
        ):
            raise ValueError
        return tuple(checkpoints)
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError("LATCH_CHECKPOINT_SIGNER_SERVICE_INVALID") from error


def _whole_positive_seconds(value: timedelta, field: str) -> int:
    if not isinstance(value, timedelta):
        raise ValueError(f"invalid {field}")
    seconds = value.total_seconds()
    if not seconds.is_integer() or not 0 < seconds <= 86400:
        raise ValueError(f"invalid {field}")
    return int(seconds)


def _validate_process_set(processes: tuple[LatchWitnessProcess, ...]) -> None:
    if any(not isinstance(process, LatchWitnessProcess) for process in processes):
        raise ValueError("invalid latch witness process")
    principal_ids: set[str] = set()
    database_paths: set[Path] = set()
    for process in processes:
        if (
            not process.principal_id
            or len(process.principal_id) > 128
            or not process.key_id
            or len(process.key_id) > 128
            or not isinstance(process.database_path, Path)
            or not isinstance(process.private_key_path, Path)
            or not process.database_path.parent.exists()
            or process.database_path.is_symlink()
            or not process.private_key_path.is_file()
            or process.private_key_path.is_symlink()
        ):
            raise ValueError("invalid latch witness process")
        resolved_database = process.database_path.resolve()
        if (
            process.principal_id in principal_ids
            or resolved_database in database_paths
        ):
            raise ValueError("LATCH_WITNESS_PROCESS_SET_NOT_SEPARATED")
        principal_ids.add(process.principal_id)
        database_paths.add(resolved_database)


def _validate_root_policy_process_set(
    processes: tuple[RootPolicyWitnessProcess, ...],
    *,
    pinned_policy_roots: dict[str, PinnedPolicyRoot],
    minimum_principals: int,
    placement: RuntimePlacement,
) -> None:
    if (
        not isinstance(minimum_principals, int)
        or isinstance(minimum_principals, bool)
        or minimum_principals < 2
        or len(processes) < minimum_principals
    ):
        raise ValueError("ROOT_POLICY_QUORUM_CONFIG_INVALID")
    principal_ids: set[str] = set()
    database_paths: set[Path] = set()
    try:
        policy_witness_deployment_sha256(processes)
    except ValueError as error:
        raise ValueError("POLICY_WITNESS_DEPLOYMENT_INVALID") from error
    for process in processes:
        if not isinstance(process, RootPolicyWitnessProcess):
            raise ValueError("invalid root policy witness process")
        root = pinned_policy_roots.get(process.key_id)
        if (
            root is None
            or root.principal_id != process.principal_id
            or not isinstance(process.database_path, Path)
            or not process.database_path.parent.exists()
            or process.database_path.is_symlink()
            or not isinstance(process.private_key_path, Path)
            or not process.private_key_path.is_file()
            or process.private_key_path.is_symlink()
        ):
            raise ValueError("invalid root policy witness process")
        resolved_database = process.database_path.resolve()
        if (
            process.principal_id in principal_ids
            or resolved_database in database_paths
        ):
            raise ValueError("ROOT_POLICY_WITNESS_PROCESS_SET_NOT_SEPARATED")
        principal_ids.add(process.principal_id)
        database_paths.add(resolved_database)
    execution_authority_domains = {
        placement.execution_journal_authority_domain,
        placement.execution_integrity_key_authority_domain,
        *placement.observer_trust_root_authority_domains,
    }
    policy_authority_domains = {
        *(process.key_authority_domain for process in processes),
        *(process.state_authority_domain for process in processes),
    }
    if execution_authority_domains & policy_authority_domains:
        raise ValueError("POLICY_WITNESS_EXECUTION_AUTHORITY_DOMAIN_OVERLAP")


def _validate_checkpoint_signer_process(
    process: LatchCheckpointSignerProcess,
) -> None:
    if not isinstance(process, LatchCheckpointSignerProcess):
        raise ValueError("invalid latch checkpoint signer process")
    regular_files = (
        process.latch_integrity_key_path,
        process.signing_key_path,
        process.trust_bundle_path,
        *process.trust_checkpoint_attestation_paths,
    )
    if (
        not process.signing_key_id
        or len(process.signing_key_id) > 128
        or not process.trust_checkpoint_attestation_paths
        or not isinstance(process.trust_checkpoint_database_path, Path)
        or not process.trust_checkpoint_database_path.parent.exists()
        or process.trust_checkpoint_database_path.is_symlink()
        or any(
            not isinstance(path, Path)
            or not path.is_file()
            or path.is_symlink()
            for path in regular_files
        )
    ):
        raise ValueError("invalid latch checkpoint signer process")


def _validate_checkpoint_signer_placement(
    process: LatchCheckpointSignerProcess,
    placement: RuntimePlacement,
    witnesses: tuple[LatchWitnessProcess, ...],
    policy_witnesses: tuple[RootPolicyWitnessProcess, ...],
) -> None:
    repository_root = placement.repository_root.resolve()
    secret_paths = (
        process.latch_integrity_key_path.resolve(),
        process.signing_key_path.resolve(),
        *(witness.private_key_path.resolve() for witness in witnesses),
        *(witness.private_key_path.resolve() for witness in policy_witnesses),
    )
    if (
        len(set(secret_paths)) != len(secret_paths)
        or any(_is_relative_to(path, repository_root) for path in secret_paths)
    ):
        raise ValueError("LATCH_CHECKPOINT_SIGNER_SECRET_PLACEMENT_INVALID")
    state_paths = (
        process.trust_checkpoint_database_path.resolve(),
        placement.latch_database_path.resolve(),
        placement.nonce_database_path.resolve(),
        placement.anchor_database_path.resolve(),
        *(
            ()
            if placement.root_policy_checkpoint_database_path is None
            else (placement.root_policy_checkpoint_database_path.resolve(),)
        ),
        *(witness.database_path.resolve() for witness in witnesses),
        *(witness.database_path.resolve() for witness in policy_witnesses),
    )
    if (
        len(set(state_paths)) != len(state_paths)
        or any(_is_relative_to(path, repository_root) for path in state_paths)
    ):
        raise ValueError("LATCH_CHECKPOINT_SIGNER_STATE_PLACEMENT_INVALID")


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _pairs_hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate field")
        result[key] = value
    return result
