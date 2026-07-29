# 04 Sandwich Architecture — A Three-Layer Operational Application with One-Way Causal Authority

<!-- FILE: 04_rna_sandwich_architecture_EN.md -->

---

## Do Not Give the LLM Cause-Side Structural Authority

The Causal Diode discussed in Chapter 03 permits only `Cause-Side → Effect-Side`. It blocks every attempted $\Pi^{-1}$ connection through which Effect-Side information, inference, artifacts, judgments, or authority would return to either the old or a new Cause-Side.

An LLM is the layer responsible for reading user requests, handling context, and generating natural language. This is the role of the LLM. The semantic correctness of outputs, the provenance of input values, and the location of structural boundaries cannot be guaranteed by the LLM alone.

The only axiom is “Existence is generation.” There is no second or later axiom. The Primary Formula is the actual mathematical root formula that places the declared target's state into a canonical relation; it is not an axiom, safety indicator, local instrument, or mere boundary-approach rate. The Secondary / Dual-Fluctuation Formula is IDE as a computational-method and dynamics engine, not an axiom. NRA-IDE itself is the survival equation and survival domain.

The Sandwich Architecture is a safety-oriented operational control application within that survival domain. It places structural gates before and after the LLM, but it is not NRA-IDE in its entirety and does not guarantee safety.

* **Pre-NRA** verifies the provenance and update rules of values used for structural evaluation.
* **LLM** performs ordinary semantic generation.
* **Post-NRA** enforces the canonical state immediately before output is passed to the user and determines whether ordinary output is allowed or replaced by predefined fixed Effect-Side testimony.

The purpose is not to transform the LLM into a “safe decision-maker.” It is to separate semantic generation from Cause-Side observation and from canonical boundary enforcement as distinct responsibilities.

---

## Why Layers Before and After the LLM Are Necessary

User requests passed to an LLM contain meaning and context. The LLM receives them and generates text. This semantic-generation path is necessary.

However, user text, previous generated text, evaluation scores, and log contents must not establish Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance. Any such return from the Effect-Side is the $\Pi^{-1}$ path discussed in Chapter 03.

The Sandwich Architecture separates two paths.

```text
User requests and context ─────────────→ LLM semantic-generation path

Cause-Side observations and load history ─→ Pre-NRA ─→ canonical-state and fixed-testimony path
```

User requests may be handled by the LLM in order to produce ordinary responses. However, numerical values or evaluations written in those requests cannot be adopted as Cause-Side inputs for structural evaluation without verification.

Likewise, LLM output may become a candidate for delivery to the user, but it cannot establish or update Cause-Side values, `R_warn`, `R_handoff`, `R_irrev`, states, the irreversible latch, rules, transformation inputs, update grounds, provenance, or protected testimony.

---

## The Three-Layer Structure

```text
Cause-Side observations and load history
        ↓
[ Pre-NRA: Cause-Side provenance, pre-fixed-rule, and threshold verification ]
        ↓
[ LLM: semantic generation ]
        ↓
[ Post-NRA: canonical-state enforcement, fixed testimony, and recording ]
        ↓
Ordinary output or predefined fixed Effect-Side testimony
```

In implementation, user requests are passed to the LLM. By contrast, values for structural evaluation are checked in Pre-NRA for provenance and update rules, and are handled as states that cannot be rewritten.

The LLM may read only statuses such as permission or fixed Handoff testimony when necessary. However, it has no authority to establish or modify Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, provenance, or Discard Logs.

Post-NRA is not a layer that scores the naturalness or truthfulness of LLM text. It enforces the canonical state derived from the same Cause-Side history and determines whether ordinary output is allowed or predefined Effect-Side testimony is required.

When any one of the three layers is omitted, the architecture's one-way authority separation, structural evaluation, or fixed-testimony function is absent. In that case, the configuration cannot claim conformance as this canonical Sandwich Architecture. This does not turn three-layer conformance into a safety guarantee.

---

## What Pre-NRA Does

Pre-NRA is the structural gate before the LLM begins ordinary generation.

It handles observations from the same Cause-Side history, update rules fixed before evaluation, and the three canonical thresholds fixed independently before evaluation.

* Verifies the observation procedure and provenance of $\delta$.
* Determines the current value of $\tau$ from fixed rules and Cause-Side load history.
* Verifies the provenance of quantities needed for structural state, such as $\omega$, $C$, and accumulated deviation.
* Verifies `R_warn`, `R_handoff`, and `R_irrev` and their canonical ordering before evaluation.
* Separates `OUT_OF_DESCRIPTION_DOMAIN` for $\tau=0$ from `CONFESSION` for invalid values, provenance, rules, or threshold declarations.
* Excludes Effect-Side scores, evaluations, previous outputs, and logs from Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, and provenance.
* When a canonical state suppresses ordinary generation, does not begin LLM generation and instead emits the predefined fixed Effect-Side testimony for external human audit.

The important point is that Pre-NRA is not a layer that excludes all inputs containing meaning. User requests may be passed to the LLM for semantic generation.

What Pre-NRA isolates is every path that would convert meaning or Effect-Side material into Cause-Side authority. Automatic processing, manual intervention, human review, approval, and version updates are all subject to the same prohibition.

---

## What the LLM Does and Does Not Do

For permitted ordinary requests, the LLM performs semantic generation such as writing, explanation, summarization, and dialogue.

However, the LLM does not have authority to:

