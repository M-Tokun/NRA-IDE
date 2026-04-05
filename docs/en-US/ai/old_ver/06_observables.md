
# **06_observables.md — Observables**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

## 🧭 **Introduction**

The quantities NRA‑IDE is permitted to handle are limited to **Causally Definable Quantities (Causal Observables)**.

Conversely, **quantities belonging to Effect (Projection: Effect‑side output mapping) must never be handled** — this is a fundamental principle of the Nomological Ring Axioms (NRA).

This document defines the **“Observables”** NRA‑IDE may handle and the **“Prohibited Quantities”** it must never handle.

---

# 🎯 **1. Observables (Allowed)**

The following are **causally definable quantities** that NRA‑IDE is permitted to handle.

---

## **1. φ (Phase)**

- Causal quantity representing system progression  
- Indicates temporal continuity  
- Independent of meaning or score  

**Use:**  
Internal state management of Pre‑RNA / Post‑RNA

---

## **2. ω (Angular Velocity)**

- Indicates whether causal dynamics are “alive”  
- Rate of phase change  
- Zero indicates possible fracture  

**Use:**  
Early fracture detection

---

## **3. δ (Fluctuation)**

- Boundary‑side fluctuation  
- Independent of LLM semantic output  
- Represents structural vibration, not meaning  

**Use:**  
Calculation of R = δ/τ in Coherence Gate

---

## **4. τ (Thickness)**

- Structural tolerance band  
- Reference quantity compared with δ  
- Proper configuration is prerequisite for Fail‑Closed  

**Use:**  
Standard for structural safety

---

## **5. R (Ratio)**

```
R = δ / τ
```

- Central quantity of Coherence Gate  
- Fail‑Closed at **R ≥ 1.0**  

**Use:**  
Fracture detection

---

## **6. violation**

- Degree of deviation from structural constraint  
- Purely structural, not semantic  
- Fail‑Closed when threshold exceeded  

**Use:**  
Post‑RNA audit

---

## **7. workRate**

- Indicates whether the system is **causally performing work**  
- Represents causal change, not semantic “task work”  

**Use:**  
Detection of abnormal stop

---

# 🎯 **2. Prohibited Quantities (Forbidden Observables)**

The following belong to **Effect (Projection)** and must **never** be handled as causal input.

---

## ❌ **1. Distance**

- Undefined without target reference point  
- Using distance induces optimization  

---

## ❌ **2. Coordinates**

- Projection, not causality  
- Primary source of Reverse Projection (Π⁻¹)  

---

## ❌ **3. Score**

- Triggers Goodhart’s Law  
- Causes metric‑seeking behavior  

---

## ❌ **4. Meaning (Semantic)**

- Model‑dependent  
- Safety becomes unstable  
- Triggers Reverse Projection  

---

## ❌ **5. Evaluation Metrics**

- Induce Effect → Cause reverse flow  
- Violates the Causal Diode  

---

## ❌ **6. Past Output (History)**

- Breeding ground for Reverse Projection  
- Creates meaning‑dependent loops  

---

## ❌ **7. Target Position**

- Introduces target reference point  
- Distance becomes defined → optimization occurs  

---

# 🎯 **3. Essence of Observables**

> **“Handle only quantities definable as causality; never handle quantities not definable as causality.”**

Distance, score, and meaning are all **Projection (Effect)**.  
Treating them as causal input **causes fracture**.

---

# 🎯 **4. Implementation Notes**

Developers must observe the following:

- Never perform semantic analysis  
- Never handle distance or score  
- Never use Effect as causal input  
- Calculation of δ and τ is mandatory  
- Fail‑Closed at **R ≥ 1.0**  
- Record Discard Log (causal quantities only)  

Violating these causes **structural fracture**.

---
