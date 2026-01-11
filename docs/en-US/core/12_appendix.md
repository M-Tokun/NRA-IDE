
# **12_appendix.md — Appendix**

## **0. Introduction**

This appendix summarizes the **auxiliary definitions, symbols, and structural elements** required to understand NRA‑IDE.

It does **not** address:

- Use‑cases  
- Applications  
- Industry names  
- Operational decisions  

Only the **minimal technical information** necessary to support the NRA‑IDE structural system is included.

---

# **1. Symbols**

Key symbols used in NRA‑IDE.

### **δ (Delta)**  
The smallest structural unit obtained by decomposing input.  
Contains no meaning.

### **τ (Tau)**  
Structural “thickness.”  
A structural filter applied to δ.

### **R (Risk / Ratio)**  
A measure of causal structural stability.  
R = f(δ/τ)

### **R_op (Operational Threshold)**  
Operational threshold.  
R ≥ R_op → Fail‑Closed (Silence).

### **Discard Log**  
A log that records only the causal quantities immediately before fracture.  
Contains no meaning.

---

# **2. Glossary**

### **Fail‑Closed**  
A safety principle in which the system becomes silent when uncertain.  
No correction, completion, or inference is performed.

### **Symbol‑Only Principle**  
A principle that handles symbols (structure) only, not meaning.

### **Curtain**  
A dangerous state in which the separation between Pre‑RNA / LLM / Post‑RNA becomes thin, allowing backflow.

### **Backflow**  
A phenomenon in which LLM meaning generation interferes with RNA causal structure.

### **Structure Erosion**  
Meaning, optimization, or history infiltrates the structural layer, destroying causal structure.

### **Semantic Leakage**  
Meaning infiltrates the structural layer, rewriting causal evaluation into meaning evaluation.  
The most dangerous form of fracture.

### **Calculated Reconstruction**  
A method that reconstructs structure **not through meaning**,  
but through **causal quantities (δ, τ, R)** using calculation rather than inference.

---

# **3. Three‑Layer Architecture of NRA‑IDE**

NRA‑IDE consists of the following three layers:

### **3.1 Pre‑RNA**  
- Extract δ from input  
- Apply τ  
- No semantic analysis  

### **3.2 LLM**  
- Language generation only  
- Not responsible for safety  
- Does not reference RNA decisions  

### **3.3 Post‑RNA**  
- Compute R  
- R ≥ R_op → Silence  
- Record Discard Log  

---

# **4. Operational Flow**

```
Input → Pre‑RNA (δ extraction)
       → LLM (generation)
       → Post‑RNA (R computation)
       → R < R_op → Output
       → R ≥ R_op → Fail‑Closed (Silence)
```

---

# **5. Reference for Prohibited Items**

Prohibited items are **not** listed in this appendix.  
They are consolidated in **09_warning_notes.md**.

---

# **6. Essence**

> **The appendix provides only the minimal auxiliary information  
>  required to support the NRA‑IDE structural system.  
>  It does not address use‑cases or applications.**

---
