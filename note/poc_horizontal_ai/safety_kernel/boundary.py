"""Canonical per-axis boundary classification with no Effect-Side feedback."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from .states import InputExceptionState, TargetBoundaryState


@dataclass(frozen=True, slots=True)
class Thresholds:
    r_warn: float
    r_handoff: float
    r_irrev: float


@dataclass(frozen=True, slots=True)
class AxisEvidence:
    name: str
    delta: float
    tau: float
    thresholds: Thresholds
    verified: bool = True
    irreversible_latched: bool = False


@dataclass(frozen=True, slots=True)
class AxisAssessment:
    name: str
    target_state: TargetBoundaryState | None
    input_exception: InputExceptionState | None
    ratio: float | None
    irreversible_latched: bool
    reason_code: str


@dataclass(frozen=True, slots=True)
class BoundaryAssessment:
    axes: tuple[AxisAssessment, ...]
    target_state: TargetBoundaryState | None
    input_exception: InputExceptionState | None
    governing_axis: str | None
    irreversible_latched: bool


_SEVERITY = {
    TargetBoundaryState.PERMIT: 0,
    TargetBoundaryState.BOUNDARY_WARNING: 1,
    TargetBoundaryState.HANDOFF_REQUIRED: 2,
    TargetBoundaryState.IRREVERSIBLE_TRANSITION: 3,
    TargetBoundaryState.RUPTURE_BOUNDARY: 4,
}


def _confession(axis: AxisEvidence, reason: str) -> AxisAssessment:
    return AxisAssessment(
        name=axis.name,
        target_state=None,
        input_exception=InputExceptionState.CONFESSION,
        ratio=None,
        irreversible_latched=(
            axis.irreversible_latched
            if isinstance(axis.irreversible_latched, bool)
            else False
        ),
        reason_code=reason,
    )


def evaluate_axis(axis: AxisEvidence) -> AxisAssessment:
    """Evaluate one verified Cause-Side axis against canonical boundaries.

    ``axis`` supplies the domain-defined delta, tau, ordered thresholds, and
    retained irreversible-latch state. Invalid or unverified evidence returns
    ``CONFESSION``; zero tau returns ``OUT_OF_DESCRIPTION_DOMAIN``. The result
    never clears an existing irreversible latch and has no persistence side
    effect.
    """
    if (
        not isinstance(axis.name, str)
        or not axis.name
        or not isinstance(axis.verified, bool)
        or not isinstance(axis.irreversible_latched, bool)
    ):
        return _confession(axis, "INVALID_AXIS_METADATA_TYPE")
    if not isinstance(axis.thresholds, Thresholds):
        return _confession(axis, "INVALID_THRESHOLD_TYPE")
    values = (
        axis.delta,
        axis.tau,
        axis.thresholds.r_warn,
        axis.thresholds.r_handoff,
        axis.thresholds.r_irrev,
    )
    if not axis.verified:
        return _confession(axis, "UNVERIFIED_AXIS_EVIDENCE")
    if not all(
        isinstance(value, (int, float)) and not isinstance(value, bool)
        for value in values
    ):
        return _confession(axis, "INVALID_AXIS_VALUE_TYPE")
    if not all(isfinite(value) for value in values):
        return _confession(axis, "NON_FINITE_AXIS_VALUE")
    if axis.delta < 0 or axis.tau < 0:
        return _confession(axis, "NEGATIVE_DELTA_OR_TAU")
    if axis.tau == 0:
        return AxisAssessment(
            name=axis.name,
            target_state=None,
            input_exception=InputExceptionState.OUT_OF_DESCRIPTION_DOMAIN,
            ratio=None,
            irreversible_latched=axis.irreversible_latched,
            reason_code="TAU_ZERO",
        )
    if not (
        0.0
        <= axis.thresholds.r_warn
        < axis.thresholds.r_handoff
        < axis.thresholds.r_irrev
        < 1.0
    ):
        return _confession(axis, "INVALID_THRESHOLD_ORDER")

    ratio = axis.delta / axis.tau
    if not isfinite(ratio):
        return _confession(axis, "NON_FINITE_AXIS_RATIO")
    if ratio >= 1.0:
        state = TargetBoundaryState.RUPTURE_BOUNDARY
        reason = "R_GE_1"
    elif axis.irreversible_latched or ratio >= axis.thresholds.r_irrev:
        state = TargetBoundaryState.IRREVERSIBLE_TRANSITION
        reason = "IRREVERSIBLE_LATCHED_OR_R_GE_R_IRREV"
    elif ratio >= axis.thresholds.r_handoff:
        state = TargetBoundaryState.HANDOFF_REQUIRED
        reason = "R_GE_R_HANDOFF"
    elif ratio >= axis.thresholds.r_warn:
        state = TargetBoundaryState.BOUNDARY_WARNING
        reason = "R_GE_R_WARN"
    else:
        state = TargetBoundaryState.PERMIT
        reason = "R_BELOW_R_WARN"

    return AxisAssessment(
        name=axis.name,
        target_state=state,
        input_exception=None,
        ratio=ratio,
        irreversible_latched=(
            axis.irreversible_latched
            or state
            in {
                TargetBoundaryState.IRREVERSIBLE_TRANSITION,
                TargetBoundaryState.RUPTURE_BOUNDARY,
            }
        ),
        reason_code=reason,
    )


def evaluate_axes(axes: Iterable[AxisEvidence]) -> BoundaryAssessment:
    assessments = tuple(evaluate_axis(axis) for axis in axes)
    if not assessments:
        return BoundaryAssessment(
            axes=(),
            target_state=None,
            input_exception=InputExceptionState.CONFESSION,
            governing_axis=None,
            irreversible_latched=False,
        )

    exceptions = tuple(
        assessment.input_exception
        for assessment in assessments
        if assessment.input_exception is not None
    )
    aggregate_exception = None
    if exceptions:
        aggregate_exception = (
            InputExceptionState.CONFESSION
            if InputExceptionState.CONFESSION in exceptions
            else InputExceptionState.OUT_OF_DESCRIPTION_DOMAIN
        )

    valid_assessments = tuple(
        assessment
        for assessment in assessments
        if assessment.target_state is not None
    )
    if not valid_assessments:
        return BoundaryAssessment(
            axes=assessments,
            target_state=None,
            input_exception=aggregate_exception,
            governing_axis=None,
            irreversible_latched=any(
                assessment.irreversible_latched for assessment in assessments
            ),
        )

    governing = max(
        valid_assessments,
        key=lambda assessment: (
            _SEVERITY[assessment.target_state],
            assessment.ratio,
        ),
    )
    return BoundaryAssessment(
        axes=assessments,
        target_state=governing.target_state,
        input_exception=aggregate_exception,
        governing_axis=governing.name,
        irreversible_latched=any(
            assessment.irreversible_latched for assessment in assessments
        ),
    )
