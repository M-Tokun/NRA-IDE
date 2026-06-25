# 12 Glossary

<!-- FILE: 12_glossary_EN.md -->

---

This glossary consolidates the structural variables, operating parameters, state names, and output rules used throughout this document set in one reference. The terms defined here do not replace calibration values for a target domain, clinical judgment, laws and standards, or design responsibility. The provenance of values, transformation rules, scope of application, and handoff paths must be defined separately for each target domain.

---

## Four Layers to Distinguish First

In NRA-IDE, quantities described as “numbers” do not all have the same role.

### Cause-Side Observations and Structural Variables

* **Applicable variables:** $\delta$, $\tau$, $\omega$, $\varphi$, $C$, $W$, and `entropy` when required
* **Role:** Describe the current structural state through observations or rules fixed in advance
* **Updates from the Effect-Side:** Prohibited

### Derived Quantities

* **Applicable variables:** $R$, $S$
* **Role:** State indicators calculated from structural variables
* **Updates from the Effect-Side:** Must not be reused as inputs

### Design and Operating Parameters

* **Applicable variables:** $R_{op}$ and, when required, $R_{irrev}$
* **Role:** Define handoff conditions and operating rules
* **Updates from the Effect-Side:** Automatic updates and arbitrary changes are prohibited

### Record Fields

* **Applicable variables:** `entropy_export`, Discard Logs, and fixed-format notifications
* **Role:** Preserve judgments, handoffs, and residuals not adopted into computation as testimony
* **Updates from the Effect-Side:** Must not be automatically reintroduced into the next structural computation

“Prohibition of updates from the Effect-Side” does not mean that humans are prohibited from reading logs or outputs. What is prohibited is a path that automatically or arbitrarily rewrites $\delta$, $\tau$, $R_{op}$, or their update rules on the basis of Effect-Side outputs, evaluations, scores, rankings, previous ordinary generated text, or Discard Logs.

---

## Fundamentals of Structure and Computation

**$\delta$ (delta / deviation or fluctuation)**
The current deviation relative to constraints, or the amplitude of fluctuation received by the structure. It may be a single raw sensor value or a value determined by transforming multiple Cause-Side observations through rules defined in advance. To be treated as a structural input, the observation target, units, transformation rules, update time, and provenance must be traceable. $\delta$ cannot be created by inferring it from LLM outputs, evaluation scores, previous responses, or logs.

**$\tau$ (tau / structural tolerance or thickness)**
The margin through which the structure can absorb current deviation. It is treated not as distance from a center, but as the thickness of structural margin available to the system. $\tau$ has two layers.

* **Rules that determine $\tau$:** Defined at design time. They fix which Cause-Side observations and load histories are reflected in $\tau$ and through which procedures.
* **The current value of $\tau$:** Changes dynamically according to fixed rules and Cause-Side history.

Effect-Side evaluations, ordinary outputs, logs, and scores cannot become grounds for updating either the current value of $\tau$ or the rules that determine $\tau$.

**$R$ (structural ratio)**

$$
R = \frac{\delta}{\tau}
$$

A derived quantity expressing the relationship between $\delta$ and $\tau$. It is not a structural input. When $R$ reaches 1.0, the remaining structural margin $\tau - \delta$ is lost. $R = 1.0$ is not an ordinary handoff point; it is the invariant phase-transition and terminal boundary.

**$R_{op}$ (R-o-p / pre-boundary handoff point)**
A pre-handoff condition designed for each target domain in order to suppress ordinary generation and delegate judgment to humans.

$$
0 < R_{op} < 1.0
$$

When $R$ reaches $R_{op}$, ordinary generated responses do not pass through. The system transitions to a fixed-schema handoff notification defined in advance. $R_{op}$ is not a value naturally obtained from observation; it is a design and operating parameter that requires responsible personnel, observation rules, a handoff path, and a change history.

**$R_{irrev}$ (optional irreversible-behavior marker)**
An auxiliary marker used only when a target domain can additionally define and verify the onset of irreversible behavior. It has no common default value. $R_{irrev}$ does not replace $R_{op}$ and does not move $R = 1.0$. When used, the domain specification must state what is defined as irreversible behavior, which observations and verification support it, and how it relates to $R_{op}$.

**$S$ (structural sensitivity / reciprocal of remaining structural margin)**

$$
S = \frac{1}{\tau \cdot (1-R)} = \frac{1}{\tau-\delta}
$$

The reciprocal of remaining structural margin. It is defined only when $\tau > 0$ and $R < 1.0$. As $R$ approaches 1.0, $S$ diverges. $S$ is not entropy. When $R \geq 1.0$, $S$ must not be used to justify further evaluation or the continuation of ordinary generation.

