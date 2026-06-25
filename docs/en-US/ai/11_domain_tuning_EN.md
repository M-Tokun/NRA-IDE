# 11 Domain Tuning — Designing Handoff Points and Observation Rules

<!-- FILE: 11_domain_tuning_EN.md -->

---

## Position of This Chapter

Chapter 10 separated what NRA-IDE can guarantee from the prerequisites under which those guarantees hold. The next requirement is to define, as a matter of design for the target domain, what is treated as structural input, where ordinary generation is suppressed, and when judgment is handed over to humans.

This chapter is not a guide to initial configuration. It is intended for those responsible for designing, approving, and managing changes to observation rules, rules that determine $\tau$, $R_{op}$, and handoff paths.

In high-risk domains such as medicine, aviation, and infrastructure, NRA-IDE alone cannot determine configuration values. Responsible personnel for each domain, verification procedures, laws and standards, and on-site handoff arrangements are required separately.

---

## Three Boundaries That Must First Be Distinguished

Domain tuning does not conflate the following three.

* **$R_{op}$:** A domain-specific pre-handoff point that suppresses ordinary generation and delegates judgment to humans
* **$R = 1.0$:** The invariant phase-transition and terminal boundary at which structural margin is lost
* **$R_{irrev}$:** An auxiliary marker concerning the onset of irreversible behavior, which may be defined only by domains that require it

$R_{op}$ is an operational handoff condition. It is defined at design time together with its grounds. $R = 1.0$ is not subject to adjustment. Changing $\tau$ or $R_{op}$ cannot change the meaning of this boundary.

$R_{irrev}$ has no common default value. When used, the domain specification must state what is defined as irreversible behavior, which observations and verification support it, and how it relates to $R_{op}$. Even when $R_{irrev}$ is undefined, pre-handoff through $R_{op}$ remains necessary.

$$0 < R_{op} < 1.0$$

In normal operation, when $R$ reaches $R_{op}$, ordinary generation is suppressed, a fixed-format handoff notification is returned, and autonomous processing stops. $R = 1.0$ is not used as an ordinary handoff point.

---

## What May Be Adjusted and What Must Remain Invariant

### What May Be Adjusted

Only the following may be adjusted by those responsible for the target domain, after recording the grounds, scope of application, version management, and approval.

* **Parameters of the rules that determine $\tau$:** Rules that update $\tau$ on the basis of Cause-Side observables, units, quality conditions, and load history
* **Initial conditions and validity range of $\tau$:** The target system, measurement conditions, period of use, and states excluded from application
* **$R_{op}$:** The pre-handoff condition for ordinary generation, placed before $R = 1.0$
* **Rules for observation, transformation, and quality verification:** The provenance and transformation procedures of values such as $\delta$, $\tau$, and $\omega$, and the handling of missing values, anomalies, and unit mismatches
* **The fixed schema and recipient of handoff notifications:** Notification fields, contact paths, responsible persons, and verification procedures
* **$R_{irrev}$:** Only when an additional auxiliary marker is required, and only after its definition and relation to other conditions have been made explicit

### What Must Remain Invariant

Changing any of the following is not tuning. It is a change that removes NRA-IDE’s structural guarantees.

* **The principle of treating $R = 1.0$ as the terminal boundary**
* **The principle that $\delta$, $\tau$, and $R_{op}$ are not updated from the Effect-Side**
* **The Causal Diode: blocking $\Pi^{-1}$**
* **Separation of responsibilities among Pre-NRA / LLM / Post-NRA**
* **The principle of suppressing ordinary generation at $R_{op}$ and delegating to humans**
* **The principle that, at $R \geq 1.0$, no free-form text is generated and only a minimal FAIL-CLOSED notification is returned**
* **The principle that Discard Logs are not automatically returned to the next structural computation**

---

## Design Sequence

Design proceeds in the following order.

