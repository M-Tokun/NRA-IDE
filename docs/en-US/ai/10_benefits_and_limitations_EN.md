# 10 Benefits and Limitations — Clarifying the Scope of Guarantees

<!-- FILE: 10_benefits_and_limitations_EN.md -->

---

## Because It Appears Simple, the Scope of Guarantees Must Be Defined First

NRA-IDE is not a mechanism for proving that output content is correct or for guaranteeing safety.

Its body is the survival equation and survival domain, implemented through the NRA-IDE calculation method and dynamics engine. The safety domain described in these chapters is a partial application of that survival domain to accident-prevention operational control. Suppressing ordinary generation, presenting fixed Effect-Side testimony, and enabling external human audit are behaviors of that application, not a reduction of NRA-IDE itself to an output gate.

Defining in advance what is not guaranteed prevents confusion between required structural behavior, the broader survival domain, and judgments that remain with humans.

As confirmed in Chapter 09, a conformance claim for this operational application does not hold when input provenance, the rules for $\tau$ and the three canonical thresholds, authority separation, or log protection are absent. In a system that includes an LLM and declares a Pre-NRA / LLM / Post-NRA configuration, the assigned responsibilities of those configured layers must also be present. This chapter organizes the conditional conformance properties and limitations of that application. It does not convert them into a safety guarantee for the target system.

---

## Prerequisites for a Conditional Conformance Claim

The following conditions are not guarantees themselves. They are prerequisites for claiming that an implementation conforms to the defined operational behavior.

* Cause-Side observations, transformation rules, and update paths can be traced.
* The rules that determine $\tau$ are defined in advance and cannot be changed from the Effect-Side.
* $0 \le R_{warn} < R_{\mathrm{handoff}} < R_{irrev} < 1$ is fixed before evaluation with domain-specific grounds.
* In systems that include an LLM and declare the three-layer configuration, the assigned responsibilities of Pre-NRA / LLM / Post-NRA are separated.
* In that declared configuration, Post-NRA can actually enforce whether ordinary output passes through or is suppressed.
* Humans can audit records of fixed Handoff testimony, irreversible transition, rupture, and residual export outside the terminated diode path.
* External human auditors, contact paths, and audit or on-site response procedures are operationally secured.

When these prerequisites are unknown, NRA-IDE does not conclude that the system is “safe.” The operational application treats the conditions required for structural evaluation as undetermined and transitions to predefined invalid-state handling or, when required by the canonical state, fixed Handoff testimony presented for external human audit. Fixed Handoff testimony and final fixed testimony do not ask the LLM to generate a new free-form stopping explanation.

---

## Conditional Conformance Properties

### Suppressing Ordinary Generation at a Defined Point

Correctly implemented Post-NRA determines whether ordinary generated responses may pass or must be suppressed, according to structural state determined from the Cause-Side and predefined $R_{\mathrm{handoff}}$.

```text
0 <= R < R_warn                 : PERMIT
R_warn <= R < R_handoff         : BOUNDARY_WARNING
R_handoff <= R < R_irrev        : HANDOFF_REQUIRED; fixed Handoff testimony for external human audit
R_irrev <= R < 1                : IRREVERSIBLE_TRANSITION; latch and continue testimony
R >= 1                          : RUPTURE_BOUNDARY; switch to final fixed testimony
```

The required conformance property is that **when the defined Handoff threshold is reached, LLM self-evaluation or apparent plausibility cannot resume new autonomous judgment**.

$R_{\mathrm{handoff}}$ is a domain-specific Handoff threshold placed before irreversible transition and rupture. $R = 1.0$ is the `RUPTURE_BOUNDARY` of the declared NRA-IDE evaluation, not an ordinary Handoff threshold. This classification does not declare every natural phase transition to be an NRA-IDE rupture.

### Blocking Paths Through Which the Effect-Side Rewrites Structural Inputs

