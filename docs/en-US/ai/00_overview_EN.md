# 00 Overview — A Map of This Document



<!-- FILE: 00_overview_EN.md -->



Copyright (c) 2026 M‑Tokuni



---



## Position of This Chapter



This chapter is the **first map** you should read to guide you through all the documents. You may move directly to the section you need from here.



However, after you finish reading all the other chapters, please **return to this "00" overview as a reflection**. Looking at the same map after acquiring the knowledge from each chapter will reveal the underlying design philosophy and perspective at a completely different resolution.



---



## Structure of the Document



This document follows a single guiding question.



**What happens when an AI exceeds its structural limits?

And can that situation be prevented by design?**



Each chapter addresses a different part of this question.



---



## Chapter Structure



### Introduction



The introduction explains the structural problems in current AI development.

It asks why optimization does not guarantee correctness, and why a system that cannot stop becomes dangerous.



---



### 00.5 Nomological Ring Axioms



This section introduces the foundational axiom from which NRA-IDE emerges.



**“Existence is generation.”**



This axiom appears only once, before the computational principles begin.



---



### 01 Paradigm Shift



This chapter explains what is overlooked in the architecture used by current AI systems—floating-point computation, probability, and optimization.



See figure:

`figures/01_Code_Generated_Image_.jpg`



---



### 02 Limits of AI Optimization



Here the computational principles derived from the axiom are expanded.



The origin of the three quantities



* δ (fluctuation)

* τ (structural thickness)

* R (limit ratio)



is explained.



---



### 03 Causal Diode



This chapter introduces a structural rule in which information flows only from cause to effect.



Reverse derivation (Π⁻¹) is prohibited.



See figure:

`figures/fig2_causal_diode.png`



---



### 04 Sandwich Structure (RNA Box)



This chapter explains the three-layer separation:



Pre-RNA / LLM / Post-RNA



and why the LLM must be placed between these structural layers.



See figures:



```

figures/RNA Box Sandwich Architecture_EN.jpg

figures/sandwich_architecture.html

```



---



### 05 Coherence Gate



The coherence gate classifies structural states using the formula:



```

R = δ / τ

```



The structure is divided into four states:



* NIRVANA

* ELASTIC

* CRITICAL

* SILENCE



See figure:

`figures/fig3_coherence_gate.png`



---



### 06 Observables



This chapter distinguishes between two categories of quantities.



Cause-Side observables



```

δ τ R ω C

```



and Effect-Side quantities



```

distance

score

similarity

```



Only Cause-Side quantities are permitted in computation.



See figure:

`figures/nra_dam_degradation_20260310_EN.html`



---



### 07 Fail-Closed



When



```

R ≥ Rop

```



the structure stops producing output and delegates the decision to the next agent.



This is not a failure.

It is the intended structural behavior.



---



### 08 Discard Log



This chapter explains how records are kept without re-using them for computation.



The system records



* structural state

* discarded residuals



while preventing reverse inference.



---



### 09 Risks and Misuse



Four major misuse patterns are explained:



* manipulation of τ

* tampering with logs

* removal of the sandwich structure

* mixing with external computational systems



The earliest risk appears **before a value enters NRA-IDE**.



---



### 10 Benefits and Limitations



This chapter honestly separates what NRA-IDE can guarantee and what it cannot.



Situations where Fail-Closed is valuable are distinguished from those where it is unsuitable.



---



### 11 Domain Tuning



NRA-IDE adapts to different domains by adjusting only two parameters:



```

τ

Rop

```



The structure itself does not change.



See figures:



```

figures/DOMAIN_TUNIING.png

figures/domain_tuning_structure_pure.html

```



---



### 12 Glossary



A reference section containing definitions for all terms used in the document.



Readers who begin in the middle of the text may consult this section first.



---



### Operational Checklist



A practical checklist for deployment, divided into four phases:



* before introduction

* external connection

* operation

* periodic verification



---



## Three Reading Paths



This document may be read in three different ways.



### Theory Path



```

Introduction → 00.5 → 01 → onward

```



For readers who want to follow the theoretical foundation.



---



### Architecture Path



```

04 → 03 → 05 → 07 → 08

```



For readers who want to understand the structural design.



---



### Application Path



```

10 → 11 → 09 → Operational Checklist

```



For readers considering practical implementation.



---



## Structural Invariants



Regardless of the reading path, six principles remain unchanged.



* Non-Semantic (meaning is not evaluated)

* Non-Optimization (no distance, center, or target)

* Causal Diode (Π⁻¹ prohibited)

* Three-Layer Separation (Pre-RNA / LLM / Post-RNA)

* Fail-Closed (delegation when limits are exceeded)

* Write-Only Logs (discard logs are never reused)



These principles apply consistently throughout the document.



---



## Related Resources



GitHub

https://github.com/M-Tokun/NRA-IDE



HAN-Axiom

https://github.com/M-Tokun/HAN-Axiom



Note

https://note.com/mtokuni



X

https://x.com/m_tokuni



---



## Advanced Resources (Deeper Definition and Implementation)



After understanding the philosophy and principles in this chapter (`docs/en-US/ai`), if you wish to check specific implementation methods and the latest unified definitions, please refer to the following documents in the `note` folder.



- [NRA-IDE Official Definition](../../../note/NRA-IDE_Official_Definition.md) (Refutation of existing paradigms and unified definition)

- [Hybrid Computation Architecture Implementation](../../../note/Quantum_Classical_IDE_Hybrid_Architecture.md) (Fusion of IDE flow and classical exact computation)

- [Role and Relation of IDE and Classical Computation](../../../note/IDE_Classical_Hybrid_Computation_Bilingual.md) (Resolution formulas via hybrid computation)

