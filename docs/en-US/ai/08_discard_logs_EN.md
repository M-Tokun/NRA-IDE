# 08 Discard Logs — Preserving Testimony Without Returning It to Computation

<!-- FILE: 08_discard_logs_EN.md -->

---

## Logs Are Terminal Effect-Side Records, but External Human Audit Is Not Prevented

As confirmed in Chapter 06, NRA-IDE distinguishes not only the names of values, but also their provenance and update paths. The same applies to Discard Logs.

Here, **write-only** means that recorded logs remain terminal Effect-Side or external records and never return to either an old or a new Cause-Side. It does not mean that logs cannot be read. Human auditors may refer to them only outside the terminated diode path in order to verify why handoff, irreversible transition, or rupture occurred.

The following type of feedback is prohibited.

```text
Old Discard Log → inference from effects → attempted Cause-Side update → BLOCKED
```

Any attempt to turn an old Discard Log into a Cause-Side value, any of the three canonical thresholds, a state, an irreversible latch, a rule, a transformation input, an update ground, or provenance is the $\Pi^{-1}$ path discussed in Chapter 03. It is prohibited whether automatic, manual, human-reviewed, authorized, or versioned.

The following two must be distinguished.

* **Structural-evaluation execution system:** Never reintroduces logs into an old or a new Cause-Side.
* **External human audit:** May read logs as testimony outside the terminated path, but cannot convert their contents into future rule grounds, Cause-Side material, transformation inputs, or provenance.

Human reading does not create a reverse edge. Manual review, approval, or version control does not create an exception.

---

## What Is Discarded Is Residual That Is Not Adopted into the Next Transition

In discrete phase transitions within NRA-IDE, the following process may be used.

This section describes an intra-history calculation of the IDE dynamics engine. It does not describe passage from an old Effect-Side to a new Cause-Side and grants no authority across Causal Diodes.

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

This process blocks the path by which residuals not adopted into the next transition re-enter the next phase as hidden state within that calculation history. Recording residuals does not itself create $\Pi^{-1}$; returning a Discard Log across the terminal Effect-Side boundary would create the prohibited connection.

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

## The Local Computational Invariant and Its Limits

Not carrying residual into the next discrete transition is an explicit choice in the computational structure. However, this process alone does not make the entire computation error-free.

The local computational invariant is that **residual defined by this rule as not adopted is not reintroduced as input to the next state transition within that calculation history**. This is not a safety guarantee and does not describe authority transfer between histories.

The following are not guaranteed.

* That measurement instruments or Cause-Side observations are correct
* That every error related to floating-point arithmetic disappears
* That no numerical problems exist elsewhere in the implementation beyond `math.floor`
* That the discretization rule itself is appropriate for the target domain
* That ordinary LLM output is semantically correct

Therefore, discarding does not mean “discarding precision,” nor does it mean eliminating error in general. It makes explicit, as a rule fixed in advance, what is retained and what is not retained in the next state transition.

[Escapement Demonstration — An Example Showing Residual Export at the Contact Point](../figures/08_Escapement_ContactPoint_EN.html)

---

## Discard Logs Preserve the Grounds for Suppression and Terminal Processing

Within the known numeric progression distinguished in Chapters 05 and 07, this section handles three states in which new ordinary output is suppressed.

* **`HANDOFF_REQUIRED`:** $R_{\mathrm{handoff}} \le R < R_{irrev}$; fixed Handoff testimony presented for external human audit
* **`IRREVERSIBLE_TRANSITION`:** $R_{irrev} \le R < 1$; irreversible latch and continuing structural testimony
* **`RUPTURE_BOUNDARY`:** $R \ge 1$; final fixed testimony for the declared evaluation

`CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` also suppress affected ordinary output through Fail-Closed processing. They are input exceptions rather than states in this numeric progression and are recorded separately in `INPUT_EXCEPTION_LOG`.

$R=1$ is the `RUPTURE_BOUNDARY` of the declared NRA-IDE evaluation. This classification does not declare every natural phase transition to be an NRA-IDE rupture.

Logs are necessary to avoid conflating these three states. A record format defined in advance retains at least the following information.

```text
EVENT: HANDOFF_REQUIRED, IRREVERSIBLE_TRANSITION, or RUPTURE_BOUNDARY
REASON: triggered handoff condition or structural boundary
OBSERVED: δ, τ, R, ω, and required provenance identifiers
THRESHOLDS: R_warn, R_handoff, R_irrev
DISCARD: entropy_export (only when a relevant discrete transition exists)
ACTION: ordinary generation suppressed; fixed Handoff testimony for external human audit; continuing structural testimony; or final fixed testimony
RULE_VERSION: version of the observation, update, and handoff rules used
```

For example, handoff at `R_handoff` is recorded as follows.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: δ, τ, R, ω
THRESHOLD: R_handoff
ACTION: generated response suppressed; fixed Effect-Side testimony presented for external human audit
```

For fixed Handoff testimony and final fixed testimony, the LLM is not asked to generate new free-form text in order to explain the reason for stopping. Only predefined fixed Effect-Side testimony or a protected-log reference is returned.

```text
RUPTURE_BOUNDARY
REASON: structural boundary reached
ACTION: final fixed testimony; old evaluation history terminated at Effect-Side
```

This makes it possible to distinguish, within the record itself, handoff, irreversible transition, and final fixed testimony at the rupture boundary.

---

## A Record Is Terminal Testimony, Not Cause-Side Material for Any Evaluation

Discard Logs retain not only “what was output,” but also “what was not adopted into structural computation and under which conditions ordinary generation was suppressed.”

For a record to function as testimony, it requires at least the following operating conditions.

* It is append-only.
* Tampering after recording can be detected.
* It can be associated with the version of the observation, update, and handoff rules.
* It can be audited by humans.
* Neither automatic nor manual handling reintroduces log content as a Cause-Side value, any of the three canonical thresholds, a state, an irreversible latch, a rule, a transformation input, an update ground, or provenance.

Cause-Side load history that dynamically changes $\tau$ is an input to the $\tau$ update rule defined at design time. It must be distinguished from a Discard Log that records previous results. A Discard Log must not be treated as a substitute for Cause-Side history.

The old path terminates at its Effect-Side. If a later evaluation is needed, it begins from an independently declared target, newly established Cause-Side observations and rules, and a new Causal Diode. Physical remnants may be newly observed as part of that target, but no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in either an old or a new Cause-Side.

Discarding and recording are not contradictory.

```text
Do not return it to computation.
Retain it for external human audit.
```

Making these two conditions hold simultaneously is the role of the Discard Log.

---

## Connection to the Next Chapter

Discard Logs preserve testimony of structural evaluation. However, issues such as input provenance, the basis for setting $\tau$, log protection, and required authority separation cannot be prevented by logs alone. In systems that include an LLM, this also applies to omission of the configured Pre-NRA, LLM, and Post-NRA layers. Conformance depends on canonical behavior, evidence, and tests, not on logs or a layer count alone.

The next chapter examines pathways through which NRA-IDE may be misused, whether accidentally or intentionally, and the operational responsibilities borne by humans.

---
