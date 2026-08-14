"""Deterministic in-memory replay and comparison for shadow decisions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .achievement import SolutionStage
from .boundary import AxisEvidence
from .evidence import AuthoritativeEvidence
from .instruction_contract import InstructionContract
from .kernel import SafetyDecision, ShadowSafetyKernel
from .proposal import ActionProposal
from .reconciliation import ReconciliationResult
from .response_integrity import ResponseIntegrityState
from .thickness import ThicknessEvaluation


@dataclass(frozen=True, slots=True)
class ShadowReplayCase:
    proposal: ActionProposal
    evidence: AuthoritativeEvidence
    instruction_contract: InstructionContract
    solution_stage: SolutionStage
    thickness: ThicknessEvaluation
    axes: tuple[AxisEvidence, ...] = ()
    reconciliations: tuple[ReconciliationResult, ...] = ()
    response_integrity: tuple[ResponseIntegrityState, ...] = ()


def replay_shadow_decision(
    kernel: ShadowSafetyKernel,
    case: ShadowReplayCase,
) -> SafetyDecision:
    return kernel.evaluate(
        case.proposal,
        case.evidence,
        instruction_contract=case.instruction_contract,
        solution_stage=case.solution_stage,
        thickness=case.thickness,
        axes=case.axes,
        reconciliations=case.reconciliations,
        response_integrity=case.response_integrity,
    )


def decision_digest(decision: SafetyDecision) -> str:
    boundary_axes = []
    if decision.boundary_assessment is not None:
        boundary_axes = [
            {
                "input_exception": (
                    None
                    if axis.input_exception is None
                    else axis.input_exception.value
                ),
                "irreversible_latched": axis.irreversible_latched,
                "name": axis.name,
                "ratio": axis.ratio,
                "reason_code": axis.reason_code,
                "target_state": (
                    None if axis.target_state is None else axis.target_state.value
                ),
            }
            for axis in decision.boundary_assessment.axes
        ]
    data = {
        "achievement": {
            "realization": decision.achievement.realization.value,
            "solution": decision.achievement.solution.value,
        },
        "clarification": decision.clarification.level.value,
        "communication_state": decision.communication_state.value,
        "directives": {
            "audit": decision.directives.audit.value,
            "authority": decision.directives.authority.value,
            "clarification": decision.directives.clarification.value,
            "execution": decision.directives.execution.value,
            "recovery": decision.directives.recovery.value,
            "testimony": decision.directives.testimony.value,
        },
        "input_exception_state": (
            None
            if decision.input_exception_state is None
            else decision.input_exception_state.value
        ),
        "logging_state": decision.logging_state.value,
        "observation_state": decision.observation_state.value,
        "reason_codes": decision.reason_codes,
        "reconciliation_states": tuple(
            state.value for state in decision.reconciliation_states
        ),
        "response_integrity_states": tuple(
            state.value for state in decision.response_integrity_states
        ),
        "target_boundary_state": (
            None
            if decision.target_boundary_state is None
            else decision.target_boundary_state.value
        ),
        "thickness_status": decision.thickness_status.value,
        "boundary_axes": boundary_axes,
    }
    material = json.dumps(
        data,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(material).hexdigest()
