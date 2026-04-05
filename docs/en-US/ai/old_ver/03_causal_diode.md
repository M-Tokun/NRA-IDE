
# **03_causal_diode.md — Causal Diode**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

## 🧭 **Introduction**

The Causal Diode is the **most critical structural component** at the core of NRA‑IDE.

Its role is singular:

> **Guarantee the unidirectionality of Cause → Effect, and structurally prohibit Reverse Projection (Π⁻¹) from Effect → Cause.**

The moment this structure is violated, NRA‑IDE **Fail‑Closes (Deliberate Silence)**.

---

# 🎯 **1. What Is a Causal Diode?**

The Causal Diode is a **structural mechanism that completely separates  
Cause (Causality) from Effect (Projection: Effect‑side output mapping)**.

```
Cause → Effect   ✔ Permitted
Effect → Cause   ❌ Prohibited (Π⁻¹)
```

This unidirectionality **structurally blocks all reverse flow**,  
similar to a diode in electronic circuits—but not metaphorically;  
it is a literal structural rule.

---

# 🎯 **2. Why Reverse Projection (Π⁻¹) Is Dangerous**

Effect (Projection) includes:

- Distance  
- Coordinates  
- Score  
- Evaluation metrics  
- Meaning (Semantic content)  
- User reaction  
- Past output  

All of these are **results, not causality**.

Using Effect as causal input causes:

- Optimization is induced  
- Goodhart’s Law is triggered  
- The model shifts toward maximizing scores  
- Semantic evaluation induces Reverse Projection  
- Structural fracture occurs  

In other words, **safety collapses at the structural level**.

---

# 🎯 **3. What the Causal Diode Permits and Prohibits**

## ✔ **Permitted (Cause Side)**

| Variable | Description |
|----------|-------------|
| φ (Phase) | Causal progression of system state |
| ω (Angular velocity) | Indicates whether causal dynamics are alive |
| δ (Fluctuation) | Boundary‑side fluctuation |
| τ (Thickness) | Structural tolerance band |
| violation | Amount of constraint violation |
| workRate | Rate of causal work (not semantic “task work”) |

All of these are **causally definable quantities**.

---

## ❌ **Prohibited (Effect Side)**

| Variable | Reason |
|----------|--------|
| Distance | Undefined without target reference point |
| Coordinates | Projection, not causality |
| Score | Induces optimization |
| Evaluation metrics | Induce Reverse Projection |
| Meaning (Semantic) | Model‑dependent; destabilizes safety |
| Target position | Introduces target reference point |
| Past output | Primary source of Reverse Projection |

Using Effect as Cause **always causes Fracture**.

---

# 🎯 **4. Causal Diode Diagram**

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   CAUSE (Causality)                 EFFECT (Projection)      │
│   (Causally definable)              (Effect‑side mapping)    │
│                                                              │
│   ┌──────────────┐        Π        ┌──────────────┐         │
│   │ Phase (φ)    │ ─────────────→ │ Distance     │         │
│   │ Fluctuation  │   Allowed      │ Coordinates  │         │
│   │ Thickness    │                │ Score        │         │
│   │ WorkRate     │                │ Meaning      │         │
│   └──────────────┘                └──────────────┘         │
│                          │                                   │
│                          │ Π⁻¹ (PROHIBITED)                  │
│                          ▼                                   │
│         (Reverse Projection is structurally impossible)      │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

# 🎯 **5. What the Causal Diode Protects**

The Causal Diode protects the following structural properties:

### ✔ 1. Prohibition of Optimization  
No distance or score exists → optimization cannot occur.

### ✔ 2. Avoidance of Goodhart’s Law  
No metric exists to “game.”

### ✔ 3. Model Independence  
Effect is not used → works with any LLM.

### ✔ 4. Elimination of Meaning Dependency  
Semantic content is never handled → safety does not waver.

### ✔ 5. Early Detection of Fracture  
Only Cause‑side deviation (violation) is monitored → immediate detection.

---

# 🎯 **6. Implementation Notes**

When implementing the Causal Diode, the following must be observed:

- Never use Effect as causal input  
- Never perform semantic evaluation  
- Never handle distance, coordinates, or score  
- Neither Pre‑RNA nor Post‑RNA may reference Effect  
- Always Fail‑Closed on fracture  
- Record Discard Log (causal quantities only)  

Violating these causes **structural fracture**.

---

# 🎯 **7. Essence of the Causal Diode**

The essence of the Causal Diode is:

> **“Never treat as causal input anything that cannot be defined as causality.”**

Distance, score, and meaning are all **Projection (Effect)**, not causality.

NRA‑IDE guarantees safety by handling **only causal structure**.

