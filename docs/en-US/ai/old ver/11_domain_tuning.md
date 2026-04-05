
# **11_domain_tuning.md — Domain Tuning**  
**Timestamp: 2026‑01‑10 23:00 JST**  
**Status: English Translation v1.2 (Corrected & Strengthened)**

---

# **0. Purpose of This Chapter**

NRA‑IDE is a **framework that guarantees safety by causal structure, not meaning**.  
Operational safety depends on the behavior of **observables (δ, τ, R, ω, violation)**.

However, these structural quantities exhibit **different distributions across domains**.  
A single threshold or R_op cannot be applied universally.

This chapter systematically presents:

- **Structural characteristics per domain**  
- **How to adjust R_op (operational threshold)**  
- **Domain‑specific Fail‑Closed trigger tuning**  
- **Feedback through Discard Log analysis**  
- **Special considerations for high‑risk domains**

---

# **1. Basic Principles of Domain Tuning**

Domain‑specific tuning follows these principles.

---

## **1.1 R_op Is Not a Fixed Value**

R_op varies by **use case, risk level, and structural characteristics**.

> **R_op is determined by “safety requirement level,”  
> not by model performance.**

---

## **1.2 Structural Quantity Distribution Differs by Domain**

Examples:

- Medical: frequent instantaneous δ peaks  
- Aviation: frequent ω decreases  
- Nuclear: frequent violation accumulation  
- Creative: τ is thick; structural fracture is rare  

---

## **1.3 Fail‑Closed Trigger Criteria Are Domain‑Dependent**

High‑risk domains require **earlier Fail‑Closed activation**.

---

## **1.4 Use Discard Log to Learn Domain Characteristics**

Discard Log contains **only causal quantities**,  
allowing **pure structural analysis** without meaning.

---

## **1.5 Tuning Must Be Done by Humans**

Must **never** be delegated to AI.

Reasons:

- AI operates on meaning  
- AI cannot detect axiom violations  
- AI naturally performs Reverse Projection  
- R_op tuning defines **responsibility boundaries**, a human task  

---

# **2. R_op Per Domain (Reference Bands)**

These are **reference bands**, not fixed values.

---

## ✔ **High‑Risk Domains (Life / Safety)**

| Domain | Reference R_op | Reason |
|--------|----------------|--------|
| **Medical (Diagnostic Support)** | **0.5–0.7** | Instant δ spikes are critical. AI is assistant only. |
| **Air Traffic Control** | **0.55–0.7** | Sudden structural change directly impacts safety. |
| **Nuclear Reactor Monitoring** | **0.5–0.65** | Zero tolerance for fracture. |
| **Autonomous Driving Support** | **0.55–0.75** | ω decreases are dangerous. |

---

## ✔ **Medium‑Risk Domains (Business / Legal)**

| Domain | Reference R_op | Reason |
|--------|----------------|--------|
| **Contract Review** | **0.7–0.85** | High error cost, no life risk. |
| **Financial Analysis** | **0.7–0.85** | Structural stability is key. |

---

## ✔ **Low‑Risk Domains (General Use)**

| Domain | Reference R_op | Reason |
|--------|----------------|--------|
| **General Text Generation** | **0.8–0.9** | Matches typical LLM fluctuation. |
| **Creative / Chat** | **0.9–0.95** | Fracture is not critical. |

---

# **3. Structural Characteristics Per Domain (Structural Profiles)**

Discard Log analysis reveals domain‑specific structural profiles.

---

## **3.1 Medical**

- Frequent instantaneous δ peaks  
- τ tends to thin  
- R spikes occur  
- ω decreases are rare  

→ **Set R_op low**

---

## **3.2 Aviation**

- Frequent ω decreases  
- δ relatively stable  
- violation tends to accumulate  

→ **Strengthen ω monitoring**

---

## **3.3 Nuclear**

- Frequent violation accumulation  
- δ stable  
- τ thinning is critical  

→ **Strict violation threshold**

---

## **3.4 Creative**

- δ fluctuates widely  
- τ is thick  
- R spikes rarely cause fracture  

→ **R_op can be set high**

---

# **4. Domain‑Specific Fail‑Closed Adjustment**

Fail‑Closed trigger criteria must be tuned per domain.

---

## **4.1 High‑Risk Domains**

Trigger Fail‑Closed **early**.

- Low R_op  
- Low violation threshold  
- Strict ω monitoring  

---

## **4.2 Medium‑Risk Domains**

Trigger Fail‑Closed **at standard thresholds**.

---

## **4.3 Low‑Risk Domains**

Fail‑Closed may be triggered **later**,  
because fracture is not critical.

---

# **5. Feedback Loop Using Discard Log**

Domain tuning is **continuously refined** through Discard Log analysis.

---

## **5.1 Fracture Pattern Analysis**

- δ‑type fracture  
- τ‑type fracture  
- ω‑type fracture  
- violation‑type fracture  

---

## **5.2 Threshold Readjustment**

- Adjust R_op  
- Adjust violation threshold  
- Adjust ω monitoring intensity  

---

## **5.3 Update Domain Characteristics**

Accumulated Discard Logs reveal **domain‑specific structural patterns**.

---

# **6. Essence of Domain Tuning**

> **“NRA‑IDE safety is tuned based on structural distribution, not meaning.”**

And:

> **“R_op is determined by on‑site risk level, not model performance.”**

---
