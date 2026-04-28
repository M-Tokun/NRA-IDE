# NRA-IDE Examples — English Edition

<!-- README_EN.md | examples/ | updated 20260425_163041_JST -->

---

## What is NRA-IDE?

**Nomological Ring Axioms — Intensional Dynamics Engine**

NRA-IDE is a deterministic control and structural judgment engine based on **tension structure**: constraint → force → displacement. It deliberately avoids making continuity, distance, or semantic interpretation the primary basis of safety judgment. In practical terms, it is a framework centered on nonlinear, physically grounded structure.

Where conventional methods can become black boxes in high-risk areas such as medical AI, autonomous driving, and infrastructure control, NRA-IDE provides an explainable judgment mechanism based on directly observed structural deviation.

---

## Why NRA-IDE Does Not Accumulate Error

A mechanical clock keeps time not because every gear is perfect, but because the escapement advances in a discrete step: exactly one tooth at a time. Residual fractions are not carried forward into the next step.

NRA-IDE implements this principle. State transitions are not treated as an endlessly drifting floating-point continuum. Instead, they are handled as structurally closed phase steps. Each step is completed as a bounded transition, and residual fragments are not inherited as causal state.

> **Error does not fail to accumulate because it is corrected afterward.  

> It does not accumulate because the structure does not allow it to be carried forward.**

The demos below are designed to visualize and quantify this difference. For implementation details such as integer phase lock and residual discard, see `nra-core/`.

---

## Principle of the Threshold System

$$R = \frac{\delta}{\tau}$$

| Symbol | Meaning | Description |

|------|------|------|

| **δ (delta)** | Deviation / fluctuation from constraint | Physically observed displacement or deviation |

| **τ (tau)** | Tolerance thickness / allowable margin | Structurally defined threshold width |

| **R** | Structural ratio | Judgment value calculated as δ ÷ τ |

| R Range | Judgment | Meaning | Action |

|--------|------|------|------|

| R < 0.40 | **SAFE** | Sufficient structural margin remains | AI may continue processing with physical basis shown |

| 0.40 ≤ R < R_J | **WATCH / CAUTION** | The system is approaching the boundary and may require preparation for intervention | Continue monitoring. Check history, correlation, and dR/dt. Gradually restrict automatic intervention if needed |

| R_J ≤ R < 1.00 | **JUDGMENT LIMIT** | Under the actual operating conditions, further progression may reach R = 1.0 due to delay, inertia, or residual fluctuation | Stop or strongly restrict automatic judgment and transfer authority to humans |

| R ≥ 1.00 | **FAIL-CLOSED** | Structural limit corresponding to phase transition, rupture, breach, or collapse | AI stops output/action and humans make the final decision |

> **Important:** R = 1.0 is not a warning value.  

> R = 1.0 is the structural boundary corresponding to phase transition, rupture, breach, or collapse. Therefore, real safety design must not wait until R reaches 1.0.  

> NRA-IDE places a **Judgment Limit (R_J)** before that boundary.  

> R_J is not a fixed axiom value. It is set according to the operating site, target object, sensor delay, stopping time, and required safety margin.

> **Design principle:** AI performs computation. Ethical and final judgment belongs to humans. This is the responsibility boundary.

---

## Demo List — 41 Demos + Standalone Visualizations, Recommended Order

All demos run directly in a browser. No installation is required.

> In many demos, the red line indicates R = 1.0. This is not a warning line; it is the structural limit line. The practical judgment limit must be placed before that line. Its value is not fixed, and should be configured according to the operating site and target domain.

### 📚 STEP 1 — First Understand “Why?”

| # | File | Content |

|---|---------|------|

| 00 | [00_Escapement_Foundation_NRA_JP.html](./00_Escapement_Foundation_NRA_JP.html) | **Escapement Foundation (JP).** Basic concept demo of integer phase lock — why residuals disappear. (Japanese only) |

| 01 | [01_Why_No_Distance_EN.html](./01_Why_No_Distance_EN.html) | **Why not use distance, calculus, or floating-point continuity as the primary basis?** A visual introduction from four perspectives. |

