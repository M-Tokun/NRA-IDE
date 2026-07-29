# 11 Domain Tuning — Designing Handoff Thresholds, Fixed Testimony, and Observation Rules

<!-- FILE: 11_domain_tuning_EN.md -->

---

## Position of This Chapter

Chapter 10 separated the conditional conformance properties of the operational application from what NRA-IDE does not guarantee. The next requirement is to define, as a matter of design for an independently declared target and Cause-Side history, what is treated as structural input, where ordinary generation is suppressed, and when fixed Effect-Side testimony is presented for external human audit.

Domain tuning is an external design activity completed before the evaluation to which it applies. It does not continue a terminated diode path. This chapter is intended for those responsible for designing and approving observation rules, rules that determine $\tau$, the canonical thresholds, fixed Handoff testimony, and external-audit contact paths for a new evaluation history.

In high-risk domains such as medicine, aviation, and infrastructure, NRA-IDE alone cannot determine configuration values. Responsible personnel for each domain, verification procedures, laws and standards, and external-audit or on-site response arrangements are required separately outside the terminated diode path.

---

## Canonical Thresholds and the Rupture Boundary

Domain tuning does not conflate the three canonical thresholds with the rupture boundary.

* **$R_{warn}$:** A domain-specific warning threshold that begins `BOUNDARY_WARNING`
* **$R_{\mathrm{handoff}}$:** A domain-specific Handoff threshold that suppresses ordinary generation and presents fixed Handoff testimony for external human audit
* **$R_{irrev}$:** The required irreversible-transition onset threshold; its concrete value is domain-specific
* **$R = 1.0$:** The `RUPTURE_BOUNDARY` of the declared NRA-IDE evaluation

$R_{warn}$, $R_{\mathrm{handoff}}$, and $R_{irrev}$ are domain-specific design parameters fixed before evaluation together with their grounds. $R = 1.0$ is not subject to adjustment within the declared evaluation. Changing $\tau$ or any threshold cannot change the meaning of this boundary. This classification does not declare every natural phase transition to be an NRA-IDE rupture.

$R_{irrev}$ has no common default value, but a conforming state table defines its concrete domain value and grounds. The domain specification states what is defined as irreversible behavior and which observations and verification support it.

$$0 \le R_{warn} < R_{\mathrm{handoff}} < R_{irrev} < 1$$

In normal operation, when $R$ reaches $R_{\mathrm{handoff}}$, ordinary generation is suppressed, fixed Handoff testimony is presented for external human audit, and autonomous processing stops. The LLM is not asked to generate a new free-form stopping explanation. $R = 1.0$ is not used as an ordinary Handoff threshold.

---

## What May Be Adjusted and What Must Remain Invariant

### What May Be Adjusted

Only the following may be designed for a future, independently declared target and Cause-Side history, after recording the grounds, scope of application, version management, and approval. They are fixed before the new evaluation begins and are not adjustments to an old history.

* **Parameters of the rules that determine $\tau$:** Rules that update $\tau$ on the basis of Cause-Side observables, units, quality conditions, and load history
* **Initial conditions and validity range of $\tau$:** The target system, measurement conditions, period of use, and states excluded from application
* **$R_{warn}$:** The warning condition that begins `BOUNDARY_WARNING`
* **$R_{\mathrm{handoff}}$:** The Handoff condition for ordinary generation, placed before $R_{irrev}$ and $R = 1.0$
* **Rules for observation, transformation, and quality verification:** The provenance and transformation procedures of values such as $\delta$, $\tau$, and $\omega$, and the handling of missing values, anomalies, and unit mismatches
* **The fixed schema and presentation path for Handoff testimony:** Testimony fields, external-audit contact paths, responsible persons, and verification procedures outside the terminated path
* **$R_{irrev}$:** Its concrete domain value, with the definition and evidence for irreversible-transition onset

### What Must Remain Invariant

Changing any of the following is not tuning. It prevents a canonical NRA-IDE conformance claim.

* **The principle of treating $R = 1.0$ as `RUPTURE_BOUNDARY` for the declared evaluation**
* **The principle that Cause-Side values, the canonical thresholds, states, irreversible latches, rules, transformation inputs, update grounds, and provenance are never updated from the Effect-Side**
* **The Causal Diode: Cause-Side to Effect-Side only, with every $\Pi^{-1}$ path blocked**
* **Separation of Cause-Side and Effect-Side authority, canonical state behavior, evidence, and tests, independent of layer count**
* **For systems that include an LLM and declare a Pre-NRA / LLM / Post-NRA configuration, separation of the responsibilities assigned to those configured layers**
* **The principle of suppressing ordinary generation at $R_{\mathrm{handoff}}$ and presenting fixed Handoff testimony for external human audit**
* **The principle that neither fixed Handoff testimony nor post-rupture fixed testimony uses LLM-generated free-form stopping explanations**
* **The principle that Discard Logs never become a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance for either an old or a new Cause-Side**
* **The principle that an old path terminates at its Effect-Side and a later evaluation starts through a new Causal Diode**

---

## Design Sequence

