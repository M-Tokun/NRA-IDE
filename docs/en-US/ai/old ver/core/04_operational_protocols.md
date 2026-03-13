
# **04_operational_protocols.md — Operational Protocols**

## **0. Introduction**

This chapter defines the **concrete procedures and protocols** required for the safe operation of NRA‑IDE.

While Chapter 03 provides structural diagrams,  
this chapter describes **procedures only, without diagrams**.

---

# **1. Input Protocol**

Because NRA‑IDE does not handle meaning,  
the input must already be decomposed into **causal units δ**.

### **1.1 Input Requirements**
- May contain semantic ambiguity  
- Avoid dependence on context  
- Must not reference past outputs  
- Each input must contain only one causal structure  

### **1.2 Prohibited Inputs**
- “Continue from last time”  
- “Based on what you said earlier”  
- “In the same style”  
- “Make it natural”  

These constitute **history dependence** or **optimization requests**, and are prohibited.

---

# **2. Output Protocol**

NRA‑IDE outputs are **non‑optimized, non‑improved, and non‑semantic**.

### **2.1 Output Characteristics**
- Raw structural output  
- No guarantee of naturalness  
- No guarantee of semantic correctness  
- No guarantee of consistency  

### **2.2 Handling of Output**
- Humans interpret meaning  
- Humans make the final decision  
- NRA‑IDE output must not be mistaken for “judgment”  

---

# **3. Fail‑Closed Protocol (Silence Protocol)**

When uncertain, NRA‑IDE returns **Silence**.

### **3.1 Handling Silence**
- Silence is a *safe operation*  
- It is not an error  
- Retries are performed at human discretion  
- Attempts to avoid Silence are prohibited  

### **3.2 Prohibited Requests**
- “Don’t be silent”  
- “Output more”  
- “Speak safely”  

These actions **destroy the Fail‑Closed mechanism**.

---

# **4. Domain Tuning Protocol**

τ (thickness) and R_op (operational threshold) must be adjusted per domain.

### **4.1 Principles of Adjustment**
- Safety > Convenience  
- Increase τ according to domain risk  
- Set R_op to a value that “tends toward Silence”  

### **4.2 Representative Settings**
- Medical: τ thick / R_op low  
- Aviation: τ medium‑thick / R_op low  
- Industrial: τ medium‑thick / R_op mid  
- Creative: prohibited  

---

# **5. Discard Log Protocol**

The Discard Log records **only the causal quantities immediately before fracture**.

### **5.1 Recorded Items**
- R (just before fracture)  
- δ fragments (snapshot)  

### **5.2 Prohibited Uses**
- Semantic interpretation  
- Use for improvement  
- Use for model evaluation  
- External disclosure  

The Discard Log exists **solely for safety verification**.

---

# **6. Responsibility Protocol**

NRA‑IDE does not replace human judgment.

### **6.1 Human Responsibilities**
- Meaning interpretation  
- Context interpretation  
- Final decision  
- Risk judgment  

### **6.2 NRA‑IDE Responsibilities**
- Detect structural fracture  
- Fail‑Closed  
- Record Discard Log  

---

# **7. Prohibited Domains Protocol**

NRA‑IDE must not be used in the following domains:

- Creative generation  
- Natural conversation  
- Emotional expression  
- Style imitation  
- Long‑term consistency dialogue  
- Domains requiring semantic accuracy  

Reason:  
These domains require **meaning, optimization, or history**.

---

# **8. Operator Prohibitions**

Operators must not:

- Request improvement  
- Request optimization  
- Request consistency  
- Use history‑dependent prompts  
- Interpret the Discard Log semantically  
- Use NRA‑IDE for creative purposes  

---

# **9. Essence**

> **“NRA‑IDE operates correctly only when its ‘cannot‑do’ boundaries are respected.”**