| 02 | [02_Error_Accumulation_EN.html](./02_Error_Accumulation_EN.html) | **The danger of error accumulation.** Runs 100,000 steps from the same initial value and compares conventional methods with NRA-style structure. |

### 🔬 STEP 2 — Experience the Difference in Behavior

| # | File | Content |

|---|---------|------|

| 03 | [03_HAN_vs_Legacy_EN.html](./03_HAN_vs_Legacy_EN.html) | **HAN vs Legacy real-time comparison.** Demonstrates tracking and stability differences under disturbance and sudden load. |

| 04 | [04_HAN_Stress_Test_EN.html](./04_HAN_Stress_Test_EN.html) | **Extreme 80 ms load test.** Legacy blindly executes commands and collapses in FPS; HAN detects tension and adapts load. |

### 📊 STEP 3 — Visualize the Threshold Mechanism

| # | File | Content |

|---|---------|------|

| 05 | [05_IDE_Threshold_Visualizer_EN.html](./05_IDE_Threshold_Visualizer_EN.html) | **Dynamic visualization of R = δ/τ.** Confirms integer phase lock and residual discard in real time. |

### ⚙️ STEP 4 — Escapement Principle

| # | File | Content |

|---|---------|------|

| 06 | `06_Escapement_Principle_EN.html` *（./06_Escapement_Principle_EN.html）* | **Why gears do not accumulate error.** Floating-point drift vs integer phase lock animation. |

### 🔴 STEP 5 — Cascade Failure: Watching the Moment Collapse Begins

| # | File | Content |

|---|---------|------|

| 07 | [07_HAN_gate_live_EN.html](./07_HAN_gate_live_EN.html) | **Live simulation of cascade failure and HAN Gate SILENCE activation.** As load spikes propagate, the chain-reaction score R rises in real time. When R crosses the operational boundary, the screen flashes red and SILENCE is declared. |

> **Why this demo is different:**  

> The waveform is not a static graph. It behaves like a real cascade failure: slow at first, then suddenly crossing the boundary. It also visualizes the dual-fluctuation structure, where the τ line begins to expand before the R peak becomes obvious.

---

### 🌿 STEP 6 — Band Gate: Real-World Domain Applications

These demos apply Band Gate logic, R = δ/τ, to physical measurement domains. Upper and lower limits are monitored independently, and asymmetric EMA sensitivity detects both overload and depletion.

| # | File | Domain | Key Point |

|---|---------|---------|---------|

| 08 | [08_Band_Gate_live_JP.html](./08_Band_Gate_live_JP.html) | Electricity, air temperature, water pressure, pulsation — JP | **Asymmetric damper structure.** Upper τ expands cautiously, lower τ shrinks sensitively. |

| 08 | [08_Band_Gate_live_EN.html](./08_Band_Gate_live_EN.html) | Same — English | English labels and explanations. |

| 09 | [09_Greenhouse_BandGate_live_JP.html](./09_Greenhouse_BandGate_live_JP.html) | Greenhouse agriculture, four-sensor monitoring — JP | Monitors irrigation pressure, air temperature, CO₂, and nutrient EC. |

| 09 | [09_Greenhouse_BandGate_live_EN.html](./09_Greenhouse_BandGate_live_EN.html) | Same — English | English labels and explanations. |

| 10 | [10_Field_DroughtGate_live_JP.html](./10_Field_DroughtGate_live_JP.html) | Outdoor field drought progression gauge — JP | Soil moisture, soil temperature, solar radiation, and wind speed. Composite R estimates drought level Lv.0–4. |

> **What current agricultural IoT often cannot do:**  

> Most systems alert only after a fixed threshold has already been crossed. They do not represent “momentum toward the boundary.” NRA-IDE makes that boundary approach visible.

---

### ⚙️ STEP 7 — Advanced Domain Applications (11–16)

| # | File | Content |

|---|---------|------|

| 11 | [11_Motor3Phase_BandGate_live_JP.html](./11_Motor3Phase_BandGate_live_JP.html) | **Three-phase motor Band Gate live monitor.** Applies R = δ/τ to load balance and overload detection. |

