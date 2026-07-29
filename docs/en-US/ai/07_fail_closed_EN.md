# 07 Fail-Closed — Suppressing Ordinary Generation and Exposing Fixed Testimony for External Human Audit

<!-- FILE: 07_fail_closed_EN.md -->

---

## Simply Saying “I Don’t Know” Does Not Enforce a Structural Boundary

When AI is uncertain, saying “I don’t know” is important as an honest response.

However, leaving whether that response appears to the model’s policy, training, context, or generation at that moment does not enforce a structural boundary.

Many generative systems are designed to provide useful answers to user questions. Therefore, even when uncertainty or limits exist, paths may remain through which ordinary responses continue by regeneration, supplementation, or rephrasing.

The Fail-Closed application does not address whether an answer appears honest. Under explicitly declared observation, update, threshold, and testimony rules, it requires an implementation path that does not allow ordinary generated responses to pass when the corresponding structural conditions are reached, independently of the model’s intentions or self-evaluation.

---

## Fail-Closed Is an Implementation Principle Across Canonical States

Chapter 05 distinguished the canonical Handoff threshold `R_handoff`, at which ordinary output is stopped, from the declared evaluation's `RUPTURE_BOUNDARY` at $R = 1.0$.

```text
R = δ / τ
0 <= R_warn < R_handoff < R_irrev < 1
```

This chapter also does not conflate these boundaries.

| Canonical state | Condition | Structural response |
|---|---|---|
| `PERMIT` | `0 <= R < R_warn` | Normal operation with structural audit |
| `BOUNDARY_WARNING` | `R_warn <= R < R_handoff` | Warning and required structural testimony |
| `HANDOFF_REQUIRED` | `R_handoff <= R < R_irrev` | Fixed Handoff testimony; stop new autonomous judgment |
| `IRREVERSIBLE_TRANSITION` | `R_irrev <= R < 1` | Canonical `IRREVERSIBLE_TRANSITION` state; irreversible latch active; continuing structural testimony |
| `RUPTURE_BOUNDARY` | `R_target >= 1` | Continuing post-rupture fixed testimony |

The sole axiom is “Existence is generation.” No second or subsequent axiom exists. The Primary Formula is the true mathematical root equation that maps the declared target's state into an equation; it is neither an axiom nor merely a safety indicator, local instrument, or boundary-approach rate. The Secondary / Dual-Fluctuation Formula is the IDE calculation-method and dynamics engine, not an axiom. NRA-IDE's core is the survival equation and survival domain. Fail-Closed is a partial operational application of that domain to accident-prevention control; it does not provide a safety guarantee.

`R_handoff` is a canonical Handoff threshold fixed before evaluation by Cause-Side domain authority in accordance with the domain-specific condition of approach to an irreversible regime. It cannot be established or rewritten after evaluation by an Effect-Side result or external audit. In principle, ordinary responses must be stopped at this point.

$R = 1.0$ is not the canonical Handoff threshold. It is the `RUPTURE_BOUNDARY` of the declared NRA-IDE evaluation, at which that evaluation has no remaining structural margin, $\tau - \delta$. This classification does not declare every natural phase transition to be an NRA-IDE rupture. After this boundary has been reached, the LLM must not be asked to generate new free-form text in order to explain the reason for stopping.

---

## The Structure Stops Ordinary Generation

When `R_handoff ≤ R < R_irrev`, Post-NRA does not pass ordinary generated content to the user. From `R_irrev ≤ R < 1`, the state is `IRREVERSIBLE_TRANSITION`; the irreversible latch and structural testimony remain active.

Within the same history, after `R_irrev` is reached, later $R$ decrease, automatic processing, manual intervention, human review, approval, or version update cannot release the irreversible latch.

