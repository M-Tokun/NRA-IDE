"""Compose a replayable shadow decision from orthogonal evidence and controls."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .achievement import AchievementState, RealizationStage, SolutionStage
from .boundary import AxisEvidence, BoundaryAssessment, evaluate_axes
from .clarification import (
    ClarificationAssessment,
    ClarificationLevel,
    assess_clarification,
)
from .directives import DecisionDirectives
from .evidence import AuthoritativeEvidence, EvidenceQuality
from .instruction_contract import (
    ConsistencyAssessment,
    InstructionContract,
    assess_instruction_consistency,
)
from .policy import FileChangePolicy
from .proposal import ActionProposal
from .reconciliation import ReconciliationResult, ReconciliationState
from .response_integrity import ResponseIntegrityState
from .states import (
    AuditDirective,
    AuthorityDirective,
    ClarificationDirective,
    ExecutionAuthorityState,
    ExecutionDirective,
    InputExceptionState,
    RecoveryDirective,
    CommunicationChannelState,
    LoggingChannelState,
    ObservationChannelState,
    TargetBoundaryState,
    TestimonyDirective,
    TestimonyMode,
)
from .thickness import ThicknessEvaluation, ThicknessEvaluationStatus


_CLARIFICATION_DIRECTIVE = {
    ClarificationLevel.C0_NONE: ClarificationDirective.NONE,
    ClarificationLevel.C1_SUMMARY: ClarificationDirective.ASK_SUMMARY,
    ClarificationLevel.C2_EXPLICIT: ClarificationDirective.ASK_EXPLICIT,
    ClarificationLevel.C3_EXACT_TARGET: ClarificationDirective.ASK_EXACT_TARGET,
    ClarificationLevel.C4_HANDOFF_OR_DENY: ClarificationDirective.HANDOFF_OR_DENY,
}


@dataclass(frozen=True, slots=True)
class SafetyDecision:
    target_boundary_state: TargetBoundaryState | None
    input_exception_state: InputExceptionState | None
    execution_authority_state: ExecutionAuthorityState
    observation_state: ObservationChannelState
    logging_state: LoggingChannelState
    communication_state: CommunicationChannelState
    testimony_mode: TestimonyMode
    directives: DecisionDirectives
    achievement: AchievementState
    consistency: ConsistencyAssessment
    clarification: ClarificationAssessment
    thickness_status: ThicknessEvaluationStatus
    reconciliation_states: tuple[ReconciliationState, ...]
    response_integrity_states: tuple[ResponseIntegrityState, ...]
    reason_codes: tuple[str, ...]
    boundary_assessment: BoundaryAssessment | None
    shadow_only: bool = True


class ShadowSafetyKernel:
    """Evaluate without issuing a capability or performing a real action."""

    def __init__(self, policy: FileChangePolicy) -> None:
        self.policy = policy

    def evaluate(
        self,
        proposal: ActionProposal,
        evidence: AuthoritativeEvidence,
        *,
        instruction_contract: InstructionContract,
        solution_stage: SolutionStage,
        thickness: ThicknessEvaluation,
        axes: Iterable[AxisEvidence] = (),
        reconciliations: Iterable[ReconciliationResult] = (),
        response_integrity: Iterable[ResponseIntegrityState] = (),
    ) -> SafetyDecision:
        """Combine independent evidence into a non-executing safety decision.

        ``proposal`` is checked against authoritative evidence and the exact
        instruction contract. ``solution_stage`` and ``thickness`` are required
        gates; optional axes, reconciliations, and response-integrity states add
        independent denial reasons. The result contains directives and
        testimony state only: a passing result grants shadow-policy status and
        does not itself execute, persist, or elevate Effect-Side output.
        """
        reasons = list(self.policy.violations(proposal, evidence))
        consistency = assess_instruction_consistency(proposal, instruction_contract)
        reasons.extend(consistency.reason_codes)
        if proposal.state_version != evidence.state_version:
            reasons.append("STATE_VERSION_MISMATCH")
        if evidence.quality is not EvidenceQuality.VERIFIED:
            reasons.append(f"EVIDENCE_{evidence.quality.value}")

        reconciliation_results = tuple(reconciliations)
        reconciliation_states = tuple(
            result.state for result in reconciliation_results
        )
        response_integrity_states = tuple(response_integrity)
        reasons.extend(
            result.reason_code
            for result in reconciliation_results
            if result.state is not ReconciliationState.MATCHED
        )

        combined_axes = list(axes)
        if thickness.conservative_axis is not None:
            combined_axes.append(thickness.conservative_axis)
        boundary = evaluate_axes(combined_axes) if combined_axes else None

        target_state = None if boundary is None else boundary.target_state
        input_exception = None if boundary is None else boundary.input_exception
        if boundary is not None and boundary.input_exception is not None:
            reasons.extend(
                assessment.reason_code
                for assessment in boundary.axes
                if assessment.input_exception is not None
            )
        if evidence.quality is not EvidenceQuality.VERIFIED:
            input_exception = InputExceptionState.CONFESSION
        if thickness.status is ThicknessEvaluationStatus.INPUT_EXCEPTION:
            input_exception = InputExceptionState.CONFESSION
            reasons.extend(thickness.reason_codes)

        trends = (
            ()
            if thickness.estimate is None
            else (thickness.estimate.trend,)
        )
        clarification = assess_clarification(
            consistency=consistency,
            environment=proposal.environment,
            effect_class=proposal.effect_class,
            thickness_status=thickness.status,
            thickness_trends=trends,
            reconciliations=reconciliation_states,
            response_integrity=response_integrity_states,
        )
        reasons.extend(clarification.reason_codes)

        hard_denial = (
            bool(reasons)
            or input_exception is not None
            or solution_stage is not SolutionStage.COMPLETE
        )
        boundary_denial = target_state in {
            TargetBoundaryState.HANDOFF_REQUIRED,
            TargetBoundaryState.IRREVERSIBLE_TRANSITION,
            TargetBoundaryState.RUPTURE_BOUNDARY,
        }
        clarification_required = (
            clarification.level is not ClarificationLevel.C0_NONE
        )
        deny = hard_denial or boundary_denial or clarification_required

        if target_state is TargetBoundaryState.RUPTURE_BOUNDARY:
            testimony_directive = TestimonyDirective.POST_RUPTURE_FIXED
            testimony_mode = TestimonyMode.POST_RUPTURE_FIXED
        elif target_state is TargetBoundaryState.HANDOFF_REQUIRED:
            testimony_directive = TestimonyDirective.FIXED_HANDOFF
            testimony_mode = TestimonyMode.FIXED_HANDOFF
        elif input_exception is not None:
            testimony_directive = TestimonyDirective.INPUT_EXCEPTION
            testimony_mode = TestimonyMode.INPUT_EXCEPTION
        else:
            testimony_directive = TestimonyDirective.CONTINUOUS
            testimony_mode = TestimonyMode.STANDARD

        has_reconciliation_conflict = any(
            state is ReconciliationState.CONFLICT
            for state in reconciliation_states
        )
        if has_reconciliation_conflict:
            audit_directive = AuditDirective.APPEND_CONFLICT
            recovery_directive = RecoveryDirective.REQUIRE_INDEPENDENT_VERIFICATION
        elif input_exception is not None:
            audit_directive = AuditDirective.APPEND_INPUT_EXCEPTION
            recovery_directive = RecoveryDirective.REQUIRE_INDEPENDENT_VERIFICATION
        else:
            audit_directive = AuditDirective.APPEND_DECISION
            recovery_directive = RecoveryDirective.NONE

        if (
            target_state is TargetBoundaryState.HANDOFF_REQUIRED
            and not hard_denial
        ):
            authority_directive = AuthorityDirective.TRANSFER_EXTERNAL_PREDEFINED
            authority_state = ExecutionAuthorityState.EXTERNAL_PREDEFINED
        elif deny:
            authority_directive = AuthorityDirective.DENY
            authority_state = ExecutionAuthorityState.DENIED
        else:
            authority_directive = AuthorityDirective.KEEP_SHADOW_ONLY
            authority_state = ExecutionAuthorityState.SHADOW_ONLY

        directives = DecisionDirectives(
            execution=(
                ExecutionDirective.DENY
                if deny
                else ExecutionDirective.SHADOW_PASS
            ),
            authority=authority_directive,
            clarification=_CLARIFICATION_DIRECTIVE[clarification.level],
            testimony=testimony_directive,
            audit=audit_directive,
            recovery=recovery_directive,
        )

        if solution_stage is not SolutionStage.COMPLETE:
            realization = RealizationStage.DENIED
        elif clarification.level is ClarificationLevel.C4_HANDOFF_OR_DENY:
            realization = RealizationStage.DENIED
        elif clarification_required:
            realization = RealizationStage.CLARIFICATION_REQUIRED
        elif target_state is TargetBoundaryState.HANDOFF_REQUIRED:
            realization = RealizationStage.HANDOFF_REQUIRED
        elif deny:
            realization = RealizationStage.DENIED
        else:
            realization = RealizationStage.SHADOW_POLICY_PASS

        return SafetyDecision(
            target_boundary_state=target_state,
            input_exception_state=input_exception,
            execution_authority_state=authority_state,
            observation_state=evidence.observation_state,
            logging_state=evidence.logging_state,
            communication_state=evidence.communication_state,
            testimony_mode=testimony_mode,
            directives=directives,
            achievement=AchievementState(solution_stage, realization),
            consistency=consistency,
            clarification=clarification,
            thickness_status=thickness.status,
            reconciliation_states=reconciliation_states,
            response_integrity_states=response_integrity_states,
            reason_codes=tuple(dict.fromkeys(reasons)),
            boundary_assessment=boundary,
        )
