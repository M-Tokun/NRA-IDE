# 01 Paradigm Shift — Structural Transformation Brought by NRA-IDE

<!-- FILE: 01_paradigm_shift_EN.md -->

---

> [!IMPORTANT]
> There is exactly one Nomological Ring Axiom: “Existence is Generation.” No second or subsequent axiom exists. The Primary Formula and the Secondary / Dual-Fluctuation Formula are the two canonical IDE calculation systems, not axioms.
>
> This chapter is an explanatory interpretation subordinate to `theory/AXIOMS.md`, `theory/axioms.json`, and the other higher-precedence canonical documents. It is not a safety guarantee, measurement result, domain validation, or independent evidence of conformance.

## What Is Being Transformed?

Many safety practices necessarily learn from completed incidents: an outcome is observed, its causes are investigated, and countermeasures are introduced afterward. Post-incident investigation remains valuable, but relying on it alone is structurally reactive. Harm has already occurred before the evidence becomes available.

NRA-IDE directs attention to the pre-incident path. It evaluates the present structural trajectory from Cause-Side observations or transformations fixed before evaluation:

- how accumulated deviation $\delta$ is developing;
- how absorption thickness $\tau$ is being consumed or otherwise changing under a declared domain rule;
- how the Primary Formula value $R=\delta/\tau$ for the declared target moves through warning, Handoff, and irreversible thresholds;
- which observations, units, provenance, uncertainties, and rules are missing.

The purpose is not to promise that an accident cannot occur. This is a safety-oriented operational application of the survival domain: it identifies and responds to a developing path before complete rupture, and especially before entry into an irreversible regime. It does not reduce the Primary Formula to a safety indicator, local instrument, or mere boundary-approach rate.

---

## The Survival Domain and Its Safety-Oriented Subdomain

NRA-IDE itself is the survival equation and survival domain, implemented through IDE as a computational-method and dynamics engine. The safety domain discussed in this chapter is the subdomain that applies the survival domain to accident prevention, operation, and control. It is not the whole survival domain and does not guarantee safety.

Survival does not mean permanent preservation of the same form. It includes dynamic persistence in which fluctuation, phase transition, rupture, selection, disappearance, and reconstruction generate new structures and histories.

Within the safety-oriented subdomain, safety is not a certificate attached to an output after evaluation. It concerns observing and responding to a declared structural path while intervention remains possible, without redefining the wider survival domain as static preservation.

This does not mean that every state with $R<1$ permits autonomous operation. The canonical states distinguish progressively stronger constraints:

```text
PERMIT
→ BOUNDARY_WARNING
→ HANDOFF_REQUIRED
→ IRREVERSIBLE_TRANSITION
→ RUPTURE_BOUNDARY
```

`CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` handle unsupported or undefined evaluations separately.

The three canonical operating thresholds have the invariant order:

```text
0 <= R_warn < R_handoff < R_irrev < 1
```

- At `R_warn`, boundary approach is disclosed.
- At `R_handoff`, affected new autonomous judgment and operation stop, and predefined fixed Effect-Side testimony is presented for external human audit.
- At `R_irrev`, irreversible transition is latched. Within the same history, later $R$ decrease, automatic processing, manual intervention, human review, approval, or version update cannot release the latch.
- At $R\ge1$, the system reports `RUPTURE_BOUNDARY` and switches to post-rupture fixed testimony.

Avoidance therefore has meaning before the accident result: observe the path, disclose increasing risk, and emit fixed Handoff testimony before the irreversible threshold rather than waiting for rupture and then reconstructing causes from the outcome. External audit does not continue or rewrite the old causal path.

---

## Observation Can Become Clearer While Quantification Becomes Harder

As a physical structure approaches a severe boundary, observable signs may become more pronounced while reliable quantification becomes harder. Sensors may saturate, uncertainty may widen, the applicable model may weaken, and the remaining observation time may shrink. A strong physical indication does not justify invented numerical precision.

NRA-IDE therefore separates:

- a physically observed Cause-Side sign;
- its measured value and unit;
- uncertainty and instrument limits;
- a valid domain transformation rule;
- the resulting canonical state;
- information that remains unavailable.

When the required structure cannot be supported, the system returns `CONFESSION`. When $\tau=0$, canonical $R$ is undefined and the state is `OUT_OF_DESCRIPTION_DOMAIN`. Neither case may be filled by analogy, semantic similarity, or Effect-Side output.

At `BOUNDARY_WARNING`, the double-fluctuation result must be reported when observable, or `NOT_OBSERVABLE` with the missing reason. This preserves physical testimony without pretending to possess exact values that were not measured.

---

## The Structural Problem in Result-Centered Safety

