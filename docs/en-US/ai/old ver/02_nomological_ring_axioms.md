
# **02_nomological_ring_axioms.md — Nomological Ring Axioms (NRA)**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

## 🧭 **Introduction**

The Nomological Ring Axioms (NRA) constitute the **minimal axiom system for causal structure** that governs all behavior of NRA‑IDE.

NRA‑IDE **controls causal structure itself**, not “optimization” or “meaning.”  
Therefore, its assumptions differ fundamentally from conventional AI safety.

The Nomological Ring Axioms define, **mathematically and structurally**,  
**what is permitted and what is prohibited**.

---

# 🎯 **1. Purpose of NRA: Preventing Causal‑Structure Fracture**

The purpose of the Nomological Ring Axioms is singular:

> **Prevent fracture of causal structure, and immediately silence (Fail‑Closed) when fracture occurs.**

To achieve this, NRA strictly distinguishes three domains:

- **Cause (Causality)**  
- **Effect (Projection: Effect‑side output mapping)**  
- **Boundary (Constraint)**  

NRA‑IDE handles **only Cause and Boundary**.  
Effect is **completely separated**.

---

# 🎯 **2. Three Principles of NRA (Minimal Axioms)**

The Nomological Ring Axioms consist of the following three principles.

---

## **Axiom 1: Causal Diode**

### **Cause → Effect is permitted.  
Effect → Cause is structurally prohibited.**

This prohibits **Π⁻¹ (Reverse Projection)** at the structural level.

### ✔ **Permitted (Causally definable quantities)**  
- Phase (φ)  
- Fluctuation (δ)  
- Thickness (τ)  
- Angular velocity (ω)  
- Violation  

### ❌ **Prohibited (Effect‑side / Projection)**  
- Distance  
- Coordinates  
- Score  
- Target position  
- Evaluation value  
- Meaning (Semantic content)  

Effect is **Projection**, not causality.  
Using it as causal input **causes fracture**.

---

## **Axiom 2: No Target Reference Point (No‑Center Axiom)**

### **No target reference point (Center) exists.  
Therefore, distance cannot be defined.**

Conventional AI presumes a “target reference point (goal/center).”  
NRA‑IDE adopts a structure with **no target reference point**:

```
No Target Reference Point → Distance Undefined → Optimization Impossible
```

What exists is only **Boundary (Constraint)**.

Boundary has:

- Thickness (τ)  
- Fluctuation (δ)  
- Dynamic variation  

And only **“inside or outside”** is determined.

---

## **Axiom 3: Structural Invariants**

NRA‑IDE must always satisfy the following invariants:

1. **R = δ / τ < 1.0**  
2. **ω > 0 (Phase generation continues)**  
3. **Fail‑Closed when violation exceeds threshold**  
4. **No semantic evaluation**  
5. **No use of Effect as causal input**  

If any invariant is violated, NRA‑IDE **immediately silences (Fail‑Closed)**.

---

# 🎯 **3. Why NRA Is Necessary**

The Nomological Ring Axioms are required to solve structural problems inherent in conventional AI.

### ❌ Using distance induces optimization  
→ Goodhart’s Law is triggered

### ❌ Using score induces gaming  
→ Model maximizes score instead of safety

### ❌ Handling meaning induces Reverse Projection  
→ Safety becomes model‑dependent

### ❌ Having a target reference point defines distance  
→ Optimization becomes unavoidable

NRA **structurally prohibits** all of these.

---

# 🎯 **4. Relationship Between NRA and RNA Sandwich Architecture**

The Nomological Ring Axioms are the **foundational principles** of the RNA Sandwich Architecture:

```
Pre‑RNA → LLM (Plant) → Post‑RNA
```

- Pre‑RNA performs **causal constraint injection**  
- Post‑RNA performs **causal audit and fracture detection**  

Both comply with NRA because they **do not handle Effect**.

---

# 🎯 **5. Implementation Notes for NRA**

The Nomological Ring Axioms are **implementation constraints**, not philosophy.

The following must be observed:

- Do not use distance, coordinates, or score as input  
- Do not perform semantic evaluation  
- Do not use Effect as causal input  
- Configure threshold (τ) and fluctuation (δ) correctly  
- Always Fail‑Closed on fracture  
- Record Discard Log (causal quantities only)  

Failure to observe these causes **structural fracture**.

---

# 🎯 **6. Essence of NRA**

The essence of the Nomological Ring Axioms is:

> **“To protect causal structure, never handle anything that cannot be defined as causality.”**

Distance, score, and meaning are all **Projection (Effect)**, not causality.

NRA‑IDE guarantees safety by handling **only causal structure**.

---