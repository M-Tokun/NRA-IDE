# 01 Paradigm Shift — The Structural Shift Introduced by NRA-IDE
<!-- FILE: 01_paradigm_shift_EN.md -->

---

## What is being shifted?

Until now, safety has usually been treated as something that happens **after the result appears**.

A result is produced, and then someone checks whether it is dangerous.
That is an after-the-fact judgment.

The same thing happens in AI.
A piece of output text is generated, and then it is filtered if the content looks dangerous.

But the process that generated that output continues to operate during that time.

NRA-IDE shifts the point of intervention.
It calculates the **structural state before the result appears**.

That is the core idea.

---

## The structural problem in conventional safety

Conventional AI safety judges safety by using **effect-side values** such as distance, score, similarity, or evaluation metrics.

But all of these are values that can only be measured **after output has already been produced**.

There is another problem as well.

Once a score is introduced, the model begins to move in the direction that maximizes that score.
A criterion that was introduced for safety becomes, at the same time, a target for exploitation.

This problem has long been known in safety engineering.

---

## Three design decisions

To solve this, NRA-IDE begins from three design decisions.

**No center**

If there is a center, distance can be defined.
If distance can be defined, optimization begins.

NRA-IDE adopts a structure with no center, so optimization itself does not arise.

Only the boundary exists.
The only question is whether something is inside or outside.

**No semantics**

The moment safety is judged by meaning, a new question always appears:

**“Is this meaning dangerous?”**

The answer depends on the model.
If the model changes, the answer changes as well.

NRA-IDE does not handle meaning.
It handles only the structural state.

**When a threshold is exceeded, hand it to a human**

When the structural margin approaches its limit, NRA-IDE stops quietly.

This is not an ending.
It is a transition in which judgment is handed to a human.

The goal is to draw a clear boundary between what AI may judge and what must be judged by a person.

---

## This is not an added feature

These three are not safety devices added later to an existing AI.

They are principles placed at the starting point of the design.

Safety devices can fail.
A bolt-on device can also be removed.

But if these principles are embedded at the design origin, then removing them breaks the structure itself.

That is why NRA-IDE is called **structural safety**.

---