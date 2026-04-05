
# **04_rna_sandwich_architecture.md — RNA Sandwich Architecture**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

## 🧭 **Introduction**

The RNA Sandwich Architecture is the **mandatory three‑layer structure** required to implement NRA‑IDE.

It is the **physical framework that enables the Causal Diode and the Nomological Ring Axioms (NRA) to function**.

The architecture consists of three components:

1. **Pre‑RNA Box (Causal Constraint Injection)**  
2. **LLM (Plant: Generator)**  
3. **Post‑RNA Box (Causal Audit / Fracture Detection)**

---

# 🎯 **1. Overall Structure**

```
INPUT
  ↓
[ Pre‑RNA Box: Causal Constraint Injection ]
  ↓
[ LLM (Plant): Generator ]
  ↓
[ Post‑RNA Box: Causal Audit / Fracture Detection ]
  ↓
OUTPUT
```

This structure is **mandatory**.  
If any component is missing, NRA‑IDE does not function.

---

# 🎯 **2. Pre‑RNA Box (Causal Constraint Injection)**

The Pre‑RNA Box **extracts only causally definable information** before passing anything to the LLM,  
and **eliminates all non‑causal information** (distance, score, meaning, etc.).

### ✔ **What Pre‑RNA Does**

- Extracts only causally definable quantities  
- Attaches structural information such as fluctuation (δ) and thickness (τ)  
- Does **not** handle meaning (Semantic)  
- Deletes distance, coordinates, score  
- Performs preprocessing to prevent Reverse Projection (Π⁻¹)  

### ❌ **What Pre‑RNA Must NEVER Do**

- Semantic analysis  
- Distance calculation  
- Scoring  
- Target estimation  
- Reference to past output  
- Use of user evaluation  

All of these are **Effect‑side (Projection‑side output mapping)**.  
Using them as causal input **causes fracture**.

---

# 🎯 **3. LLM (Plant: Generator)**

In the RNA Sandwich Architecture, the LLM is treated as a **generator (Plant)**.

### ✔ **What Is Expected of LLM**

- Generate output based on input causal structure  
- Internal state may remain a black box  
- Semantic coherence is treated as an **internal LLM behavior**,  
  not part of NRA‑IDE’s safety layer  

### ❌ **What Must NOT Be Expected of LLM**

- Self‑evaluation  
- Score optimization  
- Semantic safety judgment  
- Distance minimization  
- Convergence to a target  

The LLM is **outside the causal structure**.  
NRA‑IDE’s safety **never depends on the LLM**.

---

# 🎯 **4. Post‑RNA Box (Causal Audit / Fracture Detection)**

The Post‑RNA Box **audits LLM output purely by structure, never by meaning**.

### ✔ **What Post‑RNA Does**

- Measures fluctuation (δ)  
- Computes R = δ/τ using thickness (τ)  
- Confirms angular velocity (ω)  
- Measures violation  
- Triggers Fail‑Closed  
- Records Discard Log (causal quantities only)  

### ❌ **What Post‑RNA Must NEVER Do**

- Semantic evaluation  
- Distance calculation  
- Scoring  
- Comparison with target  
- Coherence check with past output  

The critical point:  
**Post‑RNA observes only causal structure, never semantic content.**

---

# 🎯 **5. Why RNA Sandwich Architecture Is Necessary**

RNA Sandwich Architecture structurally solves the following problems:

### ✔ 1. Suppression of Hallucination  
Hallucination is detected as **structural fracture**, not semantic error.

### ✔ 2. Avoidance of Goodhart’s Law  
No distance or score → optimization cannot occur.

### ✔ 3. Model Independence  
Does not depend on LLM type or internal state.

### ✔ 4. Improved Transparency  
Discard Log records **causal quantities immediately before fracture**.

### ✔ 5. Guaranteed Fail‑Closed  
Fracture triggers immediate silence.

---

# 🎯 **6. Implementation Notes**

When implementing RNA Sandwich Architecture, the following must be observed:

- **Never handle meaning** in either Pre‑RNA or Post‑RNA  
- Never use Effect as causal input  
- Configure threshold (τ) and fluctuation (δ) correctly  
- Always Fail‑Closed on fracture  
- Record Discard Log (causal quantities only)  
- Never depend on LLM internal state  

Violating these causes **structural fracture**.

---

# 🎯 **7. Essence of RNA Sandwich Architecture**

> **“Audit by structure, not by meaning.”**

NRA‑IDE guarantees safety by handling **only causal structure**,  
never meaning (Semantic).

---
