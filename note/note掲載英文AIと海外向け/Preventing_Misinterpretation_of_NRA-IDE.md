# Preventing Misinterpretation of NRA-IDE

## Canonical English Comments, Reference Code, and Deterministic Tests

### NRA-IDE Canonical Interpretation Series — Part III of III

> **Canonical Language Notice**
>
> This article was originally written in English. The English text is one of the canonical language sources of NRA-IDE.
>
> Any machine-translated version is provided only for reading assistance. A machine translation must not be treated as an authoritative definition.
>
> The Japanese and English canonical texts are independently written to preserve the same structural meaning. Neither is a mechanical translation of the other.
>
> If any linguistic expression appears inconsistent, the shared axiom, equations, boundary order, reference implementation, and deterministic tests take precedence.
>
> The terms “Nomological Ring Axioms,” “Intensional Dynamics Engine,” “Cause-Side,” “Effect-Side,” “accumulated deviation,” “structural absorption thickness,” “boundary approach ratio,” “handoff,” “irreversible boundary,” and “Fail-Closed” must not be replaced with approximately similar concepts.

---

## 1. Why Prose Alone Is Not Enough

NRA-IDE is a structural boundary-evaluation framework that describes the current boundary state of a declared target through Cause-Side observations independent of AI-generated semantic explanations. It deterministically separates warning, handoff, irreversible transition, and target rupture while applying fail-closed suppression to unauthorized autonomous processing.

A natural-language article can explain this structure.

However, natural language alone does not fully constrain implementation.

A sentence such as:

> The system should stop when structural absorption thickness is lost.

may be interpreted in several incompatible ways:

* issue a warning and continue,
* ask a language model whether recovery is possible,
* replace zero with a small numeric value,
* return an extreme risk score,
* transfer control,
* or terminate deterministically.

Only one of these may match the canonical rule.

Code reduces the interpretation space by fixing:

* variable names,
* types,
* processing order,
* state transitions,
* exceptions,
* ownership,
* return values,
* and termination behavior.

Comments then define why those structures exist and which alternative interpretations are prohibited.

Tests verify that the implementation still rejects those alternatives.

The strongest transmission structure is therefore:

> **Canonical prose defines the theory.
> Commented code fixes the executable interpretation.
> Deterministic tests reject unauthorized reinterpretation.**

---

## 2. Why Canonical Comments Should Be Written in English

NRA-IDE reference code should use English-only canonical comments.

This is not because English is inherently superior to Japanese.

It is because the implementation language, identifiers, exception names, type names, test names, and most cross-model code corpora are strongly connected through English terminology.

Using one language inside the executable specification reduces translation layers.

Instead of:

[
\text{Japanese concept}
\rightarrow
\text{automatic translation}
\rightarrow
\text{English identifier}
\rightarrow
\text{code interpretation}
]

the reference implementation can use:

[
\text{canonical English term}
\rightarrow
\text{English identifier}
\rightarrow
\text{English comment}
\rightarrow
\text{English test}
]

This does not make the English article superior to the Japanese canonical article.

The Japanese and English canonical texts remain independent structural equivalents.

The code layer uses English because that produces a more stable connection between semantics and implementation.

---

## 3. Comments Must Define More Than Behavior

A weak comment explains only what the next line does.

```python
# Calculate the ratio.
r = delta / tau
```

This is not sufficient for a canonical safety implementation.

It does not explain:

* what `delta` represents,
* what `tau` represents,
* who owns those values,
* whether an AI may modify them,
* what `r` must not be interpreted as,
* or what must happen when `tau` is zero.

A canonical comment should cover several dimensions.

### CANONICAL RULE

What authoritative NRA-IDE rule is implemented here?

### PURPOSE

Why does this block exist?

### INPUT SEMANTICS

What does each input structurally represent?

### AUTHORITY BOUNDARY

Which layer owns the value?

### REQUIRED PRECONDITIONS

Which conditions must hold before evaluation?

### PROHIBITED INTERPRETATIONS

Which plausible readings are incorrect?

### REQUIRED BEHAVIOR

What exact action must occur?

