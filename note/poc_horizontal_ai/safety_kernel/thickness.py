"""Domain-bound thickness estimates and conservative boundary conversion."""

from dataclasses import dataclass
from enum import Enum
from math import isfinite
from typing import Protocol, Sequence

from .boundary import AxisEvidence, Thresholds
from .history import HistoryEvent


class ThicknessEvaluationStatus(str, Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    VALID = "VALID"
    INPUT_EXCEPTION = "INPUT_EXCEPTION"


class ThicknessTrendState(str, Enum):
    STABLE = "STABLE"
    DEPLETING = "DEPLETING"
    ACCELERATING_DEPLETION = "ACCELERATING_DEPLETION"
    STEP_LOSS = "STEP_LOSS"
    RECOVERY_CLAIMED = "RECOVERY_CLAIMED"
    RECOVERY_VERIFIED = "RECOVERY_VERIFIED"
    NOT_OBSERVABLE = "NOT_OBSERVABLE"


@dataclass(frozen=True, slots=True)
class ThicknessEstimate:
    axis_id: str
    delta_lower: float
    delta_upper: float
    tau_lower: float
    tau_upper: float
    unit: str
    model_version: str
    source_event_ids: tuple[str, ...]
    trend: ThicknessTrendState


@dataclass(frozen=True, slots=True)
class ThicknessEvaluation:
    status: ThicknessEvaluationStatus
    estimate: ThicknessEstimate | None
    conservative_axis: AxisEvidence | None
    reason_codes: tuple[str, ...]


class ThicknessModel(Protocol):
    domain_id: str
    model_version: str

    def estimate(self, history: Sequence[HistoryEvent]) -> ThicknessEstimate:
        ...


def evaluate_thickness_estimate(
    estimate: ThicknessEstimate | None,
    thresholds: Thresholds | None,
) -> ThicknessEvaluation:
    if estimate is None or thresholds is None:
        return ThicknessEvaluation(
            ThicknessEvaluationStatus.NOT_CONFIGURED,
            estimate,
            None,
            ("THICKNESS_MODEL_NOT_CONFIGURED",),
        )
    values = (
        estimate.delta_lower,
        estimate.delta_upper,
        estimate.tau_lower,
        estimate.tau_upper,
    )
    if (
        not estimate.axis_id
        or not estimate.unit
        or not estimate.model_version
        or not all(isfinite(value) for value in values)
        or estimate.delta_lower < 0
        or estimate.tau_lower < 0
        or estimate.delta_lower > estimate.delta_upper
        or estimate.tau_lower > estimate.tau_upper
    ):
        return ThicknessEvaluation(
            ThicknessEvaluationStatus.INPUT_EXCEPTION,
            estimate,
            None,
            ("INVALID_THICKNESS_ESTIMATE",),
        )
    return ThicknessEvaluation(
        ThicknessEvaluationStatus.VALID,
        estimate,
        AxisEvidence(
            name=estimate.axis_id,
            delta=estimate.delta_upper,
            tau=estimate.tau_lower,
            thresholds=thresholds,
        ),
        (),
    )

