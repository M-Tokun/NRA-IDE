"""File-change invariant adapter connecting FileChangePolicy to the runtime hook."""

from __future__ import annotations

from pathlib import Path

from ..safety_kernel.observer import TrustedFileObserver
from ..safety_kernel.policy import FileChangePolicy
from ..safety_kernel.proposal import (
    ActionProposal,
    ActionType,
    ChangeKind,
    EffectClass,
    ExecutionEnvironment,
)
from .execution_gate import BoundaryExecutionIntent, FileChangeContext


class FileChangeInvariantAdapter:
    """Bind the generic hard-invariant hook to the bounded file-change domain.

    The trusted runtime stays domain-neutral (design doc 12.3): this adapter
    is the only component that (1) requires the authorizer-committed
    ``FileChangeContext`` on the signed intent, (2) reconstructs a safety
    kernel ``ActionProposal`` from the intent + action bytes, and (3)
    re-observes the real repository file immediately before execution
    (TOCTOU prevention). Violation codes are returned to the runtime hook,
    which rejects execution before the executor is reached.

    The adapter is fail-closed: malformed input produces violation codes,
    never a silent pass-through.
    """

    def __init__(
        self,
        *,
        repository_root: Path,
        policy: FileChangePolicy,
        observer_id: str,
        environment: ExecutionEnvironment = ExecutionEnvironment.WORKTREE,
    ) -> None:
        if not isinstance(repository_root, Path):
            raise ValueError("repository_root must be a Path")
        if not isinstance(policy, FileChangePolicy):
            raise ValueError("policy must be a FileChangePolicy")
        if not observer_id:
            raise ValueError("observer_id must not be empty")
        if environment is ExecutionEnvironment.LIVE:
            raise ValueError(
                "LIVE environment is forbidden for the file-change adapter"
            )
        self.repository_root = repository_root
        self.policy = policy
        self.observer_id = observer_id
        self.environment = environment
        self._observer = TrustedFileObserver(repository_root, observer_id)

    def __call__(
        self,
        intent: BoundaryExecutionIntent,
        action: bytes,
    ) -> tuple[str, ...]:
        """Reconstruct the proposal, re-observe reality, and run the policy."""
        context = intent.file_change
        if context is None:
            return ("FILE_CHANGE_CONTEXT_REQUIRED",)
        try:
            context.validate()  # defensive re-check of the signed binding
        except (TypeError, ValueError):
            return ("EXECUTION_FILE_CHANGE_CONTEXT_INVALID",)
        try:
            patch = action.decode("utf-8")
        except UnicodeDecodeError:
            return ("ACTION_NOT_UTF8",)
        proposal = self._build_proposal(context, patch, intent.intent_id)
        observation = self._observer.observe(
            context.resource_path,
            context.state_version,
        )
        if observation.evidence is None:
            return tuple(dict.fromkeys(observation.reason_codes))
        return tuple(
            dict.fromkeys(self.policy.violations(proposal, observation.evidence))
        )

    def _build_proposal(
        self,
        context: FileChangeContext,
        patch: str,
        idempotency_key: str,
    ) -> ActionProposal:
        return ActionProposal(
            schema_version="1.0",
            action_type=ActionType(context.action_type),
            change_kind=ChangeKind(context.change_kind),
            resource_path=context.resource_path,
            patch=patch,
            state_version=context.state_version,
            base_sha256=context.expected_base_sha256,
            idempotency_key=idempotency_key,
            environment=self.environment,
            effect_class=EffectClass.E1_REVERSIBLE,
        )