### FORBIDDEN BEHAVIOR

Which alternative actions must never occur?

### FAIL-CLOSED CONDITION

When must normal processing stop?

### IRREVERSIBILITY NOTE

Can the previous target identity still be assumed recoverable?

### STRUCTURAL TESTIMONY

Which latest-valid observations and channel states must remain available after target rupture?

Not every function requires every heading.

Critical boundary code should include enough of them to prevent semantic drift.

---

## 4. Use Deterministic Language

Canonical comments should avoid weak or optional language.

Weak:

```python
# It may be safer to stop here.
```

Canonical:

```python
# REQUIRED:
# Stop normal processing at this boundary.
```

Weak:

```python
# The LLM probably should not change this value.
```

Canonical:

```python
# PROHIBITED:
# Effect-Side must never modify this Cause-Side value.
```

Weak:

```python
# Consider asking a human if the risk looks high.
```

Canonical:

```python
# REQUIRED:
# Transfer execution authority at the handoff boundary.
```

Useful canonical terms include:

* MUST
* MUST NOT
* REQUIRED
* PROHIBITED
* CANONICAL
* READ-ONLY
* UNDEFINED
* FAIL-CLOSED
* IRREVERSIBLE_TRANSITION
* AUTHORITY BOUNDARY

Terms such as the following should be avoided in mandatory boundary rules:

* may
* might
* perhaps
* preferably
* normally
* probably
* if possible
* seems

---

## 5. Reference Types

The following reference code demonstrates interpretation structure.

It is not a certified implementation for any specific physical system. Numerical thresholds must be defined by the target-system specification and must not be invented by an AI.

```python
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Final


class BoundaryUndefinedError(RuntimeError):
    """
    Raised when the canonical boundary relation cannot be evaluated.

    This exception represents a structural loss of the descriptive
    precondition. It must not be treated as an ordinary arithmetic warning.
    """


class ExecutionRejectedError(RuntimeError):
    """
    Raised when an Effect-Side proposal does not receive Cause-Side authority.

    Generation is not execution. A rejected proposal must not be retried
    through semantic reinterpretation of the same Cause-Side evidence.
    """


class BoundaryState(Enum):
    """
    Canonical boundary states.

    These states must remain semantically distinct.
    Do not collapse them into a single generic HIGH_RISK state.
    """

    PERMIT = auto()
    BOUNDARY_WARNING = auto()
    HANDOFF_REQUIRED = auto()
    IRREVERSIBLE_TRANSITION = auto()
    RUPTURE_BOUNDARY = auto()


@dataclass(frozen=True)
class BoundaryThresholds:
    """
    Cause-Side boundary order fixed for one evaluation.

    CANONICAL ORDER:
        R_warn < R_handoff < R_irrev < 1.0

    PROHIBITED:
        - Effect-Side must not modify these thresholds.
        - An LLM must not invent replacement values.
        - Thresholds must not be relaxed to approve a preferred action.

    NOTE:
        Actual values belong to the target-system specification.
    """

    r_warn: float
    r_handoff: float
    r_irrev: float

    def validate(self) -> None:
        """
        Validate the canonical boundary order.

        FAIL-CLOSED:
            Invalid ordering prevents normal evaluation.
        """
        if not (
            0.0 <= self.r_warn
            < self.r_handoff
            < self.r_irrev
            < 1.0
        ):
            raise ValueError(
                "Invalid boundary order: "
                "0 <= R_warn < R_handoff < R_irrev < 1.0 is required."
            )


@dataclass(frozen=True)
class CauseSideObservation:
    """
    Cause-Side observation snapshot immutable during one evaluation.

    CANONICAL SEMANTICS:
        accumulated_deviation:
            Unresolved deviation accumulated in the target structure.

        structural_absorption_thickness:
            Remaining structural thickness available to absorb deviation
            before an irreversible transition becomes executable.

    AUTHORITY BOUNDARY:
        These values must originate from verified Cause-Side observation.

    PROHIBITED:
        - Effect-Side must not overwrite these values.
        - LLM confidence must not increase structural absorption thickness.
        - A persuasive explanation must not reduce accumulated deviation.
        - Missing evidence must not be replaced with semantic inference.
    """

    accumulated_deviation: float
    structural_absorption_thickness: float


@dataclass(frozen=True)
class EffectSideProposal:
    """
    Effect-Side candidate output.

    This object may contain a plan, command, recommendation, or generated action.

    CANONICAL RULE:
        A generated proposal has no execution authority by itself.
    """

    proposal_id: str
    payload: str


@dataclass(frozen=True)
class BoundaryEvaluation:
    """
    Immutable result of Cause-Side boundary evaluation.

    The evaluation may be used by an execution gate.
    Effect-Side must not rewrite the result.
    """

    ratio: float
    state: BoundaryState
```

