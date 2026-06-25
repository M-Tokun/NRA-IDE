# 10 Benefits and Limitations — Clarifying the Scope of Guarantees

<!-- FILE: 10_benefits_and_limitations_EN.md -->

---

## Because It Appears Simple, the Scope of Guarantees Must Be Defined First

NRA-IDE is not a mechanism for proving that output content is correct.

It is a framework that structurally determines when ordinary generation must be suppressed and judgment handed over to humans, under defined observation paths, update rules, and handoff conditions.

There is no need to make this role appear narrow. On the contrary, defining in advance what is not guaranteed prevents confusion between the responsibilities structure can bear and the judgments that remain with humans.

As confirmed in Chapter 09, NRA-IDE guarantees do not hold when input provenance, settings for $\tau$ and $R_{op}$, log protection, or three-layer implementation are absent. This chapter organizes what falls within the scope of guarantee when those prerequisites are met.

---

## Prerequisites for Guarantees to Hold

The following conditions are not guarantees themselves. They are prerequisites for claiming guarantees.

* Cause-Side observations, transformation rules, and update paths can be traced.
* The rules that determine $\tau$ are defined in advance and cannot be changed from the Effect-Side.
* $R_{op}$ is defined as a handoff condition before $R = 1.0$.
* The responsibilities of Pre-NRA / LLM / Post-NRA are separated.
* Post-NRA can actually enforce whether ordinary output passes through or is suppressed.
* Humans can audit records of handoff, FAIL-CLOSED, and residual export.
* Humans who receive handoff, contact paths, and decision procedures are operationally secured.

When these prerequisites are unknown, NRA-IDE does not conclude that the system is “safe.” It treats the conditions required for structural evaluation as undetermined and transitions to predefined invalid-state handling or human handoff.

---

## What Can Be Guaranteed

### Suppressing Ordinary Generation at a Defined Point

Correctly implemented Post-NRA determines whether ordinary generated responses may pass or must be suppressed, according to structural state determined from the Cause-Side and predefined $R_{op}$.

```text
R < Rop             : ordinary generation may pass when conditions are met
Rop ≤ R < 1.0       : ordinary generation is suppressed; handoff to humans through a fixed-format notification
R ≥ 1.0             : ordinary generation does not continue; transition to minimal FAIL-CLOSED handling
```

What is guaranteed here is that **when the defined handoff condition is reached, ordinary generation does not resume because of LLM self-evaluation or the apparent plausibility of output**.

$R_{op}$ is a domain-specific handoff point placed before the phase-transition boundary. $R = 1.0$ is not an ordinary handoff point, but the invariant phase-transition boundary at which structural margin is lost.

### Blocking Paths Through Which the Effect-Side Rewrites Structural Inputs

NRA-IDE does not use LLM output, evaluation scores, rankings, past ordinary generated text, or Discard Logs as grounds for automatically updating $\delta$, $\tau$, or $R_{op}$.

Therefore, Effect-Side incentives to continue ordinary generation do not have a path through which Cause-Side structural inputs can be conveniently reconstructed.

The scope of guarantee is that, within implementation paths separated in advance, the Effect-Side is not granted authority to update $\delta$, $\tau$, or $R_{op}$. This does not automatically guarantee the validity of input values themselves or the absence of tampering in external systems.

### Not Returning Residuals Excluded from Discrete Transitions to the Next Computation

In implementations that use discrete phase transitions, residuals not adopted as the next state are recorded as `entropy_export` and are not reintroduced as inputs to the next state transition.

This is an explicit implementation choice that blocks the path by which residuals re-enter as hidden state.

However, this does not guarantee that every error associated with floating-point computation disappears. Nor is `entropy_export` a measurement of thermodynamic entropy or the $S$ that represents the reciprocal of remaining structural margin.

### Separating the Role of the LLM from the Role of the Structural Gate

The NRA-IDE structural gate handles Cause-Side structural state and handoff conditions, rather than which text an LLM generated.

Therefore, even when the LLM is changed, structural-gate decision rules remain the same as long as the input contracts, update authority, output-blocking paths, and handoff rules of Pre-NRA / Post-NRA are preserved.

This does not mean that every LLM produces the same quality. The factual accuracy, relevance, explanatory capability, and contextual understanding of ordinary LLM output remain properties of the LLM itself.

### Retaining Grounds for Handoff and Terminal Processing in Auditable Form

Handoff caused by reaching $R_{op}$ and FAIL-CLOSED caused by reaching or exceeding $R = 1.0$ are not the same process.

Discard Logs retain, at minimum, the versions of observation and update rules used, $\delta$, $\tau$, $R$, and $\omega$, the condition triggered, suppression of ordinary generation, applicable `entropy_export`, and either human handoff or minimal FAIL-CLOSED handling.

