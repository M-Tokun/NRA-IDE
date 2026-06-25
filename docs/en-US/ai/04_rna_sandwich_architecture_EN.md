# 04 Sandwich Architecture — A Three-Layer Design That Isolates the LLM with Structural Gates Before and After It

<!-- FILE: 04_rna_sandwich_architecture_EN.md -->

---

## Do Not Make the LLM Solely Responsible for Structural Safety

The Causal Diode discussed in Chapter 03 is the principle that blocks $\Pi^{-1}$, the path through which Effect-Side values return to Cause-Side structural inputs.

An LLM is the layer responsible for reading user requests, handling context, and generating natural language. This is the role of the LLM. The semantic correctness of outputs, the provenance of input values, and the location of structural boundaries cannot be guaranteed by the LLM alone.

For this reason, NRA-IDE places structural gates before and after the LLM.

* **Pre-NRA** verifies the provenance and update rules of values used for structural evaluation.
* **LLM** performs ordinary semantic generation.
* **Post-NRA** verifies the structural state immediately before output is passed to the user and determines whether ordinary output is allowed to pass or must be replaced by a fixed-format notification.

The purpose is not to transform the LLM into a “safe decision-maker.” It is to separate semantic generation from the judgment and delegation of structural boundaries as distinct responsibilities.

---

## Why Layers Before and After the LLM Are Necessary

User requests passed to an LLM contain meaning and context. The LLM receives them and generates text. This semantic-generation path is necessary.

However, user text, previous generated text, evaluation scores, and log contents must not become grounds for determining $\delta$ or $\tau$ directly. When Effect-Side content updates the inputs used for structural evaluation, the $\Pi^{-1}$ path discussed in Chapter 03 arises.

The Sandwich Architecture separates two paths.

```text
User requests and context ─────────────→ LLM semantic-generation path

Cause-Side observations and load history ─→ Pre-NRA ─→ structural-evaluation and delegation path
```

User requests may be handled by the LLM in order to produce ordinary responses. However, numerical values or evaluations written in those requests cannot be adopted as Cause-Side inputs for structural evaluation without verification.

Likewise, LLM output may become a candidate for delivery to the user, but it cannot become grounds for updating $\delta$, $\tau$, delegation points, or logs.

---

## The Three-Layer Structure

```text
Cause-Side observations and load history
        ↓
[ Pre-NRA: provenance verification and determination of structural inputs ]
        ↓
[ LLM: semantic generation ]
        ↓
[ Post-NRA: final structural verification, passage/suppression, and recording ]
        ↓
Ordinary output or a fixed-format handoff notification
```

In implementation, user requests are passed to the LLM. By contrast, values for structural evaluation are checked in Pre-NRA for provenance and update rules, and are handled as states that cannot be rewritten.

The LLM may read only statuses such as permission or handoff when necessary. However, it has no authority to modify $\delta$, $\tau$, delegation points, Discard Logs, or the structural inputs themselves.

Post-NRA is not a layer that scores the naturalness or truthfulness of LLM text. It verifies only the latest structural state derived from the Cause-Side and determines whether ordinary output is allowed to pass to the user or must be suppressed.

When any one of the three layers is omitted, the Causal Diode, structural evaluation, or output-blocking function is absent. In that case, the configuration cannot be described as providing NRA-IDE structural guarantees.

---

## What Pre-NRA Does

Pre-NRA is the structural gate before the LLM begins ordinary generation.

It handles Cause-Side observations obtained from the target system and update rules defined at design time.

* Verifies the observation procedure and provenance of $\delta$.
* Determines the current value of $\tau$ from fixed rules and Cause-Side load history.
* Verifies the provenance of quantities needed for structural state, such as $\omega$, $C$, and accumulated deviation.
* Excludes Effect-Side scores, evaluations, previous outputs, and logs from the grounds for updating structural inputs.
* When a domain-specific point of approach to an irreversible regime has been reached, does not begin ordinary generation and instead moves to handoff processing.

