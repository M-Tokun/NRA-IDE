# NRA-IDE Examples — English Edition

<!-- README_EN.md | examples/ | updated 20260425_163041_JST -->

---

## Canonical Reference Quick Demo

Run the current normative reference implementation from the repository root:

```powershell
python examples/nra_ide_reference_quick_demo.py
```

The demo calls [`nra-core/foundations/NRA-IDE_Architecture_public.py`](../nra-core/foundations/NRA-IDE_Architecture_public.py) directly and checks seven canonical outcomes: `PERMIT`, `BOUNDARY_WARNING`, `HANDOFF_REQUIRED`, `IRREVERSIBLE_TRANSITION`, `RUPTURE_BOUNDARY`, `CONFESSION`, and `OUT_OF_DESCRIPTION_DOMAIN`.

Its thresholds are explicit demonstration values, not inferred defaults. The demo is not a separate canonical evaluator and must not be used for medical, autonomous-control, or other operational decisions.

Other examples in this directory preserve research, explanatory, illustrative, domain-specific, or historical work and may use legacy state names.

---

## What is NRA-IDE?

**Nomological Ring Axioms — Intensional Dynamics Engine**

NRA-IDE describes the present boundary state of a declared target from Cause-Side accumulated deviation and absorption thickness. Domain-specific observations and construction rules determine those variables. This evaluation structure does not provide a universal physical model or a safety guarantee. See the [root introduction](../README.md) and [canonical definitions](../theory/AXIOMS.md).

---

## Numerical Residuals and Integer Phase Lock

Integer phase lock is a design principle for preventing rounding errors and residuals from being inherited by the next state without audit. It does not establish that all physical or numerical error is absent, and individual demos require their own verification.

Known rounding, approximation and discarded residuals with established values and provenance belong in `STRUCTURAL_DISCLOSURE_LOG`. Unknown, invalid, ambiguous, non-finite or unsupported structural information is `CONFESSION`; it belongs in `INPUT_EXCEPTION_LOG`, separately from known numeric progression.

---

## Current Canonical Threshold System

`R = delta / tau`: delta is accumulated deviation, tau is absorption thickness, and R is the boundary-approach ratio. Finite delta >= 0 and finite tau > 0 are required. The three predeclared domain thresholds satisfy `0 <= R_warn < R_handoff < R_irrev < 1`.

| Canonical state | Condition | Adapter operational action |
|---|---|---|
| `PERMIT` | 0 <= R < R_warn | CONTINUE |
| `BOUNDARY_WARNING` | R_warn <= R < R_handoff | LOG_WARN |
| `HANDOFF_REQUIRED` | R_handoff <= R < R_irrev | Fail-Closed |
| `IRREVERSIBLE_TRANSITION` | R_irrev <= R < 1, or retained irreversible latch | Fail-Closed |
| `RUPTURE_BOUNDARY` | R >= 1, or retained target rupture | Fail-Closed |
| `CONFESSION` | Invalid or unknown structural input/declaration | Fail-Closed |
| `OUT_OF_DESCRIPTION_DOMAIN` | tau = 0 for otherwise valid structure | Fail-Closed |

The adapter retains irreversible and target-rupture history across calls. A lower R does not clear either state. Invalid new samples are disclosed separately without clearing the target history. Fail-Closed suppresses affected new autonomous judgment and operation; it is not an eighth state or complete silence. Surviving observation, logging and communication continue independently, with continuing `POST_RUPTURE_FIXED` testimony after target rupture.

Remaining margins are distinct: `M_R = 1 - R` is dimensionless; `M_tau = tau - delta` has the same unit as delta and tau. Concrete thresholds require a domain basis. The SOFTWARE_DEMO values 0.4/0.6/0.8 are unvalidated illustrative values.

The tables below describe local behavior of historical or domain-specific demos. Their SAFE/WATCH/CAUTION/R_J labels and reset controls do not define current canonical states, thresholds or recovery authorization.

---

## Demo List — 50+ Demos + Standalone Visualizations, Recommended Order

All demos run directly in a browser. No installation is required.

