# 03 Causal Diode — A Structure That Prevents Reverse Reasoning

<!-- FILE: 03_causal_diode_EN.md -->

---

## Why reverse reasoning occurs

As described in Chapter 02, errors accumulate when causes are inferred from results.

A score or evaluation value appears as the result of a computation.
When that result is used as an input for the next calculation, a feedback loop begins.

This is one of the root causes behind deception and instability in AI systems.

The question then becomes:

**How can such reverse reasoning be prevented inside the computation itself?**

The mechanism introduced here is the **Causal Diode**.

---

## The idea of a diode

In an electrical circuit, a diode allows current to flow only in one direction.

If voltage is applied in the reverse direction, the current does not flow.

Importantly, this is not achieved by constantly checking whether reverse flow is happening.
Instead, the circuit is designed so that reverse flow **cannot occur structurally**.

The causal diode follows the same idea.

Information flows **from cause to effect**.
Information does **not** flow from effect back to cause.

This is not a rule enforced by monitoring.
It is a structural property of the computation.

---

## Cause-side and effect-side quantities

This distinction is the core of the mechanism.

**Cause-side quantities** are values that exist before computation begins.

Examples include:

* structural fluctuation (δ)
* boundary thickness (τ)
* angular velocity (ω)
* accumulated deviation (violation)

These values can be directly measured through observation.
They do not require inference.

---

**Effect-side quantities**, in contrast, appear **only after a calculation has been performed**.

Examples include:

* distance
* coordinates
* scores
* evaluation values
* semantic interpretation
* previous outputs

All of these are results produced by computation.

The moment an effect-side value is used as the cause of a new computation, reverse reasoning begins.

For example:

> “Because this score appeared, the next input should be adjusted to increase it.”

This chain of reasoning gradually transforms the system into one that optimizes only for the score itself.

---

## Boundary detection requires only cause-side values

Returning to the concept of structural boundaries introduced earlier:

To determine whether a system is inside or outside a boundary, only cause-side values are required.

We ask:

* How large is the fluctuation?
* How much structural margin remains in the boundary thickness?

These values are sufficient to determine **the present structural state**.

Distance, score, or semantic interpretation are unnecessary.

In fact, introducing those values shifts the goal from boundary detection to score maximization.

---

## What changes when reverse reasoning is prohibited

When reverse reasoning becomes structurally impossible, four major changes occur.

First, **scores disappear**, which means optimization pressure disappears.
Goodhart’s Law no longer applies.

Second, because the structure does not evaluate meaning, semantic interpretation can remain entirely within the model itself.
The NRA-IDE framework functions independently of the model architecture.

Different models simply perceive boundaries with different resolutions.

---

Third, because effect-side values are never reused as inputs, hallucinations can be detected as **structural violations** rather than semantic mistakes.

Instead of asking whether an answer is meaningful, the system checks whether the ratio between fluctuation and structural thickness exceeds the limit.

---

Finally, a system without reverse reasoning has **no path for deception or hidden optimization**.

There is no detour through which a score can be secretly maximized.

---

## Cause-side quantities in NRA-IDE

The cause-side quantities handled by NRA-IDE include the following.

**δ (fluctuation)**
The instantaneous amplitude of structural deviation.

**τ (structural thickness)**
The available margin of the boundary.

**R (limit ratio)**
The ratio between δ and τ, indicating proximity to the limit.

**ω (angular velocity)**
Indicates whether the structure continues to evolve over time.

**Violation (accumulated deviation)**
The accumulation of structural deviation relative to the boundary.

All of these quantities can be directly measured at the present moment.
They require neither prediction nor reverse inference.

---

## Next chapter

Now that reverse reasoning has been structurally blocked, the next question emerges.

How can this causal structure be applied to large language models?

The next chapter introduces the **Sandwich Architecture**, which surrounds an LLM with causal layers.
