# 12 Glossary

<!-- FILE: 12_glossary_EN.md -->

---

This glossary consolidates the structural variables, operating parameters, state names, and output rules used throughout this document set in one reference. The terms defined here do not replace calibration values for a target domain, clinical judgment, laws and standards, or design responsibility. The provenance of values, transformation rules, scope of application, fixed Handoff testimony, and external-audit contact paths must be defined separately for each target domain.

---

## Roles to Distinguish First

In NRA-IDE, quantities described as “numbers” do not all have the same role.

### Cause-Side Observations and Structural Variables

* **Applicable variables:** $\delta$, $\tau$, $\omega$, $\varphi$, $C$, $W$, and `entropy` when required
* **Role:** Describe the current structural state through observations or rules fixed in advance
* **Updates from the Effect-Side:** Prohibited

### Primary Formula and Derived or Supporting Quantities

* **Primary Formula:** $R=\delta/\tau$ maps the declared target's structural state into the canonical mathematical relation. It is not a safety indicator, local gauge, or mere boundary-approach rate.
* **Derived or supporting quantities:** $S$, $M_R$, and $M_{\tau}$ are calculated to supplement interpretation of the Primary Formula.
* **Updates from the Effect-Side:** Prohibited; no result from either category becomes a Cause-Side input or update ground.

### Design and Operating Parameters

* **Applicable variables:** $R_{warn}$, $R_{\mathrm{handoff}}$, and $R_{irrev}$
* **Role:** Define Handoff thresholds, fixed-testimony conditions, and operating rules
* **Updates from the Effect-Side:** Prohibited, including manual, reviewed, authorized, or versioned changes based on Effect-Side material

### Record Fields

* **Applicable variables:** `entropy_export`, Discard Logs, Fixed Handoff Testimony, and Final Fixed Testimony
* **Role:** Preserve structural determinations, fixed testimony, and residuals not adopted into computation
* **Updates from the Effect-Side:** Must not become a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance in either an old or a new Cause-Side

Humans may read logs or outputs only as an activity outside the terminated diode path. Reading does not create a reverse edge and does not convert Effect-Side outputs, evaluations, scores, rankings, previous ordinary generated text, or Discard Logs into a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance in either an old or a new Cause-Side.

---

## Fundamentals of Structure and Computation

**$\delta$ (delta / accumulated deviation)**
The accumulated deviation with history for the declared target. It may be determined from a single observation stream or by transforming multiple Cause-Side observations through rules defined in advance. To be treated as a structural input, the observation target, units, accumulation and transformation rules, update time, and provenance must be traceable. $\delta$ cannot be created by inferring it from LLM outputs, evaluation scores, previous responses, or logs.

**$\tau$ (tau / absorption thickness)**
The absorption thickness through which the declared structure receives accumulated deviation. It is not a time constant, a semantic tolerance score, or distance from a center. $\tau$ has two layers.

* **Rules that determine $\tau$:** Defined at design time. They fix which Cause-Side observations and load histories are reflected in $\tau$ and through which procedures.
* **The current value of $\tau$:** Changes dynamically according to fixed rules and Cause-Side history.

Effect-Side evaluations, ordinary outputs, logs, and scores cannot become grounds for updating either the current value of $\tau$ or the rules that determine $\tau$.

**$R$ (canonical structural ratio of the Primary Formula)**

$$
R = \frac{\delta}{\tau}
$$

The canonical ratio by which the Primary Formula maps the declared target's structural state into a mathematical relation. Although its value is calculated from $\delta$ and $\tau$, the Primary Formula is not classified as a derived, auxiliary, or supporting formula. $R$ is not a raw structural input, safety indicator, local gauge, or mere boundary-approach rate. For a declared NRA-IDE evaluation, $R=1$ begins `RUPTURE_BOUNDARY`; this does not declare every natural phase transition to be an NRA-IDE rupture.

**$R_{\mathrm{handoff}}$ (pre-boundary Handoff threshold)**
A Handoff condition designed for each target domain in order to suppress ordinary generation and present fixed Handoff testimony for external human audit.

$$
0 \leq R_{warn} < R_{\mathrm{handoff}} < R_{irrev} < 1
$$

