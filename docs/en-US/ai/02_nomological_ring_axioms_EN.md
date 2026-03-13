# 02 Nomological Ring Axioms — From Axiom to Computation

<!-- FILE: 02_nomological_ring_axioms_EN.md -->

---

## From the axiom to a computational structure

In the previous chapter, we introduced a simple axiom.

**Existence is generation.**

Generation always produces boundaries.
A boundary implies a threshold.
A dynamic system with thresholds inevitably changes state.

The question then becomes:

**How can the state of such a structure be measured?**

NRA-IDE answers this question using two directly observable quantities.

---

## Fluctuation (δ)

**δ represents fluctuation.**

More precisely, δ is the **instantaneous amplitude of deviation** within a structure.

External forces, environmental variation, pressure, or load may disturb the structure.
The magnitude of that disturbance at a given moment is δ.

This quantity is not inferred through a calculation.
It is measured directly.

Examples include:

* vibration in a mechanical structure
* variation in physiological signals
* changes in system load
* deviations in environmental measurements

In all cases, δ expresses **how strongly the structure is currently fluctuating**.

---

## Structural thickness (τ)

The second quantity is **τ (tau)**.

τ represents the **structural thickness**, or margin, of the boundary.

It is not a distance from a center.
NRA-IDE assumes **no center exists**.

Instead, τ describes the **capacity of the boundary to absorb fluctuation**.

You can think of τ as the structural margin before the boundary is exceeded.

Examples include:

* the stress tolerance of a material
* the physiological tolerance of a patient
* the safe operating margin of a control system
* the load capacity of an infrastructure system

As long as fluctuation remains within this margin, the structure remains stable.

---

## The ratio that defines the state

Once δ and τ are known, the structural state can be expressed by a simple ratio.

```text
R = δ / τ
```

R represents **how much of the structural margin is currently being used**.

This ratio does not require a center, distance, or optimization target.

It only measures the relationship between fluctuation and available margin.

---

## Why a ratio instead of distance

Traditional systems rely on distance.

Distance requires a center.
The state is measured by how far something moves away from that center.

But in many real systems there is **no meaningful center**.

Structures operate between boundaries rather than around centers.

By using a ratio instead of distance, NRA-IDE removes the need for:

* central coordinates
* optimization targets
* score functions

The structure simply evaluates how close it is to its boundary.

---

## Observing the state of a structure

Once δ and τ are available, the state of the structure becomes visible.

We can ask three simple questions:

* How strongly is the structure fluctuating? (δ)
* How much structural margin remains? (τ)
* How close is the structure to its limit? (R)

These three quantities describe the present state without relying on prediction or semantic interpretation.

---

## Separation between axiom and computation

It is important to keep two layers separate.

The **axiom** is philosophical.
The **equation** is computational.

The axiom states that dynamic systems emerge through generation and boundaries.

The equation

```text
R = δ / τ
```

is simply a practical method for measuring the state of such a structure.

Mixing the two layers would create confusion.

The axiom provides the foundation.
The equation provides the measurement.

---

## The next step

Now that the structural state can be expressed through δ and τ, another question appears.

Even if we measure the structure correctly, **how do we prevent reverse reasoning from the result back to the cause?**

This problem appears in many AI systems, where results are used to infer the next input.

The next chapter introduces the mechanism designed to prevent this.

**The Causal Diode.**