> In many demos, the red line indicates R = 1.0. This is not a warning line; it is the structural limit line. The practical judgment limit must be placed before that line. Its value is not fixed, and should be configured according to the operating site and target domain.

### Judgment limits (R_J) per demo

**Historical demo conventions:** Many ratio-based demos use R = 1.0 for a local rupture or suppression boundary; non-canonical scores and other exceptions are described in their source files. 0.4 is the start of WATCH in many demos. The warning threshold in between (the judgment limit R_J) is a value declared per demo, not a fixed axiom value (see the note above).

| Demo | Warning / judgment limit | Note |
|---|---|---|
| #08–#11 | WARN 0.65 (log); colors at 0.7 | Upper and lower sides evaluated separately. SILENCE at R ≥ 1.0 |
| #12, #13, #17, #18–#20, #27–#32, #36–#39 | WARN 0.75 | #36 also uses WATCH 0.4 |
| #14 | CAUTION 0.4 | Rupture at R ≥ 1.0 or debt > 0.8 |
| #15 | CAUTION 0.35, CRITICAL 0.6 | Judged on R_eff (R_total + debt × 0.4) |
| #23, #24 | DAMP 0.72 | Rupture (SILENCE / FALLBACK) at 1.0 |
| #34, #35 JP, #48 | WARNING 0.7 | #35 EN uses WATCH 0.40 / WARN 0.75 (separate implementation) |
| #40, #41 | Watch 0.40, Caution 0.75 | Human Review at 1.0 |
| #42, #46 | ZONE B 0.40, C 0.70 | D (RUPTURE_BOUNDARY; Fail-Closed suppression) at 1.0 |
| #43 | ZONE B 0.40, C 0.70, D 0.85 | E (RUPTURE_BOUNDARY; Fail-Closed suppression) at 1.0 |

All values are demo-declared; in operation they are set from the target, the sensor delay, and the time needed to stop.

