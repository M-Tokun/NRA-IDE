# 06 Observables — Cause-Side and Effect-Side Quantities

<!-- FILE: 06_observables_EN.md -->

---

## Why observables must be separated

In previous chapters, we introduced the Causal Diode and the Coherence Gate.

The Causal Diode prevents reverse reasoning.

The Coherence Gate classifies the structural state.

For these mechanisms to function correctly, the system must clearly distinguish between two types of quantities.

These are:

* **Cause-Side observables**

* **Effect-Side quantities**

Mixing these two categories reintroduces reverse reasoning into the system.

Therefore, NRA-IDE strictly separates them.

---

## Cause-Side observables

Cause-side observables are values that exist **before a computation produces any result**.

They are measured directly from the state of the system or environment.

Examples include:

* **δ (fluctuation)** — the amplitude of structural deviation

* **τ (structural thickness)** — the available margin of the boundary

* **R (limit ratio)** — the ratio between fluctuation and structural thickness

* **ω (angular velocity)** — the temporal progression of structural change

* **violation accumulation** — accumulated deviation relative to the boundary

These quantities describe the **present structural state**.

They do not depend on prediction, inference, or interpretation.

---

## Effect-Side quantities

Effect-side quantities appear **after a computation has produced a result**.

They are derived from calculations or model outputs.

Examples include:

* distance from a reference point

* coordinates in a space

* similarity scores

* ranking values

* semantic interpretation

* previous outputs of a model

These values can be useful for analysis or logging, but they **cannot be used as causal inputs**.

If effect-side quantities are fed back into computation, reverse reasoning begins.

---

## The boundary between observation and computation

In NRA-IDE, the boundary between these two domains is explicit.

Only cause-side observables are allowed to participate in structural evaluation.

Effect-side quantities are treated as **records of what happened**, not as inputs for further reasoning.

This design prevents optimization loops and score-chasing behavior.

---

## Example: infrastructure monitoring

Consider an infrastructure system such as a dam.

Cause-side observables might include:

* vibration amplitude

* water pressure fluctuation

* structural stress measurements

From these values the system calculates:

```

R = δ / τ

```

This ratio determines whether the structure remains within safe limits.

In contrast, effect-side quantities such as evaluation scores or predicted outcomes are unnecessary for determining the present structural state.

---

## Observables and transparency

Because cause-side observables are directly measurable, they also improve transparency.

An operator can inspect the measurements and verify the system’s state independently.

This differs from systems that rely on complex internal scores or hidden evaluation metrics.

In NRA-IDE, the structural condition of the system is visible through measurable quantities.

---

## Visualization

An example visualization of structural degradation can be seen here:

[nra_dam_degradation_EN.html](../figures/nra_dam_degradation_EN.html)

This example illustrates how observable fluctuations relate to the structural margin.

---

## Next chapter

Now that the system can observe structural conditions and classify them, the remaining question is operational behavior.

What should happen when the structural boundary is exceeded?

The next chapter introduces the **Fail-Closed mechanism**, which ensures that the system stops safely when limits are reached.