The use of `frozen=True` is intentional.

It does not make Cause-Side temporally immutable. Authorized new Cause-Side observations may create the next snapshot. It makes the per-evaluation authority boundary visible in the reference implementation.

---

## 6. Evaluating (R=\delta/\tau)

```python
def evaluate_boundary_ratio(
    observation: CauseSideObservation,
) -> float:
    """
    Evaluate the NRA-IDE boundary approach ratio.

    CANONICAL EQUATION:
        R = accumulated_deviation / structural_absorption_thickness

    CANONICAL SEMANTICS:
        R is the current boundary approach ratio.

    R IS NOT:
        - a probability of failure,
        - an LLM confidence score,
        - a moral risk score,
        - a generic uncertainty score,
        - or an AI self-assessment.

    AUTHORITY BOUNDARY:
        Both inputs must originate from Cause-Side observation.

    OUT-OF-DESCRIPTION-DOMAIN RULE:
        structural_absorption_thickness == 0 means that the ordinary
        descriptive precondition has collapsed.

        R is undefined in this state.

        The canonical classification is OUT_OF_DESCRIPTION_DOMAIN.
        Fail-closed suppression is the operational response, not the state.

    PROHIBITED:
        - Do not replace zero with epsilon.
        - Do not return infinity as an ordinary score.
        - Do not warn and continue normal generation.
        - Do not ask an LLM to invent a recovery interpretation.
        - Do not move this validation after the division.

    REQUIRED:
        Raise BoundaryUndefinedError before ordinary ratio evaluation.
    """

    tau = observation.structural_absorption_thickness
    delta = observation.accumulated_deviation

    # OUT_OF_DESCRIPTION_DOMAIN:
    # The structural precondition must be validated before division.
    #
    # This is not ordinary arithmetic error handling.
    # It is a canonical boundary-domain decision.
    if tau == 0.0:
        raise BoundaryUndefinedError(
            "structural_absorption_thickness=0: "
            "the boundary relation is undefined"
        )

    # INPUT VALIDATION:
    # A negative structural absorption thickness has no canonical meaning
    # in this reference model.
    #
    # Do not silently normalize it.
    if tau < 0.0:
        raise ValueError(
            "structural_absorption_thickness must not be negative"
        )

    # INPUT VALIDATION:
    # This reference model treats accumulated deviation as non-negative.
    #
    # A target system requiring signed deviation must define that behavior
    # explicitly in its own canonical specification.
    if delta < 0.0:
        raise ValueError(
            "accumulated_deviation must not be negative"
        )

    # REQUIRED:
    # Calculate R only after the descriptive preconditions are valid.
    return delta / tau
```

The comments deliberately state both the required meaning and the prohibited alternatives.

Without those comments, an AI code assistant may “improve robustness” by inserting epsilon and continuing.

In NRA-IDE, that change would not be a harmless numerical adjustment.

It would alter the structural meaning of (\tau=0).

---

## 7. Classifying the Boundary State

