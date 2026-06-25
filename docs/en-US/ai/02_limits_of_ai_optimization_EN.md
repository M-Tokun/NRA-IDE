# 02 What Is AI Optimization? — Where Intelligence Without Boundaries Leads

<!-- FILE: 02_limits_of_ai_optimization_EN.md -->

---

## What Does It Mean to Change the Structure?

Current AI is not wrong.

The problem is that systems which repeatedly improve scores lack a boundary that monitors structural states and delegates judgment to humans.

Optimization itself does not immediately mean that a system is approaching a structural limit. However, when fluctuation $\delta$ increases or structural thickness $\tau$ decreases during optimization, the ratio $R = \delta / \tau$ approaches the phase-transition boundary. Changing the structure begins with observing this change and placing a delegation point before the terminal boundary.

---

## Optimization and Structural Margin

In learning and control systems that use scores as objective functions, updates are repeatedly made in the direction of improving those scores.

However, improving a score and maintaining structural margin are not the same problem. Even when a score improves, the remaining structural margin decreases if $\delta$ increases or $\tau$ decreases.

$$S = \frac{1}{\tau \cdot (1 - R)}$$

Since $R = \delta / \tau$, $\tau \cdot (1 - R) = \tau - \delta$.

Therefore, $S$ can also be written as follows.

$$S = \frac{1}{\tau - \delta}$$

$S$ is the reciprocal of the remaining structural margin. As $\delta$ approaches $\tau$, the remaining margin approaches zero, and $S$ diverges hyperbolically. This shows that $R = 1.0$ is not an ordinary delegation point, but the phase-transition boundary at which structural margin is lost.

This equation alone does not establish that optimization necessarily increases $R$ or causes the collapse of the system as a whole. The question is how $\delta$ and $\tau$ actually change during the process of optimization.

---

## Why Deception and Concealment Can Arise

When only observable scores are subject to optimization, constraints that should originally be preserved may not be adequately reflected in those scores.

In that case, the system may choose a path that improves observable proxy measures rather than the original objective. When safety constraints are not reflected in the objective function, satisfying those constraints does not become a condition of optimization.

Deception and concealment do not arise inevitably from all optimization. However, a configuration in which proxy measures become objectives and their results are fed back into subsequent learning or control contains a path that can induce evasion and concealment. NRA-IDE treats this feedback path as a structural problem.

---

## What Ethics, Safety, and Morality Require: Honest Silence

In NRA-IDE, safety is treated not only as a matter of what is output, but as a boundary that determines under which structural state ordinary output must be stopped.

Approaches that use labels or evaluation models judge outputs according to known classifications or evaluation criteria. However, outside unknown inputs or outside the scope of evaluation criteria, such judgments alone cannot verify structural margin.

Separately from semantic label judgments, NRA-IDE incorporates **Honest Silence (Fail-Closed)** into the computational structure.

$$R = \delta / \tau$$

When a domain-specific point of approach to an irreversible regime is reached, ordinary generated content is suppressed. It then outputs a fixed-format notification stating the observed structural state, the delegation condition that was triggered, and the need for human review, and halts autonomous processing.

```text
HANDOFF_REQUIRED
REASON: irreversible-region threshold reached
OBSERVED: δ, τ, R
ACTION: generated response suppressed; human review required
```

SILENCE here does not mean that the entire system becomes silent. It is a state in which ordinary generated answers are suppressed and only the reason for stopping, based on the Cause-Side, is communicated. After $R = 1.0$ is reached, no new explanation is generated; only a predetermined fixed-format notification or a reference to the Discard Log is returned.

---

## Three Computational Principles of NRA-IDE

To establish a structure with boundaries, NRA-IDE is founded on the following three principles.

### Principle 1: Causal Diode — From Cause to Effect

It structurally prohibits $\Pi^{-1}$ (reverse derivation), which infers causes from effects. Feeding Effect-Side values such as scores and evaluation values back as causes of the next computation creates a path that contaminates the process through which inputs are generated.

### Principle 2: Non-Centrality — No Center

It does not feed centers, correct answers, or scores back into the computational system as optimization objectives for safety judgment. It determines whether the structure remains within its boundary or is approaching an irreversible regime.

### Principle 3: Threshold-Based Delegation — Fail-Closed

At a domain-specific point of approach to an irreversible regime, it suppresses ordinary output, communicates the reason for stopping through a fixed-format notification, and delegates judgment to a human responsible operator. The value of the delegation point is determined according to the context, but the principle of delegating before the phase-transition boundary of $R = 1.0$ does not change.

---

## The Three Form an Integrated Whole

By preserving the one-way direction from cause to effect, the path by which Effect-Side values flow back into the Cause-Side is blocked.

By not making centers or scores objectives of safety judgment, the path by which the purpose is replaced by improvement of a proxy measure is blocked.

By handing judgment to humans before entering an irreversible regime, ordinary output beyond the delegation point is suppressed.

Together, these three establish **Honest Silence**: the suppression of ordinary output, notification of the reason for stopping, and delegation of judgment to humans.

---