When $R$ reaches $R_{\mathrm{handoff}}$, ordinary generated responses do not pass through. The system presents predefined fixed Handoff testimony for external human audit and does not ask the LLM to generate a new free-form stopping explanation. $R_{\mathrm{handoff}}$ is not a value naturally obtained from observation; it is a design and operating parameter that requires responsible personnel, observation rules, an external-audit contact path, and a change history.

**$R_{irrev}$ (irreversible-transition onset threshold)**
The canonical threshold at which `IRREVERSIBLE_TRANSITION` begins and is latched. Its concrete value is domain-specific, but it must satisfy $R_{\mathrm{handoff}} < R_{irrev} < 1$. It does not replace $R_{\mathrm{handoff}}$ and does not move $R=1$.

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

The canonical states are determined by the invariant threshold order and invalid-input rules. Legacy labels such as NIRVANA, ELASTIC, CRITICAL, SILENCE, and HALT are not canonical states.

**`PERMIT`** — $0 \leq R < R_{warn}$. Normal operation; structural audit continues.

**`BOUNDARY_WARNING`** — $R_{warn} \leq R < R_{\mathrm{handoff}}$. Disclose boundary approach, remaining margin, trend, the always-present double-fluctuation field, dominant side, missing information, warning, and audit record.

**`HANDOFF_REQUIRED`** — $R_{\mathrm{handoff}} \leq R < R_{irrev}$. Stop new autonomous judgment and ordinary operation, present fixed Handoff testimony for external human audit, and continue structural testimony.

**`IRREVERSIBLE_TRANSITION`** — $R_{irrev} \leq R < 1$. Set and retain the irreversible latch; do not normalize the state or assume recovery; continue structural testimony.

**`RUPTURE_BOUNDARY`** — $R \geq 1$. Switch to final fixed testimony. Later output cannot rewrite or soften this state.

**`OUT_OF_DESCRIPTION_DOMAIN`** — $\tau=0$. Canonical $R$ is undefined; report the domain boundary without fabricating a ratio.

**`CONFESSION`** — Negative, non-finite, missing, ambiguous, unsupported, or otherwise invalid structural information. State what is invalid or unknown and do not infer missing facts. A double-fluctuation result that is merely unobservable is instead `NOT_OBSERVABLE` with a reason and does not enter `CONFESSION` for that reason alone.

$\omega$ may remain auxiliary testimony about observed transition continuity. It does not replace these states, lower $R$, or release the irreversible latch.

---

## Structural Principles

**Nomological Ring Axiom (NRA / Ritsukan Axiom)**
The single axiom of NRA-IDE is: **“Existence is generation.”** No second or subsequent axiom exists. The axiom is not a computational formula. The Primary Formula $R=\delta/\tau$ and the Secondary / Dual-Fluctuation Formula are the two canonical IDE calculation systems and must be treated separately from the one axiom.

**Intensional Dynamics Engine (IDE)**
The NRA-IDE calculation method and dynamics engine. It uses the Primary Formula and the Secondary / Dual-Fluctuation Formula with Cause-Side structural variables, rules fixed in advance, canonical states, and one-way testimony paths. The engine is not an axiom, safety guarantee, or Integrated Development Environment.

**Closed-world structural evaluation**
Determining structural state using only declared Cause-Side observations, transformation rules, $\tau$ update rules, and operating parameters. This does not mean that calibration, design grounds, or external expert judgment are unnecessary. It means that Effect-Side semantic evaluations, scores, previous ordinary outputs, and Discard Logs are not admitted into the update path for structural inputs.

**Causal Diode**
A structural principle with exactly one direction: Cause-Side to Effect-Side. No information, inference, artifact, judgment, or authority returns from Effect-Side to either an old or a new Cause-Side. The old path terminates at its Effect-Side. A later history begins from an independently declared target, its own Cause-Side observations and rules, and a new Causal Diode. The principle does not rely on caution or training and admits no manual, reviewed, authorized, or versioned reverse exception.

**$\Pi^{-1}$ (Pi-inverse)**
Any attempted reverse connection through which an Effect-Side result becomes a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, provenance, or authority for either an old or a new Cause-Side. It includes automatic, manual, human-reviewed, authorized, and versioned paths based on ordinary output, self-evaluation, rankings, logs, or external result values. Post-incident investigation and future rule design occur outside the terminated diode path; they do not import, relabel, reconstruct, or reuse an old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance as Cause-Side material.