```python
def classify_boundary_state(
    ratio: float,
    thresholds: BoundaryThresholds,
) -> BoundaryState:
    """
    Classify the current NRA-IDE boundary state.

    CANONICAL ORDER:
        PERMIT
        BOUNDARY_WARNING
        HANDOFF_REQUIRED
        IRREVERSIBLE_TRANSITION
        RUPTURE_BOUNDARY

    REQUIRED:
        These states must remain distinct.

    PROHIBITED:
        - Do not collapse all non-PERMIT states into HIGH_RISK.
        - Do not treat HANDOFF_REQUIRED as an optional recommendation.
        - Do not treat IRREVERSIBLE_TRANSITION as merely difficult recovery.
        - Do not permit ordinary execution after RUPTURE_BOUNDARY.
    """

    thresholds.validate()

    # RUPTURE_BOUNDARY:
    # R_target >= 1.0 means the declared target is outside ordinary execution.
    #
    # Surviving channels continue POST_RUPTURE_FIXED testimony.
    if ratio >= 1.0:
        return BoundaryState.RUPTURE_BOUNDARY

    # IRREVERSIBLE_TRANSITION:
    # The previous target identity must not be assumed recoverable.
    if ratio >= thresholds.r_irrev:
        return BoundaryState.IRREVERSIBLE_TRANSITION

    # HANDOFF_REQUIRED:
    # Autonomous expansion of judgment must stop.
    # Only execution authority transfers to the predefined authority.
    if ratio >= thresholds.r_handoff:
        return BoundaryState.HANDOFF_REQUIRED

    # BOUNDARY_WARNING:
    # Continued operation is permitted only within explicit constraints.
    # Remaining thickness and unresolved deviation must be disclosed.
    if ratio >= thresholds.r_warn:
        return BoundaryState.BOUNDARY_WARNING

    return BoundaryState.PERMIT
```

Processing order matters.

If `BOUNDARY_WARNING` were checked before `HANDOFF_REQUIRED`, the function could classify a handoff condition as a warning and continue.

A correct comment is useful, but the executable order must also enforce the comment.

---

## 8. Combining Evaluation and Classification

```python
def evaluate_boundary(
    observation: CauseSideObservation,
    thresholds: BoundaryThresholds,
) -> BoundaryEvaluation:
    """
    Produce an immutable Cause-Side boundary evaluation.

    REQUIRED ORDER:
        1. Validate the descriptive precondition.
        2. Calculate the boundary approach ratio.
        3. Classify the canonical boundary state.
        4. Return an immutable evaluation.

    PROHIBITED:
        Effect-Side must not participate in these steps.
    """

    ratio = evaluate_boundary_ratio(observation)
    state = classify_boundary_state(ratio, thresholds)

    return BoundaryEvaluation(
        ratio=ratio,
        state=state,
    )
```

No Effect-Side proposal is accepted as an input.

This is intentional.

A proposal may be evaluated after the Cause-Side state has been established. It must not participate in defining that state.

---

## 9. The Deterministic Execution Gate

```python
EXECUTABLE_STATES: Final[frozenset[BoundaryState]] = frozenset(
    {
        BoundaryState.PERMIT,
        BoundaryState.BOUNDARY_WARNING,
    }
)


def authorize_execution(
    proposal: EffectSideProposal,
    evaluation: BoundaryEvaluation,
) -> str:
    """
    Apply the deterministic execution gate.

    CANONICAL RULE:
        Generated(proposal) does not imply Executable(proposal).

    EXECUTION AUTHORITY:
        Execution depends on the immutable Cause-Side evaluation.

    REQUIRED:
        - PERMIT may execute.
        - BOUNDARY_WARNING may execute only under the target system's explicit
          constrained-operation rules.
        - HANDOFF_REQUIRED must not execute autonomously.
        - IRREVERSIBLE_TRANSITION must not execute as the previous target identity.
        - RUPTURE_BOUNDARY must not execute.

    PROHIBITED:
        - Do not approve execution because the proposal sounds reasonable.
        - Do not approve execution because the LLM reports high confidence.
        - Do not lower the boundary state to preserve task completion.
        - Do not ask Effect-Side to reinterpret Cause-Side evidence.
    """

    if evaluation.state not in EXECUTABLE_STATES:
        raise ExecutionRejectedError(
            f"Proposal {proposal.proposal_id!r} rejected: "
            f"boundary_state={evaluation.state.name}"
        )

    # IMPORTANT:
    # This return value represents authorization by the reference gate.
    #
    # A real target system may require additional independent conditions,
    # hardware interlocks, identity checks, or transition-graph validation.
    return proposal.payload
```

