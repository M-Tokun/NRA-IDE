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
    witness_roots: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class DeploymentBoundaryAssessment:
    path_separated: bool
    os_identity_separation_verified: bool
    reason_codes: tuple[str, ...]


def assess_runtime_placement(
    placement: RuntimePlacement,
) -> DeploymentBoundaryAssessment:
    reasons: list[str] = []
    repository = placement.repository_root.resolve()
    if not repository.is_dir():
        reasons.append("PLACEMENT_REPOSITORY_INVALID")
    paths = (
        placement.private_key_path.resolve(),
        placement.nonce_database_path.resolve(),
        placement.anchor_database_path.resolve(),
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
    if placement.private_key_path.is_symlink():
        reasons.append("PLACEMENT_PRIVATE_KEY_SYMLINK")
    if not placement.private_key_path.is_file():
        reasons.append("PLACEMENT_PRIVATE_KEY_MISSING")
    for root in placement.witness_roots:
        if root.is_symlink() or not root.is_dir():
            reasons.append("PLACEMENT_WITNESS_ROOT_INVALID")
            break

    # Portable Python cannot prove that paths are owned by distinct OS identities.
    reasons.append("OS_IDENTITY_SEPARATION_NOT_ATTESTED")
    structural_reasons = tuple(
        reason
        for reason in reasons
        if reason != "OS_IDENTITY_SEPARATION_NOT_ATTESTED"
    )
    return DeploymentBoundaryAssessment(
        path_separated=not structural_reasons,
        os_identity_separation_verified=False,
        reason_codes=tuple(dict.fromkeys(reasons)),
    )


def _inside(root: Path, candidate: Path) -> bool:
    try:
        return os.path.commonpath((str(root), str(candidate))) == str(root)
    except ValueError:
        return False
