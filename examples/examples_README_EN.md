# NRA-IDE Demonstration Suite (English Edition)
# NRA-IDE Examples — English Edition
<!-- README_EN.md | examples/ | 2026-03-05 -->

---

## What is NRA-IDE?

**Nomological Ring Axioms — Intensional Dynamics Engine**

This is a deterministic control engine based on **Tension Structure (Constraint → Force → Displacement)**,
completely eliminating linear concepts such as continuity, distance, and ambiguous semantics.

In high-risk areas where conventional methods often become "black boxes"
(such as Medical AI, Autonomous Driving, and Critical Infrastructure),
NRA-IDE provides a judgment mechanism that is **fully explainable and free from error accumulation**.

---

## Why NRA-IDE Does Not Accumulate Error

A mechanical clock keeps accurate time not because its gears are perfect, but because its
**escapement mechanism advances in discrete, complete steps** — no fractional remainder carries forward.

NRA-IDE applies this same principle. Rather than processing state transitions as continuous
floating-point values, the IDE operates on **integer phase locks**.
Each step is structurally complete. There is no residual to inherit.

> **This is why error does not accumulate — not because it is corrected,
> but because the system is defined in a way that leaves no room for it to arise.**

The demos below make this difference visible and measurable.
For the implementation detail (Integer Phase Lock / Residual Discard), see `nra-core/`.

---

## The Threshold System Principle

$$R = \frac{\delta}{\tau}$$

| Symbol | Meaning | Description |
|--------|---------|-------------|
| **δ (Delta)** | Deviation from Constraint | The physically measured displacement (Fluctuation). |
| **τ (Tau)** | Tolerance Range | The threshold (thickness) defined during design. |
| **R** | Structural Ratio | Judgment is made based on the value of δ ÷ τ. |

| Value of R | Judgment | Action |
|------------|----------|--------|
| R < 1.0 | **SAFE** | AI presents physical evidence and continues processing. |
| R ≥ 1.0 | **STOP** | Structural limit reached. AI ceases output → Human makes the final decision. |

> **Design Philosophy:** The AI is strictly for calculation.
> Ethical and final decisions are the responsibility of humans. (Boundary of Responsibility)

---

## Demo List (Recommended Order)

These demos run directly in your browser — no installation required.

### 📚 STEP 1 — Understand "Why?"

| # | File | Content |
|---|------|---------|
| 01 | [01_Why_No_Distance_EN.html](./01_Why_No_Distance_EN.html) | **Why no distance, calculus, or floating-point arithmetic?** Visually explained from 4 perspectives via tab switching. The entry point to understanding the fundamental difference from legacy methods. |
| 02 | [02_Error_Accumulation_EN.html](./02_Error_Accumulation_EN.html) | **The Terror of Error Accumulation.** Running 100,000 steps from identical initial values to compare error accumulation between legacy methods and Nomological Ring Axioms. Displays breakdown lines for Medical, Auto, and Finance. |

### 🔬 STEP 2 — Experience the Difference

| # | File | Content |
|---|------|---------|
| 03 | [03_HAN_vs_Legacy_EN.html](./03_HAN_vs_Legacy_EN.html) | **Real-time comparison: HAN (Non-linear Adaptive Control) vs Legacy (Fixed If-Then Control).** Demonstrates the difference in tracking and stability against disturbances and sudden loads using waveform graphs. |
| 04 | [04_HAN_Stress_Test_EN.html](./04_HAN_Stress_Test_EN.html) | **Extreme experiment: Intentional 80ms high-load injection.** Legacy blindly executes commands causing FPS collapse. HAN detects tension, adaptively reduces load, and maintains rendering. |

### 📊 STEP 3 — Visualize the Threshold Mechanism

| # | File | Content |
|---|------|---------|
| 05 | [05_IDE_Threshold_Visualizer_EN.html](./05_IDE_Threshold_Visualizer_EN.html) | **Dynamic visualization of R = δ/τ via Phase Scope.** Confirm the mechanisms of Integer Phase Lock and Residual Discard in real-time. |