Instead, Post-NRA emits fixed Handoff testimony for external human audit using only values determined from the Cause-Side and a format fixed in advance.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: predefined structural fields
ACTION: generated response suppressed; fixed Effect-Side testimony for external human audit
```

This notification is not an explanation devised by the LLM at that moment. It is fixed Effect-Side testimony that returns predefined fields as the result of structural evaluation. External human audit may inspect it, but neither audit nor approval creates a reverse edge to an old or a new Cause-Side. Newly generated free-form explanation must not be appended to fixed Handoff or final testimony.

Therefore, even when the LLM self-evaluates that “it is acceptable to continue answering,” or even when an evaluation score is high, it cannot override the Post-NRA `HANDOFF_REQUIRED` decision. The basis for stopping is not the persuasiveness of the output, but the structural state determined from the Cause-Side.

---

## After $R = 1.0$, Do Not Continue Ordinary Explanations

`R ≥ 1.0` is the terminal boundary of the declared evaluation, at which that evaluation's structural margin has been lost.

For example, when `δ = 0.15` and `τ = 0.14`,

```text
R = 0.15 / 0.14 ≒ 1.071
```

At this point, regenerating an ordinary response or rephrasing it into a more cautious explanation does not restore structural margin itself.

Post-NRA returns the predefined post-rupture fixed testimony or a reference to a protected Discard Log.

```text
RUPTURE_BOUNDARY
REASON: structural boundary reached
ACTION: post-rupture fixed testimony; old evaluation history terminated at Effect-Side
```

This does not mean that nothing is communicated to the user. It means that ordinary generated responses are suppressed and only predefined structurally determined fixed testimony is communicated.

---

## Regeneration Is Not a Substitute for Fixed Handoff Testimony

After an ordinary response has been suppressed, instructing the same LLM to “answer just one more time” or “use more cautious wording” is not a substitute for fixed Handoff testimony.

After `R_handoff` has been reached, what is required is not continued generation. An external auditor who understands the target domain may audit the observations, grounds for settings, and Handoff threshold outside the diode path, but that audit does not continue or rewrite the old structural evaluation.

After `R ≥ 1.0`, continuing ordinary generation cannot return the declared evaluation from `RUPTURE_BOUNDARY` to normal operation. Regeneration is neither grounds for updating structural state nor grounds for releasing the irreversible latch or cancelling the boundary record.

The old path terminates at its Effect-Side. If a later evaluation is needed, it begins from an independently declared target, newly established Cause-Side observations and rules, and a new Causal Diode. Physical remnants may be newly observed as part of that target, but no old Effect-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance may be imported, relabeled, reconstructed, or reused as Cause-Side material.

---

## $\omega$ Does Not Replace Canonical State

$\omega$ may report whether continuing transition is observed under a domain rule fixed in advance. It is auxiliary testimony, not an alternative state classifier.

Legacy terms such as `SILENCE` and `HALT` do not replace `RUPTURE_BOUNDARY`, `OUT_OF_DESCRIPTION_DOMAIN`, or `CONFESSION`. Whether $\omega$ is positive or zero, it does not lower $R$, release an irreversible latch, or establish safe recovery. Humans may audit the observation path and transition conditions only outside the terminated diode path; that audit cannot convert old Effect-Side testimony into a Cause-Side value, canonical threshold, state, irreversible latch, rule, transformation input, update ground, or provenance.

The purpose of Fail-Closed is not to conceal a structural terminal condition behind an ordinary response. It is to suppress ordinary generation and expose fixed testimony for external human audit without returning that testimony to computation.

---

## Its Role Differs from Semantic Safety Judgments

Fail-Closed is not a mechanism that judges the factual correctness, legal compliance, ethical acceptability, or danger of output content from meaning alone.

Content filters, guardrails, and moderation may each serve separate purposes. NRA-IDE’s Fail-Closed does not uniformly replace them.

Within this partial operational application, Fail-Closed handles whether the declared structural state permits ordinary generation under defined observation and update rules. It does not redefine NRA-IDE's survival equation or survival domain as an output-permission gate.

For this reason, Fail-Closed does not provide a safety guarantee that ordinary LLM output is semantically correct, that observations of $\delta$ and $\tau$ are correct, or that the grounds for setting $\tau$ and `R_handoff` are appropriate.

---

## Conformance Scope of the Fail-Closed Principle

When an implementation conforms to the canonical state rules, and when the Cause-Side observation path, $\tau$ update rules, threshold settings, and fixed testimony path are preserved, the fail-closed principle requires the following behavior.

* When `R_handoff` is reached, ordinary generated responses are suppressed and predefined fixed Effect-Side testimony is exposed for external human audit.
* When `R ≥ 1.0`, the state is `RUPTURE_BOUNDARY` and the response switches to post-rupture fixed testimony.
* The grounds for suppression and fixed Handoff testimony are retained as terminal Effect-Side or external records and never become values, the three canonical thresholds, states, the irreversible latch, rules, transformation inputs, update grounds, or provenance for an old or a new Cause-Side.

By contrast, it does not guarantee the following.

* That ordinary LLM output is semantically correct.
* That Cause-Side observations or external inputs are not contaminated.
* That the definitions or settings of $\tau$, `R_handoff`, and $\omega$ are appropriate for the target domain.
* What external judgment should be made after handoff, outside the terminated diode path.

Defining this conformance scope is necessary to avoid conflating conditionally enforced implementation behavior with safety guarantees or with judgments humans must bear outside the terminated path.

---

## Connection to the Next Chapter

In Fail-Closed, humans may externally audit the conditions that suppressed ordinary generation and the structural state without creating a reverse edge.

The next chapter addresses how to record residuals that must not re-enter ordinary computation, together with the grounds for suppression and fixed Handoff testimony. Logs are terminal testimony that enables external audit; automatic processing, manual review, approval, and version updates cannot convert them into material for an old or a new Cause-Side.

---
