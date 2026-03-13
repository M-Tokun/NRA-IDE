
# **06_implementation_guidelines.md  
Implementation Guidelines**

## **0. Introduction**

This chapter defines the **implementation guidelines** required to integrate NRA‑IDE into an actual system.

Intended readers:

- System architects  
- Implementation engineers  
- Developers in safety‑critical domains  
- LLM integration engineers  

This chapter provides the **minimum requirements for implementation**.  
For detailed structural design, refer to Chapter 03 (Structural Grand Compendium).

---

# **1. Implementation Requirements for the Three‑Layer Structure (RNA Sandwich Implementation)**

NRA‑IDE operates through the three‑layer structure  
**Pre‑RNA / LLM / Post‑RNA**.  
Implementers must keep these layers **physically and logically separated**.

## **1.1 Pre‑RNA Implementation Requirements**
- Decompose input into causal units δ  
- Perform no semantic analysis  
- Shape the structure before passing it to the LLM  
- Input normalization is allowed, but semantic completion is prohibited  
- Must not reference past outputs  

## **1.2 LLM Implementation Requirements**
- Responsible only for meaning generation  
- Not responsible for safety  
- LLM output must always be passed to Post‑RNA  
- LLM must not access internal states of Pre‑RNA or Post‑RNA  

## **1.3 Post‑RNA Implementation Requirements**
- Re‑evaluate LLM output as causal structure  
- Compute R(δ/τ)  
- If R ≥ R_op → fracture → SILENCE  
- Record the Discard Log  
- Perform no semantic analysis  
- Do not return feedback to the LLM  

---

# **2. Implementation of the Box Sandwich Structure (Curtain Prohibited)**

## **2.1 Prohibition of Curtain Structures**

The following configurations are considered **Curtain structures** and are prohibited:

- Pre‑RNA and LLM running in the same process  
- Post‑RNA referencing LLM internal states  
- LLM using Post‑RNA decisions  
- Bidirectional data flow  

These cause **Structure Erosion**.

## **2.2 Box Structure Implementation Requirements**
- Separate Pre‑RNA / LLM / Post‑RNA into different processes or containers  
- Fix API boundaries and prohibit bidirectional communication  
- Do not expose LLM internal states  
- Do not return Post‑RNA decisions to the LLM  
- Do not pass semantic data into structural layers  

## **2.3 Recommended Implementation**
- Pre‑RNA: lightweight structural extraction module  
- LLM: external API or isolated inference server  
- Post‑RNA: independent safety evaluation module  
- Only **structural data** may pass between the three layers  

---

# **3. Implementation of Fail‑Closed (Silence Handling)**

## **3.1 SILENCE Implementation Requirements**
- On fracture, return **empty output** or a **fixed token**  
- Do not fill in  
- Do not correct  
- Do not send back to the LLM  
- Do not patch with meaning  

## **3.2 Handling Retries**
- Retries are decided by humans  
- Automatic retries are prohibited  
- Retries must not reference history  

---

# **4. Implementation of the Discard Log**

## **4.1 Recording Requirements**
- R (immediately before fracture)  
- δ fragments (snapshot)  
- Timestamp  

## **4.2 Prohibited Uses**
- Semantic interpretation  
- Use for improvement  
- Use for model evaluation  
- External disclosure  

## **4.3 Storage Requirements**
- Keep retention period short  
- Store encrypted  
- Do not share with external systems  

---

# **5. Implementation of Domain Tuning**

## **5.1 Setting τ (Thickness)**
- Set according to domain risk  
- Medical / aviation: thick  
- Industrial: medium‑thick  
- Creative: prohibited  

## **5.2 Setting R_op (Operational Threshold)**
- Lower values increase safety  
- Higher values reduce Silence but increase risk  
- Default should be “Silence‑prone”  

---

# **6. Implementation of Responsibility Boundaries**

## **6.1 Human Responsibilities**
- Meaning interpretation  
- Context interpretation  
- Final decision  
- Risk judgment  

## **6.2 System Responsibilities**
- Detect structural fracture  
- Fail‑Closed  
- Record Discard Log  

## **6.3 Fixing the Boundary**
- Pass LLM output directly to humans  
- NRA‑IDE evaluates structure only  
- Do not mix LLM and NRA‑IDE responsibilities  

---

# **7. Implementation Testing Requirements**

## **7.1 Required Tests**
- Fracture test  
- Backflow test  
- Curtain structure detection test  
- Domain‑specific τ and R_op tests  
- Fail‑Closed verification  

## **7.2 Prohibited Tests**
- Semantic evaluation tests  
- Naturalness tests  
- Consistency tests  
- Improvement tests  

---

# **8. Essence**

> **“Implementing NRA‑IDE is the act of building  
>  a structure whose purpose is to prevent meaning from entering.”**

---
