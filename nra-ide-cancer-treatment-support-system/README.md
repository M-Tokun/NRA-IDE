# ═══════════════════════════════════════════════════════════════════════

# Project: NRA-IDE Cancer Treatment Support System

# Phase:   Master (Root)

# File:    README.md (English Gateway Version)

# Rev:     2.0 (2026-07-28 - 07-29) Synced with PHASE_2 Rev 2.0

# ═══════════════════════════════════════════════════════════════════════



## 🌍 Language Notice | 言語に関する注意



**The original Japanese text takes precedence.**  

If any nuance differences arise from translation, the Japanese version (`README_JP.md` and documents under `jp/`) is authoritative.



**This is a gateway document for non-Japanese speakers.**  

**For detailed technical documentation, please translate the original Japanese files into your native language.**



日本語原文が優先です。翻訳によるニュアンスの違いが生じた場合は、日本語版（`README_JP.md` および `jp/` 配下の文書）が正となります。

本文書は非日本語話者向けのゲートウェイドキュメントです。  

詳細な技術文書は、オリジナルの日本語ファイルをあなたの母国語に翻訳してお使いください。



---



## 1. Project Overview



**NRA-IDE** (Nomological Ring Axioms - Intensional Dynamics Engine) is a research-purpose computation engine that analyzes the physical properties of cancer cells and deterministically evaluates metastasis risk.



### Key Differences from Traditional Medical AI



| Traditional AI Approach | NRA-IDE Approach |

|------------------------|------------------|

| Statistical analysis of millions of patients | Physical analysis of **one patient** in front of you |

| Relies on averages and probabilities | Relies on **measured physical values** |

| Black-box predictions | **Transparent physical equations** |



> **Determinism guarantees reproducibility, not correctness.**

> The system returns the same output for the same input, but if the model or its parameters are wrong, it will be reliably wrong. Validity must be established experimentally per `検証プロトコル_マイクロ流路試験.md` (microfluidic jamming protocol), which has **not yet been carried out**.



---



## 2. Scope of Judgement



The system answers exactly one question:



> **Can a cancer cell pass through a gap (pore) in the vascular endothelium?**



| Question | This system |

|:---|:---|

| Can the cancer cell escape through the vessel gap? | **Judged** |

| Can the drug penetrate the tumor interstitium? | **Not judged** — see §5, motivation only |



Drug penetration is fluid transport through a porous medium (Darcy flow, diffusion). Its governing law and parameters differ entirely from this model. The two must never share one equation or one output vocabulary.



### Output Vocabulary



| Output | Physical meaning |

|:---|:---|

| `BLOCKED` | Resisting stress exceeds driving pressure; the cell cannot pass |

| `PASSABLE` | The cell can deform and pass through (escape route is open) |



**The words `SAFE` and `DANGER` are not used.** "The cell is physically contained" and "it is safe to administer treatment" are different propositions. Collapsing them into one word turns a computation into a treatment authorization, violating the Gate Axiom.



---



## 3. Core Philosophy: Nomological Ring Axioms



### 1. **Physics First (物理第一主義)**

- All judgments must be explainable through **physical equations**

- **Zero black-box processing**



### 2. **Fail-Closed (Gear Mechanism)**

- If **even 1 bit** of uncertainty exists in communication, calculation, or input

- The system **fails to the safe side** and issues an **Error warning**

- Here the safe side means **assuming metastasis risk exists** (`PASSABLE`)



### 3. **Gate Axiom (ゲート公理)**

- The system remains a **computation engine**

- **Final treatment decisions** must be made by the **physician** who bears ethical responsibility



---



## 4. Technical Architecture



```

┌─────────────────────────────────────────┐

│  Compute Layer (FPGA)                   │

│  - Intel Cyclone V / Xilinx Artix-7     │

│  - Q8.8 Fixed-Point Arithmetic          │

│  - Deterministic Calculation (No OS)    │

└─────────────────────────────────────────┘

           ↕ Binary Protocol

┌─────────────────────────────────────────┐

│  Control Layer (Python)                 │

│  - Physical Validation of Input         │

│  - Clinical Report Generation           │

│  - Jamming Map Visualization            │

└─────────────────────────────────────────┘

           ↕

┌─────────────────────────────────────────┐

│  Verification Layer                     │

│  - Oracle-Based Auto-Diagnosis          │

│  - Pre-Operation Health Proof           │

└─────────────────────────────────────────┘

```



The decision logic in `20_Software_Host/nra_core_model.py` (reference model) and `10_Hardware_Design/src/10_BioCalibrator_TypeA.v` (FPGA) are **bit-identical**. The visualizer derives its boundary from that same reference model and holds no approximation of its own.



---



## 5. Background: "Not Reaching" vs "Not Working"



> **This section states the project's motivation. It is NOT what the current system judges.**

> No drug-penetration model is implemented.



Conventional evaluation asks whether a drug is effective. In practice, high interstitial fluid pressure (IFP) inside tumor tissue impedes drug delivery to the core, and low-perfusion regions become sites of local invasion and recurrence. There has been little means of evaluating "unreached regions" numerically.



Starting from that problem, NRA-IDE first formalizes the part where the physics is well-defined: **whether a cell can escape through a gap.** Modelling drug penetration remains future work.



---



## 6. Physical Model



$$\sigma_{\text{resist}} = (E + B)\cdot\frac{D-d}{D} \;+\; \frac{12\,\eta\,v\,D}{1000\,d^{2}} \;>\; \Delta P \implies \text{BLOCKED}$$



| Symbol | Meaning | Unit |