| 12 | [12_agri_mol_antagonism_JP.html](./12_agri_mol_antagonism_JP.html) | **Agricultural ion monitoring + Mg²⁺/K⁺ antagonistic chain Band Gate.** Dynamic τ and asymmetric EMA. |

| 13 | [13_photosynthesis_layer5_JP.html](./13_photosynthesis_layer5_JP.html) | **Photosynthesis Layer 5 monitor.** Uses the FvCB model as an external δ generator, then evaluates R = δ/τ. |

| 14 | [14_powergrid_transition_JP.html](./14_powergrid_transition_JP.html) | **Power-grid transition-point monitor.** Detects early structural divergence missed by fixed thresholds. |

| 15 | [15_or_icu_continuum_JP.html](./15_or_icu_continuum_JP.html) | **OR/ICU cumulative monitoring.** Tracks accumulated structural deviation across surgery and ICU phases. |

| 16 | [16_passive_safety_JP.html](./16_passive_safety_JP.html) | **Passive gravity-driven safety system.** Transitions to a safe state by physical constraints without active control. |

---

### 🔬 STEP 8 — Physical State Transition Monitoring (17–22)

| # | File | Content |

|---|---------|------|

| 17 | [17_water_ice_phase_transition_JP.html](./17_water_ice_phase_transition_JP.html) | **Water → ice phase transition.** Tracks approach to the 0°C phase boundary using R. |

| 18 | [18_chain_tension_JP.html](./18_chain_tension_JP.html) | **Chain tension with polygon effect and automatic adjustment.** Uses dR/dt prediction before limit arrival. |

| 19 | [19_air_pressure_JP.html](./19_air_pressure_JP.html) | **Air pressure management with compressible fluid and dynamic τ.** τ_hi shrinks with temperature via gas-law behavior. |

| 20 | [20_water_pressure_JP.html](./20_water_pressure_JP.html) | **Water pressure management with incompressible fluid and water hammer.** Simulates pump pulsation and valve-closing impact. |

| 21 | [21_cabg_monitor_JP.html](./21_cabg_monitor_JP.html) | **CABG monitor.** Monitors blood flow, pressure, and temperature during bypass surgery as an educational safety demo. |

| 22 | [22_vascular_monitor_JP.html](./22_vascular_monitor_JP.html) | **Vascular intervention monitor.** Six physical quantities integrated with dual fluctuation and dynamic τ. |

---

### 🧩 STEP 9 — Advanced Features and Specific Domains (23–26)

| # | File | Content |

|---|---------|------|

| 23 | [23_sample_demo_JP.html](./23_sample_demo_JP.html) / [EN](./23_sample_demo_EN.html) | **State boundary, short-term logs, and long-term reconstruction.** Demonstrates separation of short-term fluctuation and long-term structural trend. |

| 24 | [24_vehicle_mandatory_boundary_JP.html](./24_vehicle_mandatory_boundary_JP.html) / [EN](./24_vehicle_mandatory_boundary_EN.html) | **Autonomous-driving mandatory boundary demo.** Monitors collision time margin, braking distance, and lateral margin. |

| 25 | [25_dam_degradation_JP.html](./25_dam_degradation_JP.html) / [EN](./25_dam_degradation_EN.html) | **Dam management comparison + τ degradation curve.** Fixed-threshold monitoring vs NRA-IDE τ degradation tracking. |

| 26 | [JP](./26_escapement_contactpoint_JP.html) | **Phase-Gap Engine — heat release only at contact points.** Demonstrates that error/heat occurs at phase-boundary contact points, not across the whole continuous calculation. (Japanese only) |

---

### 🛠️ STEP 10 — Basic Equipment Monitoring (27–32)

These demos apply R = δ/τ to general equipment and facility monitoring domains. Across six demos, they demonstrate NRA-IDE’s **unit independence**: the same structural equation can manage fundamentally different physical quantities.

| # | File | Domain | Key Point |

|---|---------|---------|---------|

