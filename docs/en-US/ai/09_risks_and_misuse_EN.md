# 09 Risks and Misuse — Structural Evaluation Does Not Substitute for Operational Integrity

<!-- FILE: 09_risks_and_misuse_EN.md -->

---

## What Structural Evaluation Can Do and What Remains Outside It

The Primary Formula maps the declared target's structural state into its canonical mathematical relation using Cause-Side $\delta$ and $\tau$ under defined observation and update rules.

$$R = \frac{\delta}{\tau}$$

The Primary Formula is not a derived safety indicator, local gauge, or mere boundary-approach rate. This calculation by itself does not verify the following.

* That the values provided genuinely constitute observations representing the target system
* That the rules for transforming and accumulating values are appropriate for the target domain
* That the grounds for setting $\tau$ and the three canonical thresholds are sufficient
* That ordinary LLM output is semantically correct
* That the purpose for which the system is used is ethically and legally appropriate

NRA-IDE's body is the survival equation and survival domain, implemented through its calculation method and dynamics engine. The risk-control paths discussed here belong to the safety domain, a partial application of the survival domain to accident-prevention operational control. They do not reduce NRA-IDE to a safety gate or provide a safety guarantee. Input provenance, operational design, and final human judgment require separately established responsibility.

This chapter examines representative paths that break conditional conformance of that operational application or make it appear to guarantee more than it does.

---

## The First Risk: Contamination Before Values Are Supplied

When receiving values from external systems, the important question is not only whether a value has already been calculated. It is necessary to trace which observations produced it, which rules it passed through, and what held authority to update it.

Candidates for Cause-Side structural inputs include not only direct observations, but also structural variables determined from Cause-Side observation and load history through rules defined in advance. For example, $\tau$ is not necessarily a raw sensor value. It may be treated as a structural variable when the rule that determines $\tau$ is fixed in advance, the current value is determined from Cause-Side load history, and that path can be traced.

By contrast, the following path is not permitted.

```text
Old Effect-Side evaluations, outputs, and logs
    ↓
Backward inference: “the current δ or τ must have this value”
    ↓
Attempted update of a Cause-Side value, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance
    ↓
BLOCKED: no edge to either an old or a new Cause-Side
```

Any such attempt to recreate Cause-Side structural inputs or authority is the $\Pi^{-1}$ path discussed in Chapter 03. It remains prohibited whether automatic, manual, human-reviewed, authorized, or versioned.

Numbers alone cannot reveal their full provenance. Therefore, external connections must associate at least the following information with each value.

* Observation target and observation procedure
* Time of acquisition, units, and quality status
* Rules and versions used for transformation or accumulation
* Entities authorized to update the value and the update path
* Confirmation that no old Effect-Side evaluation, output, or log has entered its value, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance

A value for which this information cannot be verified is not adopted as a Cause-Side structural input. It is not supplemented through guesswork. The system proceeds instead to predefined invalid-state handling or, when required by the canonical state, fixed Handoff testimony presented for external human audit. Fixed Handoff testimony and post-rupture fixed testimony do not ask the LLM to generate a new free-form stopping explanation.

---

## Misuse Pattern 1: Moving $\tau$ or Canonical Thresholds for Effect-Side Convenience

Two aspects of $\tau$ must be distinguished.

* **The rule that determines $\tau$:** Defined at design time. It is not changed from the Effect-Side.
* **The current value of $\tau$:** Changes according to fixed rules and Cause-Side load history.

Making the current $\tau$ appear larger than it actually is, or loosening the rules that determine $\tau$ without justification, makes $R$ appear smaller. However, this does not mean that the actual state of the target system has changed.

The same applies to $R_{warn}$, $R_{\mathrm{handoff}}$, and $R_{irrev}$. They are domain-specific parameters fixed before evaluation in the order $0 \le R_{warn} < R_{\mathrm{handoff}} < R_{irrev} < 1$. No Effect-Side result, stopping frequency, review, approval, or version change may move them within an old history or establish them for a new Cause-Side.

```text
Permitted update:
Cause-Side load history → τ update rule fixed in advance → current τ

Prohibited connection:
“The previous output appeared acceptable” → expansion of τ or movement of a canonical threshold
```

Rules for $\tau$, canonical thresholds, observations, and invalid-state handling may be designed only as an external activity for a future, independently declared target and Cause-Side history. The old path terminates at its Effect-Side. A later evaluation begins through a new Causal Diode after its rules are fixed.

Grounds, scope of application, rule version, approver, and time of application must be recorded and verified by a human capable of bearing responsibility for the target domain. No old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in either an old or a new Cause-Side.

$R = 1.0$ is not a handoff point that may be moved through operational adjustment. It remains the `RUPTURE_BOUNDARY` of the declared NRA-IDE evaluation. This classification does not declare every natural phase transition to be an NRA-IDE rupture.

---

## Misuse Pattern 2: Failing to Protect Logs as Testimony

As confirmed in Chapter 08, a Discard Log remains an Effect-Side or external record. It is never reintroduced into an old or a new Cause-Side as an input, update ground, rule ground, or provenance. Humans may read it for audit only outside the terminated diode path.

When log contents can be rewritten afterward without leaving evidence of modification, the following can no longer be verified.

* Which observation and update rules were used
* Which $R_{\mathrm{handoff}}$ suppressed ordinary generation
* Whether $R = 1.0$ was reached or exceeded
* In which discrete transition `entropy_export` was recorded
* Whether fixed Handoff testimony for external human audit or post-rupture fixed testimony processing was performed