Some output-filtering systems inspect a generated result and block it when the content is judged unacceptable. This is an Effect-Side intervention applied after generation. It can be useful, but it does not by itself establish the Cause-Side structural state that produced the result.

A similar limitation appears when a proxy score is treated as both evidence and optimization objective. Once a score is optimized, the indicator and the original safety purpose may diverge.

Semantic review, output filtering, and incident investigation may occur outside a terminated Causal Diode. They do not continue the old evaluation and must not establish or rewrite Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance. This prohibition applies to automatic processing, manual intervention, human review, approval, and version updates.

```text
Effect-Side result
→ BLOCKED from old Cause-Side
→ BLOCKED from new Cause-Side
```

---

## Three Design Decisions

### 1. Observe the path before the outcome

Do not wait for rupture to be the first decisive evidence. Track declared Cause-Side variables, their provenance, their trajectory, and the applicable thresholds before the event.

### 2. Do not make Effect-Side meaning the structural authority

Semantic interpretation, translation, and output review may occur on the Effect-Side. They must not determine or update Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance. A transformation rule fixed before evaluation may derive structural variables only from declared Cause-Side observations; it cannot import, relabel, reconstruct, or reuse old Effect-Side material as its input or authority.

### 3. Emit fixed Handoff testimony before irreversible transition

At `R_handoff`, affected autonomous judgment and operation stop and predefined fixed Effect-Side testimony is presented for external human audit. The audit is outside the old Causal Diode and does not create a reverse edge to either the old or a new Cause-Side. This occurs before `R_irrev`; it is not the same as the declared evaluation's `RUPTURE_BOUNDARY` at $R=1$.

These are design decisions under the canonical state model, not additional axioms.

---

## Fail-Closed Does Not Mean Silence

The Fail-Closed operational principle suppresses affected new autonomous judgment and operation for:

- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`
- `OUT_OF_DESCRIPTION_DOMAIN`

It does not suppress required fixed structural testimony or logging. `PERMIT` is not Fail-Closed. `BOUNDARY_WARNING` alone does not require complete output suppression unless a pre-fixed domain rule requires it.

Known numeric progression is recorded in `STRUCTURAL_DISCLOSURE_LOG`. `CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` are recorded separately in `INPUT_EXCEPTION_LOG`.

These records are terminal Effect-Side or external testimony. External human audit may inspect them, but automatic processing, manual review, approval, or version updates must not convert them into Cause-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance.

---

## When an LLM Is Included

For a system that includes an LLM, Cause-Side observation, deterministic IDE evaluation, Effect-Side generation, and delivery enforcement must remain separated. A typical arrangement is:

```text
Cause-Side observation
        ↓
canonical NRA-IDE evaluator
        ↓
input gate
        ↓
LLM CORE
        ↓
output gate
        ↓
canonical-state-controlled Effect-Side output
```

Ordinary explanation is permitted only in states and fields allowed by the pre-fixed canonical behavior. Fixed Handoff or final testimony is not supplemented by newly generated free-form explanation.

This sandwich is a configuration for systems containing an LLM; it is not a claim that every NRA-IDE evaluation requires an LLM or exactly three software components.

Omitting a displayed layer does not automatically prove nonconformance, and drawing the layers does not prove conformance. Conformance depends on authority separation, canonical behavior, evidence, and applicable tests. This is a conditional implementation property, not a safety guarantee.

---

## What the Paradigm Shift Claims—and Does Not Claim

The shift is from result-only reaction toward pre-boundary structural observation and intervention:

```text
incident result → retrospective cause reconstruction
```

is supplemented by:

```text
Cause-Side trajectory
→ boundary warning
→ pre-irreversible fixed Handoff testimony
→ fixed structural testimony
→ Old Effect-Side TERMINAL
```

The old causal path is complete and one-way:

```text
Old Cause-Side
→ old Causal Diode
→ Old Effect-Side
→ TERMINAL
```

A later evaluation, if needed, begins as an independent history:

```text
independently declared new target
→ newly established Cause-Side observations and pre-fixed rules
→ new Causal Diode
→ New Effect-Side
```

There is no arrow from Old Effect-Side to either the old or new Cause-Side. Old Effect-Side values, canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance must not be imported, relabeled, reconstructed, or reused as Cause-Side authority. Physical remnants may be observed anew as part of an independently declared target, but that observation is not a transfer of old Effect-Side values or authority.

NRA-IDE does not guarantee that every risk will be observed, quantified, or avoided. It does not replace qualified external human audit, independent Cause-Side domain validation, measurement science, professional standards, or applicable law. Its safety-oriented contribution is to make the pre-rupture path, uncertainty, missing information, and the declared evaluation's `RUPTURE_BOUNDARY` explicit before treating the accident result as the first usable signal. This partial application does not replace the wider survival equation or survival domain.
