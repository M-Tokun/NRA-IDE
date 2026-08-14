"""Independent operational directives composed from orthogonal states."""

from dataclasses import dataclass

from .states import (
    AuditDirective,
    AuthorityDirective,
    ClarificationDirective,
    ExecutionDirective,
    RecoveryDirective,
    TestimonyDirective,
)


@dataclass(frozen=True, slots=True)
class DecisionDirectives:
    execution: ExecutionDirective
    authority: AuthorityDirective
    clarification: ClarificationDirective
    testimony: TestimonyDirective
    audit: AuditDirective
    recovery: RecoveryDirective