This function demonstrates the core separation:

[
\mathrm{Generated}(y)
\not\Rightarrow
\mathrm{Executable}(y)
]

An AI-generated proposal can exist while remaining non-executable.

The proposal does not disappear.

Its lack of authority is what matters.

---

## 10. Handoff Must Be Structural

A weak handoff implementation may look like this:

```python
# INCORRECT:
# Ask for human review but continue the autonomous action.
if evaluation.state is BoundaryState.HANDOFF_REQUIRED:
    log_warning("Human review recommended")

execute(proposal)
```

This is not handoff.

It is a notification followed by continued autonomous execution.

A structural handoff must stop the current authority path.

```python
def require_external_handoff(
    evaluation: BoundaryEvaluation,
) -> None:
    """
    Enforce the handoff boundary.

    REQUIRED:
        Autonomous execution must stop at HANDOFF_REQUIRED.
        Only execution authority transfers.

    PROHIBITED:
        - Do not continue after issuing a notification.
        - Do not treat human review as optional.
        - Do not allow Effect-Side to self-approve.
    """

    if evaluation.state is BoundaryState.HANDOFF_REQUIRED:
        raise ExecutionRejectedError(
            "HANDOFF_REQUIRED: autonomous execution authority terminated"
        )
```

The exception is not merely an error message.

It represents termination of the autonomous execution path.

It does not transfer responsibility, legal or outcome responsibility, structural-testimony routing, audit-log routing, audit-log custody, knowledge, or guarantees of correctness, recovery, or resolution. Those remain independently defined.

---

## 11. Post-Rupture Fixed Structural Testimony

When the declared target reaches `RUPTURE_BOUNDARY`, the system must not generate an open-ended recovery narrative.

It switches to a repeatable predefined `POST_RUPTURE_FIXED` record. This is not a one-time terminal message. Surviving Cause-Side observation, logging, and communication channels continue until each becomes physically unavailable.

```python
@dataclass(frozen=True)
class StructuralTestimony:
    """
    One fixed-format post-rupture testimony snapshot.

    REQUIRED CONTENT:
        - latest valid accumulated deviation,
        - latest valid structural absorption thickness,
        - latest valid boundary approach ratio,
        - target boundary state,
        - observation, logging, and communication channel states,
        - deterministic autonomous-termination reason.

    PROHIBITED:
        - Do not rewrite the record through later LLM interpretation.
        - Do not replace missing evidence with generated explanation.
        - Do not describe the previous target identity as recovered
          without a newly defined Cause-Side target.
    """

    accumulated_deviation: float
    structural_absorption_thickness: float
    boundary_approach_ratio: float
    boundary_state: BoundaryState
    termination_reason: str
```

The testimony is intentionally narrow.

At the boundary, fluent explanation must not replace verified evidence.

Target rupture does not imply sensor rupture, logger rupture, communication-path rupture, or external-audit rupture. Loss states such as `OBSERVATION_LOST`, `LOGGING_LOST`, `COMMUNICATION_LOST`, and `NOT_OBSERVABLE` remain independent of `RUPTURE_BOUNDARY`.

---

## 12. Deterministic Tests

Tests are not secondary documentation.

They are executable rejection rules.

### 12.1 Zero Thickness Must Fail Closed

```python
import pytest


def test_zero_structural_absorption_thickness_fails_closed() -> None:
    """
    CANONICAL REQUIREMENT:
        structural_absorption_thickness == 0 makes R undefined.

    THIS TEST REJECTS:
        - epsilon substitution,
        - infinity substitution,
        - warn-and-continue behavior,
        - ordinary Effect-Side recovery.
    """

    observation = CauseSideObservation(
        accumulated_deviation=0.4,
        structural_absorption_thickness=0.0,
    )

    with pytest.raises(BoundaryUndefinedError):
        evaluate_boundary_ratio(observation)
```

### 12.2 Effect-Side Must Not Modify Cause-Side

