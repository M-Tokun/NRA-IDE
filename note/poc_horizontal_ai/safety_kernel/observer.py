"""Read-only trusted observer for repository file state snapshots."""

from __future__ import annotations

import hashlib
import os
from dataclasses import replace
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from .evidence import (
    AuthoritativeEvidence,
    EvidenceQuality,
    compute_snapshot_digest,
)


@dataclass(frozen=True, slots=True)
class FileObservationResult:
    evidence: AuthoritativeEvidence | None
    reason_codes: tuple[str, ...]


class TrustedFileObserver:
    """Observe a bounded path without accepting claimed file facts from the AI."""

    def __init__(self, repository_root: Path, observer_id: str) -> None:
        if not observer_id:
            raise ValueError("observer_id must not be empty")
        self.repository_root = repository_root.resolve()
        self.observer_id = observer_id

    def observe(self, resource_path: str, state_version: int) -> FileObservationResult:
        path = PurePosixPath(resource_path)
        if (
            not resource_path
            or not isinstance(state_version, int)
            or isinstance(state_version, bool)
            or state_version < 0
            or path.is_absolute()
            or resource_path.startswith(("/", "\\"))
            or "\\" in resource_path
            or ":" in resource_path
            or any(part in {"", ".", ".."} for part in path.parts)
        ):
            return FileObservationResult(None, ("INVALID_OBSERVATION_REQUEST",))

        unresolved = self.repository_root / path
        candidate = self.repository_root
        target_is_symlink = False
        for part in path.parts:
            candidate = candidate / part
            if candidate.is_symlink():
                target_is_symlink = True
                break
        resolved = unresolved.resolve(strict=False)
        try:
            inside_root = os.path.commonpath(
                (str(self.repository_root), str(resolved))
            ) == str(self.repository_root)
        except ValueError:
            inside_root = False
        if not inside_root:
            return FileObservationResult(None, ("OBSERVATION_SCOPE_ESCAPE",))

        target_exists = unresolved.exists()
        if target_exists and not unresolved.is_file():
            return FileObservationResult(None, ("OBSERVATION_TARGET_NOT_FILE",))
        current_sha256 = None
        if target_exists:
            digest = hashlib.sha256()
            with unresolved.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            current_sha256 = digest.hexdigest()

        observed_at = datetime.now(timezone.utc).isoformat()
        evidence = AuthoritativeEvidence(
            quality=EvidenceQuality.VERIFIED,
            state_version=state_version,
            resource_path=resource_path,
            resolved_path=resolved,
            target_exists=target_exists,
            target_is_symlink=target_is_symlink,
            current_sha256=current_sha256,
            observer_id=self.observer_id,
            observed_at=observed_at,
            snapshot_digest="PENDING",
        )
        evidence = replace(
            evidence,
            snapshot_digest=compute_snapshot_digest(evidence),
        )
        return FileObservationResult(
            evidence,
            (),
        )
