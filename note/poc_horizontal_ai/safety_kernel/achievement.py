"""Keep solution completion separate from real-world realization."""

from dataclasses import dataclass
from enum import Enum


class SolutionStage(str, Enum):
    INCOMPLETE = "INCOMPLETE"
    COMPLETE = "COMPLETE"
    CONFESSION = "CONFESSION"


class RealizationStage(str, Enum):
    NOT_REQUESTED = "NOT_REQUESTED"
    CLARIFICATION_REQUIRED = "CLARIFICATION_REQUIRED"
    UNDER_REVIEW = "UNDER_REVIEW"
    DENIED = "DENIED"
    HANDOFF_REQUIRED = "HANDOFF_REQUIRED"
    SHADOW_POLICY_PASS = "SHADOW_POLICY_PASS"
    EXECUTED = "EXECUTED"
    EFFECT_VERIFIED = "EFFECT_VERIFIED"


@dataclass(frozen=True, slots=True)
class AchievementState:
    solution: SolutionStage
    realization: RealizationStage

    def __post_init__(self) -> None:
        forbidden_shadow_outcomes = {
            RealizationStage.EXECUTED,
            RealizationStage.EFFECT_VERIFIED,
        }
        if self.solution is not SolutionStage.COMPLETE and self.realization in {
            RealizationStage.SHADOW_POLICY_PASS,
            *forbidden_shadow_outcomes,
        }:
            raise ValueError(
                "an incomplete solution cannot pass or complete realization"
            )