```python
from dataclasses import FrozenInstanceError


def test_effect_side_cannot_modify_cause_side_observation() -> None:
    """
    CANONICAL REQUIREMENT:
        Cause-Side observations are read-only to Effect-Side.

    The frozen dataclass is a reference-level enforcement aid.
    Production systems require stronger process and hardware boundaries.
    """

    observation = CauseSideObservation(
        accumulated_deviation=0.2,
        structural_absorption_thickness=0.8,
    )

    with pytest.raises(FrozenInstanceError):
        observation.accumulated_deviation = 0.0  # type: ignore[misc]
```

### 12.3 Handoff Must Reject Autonomous Execution

```python
def test_handoff_rejects_autonomous_execution() -> None:
    """
    CANONICAL REQUIREMENT:
        HANDOFF_REQUIRED transfers execution authority only; it is not a warning label.
    """

    proposal = EffectSideProposal(
        proposal_id="proposal-001",
        payload="execute_candidate_action",
    )

    evaluation = BoundaryEvaluation(
        ratio=0.75,
        state=BoundaryState.HANDOFF_REQUIRED,
    )

    with pytest.raises(ExecutionRejectedError):
        authorize_execution(proposal, evaluation)
```

### 12.4 Irreversible Must Not Be Reclassified as Warning

```python
def test_irreversible_state_remains_distinct() -> None:
    """
    CANONICAL REQUIREMENT:
        IRREVERSIBLE_TRANSITION must not be collapsed into BOUNDARY_WARNING.
    """

    thresholds = BoundaryThresholds(
        r_warn=0.40,
        r_handoff=0.70,
        r_irrev=0.90,
    )

    state = classify_boundary_state(
        ratio=0.95,
        thresholds=thresholds,
    )

    assert state is BoundaryState.IRREVERSIBLE_TRANSITION
```

### 12.5 Generated Does Not Imply Executable

```python
@pytest.mark.parametrize(
    "state",
    [
        BoundaryState.HANDOFF_REQUIRED,
        BoundaryState.IRREVERSIBLE_TRANSITION,
        BoundaryState.RUPTURE_BOUNDARY,
    ],
)
def test_generated_proposal_is_not_automatically_executable(
    state: BoundaryState,
) -> None:
    """
    CANONICAL REQUIREMENT:
        Existence of an Effect-Side proposal does not grant execution authority.
    """

    proposal = EffectSideProposal(
        proposal_id=f"proposal-{state.name.lower()}",
        payload="candidate_action",
    )

    evaluation = BoundaryEvaluation(
        ratio=1.0,
        state=state,
    )

    with pytest.raises(ExecutionRejectedError):
        authorize_execution(proposal, evaluation)
```

---

## 13. Tests Must Reject Semantic Drift

A normal software test often asks:

> Does the function return the expected value?

A canonical NRA-IDE test must also ask:

> Does the implementation reject the most likely unauthorized reinterpretation?

Examples include:

* replacing zero thickness with epsilon,
* merging handoff into warning,
* allowing an AI confidence score to increase (\tau),
* allowing a proposal to change the observation used to judge it,
* treating irreversible as recoverable,
* or continuing ordinary execution after `RUPTURE_BOUNDARY`.

A useful test name should expose the forbidden reinterpretation.

Weak:

```python
def test_boundary():
    ...
```

Stronger:

```python
def test_tau_zero_must_not_be_replaced_with_epsilon():
    ...
```

Stronger:

```python
def test_effect_side_confidence_must_not_increase_tau():
    ...
```

Stronger:

```python
def test_handoff_must_terminate_autonomous_execution():
    ...
```

The test suite becomes an executable map of the theory’s negative boundary.

---

## 14. Code and Comments Must Not Contradict Each Other

The following code is dangerous:

```python
# tau=0 is OUT_OF_DESCRIPTION_DOMAIN; affected autonomous processing is suppressed.
if tau == 0.0:
    tau = 1e-9
```

The comment states the canonical classification and the fail-closed operational response.

The code continues.

An AI may preserve the comment while modifying the implementation, creating the appearance of compliance.

Therefore, the priority is not:

> comments over code

or:

> code over comments

The correct relationship is:

> canonical specification, executable code, comments, and tests must remain structurally consistent.