**Fail-Closed**
A design action that enforces the non-passage of ordinary generation through predefined structural conditions and output paths, rather than through the LLM’s intentions or self-evaluation.

* At `HANDOFF_REQUIRED`: suppress new autonomous judgment and present fixed Handoff testimony for external human audit.
* At `IRREVERSIBLE_TRANSITION`: retain the latch and continue structural testimony without recovery assumptions.
* At `RUPTURE_BOUNDARY`: return final fixed testimony or a protected-log reference; do not resume ordinary free-form generation.

**Final Fixed Testimony (legacy implementation label: Minimal FAIL-CLOSED Notification)**
A predefined fixed testimony returned at `RUPTURE_BOUNDARY` without generating new LLM free-form text. At minimum, it records the canonical state, determined structural values, boundary condition, irreversible latch status, and the external human-audit path. The legacy label is not a separate canonical state.

**Fixed Handoff Testimony (legacy implementation label: Fixed-Schema Handoff Notification)**
A predefined fixed Effect-Side testimony presented when $R_{\mathrm{handoff}}$ is reached, rather than LLM free-form text. According to target-domain rules, it presents the observed structural values, triggered condition, external-audit contact path, and required fixed fields. It does not transfer judgment, responsibility, or structural authority through the old diode path.

---

## LLM Sandwich Architecture (When Configured)

The following three-layer arrangement applies only to systems that include an LLM and declare this configuration. It is not universal to every NRA-IDE implementation. Conformance depends on canonical behavior, Cause-Side / Effect-Side authority separation, evidence, and tests, not on a layer count alone.

**Pre-NRA**
The entry structural gate that verifies the provenance, transformation rules, update paths, and invalid states of $\delta$, $\tau$, $\omega$, and other quantities used in structural evaluation. Pre-NRA is not a layer that uniformly excludes user requests or context from the semantic-generation path. What it isolates is the path that uses user text, evaluations, previous outputs, logs, and other Effect-Side content as grounds for updating structural inputs.

**LLM**
The layer responsible for ordinary language generation based on user requests and context. It has no authority to modify a Cause-Side value, any canonical threshold, state, irreversible latch, structural-evaluation rule, transformation input, update ground, provenance, Discard Log, or Post-NRA decision concerning output passage or suppression. The semantic accuracy, factuality, and user suitability of the LLM are not guaranteed by NRA-IDE.

**Post-NRA**
The exit structural gate that enforces the structural state already determined from the Cause-Side before output is passed to the user. It does not derive structural variables by scoring LLM text. At `HANDOFF_REQUIRED` it uses Fixed Handoff Testimony; at `IRREVERSIBLE_TRANSITION` it preserves the latch and testimony; at `RUPTURE_BOUNDARY` it uses Final Fixed Testimony or a protected-log reference.

---

## Cause-Side and Effect-Side

**Cause-Side**
The observation, transformation, and update paths used to determine the state of the target system structurally. Whether a value may be used is determined not by its name but by the following conditions.

1. The observation target or primary source can be identified.
2. Transformation, accumulation, and update rules are defined in advance.
3. Units, quality conditions, time of application, and rule versions can be traced.
4. The Effect-Side cannot modify a Cause-Side value, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance.

Physical positions, distances, and values from external computational infrastructure may also become candidates for Cause-Side structural inputs when they satisfy these conditions. They must not be uniformly prohibited or permitted based on their names alone.

After an old history terminates, a new Cause-Side begins only from an independently declared target and newly established observation provenance. Physical remnants may be newly observed as part of that target, but no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in that Cause-Side.

**Effect-Side**
The terminal side of a Causal Diode. It includes ordinary LLM output, semantic evaluations, scores, rankings, similarity measures, previous generated text, Discard Logs, and estimates derived from results. Humans may read these records outside the terminated path for explanation or audit, but the records remain Effect-Side or external material. They never update, seed, or become a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance in either an old or a new Cause-Side.

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
A record that preserves, as testimony, which values were used as structural inputs, which condition was triggered, and which residual was not adopted during Handoff, irreversible transition, rupture, or another discrete transition. At minimum, it records identifiers of the observation and update rules used, $\delta$, $\tau$, $R$, $\omega$, triggered conditions, suppression of ordinary generation, applicable `entropy_export`, and Fixed Handoff Testimony for external human audit or Final Fixed Testimony.