### ⚙️ STEP 4 — The Escapement Principle (Coming Soon)

| # | File | Content |
|---|------|---------|
| 06 | `06_Escapement_Principle_EN.html` *(06_Escapement_Principle_EN.html)* | **Why gears never accumulate error.** Animated comparison of floating-point drift vs. integer phase lock. Visualizes the structural reason NRA-IDE is free from cumulative error. |

### 🔴 STEP 5 — Cascade Failure: Watch It Happen in Real Time

| # | File | Content |
|---|------|---------|
| 07 | [07_HAN_gate_live_JP.html](./07_HAN_gate_live_JP.html) | **Live simulation of cascade failure and HAN Gate SILENCE activation.** Watch the chain reaction score R rise in real time as a load spike propagates. The moment R exceeds R_OP, the gate flashes red and SILENCE is declared. Use the **⚠ Risky Preset** to experience a setting where the wave looks calm — yet the gate never fires. This is the most direct demonstration of why "it looks safe" is not a valid reason to raise the threshold. |

> **What makes this demo different:**
> The wave does not appear as a static chart. It grows step by step, exactly as a real cascade
> failure does — slowly at first, then suddenly crossing the threshold.
> The dual-fluctuation structure (dynamic τ) is visible as the orange τ line swells
> *before* the blue R line peaks, providing early warning that a static τ cannot offer.

---


### 🌿 STEP 6 — Band Gate: Real-World Domain Applications

These demos apply the Band Gate (R = δ/τ) to physical measurement domains.
Upper and lower thresholds are monitored simultaneously with **asymmetric EMA sensitivity** —
the same formula detects both over-range (surge) and under-range (dropout) events.

| # | File | Domain | Key Point |
|---|------|--------|-----------|
| 08 | [08_Band_Gate_live_JP.html](./08_Band_Gate_live_JP.html) | Electricity / Temperature / Water / Pulse (JP) | **Asymmetric Damper** — upper τ expands (conservative), lower τ shrinks (sensitive). The animated damper on the left visualises how the two springs move in opposite directions. |
| 08 | [08_Band_Gate_live_EN.html](./08_Band_Gate_live_EN.html) | Same — English edition | English labels and explanations. |
| 09 | [09_Greenhouse_BandGate_live_JP.html](./09_Greenhouse_BandGate_live_JP.html) | Greenhouse Agriculture — 4 sensors (JP) | Irrigation Pressure · Temperature · CO₂ · Nutrient EC monitored simultaneously. Try the **🏜 Drought Simulation** to see multiple sensors fall together. |
| 09 | [09_Greenhouse_BandGate_live_EN.html](./09_Greenhouse_BandGate_live_EN.html) | Same — English edition | English labels and explanations. |
| 10 | [10_Field_DroughtGate_live_JP.html](./10_Field_DroughtGate_live_JP.html) | Outdoor Field — Drought Level Gauge (JP) | Soil Moisture · Ground Temp · Solar Radiation · Wind Speed. Drought Level **Lv.0–4** is calculated from a weighted composite R score. The **⛈ Storm-after-rain** scenario shows how EMA detects drying momentum *before* the value crosses the threshold — the feature current agricultural IoT systems lack entirely. |

> **Why current agri-IoT products cannot do this:**
> Most commercial soil-sensor systems alert only when a value crosses a fixed threshold.
> They have no concept of "momentum toward the boundary."
> The EMA pre-detection demonstrated here is structurally absent from threshold-only designs.
> This is the gap NRA-IDE closes.

## Integration Guide

To integrate the control logic into your own program,
simply define the "Deviation (δ)" and "Tolerance (τ)" of the control target.

```javascript
// Minimal Configuration Example
function gate(delta, tau) {
    const R = delta / tau;
    if (R >= 1.0) return "STOP";   // FAIL_CLOSED
    return "SAFE";
}
```

