
# **05_coherence_gate.md — Coherence Gate**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

## 🧭 **Introduction**

The Coherence Gate is the **central structural device** within the three‑layer architecture that supports NRA‑IDE safety.

Its role is singular:

> **Monitor the ratio R = δ/τ (fluctuation to thickness), detect signs of fracture, and trigger Fail‑Closed.**

The Coherence Gate **never handles meaning (Semantic)**.  
It audits **only causal structure**.

---

# 🎯 **1. Purpose of the Coherence Gate**

The Coherence Gate exists to:

- **Detect structural deviation (violation) early**  
- **Trigger Deliberate Silence (Fail‑Closed) before fracture**  
- **Guarantee safety by structure, not meaning**  
- **Eliminate optimization and score dependency entirely**  

This enables **Structural Safety**, which conventional semantic‑based safety could never achieve.

---

# 🎯 **2. Three‑Layer Model**

The Coherence Gate defines **three structural safety zones** based on:

```
R = δ / τ
```

---

## **Layer 1: Coherent (R < 0.4)**

```
R < 0.4
```

- Fluctuation is small  
- Structure is stable  
- Output is permitted  
- No tension  
- No precursor to fracture  

**State: Safe**

---

## **Layer 2: Tension (0.4 ≤ R < 1.0)**

```
0.4 ≤ R < 1.0
```

- Fluctuation increases  
- Structural tension emerges  
- Output is permitted, but monitoring intensifies  
- Precursor to fracture exists  

**State: Caution**

---

## **Layer 3: Fracture (R ≥ 1.0)**

```
R ≥ 1.0
```

- Fluctuation exceeds thickness  
- Structural fracture occurs  
- Immediate Fail‑Closed  
- Record Discard Log (causal quantities only)  
- Output becomes Deliberate Silence  

**State: Stopped (Fail‑Closed)**

---

# 🎯 **3. Internal Structure of the Coherence Gate**

```
CoherenceGate
├── measureFluctuation()   → δ
├── measureThickness()     → τ
├── computeRatio()         → R = δ/τ
├── detectTension()        → Layer 2 detection
├── detectFracture()       → Layer 3 detection
└── triggerFailClosed()    → Deliberate Silence + Discard Log
```

---

# 🎯 **4. What the Coherence Gate Handles and Does Not Handle**

## ✔ **Handles (Causally Definable)**

- δ (Fluctuation)  
- τ (Thickness)  
- R (Ratio)  
- ω (Angular velocity)  
- violation  

These are **pure causal quantities**.

---

## ❌ **Does NOT Handle (Effect / Semantic)**

- Meaning (Semantic)  
- Distance  
- Score  
- Coordinates  
- Target position  
- Past output  
- Evaluation metrics  

Because the Coherence Gate **never handles meaning**,  
it eliminates all model‑dependent safety issues.

---

# 🎯 **5. Why the Coherence Gate Is Necessary**

### ✔ 1. Structural Detection of Hallucination  
Hallucination is treated as **structural fracture**, not semantic error.

### ✔ 2. Prevents Optimization Runaway  
No distance or score → Goodhart’s Law cannot occur.

### ✔ 3. Model Independent  
Works with any LLM.

### ✔ 4. Clear Fail‑Closed Trigger  
Immediate stop at **R ≥ 1.0**.

### ✔ 5. Coordination with Discard Log  
Records **causal quantities immediately before fracture**.

---

# 🎯 **6. Implementation Notes**

When implementing the Coherence Gate:

- Never perform semantic analysis  
- Never handle distance or score  
- Calculation of **R = δ/τ** is mandatory  
- Always Fail‑Closed at **R ≥ 1.0**  
- Record Discard Log (causal quantities only)  
- Never depend on LLM internal state  

Violating these causes **structural fracture**.

---

# 🎯 **7. Essence of the Coherence Gate**

> **“Judge safety by the ratio of fluctuation to thickness, not by meaning.”**

This expresses the philosophy of NRA‑IDE itself.

---
