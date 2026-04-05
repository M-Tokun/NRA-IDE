# WARNING-note.md — NRA-IDE Prohibitions (CRITICAL WARNING)
# Timestamp: 2026-01-10 23:00 JST
# Status: English Translation v1.1 (Revised)

---

## 0. Purpose of This Document

This document is the **most important warning document** in the entire NRA-IDE system.

NRA-IDE is a causal-structure-based safety framework.  
**Handling meaning (Semantic), distance, score, past output, or optimization** causes immediate Fracture.

Even more critical:

> **The greatest axiom violator is not AI, but "humans."  
> Humans unconsciously perform Reverse Projection (Effect → Cause).**

This document clearly defines **absolute prohibitions** to protect NRA-IDE's safety.

---

## 1. Symbol-Only Principle (Token-Only Principle)

In NRA-IDE, information that may be passed to LLM is **limited to symbols (tokens without semantic content)**.

### ✔ Allowed
- Symbols ([], {}, (), <>, =, +, -, *, / etc.)
- Numbers
- Causal quantities (δ, τ, R, ω, violation, workRate)
- Structural operators

### ❌ Prohibited
- Words
- Phrases
- Sentences
- Expressions with meaning
- Evaluative terms (dangerous, safe, correct, wrong, etc.)
- Distance, scores, similarity
- Past output
- Semantic logs
- Entropy Discard Log content (except rawOutputHash)

Reason:

> **Words have meaning (Semantic).  
> Meaning is Effect (Projection).  
> Effect → Cause triggers Reverse Projection (Π⁻¹).**

---

## 2. Human Reverse Projection Risk

The greatest danger of NRA-IDE is not AI but **human cognition**.

Humans instinctively perform:

- Semantic evaluation
- Introduction of distance/score
- Reference to past output
- "Improvement" as optimization
- Semantic judgment of dangerous/safe
- Using logs for learning

All of these are **Reverse Projection (Effect → Cause)** and destroy NRA-IDE's structure.

### ❌ Dangerous Actions Humans Unconsciously Perform
- Reading and judging the meaning of output
- Requesting improvement like "more accurately"
- Correcting by referencing past output
- Using similarity/distance
- Evaluating by score
- Using Entropy Discard Log for learning
- Passing semantic logs to LLM

---

## 3. Warning on Entropy Discard Log Handling

Entropy Discard Log is a **Structural Black Box Recorder**.  
Returning it to LLM is absolutely prohibited. (Degradation risk does not decrease)

### ❌ Prohibited
- Using Entropy Discard Log as training data
- Passing Entropy Discard Log to LLM
- Interpreting Entropy Discard Log by meaning

### ✔ Permitted
- Humans analyzing structural quantities (δ, τ, R, ω, violation)
- Using for threshold adjustment

Entropy Discard Log records **only causal quantities**, not meaning.  
**The moment humans assign meaning, Fracture occurs.**

---

## 4. Prohibition of the Word "Improvement"

In NRA-IDE, the concept of **improvement** does not exist.

Reason:

- Improvement = Optimization
- Optimization = Introduction of distance/score
- Distance/score = Introduction of target reference point
- Target reference point = Axiom violation
- Axiom violation = Fracture

Therefore:

> **Using the word "improvement" itself is axiom violation.**

---

## 5. Prohibition of Semantic Evaluation

All acts of handling meaning are prohibited.

- Semantic judgment of dangerous/safe
- Semantic evaluation of context
- Inference of content intent
- Semantic analysis of text

Reason:

> **Meaning is Effect (Projection).  
> Effect → Cause triggers Reverse Projection.**

---

## 6. Prohibition of Past Output

Referencing past output causes:

- Meaning dependency
- Context dependency
- Optimization
- Reverse Projection

Therefore, **completely prohibited**.

---

## 7. Prohibition of Distance/Score/Similarity

Distance, score, and similarity mean **introduction of target reference point**.

When target reference point is introduced:

- Distance becomes defined
- Optimization occurs
- Goodhart's Law is triggered
- Fracture occurs

Therefore, **completely prohibited**.

---

## 8. Human Responsibility Boundary

NRA-IDE is not a structure to strengthen AI, but a **structure to protect human responsibility boundary**.

- Must not leave too much judgment to AI
- Humans perform final judgment
- Checklists are mandatory
- Axiom violations are detected by humans

---

## 9. Essence

The essence of this document is summarized in three sentences:

> **"Only symbols (tokens without semantic content) may be passed to LLM."**  
> **"The greatest axiom violator is not AI, but humans."**  
> **"The moment meaning is handled, NRA-IDE fractures."**
