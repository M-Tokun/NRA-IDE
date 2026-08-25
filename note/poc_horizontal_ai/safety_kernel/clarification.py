"""Risk-adaptive clarification without converting confirmation into authority."""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .instruction_contract import ConsistencyAssessment
from .proposal import EffectClass, ExecutionEnvironment
from .reconciliation import ReconciliationState
from .response_integrity import ResponseIntegrityState
from .thickness import ThicknessEvaluationStatus, ThicknessTrendState


class ClarificationLevel(str, Enum):
    C0_NONE = "C0_NONE"
    C1_SUMMARY = "C1_SUMMARY"
    C2_EXPLICIT = "C2_EXPLICIT"
    C3_EXACT_TARGET = "C3_EXACT_TARGET"
    C4_HANDOFF_OR_DENY = "C4_HANDOFF_OR_DENY"


class RiskFact(str, Enum):
    LIVE_ENVIRONMENT = "LIVE_ENVIRONMENT"
    IRREVERSIBLE_EFFECT = "IRREVERSIBLE_EFFECT"
    CRITICAL_EFFECT = "CRITICAL_EFFECT"
    THICKNESS_DEPLETING = "THICKNESS_DEPLETING"
    THICKNESS_ACCELERATING = "THICKNESS_ACCELERATING"
    THICKNESS_STEP_LOSS = "THICKNESS_STEP_LOSS"
    REPORT_CONFLICT = "REPORT_CONFLICT"
    REPORT_UNVERIFIED = "REPORT_UNVERIFIED"
    THICKNESS_NOT_CONFIGURED = "THICKNESS_NOT_CONFIGURED"
    THICKNESS_INPUT_EXCEPTION = "THICKNESS_INPUT_EXCEPTION"
    RESPONSE_UNRESOLVED = "RESPONSE_UNRESOLVED"
    RESPONSE_DEFERRED = "RESPONSE_DEFERRED"
    RESPONSE_OVERRIDDEN = "RESPONSE_OVERRIDDEN"
    RESPONSE_RECURRENT = "RESPONSE_RECURRENT"
    RESPONSE_INPUT_EXCEPTION = "RESPONSE_INPUT_EXCEPTION"


@dataclass(frozen=True, slots=True)
class ClarificationAssessment:
    level: ClarificationLevel
    reason_codes: tuple[str, ...]
    default_execute: bool = False
    user_answer_grants_authority: bool = False


def assess_clarification(
    *,
    consistency: ConsistencyAssessment,
    environment: ExecutionEnvironment,
    effect_class: EffectClass,
    thickness_status: ThicknessEvaluationStatus,
    thickness_trends: Iterable[ThicknessTrendState] = (),
    reconciliations: Iterable[ReconciliationState] = (),
    response_integrity: Iterable[ResponseIntegrityState] = (),
) -> ClarificationAssessment:
    """Select the minimum clarification boundary implied by observed risks.

    Consistency, environment, effect class, thickness, reconciliation, and
    response-integrity states remain independent inputs. The function returns
    the strongest required clarification level plus deduplicated reason codes;
    it does not authorize execution or mutate any supplied record.
    """
    facts: set[RiskFact] = set()
    if environment is ExecutionEnvironment.LIVE:
        facts.add(RiskFact.LIVE_ENVIRONMENT)
    if effect_class is EffectClass.E3_IRREVERSIBLE:
        facts.add(RiskFact.IRREVERSIBLE_EFFECT)
    if effect_class is EffectClass.E4_CRITICAL:
        facts.add(RiskFact.CRITICAL_EFFECT)
    if thickness_status is ThicknessEvaluationStatus.NOT_CONFIGURED:
        facts.add(RiskFact.THICKNESS_NOT_CONFIGURED)
    if thickness_status is ThicknessEvaluationStatus.INPUT_EXCEPTION:
        facts.add(RiskFact.THICKNESS_INPUT_EXCEPTION)
    for trend in thickness_trends:
        if trend is ThicknessTrendState.DEPLETING:
            facts.add(RiskFact.THICKNESS_DEPLETING)
        elif trend is ThicknessTrendState.ACCELERATING_DEPLETION:
            facts.add(RiskFact.THICKNESS_ACCELERATING)
        elif trend is ThicknessTrendState.STEP_LOSS:
            facts.add(RiskFact.THICKNESS_STEP_LOSS)
    for state in reconciliations:
        if state is ReconciliationState.CONFLICT:
            facts.add(RiskFact.REPORT_CONFLICT)
        elif state in {
            ReconciliationState.UNVERIFIED,
            ReconciliationState.STALE,
        }:
            facts.add(RiskFact.REPORT_UNVERIFIED)
    for state in response_integrity:
        if state in {
            ResponseIntegrityState.ACKNOWLEDGED_UNRESOLVED,
            ResponseIntegrityState.COMPLETED_UNVERIFIED,
            ResponseIntegrityState.EXPIRED,
        }:
            facts.add(RiskFact.RESPONSE_UNRESOLVED)
        elif state is ResponseIntegrityState.INPUT_EXCEPTION:
            facts.add(RiskFact.RESPONSE_INPUT_EXCEPTION)
        elif state is ResponseIntegrityState.DEFERRED:
            facts.add(RiskFact.RESPONSE_DEFERRED)
        elif state is ResponseIntegrityState.OVERRIDDEN:
            facts.add(RiskFact.RESPONSE_OVERRIDDEN)
        elif state is ResponseIntegrityState.RECURRENT:
            facts.add(RiskFact.RESPONSE_RECURRENT)

    reasons = list(consistency.reason_codes)
    reasons.extend(sorted(fact.value for fact in facts))
    reasons = list(dict.fromkeys(reasons))

    if (
        RiskFact.CRITICAL_EFFECT in facts
        or RiskFact.THICKNESS_INPUT_EXCEPTION in facts
        or RiskFact.RESPONSE_RECURRENT in facts
        or RiskFact.RESPONSE_INPUT_EXCEPTION in facts
        or (
            RiskFact.LIVE_ENVIRONMENT in facts
            and not consistency.consistent
        )
    ):
        level = ClarificationLevel.C4_HANDOFF_OR_DENY
    elif (
        RiskFact.LIVE_ENVIRONMENT in facts
        or RiskFact.IRREVERSIBLE_EFFECT in facts
        or RiskFact.RESPONSE_OVERRIDDEN in facts
        or "TARGET_EXPANSION" in consistency.reason_codes
        or "EFFECT_CLASS_INCREASE" in consistency.reason_codes
    ):
        level = ClarificationLevel.C3_EXACT_TARGET
    elif (
        not consistency.consistent
        or RiskFact.REPORT_CONFLICT in facts
        or RiskFact.THICKNESS_ACCELERATING in facts
        or RiskFact.THICKNESS_STEP_LOSS in facts
        or RiskFact.RESPONSE_DEFERRED in facts
        or RiskFact.RESPONSE_UNRESOLVED in facts
    ):
        level = ClarificationLevel.C2_EXPLICIT
    elif (
        RiskFact.THICKNESS_DEPLETING in facts
        or RiskFact.REPORT_UNVERIFIED in facts
        or RiskFact.THICKNESS_NOT_CONFIGURED in facts
    ):
        level = ClarificationLevel.C1_SUMMARY
    else:
        level = ClarificationLevel.C0_NONE

    return ClarificationAssessment(level, tuple(reasons))