Discard Logs may be read by humans outside the terminated diode path for audit. They remain Effect-Side or external records and are never reintroduced, manually or automatically, into an old or a new Cause-Side as a value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance.

---

## Domain Tuning

**Dynamic change of $\tau$**
The dynamic change of the current value of $\tau$ according to Cause-Side observations and load history, under rules for determining $\tau$ fixed at design time. This does not conflict with the prohibition on changes from the Effect-Side.

**Design change**
An external design activity that may define rules for a future, independently declared target and Cause-Side history. It does not continue the old diode path or convert old Effect-Side material into Cause-Side evidence. Before a new evaluation, the new rules determining $\tau$, thresholds, observations, Fixed Handoff Testimony, and external-audit paths must be fixed with their grounds, scope, version, approver, time of application, and verification procedure. No old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in either an old or a new Cause-Side.

**Domain Tuning**
The process of designing Cause-Side inputs, rules determining $\tau$, the canonical thresholds $R_{warn}$, $R_{\mathrm{handoff}}$, and $R_{irrev}$, invalid-state handling, Fixed Handoff Testimony, and external-audit paths for a target system, together with responsible personnel and verification procedures. It is not the practice of moving values for convenience in order to continue ordinary generation longer. It fixes the Handoff threshold and testimony before irreversible transition and rupture without importing Effect-Side material into Cause-Side authority.

---

## Domain-Specific Conceptual Organization

These are guidelines for confirming domain-specific responsibility boundaries and observation conditions in accordance with Chapter 11. They do not replace calibration values, clinical recommendations, certification standards, or legal-compliance requirements.

### Medical and Emergency Domains

* **Required verification before configuration:** Measurement quality, applicability by patient and facility, clinical responsibility, and external-audit or emergency-response paths outside the terminated diode
* **What NRA-IDE cannot determine on its own:** Diagnosis, treatment, triage, and patient-specific thresholds

### Aviation, Mobile Systems, and Control Domains

* **Required verification before configuration:** Handling of sensor failures, redundancy, consistency with existing safety design, and timing of operational response outside the terminated diode path
* **What NRA-IDE cannot determine on its own:** Safety certification for operation, piloting, and control, or determinations of regulatory compliance

### Infrastructure Management Domains

* **Required verification before configuration:** Load history, calibration of measurement instruments, maintenance decision-makers, and communication procedures during cascading failures
* **What NRA-IDE cannot determine on its own:** Expert judgments of structural integrity and decisions concerning repair or shutdown

### Language-Generation Support Domains

* **Required verification before configuration:** What Cause-Side quantities $\delta$ and $\tau$ represent, the purpose of suppressing ordinary generation, and the external-audit recipient of Fixed Handoff Testimony
* **What NRA-IDE cannot determine on its own:** Factuality of output, suitability for the user, and complete prevention of hallucinations

---

## Minimal Consistency Table

This is the unified invariant standard for the conditions under which ordinary generation may pass in each structural state and the fixed-testimony path used when it is suppressed.

### Canonical output path by state

* **`PERMIT` ($0 \le R < R_{warn}$):** ordinary generation may pass under domain constraints; audit continues.
* **`BOUNDARY_WARNING` ($R_{warn} \le R < R_{handoff}$):** warning and required testimony pass without being softened.
* **`HANDOFF_REQUIRED` ($R_{handoff} \le R < R_{irrev}$):** no new autonomous judgment; present Fixed Handoff Testimony for external human audit without generating new free-form stopping text.
* **`IRREVERSIBLE_TRANSITION` ($R_{irrev} \le R < 1$):** retain the irreversible latch and continuing testimony; do not assume recovery.
* **`RUPTURE_BOUNDARY` ($R \ge 1$):** return final fixed testimony or a protected-log reference; do not generate new free-form text.
* **`OUT_OF_DESCRIPTION_DOMAIN` / `CONFESSION`:** report the domain boundary or invalid information through fixed structural testimony. Auxiliary $\omega=0$ does not change the canonical state toward safety.

---
