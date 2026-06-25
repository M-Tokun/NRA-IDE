
# 06 Observable Quantities — Verifying the Provenance and Update Path of Values

<!-- FILE: 06_observables_EN.md -->

---

## “Observable” Does Not Mean Only Raw Sensor Values

Chapter 05 confirmed that structural state is read through the following computational principle.

```text
R = δ / τ
```

The important point here is that values usable for structural evaluation must not be divided simply into “directly measured values” and “calculated values.”

Raw sensor values are not the only values that may be used. Structural variables obtained by transforming or accumulating Cause-Side observations according to rules defined in advance also exist. $\tau$, $\omega$, $\varphi$, and $R$ are representative examples.

Conversely, not every calculated value may be used. When LLM output, evaluation scores, past logs, or estimates made after examining results become grounds for updating $\delta$ or $\tau$, the $\Pi^{-1}$ path discussed in Chapter 03 arises.

What NRA-IDE asks is not whether a value “has been calculated,” but **where it originated, under which rules it was updated, and whether it cannot be rewritten from the Effect-Side**.

---

## Conditions for Treating a Value as a Structural Input

For a value to be treated as a Cause-Side structural input, it must satisfy at least the following conditions.

1. **Its provenance can be traced**

   * It originates from observations of the target system, physical loads, or records of those observations or loads.
2. **Observation, transformation, and update rules are defined in advance**

   * Rules must not be altered opportunistically after examining outputs or evaluations produced during execution.
3. **The path to the current value can be verified**

   * It must be possible to trace which observations and rules produced the current value.
4. **The Effect-Side is not granted update authority**

   * LLMs, evaluators, scores, previous generated text, and logs must not be able to modify $\delta$, $\tau$, or the handoff point.
5. **Missing values are not filled through Effect-Side estimation**

   * When required observations or update histories are missing, they must not be supplemented through inference, averaging, or past outputs.

A value that does not satisfy these conditions has not been established as a structural input. The system must not proceed to ordinary structural evaluation. It transitions instead to predefined invalid-state handling or human handoff.

---

## Distinguishing Observations, Structural Variables, and Design Parameters

The following quantities do not have the same role. Raw observations, structural variables determined from the Cause-Side, and operating parameters defined at design time must be distinguished.

| Quantity                               | Role                                                                   | Determination Method                                                                                          | Update from the Effect-Side                         |
| -------------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **$\delta$ (fluctuation / deviation)** | Structural input representing deviation occurring in the target system | Determined from direct observations or observation procedures defined in advance for the target domain        | Prohibited                                          |
| **$\tau$ (thickness)**                 | Currently absorbable structural margin                                 | Determined from rules fixed at design time and Cause-Side load history                                        | Prohibited                                          |
| **$\omega$ (angular velocity)**        | Quantity indicating whether the structure continues transitioning      | Determined from time-series Cause-Side observations or state-transition rules fixed in advance                | Prohibited                                          |
| **$\varphi$ (phase)**                  | Internal state indicating the position of structural state transition  | Updated according to transition rules originating from the Cause-Side                                         | Prohibited                                          |
| **$C$ (constraint)**                   | Load or constraint applied externally to the target system             | Determined from sensor values, verified load records, or fixed physical conversions                           | Prohibited                                          |
| **$W$ (work)**                         | Auxiliary quantity used only when required by the domain               | Used only when its definition, unit, and observation procedure are specified in the domain specification      | Prohibited                                          |
| **entropy**                            | Auxiliary quantity used only when required by the domain               | Used only when its definition, calculation rule, and purpose of use are specified in the domain specification | Prohibited                                          |
| **$R$ (structural ratio)**             | Structural state inside the gate derived from $\delta$ and $\tau$      | Calculated through `R = δ / τ`                                                                                | Not used as grounds for updating $\delta$ or $\tau$ |
| **`Rop` (handoff point)**              | Operating condition for suppressing ordinary output                    | Defined in advance by humans as a domain specification, with grounds for changes recorded                     | Prohibited                                          |

“Prohibited” in this table does not mean that the values themselves may not be read. For example, humans may refer to $R$ or logs in order to verify the state. What is prohibited is automatically or arbitrarily rewriting the next $\delta$, $\tau$, or `Rop` on the basis of Effect-Side values.

---

## Do Not Conflate the Meaning of Each Quantity

### $\delta$ Is a Deviation in the Target System

$\delta$ is a value that expresses fluctuations, displacement, or load deviation occurring in the target system through observation procedures defined for the target domain.

$\delta$ is not necessarily a single raw sensor value. Even when it is determined as a deviation from multiple Cause-Side observations, it may be treated as a structural input when the observation targets, transformation formulas, units, update times, and provenance are defined in advance and remain traceable.

Conversely, a “value that appears dangerous” estimated by an LLM from the impression of text, or a value inferred backward from an evaluation score, cannot be treated as $\delta$.

### $\tau$ Is Not a Direct Observation but the Current Thickness Determined by Rules

$\tau$ is the current thickness through which the structure can absorb fluctuation. It is not a value returned directly by a raw sensor.

$\tau$ has two layers.

* **Rules that determine $\tau$:** Fixed at design time. These define which Cause-Side loads are reflected in $\tau$ and through which procedures.
* **The current value of $\tau$:** Changes according to the fixed rules and Cause-Side load history.

Through this distinction, $\tau$ may change dynamically, but LLMs and evaluation scores cannot enlarge it in order to make the system appear safe.