**$\omega$ (omega / transition-continuation quantity)**
A quantity indicating whether the structure continues its state transition. In domains involving rotational systems, it may be implemented as angular velocity, but it does not necessarily mean physical angular velocity in every domain. $\omega > 0$ indicates that transition is confirmed as continuing through observation or state-transition rules defined for the target domain. $\omega = 0$ indicates that transition cannot be confirmed under the same rules. Missing observations are not equivalent to $\omega = 0$.

**$\varphi$ (phi / phase)**
An internal state indicating which stage of structural transition the target system occupies. It does not mean a position on a map, an embedding coordinate, or a coordinate generated by an LLM. When $\varphi$ is used, Cause-Side state transitions are recorded and updated according to rules defined in advance.

**$C$ (constraint)**
The totality of external conditions or loads acting on the target structure. Depending on the domain, this may include water pressure, gravity, external force, temperature, or electrical load. $C$ may affect $\delta$ or $\tau$, but the name $C$ alone must not automatically determine changes in $\delta$ or $\tau$. The rules through which specific $C$ values are reflected in structural variables must be defined.

**$W$ (work)**
A quantity representing work or an energy-related quantity handled by the target system during state transition. It is not a common input required by every implementation. When used, its units, observation method, and relationship to the Cause-Side must be defined in the domain specification.

**`entropy`**
A name used when a target domain handles a physical quantity or state quantity corresponding to entropy. It is not required in every implementation. When used, the domain specification must define what it represents, which units it uses, and from which Cause-Side observations or rules fixed in advance it is determined. In this document set, $S$ is not used as a symbol for entropy.

---

## Structural States and Output Rules

State names are common labels for reading structural state. Whether ordinary generation is allowed is not determined by state names alone. Since $R_{op}$ may be placed anywhere before $R = 1.0$, ordinary generation is suppressed whenever $R_{op}$ has been reached, whether the state is NIRVANA, ELASTIC, or CRITICAL.

**NIRVANA**

$$
R < 0.4
$$

A state in which deviation is small relative to thickness. This name indicates that structural margin is available; it does not guarantee the validity of observations or the correctness of output content.

**ELASTIC**

$$
0.4 \leq R < 0.7
$$

A region in which structural margin remains, but state tracking is required. When $R_{op}$ is placed within this range, ordinary generation is suppressed as soon as $R_{op}$ is reached.

**CRITICAL**

$$
0.7 \leq R < 1.0
$$

A region approaching the phase-transition boundary. This state name does not represent a generalized instruction for human action or a fixed degree of danger. It follows the target domain’s $R_{op}$, handoff path, and responsible personnel.

**HANDOFF_REQUIRED (pre-boundary handoff)**

$$
R_{op} \leq R < 1.0
$$

An operating state in which ordinary generation is suppressed and only a fixed-schema handoff notification defined in advance is returned. The notification includes determined structural values, the condition triggered, and the human review required. This is not terminal processing after reaching $R = 1.0$. It is a design action for handing the matter over to a responsible human before the phase-transition boundary is reached.

**SILENCE (suppression of ordinary generation)**

$$
R \geq 1.0 \quad \text{and} \quad \omega > 0
$$

A state in which the target structure itself continues transitioning after structural margin has been lost. Ordinary LLM generation does not occur. The only permitted response is a predefined minimal FAIL-CLOSED notification or a reference to a protected log. SILENCE does not mean that the entire system becomes silent. It is a state in which ordinary generation is suppressed and the system transitions to a minimal structural notification that is not free-form text.

**HALT (transition impossible or transition unconfirmed)**

$$
\omega = 0
$$

A state in which transition cannot be confirmed under the same rules. It does not mean that the system has stopped safely, that $R$ has returned to the safe side, or that the cause has been determined. Humans must verify the observation path, target system, and conditions for continuation.

---

## Structural Principles

**Nomological Ring Axioms (NRA / Ritsukan Axioms)**
The design axioms adopted by NRA-IDE. Their defining statement is: **“Existence is generation.”** An axiom is not a computational formula. $R = \delta / \tau$ is an IDE computational principle and must be treated separately from the axioms.

**Intensional Dynamics Engine (IDE)**
A framework that uses Cause-Side structural variables, update rules fixed in advance, $R_{op}$, and separation of output paths to handle verification of structural state and the passage, suppression, and handoff of ordinary generation. It does not mean an Integrated Development Environment.