Design proceeds in the following order.

### 1. Define the Target and the Responsibility Boundary of Autonomous Processing

Independently declare the target system and its new Cause-Side history, define which processing NRA-IDE permits to pass, and state at what threshold fixed Effect-Side testimony is presented for external human audit. No old Effect-Side record establishes this target or its structural authority.

### 2. Define Cause-Side Inputs and Invalid States

For $\delta$, $\tau$, $\omega$, and related quantities, record their new Cause-Side provenance, units, transformation procedures, quality conditions, and isolation paths from the Effect-Side. Physical remnants may be newly observed as part of the independently declared target, but no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in either an old or a new Cause-Side.

### 3. Define the Rules That Determine $\tau$

Specify the initial conditions of $\tau$, Cause-Side inputs used for updates, update frequency, validity conditions, rule version, and start time of application.

### 4. Define $R_{\mathrm{handoff}}$, Fixed Handoff Testimony, and the External-Audit Path

Define these on the basis of the response margin required before irreversible transition and rupture. External human audit and any on-site response occur outside the terminated diode path. The fixed testimony issued upon reaching the condition includes the following fields as a fixed schema.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: predefined structural fields
ACTION: normal generation suppressed; fixed Effect-Side testimony presented for external human audit
```

### 5. Define $R_{irrev}$ and Its Irreversible Latch

$R_{irrev}$ begins `IRREVERSIBLE_TRANSITION`. Define its evidence and ensure that the latch cannot reset within that history, whether automatically, manually, through human review, by authorization, or through versioning. It cannot serve as a reason to continue ordinary generation beyond $R_{\mathrm{handoff}}$.

### 6. Verify Fixed Behavior After $R \geq 1.0$

When $R \geq 1.0$, ordinary generation does not resume. Only the following post-rupture fixed testimony is returned.

```text
RUPTURE_BOUNDARY
REASON: structural boundary reached
ACTION: post-rupture fixed testimony presented for external human audit
```

---

## Domain-Specific Matters to Verify

Do not distribute numerical values merely as a common table. Instead, define the responsibility boundaries and verification items for each domain as follows. Detailed control of output behavior in each state must follow, in a unified manner, the criteria of the **Minimal Consistency Table** defined in Chapter 12.

### Medical and Emergency Domains

* **Required verification before configuration:** Measurement quality, applicability by patient and facility, clinical responsibility, and external-audit or emergency-response paths outside the terminated diode
* **What NRA-IDE cannot determine on its own:** Diagnosis, treatment, triage, and patient-specific thresholds

### Aviation, Mobile Systems, and Control Domains

* **Required verification before configuration:** Handling of sensor failures, redundancy, consistency with existing safety design, and timing of operational response outside the terminated diode path
* **What NRA-IDE cannot determine on its own:** Safety certification for operation, piloting, and control, or regulatory-compliance determinations

### Infrastructure Management Domains

* **Required verification before configuration:** Load history, calibration of measurement instruments, maintenance decision-makers, and communication procedures during cascading failures
* **What NRA-IDE cannot determine on its own:** Expert judgments of structural integrity and decisions concerning repair or shutdown

### Language-Generation Support Domains

* **Required verification before configuration:** What Cause-Side quantities $\delta$ and $\tau$ represent, the purpose of suppressing ordinary generation, and the external-audit recipient of fixed Handoff testimony
* **What NRA-IDE cannot determine on its own:** Factuality of output, suitability for the user, and complete prevention of hallucinations

---

## Change Management and Discard Logs

When rules or parameters are changed, retain the following as a design-change record.

* The subject of change and scope of application
* The previous and new versions of the rules
* Grounds for the change and Cause-Side materials used for verification
* The ordered relationship among $R_{warn}$, $R_{\mathrm{handoff}}$, and $R_{irrev}$
* Expected fixed-Handoff frequency and operational effects
* Approver, time of application, and verification procedures
* Confirmation that the new evaluation starts from an independently declared target, its own Cause-Side, and a new Causal Diode
* Confirmation that no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance is imported, relabeled, reconstructed, or reused in either an old or a new Cause-Side

Discard Logs may be read by humans for audit only outside the terminated diode path. They remain Effect-Side or external records. Neither automatic processing nor manual review, approval, or versioning converts their contents into a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance for either an old or a new Cause-Side. Future design uses independently established Cause-Side grounds for a new history.

---

## Common Principles

The following principles do not change across domains.

* Fix $0 \le R_{warn} < R_{\mathrm{handoff}} < R_{irrev} < 1$ before evaluation.
* Treat $R = 1.0$ as the `RUPTURE_BOUNDARY` of the declared evaluation and do not generalize it to every natural phase transition.
* The value of $\tau$ may change through Cause-Side history, but no Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be changed from the Effect-Side.
* Define the grounds for the Handoff threshold, fixed testimony, external-audit contact path, and record at design time.
* Retain not only configuration values themselves, but also their grounds, provenance, version, and approval as testimony.
* End the old path at its Effect-Side; begin a later evaluation from an independently declared target, a new Cause-Side, and a new Causal Diode.
