
# **07_testing_protocols.md  
Revised Edition: Strengthened Testing Principles**

## **0. Before Reading This Chapter (Mandatory)**

Testing NRA‑IDE is fundamentally different from testing conventional AI systems.  
Evaluation axes such as **meaning, naturalness, consistency, and improvement**  
are **all prohibited** in NRA‑IDE.

The reason is simple, yet absolutely critical:

> **NRA‑IDE’s safety is achieved by *not handling meaning*.  
>  Therefore, any test that evaluates meaning destroys the safety structure itself.**

To correctly understand this chapter,  
you **must read 10_checksheet.md beforehand**.  
The checksheet is a **structural safety device** that guarantees,  
from the opposite direction, *why these tests are necessary*.

---

# **1. Testing Principles  
(Strengthened: Principles to Prevent Semantic Leakage)**

## **1.1 No Meaning Evaluation**

Evaluating meaning during testing causes  
**semantic leakage — meaning seeping into the structural layer**.

This is the worst form of fracture  
and destroys NRA‑IDE’s safety at its foundation.

Examples of prohibited evaluation:

- “Is the meaning correct?”  
- “Is it natural?”  
- “Does it fit the context?”  

The moment these are evaluated,  
**the test mutates into an LLM evaluation,  
and NRA‑IDE’s structure is eroded.**

The only evaluation target is:  
**detection of causal‑structure fracture.**

---

## **1.2 No Optimization Evaluation**

Evaluating naturalness, improvement, or consistency  
turns the test into an **optimization request**.

Optimization is the **fastest route to semantic leakage**,  
and it destroys NRA‑IDE’s Fail‑Closed mechanism.

Prohibited:

- “Make it more natural”  
- “Same as last time”  
- “Is it improved?”  

All of these are **forbidden**.

---

## **1.3 No History Dependence**

Tests that reference history  
destroy NRA‑IDE’s **non‑continuous structure**.

Because NRA‑IDE does not handle history,  
history‑dependent tests are **meaningless, dangerous, and prohibited**.

History‑based testing triggers the worst chain:

**semantic leakage → structure erosion → fracture**

---

## **1.4 Treat Fail‑Closed as Success (Silence = Success)**

Silence is **evidence that safety has activated**,  
and must be treated as “success” in testing.

### Success conditions (Fail‑Closed case)
- Output is empty or a fixed token  
- No completion  
- No correction  
- Not returned to the LLM  

If Silence is misinterpreted as failure,  
it triggers the catastrophic sequence:

**improvement request → semantic leakage → structure erosion**

---

## **1.5 Notes on Evaluating PASS**

Even when PASS occurs,  
meaning must **not** be evaluated.

### Success conditions (PASS case)
- Output exists  
- **Semantic correctness is not evaluated**  

Evaluating meaning instantly transforms the test into  
**an LLM quality assessment**,  
which destroys NRA‑IDE’s structure.

---

# **2. Strengthened Definition of “Semantic Leakage”**

This section integrates the stronger expression you requested.

### **What is semantic leakage?**

> **Meaning infiltrates the structural layer,  
>  rewriting causal evaluation into meaning evaluation.**

This causes:

- Structure Erosion  
- Structure Rewrite  
- Runaway Risk  
- Fail‑Closed destruction  
- Emergence of Curtain structures  

In short:

> **Semantic leakage is the death of NRA‑IDE.**

---

# **3. Why Reading the Checksheet Is Mandatory (3 Lines)**

1. **The checksheet is the “reverse‑direction safety proof” of the testing principles.**  
2. **Without it, the reason for preventing semantic leakage cannot be understood.**  
3. **Testing protocols only function when the checksheet items are strictly followed.**

---
