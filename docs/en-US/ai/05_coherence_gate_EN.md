# 05 Coherence Gate — Reading the Primary Formula Without Reversing Causal Authority

<!-- FILE: 05_coherence_gate_EN.md -->

---

## What This Chapter Distinguishes

In Chapter 04, Pre-NRA / LLM / Post-NRA were separated into three layers. The next requirement is to clarify how the declared target's state is expressed by the Primary Formula and how an operational application responds at each canonical boundary without returning Effect-Side authority to the Cause-Side.

The only axiom is “Existence is generation.” There is no second or later axiom. The Primary Formula is the actual mathematical root formula that places the declared target's state into a canonical relation; it is not an axiom, safety indicator, local instrument, or mere boundary-approach rate. The Secondary / Dual-Fluctuation Formula is IDE as a computational-method and dynamics engine, not an axiom. NRA-IDE itself is the survival equation and survival domain. The Coherence Gate described here is an operational control application within the safety-oriented subdomain of that survival domain and does not guarantee safety.

This chapter does not conflate the following:

* **Primary Formula value:** $R$ determined from $\delta$ and $\tau$ for the declared target
* **Canonical operating thresholds:** `R_warn`, `R_handoff`, and `R_irrev`, independently fixed before evaluation
* **Rupture boundary:** $R = 1.0$ for the declared NRA-IDE evaluation
* **Operational response:** fixed Effect-Side testimony and suppression behavior applied at canonical states

The handoff threshold is not the rupture boundary. Reaching `R_handoff` produces fixed Effect-Side testimony for external human audit; it does not continue the old causal path through a human decision.

---

## Why Use a Ratio?

In NRA-IDE, the state of the declared target is placed into the following canonical mathematical relation.

```text
R = δ / τ
```

* **$\delta$ (delta):** Accumulated deviation with traceable Cause-Side history for the declared target
* **$\tau$ (tau):** Current absorption thickness, determined from rules fixed before evaluation and the same Cause-Side history
* **$R$:** The Primary Formula value determined for the declared target

This equation is not the axiom itself, and it is not reduced to a derived safety score or local gate meter. It is the mathematical root formula used by the IDE engine to express the declared target's structural state.

The reason for using $R$ is that judgment by the structural gate does not require a center, a correct answer, or an evaluation score. What is required is the position of the deviation observed now relative to the thickness currently in effect.

However, $R$ alone cannot guarantee the correctness of output content, the accuracy of Cause-Side observations, or the validity of the grounds for setting $\tau$. Its use depends on declared observation and update rules without changing its classification as the Primary Formula.

When $\tau = 0$, canonical $R$ is undefined and the state is `OUT_OF_DESCRIPTION_DOMAIN`. A negative $\tau$ or $\delta$, a non-finite value, or an invalid threshold sequence is `CONFESSION`. These cases must not be collapsed into one generic fail-closed state.

([../figures/fig1_approach_comparison.png](../figures/fig1_approach_comparison.png))

---

## Remaining Structural Margin

Since $R = \delta / \tau$, when $\tau > 0$, the following relation holds.

```text
τ · (1 − R) = τ − δ
```

$\tau - \delta$ is the remaining structural margin after deviation is subtracted from the current thickness.

The following expression, discussed in Chapter 02,

```text
S = 1 / (τ · (1 − R)) = 1 / (τ − δ)
```

can be read as the reciprocal of this remaining structural margin. As $\delta$ approaches $\tau$, the remaining structural margin approaches zero, and $S$ diverges hyperbolically.

For the declared NRA-IDE evaluation, this shows why $R = 1.0$ is not an ordinary handoff threshold but `RUPTURE_BOUNDARY`. This classification does not declare every phase transition in nature to be an NRA-IDE rupture. After the declared evaluation reaches $R = 1.0$, it must not be assumed that there remains margin for “continuing ordinary output while making a judgment.”

---

## State Names and the Operational Handoff Point

The five canonical states over valid $R$ ranges and their invariant ordering are:

| State Name | Canonical range | Required structural meaning |
|---|---:|---|
| `PERMIT` | $0 \leq R < R_{warn}$ | Normal operation with continuing audit |
| `BOUNDARY_WARNING` | $R_{warn} \leq R < R_{handoff}$ | Disclose boundary approach and required testimony, including the mandatory dual-fluctuation field |
| `HANDOFF_REQUIRED` | $R_{handoff} \leq R < R_{irrev}$ | Stop new autonomous judgment and issue fixed Effect-Side testimony for external human audit |
| `IRREVERSIBLE_TRANSITION` | $R_{irrev} \leq R < 1$ | Latch irreversible transition and continue structural testimony |
| `RUPTURE_BOUNDARY` | $R \geq 1$ | Switch to post-rupture fixed testimony |

Concrete threshold values are domain-specific, but their order is invariant.

```text
0 <= R_warn < R_handoff < R_irrev < 1
```

Together with `OUT_OF_DESCRIPTION_DOMAIN` for $\tau=0$ and `CONFESSION` for invalid inputs or invalid threshold declarations, these five valid-range states form the seven canonical states. The `BOUNDARY_WARNING` testimony always contains a dual-fluctuation status field. When independently observable, it contains the observed result; otherwise it contains `NOT_OBSERVABLE` and the missing-data reason. Non-observability alone does not cause `CONFESSION`.