| 27 | [JP](./27_belt_tension_JP.html) / [EN](./27_belt_tension_EN_20260425_011850_JST.html) | Belt conveyor / V-belt tension | Defines τ as the full margin from optimal value to structural limit. Fail-Closed stops the belt. |

| 28 | [JP](./28_water_temp_JP.html) / [EN](./28_water_temp_EN_20260425_012100_JST.html) | Water temperature upper/lower management | Evaluates R_hi and R_lo independently. |

| 29 | [JP](./29_light_lux_JP.html) / [EN](./29_light_lux_EN_20260425_012747_JST.html) | Light / illuminance management | Measures the receiving side in lux and increases shading from the precursor stage. |

| 30 | [JP](./30_power_JP.html) / [EN](./30_power_EN_20260425_012956_JST.html) | Power management using V × I | Integrates voltage and current as P = V × I; sustained over-power raises R over time. |

| 31 | [JP](./31_move_water_or_ice_JP.html) / [EN](./31_move_water_or_ice_EN_20260425_013623_JST.html) | Water/ice state navigation | Interactive phase-transition navigation while tracking R at the boundary. |

| 32 | [JP](./32_nra_ide_water_ice_20260324_2216_JP.html) / [EN](./32_nra_ide_ice_water_EN_20260425_013818_JST.html) | Ice → water phase transition | Reverse direction of Demo 17: ice absorbs latent heat after crossing 0°C. |

---

### 🔭 Standalone Demos

| File | Content |

|---------|------|

| [JP](./33_nra_ide_6d_layer_viz_JP_2026-03-21_1237.html) / [EN](./33_nra_ide_6d_layer_viz_EN_20260425_013923_JST.html) | **6D multi-layer visualizer.** Displays six R-value surfaces simultaneously. Opacity, saturation, and monochrome modes are available. |

| [Bilingual](../docs/en-US/figures/causal_diode_fail_closed_Bilingual.html) | **Causal Diode & Fail-Closed Visualizer.** An intuitive animation demonstrating how NRA-IDE structurally blocks AI from manipulating physical thresholds (Π⁻¹ backward flow) and how it autonomously shuts down upon reaching the limit. |

---

### 🔗 STEP 11 — Correlation and Multi-Factor Templates (34–41)

From Demo 34 onward, the sample set develops from single-quantity R judgment into multi-layer correlation, mediated variables, closed loops, and individual baseline differences. The basic safety form is **R_total = max(R_i, R_corr, R_coupling)** so that a dangerous layer is not diluted by averaging. Medical examples are kept as **Medical Education Templates**, not operational clinical systems.

| # | File | Domain | Key Point |

|---|---------|---------|---------|

| 34 | [JP](./34_NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_JP.html) / [EN](./34_NRA-IDE_AgroDrone_4Factor_Simulation_2026-04-20_2041_EN.html) | Seedling greenhouse / agro-drone four-factor correlation | Tracks temperature, humidity, light, and water with R = δ/τ. Combines correlation matrix C[i][j](t), residual gate G(r), and delayed observed record x_{t-τ}. |

| 35 | [JP](./35_rotor_bearing_correlation_JP_20260425_024602_JST.html) / [EN](./35_rotor_bearing_correlation_EN_20260425_160443_JST.html) | Rotor / bearing correlation | Monitors vibration, bearing temperature, current, lubrication pressure, acoustic noise, and RPM deviation. Vibration leads, then temperature/current/noise follow. |

| 36 | [JP](./36_battery_thermal_runaway_correlation_JP_20260425_025803_JST.html) / [EN](./36_battery_thermal_runaway_correlation_EN_20260425_160443_JST.html) | Battery thermal runaway correlation | Treats internal resistance and dT/dt as leading indicators, then shows propagation to temperature, swelling pressure, and voltage deviation. Educational visualization only, not real control. |

| 37 | [JP](./37_greenhouse_vpd_correlation_JP_20260425_032257_JST.html) / [EN](./37_greenhouse_vpd_correlation_EN_20260425_160443_JST.html) | Greenhouse VPD-mediated correlation | Does not simply add temperature and humidity. VPD acts as a mediator layer, propagating correlation pressure to soil water, CO₂, light, and EC. |

