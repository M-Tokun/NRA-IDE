# 05 Coherence Gate — Reading Structural State Through a Ratio and Separating Handoff Points

<!-- FILE: 05_coherence_gate_EN.md -->

---

## What This Chapter Distinguishes

In Chapter 04, Pre-NRA / LLM / Post-NRA were separated into three layers. The next requirement is to clarify what Post-NRA uses as grounds for allowing ordinary output to pass, and when it suppresses ordinary output and hands judgment over to humans.

This chapter does not conflate the following three:

* **Structural state:** The ratio $R$ derived from $\delta$ and $\tau$ originating from the Cause-Side
* **Handoff point:** A domain-specific operating point at which ordinary output is suppressed and judgment is handed over to humans
* **Phase-transition boundary:** $R = 1.0$, the invariant terminal boundary at which structural margin is lost

The handoff point is not the same as the phase-transition boundary. In safety design, ordinary output is stopped, in principle, before $R = 1.0$ is reached.

---

## Why Use a Ratio?

In NRA-IDE, the state of a structure is described through the following computational principle.

```text
R = δ / τ
```

* **$\delta$ (delta):** A deviation or fluctuation observed in the target system
* **$\tau$ (tau):** The currently absorbable structural thickness, determined from rules defined at design time and Cause-Side load history
* **$R$:** The structural ratio occupied by deviation relative to the current thickness

This equation is not the axiom itself. It is a computational principle adopted by IDE to read structural state from the design premise that “Existence is generation.”

The reason for using $R$ is that judgment by the structural gate does not require a center, a correct answer, or an evaluation score. What is required is the position of the deviation observed now relative to the thickness currently in effect.

However, $R$ alone cannot guarantee the correctness of output content, the accuracy of Cause-Side observations, or the validity of the grounds for setting $\tau$. This equation indicates structural state under the defined observation and update rules.

When $\tau \leq 0$, the ratio cannot be validly defined. This state does not permit ordinary output. It transitions to predefined invalid-state notification and human handoff.

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

This shows that $R = 1.0$ is not an ordinary handoff point, but the phase-transition boundary at which structural margin is lost. After $R = 1.0$, it must not be assumed that there remains margin for “continuing ordinary output while making a judgment.”

---

## State Names and the Operational Handoff Point

This document set uses the following names to explain structural states.

| State Name |           Reference $R$ Range | Description                                                                                                            |
| ---------- | ----------------------------: | ---------------------------------------------------------------------------------------------------------------------- |
| NIRVANA    |                     $R < 0.4$ | A state in which deviation is small relative to thickness                                                              |
| ELASTIC    |            $0.4 \leq R < 0.7$ | A region in which margin remains, but state tracking is required                                                       |
| CRITICAL   |            $0.7 \leq R < 1.0$ | A region approaching the phase-transition boundary                                                                     |
| SILENCE    | $R \geq 1.0$ and $\omega > 0$ | A state in which the phase-transition boundary has been reached or exceeded, and ordinary generation does not continue |

These ranges are **explanatory baseline classifications** for reading the document. They are not autonomous operating thresholds shared by every domain.

In actual operation, a domain-specific **handoff point** is established before the phase-transition boundary. This chapter denotes it as `Rop`.

```text
0 < Rop < 1.0
```

When $R$ reaches `Rop`, Post-NRA does not pass ordinary generated content to the user. Instead, it issues a predefined fixed-format notification and delegates judgment to humans.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: predefined structural fields
ACTION: generated response suppressed; human review required
```

The important point is that `Rop` is an operational handoff condition distinct from the names NIRVANA / ELASTIC / CRITICAL. In high-risk domains, `Rop` may be placed before entry into CRITICAL. Therefore, whether ordinary output is allowed must not be determined from the state name alone.

When another document uses the notation `R_irrev`, the domain specification must explicitly state whether it is the same handoff point as `Rop` or a separate warning threshold. It must not be conflated with $R = 1.0$.

([../figures/fig3_coherence_gate.png](../figures/fig3_coherence_gate.png))

---

## Operation After $R = 1.0$

$R = 1.0$ is not an ordinary threshold that a designer may move according to the situation. It is the phase-transition boundary at which structural margin is lost.

When $R \geq 1.0$, Post-NRA does not output ordinary generated content. It also does not ask the LLM to generate new free-form text in order to explain the reason for stopping. The only permitted response is a predefined minimal FAIL-CLOSED indicator or a reference to a protected Discard Log.

```text
FAIL_CLOSED
REASON: structural boundary reached
ACTION: no further generated response; human handoff required
```

This does not mean that nothing is communicated. It means that ordinary generated responses are stopped and only the minimum structurally determined state is communicated in a fixed format.

Handoff at `Rop` and FAIL-CLOSED at $R \geq 1.0$ both suppress ordinary generation. However, their roles are different.

* **Reaching `Rop`:** Operational handoff to humans before the phase-transition boundary
* **$R \geq 1.0$:** Terminal processing after structural margin has been lost. No new LLM generation is performed

---

## $\omega$: Indicating Whether Transition Continues

$R$ indicates the ratio between deviation and thickness. $R$ alone does not indicate whether the target system continues to transition.

The quantity used to make that distinction is $\omega$ (omega). $\omega$ is a quantity determined through observation or calculation procedures defined in advance for the target domain, indicating whether the structure continues transitioning.

* **$\omega > 0$:** The structure continues transitioning
* **$\omega = 0$:** Transition cannot be confirmed under the same rules; handled separately as HALT

SILENCE and HALT are not the same.

* **SILENCE:** $R \geq 1.0$ and $\omega > 0$. The phase-transition boundary has been crossed, but the structure continues transitioning. Ordinary generation is stopped, and the matter is handed over to humans through a minimal fixed-format output.
* **HALT:** $\omega = 0$. Transition cannot be treated as continuing. This does not provide grounds for reinterpreting $R$ toward the safe side, and requires separate human judgment.

$\omega = 0$ does not simply mean that the system has “stopped safely.” Humans must verify the observation procedure, target system, and conditions for continuation.

([../figures/fig4_circle_vs_spiral.png](../figures/fig4_circle_vs_spiral.png))

---

## Scope Protected by the Coherence Gate

The Coherence Gate handles $\delta$, $\tau$, and $\omega$ determined from the Cause-Side, together with handoff conditions defined in advance.

What this gate guarantees is that, when defined conditions are reached, ordinary generation is suppressed and Effect-Side semantic evaluation does not rewrite $\delta$, $\tau$, or `Rop`.

By contrast, the gate alone cannot guarantee the following:

* That the observation procedure or measurement instruments for $\delta$ are correct
* That the update rules and grounds for setting $\tau$ are appropriate
* That `Rop` is appropriate as a point of approach to an irreversible regime in that domain
* That ordinary LLM output is semantically correct

These are premises that humans must verify in design, implementation, and operation.

---

## Connection to the Next Chapter

So far, this chapter has distinguished the ratio $R$, the phase-transition boundary $R = 1.0$, and the handoff point `Rop` placed before that boundary.

The next chapter examines the provenance and observation procedures through which values such as $\delta$, $\tau$, and $\omega$ may be treated as structural inputs. The basis for judgment is not the name of a value, but where that value originated and through which path it was updated.

---
