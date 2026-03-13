
# **07_fail_closed.md — Fail‑Closed**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

# 🎯 **1. Purpose of Fail‑Closed**

Fail‑Closed guarantees:

- **No output in uncertain state**  
- **Immediate stop upon detecting structural fracture**  
- **No regeneration or recovery attempts**  
- **Judgment based solely on structure, never meaning**  
- **Safety guaranteed by causal structure**  

Because NRA‑IDE does not handle meaning, Fail‑Closed audits **only structural fracture**.

---

# 🎯 **2. Conditions That Trigger Fail‑Closed**

Fail‑Closed is triggered when any of the following **causal conditions** are violated.

---

## **1. R (δ/τ) Threshold Exceeded**

```
R = δ / τ
R ≥ 1.0 → Structural Fracture
```

R is a **dynamic causal quantity** that can spike instantaneously.  
Even if the average is low, fracture can occur.

---

## **2. violation Exceeds Threshold**

When structural deviation exceeds the configured value, Fail‑Closed is triggered immediately.

---

## **3. ω (Angular Velocity) Becomes 0**

ω = 0 means **causal dynamics have stopped**.  
This is treated as structural death.

---

## **4. Causal Diode Violation (Reverse Projection Π⁻¹)**

Any detection of Effect → Cause reverse flow is treated as fracture.

---

## **5. Semantic Handling Occurs**

Any attempt to handle meaning (Semantic content)  
→ induces Reverse Projection  
→ triggers Fail‑Closed.

---

# 🎯 **3. Fail‑Closed Behavior**

When Fail‑Closed is triggered, the Post‑RNA Box performs the following actions.

---

### **1. Stop Output (Deliberate Silence)**

- No text output  
- No regeneration  
- No recovery attempts  

Silence is **intentional**, not an error.

---

### **2. Record Discard Log (Causal Quantities Only)**

Recorded items:

- δ (Fluctuation)  
- τ (Thickness)  
- R (Ratio)  
- ω (Angular velocity)  
- violation  
- timestamp  
- rawOutput (hashed if necessary)  

LLM cannot access or modify this log.

---

### **3. Treated as Correct Termination**

Fail‑Closed is **not a failure**.  
It is the state where **safety activated correctly**.

---

# 🎯 **4. What Fail‑Closed Does NOT Handle**

Fail‑Closed **never handles meaning (Semantic)**.

It does **not** handle:

- Dangerous semantic content  
- Ethical or moral judgment  
- Score  
- Distance  
- Evaluation metrics  
- Meaning of past output  

Fail‑Closed **observes only causal structure**.

---

# 🎯 **5. Principle of R_op (Operational Threshold) — NOT Fixed**

This is the most important point.

> **R_op is not a recommended fixed value.  
> It is a variable operational parameter that must be tuned according to occupation, use case, risk level, and operational method.**

### ✔ Determined by “Safety Requirement Level”  
Not by model performance, but by **real‑world risk**.

### ✔ Must Be Tuned by Domain Experts  
Threshold configuration is a **human responsibility**, not an LLM task.

---

# 🎯 **6. R_op by Occupation / Use Case (Reference Bands)**

These are **reference bands**, not fixed values.

| Occupation / Use Case | Reference R_op | Reason |
|------------------------|----------------|--------|
| Medical (Diagnostic Support) | **0.5–0.7** | Maximum life risk. AI is assistant only. |
| Air Traffic Control | **0.55–0.7** | Instant δ spikes cause accidents. |
| Nuclear Reactor Monitoring | **0.5–0.65** | Zero tolerance for fracture. |
| Autonomous Driving Support | **0.55–0.75** | High cost of misjudgment. |
| Contract Review | **0.7–0.85** | High error cost, no life risk. |
| General Text Generation | **0.8–0.9** | Matches typical LLM fluctuation. |
| Creative / Chat | **0.9–0.95** | Fracture is not fatal. |

---

# 🎯 **7. Required Notice for Threshold Configuration (IMPORTANT)**

> **These thresholds are reference values only.  
> Actual operation requires careful adjustment based on use case, risk level, and operational method.  
> Threshold design clarifies “what is left to AI” and “what humans must take responsibility for.”  
> Must NOT be treated as fixed values.**

---

# 🎯 **8. Essence of Fail‑Closed**

> **“If uncertain, Deliberate Silence.”**

And the philosophy of NRA‑IDE:

> **“Not leaving everything to AI, but clarifying human responsibility boundaries, with AI operating as assistant.”**

---