|:---:|:---|:---:|

| $E$ | Young's modulus of the cell | kPa |

| $B$ | Stiffening contribution from the drug | kPa |

| $D$ | Cell diameter | μm |

| $d$ | Pore size | μm |

| $(D-d)/D$ | **Compressive strain (dimensionless)** | – |

| $\eta$ | Viscosity (cytoplasm, surrounding fluid) | Pa·s |

| $v$ | Deformation velocity | μm/s |

| $\Delta P$ | Blood flow driving pressure | kPa |



The first term is elastic resistance, the second is viscous resistance inside the pore. **All terms are in kPa; both sides are dimensionally consistent.**



- Zero viscosity input → **Error 0x03** (physically impossible in tissue; indicates instrument fault)

- Cell diameter smaller than the pore → **Error 0x01** (passes without deforming)



See `jp/.../00_Documentation/PHASE_2_Mesoscale_Physics.md` for the derivation.



---



## 7. Jamming Map



Input parameters are processed in Q8.8 fixed point, and the decision boundary is drawn on the plane of drug boost $B$ against flow pressure $\Delta P$.



| Zone | Condition | Meaning |

|:---|:---|:---|

| 🟩 BLOCKED | $\sigma_{resist} > \Delta P$ | The cell cannot pass through the gap |

| 🟥 PASSABLE | $\sigma_{resist} \le \Delta P$ | The cell may deform and pass |



The plotted boundary is not an approximation — it is **the FPGA decision boundary itself**, computed with identical Q8.8 arithmetic.



> **Margin evaluation near the boundary (the former "BORDER" zone) is not implemented.** The current output is binary and carries no measure of how close a case sits to the boundary. Clinically this margin matters most, and it remains future work.



---



## 8. Quick Start



```bash

cd jp/NRA-IDE_Cancer_Treatment_Support_System/20_Software_Host

pip install -r requirements.txt



# Self-diagnostic (works without FPGA, via the reference model)

python main.py --test



# Full validation suite (7 cases)

cd ../30_Test_Data && python run_validation.py



# Clinical session (emits report and jamming map)

cd ../20_Software_Host

python main.py --data ../30_Test_Data/sample_patient_data.json --out ./output

```



| Command | Status |

|:---|:---|

| `python main.py --test` | **Working** (falls back to the reference model when no FPGA is attached) |

| `python run_validation.py` | **Working** (7/7 PASS) |

| `python main.py --data <path> [--out <dir>]` | **Working** (emits a `.txt` report and a `.png` map) |



If the input falls outside the Phase 4 ranges, no computation is performed; only a `_REJECTED.txt` record is written (Fail-Closed).



---



## 9. Current State and Open Items



> **Revision history: [jp/.../CHANGELOG.md](./jp/NRA-IDE_Cancer_Treatment_Support_System/CHANGELOG.md)** (Japanese).
> **If you obtained Rev 1.0, please read it.** The Rev 1.0 governing equation was dimensionally inconsistent and the decision engine did not function. That file lists every corrected claim.



This repository is a research template. The following are **incomplete**, stated without embellishment:



| Item | Status |

|:---|:---|

| Type A (single cell) decision model | Formalized, reference implementation, 7 verification cases — complete |

| Type B (cell cluster) model | **Not implemented.** The $\sqrt{N}$ law is not supported by the cited literature, so the RTL is a stub returning `0x06 ERR_UNSUPPORTED` |

| FPGA RTL (simulation) | **Verified** (2026-07-29, Icarus Verilog 11.0). Core unit 7/7, full integration 8/8, also confirmed at the real 115200 baud |

| FPGA RTL (synthesis / timing) | **Not performed** (no Vivado / Quartus run) |

| Drug penetration model | **Not started** |

| Microfluidic experimental validation | **Not performed** (protocol drafted only) |



---



## 📂 Repository Structure



```

NRA-IDE_CancerTreatmentSupport_System/

├── README.md              # This file (English Gateway)

├── README_JP.md           # Japanese Main README

└── jp/                    # Detailed Documentation (Japanese, Primary)

    └── NRA-IDE_Cancer_Treatment_Support_System/

        ├── 00_Documentation/     # Full 10-phase documents

        ├── 10_Hardware_Design/   # FPGA design files

        ├── 20_Software_Host/     # Python (nra_core_model.py is the single source of decisions)

        ├── 30_Test_Data/         # Test data & validation

        ├── 40_Output_Reports/    # Report templates

        ├── 50_Deployment/        # Installation & business plan

        ├── 60_Research/          # References & resources

        └── src/                  # Reference images

```



---



## ⚠️ Disclaimer



**This system is a non-commercial support template tool that presents "physical calculation results."**



- **For research use, not clinical use**

- **Not a medical device** under Japanese pharmaceutical and medical device law

- **Final treatment decisions must be made by qualified physicians**

- **Translation accuracy is the responsibility of the user**



---



## ⚠️ Critical Translation Notice



1. **Translate the original Japanese documents** (`jp/` directory) **into your native language**

2. **Medical terminology translation must be performed by qualified professionals**

3. **Nomological Ring Axioms concept may not have direct equivalents in other languages**



**NRA-IDE の詳細な理解のために：**



1. **オリジナルの日本語文書**（`jp/` ディレクトリ）**をあなたの母国語に翻訳してください**

2. **医療用語の翻訳は資格のある専門家が行う必要があります**

3. **律環公理の概念は他の言語に直接相当するものがない可能性があります**



---

*All descriptions in this repository were generated by an AI assistant implementing the NRA-IDE framework.*