| 38 | [JP](./38_datacenter_cascade_correlation_JP_20260425_032611_JST.html) / [EN](./38_datacenter_cascade_correlation_EN_20260425_160443_JST.html) | Datacenter cascade correlation | Connects CPU load, power, rack temperature, inlet temperature, fan rate, airflow, and latency. Visualizes the positive feedback loop power → heat → fan → power. |

| 39 | [JP](./39_coldchain_temperature_correlation_JP_20260425_033809_JST.html) / [EN](./39_coldchain_temperature_correlation_EN_20260425_160443_JST.html) | Cold-chain temperature excursion correlation | Connects ambient temperature, cargo temperature, door opening, compressor load, battery level, humidity, and delivery delay. Shows the mediation chain ambient + door → compressor reserve → cargo temperature. |

| 40 | [JP](./40_medical_education_individual_stratification_template_JP_20260425_040110_JST.html) / [EN](./40_medical_education_individual_stratification_template_EN_20260425_160443_JST.html) | Medical education / individual stratification | Uses synthetic data for SpO₂, respiratory rate, heart rate, systolic BP, and temperature. Visualizes individual reserve differences via profile pressure from age, frailty, and chronic background. Not diagnosis or treatment. |

| 41 | [JP](./41_medical_education_infection_observation_template_JP_20260425_040544_JST.html) / [EN](./41_medical_education_infection_observation_template_EN_20260425_160443_JST.html) | Medical education / infection observation cohort | Uses synthetic data for fever, respiration, circulation, hydration, and inflammation-like markers. Sorts individuals into Observe / Watch / Caution / Human Review without disease naming or treatment recommendation. |

---

## How to Embed

Physical control begins by defining the target’s deviation (δ) and tolerance thickness (τ).

```javascript

// Minimal example

function gate(delta, tau) {

    const R = delta / tau;

    if (R >= 1.0) return "FAIL_CLOSED";

    return "SAFE";

}

```

**Implementation example: medical AI support**

```javascript

// Physically verify drug delivery reachability

const tumorResistance = measureResistance();  // δ: tumor-side resistance

const infusionPressure = getPumpCapacity();   // τ: available pump pressure

const deliveryStatus = gate(tumorResistance, infusionPressure);

if (deliveryStatus === "FAIL_CLOSED") {

    alert("Physical reachability failure detected. Human medical judgment is required.");

    // AI stops judgment and transfers authority to a qualified human.

}

```

Specific implementation patterns are documented inside each demo source file.

---

## Application Areas

### 🏥 Medical AI

- **Problem:** Uncertainty of physical drug reachability to the target.

- **NRA solution:** Verify physical consistency of the delivery path.

- **Threshold:** R = target-side resistance / delivery pressure.

### 🚗 Autonomous Driving

- **Problem:** Safety issues caused by black-box decisions.

- **NRA solution:** Verify structural constraints for collision avoidance.

- **Threshold:** R = obstacle margin / braking capability.

### 🖥️ Infrastructure Resilience

- **Problem:** Cascade failure in distributed systems.

- **NRA solution:** Prevent propagation by monitoring load-limit approach.

- **Threshold:** R = excess load / buffer capacity.

| Area | δ (Deviation from constraint) | τ (Tolerance thickness) | Meaning of R ≥ 1.0 |

|------|-------------------------------|--------------------------|--------------------|

| Medical AI | Target-side resistance | Delivery pressure | The drug physically cannot reach the target |

| Autonomous driving | Obstacle time/distance margin | Braking distance/capability | Collision danger → emergency stop |

| Infrastructure | Excess load | Buffer capacity | Server overload → isolation |

---

## License

Redistribution must preserve the following copyright notice:

**Copyright (c) 2026 M-Tokuni**

This project is provided under the **MIT License**. It may be used, modified, and redistributed for research, personal, and commercial purposes, subject to the license terms.

For the latest information, see the official repository:

- **GitHub:** https://github.com/M-Tokun/NRA-IDE

---

- **Facebook:** https://www.facebook.com/tokuni.masa

- **Note:** https://note.com/mtokuni