### $\omega$ Indicates Whether Transition Continues

$\omega$ is a quantity that indicates whether the structure continues its state transition. It is not determined from the impression of a single point in time.

When transition can be confirmed on the basis of continuous observations or phase-update rules defined for the target domain, it is treated as $\omega > 0$. Missing observations and $\omega = 0$ are not the same. When the observation path is unknown, $\omega$ must not be filled with a value assumed to be safe; it is treated as an unknown input.

### $\varphi$ Is Not a Spatial Coordinate

$\varphi$ is a **phase** that indicates which stage of structural transition the target system occupies. It does not mean a position on a map or an embedding coordinate generated by a model.

$\varphi$ is an internal state that records Cause-Side state transitions according to rules defined in advance. It is not the same as a “coordinate” or “center” generated by the Effect-Side.

### $C$, $W$, and entropy Are Used Only After Their Necessity Is Defined

$C$ represents external constraints or loads applied to the target system. The observation target is specified for the target domain, such as water pressure, gravity, vibration, or electrical load.

$W$ and entropy are not common inputs required in every implementation. Only when they are used must the domain specification record what they represent, which units they use, and from which Cause-Side observations they are determined.

In this document set, $S = 1 / (\tau \cdot (1 - R))$ is used as the reciprocal of remaining structural margin. Therefore, representing entropy with the same symbol $S$ would create a notation conflict. This chapter denotes entropy as `entropy`. The glossary in Chapter 12 must maintain this notation consistently.

### $R$ and `Rop` Are Not Inputs

$R$ is the structural ratio derived from $\delta$ and $\tau$. $R$ itself is used to read structural state, but a low value of $R$ must not be used as grounds to enlarge $\tau$ or redefine $\delta$ as smaller.

`Rop` is the handoff condition placed at a domain-specific point of approach to an irreversible regime. It is not a value obtained naturally through observation, but a design and operating parameter. When `Rop` is changed, the grounds for change, time of application, approver, and related records must be retained.

$R = 1.0$ is an invariant boundary distinct from `Rop`. Ordinary handoff occurs at `Rop`; after $R = 1.0$ has been reached or exceeded, ordinary generated content does not continue.

---

## Paths That Must Not Be Used as Structural Inputs

The following values and paths must not be used as grounds for updating Cause-Side structural inputs.

**Evaluation scores, similarity measures, and rankings**

These are results produced by evaluators or models. They cannot be used as grounds for adjusting $\delta$ or $\tau$ to make the system appear safe.

**Semantic labels, previous generated text, and LLM self-evaluation**

These are interpretations or generated results in natural language. They must not be fed back into $\delta$ or $\tau$ as grounds for structural state.

**Log contents**

Logs are retained as testimony. Humans may examine them, but they are not used as inputs to the next structural evaluation.

**$\delta$ or $\tau$ inferred backward from results**

Paths that estimate $\delta$ or $\tau$ from results such as “the previous result was safe” or “this output seems plausible” are $\Pi^{-1}$.

**Distances, coordinates, or centers in semantic space**

Distances, coordinates, centers, or positions in similarity space generated by models or evaluators must not be used as grounds for structural input.

However, this does not uniformly prohibit physical positions or distances directly obtained by sensors merely because of their names. When their provenance and transformation rules can be verified as Cause-Side observations of the target system, they may be candidates for structural input. What matters is not the name, but the generation process and update path.

---

## Do Not Fill Gaps When Inputs Are Missing

When the provenance, current value, update history, unit, or applicable rules of a value required for structural evaluation cannot be verified, the gap must not be filled through inference.

```text
CONFESSION: structural input provenance unknown or ambiguous.
UNKNOWN: [missing observation, update rule, unit, or history]
ACTION: do NOT derive from Effect-Side; use predefined invalid-state handling or human handoff.
```

This stop does not reinterpret insufficient observation as “safe.” It records that the prerequisites for structural evaluation have not been established and hands the matter over to humans.

---

## The Duty of Testimony

The duty of testimony in NRA-IDE is to retain not only the values used, but also **where those values came from and under which rules they became their current values**.

At minimum, the following must be recorded.

* Provenance, acquisition time, and units of observations
* Identifiers of the rules used to determine $\delta$, $\tau$, $\omega$, $\varphi$, and related quantities
* Cause-Side load history used to update $\tau$
* Grounds for setting `Rop` and its change history
* Conditions under which ordinary output was suppressed
* Discarded residuals and the storage location of the Discard Log
* Reasons why an input was unknown or an invalid state occurred

This record is testimony that enables humans to verify the grounds for stopping or handoff. It must be protected as write-only and must not become grounds for updating the next $\delta$, $\tau$, or `Rop`.

---

## What Becomes Visible When the Observation Path Is Established

When the provenance and update rules for $\delta$, $\tau$, $\omega$, and $\varphi$ are established, structural state can be traced.

* Which deviations are being observed.
* From which Cause-Side load history the current thickness was determined.
* Whether the structure continues transitioning.
* Under which state-transition rules the phase is advancing.
* Whether the handoff condition for stopping ordinary output has been reached.

This is not about selecting an answer that appears semantically plausible. It is about verifying that the grounds for structural evaluation have not been contaminated by Effect-Side values.

The next chapter explains how, once the observation path has been established, Fail-Closed operates as suppression of ordinary generation, fixed-format notification, and human handoff.

---
