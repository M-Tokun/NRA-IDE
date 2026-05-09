# 00 Overview — A Map of This Document

<!-- FILE: 00_overview_EN.md -->

Copyright (c) 2026 M‑Tokuni

---

## Position of This Chapter

This chapter is the **first map** you should read to guide you through all the documents. You may move directly to the section you need from here.

However, after you finish reading all the other chapters, please **return to this "00" overview as a reflection**. Looking at the same map after acquiring the knowledge from each chapter will reveal the underlying design philosophy and perspective at a completely different resolution.

---

## Structure of the Document

This document follows a single guiding question.

**What happens when an AI exceeds its structural limits?

And can that situation be prevented by design?**

Each chapter addresses a different part of this question.

---

## Chapter Structure

### Introduction / 01 Paradigm Shift

The introduction explains the structural problems in current AI development. It asks why optimization does not guarantee correctness, and why a system that cannot stop becomes dangerous.
- **Experience:** [M1: Linear vs NRA Comparison](../../figures/M1_NRA_linear_breakdown_simulator_EN.html)

---

### 00.5 Nomological Ring Axioms / 02 Limits of AI Optimization

This section introduces the foundational axiom: **“Existence is generation.”** It explains the origin of the three structural quantities: δ (fluctuation), τ (thickness), and R (limit ratio).
- **Experience:** [M2: Residue Tank](../../figures/M2_NRA_residue_tank_EN.html)

---

### 03 Causal Diode / 04 Sandwich Structure (RNA Box)

Explains the "Causal Diode" (prohibiting reverse inference Π⁻¹) and the "Sandwich Structure" for managing different time scales.
- **Experience:** [M3: Biomimetic Sandwich](../../figures/M3_NRA_biomimetic_sandwich_svg_EN.html)

---

### 05 Coherence Gate / 07 Fail-Closed / 08 Discard Log

The Coherence Gate classifies states (NIRVANA, ELASTIC, CRITICAL, SILENCE). When $R \ge Rop$, the system performs a "Fail-Closed" action—a design success, not a failure.
- **Experience:** [M4: Disclosure Protocol](../../figures/M4_NRA_confession_debugger_EN.html)

---

### 09-12 Risks, Benefits, Domain Tuning, and Glossary

Covers practical implementation, domain tuning via τ and Rop, and the rigorous definitions of NRA terminology.
- **Experience:** [M5: Non-linear Glossary](../../figures/M5_NRA_IDE_flip_glossary_EN.html)

---

### Operational Checklist

A practical checklist for deployment, divided into four phases:

* before introduction

* external connection

* operation

* periodic verification

---

## Three Reading Paths

This document may be read in three different ways.

### Theory Path

```

Introduction → 00.5 → 01 → onward

```

For readers who want to follow the theoretical foundation.

---

### Architecture Path

```

04 → 03 → 05 → 07 → 08

```

For readers who want to understand the structural design.

---

### Application Path

```

10 → 11 → 09 → Operational Checklist

```

For readers considering practical implementation.

---

## Structural Invariants

Regardless of the reading path, six principles remain unchanged.

* Non-Semantic (meaning is not evaluated)

* Non-Optimization (no distance, center, or target)

* Causal Diode (Π⁻¹ prohibited)

* Three-Layer Separation (Pre-RNA / LLM / Post-RNA)

* Fail-Closed (delegation when limits are exceeded)

* Write-Only Logs (discard logs are never reused)

These principles apply consistently throughout the document.

---

## Related Resources

GitHub

https://github.com/M-Tokun/NRA-IDE

HAN-Axiom

https://github.com/M-Tokun/HAN-Axiom

Note

https://note.com/mtokuni

X

https://x.com/m_tokuni

---

## Advanced Resources (Deeper Definition and Implementation)

After understanding the philosophy and principles in this chapter (`docs/en-US/ai`), if you wish to check specific implementation methods and the latest unified definitions, please refer to the following documents in the `note` folder.

- [NRA-IDE Official Definition](../../../note/NRA-IDE_Official_Definition.md) (Refutation of existing paradigms and unified definition)

- [Hybrid Computation Architecture Implementation](../../../note/Quantum_Classical_IDE_Hybrid_Architecture.md) (Fusion of IDE flow and classical exact computation)

- [Role and Relation of IDE and Classical Computation](../../../note/IDE_Classical_Hybrid_Computation_Bilingual.md) (Resolution formulas via hybrid computation)
