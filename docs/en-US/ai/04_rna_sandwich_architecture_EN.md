# 04 RNA Sandwich Architecture — Structural Isolation of the LLM

<!-- FILE: 04_rna_sandwich_architecture_EN.md -->

---

## Why the model itself cannot guarantee safety

Large Language Models generate outputs by predicting the most probable continuation of a sequence.

This mechanism is extremely powerful for producing language.
However, it does not inherently understand **structural limits**.

The model attempts to produce an answer even when the available information is insufficient.
As a result, hallucinations and unstable outputs can occur.

Traditional safety approaches try to solve this problem **inside the model** by adding filters, alignment rules, or reinforcement learning signals.

But those approaches still depend on the internal behavior of the model.

NRA-IDE takes a different approach.

Instead of modifying the model, it **places the model inside a structural boundary**.

---

## The sandwich structure

The architecture is composed of three layers.

```text
Pre-RNA   →   LLM   →   Post-RNA
```

The language model operates only in the middle.

Both the input and the output pass through structural layers that enforce the causal rules described earlier.

This structure prevents reverse reasoning and ensures that structural limits are respected.

---

## Pre-RNA: the causal entrance

The **Pre-RNA layer** receives information from the external environment.

At this stage, the system measures the cause-side quantities:

* δ (fluctuation)
* τ (structural thickness)
* R (limit ratio)
* ω (angular velocity)

Only values that belong to the cause-side domain are allowed to enter the computation.

Effect-side values such as scores, similarity metrics, or previous outputs are excluded.

If the measured state exceeds the permitted boundary, the system stops before reaching the model.

This ensures that the LLM never receives inputs that already violate the structural margin.

---

## LLM: semantic processing only

Inside the sandwich sits the **language model itself**.

The LLM performs semantic processing:

* interpretation of language
* generation of responses
* transformation of information into human-readable form

However, the LLM does **not evaluate structural limits**.

Those evaluations occur outside the model.

Because of this separation, the architecture does not depend on the internal design of a particular model.

Different models can be replaced or updated without changing the surrounding structure.

---

## Post-RNA: structural verification

After the model produces an output, the **Post-RNA layer** performs structural verification.

The system checks whether the generated result remains within the allowed structural margin.

The same cause-side quantities are used again to evaluate the state.

If the boundary is exceeded, the output is not propagated further.

Instead, the system activates the **Fail-Closed mechanism**, which transfers the decision to the next responsible agent.

---

## Why this architecture is robust

The sandwich structure introduces two critical properties.

First, **semantic processing and structural safety are separated**.

The LLM handles meaning.
The surrounding layers handle structure.

Second, **reverse reasoning remains impossible**.

Because the LLM never receives effect-side values as causal inputs, optimization loops cannot form.

The model cannot chase scores or evaluation signals.

Instead, it operates strictly within the structural limits defined by the surrounding layers.

---

## Visualization of the architecture

See the following diagram for a conceptual overview:

```text
figures/RNA Box Sandwich Architecture_EN.jpg
```

An interactive explanation is also available:

```text
figures/sandwich_architecture.html
```

These figures illustrate how information passes through the three layers while maintaining causal direction.

---

## The next step

Now that the LLM has been structurally isolated, the remaining question is how the system determines **when the structural margin is being approached**.

This is handled by the **Coherence Gate**, which classifies the state of the system according to the ratio between fluctuation and structural thickness.

The next chapter introduces this mechanism.