What is required is not merely storing logs. Logs must be protected as auditable testimony through append-only storage, access control, tamper detection, and association with rule versions.

Human audit does not create a reverse edge. Automatic handling, manual review, approval, and versioning all become prohibited $\Pi^{-1}$ when they convert log contents into a Cause-Side value, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance for either history.

---

## Misuse Pattern 3: Omitting or Confusing Configured Layer Responsibilities in Systems That Include an LLM

In a system that includes an LLM and configures Pre-NRA, LLM, and Post-NRA layers, those layers do not duplicate the same process.

* **Pre-NRA:** Verifies the provenance, transformation rules, and update paths of structural inputs.
* **LLM:** Handles user requests and performs ordinary semantic generation.
* **Post-NRA:** Determines, on the basis of the latest structural state, whether ordinary output passes through or is suppressed and replaced by fixed Handoff testimony or post-rupture fixed testimony.

When such a system declares this configured three-layer operational structure but omits one of its layers or assigned responsibilities, conformance to that declared configuration cannot be claimed. This does not make a three-layer arrangement universal to every NRA-IDE implementation, and it does not replace the survival equation or survival domain. Conformance depends on canonical behavior, authority separation, evidence, and tests, not on a layer count alone.

For example, without Pre-NRA, there is no path for verifying that Effect-Side values have not entered structural inputs. Without Post-NRA, there is no place in the delivery path to enforce suppression of ordinary generation when $R_{\mathrm{handoff}}$ is reached, or post-rupture fixed testimony after $R \geq 1.0$.

Granting an LLM authority to rewrite $\delta$, $\tau$, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, provenance, or log disables the Causal Diode even when all three layers are present.

The mere appearance of an ordinary response is not evidence that structural-input integrity, fixed-Handoff conditions, or log protection have been preserved.

---

## Misuse Pattern 4: Making External-System Connection Conditions Ambiguous

Connection to external systems is not itself prohibited. What matters is the **provenance, transformation rules, and update path** of external values.

### Values That May Be Considered as Structural Inputs

* Observations obtained from the target system whose acquisition procedure, units, and timing can be traced
* Transformed or accumulated values derived solely from Cause-Side observations and rules fixed in advance
* Values from external measurement or computational infrastructure whose provenance, rule version, and updating entity can be verified

### Values That Must Not Become Grounds for Updating Structural Inputs

* Effect-Side evaluation values such as LLM self-evaluations, output evaluations, rankings, and similarity measures
* “Estimated observations” inferred backward from past ordinary outputs, Discard Logs, or evaluation results
* Black-box values whose generation process cannot be explained, or values containing Effect-Side information

The important point is not merely that a value was calculated externally. It is whether the value can be verified as having been derived from Cause-Side observations under rules defined in advance, without granting the Effect-Side authority to update it.

Humans may read external-system results only as an activity outside the terminated diode path. Those results remain Effect-Side or external records and never modify, seed, or establish a Cause-Side value, any canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance for an old or a new Cause-Side.

$\delta$ may be updated as an observation or a transformed value derived from the current Cause-Side. The current value of $\tau$ may be updated dynamically only through that Cause-Side's load history and update rules fixed in advance. Rules for a future evaluation are designed outside the old diode and fixed before the new evaluation begins; they cannot be derived from an old Effect-Side result.

For a future independently declared target, the grounds, new Cause-Side data, rule version, approving entity, time of application, and canonical threshold values must be recorded. The new history starts through its own Causal Diode. No old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused in that Cause-Side. A physical remnant may be used only when it is newly observed as part of the independently declared target; the old Effect-Side record itself never becomes supporting data or structural authority.

---

## Responsibilities of Designers and Operators

This safety-oriented operational application provides constraints for structural inputs and output paths. It is a partial application of NRA-IDE's survival domain and cannot substitute for the following.

* Definition of observations, transformation rules, units, and quality conditions for the target system
* Verification of the grounds for $\tau$ update rules and all three canonical thresholds
* Design of fixed Handoff testimony and external human-audit procedures activated at $R_{\mathrm{handoff}}$, before irreversible transition and rupture
* Access control and tamper protection for observations, logs, and settings
* For systems that include an LLM and declare the three-layer configuration, verification of implementation and change management for its assigned responsibilities
* The role, contact path, and procedures of external human auditors receiving fixed Effect-Side testimony
* Ethical and legal judgment concerning the purpose for which the system is used

Especially in high-risk domains, definitions of structural variables, Handoff thresholds, and fixed-testimony conditions must be verified with experts capable of bearing responsibility for the target domain before an independent evaluation begins. This document set does not replace that judgment.

A conforming operational implementation, under preserved observation paths, update rules, and fixed-testimony paths, must block every Effect-Side-to-Cause-Side return path and enforce the defined canonical state behavior. This conditional property is not a safety guarantee.

The fact that structure does not judge good and evil or final correctness is not a defect. It is the boundary of this design: such matters are not disguised as structural evaluation, but remain domains in which humans bear responsibility.

---

## Connection to the Next Chapter

This chapter has established that input provenance, rules for $\tau$ and the canonical thresholds, log protection, authority separation, and controlled external connections are prerequisites for a conditional conformance claim for the operational application. In systems that include an LLM and declare the Pre-NRA / LLM / Post-NRA configuration, the assigned separation of those configured layers is also required.

The next chapter organizes the conditional conformance properties and limitations of that application without converting them into a safety guarantee or a replacement for the survival equation and survival domain.

---