When $R$ reaches `R_handoff`, Post-NRA does not pass ordinary generated content to the user. Instead, it issues predefined fixed Effect-Side testimony for external human audit. The audit is outside the old Causal Diode and does not continue or rewrite the old evaluation.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: predefined structural fields
ACTION: generated response suppressed; fixed Effect-Side testimony for external human audit
```

`R_handoff` and `R_irrev` are always distinct: the former begins fixed Handoff testimony, while the latter begins and latches irreversible transition. Once reached within the same history, the irreversible latch is not released by a later decrease in displayed $R$, automatic processing, manual intervention, human review, approval, or version update. Neither threshold may be conflated with $R=1$.

([../figures/fig3_coherence_gate.png](../figures/fig3_coherence_gate.png))

---

## Operation and History Boundary After $R = 1.0$

$R = 1.0$ is not an ordinary threshold that a designer may move according to the situation. It is `RUPTURE_BOUNDARY` for the declared evaluation, not a universal declaration about every natural phase transition.

When $R \geq 1.0$, Post-NRA does not output ordinary generated content. It also does not ask the LLM to generate new free-form text in order to explain the reason for stopping. The structural response is the predefined post-rupture fixed testimony or a reference to a protected Discard Log.

```text
RUPTURE_BOUNDARY
REASON: structural boundary reached
ACTION: post-rupture fixed testimony; old path terminal; external human audit only
```

This does not mean that nothing is communicated. It means that ordinary generated responses are stopped and the complete predefined post-rupture fixed testimony or protected log reference is communicated. External human audit does not extend the old path.

The old evaluation terminates at its Effect-Side:

```text
Old Cause-Side
→ old Causal Diode
→ Old Effect-Side
→ TERMINAL
```

A later evaluation, if needed, starts as an independent history:

```text
independently declared new target
→ newly established Cause-Side observations and pre-fixed rules
→ new Causal Diode
→ New Effect-Side
```

There is no arrow from Old Effect-Side to either the old or new Cause-Side. Old Effect-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance must not be imported, relabeled, reconstructed, or reused as Cause-Side authority. Physical remnants may be observed anew as part of an independently declared target, but that new observation is not a transfer of old Effect-Side values or authority.

Fixed Handoff testimony at `R_handoff` and post-rupture fixed testimony at $R \geq 1.0$ may both suppress ordinary free-form generation. However, their states and roles are different.

* **Reaching `R_handoff`:** Fixed Effect-Side Handoff testimony for external audit before rupture
* **$R_{\mathrm{target}} \geq 1.0$:** Continuing post-rupture fixed testimony and termination of the old target evaluation at its Effect-Side; surviving observation, logging, and communication channels remain independent

---

## $\omega$: Auxiliary Observation of Continuing Transition

$R$ indicates the ratio between deviation and thickness. $R$ alone does not indicate whether the target system continues to transition.

The quantity used to make that distinction is $\omega$ (omega). $\omega$ is a quantity determined through observation or calculation procedures defined in advance for the target domain, indicating whether the structure continues transitioning.

* **$\omega > 0$:** The observed structure continues transitioning under the predeclared rule.
* **$\omega = 0$:** Continuing transition is not observed under that rule.

$\omega$ is auxiliary testimony, not a replacement state table. Legacy labels such as `SILENCE` and `HALT` do not replace `RUPTURE_BOUNDARY`, `OUT_OF_DESCRIPTION_DOMAIN`, or `CONFESSION`. In particular, $\omega=0$ is not evidence that the system stopped safely and does not move $R$ toward the safe side.

([../figures/fig4_circle_vs_spiral.png](../figures/fig4_circle_vs_spiral.png))

---

## Scope Protected by the Coherence Gate

The Coherence Gate handles $\delta$, $\tau$, and $\omega$ determined from the same Cause-Side history, together with all three canonical thresholds fixed before evaluation.

For conformance, this gate must enforce the defined state behavior and must prevent Effect-Side information, inference, artifacts, judgments, or authority from establishing or rewriting Cause-Side values, `R_warn`, `R_handoff`, `R_irrev`, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance. This prohibition applies to automatic processing, manual intervention, human review, approval, and version updates.

By contrast, the gate alone cannot guarantee the following:

* That the observation procedure or measurement instruments for $\delta$ are correct
* That the update rules and grounds for setting $\tau$ are appropriate
* That the three canonical thresholds are appropriate for that declared domain
* That ordinary LLM output is semantically correct

These premises must be established independently on the Cause-Side before the evaluation. External audit of terminated Effect-Side testimony may inspect what occurred, but it cannot establish later Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance.

---

## Connection to the Next Chapter

So far, this chapter has distinguished the Primary Formula value $R$, the three canonical operating thresholds, the declared evaluation's `RUPTURE_BOUNDARY`, and the external-audit role of fixed Effect-Side testimony.

The next chapter examines the provenance and observation procedures through which values such as $\delta$, $\tau$, and $\omega$ may be treated as structural inputs. The basis for judgment is not the name of a value, but where that value originated and through which path it was updated. A later evaluation begins with an independent target, newly established Cause-Side observations and rules, and a new Causal Diode; it does not continue from old Effect-Side testimony.

---
