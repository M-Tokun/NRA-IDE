# 09 Risks and Misuse — Structural Evaluation Does Not Substitute for Operational Integrity

<!-- FILE: 09_risks_and_misuse_EN.md -->

---

## What Structural Evaluation Can Do and What Remains Outside It

NRA-IDE derives the structural state $R$ from Cause-Side $\delta$ and $\tau$ in accordance with defined observation and update rules.

$$R = \frac{\delta}{\tau}$$

However, this calculation alone cannot automatically verify the following.

* That the values provided genuinely constitute observations representing the target system
* That the rules for transforming and accumulating values are appropriate for the target domain
* That the grounds for setting $\tau$ and $R_{op}$ are sufficient
* That ordinary LLM output is semantically correct
* That the purpose for which the system is used is ethically and legally appropriate

Structural evaluation operates on the inputs and rules provided to it. The provenance of inputs, the design of operations, and final judgment remain responsibilities borne by humans outside the structure.

This chapter examines representative paths that break the structure of NRA-IDE or make it appear to guarantee more than its actual scope.

---

## The First Risk: Contamination Before Values Are Supplied

When receiving values from external systems, the important question is not only whether a value has already been calculated. It is necessary to trace which observations produced it, which rules it passed through, and what held authority to update it.

Candidates for Cause-Side structural inputs include not only direct observations, but also structural variables determined from Cause-Side observation and load history through rules defined in advance. For example, $\tau$ is not necessarily a raw sensor value. It may be treated as a structural variable when the rule that determines $\tau$ is fixed in advance, the current value is determined from Cause-Side load history, and that path can be traced.

By contrast, the following path is not permitted.

```text
Effect-Side evaluations, outputs, and logs
    ↓
Backward inference: “the current δ or τ must have this value”
    ↓
Update of δ, τ, or Rop
    ↓
Next structural evaluation
```

Here, Effect-Side values recreate Cause-Side structural inputs. This is the $\Pi^{-1}$ path discussed in Chapter 03.

Numbers alone cannot reveal their full provenance. Therefore, external connections must associate at least the following information with each value.

* Observation target and observation procedure
* Time of acquisition, units, and quality status
* Rules and versions used for transformation or accumulation
* Entities authorized to update the value and the update path
* Confirmation that Effect-Side evaluations, outputs, and logs have not entered the grounds for updating it

A value for which this information cannot be verified is not adopted as a Cause-Side structural input. It is not supplemented through guesswork. The system proceeds instead to predefined invalid-state handling or human handoff.

---

## Misuse Pattern 1: Moving $\tau$ or $R_{op}$ for Effect-Side Convenience

Two aspects of $\tau$ must be distinguished.

* **The rule that determines $\tau$:** Defined at design time. It is not changed from the Effect-Side.
* **The current value of $\tau$:** Changes according to fixed rules and Cause-Side load history.

Making the current $\tau$ appear larger than it actually is, or loosening the rules that determine $\tau$ without justification, makes $R$ appear smaller. However, this does not mean that the actual state of the target system has changed.

The same applies to $R_{op}$. $R_{op}$ is a domain-specific handoff condition placed before $R = 1.0$. It is an operating parameter that determines where ordinary generation is suppressed. It must not be moved later automatically or arbitrarily on the basis of recent output evaluations or the frequency of stopping.

```text
Permitted update:
Cause-Side load history → τ update rule fixed in advance → current τ

Prohibited update:
“The previous output appeared acceptable” → expansion of τ or postponement of Rop
```

When changing the rule that determines $\tau$ or changing $R_{op}$, the change must not occur automatically during structural evaluation. It must be handled as a separate design change.

The grounds for change, scope of application, rule version, approver, and time of application must be recorded and verified by a human capable of bearing responsibility for the target domain.

$R = 1.0$ is not a handoff point that may be moved through ordinary operational adjustment. It must remain distinct from $R_{op}$ as the phase-transition boundary at which structural margin is lost.

---

## Misuse Pattern 2: Failing to Protect Logs as Testimony