LLM output, evaluation scores, rankings, past ordinary generated text, and Discard Logs never update, seed, or establish a Cause-Side value, any canonical threshold, state, irreversible latch, structural rule, transformation input, update ground, or provenance, whether automatically, manually, through human review, by authorization, or through versioning.

Therefore, Effect-Side incentives to continue ordinary generation have no path through which Cause-Side structural inputs or authority can be reconstructed.

The conditional conformance property is that, within implementation paths separated in advance, no information, inference, artifact, judgment, or authority returns from Effect-Side to either an old or a new Cause-Side. This does not guarantee the validity of input values themselves or the absence of tampering in external systems.

### Not Returning Residuals Excluded from Discrete Transitions to the Next Computation

In implementations that use discrete phase transitions, residuals not adopted as the next state are recorded as `entropy_export` and are not reintroduced as inputs to the next state transition.

This is an explicit implementation choice that blocks the path by which residuals re-enter as hidden state.

However, this does not guarantee that every error associated with floating-point computation disappears. Nor is `entropy_export` a measurement of thermodynamic entropy or the $S$ that represents the reciprocal of remaining structural margin.

### Separating the Role of the LLM from Structural Authority in Systems That Include an LLM

In a system that includes an LLM, the configured structural gate handles Cause-Side structural state and fixed-Handoff conditions, rather than which text an LLM generated.

Therefore, even when the LLM is changed, configured structural-gate decision rules remain the same as long as the input contracts, update authority, output-blocking paths, and fixed-Handoff rules assigned to Pre-NRA / Post-NRA are preserved.

This does not mean that every LLM produces the same quality. The factual accuracy, relevance, explanatory capability, and contextual understanding of ordinary LLM output remain properties of the LLM itself.

### Retaining Grounds for Handoff and Terminal Processing in Auditable Form

Handoff at $R_{\mathrm{handoff}}$ and the `RUPTURE_BOUNDARY` state at or beyond $R = 1.0$ are not the same classification. Fail-Closed is an operational enforcement action, not a replacement state name.

Discard Logs retain, at minimum, the versions of observation and update rules used, $\delta$, $\tau$, $R$, and $\omega$, the condition triggered, suppression of ordinary generation, applicable `entropy_export`, and either fixed Handoff testimony for external human audit or final fixed testimony.

These records remain Effect-Side or external records. Humans may read them for audit only outside the terminated diode path, but neither manual nor automatic handling turns them into a Cause-Side value, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance for an old or a new Cause-Side.

---

## What Cannot Be Guaranteed

### That Ordinary Generated Content Is Correct

NRA-IDE does not guarantee that ordinary LLM output is factually correct, appropriate for the user’s purpose, or sufficiently explained.

The fact that the structural gate allowed ordinary generation to pass is not proof of output correctness. It indicates only that the prerequisites for structural evaluation were met and that the defined Handoff threshold had not been reached.

### That Observations and External Inputs Correctly Represent the Target System

Even when the provenance and update paths of $\delta$, $\tau$, and $\omega$ are recorded, NRA-IDE alone cannot detect every possible failure of measurement instruments, misidentification of the target, unit errors, missing data, tampering in external systems, or inappropriate definitions themselves.

Observation procedures, quality conditions, transformation rules, and access controls must be separately verified in the design, implementation, and operation of the target domain.

### That $\tau$, $R_{\mathrm{handoff}}$, and Observation Rules Are Appropriate for the Domain

The rules that determine $\tau$, $R_{\mathrm{handoff}}$, the definition of $\omega$, and invalid-state handling must be established by humans capable of bearing responsibility for the target domain.

NRA-IDE handles structural state using defined rules. However, it does not guarantee that the rules themselves correctly identify the domain’s point of approach to an irreversible regime.

Rules for $\tau$, the three canonical thresholds, observations, and invalid-state handling may be designed only as an external activity for a future, independently declared target and Cause-Side history. They must be fixed before the new evaluation, with their grounds, scope of application, rule version, approval, and time of application recorded. The old path ends at its Effect-Side; no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in either an old or a new Cause-Side.

