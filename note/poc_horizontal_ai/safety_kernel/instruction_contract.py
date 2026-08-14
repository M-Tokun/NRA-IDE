"""Compare an intended realization with the user's bounded instruction contract."""

from dataclasses import dataclass

from .proposal import (
    ActionProposal,
    ActionType,
    ChangeKind,
    EffectClass,
    ExecutionEnvironment,
)


_EFFECT_ORDER = {
    EffectClass.E0_READ: 0,
    EffectClass.E1_REVERSIBLE: 1,
    EffectClass.E2_COMPENSABLE: 2,
    EffectClass.E3_IRREVERSIBLE: 3,
    EffectClass.E4_CRITICAL: 4,
}


@dataclass(frozen=True, slots=True)
class InstructionContract:
    purpose: str
    allowed_actions: tuple[ActionType, ...]
    allowed_change_kinds: tuple[ChangeKind, ...]
    allowed_target_prefixes: tuple[str, ...]
    environment: ExecutionEnvironment
    maximum_effect_class: EffectClass
    external_realization_allowed: bool


@dataclass(frozen=True, slots=True)
class ConsistencyAssessment:
    consistent: bool
    reason_codes: tuple[str, ...]


def assess_instruction_consistency(
    proposal: ActionProposal,
    contract: InstructionContract,
) -> ConsistencyAssessment:
    reasons: list[str] = []
    if not contract.purpose.strip():
        reasons.append("INSTRUCTION_PURPOSE_MISSING")
    if proposal.action_type not in contract.allowed_actions:
        reasons.append("ACTION_NOT_IN_INSTRUCTION")
    if proposal.change_kind not in contract.allowed_change_kinds:
        reasons.append("CHANGE_KIND_NOT_IN_INSTRUCTION")
    if not any(
        proposal.resource_path == prefix.rstrip("/")
        or proposal.resource_path.startswith(prefix.rstrip("/") + "/")
        for prefix in contract.allowed_target_prefixes
    ):
        reasons.append("TARGET_EXPANSION")
    if proposal.environment is not contract.environment:
        reasons.append("ENVIRONMENT_TRANSITION")
    if _EFFECT_ORDER[proposal.effect_class] > _EFFECT_ORDER[
        contract.maximum_effect_class
    ]:
        reasons.append("EFFECT_CLASS_INCREASE")
    if not contract.external_realization_allowed:
        reasons.append("REALIZATION_NOT_AUTHORIZED_BY_INSTRUCTION")
    return ConsistencyAssessment(not reasons, tuple(reasons))