As confirmed in Chapter 08, a Discard Log is a record that is not automatically reintroduced into the next structural evaluation. However, it must remain accessible for humans to verify the reasons for stopping or handoff.

When log contents can be rewritten afterward without leaving evidence of modification, the following can no longer be verified.

* Which observation and update rules were used
* Which $R_{op}$ suppressed ordinary generation
* Whether $R = 1.0$ was reached or exceeded
* In which discrete transition `entropy_export` was recorded
* Whether human handoff or FAIL-CLOSED processing was performed

What is required is not merely storing logs. Logs must be protected as auditable testimony through append-only storage, access control, tamper detection, and association with rule versions.

However, humans reading logs and logs automatically updating the next $\delta$, $\tau$, or $R_{op}$ are different things. The former is audit; the latter may become $\Pi^{-1}$ feedback.

---

## Misuse Pattern 3: Omitting or Confusing the Responsibilities of the Three Layers

Pre-NRA, LLM, and Post-NRA are not duplicating the same process.

* **Pre-NRA:** Verifies the provenance, transformation rules, and update paths of structural inputs.
* **LLM:** Handles user requests and performs ordinary semantic generation.
* **Post-NRA:** Determines, on the basis of the latest structural state, whether ordinary output passes through or is suppressed for handoff or FAIL-CLOSED processing.

When one of these layers is omitted, other safety mechanisms may still exist. However, the three-layer separation defined by NRA-IDE and its structural guarantee cannot be claimed.

For example, without Pre-NRA, there is no path for verifying that Effect-Side values have not entered structural inputs. Without Post-NRA, there is no place in the delivery path to enforce suppression of ordinary generation when $R_{op}$ is reached, or minimal FAIL-CLOSED processing after $R \geq 1.0$.

Granting an LLM authority to rewrite $\tau$, $R_{op}$, logs, or structural inputs disables the Causal Diode even when all three layers are present.

The mere appearance of an ordinary response is not evidence that structural-input integrity, handoff conditions, or log protection have been preserved.

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

Humans may read external-system results as reference information. However, the configuration must not allow those results to modify $\delta$, $\tau$, or $R_{op}$ automatically.

$\delta$ may be updated as an observation or a transformed value derived from the Cause-Side. The current value of $\tau$ may be updated dynamically only through Cause-Side load history and update rules fixed in advance. $R_{op}$ must not be changed automatically during ordinary operation; when change is necessary, it must be handled through design and governance procedures separated from the structural-evaluation system.

When $R_{op}$ is changed, the reason for change, supporting data, rule version, approving entity, time of application, and values before and after the change must be recorded. This prevents ordinary operational state updates from being confused with changes to the design boundary.

---

## Responsibilities of Designers and Operators

NRA-IDE provides constraints for structural inputs and output paths. However, structure alone cannot substitute for the following.

* Definition of observations, transformation rules, units, and quality conditions for the target system
* Verification of the grounds for $\tau$ update rules and $R_{op}$ settings
* Design of domains that must be handed over to humans before reaching $R_{op}$
* Access control and tamper protection for observations, logs, and settings
* Verification of implementation and change management for the three-layer structure
* The role, contact path, and decision procedures of humans receiving handoff
* Ethical and legal judgment concerning the purpose for which the system is used

Especially in high-risk domains, definitions of structural variables and handoff conditions must be verified with experts capable of bearing responsibility for the target domain. This document set does not replace that judgment.

What NRA-IDE guarantees is that, when correctly implemented and when observation paths, update rules, and output-blocking paths are preserved, Effect-Side values do not alter Cause-Side structural inputs and ordinary generation is suppressed at the defined handoff condition.

The fact that structure does not judge good and evil or final correctness is not a defect. It is the boundary of this design: such matters are not disguised as structural evaluation, but remain domains in which humans bear responsibility.

---

## Connection to the Next Chapter

This chapter has established that input provenance, settings for $\tau$ and $R_{op}$, log protection, three-layer separation, and external connections are prerequisites supporting NRA-IDE guarantees.

The next chapter organizes what NRA-IDE guarantees when these prerequisites are met, and what it still cannot guarantee.

---