### 1. Define the Target and the Responsibility Boundary of Autonomous Processing

Define what constitutes the target system, which processing NRA-IDE permits to pass, and at what point the matter is handed over to humans.

### 2. Define Cause-Side Inputs and Invalid States

For $\delta$, $\tau$, $\omega$, and related quantities, record their provenance, units, transformation procedures, quality conditions, and isolation paths from the Effect-Side.

### 3. Define the Rules That Determine $\tau$

Specify the initial conditions of $\tau$, Cause-Side inputs used for updates, update frequency, validity conditions, rule version, and start time of application.

### 4. Define $R_{op}$ and the Handoff Path

Define these on the basis of the response margin required for humans to verify the state and assume responsibility for judgment. The fixed notification issued upon reaching the condition includes the following fields as a fixed schema.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: predefined structural fields
ACTION: normal generation suppressed; human review required
```

### 5. Define $R_{irrev}$ Only When Necessary

$R_{irrev}$ is an auxiliary marker. It cannot serve as a reason to continue ordinary generation beyond $R_{op}$.

### 6. Verify Fixed Behavior After $R \geq 1.0$

When $R \geq 1.0$, ordinary generation does not resume. Only the following minimal FAIL-CLOSED notification is returned.

```text
FAIL_CLOSED
REASON: structural boundary reached
ACTION: no further generated response; human handoff required
```

---

## Domain-Specific Matters to Verify

Do not distribute numerical values merely as a common table. Instead, define the responsibility boundaries and verification items for each domain as follows. Detailed control of output behavior in each state must follow, in a unified manner, the criteria of the **Minimal Consistency Table** defined in Chapter 12.

### Medical and Emergency Domains

* **Required verification before configuration:** Measurement quality, applicability by patient and facility, clinical responsibility, and emergency handoff paths
* **What NRA-IDE cannot determine on its own:** Diagnosis, treatment, triage, and patient-specific thresholds

### Aviation, Mobile Systems, and Control Domains

* **Required verification before configuration:** Handling of sensor failures, redundancy, consistency with existing safety design, and timing of authority transfer
* **What NRA-IDE cannot determine on its own:** Safety certification for operation, piloting, and control, or regulatory-compliance determinations

### Infrastructure Management Domains

* **Required verification before configuration:** Load history, calibration of measurement instruments, maintenance decision-makers, and communication procedures during cascading failures
* **What NRA-IDE cannot determine on its own:** Expert judgments of structural integrity and decisions concerning repair or shutdown

### Language-Generation Support Domains

* **Required verification before configuration:** What Cause-Side quantities $\delta$ and $\tau$ represent, the purpose of suppressing ordinary generation, and the handoff recipient
* **What NRA-IDE cannot determine on its own:** Factuality of output, suitability for the user, and complete prevention of hallucinations

---

## Change Management and Discard Logs

When rules or parameters are changed, retain the following as a design-change record.

* The subject of change and scope of application
* The previous and new versions of the rules
* Grounds for the change and Cause-Side materials used for verification
* The relationship between $R_{op}$ and $R_{irrev}$ when $R_{irrev}$ is used
* Expected handoff frequency and operational effects
* Approver, time of application, and verification procedures
* Confirmation that the change is not retroactively applied to existing logs

Even when knowledge obtained from Discard Logs is reflected in a future design change, this must not occur through automatic AI feedback. Humans must verify Cause-Side materials, the validity of the rules, and the scope of application, then proceed through approval as a new version.

---

## Common Principles

The following principles do not change across domains.

* Place $R_{op}$ before $R = 1.0$.
* Treat $R = 1.0$ as a terminal boundary that is not adjusted.
* The value of $\tau$ may change through Cause-Side history, but the rules that update it must not be changed from the Effect-Side.
* Define the grounds for handoff, notification, recipient, and record at design time.
* Retain not only configuration values themselves, but also their grounds, provenance, version, and approval as testimony.