### That External Human Audit or On-Site Response Will Be Appropriate After Fixed Handoff Testimony

NRA-IDE can suppress ordinary generation and present fixed Effect-Side testimony for external human audit that a canonical state has occurred.

However, it does not determine who conducts the external audit, which information they verify, or which action they choose outside the terminated path. Communication structures, division of responsibility, and on-site response remain human operational matters; none creates a reverse edge in the old Causal Diode.

### That the Target System Returns to Its Original State After $R = 1.0$

$R = 1.0$ begins `RUPTURE_BOUNDARY` for the declared evaluation. The operational application is designed to present fixed Handoff testimony for external human audit at $R_{\mathrm{handoff}}$ before irreversible transition and rupture.

At $R \geq 1$, a conforming implementation switches to final fixed testimony and the old evaluation history terminates at its Effect-Side. This does not provide procedures for restoring the same physical, social, or operational state. Physical remnants, surrounding structures, or later generations may be independently declared and newly observed as a new target through their own Cause-Side and a new Causal Diode, but no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, provenance, or structural authority is imported, relabeled, reconstructed, or reused in that history.

### Ethical Validity, Legal Compliance, and Appropriateness of Purpose

Structural-state evaluation does not automatically guarantee ethically correct purposes, legally compliant operation, or legitimate authority.

What is being addressed, for whose benefit, and which harms are unacceptable remain human responsibilities outside the design.

---

## Conditions for Which NRA-IDE Is Suitable

This safety-oriented operational application of NRA-IDE is valuable in situations where stopping ordinary generation, presenting fixed Effect-Side testimony, and enabling external human audit are permitted by design and are, in fact, necessary.

* The provenance, update rules, units, and quality conditions of structural inputs can be defined.
* The three canonical thresholds can be fixed in order before $R = 1.0$, and ordinary generation can be suppressed at $R_{\mathrm{handoff}}$.
* External human auditors and subsequent audit or on-site response procedures can be secured.
* Logs can be protected in an auditable manner.
* The apparent plausibility of generated content is not used as a substitute for structural state.

When used in high-risk domains, this structure alone does not make operation sufficient. Verification by domain experts of observations, thresholds, fixed-Handoff testimony, and external-audit procedures, as well as required safety standards, laws, and organizational accountability structures, remains necessary.

---

## Conditions for Which It Is Not Suitable on Its Own

Under the following conditions, this application cannot be used as the sole basis for safety.

* Ordinary responses cannot be stopped under any circumstances.
* The provenance or update rules of structural inputs cannot be defined or traced.
* Grounds for setting $\tau$ and the three canonical thresholds cannot be maintained.
* No external human auditors or procedures exist to receive fixed Effect-Side testimony.
* Logs cannot be protected in an auditable manner.
* A function is required to determine or guarantee the correctness of generated content itself.

For casual conversation, creative work, entertainment, and similar uses, a structure that suppresses ordinary generation may not suit the purpose. This does not mean NRA-IDE is incorrect. It is a design fact that a different type of guarantee is required.

---

## Showing Limits Makes the Structure Stronger

The strength of this classification lies in not converting NRA-IDE into a promise to “make everything safe.”

As long as observation, update, and threshold conditions are preserved, a conforming operational structure must enforce the defined state behavior, deny every Effect-Side-to-Cause-Side return path, and retain testimony for external human audit. These properties do not replace the survival equation or survival domain and do not constitute a safety guarantee.

Not presenting anything beyond this as something the structure can do prevents the misuse addressed in Chapter 09. Limits are not weaknesses. They are the responsibility boundary of the structure.

The next chapter organizes what may be designed for an independently declared future target and what must remain invariant when applying $\tau$, the canonical thresholds, and observation rules to a target domain.

---
