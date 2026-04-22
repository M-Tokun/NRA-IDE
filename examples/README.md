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

## Demo List (32 demos — Recommended Order)

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

---

### ⚙️ STEP 7 — Advanced Domain Applications (11–16)

| # | File | Content |
|---|------|---------|
| 11 | [11_Motor3Phase_BandGate_live_JP.html](./11_Motor3Phase_BandGate_live_JP.html) | **Three-phase motor Band Gate live monitoring.** Real-time R = δ/τ applied to three-phase motor load balance and overload detection. (JP) |
| 12 | [12_agri_mol_antagonism_JP.html](./12_agri_mol_antagonism_JP.html) | **Agricultural ion monitoring + Mg²⁺/K⁺ antagonism chain Band Gate.** Andosol / general farmland profile switching. Dynamic τ with asymmetric EMA; Mg deficiency triggers linked K⁺ τ gate. (JP) |
| 13 | [13_photosynthesis_layer5_JP.html](./13_photosynthesis_layer5_JP.html) | **Photosynthesis Layer 5 monitoring.** Farquhar-von Caemmerer-Berry (FvCB) model as external δ generator → R = δ/τ. Non-linear preprocessor as NRA-IDE Layer 5. (JP) |
| 14 | [14_powergrid_transition_JP.html](./14_powergrid_transition_JP.html) | **Power grid transition / phase transition point.** Detects structural transition points in power grid state, where conventional threshold monitoring misses early divergence. (JP) |
| 15 | [15_or_icu_continuum_JP.html](./15_or_icu_continuum_JP.html) | **OR/ICU continuum monitoring (cumulative state type).** Tracks accumulated deviation across surgical and ICU phases; R reflects ongoing structural burden, not just instantaneous values. (JP) |
| 16 | [16_passive_safety_JP.html](./16_passive_safety_JP.html) | **Passive gravity-driven safety system.** Safety architecture that relies solely on physical constraints (gravity, tension) — no active control required to enter safe state. (JP) |

---

### 🔬 STEP 8 — Physical State Transition Monitoring (17–22)

| # | File | Content |
|---|------|---------|
| 17 | [17_water_ice_phase_transition_JP.html](./17_water_ice_phase_transition_JP.html) | **Water → ice phase transition.** NRA-IDE tracks the approach to the phase boundary (0°C); R rises as temperature and latent heat cross the structural threshold. (JP) |
| 18 | [18_chain_tension_JP.html](./18_chain_tension_JP.html) | **Chain tension with polygon effect auto-adjustment.** Three-layer composite wave reproduces sprocket polygon effect. dR/dt predictive control intervenes before the limit is reached. (JP) |
| 19 | [19_air_pressure_JP.html](./19_air_pressure_JP.html) | **Air pressure management (compressible fluid · dynamic τ · dual fluctuation).** τ_hi shrinks with temperature rise via Boyle–Charles law; δ and τ fluctuate independently. The deepest dual-fluctuation structure in the series. (JP) |
| 20 | [20_water_pressure_JP.html](./20_water_pressure_JP.html) | **Water pressure management (incompressible fluid · fixed τ · water hammer).** Pump pulsation via three-layer harmonics; valve rapid closure generates water hammer (exponential decay × sine wave). (JP) |
| 21 | [21_cabg_monitor_JP.html](./21_cabg_monitor_JP.html) | **CABG (coronary artery bypass graft) monitor.** Intraoperative monitoring of blood flow, pressure, and temperature for bypass surgery; Fail-Closed triggers surgical suspension recommendation. (JP) |
| 22 | [22_vascular_monitor_JP.html](./22_vascular_monitor_JP.html) | **NRA-IDE Vascular Intervention Monitor.** Six physical quantities (pressure · shear · wall tension · flow · temperature · adhesion) monitored via Dual Fluctuation + Dynamic τ. Specialized for PTA, stent, anastomosis, cryotherapy. (JP) |

---

### 🧩 STEP 9 — Advanced Features and Specific Domains (23–26)