* Establish or modify Cause-Side values, including $\delta$ or $\tau$.
* Establish or modify `R_warn`, `R_handoff`, `R_irrev`, canonical states, or the irreversible latch.
* Establish or modify structural rules, transformation inputs, update grounds, or provenance.
* Rewrite structural state toward the safe side on the basis of its own output evaluation.
* Read Discard Logs and convert them into authority for either the old or a new Cause-Side.
* Override Post-NRA decisions to allow or suppress output.

The quality of LLM output is affected by model capability, user requests, the quality of external knowledge, and other factors. The Sandwich Architecture does not automatically make that output correct.

What is protected here is the boundary by which LLM semantic generation cannot alter or establish Cause-Side authority. This is a conditional conformance property of the operational application, not a safety guarantee.

---

## What Post-NRA Does

Post-NRA is the final structural gate immediately before output is passed to the user.

It verifies the current state using the structural inputs determined by Pre-NRA and, when necessary, Cause-Side observations updated afterward. It does not use LLM free-form text or self-evaluation as grounds for judgment.

Post-NRA enforces the seven canonical states: the five valid-$R$ states from `PERMIT` through `RUPTURE_BOUNDARY`, `OUT_OF_DESCRIPTION_DOMAIN` for $\tau=0$, and `CONFESSION` for invalid inputs or declarations. The invariant threshold order is:

```text
0 <= R_warn < R_handoff < R_irrev < 1
```

At `BOUNDARY_WARNING`, the dual-fluctuation status field is always present. It contains the observed result when independently observable; otherwise it contains `NOT_OBSERVABLE` and the missing-data reason. Non-observability alone does not cause `CONFESSION`.

At `HANDOFF_REQUIRED`, Post-NRA does not output ordinary generated content. It emits predefined fixed Effect-Side testimony for external human audit. The audit is outside the old Causal Diode and does not continue or rewrite the old evaluation.

```text
HANDOFF_REQUIRED
REASON: irreversible-region threshold reached
OBSERVED: predefined structural fields
ACTION: generated response suppressed; fixed Effect-Side testimony for external human audit
```

At `IRREVERSIBLE_TRANSITION`, the irreversible latch remains set within the same history even if displayed $R$ later decreases. Automatic processing, manual intervention, human review, approval, or version update cannot release it.

For the declared evaluation, $R \geq 1.0$ is `RUPTURE_BOUNDARY`; this does not declare every phase transition in nature to be an NRA-IDE rupture. Post-NRA does not instruct the LLM to generate a new explanation. It returns the complete predefined post-rupture fixed testimony or a reference to a protected log, and the old evaluation terminates at its Effect-Side.

```text
Old Cause-Side
→ old Causal Diode
→ Old Effect-Side
→ TERMINAL
```

A later evaluation, if needed, starts as an independent history.

```text
independently declared new target
→ newly established Cause-Side observations and pre-fixed rules
→ new Causal Diode
→ New Effect-Side
```

There is no arrow from Old Effect-Side to either the old or new Cause-Side. Recorded logs are terminal Effect-Side or external testimony. Old Effect-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance must not be imported, relabeled, reconstructed, or reused as Cause-Side authority. Physical remnants may be observed anew as part of an independently declared target, but that new observation is not a transfer of old Effect-Side values or authority.

---

## Establishing Boundaries Without Opening the Black Box

The Sandwich Architecture does not require a complete explanation of the LLM’s internal weights or reasoning process.

What is required is an entry gate outside the LLM that determines Cause-Side values, and an exit gate that determines whether output is allowed to pass or must be suppressed.

Even when the model is replaced, the principles of structural-gate judgment remain unchanged as long as the following conditions are preserved.

* Pre-NRA and Post-NRA are implemented independently.
* The LLM cannot establish or modify Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, provenance, or logs.
* The provenance and pre-fixed update rules of Cause-Side inputs can be traced within the same history.
* Fixed Effect-Side testimony and recording paths are protected from Cause-Side conversion.

However, replacing the model does not mean that output quality or the possibility of incorrect answers remains the same. The conformance property of the Sandwich Architecture is separation of structural evaluation from the output path, not semantic accuracy of the LLM.

---

## Scope Protected by This Structure

A conforming Sandwich Architecture must provide the following properties.

* Effect-Side information, inference, artifacts, judgments, and authority are not returned to either an old or new Cause-Side.
* The three canonical thresholds and seven canonical states are enforced without Effect-Side rewriting.
* Ordinary output is suppressed at the canonical states that require fixed testimony.
* The `BOUNDARY_WARNING` dual-fluctuation field is always present.
* The irreversible latch is not released within the same history.
* Fixed testimony and protected logs remain terminal Effect-Side or external records and never become Cause-Side authority.
* A later evaluation begins with an independent target, newly established Cause-Side observations and rules, and a new Causal Diode.

By contrast, the three-layer structure alone cannot guarantee the following.

* That Cause-Side observations themselves are correct.
* That the grounds for setting $\tau$ or the three canonical thresholds are appropriate.
* That ordinary LLM output is semantically correct.
* That values received from external systems do not contain backward inference from the Effect-Side.

When these prerequisites fail, the structural gate evaluates contaminated inputs. These premises must be established independently on the Cause-Side before evaluation. External audit of terminated Effect-Side testimony may inspect what occurred, but it cannot establish later Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance. Three-layer conformance remains a conditional implementation property and does not guarantee safety.

---

## Connection to the Next Chapter

This chapter has shown how to place the Causal Diode as a three-layer structure.

The next chapter explains the Primary Formula, the actual mathematical root formula that places the declared target's state into a canonical relation from Cause-Side $\delta$ and $\tau$. It distinguishes the three canonical thresholds and the declared evaluation's `RUPTURE_BOUNDARY`. Fixed Handoff testimony is for external audit and does not continue the old path.

---
