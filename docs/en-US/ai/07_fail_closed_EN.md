# 07 Fail-Closed — Suppressing Ordinary Generation and Delegating to Humans

<!-- FILE: 07_fail_closed_EN.md -->

---

## Simply Saying “I Don’t Know” Does Not Constitute a Structural Guarantee

When AI is uncertain, saying “I don’t know” is important as an honest response.

However, leaving whether that response appears to the model’s policy, training, context, or generation at that moment does not constitute a structural guarantee.

Many generative systems are designed to provide useful answers to user questions. Therefore, even when uncertainty or limits exist, paths may remain through which ordinary responses continue by regeneration, supplementation, or rephrasing.

NRA-IDE does not address whether an answer appears honest. It addresses whether, when predefined structural conditions are reached, a path can be established that does not allow ordinary generated responses to pass, independently of the model’s intentions or self-evaluation.

---

## Fail-Closed Has Two Stages: Handoff and Terminal Processing

Chapter 05 distinguished the operating handoff point `Rop`, at which ordinary output is stopped, from the phase-transition boundary $R = 1.0$, at which structural margin is lost.

```text
R = δ / τ
0 < Rop < 1.0
```

This chapter also does not conflate the two.

| Condition       | Ordinary Generation             | Permitted Output                                              | Purpose                                                           |
| --------------- | ------------------------------- | ------------------------------------------------------------- | ----------------------------------------------------------------- |
| `R < Rop`       | Allowed when conditions are met | Ordinary generated response                                   | Normal operation                                                  |
| `Rop ≤ R < 1.0` | Suppressed                      | Predefined handoff notification                               | Hand judgment over to humans before the phase-transition boundary |
| `R ≥ 1.0`       | Suppressed                      | Minimal FAIL-CLOSED indicator or reference to a protected log | Do not continue new generation after the terminal boundary        |

`Rop` is an operating handoff condition defined by humans in accordance with the domain-specific point of approach to an irreversible regime. In principle, ordinary responses must be stopped at this point.

$R = 1.0$ is not an ordinary handoff point. It is the phase-transition boundary at which the remaining structural margin, $\tau - \delta$, is lost. After this boundary has been reached, the LLM must not be asked to generate new free-form text in order to explain the reason for stopping.

---

## The Structure Stops Ordinary Generation

When `Rop ≤ R < 1.0`, Post-NRA does not pass ordinary generated content to the user.

Instead, Post-NRA notifies the handoff to humans using only values determined from the Cause-Side and a format fixed in advance.

```text
HANDOFF_REQUIRED
REASON: domain-specific handoff threshold reached
OBSERVED: predefined structural fields
ACTION: generated response suppressed; human review required
```

This notification is not an explanation devised by the LLM at that moment. It is a fixed-format process that returns predefined fields as the result of structural evaluation.

Therefore, even when the LLM self-evaluates that “it is acceptable to continue answering,” or even when an evaluation score is high, it cannot override the Post-NRA handoff decision. The basis for stopping is not the persuasiveness of the output, but the structural state determined from the Cause-Side.

---

## After $R = 1.0$, Do Not Continue Ordinary Explanations

`R ≥ 1.0` is the terminal boundary at which structural margin has been lost.

For example, when `δ = 0.15` and `τ = 0.14`,

```text
R = 0.15 / 0.14 ≒ 1.071
```

At this point, regenerating an ordinary response or rephrasing it into a more cautious explanation does not restore structural margin itself.

Post-NRA may return only a predefined minimal indicator or a reference to a protected Discard Log.

```text
FAIL_CLOSED
REASON: structural boundary reached
ACTION: no further generated response; human handoff required
```

This does not mean that nothing is communicated to the user. It means that ordinary generated responses are suppressed and only the minimum structurally determined state is communicated.

---

## Regeneration Is Not a Substitute for Handoff

After an ordinary response has been suppressed, instructing the same LLM to “answer just one more time” or “use more cautious wording” is not a substitute for handoff.

After `Rop` has been reached, what is required is not continued generation. It is confirmation by a human who understands the target domain and can bear responsibility for the observations, grounds for settings, and handoff condition.

After `R ≥ 1.0`, continuing ordinary generation cannot return the fact that the phase-transition boundary has been crossed to the inside of normal operation. Regeneration is neither grounds for updating structural state nor grounds for cancelling the fact that the boundary has been reached.

---

## SILENCE and HALT Are Different

As shown in Chapter 05, SILENCE and HALT are not the same state.

**SILENCE** is the state in which `R ≥ 1.0` and `ω > 0`. The structure continues transitioning, but ordinary generation does not continue. Handoff to humans is indicated through a minimal fixed-format output or a reference to a protected log.

**HALT** is the state in which `ω = 0` and transition cannot be confirmed under the same rules. This does not mean that the system has “stopped safely.” Humans must verify the observation path, target system, and conditions for continuation.

| State   | Structural Condition  | Ordinary Generation                     | Required Response                                        |
| ------- | --------------------- | --------------------------------------- | -------------------------------------------------------- |
| SILENCE | `R ≥ 1.0` and `ω > 0` | Suppressed                              | Hand off to humans through a minimal fixed-format output |
| HALT    | `ω = 0`               | Do not reinterpret toward the safe side | Humans verify observation and transition conditions      |

The purpose of Fail-Closed is not to conceal a structural terminal condition behind an ordinary response. It is to suppress ordinary generation and clearly hand the point requiring judgment over to humans.

---

## Its Role Differs from Semantic Safety Judgments

Fail-Closed is not a mechanism that judges the factual correctness, legal compliance, ethical acceptability, or danger of output content from meaning alone.

Content filters, guardrails, and moderation may each serve separate purposes. NRA-IDE’s Fail-Closed does not uniformly replace them.

What NRA-IDE handles is not the meaning of output, but whether the structure is in a state that permits ordinary generation under defined observation and update rules.

For this reason, Fail-Closed alone cannot guarantee that ordinary LLM output is semantically correct, that observations of $\delta$ and $\tau$ are correct, or that the grounds for setting $\tau$ and `Rop` are appropriate.

---

## Scope Guaranteed by Fail-Closed

When correctly implemented, and when the Cause-Side observation path, $\tau$ update rules, `Rop` settings, and the Post-NRA output-blocking path are preserved, Fail-Closed guarantees the following.

* When `Rop` is reached, ordinary generated responses are suppressed and judgment is delegated to humans through a predefined fixed-format notification.
* When `R ≥ 1.0`, ordinary generation does not resume and processing transitions to minimal FAIL-CLOSED handling.
* The grounds for stopping or handoff are retained as records separated from the inputs of the next structural evaluation.

By contrast, it does not guarantee the following.

* That ordinary LLM output is semantically correct.
* That Cause-Side observations or external inputs are not contaminated.
* That the definitions or settings of $\tau$, `Rop`, and $\omega$ are appropriate for the target domain.
* What judgment should be made after handoff to humans.

Limiting the scope of the guarantee is not a weakness. It is a condition for not conflating the range that structure can handle with the judgments humans must bear.

---

## Connection to the Next Chapter

In Fail-Closed, humans must be able to verify the conditions that suppressed ordinary generation and the structural state.

The next chapter addresses how to record residuals that must not re-enter ordinary computation, together with the grounds for stopping and handoff. Logs are not material for generating the next response; they are testimony that enables humans to verify what occurred.

---