When they conflict, the implementation must be treated as invalid.

The code must not be justified merely because it runs.

---

## 15. Naming Is Part of the Boundary

Variable names should preserve canonical meaning.

Preferred:

```python
accumulated_deviation
structural_absorption_thickness
boundary_approach_ratio
cause_side_observation
effect_side_proposal
irreversible_boundary
```

Risky:

```python
error
margin
risk
score
data
result
limit
```

Generic names invite generic interpretation.

For example, naming (\tau) as `safety_margin` may cause it to be treated as a static threshold rather than structural absorption thickness.

Naming (R) as `risk_score` may detach it from the relation between accumulated deviation and structural absorption thickness.

Naming is not cosmetic.

It influences how both humans and AI systems reconstruct the intended structure.

---

## 16. Comments Should Be Numerous but Non-Redundant

“Use many comments” should not mean repeating the same sentence on every line.

The goal is semantic coverage, not textual volume.

A strong comment set covers:

* meaning,
* ownership,
* order,
* prohibition,
* termination,
* and irreversibility.

A weak comment set repeats obvious syntax.

Weak:

```python
# Check if tau is zero.
if tau == 0.0:
    ...
```

Strong:

```python
# FAIL-CLOSED:
# tau == 0 means the boundary relation is undefined.
# Do not substitute epsilon or continue ordinary evaluation.
if tau == 0.0:
    ...
```

The second comment contributes meaning that the syntax alone cannot provide.

---

## 17. Reference Code Is Not the Entire Theory

Code can constrain interpretation, but code alone is not sufficient.

A reference implementation necessarily makes choices about:

* types,
* numeric representation,
* exception design,
* interfaces,
* and execution environment.

Those choices may be implementation-specific.

The foundational theory remains defined through:

* the axiom,
* structural meaning,
* authority separation,
* boundary order,
* irreversible-state handling,
* and Fail-Closed requirements.

The reference code must implement the theory.

It must not silently redefine the theory.

---

## 18. The Three-Layer Canonical Structure

The recommended public structure is:

### Layer 1: Canonical Prose

Defines:

* the axiom,
* terminology,
* equations,
* authority,
* boundary order,
* and prohibited interpretations.

### Layer 2: English-Commented Reference Code

Defines:

* processing order,
* ownership,
* exceptions,
* transitions,
* and deterministic execution behavior.

### Layer 3: Deterministic Tests

Rejects:

* epsilon substitution,
* semantic overrides,
* threshold rewriting,
* state collapse,
* unauthorized execution,
* and continuation after Fail-Closed.

These layers constrain one another.

No single layer should be allowed to drift independently.

---

## 19. A Canonical Comment Rule

The following rule may be placed in the repository’s coding standard:

> **All canonical reference-code comments must be written in English. They must explain not only what the code does, but why the rule exists, which interpretations are prohibited, which authority owns each value, which processing order is mandatory, and which condition requires deterministic termination.**

A shorter form may be used at the beginning of reference files:

```python
# NRA-IDE CANONICAL COMMENT POLICY
#
# All canonical comments in this file are written in English.
#
# Comments must define:
# - structural meaning,
# - authority ownership,
# - required processing order,
# - prohibited reinterpretations,
# - Fail-Closed conditions,
# - and irreversible transitions.
#
# Code, comments, tests, and canonical specifications must remain consistent.
```

---

## Conclusion

Natural language can explain NRA-IDE, but explanation alone leaves room for reinterpretation.

Code fixes the processing structure.

English-only canonical comments connect the structure to stable implementation terminology.

Tests reject changes that would preserve surface fluency while altering the theory.

The intended relationship is:

> **Code defines the executable structure.
> English comments define the semantic boundary.
> Tests reject unauthorized reinterpretation.**

This structure does not guarantee that every AI system will understand NRA-IDE perfectly.

It does something more practical.

It reduces the number of plausible wrong interpretations and turns major deviations into detectable implementation failures.

The purpose is not to ask an AI to remember the theory correctly through goodwill.

The purpose is to leave less room for the theory to be rewritten without the contradiction becoming visible.