> Demos that enter RUPTURE_BOUNDARY, FAIL, or FALLBACK keep that state until "New evaluation" ("Reset" in #23) is pressed (irreversible latch). The R value keeps showing the current reading. The SILENCE in demos 08–11 is a temporary cut-off released after the HOLD time; it is a different concept from latching the rupture boundary.

### 📚 STEP 1 — First Understand “Why?”

| # | File | Content |
|---|---------|------|
| 00 | [00_Escapement_Foundation_NRA_JP.html](./00_Escapement_Foundation_NRA_JP.html) | **Escapement Foundation (JP).** Basic concept demo of integer phase lock — why residuals disappear. (Japanese only) |
| 01 | [01_Why_No_Distance_EN.html](./01_Why_No_Distance_EN.html) | **Why not use distance, calculus, or floating-point continuity as the primary basis?** A visual introduction from four perspectives. |
| 02 | [02_Error_Accumulation_EN.html](./02_Error_Accumulation_EN.html) | **The danger of error accumulation.** Runs 100,000 steps from the same initial value and compares conventional methods with NRA-style structure. |

### 🔬 STEP 2 — Experience the Difference in Behavior

| # | File | Content |
|---|---------|------|
| 03 | [03_HAN_vs_Legacy_EN.html](./03_HAN_vs_Legacy_EN.html) | **HAN vs Legacy real-time comparison.** Compares tracking and stability under disturbance and sudden load on a simplified model (the ratio is clamped at 0.99 and the force at ±20, so it does not guarantee that the limit is never crossed). |
| 04 | [04_HAN_Stress_Test_EN.html](./04_HAN_Stress_Test_EN.html) | **Extreme 80 ms load test.** Legacy blindly executes commands and collapses in FPS; HAN detects tension and adapts load. |

### 📊 STEP 3 — Visualize the Threshold Mechanism

| # | File | Content |
|---|---------|------|
| 05 | [05_IDE_Threshold_Visualizer_EN.html](./05_IDE_Threshold_Visualizer_EN.html) | **Phase scope of integer phase lock and residual discard.** Does not compute R, δ or τ themselves; it illustrates the discretization. |

### ⚙️ STEP 4 — Escapement Principle

| # | File | Content |
|---|---------|------|
| 06 | [06_Escapement_Principle_JP.html](./06_Escapement_Principle_JP.html) | **Why gears do not accumulate error.** Floating-point drift vs integer phase lock animation. (Japanese only; there is no EN page yet.) |

### 🔴 STEP 5 — Cascade Failure: Watching the Moment Collapse Begins

| # | File | Content |
|---|---------|------|
| 07 | [07_HAN_gate_live_EN.html](./07_HAN_gate_live_EN.html) | **Live simulation of cascade failure and HAN Gate SILENCE activation.** The non-canonical chain-warning score rises with the load spike; SILENCE starts when it reaches the local score limit. This is not canonical R = δ/τ. |

> **Why this demo is different:**  

> The waveform is not a static graph. The orange line shows an EMA-based score gain, not canonical absorption thickness τ. The illustrative simulation uses different normalization and EMA inputs from the deployed HAN Gate service.

---

### 🌿 STEP 6 — Band Gate: Real-World Domain Applications

These demos apply Band Gate logic, R = δ/τ, to physical measurement domains. Upper and lower limits are monitored independently, and asymmetric EMA sensitivity detects both overload and depletion.

| # | File | Domain | Key Point |
|---|---------|---------|---------|
| 08 | [08_Band_Gate_live_JP.html](./08_Band_Gate_live_JP.html) | Electricity, air temperature, water pressure, pulsation — JP | **Asymmetric damper structure.** δ is the deviation from the reference; R = 1.0 at the declared limits. Sustained deviation shrinks τ for earlier detection (never widens). Upper side shrinks little (cautious), lower side shrinks more (sensitive). |
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
| 11 | [JP](./11_Motor3Phase_BandGate_live_JP.html) / [EN](./11_Motor3Phase_BandGate_live_EN.html) | **Three-phase motor Band Gate live monitor.** Applies R = δ/τ to load balance and overload detection. |
| 12 | [JP](./12_agri_mol_antagonism_JP.html) / [EN](./12_agri_mol_antagonism_EN.html) | **Agricultural ion monitoring + Mg²⁺/K⁺ antagonistic chain Band Gate.** Dynamic τ and asymmetric EMA. |
| 13 | [JP](./13_photosynthesis_layer5_JP.html) / [EN](./13_photosynthesis_layer5_EN.html) | **Photosynthesis Layer 5 monitor.** Uses the FvCB model as an external δ generator, then evaluates R = δ/τ. |
| 14 | [JP](./14_powergrid_transition_JP.html) / [EN](./14_powergrid_transition_EN.html) | **Power-grid transition-point monitor.** Detects early structural divergence missed by fixed thresholds. |
| 15 | [JP](./15_or_icu_continuum_JP.html) / [EN](./15_or_icu_continuum_EN.html) | **OR/ICU cumulative monitoring.** Tracks accumulated structural deviation across surgery and ICU phases. |
| 16 | [JP](./16_passive_safety_JP.html) / [EN](./16_passive_safety_EN.html) | **Passive gravity-driven safety system.** Transitions to a safe state by physical constraints without active control. |

---

### 🔬 STEP 8 — Physical State Transition Monitoring (17–22)

| # | File | Content |
|---|---------|------|
| 17 | [JP](./17_water_ice_phase_transition_JP.html) / [EN](./17_water_ice_phase_transition_EN.html) | **Water → ice phase transition.** The input is the heat Q removed; the temperature stops at 0°C for the latent heat (334 kJ/kg). R = 1.0 coincides with the start of freezing (0°C); beyond it the state is "boundary reached, transition in progress". In the dynamic τ model R ≥ 1 is a model-side alert boundary, not the physical phase transition. |
| 18 | [JP](./18_chain_tension_JP.html) / [EN](./18_chain_tension_EN.html) | **Chain tension with polygon effect and automatic adjustment.** Uses dR/dt prediction before limit arrival. |
| 19 | [JP](./19_air_pressure_JP.html) / [EN](./19_air_pressure_EN.html) | **Air pressure management with compressible fluid and dynamic τ.** Temperature rise raises the pressure (δ side); τ_hi shrinks under an assumed loss of material strength with temperature (demo assumption). |
| 20 | [JP](./20_water_pressure_JP.html) / [EN](./20_water_pressure_EN.html) | **Water pressure management with incompressible fluid and water hammer.** Simulates pump pulsation and valve-closing impact. |
| 21 | [JP](./21_cabg_monitor_JP.html) / [EN](./21_cabg_monitor_EN.html) | **CABG monitor.** Monitors graft flow (MGF), pulsatility index (PI), and diastolic filling (DF) during bypass surgery, with the tolerance adjusted by temperature and blood flow, as an educational safety demo. |
| 22 | [JP](./22_vascular_monitor_JP.html) / [EN](./22_vascular_monitor_EN.html) | **Vascular intervention monitor.** Six quantities (pressure, shear, wall tension, flow, temperature, adhesion) are each evaluated against a reference and a declared limit, upper and lower sides separately, with τ shrinking with temperature (dual fluctuation). Combined by the maximum; rupture is latched. Action buttons: balloon inflation, flow stasis, cooling. Educational; reference values are not clinical criteria. |

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
| 27 | [JP](./27_belt_tension_JP.html) / [EN](./27_belt_tension_EN.html) | Belt conveyor / V-belt tension | Defines τ as the full margin from optimal value to structural limit. Fail-Closed stops the belt. |
| 28 | [JP](./28_water_temp_JP.html) / [EN](./28_water_temp_EN.html) | Water temperature upper/lower management | Evaluates R_hi and R_lo independently. |
| 29 | [JP](./29_light_lux_JP.html) / [EN](./29_light_lux_EN.html) | Light / illuminance management | Measures the receiving side in lux and increases shading from the precursor stage. |
| 30 | [JP](./30_power_JP.html) / [EN](./30_power_EN.html) | Power management using V × I | Integrates voltage and current as P = V × I; sustained over-power raises R over time. |
| 31 | [JP](./31_move_water_or_ice_JP.html) / [EN](./31_move_water_or_ice_EN.html) | Water/ice state navigation | Interactive phase-transition navigation: remove (freezing) or add (melting) the heat Q and track R at the boundary, including the latent-heat interval. |
| 32 | [JP](./32_nra_ide_water_ice_JP.html) / [EN](./32_nra_ide_ice_water_EN.html) | Ice → water phase transition | Reverse direction of Demo 17: heat Q added to ice brings it to 0°C, and R is tracked while it absorbs latent heat and melts (R = 1.0 at the start of melting). |

---

### 🔭 Standalone Demos

| File | Content |
|---------|------|
| [JP](./33_nra_ide_6d_layer_viz_JP.html) / [EN](./33_nra_ide_6d_layer_viz_EN.html) | **6D multi-layer visualizer.** Displays six R-value surfaces simultaneously. Opacity, saturation, and monochrome modes are available. |
| [EN](../docs/en-US/figures/causal_diode_fail_closed_EN.html) / [JP](../docs/ja-JP/figures/causal_diode_fail_closed_JP.html) | **Causal Diode & Fail-Closed Visualizer.** An intuitive animation demonstrating how NRA-IDE structurally blocks AI from manipulating physical thresholds (Π⁻¹ backward flow) and how it autonomously shuts down upon reaching the limit. |

---

### 🔗 STEP 11 — Correlation and Multi-Factor Templates (34–41)

From Demo 34 onward, the sample set develops from single-quantity R judgment into multi-layer correlation, mediated variables, closed loops, and individual baseline differences.

> **The JP and EN pages of Demos 35–41 and 49 are separate implementations.** Their factor sets, warning thresholds, correlation normalization widths, and state names differ (e.g. in Demo 35 the JP page warns at 0.70 while the EN page uses WATCH 0.40 / WARN 0.75). Running both with the same input does not give the same result. The differences are noted in the comment at the top of each page's code. The basic safety form is **R_total = max(R_i, R_corr, R_coupling)** so that a dangerous layer is not diluted by averaging. Medical examples are kept as **Medical Education Templates**, not operational clinical systems.

| # | File | Domain | Key Point |
|---|---------|---------|---------|
| 34 | [JP](./34_NRA-IDE_AgroDrone_4Factor_Simulation_JP.html) / [EN](./34_NRA-IDE_AgroDrone_4Factor_Simulation_EN.html) | Seedling greenhouse / agro-drone four-factor correlation | Tracks temperature, humidity, light, and water with R = δ/τ. Combines correlation matrix C[i][j](t), residual gate G(r), and delayed observed record x_{t-τ}. |
| 35 | [JP](./35_rotor_bearing_correlation_JP.html) / [EN](./35_rotor_bearing_correlation_EN.html) | Rotor / bearing correlation | Monitors vibration, bearing temperature, current, lubrication pressure, acoustic noise, and RPM deviation. Vibration leads, then temperature/current/noise follow. |
| 36 | [JP](./36_battery_thermal_runaway_correlation_JP.html) / [EN](./36_battery_thermal_runaway_correlation_EN.html) | Battery thermal runaway correlation | Treats internal resistance and dT/dt as leading indicators, then shows propagation to temperature, swelling pressure, and voltage deviation. Educational visualization only, not real control. |
| 37 | [JP](./37_greenhouse_vpd_correlation_JP.html) / [EN](./37_greenhouse_vpd_correlation_EN.html) | Greenhouse VPD-mediated correlation | Does not simply add temperature and humidity. VPD acts as a mediator layer, propagating correlation pressure to soil water, CO₂, light, and EC. |
| 38 | [JP](./38_datacenter_cascade_correlation_JP.html) / [EN](./38_datacenter_cascade_correlation_EN.html) | Datacenter cascade correlation | Connects CPU load, power, rack temperature, inlet temperature, fan rate, airflow, and latency. Visualizes the positive feedback loop power → heat → fan → power. |
| 39 | [JP](./39_coldchain_temperature_correlation_JP.html) / [EN](./39_coldchain_temperature_correlation_EN.html) | Cold-chain temperature excursion correlation | Connects ambient temperature, cargo temperature, door opening, compressor load, battery level, humidity, and delivery delay. Shows the mediation chain ambient + door → compressor reserve → cargo temperature. |
| 40 | [JP](./40_medical_education_individual_stratification_template_JP.html) / [EN](./40_medical_education_individual_stratification_template_EN.html) | Medical education / individual stratification | Uses synthetic data for SpO₂, respiratory rate, heart rate, systolic BP, and temperature. Visualizes individual reserve differences via profile pressure from age, frailty, and chronic background. Not diagnosis or treatment. |
| 41 | [JP](./41_medical_education_infection_observation_template_JP.html) / [EN](./41_medical_education_infection_observation_template_EN.html) | Medical education / infection observation cohort | Uses synthetic data for fever, respiration, circulation, hydration, and inflammation-like markers. Sorts individuals into Observe / Watch / Caution / Human Review without disease naming or treatment recommendation. |

---

### 🚀 STEP 12 — Extended POC and Additional Concepts (42–52)

From Demo 42 onward, the demos cover POCs for autonomous driving, robot control, FPGA implementation, and foundational philosophy.

| # | File | Domain / Content |
|---|---------|---------|
| 42 | [JP](./42_AutoDrive_POC_2_JP.html) / [EN](./42_AutoDrive_POC_2_EN.html) | Autonomous Driving Gate POC 2 (Early-stage limit setting and operation demo) |
| 43 | [JP](./43_AutoDrive_POC_3_JP.html) / [EN](./43_AutoDrive_POC_3_EN.html) | Autonomous Driving Gate POC 3 (Advanced boundary testing) |
| 44 | [JP](./44_RobotArm_POC_1_JP.html) / [EN](./44_RobotArm_POC_1_EN.html) | Industrial Robot Arm Control POC 1 |
| 45 | [JP](./45_HybridCalc_vs_Traditional_JP.html) / [EN](./45_HybridCalc_vs_Traditional_EN.html) | Hybrid Calculation vs. Traditional Method Comparison |
| 46 | [JP](./46_Connection_vs_Mixing_JP.html) / [EN](./46_Connection_vs_Mixing_EN.html) | Connection vs Mixing (Risk evaluation of connection and mixing) |
| 47 | [JP](./47_FPGA_Demo_SPEED_JP.html) / [EN](./47_FPGA_Demo_SPEED_EN.html) | FPGA Hardware Implementation Speed Demo |
| 48 | [JP](./48_Human_5Factors_Correlation_JP.html) / [EN](./48_Human_5Factors_Correlation_EN.html) | Human 5-Factor Correlation Real-Value Transition Demo (Initial lightweight medical template) |
| 49 | [JP](./49_Architecture_Infographic_JP.html) / [EN](./49_Architecture_Infographic_EN.html) | NRA-IDE Architecture Infographic |
| 50 | [JP](./50_Constraint_Philosophy_JP.html) / [EN](./50_Constraint_Philosophy_EN.html) | Philosophy Concept "Constraint is not a limitation. Constraint is the force that drives intelligence." |
| 52 | [JP](./52_Hybrid_DoubleFluctuation_EntropyTracking_JP.html) | Hybrid Double Fluctuation Entropy Tracking |
| 53 | [JP](./53_Formula_Lab_JP.html) | Formula Lab — Interactive prototype visualizing the primary formula (R = δ/τ) and secondary formula (dual fluctuation, R_upper / R_lower) as boundary motion with synchronized explanation. (Japanese only) |

---

## How to Embed

Run this unvalidated software example from the repository root. It uses the current adapter rather than a separate two-state evaluator.

```python
import json
from pathlib import Path
from gate.en import ThresholdGuardian

demo = json.loads(Path('config/ide_presets.json').read_text(encoding='utf-8'))['presets']['SOFTWARE_DEMO']
gate = ThresholdGuardian(config=demo)
notice = gate.evaluate(0.995, 1.0, timestamp='DEMO_T0').as_dict()
assert notice['status'] == 'IRREVERSIBLE_TRANSITION'
assert notice['fail_closed'] is True
```

The default configuration is deliberately undeclared and returns `CONFESSION`. Real evaluation requires predeclared target, unit, source, delta/tau rules, applicable domain, threshold basis and per-call observation time. Retain the same instance and preserve its history across restarts; creating a new instance does not establish recovery. See [current gate documentation](../gate/en/README.md). Physical control and domain safety are not established by this example.

---

## Application Areas

### 🚗 Autonomous Driving

- **Problem:** Safety issues caused by black-box decisions.

- **NRA solution:** Verify structural constraints for collision avoidance.

- **Threshold:** R = (intrusion of the stopping distance into the safety-margin band) / (safety-margin distance). R = 1.0 when stopping distance equals the gap.

### 🖥️ Infrastructure Resilience

- **Problem:** Cascade failure in distributed systems.

- **NRA solution:** Prevent propagation by monitoring load-limit approach.

- **Threshold:** R = (increase over the reference load) / (margin from the reference load to the allowed upper limit). R = 1.0 when the load equals the allowed limit.

| Area | δ (Deviation from constraint) | τ (Tolerance thickness) | Meaning of R ≥ 1.0 |
|------|-------------------------------|--------------------------|--------------------|
| Autonomous driving | Intrusion of the stopping distance into the safety-margin band (the last τ before the gap) | Safety-margin distance (fixed at design time) | Stopping distance ≥ gap: collision danger → emergency stop |
| Infrastructure | max(0, load − reference load) | Allowed limit − reference load | Load = allowed limit: server overload → isolation |

---

## License

Redistribution must preserve the following copyright notice:

**Copyright (c) 2026 M-Tokuni**

This project is provided under the **MIT License**. It may be used, modified, and redistributed for research, personal, and commercial purposes, subject to the license terms.

For the latest information, see the official repository:

- **GitHub:** https://github.com/M-Tokun/NRA-IDE
