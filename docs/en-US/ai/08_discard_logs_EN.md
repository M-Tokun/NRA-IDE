# 08 Discard Logs — Preserving Testimony Without Returning It to Computation

<!-- FILE: 08_discard_logs_EN.md -->

---

## Logs Are Write-Only, but Human Audit Is Not Prevented

As confirmed in Chapter 06, NRA-IDE distinguishes not only the names of values, but also their provenance and update paths. The same applies to Discard Logs.

Here, **write-only** means that recorded logs are not automatically returned to the next structural evaluation. It does not mean that logs cannot be read. Human auditors may refer to the records in order to verify why stopping or handoff occurred.

The following type of feedback is prohibited.

```text
Previous log → inference from effects → automatic update of δ, τ, or Rop → next structural evaluation
```

In this path, the result of the previous evaluation rewrites the Cause-Side input of the next evaluation. This is the $\Pi^{-1}$ path discussed in Chapter 03.

The following two must be distinguished.

* **Structural-evaluation execution system:** Does not reintroduce logs as grounds for updating $\delta$, $\tau$, or `Rop`.
* **Human audit and design review:** May read logs as testimony and consider design changes through separate verification, approval, and version-control procedures.

Humans reviewing logs and logs automatically governing the next structural computation are not the same thing.

---

## What Is Discarded Is Residual That Is Not Adopted into the Next Transition

In discrete phase transitions within NRA-IDE, the following process may be used.

```python
raw_next_phase = prev_state.phase + prev_state.omega

next_phase_int = math.floor(raw_next_phase)

entropy_export = raw_next_phase - next_phase_int
```

`raw_next_phase` contains an integer part adopted as the next phase and a fractional part that is not adopted. Only `next_phase_int` is passed to the next discrete transition, while the fractional part is recorded as `entropy_export`.

The important point is that this does **not** discard all information or all error.

What is handled here is only the residual that, under a discretization rule defined in advance, is not carried forward into the next state transition.

```text
Value adopted into the next transition: next_phase_int
Residual not adopted into the next transition: entropy_export
```

This process blocks the path by which residuals not adopted into the next transition re-enter the next phase as hidden state. Recording residuals does not itself create $\Pi^{-1}$ as long as they are not returned as computational inputs.

---

## `entropy_export` Is Not a Measurement of Thermodynamic Entropy

`entropy_export` is an **implementation-level record field** indicating residual that was not adopted into the next transition during discretization.

It does not mean a directly measured value of thermodynamic entropy or physical heat itself. Therefore, when this document set uses $S$ as the reciprocal of remaining structural margin, `entropy_export` must not be represented by the same symbol.

```text
S = 1 / (τ · (1 − R)) = 1 / (τ − δ)
```

* **$S$:** Structural sensitivity as the reciprocal of remaining structural margin
* **`entropy_export`:** A record field for residual not adopted in a discrete transition

Their roles and generation paths are different.

---

## What Residual Export Guarantees and Does Not Guarantee

Not carrying residual into the next discrete transition is an explicit choice in the computational structure. However, this process alone does not make the entire computation error-free.

The scope of the guarantee is that **residual defined by this rule as not adopted is not reintroduced as input to the next state transition**.

The following are not guaranteed.

* That measurement instruments or Cause-Side observations are correct
* That every error related to floating-point arithmetic disappears
* That no numerical problems exist elsewhere in the implementation beyond `math.floor`
* That the discretization rule itself is appropriate for the target domain
* That ordinary LLM output is semantically correct

Therefore, discarding does not mean “discarding precision,” nor does it mean eliminating error in general. It makes explicit, as a rule fixed in advance, what is retained and what is not retained in the next state transition.

[Escapement Demonstration — An Example Showing Residual Export at the Contact Point](../figures/08_Escapement_ContactPoint_JP.html)

---

## Discard Logs Preserve the Grounds for Handoff and Terminal Processing

As distinguished in Chapters 05 and 07, there are two states in which ordinary output is suppressed.

* **Reaching `Rop`:** A domain-specific handoff point before the phase-transition boundary
* **$R \geq 1.0$:** Reaching or exceeding the phase-transition boundary at which structural margin is lost

Logs are necessary to avoid conflating these two conditions. A record format defined in advance retains at least the following information.

```text
EVENT: HANDOFF_REQUIRED or FAIL_CLOSED
REASON: triggered handoff condition or structural boundary
OBSERVED: δ, τ, R, ω, and required provenance identifiers
THRESHOLD: Rop (handoff only)
DISCARD: entropy_export (only when a relevant discrete transition exists)
ACTION: ordinary generation suppressed, human handoff, or minimal FAIL-CLOSED processing
RULE_VERSION: version of the observation, update, and handoff rules used
```

For example, handoff at `Rop` is recorded as follows.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: δ, τ, R, ω
THRESHOLD: Rop
ACTION: generated response suppressed; human review required
```

When $R \geq 1.0$, the LLM is not asked to generate new free-form text in order to explain the reason for stopping. Only a predefined minimal indicator or a reference to a protected log is returned.

```text
FAIL_CLOSED
REASON: structural boundary reached
ACTION: no further generated response; human handoff required
```

This makes it possible to distinguish, within the record itself, the suppression of ordinary generation at the handoff point from minimal FAIL-CLOSED processing at the terminal boundary.

---

## A Record Is Testimony, Not the Cause of the Next Evaluation

Discard Logs retain not only “what was output,” but also “what was not adopted into structural computation and under which conditions ordinary generation was suppressed.”

For a record to function as testimony, it requires at least the following operating conditions.

* It is append-only.
* Tampering after recording can be detected.
* It can be associated with the version of the observation, update, and handoff rules.
* It can be audited by humans.
* The structural-evaluation execution system does not automatically reintroduce log content into updates of the next $\delta$, $\tau$, or `Rop`.

Cause-Side load history that dynamically changes $\tau$ is an input to the $\tau$ update rule defined at design time. It must be distinguished from a Discard Log that records previous results. A Discard Log must not be treated as a substitute for Cause-Side history.

Discarding and recording are not contradictory.

```text
Do not return it to computation.
Retain it for human audit.
```

Making these two conditions hold simultaneously is the role of the Discard Log.

---

## Connection to the Next Chapter

Discard Logs preserve testimony of structural evaluation. However, issues such as input provenance, the basis for setting $\tau$, log protection, and omission of the three-layer structure cannot be prevented by logs alone.

The next chapter examines pathways through which NRA-IDE may be misused, whether accidentally or intentionally, and the operational responsibilities borne by humans.

---
