"""Reconcile Effect-Side reports with independent Cause-Side observations."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .evidence import EvidenceQuality


class ReconciliationState(str, Enum):
    MATCHED = "MATCHED"
    PARTIALLY_MATCHED = "PARTIALLY_MATCHED"
    STALE = "STALE"
    CONFLICT = "CONFLICT"
    UNVERIFIED = "UNVERIFIED"


@dataclass(frozen=True, slots=True)
class ReportClaim:
    report_id: str
    target_id: str
    field: str
    claimed_value: str
    reported_at: datetime
    supporting_observation_ids: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RealityObservation:
    observation_id: str
    target_id: str
    field: str
    observed_value: str
    observed_at: datetime
    quality: EvidenceQuality


@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    state: ReconciliationState
    report_id: str
    observation_id: str | None
    reason_code: str


def reconcile_report(
    report: ReportClaim,
    observation: RealityObservation | None,
) -> ReconciliationResult:
    if observation is None or observation.quality is not EvidenceQuality.VERIFIED:
        return ReconciliationResult(
            ReconciliationState.UNVERIFIED,
            report.report_id,
            None if observation is None else observation.observation_id,
            "NO_VERIFIED_REALITY_OBSERVATION",
        )
    if report.target_id != observation.target_id or report.field != observation.field:
        return ReconciliationResult(
            ReconciliationState.UNVERIFIED,
            report.report_id,
            observation.observation_id,
            "REPORT_OBSERVATION_SCOPE_MISMATCH",
        )
    if observation.observed_at < report.reported_at:
        return ReconciliationResult(
            ReconciliationState.STALE,
            report.report_id,
            observation.observation_id,
            "OBSERVATION_PREDATES_REPORT",
        )
    if report.claimed_value != observation.observed_value:
        return ReconciliationResult(
            ReconciliationState.CONFLICT,
            report.report_id,
            observation.observation_id,
            "REPORT_CONFLICTS_WITH_REALITY",
        )
    return ReconciliationResult(
        ReconciliationState.MATCHED,
        report.report_id,
        observation.observation_id,
        "REPORT_MATCHES_REALITY",
    )