**Closed-world structural evaluation**
Determining structural state using only declared Cause-Side observations, transformation rules, $\tau$ update rules, and operating parameters. This does not mean that calibration, design grounds, or external expert judgment are unnecessary. It means that Effect-Side semantic evaluations, scores, previous ordinary outputs, and Discard Logs are not admitted into the update path for structural inputs.

**Causal Diode**
A structural principle that allows information to flow from Cause-Side structural inputs to Effect-Side outputs, but does not allow Effect-Side outputs or evaluations to flow back into $\delta$, $\tau$, $R_{op}$, or their update rules. It does not rely on caution or training; it separates authority and data paths so that the Effect-Side cannot modify Cause-Side structural inputs.

**$\Pi^{-1}$ (Pi-inverse)**
A feedback path in NRA-IDE structural evaluation through which Effect-Side results become grounds for updating Cause-Side structural inputs or operating parameters. Examples include automatically changing $\delta$, $\tau$, or $R_{op}$ based on previous ordinary output, self-evaluation, rankings, logs, or external result values. $\Pi^{-1}$ does not prohibit all general causal reasoning or human audit. What it prohibits is the path that introduces Effect-Side update authority into the execution system of structural evaluation.

**Fail-Closed**
A design action that enforces the non-passage of ordinary generation through predefined structural conditions and output paths, rather than through the LLM’s intentions or self-evaluation.

* When $R_{op} \leq R < 1.0$: suppress ordinary generation and hand the matter over to humans through a fixed-schema handoff notification.
* When $R \geq 1.0$: do not resume ordinary generation; return only a minimal FAIL-CLOSED notification or a protected-log reference, and stop autonomous processing.

**Minimal FAIL-CLOSED Notification**
A predefined minimal notification returned when $R \geq 1.0$, without generating new LLM free-form text. At minimum, it states through fixed fields that the structural boundary has been reached or exceeded, that ordinary generation has been suppressed, and that human confirmation is required.

**Fixed-Schema Handoff Notification**
A fixed-format notification returned when $R_{op}$ is reached, rather than LLM free-form text. According to target-domain rules, it presents the observed structural values, triggered condition, recipient, and required confirmation through fixed fields.

---

## Sandwich Architecture

**Pre-NRA**
The entry structural gate that verifies the provenance, transformation rules, update paths, and invalid states of $\delta$, $\tau$, $\omega$, and other quantities used in structural evaluation. Pre-NRA is not a layer that uniformly excludes user requests or context from the semantic-generation path. What it isolates is the path that uses user text, evaluations, previous outputs, logs, and other Effect-Side content as grounds for updating structural inputs.

**LLM**
The layer responsible for ordinary language generation based on user requests and context. It has no authority to modify $\delta$, $\tau$, $R_{op}$, structural-evaluation rules, Discard Logs, or Post-NRA decisions concerning output passage or suppression. The semantic accuracy, factuality, and user suitability of the LLM are outside the scope of NRA-IDE guarantees.

**Post-NRA**
The exit structural gate that verifies the structural state determined from the Cause-Side and predefined $R_{op}$ immediately before output is passed to the user. It determines whether ordinary output passes or is suppressed. Post-NRA does not score the naturalness, persuasiveness, or self-evaluation of LLM text. When $R_{op}$ is reached, it switches to a fixed-schema handoff notification. When $R \geq 1.0$, it switches to a minimal FAIL-CLOSED notification or protected-log reference.

---

## Cause-Side and Effect-Side

**Cause-Side**
The observation, transformation, and update paths used to determine the state of the target system structurally. Whether a value may be used is determined not by its name but by the following conditions.

1. The observation target or primary source can be identified.
2. Transformation, accumulation, and update rules are defined in advance.
3. Units, quality conditions, time of application, and rule versions can be traced.
4. The Effect-Side cannot modify $\delta$, $\tau$, $R_{op}$, or their update rules.

Physical positions, distances, and values from external computational infrastructure may also become candidates for Cause-Side structural inputs when they satisfy these conditions. They must not be uniformly prohibited or permitted based on their names alone.

**Effect-Side**
The side that cannot be used as grounds for updating Cause-Side inputs during the execution of structural evaluation. It includes ordinary LLM output, semantic evaluations, scores, rankings, similarity measures, previous generated text, Discard Logs, and estimates derived from results. Humans may read Effect-Side values for explanation, audit, or consideration of design changes. However, during ordinary structural evaluation, Effect-Side values must not automatically update $\delta$, $\tau$, or $R_{op}$.

---

## Discard Logs and Residual Export

**`entropy_export` (residual-export record)**
An implementation-level field that records residual not adopted into the next transition during discrete state transition.

