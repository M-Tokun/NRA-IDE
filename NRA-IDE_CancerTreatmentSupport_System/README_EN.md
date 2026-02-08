# ═══════════════════════════════════════════════════════════════════════
# Project: NRA-IDE Cancer Treatment Support System
# Phase:   Master (Root)
# File:    README_EN.md (English Gateway Version)
# ═══════════════════════════════════════════════════════════════════════

## 🌍 Language Notice | 言語に関する注意

**This is a gateway document for non-Japanese speakers.**  
**For detailed technical documentation, please translate the original Japanese files into your native language.**

本文書は非日本語話者向けのゲートウェイドキュメントです。  
詳細な技術文書は、オリジナルの日本語ファイルをあなたの母国語に翻訳してお使いください。

---

## 1. Project Overview

**NRA-IDE** (Non-statistical Ritsukan Axiom - Integrated Deterministic Engine) is a next-generation cancer treatment support system that analyzes the physical properties of cancer cells and deterministically evaluates metastasis risk.

### Key Differences from Traditional Medical AI

| Traditional AI Approach | NRA-IDE Approach |
|------------------------|------------------|
| Statistical analysis of millions of patients | Physical analysis of **one patient** in front of you |
| Relies on averages and probabilities | Relies on **measured physical values** |
| Black-box predictions | **Transparent physical equations** |

The system identifies **conditions under which metastasis is physically impossible** through structural mechanics calculations.

---

## 2. Core Philosophy: The Ritsukan Axiom

All design decisions in this system follow three foundational axioms:

### 1. **Physics First (物理第一主義)**
- All judgments must be explainable through **physical equations**
- **Zero black-box processing**

### 2. **Fail-Closed (Gear Mechanism)**
- If **even 1 bit** of uncertainty exists in communication, calculation, or input
- The system **fails to the safe side** and issues an **Error warning**

### 3. **Gate Axiom (ゲート公理)**
- The system remains a **computation engine**
- **Final treatment decisions** must be made by the **physician** who bears ethical responsibility

---

## 3. Technical Architecture

The system adopts a **hybrid hardware-software configuration** to guarantee high reproducibility and real-time performance.

### Architecture Layers

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
│  - Safety Map Visualization             │
└─────────────────────────────────────────┘
           ↕
┌─────────────────────────────────────────┐
│  Verification Layer                     │
│  - Oracle-Based Auto-Diagnosis          │
│  - Pre-Operation Health Proof           │
└─────────────────────────────────────────┘
```

---

## 4. Quick Start

For installation and operation details, please refer to the following documents **after translating them into your native language:**

1. **Installation:** `50_Deployment/installation_guide.md`
2. **Startup Test:** `python main.py --test`
3. **Clinical Operation:** `python main.py --data patient.json`

---

## 5. Physical Approach: "Unreachable" vs "Ineffective"

### ⚠️ Core Problem

Conventional cancer treatment evaluates **"whether the drug is effective"**  
NRA-IDE evaluates **"whether the drug physically reaches the target"**

### Physical Resistance Model

$$
F_{\text{resist}} = (k_{\text{cell}} + B_{\text{drug}}) \cdot \Delta x + \eta \cdot \frac{dv}{dt}
$$

Where:
- $k_{\text{cell}}$: Tumor cell stiffness (Young's modulus)
- $\eta$: Viscosity (cytoplasm, plasma, matrix fluid)
- $\Delta x$: Drug deformation penetration (mismatch with tumor interstitium)
- $\frac{dv}{dt}$: Administration rate variation

### Decision Criterion

$$
F_{\text{resist}} > \Delta P \cdot A \Rightarrow \text{STOP (Drug Cannot Reach)}
$$

If administration pressure cannot overcome structural resistance → **"Unreachable Zone"**

---

## 6. Application: SAFE / BORDER / DANGER Zone Definition

NRA-IDE processes input parameters **(cell stiffness, viscosity, blood flow pressure, tumor thickness)** in real-time using FPGA, separating the tumor region into three zones:

| Zone | Condition | Treatment Policy |
|------|-----------|------------------|
| ✅ SAFE | Resistance < Administration Pressure | Normal dosing permitted |
| ⚠️ BORDER | Resistance ≈ Administration Pressure | Viscosity/speed adjustment recommended |
| ❌ DANGER | Resistance > Administration Pressure | Stop dosing / Change route |

---

## 7. Disclaimer

**This system is a non-commercial support template tool that presents "physical calculation results."**

- **For research use, not clinical use**
- **Final treatment decisions must be made by qualified physicians**
- **Translation accuracy is the responsibility of the user**

---

## 📂 Repository Structure

```
NRA-IDE_CancerTreatmentSupport_System/
├── jp/                    # Japanese Documentation (Primary)
│   ├── README.md          # Detailed Japanese README
│   ├── 00_Overview/       # Project overview documents
│   ├── 10_Theory/         # Ritsukan Axiom theory
│   ├── 20_Design/         # System design specifications
│   ├── 30_Implementation/ # FPGA & Python implementation
│   ├── 40_Validation/     # Verification framework
│   └── 50_Deployment/     # Installation guides
└── en/                    # English Documentation (Gateway Only)
    └── README_EN.md       # This file
```

---

## 🔗 External Resources

- **Project Blog (Japanese)**: [https://mtokuni.hatenablog.com/](https://mtokuni.hatenablog.com/)
- **Developer Note**: [https://note.com/mtokuni](https://note.com/mtokuni)
- **GitHub Repository**: [https://github.com/M-Tokun/NRA-IDE](https://github.com/M-Tokun/NRA-IDE)

---

## ⚠️ Critical Translation Notice

**For detailed understanding of this system:**

1. **Translate the original Japanese documents** (`jp/` directory) **into your native language**
2. **Medical terminology translation must be performed by qualified professionals**
3. **The Ritsukan Axiom concept may not have direct equivalents in other languages**

**NRA-IDE の詳細な理解のために：**

1. **オリジナルの日本語文書**（`jp/` ディレクトリ）**をあなたの母国語に翻訳してください**
2. **医療用語の翻訳は資格のある専門家が行う必要があります**
3. **律環公理の概念は他の言語に直接相当するものがない可能性があります**

---

*All descriptions in this repository were generated by an AI assistant implementing the RCA-IDE framework.*

[![M-Tokuni profile views](https://u8views.com/api/v1/github/profiles/214784860/views/day-week-month-total-count.svg)](https://u8views.com/github/M-Tokun)
