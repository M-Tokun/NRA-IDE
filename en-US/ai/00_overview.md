
## **0. Purpose of This Document**

This document serves as the **initial entry point** to the NRA‑IDE  
(Nomological Ring Axioms – Intensional Dynamics Engine),  
clarifying the *prerequisites*, *prohibitions*, and *structural stance*  
required to read the subsequent chapters.

NRA‑IDE is not an extension of conventional AI safety techniques.  
It is a **paradigm shift that requires abandoning the previous assumptions**.

Therefore, this document first defines  
the **“forbidden operations”**,  
preventing readers from proceeding with incorrect assumptions.

Detailed explanations are provided in later chapters.

---

## **0.5 Paradigm Shift (Abandoning Conventional Assumptions)**

NRA‑IDE handles neither meaning nor inference.  
It deals solely with the causal structure of reality itself.  
Proofs and experiments are unnecessary; doing it is sufficient.  
Only strict adjustment is required.

To understand NRA‑IDE,  
**one must reset the existing assumptions  
(distance, coordinates, meaning, optimization).**

Conventional AI safety relied on:

- distance  
- scores  
- similarity  
- semantic analysis  
- optimization  
- guardrails  
- RLHF  

These are all **Effects (projections)**.

In contrast, NRA‑IDE operates under completely different premises:

- no center  
- no definable distance  
- no semantics  
- no optimization  
- prohibition of reverse derivation (Π⁻¹)  

---

## **0.6 (Important) Overview of Prohibited Operations**  
*See **13_warning.md** for details.*

The following inputs, operations, and judgments  
are strictly prohibited in NRA‑IDE,  
as they cause **structural fracture**.

### ❌ Prohibited (Effect / Semantic)

- words, phrases, sentences  
- meaning (semantics)  
- evaluative terms (safe, dangerous, correct, wrong, etc.)  
- distance, scores, similarity  
- past outputs  
- “improvement” (optimization)  
- using semantic logs for training  
- feeding Discard Logs back into the LLM  

These are all **Effects (projections)**.  
Passing them to the LLM induces **reverse derivation (Effect → Cause)**  
and destroys the structural safety of NRA‑IDE.

### ✔ Allowed (Cause / Structure)

- symbols  
  - [], {}, (), <>, =, +, -, *, /, etc.  
- numerical values  
- causal observables (δ, τ, R, ω, violation, workRate)  
- structural operators  

**Only symbols may be passed to the LLM.**  
Details are defined in **13_warning.md**.

---

## **1. Overview of NRA‑IDE (Entrance to Structure)**

NRA‑IDE is an engine that provides  
**causal‑structural safety** to large language models  
from the outside.

Unlike conventional “semantic‑based safety,”  
NRA‑IDE handles **only causal structure**.

This enables:

- structural suppression of hallucinations  
- Fail‑Closed behavior (silence under uncertainty)  
- complete prohibition of reverse derivation (Π⁻¹)  
- transparency via thermal discard logs  
- model‑independent safety  

---

## **2. Basic Structure: The RNA Sandwich Architecture**

NRA‑IDE operates through the following three‑layer structure:

```
INPUT
  ↓
[ Pre‑RNA Box: injection of causal constraints ]
  ↓
[ LLM (Plant): generator ]
  ↓
[ Post‑RNA Box: causal audit / fracture detection ]
  ↓
OUTPUT
```

### Pre‑RNA  
- no semantics  
- no distance or scores  
- passes only causal quantities  

### LLM (Plant)  
- internal state is a black box  
- semantic coherence is left to the LLM  
- safety is *not* left to the LLM  

### Post‑RNA  
- no semantic evaluation  
- audits only structural deviation  
- Fail‑Closed on fracture  

---

## **3. Problems Solved by NRA‑IDE (Structural Perspective)**

### ✔ Hallucination  
Detected as **structural fracture**, not semantic error.

### ✔ Reduced Black‑Box Nature  
Discard Logs expose causal quantities near fracture.

### ✔ Model Independence  
No semantics → applicable to any LLM.

---

## **4. Operational Notes (Required Reading)**

- Never operate without the RNA Sandwich structure  
- Incorrect δ / τ thresholds are dangerous  
- Semantic evaluation causes structural fracture  
- Reverse derivation (Π⁻¹) is a violation of the axioms  
- Fail‑Closed is not an error but a specification  

---

## **5. Document Structure (Table of Contents)**

```
00_overview.md
01_paradigm_shift.md
02_nomological_ring_axioms.md
03_causal_diode.md
04_rna_sandwich_architecture.md
05_coherence_gate.md
06_observables.md
07_fail_closed.md
08_discard_logs.md
09_risks_and_misuse.md
10_benefits_and_limitations.md
11_domain_tuning.md
12_glossary.md
- developer_warning-note.md (independent file)
```

---

## **6. Essence**

> **“NRA‑IDE handles causal structure, not meaning.”**  
> **“Only symbols may be passed to the LLM.”**  
> **“The primary axiom violator is not the AI, but the human.”**