The important point is that Pre-NRA is not a layer that excludes all inputs containing meaning. User requests may be passed to the LLM for semantic generation.

What Pre-NRA isolates is the path that uses meaning or Effect-Side values as Cause-Side inputs for structural evaluation.

---

## What the LLM Does and Does Not Do

For permitted ordinary requests, the LLM performs semantic generation such as writing, explanation, summarization, and dialogue.

However, the LLM does not have authority to:

* Modify $\delta$ or $\tau$.
* Modify structural boundaries or delegation points.
* Rewrite structural state toward the safe side on the basis of its own output evaluation.
* Read Discard Logs and use them as inputs for the next structural evaluation.
* Override Post-NRA decisions to allow or suppress output.

The quality of LLM output is affected by model capability, user requests, the quality of external knowledge, and other factors. The Sandwich Architecture does not automatically make that output correct.

What is protected here is the boundary by which LLM semantic generation cannot alter the Cause-Side of the structural safety gate.

---

## What Post-NRA Does

Post-NRA is the final structural gate immediately before output is passed to the user.

It verifies the current state using the structural inputs determined by Pre-NRA and, when necessary, Cause-Side observations updated afterward. It does not use LLM free-form text or self-evaluation as grounds for judgment.

The condition for suppressing ordinary output is a domain-specific **point of approach to an irreversible regime**. This is a delegation point for transferring judgment to humans, and it is not identical to the phase-transition boundary of $R = 1.0$.

When the delegation point is reached, Post-NRA does not output ordinary generated content. Instead, it uses a predefined fixed-format notification to indicate only the structural state and the need for human judgment.

```text
HANDOFF_REQUIRED
REASON: irreversible-region threshold reached
OBSERVED: predefined structural fields
ACTION: generated response suppressed; human review required
```

After $R = 1.0$ has been reached or exceeded, Post-NRA does not instruct the LLM to generate a new explanation. It returns only a predefined minimal FAIL-CLOSED indicator or a reference to a protected log, and hands the matter over to humans.

Post-NRA also records structural states. Recorded logs are preserved as testimony, but are not returned as inputs to the next structural evaluation.

---

## Establishing Boundaries Without Opening the Black Box

The Sandwich Architecture does not require a complete explanation of the LLM’s internal weights or reasoning process.

What is required is an entry gate outside the LLM that determines Cause-Side values, and an exit gate that determines whether output is allowed to pass or must be suppressed.

Even when the model is replaced, the principles of structural-gate judgment remain unchanged as long as the following conditions are preserved.

* Pre-NRA and Post-NRA are implemented independently.
* The LLM cannot modify structural inputs, delegation points, or logs.
* The provenance and update rules of structural inputs can be traced.
* Fixed-format handoff notifications and recording paths are protected.

However, replacing the model does not mean that output quality or the possibility of incorrect answers remains the same. What the Sandwich Architecture guarantees is not the semantic accuracy of the LLM, but the separation of structural evaluation from the output path.

---

## Scope Protected by This Structure

The Sandwich Architecture guarantees the following.

* Effect-Side values are not returned to Cause-Side structural inputs.
* Ordinary output is suppressed at a domain-specific delegation point and replaced with a fixed-format notification.
* The grounds for delegation and stopping are preserved as logs separated from computational inputs.

By contrast, the three-layer structure alone cannot guarantee the following.

* That Cause-Side observations themselves are correct.
* That the grounds for setting $\tau$ or delegation points are appropriate.
* That ordinary LLM output is semantically correct.
* That values received from external systems do not contain backward inference from the Effect-Side.

When these prerequisites fail, the structural gate evaluates contaminated inputs. Value provenance, grounds for settings, and log protection must be verified in both implementation and operation.

---

## Connection to the Next Chapter

This chapter has shown how to place the Causal Diode as a three-layer structure.

The next chapter explains how structural state is read from Cause-Side $\delta$ and $\tau$, and how ordinary output, caution, and delegation are distinguished. $R = 1.0$ is a phase-transition boundary, while the ordinary delegation point is determined by domain before that boundary is reached.

---
