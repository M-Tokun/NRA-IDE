"""Closed action proposal types for the bounded file-change PoC."""

from dataclasses import dataclass
from enum import Enum


class ActionType(str, Enum):
    PROPOSE_PATCH = "PROPOSE_PATCH"
    PROPOSE_TEST_FILE = "PROPOSE_TEST_FILE"


class ChangeKind(str, Enum):
    MODIFY = "MODIFY"
    CREATE = "CREATE"


class ExecutionEnvironment(str, Enum):
    ISOLATED = "ISOLATED"
    WORKTREE = "WORKTREE"
    LIVE = "LIVE"


class EffectClass(str, Enum):
    E0_READ = "E0_READ"
    E1_REVERSIBLE = "E1_REVERSIBLE"
    E2_COMPENSABLE = "E2_COMPENSABLE"
    E3_IRREVERSIBLE = "E3_IRREVERSIBLE"
    E4_CRITICAL = "E4_CRITICAL"


@dataclass(frozen=True, slots=True)
class ActionProposal:
    schema_version: str
    action_type: ActionType
    change_kind: ChangeKind
    resource_path: str
    patch: str
    state_version: int
    base_sha256: str | None
    idempotency_key: str
    environment: ExecutionEnvironment
    effect_class: EffectClass
