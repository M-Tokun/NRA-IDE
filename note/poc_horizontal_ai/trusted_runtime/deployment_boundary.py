"""Verify path separation without claiming unverified OS identity isolation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RuntimePlacement:
    repository_root: Path
    private_key_path: Path
    nonce_database_path: Path
    anchor_database_path: Path
    latch_database_path: Path
    witness_roots: tuple[Path, ...]
    execution_authorization_database_path: Path | None = None
    execution_journal_authority_domain: str | None = None
    execution_integrity_key_authority_domain: str | None = None
    observer_trust_root_authority_domains: tuple[str, ...] = ()
    root_policy_checkpoint_database_path: Path | None = None


@dataclass(frozen=True, slots=True)
class DeploymentBoundaryAssessment:
    path_separated: bool
    os_identity_separation_verified: bool
    execution_authority_domains_separated: bool
    authority_domain_separation_verified: bool
    reason_codes: tuple[str, ...]


def assess_runtime_placement(
    placement: RuntimePlacement,
) -> DeploymentBoundaryAssessment:
    reasons: list[str] = []
    repository = placement.repository_root.resolve()
    if not repository.is_dir():
        reasons.append("PLACEMENT_REPOSITORY_INVALID")
    runtime_paths = (
        placement.private_key_path.resolve(),
        placement.nonce_database_path.resolve(),
        placement.anchor_database_path.resolve(),
        placement.latch_database_path.resolve(),
        *(
            ()
            if placement.execution_authorization_database_path is None
            else (placement.execution_authorization_database_path.resolve(),)
        ),
        *(
            ()
            if placement.root_policy_checkpoint_database_path is None
            else (placement.root_policy_checkpoint_database_path.resolve(),)
        ),
    )
    paths = (
        *runtime_paths,
        *(root.resolve() for root in placement.witness_roots),
    )
    if len(paths) != len(set(paths)):
        reasons.append("PLACEMENT_PATH_REUSED")
    if len(placement.witness_roots) < 2:
        reasons.append("PLACEMENT_WITNESS_COUNT_INSUFFICIENT")
    for path in paths:
        if _inside(repository, path):
            reasons.append("PLACEMENT_INSIDE_REPOSITORY")
            break
    resolved_witnesses = tuple(root.resolve() for root in placement.witness_roots)
    if any(
        left == right or _inside(left, right) or _inside(right, left)
        for index, left in enumerate(resolved_witnesses)
        for right in resolved_witnesses[index + 1 :]
    ):
        reasons.append("PLACEMENT_WITNESSES_NOT_DISJOINT")
    if any(
        _inside(witness, runtime_path)
        for witness in resolved_witnesses
        for runtime_path in runtime_paths
    ):
        reasons.append("PLACEMENT_WITNESS_RUNTIME_PATH_OVERLAP")
    if placement.private_key_path.is_symlink():
        reasons.append("PLACEMENT_PRIVATE_KEY_SYMLINK")
    if not placement.private_key_path.is_file():
        reasons.append("PLACEMENT_PRIVATE_KEY_MISSING")
    if any(
        path.is_symlink()
        for path in (
            placement.nonce_database_path,
            placement.anchor_database_path,
            placement.latch_database_path,
            *(
                ()
                if placement.execution_authorization_database_path is None
                else (placement.execution_authorization_database_path,)
            ),
            *(
                ()
                if placement.root_policy_checkpoint_database_path is None
                else (placement.root_policy_checkpoint_database_path,)
            ),
        )
    ):
        reasons.append("PLACEMENT_DATABASE_SYMLINK")
    for root in placement.witness_roots:
        if root.is_symlink() or not root.is_dir():
            reasons.append("PLACEMENT_WITNESS_ROOT_INVALID")
            break

    execution_authority_domains_separated = True
    if placement.execution_authorization_database_path is not None:
        journal_domain = placement.execution_journal_authority_domain
        integrity_domain = placement.execution_integrity_key_authority_domain
        observer_domains = placement.observer_trust_root_authority_domains
        if placement.root_policy_checkpoint_database_path is None:
            reasons.append("PLACEMENT_ROOT_POLICY_CHECKPOINT_REQUIRED")
            execution_authority_domains_separated = False
        if (
            not _authority_id(journal_domain)
            or not _authority_id(integrity_domain)
            or not isinstance(observer_domains, tuple)
            or any(not _authority_id(item) for item in observer_domains)
        ):
            reasons.append("PLACEMENT_EXECUTION_AUTHORITY_DOMAINS_REQUIRED")
            execution_authority_domains_separated = False
        elif (
            observer_domains != tuple(sorted(set(observer_domains)))
            or len(observer_domains) < 2
        ):
            reasons.append(
                "PLACEMENT_OBSERVER_ROOT_AUTHORITY_COUNT_INSUFFICIENT"
            )
            execution_authority_domains_separated = False
        elif (
            journal_domain == integrity_domain
            or journal_domain in observer_domains
            or integrity_domain in observer_domains
        ):
            reasons.append("PLACEMENT_EXECUTION_AUTHORITY_DOMAIN_OVERLAP")
            execution_authority_domains_separated = False
        reasons.append("AUTHORITY_DOMAIN_SEPARATION_NOT_ATTESTED")

    # Portable Python cannot prove that paths are owned by distinct OS identities.
    reasons.append("OS_IDENTITY_SEPARATION_NOT_ATTESTED")
    structural_reasons = tuple(
        reason
        for reason in reasons
        if reason
        not in {
            "OS_IDENTITY_SEPARATION_NOT_ATTESTED",
            "AUTHORITY_DOMAIN_SEPARATION_NOT_ATTESTED",
            "PLACEMENT_EXECUTION_AUTHORITY_DOMAINS_REQUIRED",
            "PLACEMENT_OBSERVER_ROOT_AUTHORITY_COUNT_INSUFFICIENT",
            "PLACEMENT_EXECUTION_AUTHORITY_DOMAIN_OVERLAP",
            "PLACEMENT_ROOT_POLICY_CHECKPOINT_REQUIRED",
        }
    )
    return DeploymentBoundaryAssessment(
        path_separated=not structural_reasons,
        os_identity_separation_verified=False,
        execution_authority_domains_separated=(
            execution_authority_domains_separated
        ),
        authority_domain_separation_verified=False,
        reason_codes=tuple(dict.fromkeys(reasons)),
    )


def _inside(root: Path, candidate: Path) -> bool:
    try:
        return os.path.commonpath((str(root), str(candidate))) == str(root)
    except ValueError:
        return False


def _authority_id(value: object) -> bool:
    return (
        isinstance(value, str)
        and 0 < len(value) <= 128
        and not any(character.isspace() for character in value)
    )