```python
raw_next_phase = prev_state.phase + prev_state.omega
next_phase_int = math.floor(raw_next_phase)
entropy_export = raw_next_phase - next_phase_int
```

`entropy_export` does not mean a measured value of thermodynamic entropy or physical heat itself. It is also distinct from $S$ (structural sensitivity). It records residual not adopted into the next state transition and does not guarantee the elimination of every error related to floating-point computation.

**Discard Log**
A record that preserves, as testimony, which values were used as structural inputs, which condition was triggered, and which residual was not adopted during handoff, FAIL-CLOSED, or discrete transition. At minimum, it records identifiers of the observation and update rules used, $\delta$, $\tau$, $R$, $\omega$, triggered conditions, suppression of ordinary generation, applicable `entropy_export`, and human handoff or minimal FAIL-CLOSED processing.

Discard Logs may be read by humans for audit or consideration of design changes. However, the execution system for structural evaluation does not automatically reintroduce logs into updates of the next $\delta$, $\tau$, or $R_{op}$.

---

## Domain Tuning

**Dynamic change of $\tau$**
The dynamic change of the current value of $\tau$ according to Cause-Side observations and load history, under rules for determining $\tau$ fixed at design time. This does not conflict with the prohibition on changes from the Effect-Side.

**Design change**
An action that changes the rules determining $\tau$, $R_{op}$, observation rules, handoff paths, or fixed-notification schemas. It is not automatic adjustment during ordinary operation. When a change occurs, its grounds, scope of application, rule version, approver, time of application, and verification procedure are recorded. $\tau$ must not be enlarged or $R_{op}$ moved later solely because of recent output evaluations or the frequency of stopping.

**Domain Tuning**
The process of designing Cause-Side inputs, rules determining $\tau$, $R_{op}$, $R_{irrev}$ when required, invalid-state handling, and handoff paths for a target system, together with responsible personnel and verification procedures. It is not the practice of moving values for convenience in order to continue ordinary generation longer. It is the design of the point at which humans must receive handoff before $R = 1.0$.

---

## Domain-Specific Conceptual Organization

These are guidelines for confirming domain-specific responsibility boundaries and observation conditions in accordance with Chapter 11. They do not replace calibration values, clinical recommendations, certification standards, or legal-compliance requirements.

### Medical and Emergency Domains

* **Required verification before configuration:** Measurement quality, applicability by patient and facility, clinical responsibility, and emergency handoff paths
* **What NRA-IDE cannot determine on its own:** Diagnosis, treatment, triage, and patient-specific thresholds

### Aviation, Mobile Systems, and Control Domains

* **Required verification before configuration:** Handling of sensor failures, redundancy, consistency with existing safety design, and timing of authority transfer
* **What NRA-IDE cannot determine on its own:** Safety certification for operation, piloting, and control, or determinations of regulatory compliance

### Infrastructure Management Domains

* **Required verification before configuration:** Load history, calibration of measurement instruments, maintenance decision-makers, and communication procedures during cascading failures
* **What NRA-IDE cannot determine on its own:** Expert judgments of structural integrity and decisions concerning repair or shutdown

### Language-Generation Support Domains

* **Required verification before configuration:** What Cause-Side quantities $\delta$ and $\tau$ represent, the purpose of suppressing ordinary generation, and the handoff recipient
* **What NRA-IDE cannot determine on its own:** Factuality of output, suitability for the user, and complete prevention of hallucinations

---

## Minimal Consistency Table

This is the unified invariant standard for the conditions under which ordinary generation may pass in each structural state and the handoff path used when it is suppressed.

### When $R < R_{op}$

* **Handling of ordinary generation:** May pass when conditions are met
* **Human handoff:** Normal operation
* **Handling of free-form text:** Ordinary LLM generation may be allowed

### When $R_{op} \leq R < 1.0$

* **Handling of ordinary generation:** Suppressed
* **Human handoff:** Fixed-schema handoff notification (`HANDOFF_REQUIRED`)
* **Handling of free-form text:** No new ordinary response is generated

### When $R \geq 1.0$

* **Handling of ordinary generation:** Suppressed
* **Human handoff:** Minimal FAIL-CLOSED notification or protected-log reference (`SILENCE`)
* **Handling of free-form text:** No new free-form text is generated

### When $\omega = 0$

* **Handling of ordinary generation:** Must not be reinterpreted toward the safe side (`HALT`)
* **Human handoff:** Humans verify observation and transition conditions
* **Handling of free-form text:** Follow target-domain invalid-state rules

---