| # | File | Content |
|---|------|---------|
| 23 | [23_sample_demo_EN.html](./23_sample_demo_EN.html) / [JP](./23_sample_demo_JP.html) | **State boundary · short-term log · long-term reconstruction.** Demonstrates how NRA-IDE separates short-term fluctuation tracking from long-term structural trend reconstruction. |
| 24 | [24_vehicle_mandatory_boundary_EN.html](./24_vehicle_mandatory_boundary_EN.html) / [JP](./24_vehicle_mandatory_boundary_JP.html) | **Autonomous driving mandatory boundary monitoring.** Physical quantity monitoring (time-to-collision, braking distance, lateral clearance); mandatory Fail-Closed when R ≥ 1.0 with no override path. |
| 25 | [25_dam_degradation_EN.html](./25_dam_degradation_EN.html) / [JP](./25_dam_degradation_JP.html) | **Dam management comparison + τ degradation curve.** Compares conventional fixed-threshold monitoring vs. NRA-IDE τ degradation tracking. τ shrinks over time as structural margin erodes. |
| 26 | [26_escapement_contactpoint_JP.html](./26_escapement_contactpoint_JP.html) | **Phase-gap engine — heat dissipation at contact points only.** Demonstrates that error/heat is generated only at phase-boundary contact, not throughout continuous computation. (JP) |

---

### 🛠️ STEP 10 — Equipment Monitoring Fundamentals (27–32)

These demos apply R = δ/τ to common industrial and facility monitoring domains.
Each demonstrates unit independence: the same formula structure manages fundamentally different physical quantities.

| # | File | Domain | Key Point |
|---|------|--------|-----------|
| 27 | [27_belt_tension_JP.html](./27_belt_tension_JP.html) | Belt conveyor / V-belt tension | τ defined as full margin from optimum to limit → R naturally normalizes to [0,1]. Fail-Closed stops belt animation. (JP) |
| 28 | [28_water_temp_JP.html](./28_water_temp_JP.html) | Water temperature upper/lower limits | R_hi and R_lo evaluated independently. Thermal convection fluctuation (3-frequency composite). Fail-Closed stops the opposing action direction. (JP) |
| 29 | [29_light_lux_JP.html](./29_light_lux_JP.html) | Luminosity (illuminance) management | Measured in lux (receiver side). AUTO-SHADE increases shade ratio proportionally from R_hi > 0.75 — stepwise intervention from precursor stage. (JP) |
| 30 | [30_power_JP.html](./30_power_JP.html) | Power management (V × I integration) | Current and voltage unified as P = V×I. Heat accumulation: prolonged excess power pushes R upward over time (temporal integral). (JP) |
| 31 | [31_move_water_or_ice_JP.html](./31_move_water_or_ice_JP.html) | Water / ice phase navigation | Interactive phase transition control; slide between liquid and solid states while tracking R across the phase boundary. (JP) |
| 32 | [32_氷から水への相転移nra_ide_water_ice_20260324_2216_JP.html](./32_氷から水への相転移nra_ide_water_ice_20260324_2216_JP.html) | Ice → water phase transition | Reverse of Demo 17: tracks structural R as ice warms past 0°C and latent heat is absorbed during phase change. (JP) |

---

### 🔭 Standalone Demos

| File | Content |
|------|---------|
| [nra_ide_6d_layer_viz_2026-03-21_1237.html](./nra_ide_6d_layer_viz_2026-03-21_1237.html) | **6D multi-layer visualizer.** Six simultaneous R-value surfaces with transparency, saturation, and black-and-white mode. Each layer = one physical domain's fluctuation × threshold plane. Time axis shows structural approach to Fail-Closed across all dimensions simultaneously. |
| [NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_EN.html](./NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_EN.html) / [JP](./NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_JP.html) | **Agricultural Drone 4-Factor Simulation.** NRA-IDE applied to agro-drone field monitoring: four simultaneous physical factors tracked with R = δ/τ. Fail-Closed triggers when any factor breaches structural limits. |

---

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