**Implementation Example: Medical AI (Cancer Drug Delivery Control)**
```javascript
// Physically verify the reachability of the drug to the tumor
const tumorResistance = measureResistance();  // δ (Resistance of the tumor)
const infusionPressure = getPumpCapacity();   // τ (Infusion pressure of the pump)

const deliveryStatus = gate(tumorResistance, infusionPressure);

if (deliveryStatus === "STOP") {
    alert("Physical unreachability detected. Physician judgment required.");
    // AI stops judgment and delegates the final decision to the human (doctor).
}
```

Specific implementation patterns are documented within the source code of each demo.

---

## Areas of Application

### 🏥 Medical AI
- **Challenge:** Uncertainty of drug reachability to tumors.
- **NRA Solution:** Verification of physical integrity of the administration route.
- **Threshold:** R = (Tumor Resistance) / (Infusion Pressure)

### 🚗 Autonomous Driving
- **Challenge:** Safety issues due to black-box decision making.
- **NRA Solution:** Verification of structural constraints for collision avoidance.
- **Threshold:** R = (Time Margin to Collision) / (Braking Capability)

### 🖥️ Infrastructure Resilience
- **Challenge:** Cascade failures in distributed systems.
- **NRA Solution:** Prevention of failure propagation via load limit monitoring.
- **Threshold:** R = (Load Excess) / (Buffer Capacity)

| Area | δ (Deviation) | τ (Tolerance) | Meaning of R ≥ 1.0 |
|------|---------------|---------------|--------------------|
| Medical AI | Tumor Resistance | Infusion Pressure | Drug physically cannot reach target. |
| Autonomous | Obstacle Margin | Braking Distance | Collision Danger → Emergency Stop. |
| Infra | Load Excess | Buffer Size | Server Overload → Cutoff/Throttling. |

---

## License

**Copyright (c) 2026 M-Tokuni**

This project is provided under the **MIT License** — free to use, modify, and distribute
for research, personal, and commercial purposes.
Attribution is required in all redistributed materials and source code:

```javascript
// Powered by NRA-IDE. (c) 2026 M-Tokuni.
// Principle: L∧P∧C∧D Verified.
```

**Before using this project, you must read the Ethical Guidelines.**
Prohibited uses (weapons, surveillance, inverse derivation Π⁻¹, unverified safety-critical systems, etc.)
are defined independently in:

👉 **[ETHICS.md](../../theory/ETHICS.md)**

See **[LICENSE](../../LICENSE)** for full license terms.

**Principle Verification:** L∧P∧C∧D (Logic ∧ Physics ∧ Causality ∧ Determinism)

---

## Author

**M-Tokuni**  
Theory: Nomological Ring Axioms / Intensional Dynamics Engine

- **GitHub:** https://github.com/M-Tokun/NRA-IDE
- **Twitter/X:** https://x.com/m_tokuni
- **Facebook:** https://www.facebook.com/tokuni.masa
- **Note:** https://note.com/mtokuni
- **Blog:** https://mtokuni.blogspot.com/
- **Hatena:** https://mtokuni.hatenablog.com/

---

## Citation

```
M-Tokuni (2026). NRA-IDE: Nomological Ring Axioms — Intensional Dynamics Engine.
GitHub. https://github.com/M-Tokun/NRA-IDE
```

---

## Detailed Documentation

- **Theoretical Basis:** [`/theory/THEORY.md`](../../theory/THEORY.md)
- **Foundational Thesis:** [`/theory/Foundational_Thesis.md`](../../theory/Foundational_Thesis.md)
- **Ethical Guidelines:** [`/theory/ETHICS.md`](../../theory/ETHICS.md)
- **Core Implementation:** [`/nra-core/`](../../nra-core/)
- **Unified Definition:** [`NRA-IDE_The_Gate_Axioms_Unified_Definition.md`](../../docs/)

---

For the latest information, please check the official repository.