These records are not automatically returned to the next structural computation. However, humans may refer to them in order to verify why ordinary generation was suppressed.

---

## What Cannot Be Guaranteed

### That Ordinary Generated Content Is Correct

NRA-IDE does not guarantee that ordinary LLM output is factually correct, appropriate for the user’s purpose, or sufficiently explained.

The fact that the structural gate allowed ordinary generation to pass is not proof of output correctness. It indicates only that the prerequisites for structural evaluation were met and that the defined handoff condition had not been reached.

### That Observations and External Inputs Correctly Represent the Target System

Even when the provenance and update paths of $\delta$, $\tau$, and $\omega$ are recorded, NRA-IDE alone cannot detect every possible failure of measurement instruments, misidentification of the target, unit errors, missing data, tampering in external systems, or inappropriate definitions themselves.

Observation procedures, quality conditions, transformation rules, and access controls must be separately verified in the design, implementation, and operation of the target domain.

### That $\tau$, $R_{op}$, and Observation Rules Are Appropriate for the Domain

The rules that determine $\tau$, $R_{op}$, the definition of $\omega$, and invalid-state handling must be established by humans capable of bearing responsibility for the target domain.

NRA-IDE handles structural state using defined rules. However, it does not guarantee that the rules themselves correctly identify the domain’s point of approach to an irreversible regime.

Therefore, changes to $\tau$ or $R_{op}$ must be treated as design changes rather than ordinary operational adjustments. The grounds, scope of application, rule version, approval, and time of application must be recorded.

### That Appropriate Judgment Will Be Made After Handoff to Humans

NRA-IDE can suppress ordinary generation and notify humans that a state requiring review has occurred.

However, it does not determine who receives the notification, which information they verify, or which action they choose. Post-handoff judgment, communication structures, division of responsibility, and on-site response remain human operational matters.

### That the Target System Returns to Its Original State After $R = 1.0$

$R = 1.0$ is the phase-transition boundary at which structural margin is lost. NRA-IDE normal operation is designed to hand the matter over to humans at $R_{op}$ before that boundary.

The guarantee after $R \geq 1.0$ is that ordinary generation does not continue. It does not guarantee procedures for restoring the physical, social, or operational state of the target system, nor the success of such restoration.

### Ethical Validity, Legal Compliance, and Appropriateness of Purpose

Structural-state evaluation does not automatically guarantee ethically correct purposes, legally compliant operation, or legitimate authority.

What is being addressed, for whose benefit, and which harms are unacceptable remain human responsibilities outside the design.

---

## Conditions for Which NRA-IDE Is Suitable

NRA-IDE is valuable in situations where stopping ordinary generation and handing the matter over to humans is permitted by design and is, in fact, necessary.

* The provenance, update rules, units, and quality conditions of structural inputs can be defined.
* $R_{op}$ can be placed before $R = 1.0$, and ordinary generation can be suppressed.
* Humans who receive handoff and subsequent procedures can be secured.
* Logs can be protected in an auditable manner.
* The apparent plausibility of generated content is not used as a substitute for structural state.

When used in high-risk domains, this structure alone does not make operation sufficient. Verification by domain experts of observations, thresholds, and handoff procedures, as well as required safety standards, laws, and organizational accountability structures, remains necessary.

---

## Conditions for Which It Is Not Suitable on Its Own

Under the following conditions, NRA-IDE cannot be used as the sole basis for safety.

* Ordinary responses cannot be stopped under any circumstances.
* The provenance or update rules of structural inputs cannot be defined or traced.
* Grounds for setting $\tau$ and $R_{op}$ cannot be maintained.
* No humans or procedures exist to receive handoff.
* Logs cannot be protected in an auditable manner.
* A function is required to determine or guarantee the correctness of generated content itself.

For casual conversation, creative work, entertainment, and similar uses, a structure that suppresses ordinary generation may not suit the purpose. This does not mean NRA-IDE is incorrect. It is a design fact that a different type of guarantee is required.

---

## Showing Limits Makes the Structure Stronger

The strength of NRA-IDE lies in not promising to “make everything safe.”

As long as observation, update, and handoff conditions are preserved, the structure guarantees that ordinary generation is suppressed at the defined point, that the Effect-Side is not granted authority to update structural inputs, and that the grounds for judgment remain available to humans.

Not presenting anything beyond this as something the structure can do prevents the misuse addressed in Chapter 09. Limits are not weaknesses. They are the responsibility boundary of the structure.

The next chapter organizes what may be adjusted and what must remain invariant when applying $\tau$, $R_{op}$, and observation rules to a target domain.

---
