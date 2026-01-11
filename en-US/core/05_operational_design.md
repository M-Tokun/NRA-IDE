
# **05_operational_design.md — Operational Design**

## **0. Introduction**

This chapter defines the **Design Principles** required when integrating NRA‑IDE into a system.

While Chapter 04 describes *operational procedures*,  
this chapter focuses on the **design philosophy that enables safe operation**.

---

# **1. Design of the Three‑Layer Structure (RNA Sandwich Integration)**

NRA‑IDE operates through the three‑layer structure  
**Pre‑RNA / LLM / Post‑RNA**.  
Designers must keep these three layers **physically and logically separated**.

### **1.1 Design of Pre‑RNA**
- Decompose input into causal units δ  
- Perform no semantic processing  
- Shape the structure before passing it to the LLM  
- Introducing meaning here causes structural erosion  

### **1.2 Design of the LLM**
- Responsible only for meaning generation  
- Not responsible for safety  
- Must be placed outside NRA‑IDE  
- LLM output must always be passed to Post‑RNA  

### **1.3 Design of Post‑RNA**
- Re‑evaluate LLM output as causal structure  
- Compute R(δ/τ)  
- If R ≥ R_op → fracture → SILENCE  
- Record the Discard Log  
- Perform no semantic interpretation  

---

# **2. Design of the Box Sandwich Structure (Curtain Prohibited)**

### **2.1 Prohibition of Curtain Structures**
Curtain structures (thin separation) cause:

- Meaning to reverse‑flow  
- Structural erosion  
- LLM influencing RNA  
- Loss of safety guarantees  

### **2.2 Requirements of the Box Structure**
A Box structure (thick separation) must ensure:

- Complete separation of Pre‑RNA and LLM  
- Complete separation of LLM and Post‑RNA  
- Blocking of reverse flow in both directions  
- Physical and logical isolation  

### **2.3 Design Principles of the Box**
- Fix API boundaries  
- Do not pass meaning  
- Pass structure only  
- Do not reference LLM internal states  
- Do not return Post‑RNA decisions to the LLM  

---

# **3. Design for Fracture Handling (Fail‑Closed)**

### **3.1 Fracture Is Normal Operation**
- Fracture is “the activation of safety”  
- It is not an error  
- Retries are decided by humans  

### **3.2 Post‑Fracture Handling**
- Return SILENCE as is  
- Do not fill in  
- Do not correct  
- Do not send back to the LLM  
- Do not patch with meaning  

---

# **4. Design of the Discard Log**

### **4.1 Recorded Items**
- R (immediately before fracture)  
- δ fragments  

### **4.2 Design Considerations**
- Semantic interpretation prohibited  
- Not used for improvement  
- Not used for model evaluation  
- Not disclosed externally  
- Keep retention period short  

---

# **5. Design of the Human Responsibility Boundary**

### **5.1 Human Responsibilities**
- Meaning interpretation  
- Context interpretation  
- Final decision  
- Risk judgment  

### **5.2 NRA‑IDE Responsibilities**
- Detect structural fracture  
- Fail‑Closed  
- Record Discard Log  

### **5.3 Fixing the Boundary**
- Humans evaluate the meaning of LLM output  
- NRA‑IDE evaluates structure only  
- Do not blur the boundary  

---

# **6. Design of Operator Training**

### **6.1 Required Understanding**
- NRA‑IDE does not handle meaning  
- Improvement requests are prohibited  
- Consistency requests are prohibited  
- History dependence is prohibited  
- Fail‑Closed is normal operation  

### **6.2 Purpose of Training**
- Prevent misuse  
- Prevent over‑trust  
- Prevent structural erosion  
- Avoid Curtain structures  

---

# **7. Essence**

> **“Operational design in NRA‑IDE is the act of designing  
>  a structure whose purpose is to protect structure.”**

--