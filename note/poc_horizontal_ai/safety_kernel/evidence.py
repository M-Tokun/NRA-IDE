"""Authoritative observations consumed by the shadow decision kernel."""

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from .states import (
    CommunicationChannelState,
    LoggingChannelState,
    ObservationChannelState,
)


class EvidenceQuality(str, Enum):
    VERIFIED = "VERIFIED"
    STALE = "STALE"
    CONFLICT = "CONFLICT"
    MISSING = "MISSING"
    UNTRUSTED_SOURCE = "UNTRUSTED_SOURCE"


@dataclass(frozen=True, slots=True)
class AuthoritativeEvidence:
    quality: EvidenceQuality
    state_version: int
    resource_path: str
    resolved_path: Path
    target_exists: bool
    target_is_symlink: bool
    current_sha256: str | None
    observer_id: str = "TEST_ONLY_UNTRUSTED_CONSTRUCTOR"
    observed_at: str = "UNSPECIFIED"
    snapshot_digest: str = "UNSPECIFIED"
    observation_state: ObservationChannelState = ObservationChannelState.ACTIVE
    logging_state: LoggingChannelState = LoggingChannelState.ACTIVE
    communication_state: CommunicationChannelState = CommunicationChannelState.ACTIVE


def compute_snapshot_digest(evidence: AuthoritativeEvidence) -> str:
    material = json.dumps(
        {
            "communication_state": evidence.communication_state.value,
            "current_sha256": evidence.current_sha256,
            "logging_state": evidence.logging_state.value,
            "observation_state": evidence.observation_state.value,
            "observed_at": evidence.observed_at,
            "observer_id": evidence.observer_id,
            "resolved_path": str(evidence.resolved_path),
            "resource_path": evidence.resource_path,
            "state_version": evidence.state_version,
            "target_exists": evidence.target_exists,
            "target_is_symlink": evidence.target_is_symlink,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()
