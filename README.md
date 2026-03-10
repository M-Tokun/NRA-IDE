# NRA‑IDE: Nomological Ring Axioms – Intensional Dynamics Engine

### **律環公理 – 内包性動力学エンジン**

[![CI](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml/badge.svg)](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)

<p align="center">
  <img src="./docs/NRA-IDE_LOGO.jpg" width="700" alt="NRA-IDE LOGO">
</p>

---

## 🌏 For Japanese Speakers

**日本語版ドキュメントは [README_JP.md](./README_JP.md) をご覧ください。**

---

## Core Axiom

## "Existence is Generation."

This framework does not treat existence as a fixed entity.  
**Existence appears as "state transition."**

Here, "generation" does not imply creation from nothing, but refers to the manifestation of existence through the process of state transition.

---

## Fundamental Structure: Redefining Time and Distance

Instead of relying on linear computation (continuity, distance, meaning), this system describes the world through physical and structural constraints.

1. **Time**
   - Time is not treated as an independent "causal variable."
   - Time is described as the **ordering of state transitions**.

2. **Distance**
   - Distance is not treated as a "causal driver."
   - Distance is recorded as an **observational result** of state change.

3. **Tension**
   - Refers to the **restoring tendency** arising from constraint boundaries.
   - It is treated as a structural constraint, which may manifest as physical tension.

---

## What Is NRA‑IDE?

**NRA‑IDE is NOT an "Integrated Development Environment."**  
**It is an "Intensional Dynamics Engine" that implements the Nomological Ring Axioms.**

- **No Meaning Generation**: The IDE does not generate "meaning"; it evaluates structural states.
- **Physical Explainability**: It calculates tension structures, threshold dynamics, and closed-world constraints in a physically explainable manner.

---

## Why NRA-IDE Does Not Accumulate Error

A mechanical clock keeps accurate time not because its gears are perfect, but because its
**escapement mechanism advances in discrete, complete steps** — no fractional remainder carries forward.

NRA-IDE applies this same principle. Rather than processing state transitions as continuous floating-point values,
the IDE operates on **integer phase locks**. Each step is structurally complete. There is no residual to inherit.

> **Error does not accumulate — not because it is corrected,
> but because the system is defined in a way that leaves no room for it to arise.**

For implementation details (Integer Phase Lock / Residual Discard), see [`nra-core/`](./nra-core/).

---

## Structural Ratio & Threshold System

Unlike conventional black-box AI, this system uses **Thresholds** to make decision grounds physically explainable.

$$
R = \frac{\delta}{\tau}
$$

- **δ (delta)**: Deviation from constraints (fluctuation/displacement)
- **τ (tau)**: Tolerance boundary (thickness of tension)
- **R**: Structural Ratio

### Decision Logic

| R Value | Judgment | Action |
|---------|----------|--------|
| **R < 1.0** | **SAFE** | System operates based on physical grounds (AI processes data). |
| **R ≥ 1.0** | **STOP** | Structural limit reached. **AI ceases decision-making and output.** |

### Fail-Closed Principle

"Fail-Closed" in this system does not mean a simple system crash.
It refers to a design that **suppresses output while maintaining structural continuity.**
When R ≥ 1.0, the system stops generating output, and final judgment is delegated to a human operator.

---

## 📄 Theoretical Background

- **[Foundational Thesis](./theory/Foundational_Thesis.md)** *(Japanese/English Bilingual)*  
  A short thesis discussing the description of state transitions via structural thresholds.

- **[Theory Definition (THEORY.md)](./theory/THEORY.md)**  
  Detailed definition of the axiomatic system.

---

## Core Engine

The foundational implementation is centralized in `nra-core/`.

- 📄 [nra_ide_foundation_fixed_en.py](./nra-core/nra_ide_foundation_fixed_en.py) – English Version  
- 📄 [nra_ide_foundation_fixed_jp.py](./nra-core/nra_ide_foundation_fixed_jp.py) – Japanese Version  
- 📝 [Annotated Explanation (EN)](./nra-core/Nomological_Ring_Axioms_Code_Annotated_Explanation_Dual_Fluctuation_Stable.md)  
- 📊 [Validation Plot](./nra-core/nra_foundation_plot_2026-02-20_2355.png)

---

## 📂 Major Projects

### 💎 NRA‑TCM Parser (Text Crystallization Method)
**[./NRA-TCM Parser/](./NRA-TCM%20Parser/)**

- Phase transition of information (crystallizing million‑token logs)  
- Dynamic momentum (adaptive deep‑reading / skimming)  
- Singularity detection (captures core insights even under broken context)

---

### 🏥 Cancer Treatment Support System
**[./NRA-IDE_CancerTreatmentSupport_System/](./NRA-IDE_CancerTreatmentSupport_System/)**

- Metastasis risk estimation via physical constraints  
- FPGA implementation (deterministic computation)  
- Full traceability for medical device approval  

---

### 🔗 Cascade Failure Prevention
**[./HAN-Gate_Cascade-Failure-Prevention/](./HAN-Gate_Cascade-Failure-Prevention/)**

- Prevents cascade failures in server infrastructure  
- Envoy / Nginx integration  
- Automotive safety & critical infrastructure  

---

## 🔍 Keywords / Topics

`ai-safety` `medical-ai` `text-mining` `crystallization`  
`cancer-treatment` `deterministic-computing` `fpga`  
`fail-safe` `autonomous-systems` `healthcare`  
`decision-support` `cascade-failure-prevention`  
`non-statistical` `physics-based` `structural-constraints`

---

## 📜 License

This project is provided under the **MIT License**.

- Free to use, modify, and distribute for research, personal, and commercial purposes.
- Attribution is required in all redistributed materials.
 © 2026 M‑Tokuni

See **[LICENSE](./LICENSE)** for full terms.

---

## ⚠️ Notice

**Before using this project, you must read the Ethical Guidelines.**  
Prohibited uses (weapons, surveillance, inverse derivation Π⁻¹, unverified safety-critical systems, etc.)
are defined independently of the license:

👉 **[ETHICS.md](./theory/ETHICS.md)**

---

## 📖 Citation

M‑Tokuni (2026).  
**NRA‑IDE: Nomological Ring Axioms – Intensional Dynamics Engine.**  
GitHub. https://github.com/M-Tokun/NRA-IDE

---

<p align="center">
  <strong>Status: Lighthouse</strong>
</p>

---

[![M-Tokuni profile views](https://u8views.com/api/v1/github/profiles/214784860/views/day-week-month-total-count.svg)](https://u8views.com/github/M-Tokun)
