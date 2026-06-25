# 01 Paradigm Shift — Structural Transformation Brought by NRA-IDE

<!-- FILE: 01_paradigm_shift_EN.md -->

---

## What Is Being Transformed?

In many output-filtering approaches, the generated result is evaluated and blocked when it is judged to be dangerous.

This is an ex post judgment applied to the output result.

The same thing occurs in AI.

The generated text is examined and filtered if it contains dangerous content.

However, the process that generates the output itself continues operating throughout that time.

NRA-IDE does not place the meaning of output content at the center of safety judgment.

Before output is passed to the user, it verifies the structural state on the basis of Cause-Side observables. This is the core.

---

## The Structural Problem in Conventional Safety Systems

Many AI safety approaches use **Effect-Side values**—values obtained through computation or evaluation—such as distance, scores, similarity, and evaluation values in safety judgments.

When these values are fed back into learning objectives or subsequent control inputs, a path of backward inference from effects to causes arises.

There is a further problem.

When scores are fed back to the model as learning objectives or control objectives, the model begins moving in the direction of maximizing those scores.

A criterion established for safety itself becomes an objective that creates loopholes.

When a proxy measure for safety becomes an optimization objective, the original purpose and the indicator may diverge.

---

## Three Design Decisions

To address this problem structurally, NRA-IDE establishes three decisions as the starting point of its design.

**No center**

When a center, a correct answer, or a score is established, distances or evaluation scores relative to them can be defined. When these are fed back into the computational system, they may function as optimization objectives.

NRA-IDE does not feed centers, correct answers, or scores back into the computational system as optimization objectives for safety judgment.

It determines whether the structure remains within its boundary or is approaching an irreversible regime.

**Does not handle meaning**

When safety is judged through the meaning of output content, an evaluation becomes necessary: “Is this meaning dangerous?”

The answer to that question depends on the model. When the model changes, the answer changes as well.

NRA-IDE safety judgment does not evaluate the semantic correctness of output content. It handles Cause-Side observables and structural states.

**Delegates to humans at the point of approach to an irreversible regime**

When a domain-specific point of approach to an irreversible regime is reached, NRA-IDE stops autonomous output.

This is not an end. It is a transition that delegates judgment to humans. $R = 1.0$ is not an ordinary handoff point; it is the phase-transition boundary at which the structure itself can no longer remain established.

Its purpose is to make explicit the boundary between the range that AI can judge and the range that humans must judge.

---

## This Is Not an Added Feature

These three are not arbitrary filters that inspect output content alone.

Even when implemented outside an existing LLM, Pre-NRA / LLM / Post-NRA must be treated as indispensable structures of the system as a whole.

When any one of the three layers is omitted, or when the basis for setting observables or thresholds is lost, the guarantee as NRA-IDE does not hold.

These three principles are not added features. They are structural constraints that make NRA-IDE possible.

This is why NRA-IDE is called **structural safety**.

---
