# Canonical basis of examples 01–20

This document shows where in the canon each sample was built from, and what is central and what is auxiliary. Canon text is not copied here; only references are given: [AXIOMS.md](../theory/AXIOMS.md), [THEORY.md](../theory/THEORY.md), [FORMULA.md](../FORMULA.md), [Foundational Thesis](../theory/NRA-IDE_Foundational_Thesis_Bilingual.md), [Dictionary](../dictionary/NRA-IDE_Dictionary_EN.md). Japanese edition: [README_canon_basis_JP.md](./README_canon_basis_JP.md)

## 1. Read this first: what is central and what is auxiliary

| Class | Content | Basis |
|---|---|---|
| Central | **The integer step (the escapement, "heat discharge").** Evaluation advances one tooth at a time; the remainder between teeth is not discarded but recorded. | Thesis §9.1 (integer phase lock), AXIOMS §13 (STRUCTURAL_DISCLOSURE_LOG) |
| Central | **R = δ/τ is the subject of the judgment.** δ is the accumulated deviation from a reference state fixed before evaluation; τ is the absorption thickness (= "play"). | AXIOMS §3, §4, §5 |
| Central | **Latching of arrival, and history.** The moment R ≥ 1 is reached (value, time, channel) is kept and never erased. | AXIOMS §9, §10.5 |
| Auxiliary | Averaging, smoothing (EMA), decimal calculation, residual formulas, debt, R_total. **An auxiliary never lightens, overturns or replaces the judgment. It can only make stopping happen earlier.** | AXIOMS §4.5, FORMULA §4 |
| Auxiliary | Another target's R may be used only to **narrow** one's own side-specific effective gate width. | AXIOMS §14 |

"Play" is the absorption thickness τ that a structure holds. Rigor without play collapses (AXIOMS §3). τ does not recover spontaneously (AXIOMS §7). Where a width appears to come back on screen, it is a side-specific effective gate width, not a recovery of τ (THEORY dual-fluctuation formula, FORMULA §4).

**Distance and calculus are not denied.** Distance data is not deleted and calculus is not denied (THEORY, Thesis §6.1). They are simply not the main axis.

**Limits common to all samples.** All numbers, coefficients and reference values are demo-declared, not measurements and not an operational basis. The samples are idealized but kept within what holds as a realistic hypothesis even without experiments.

## 2. Basis per sample

Each entry gives: origin (where in the canon it was built from) / center / auxiliary / easily misread / not claimed.

### #01 Why no distance, calculus, or floating point
| | |
|---|---|
| Origin | AXIOMS §4 (δ, τ), Thesis §6.1, §9.1, THEORY (distance is not denied) |
| Center | Accumulated deviation δ from the reference (positive side only), thickness τ, the integer step |
| Auxiliary | Comparison display of distance / calculus (for contrast) |
| Easily misread | Reading it as "conventional methods are wrong". Only the main axis differs. |
| Not claimed | Superiority in real operation such as medicine. The formulas are simplified for explanation. |

### #02 Error accumulation
| | |
|---|---|
| Origin | Thesis §9.1, AXIOMS §13 (record of discarded remainders) |
| Center | The integer step; discarded remainders are recorded |
| Auxiliary | Display of floating-point error (a synthetic random walk) |
| Easily misread | "The axiom has zero error". Remainders do not vanish; they are recorded. |
| Not claimed | Failure lines of real equipment. No domain-specific numbers are given. |

### #03 HAN vs Legacy
| | |
|---|---|
| Origin | AXIOMS §5 (stop by the ratio to the boundary), §4.5 |
| Center | Reduce the load according to closeness to the limit (R) |
| Auxiliary | Smoothing, ratio cap 0.99, force cut-off ±20 |
| Easily misread | The 0.99 cap is a simplification of the model, not complete prevention |
| Not claimed | Complete prevention of limit overshoot |

### #04 HAN stress test
| | |
|---|---|
| Origin | AXIOMS §14 (another target's R is used only in the narrowing direction) |
| Center | When load grows, throttle drawing (move toward the safe side) |
| Auxiliary | Frame-rate estimate (about 25–30 fps, illustrative) |
| Easily misread | The structure avoids a return loop (one's own throttling changing one's own input) |
| Not claimed | Measured frame rates |

### #05 Integer phase lock visualizer
| | |
|---|---|
| Origin | Thesis §9.1, AXIOMS §13 |
| Center | Integer ticks; the remainder ε is recorded |
| Auxiliary | Floating-point comparison |
| Easily misread | R, δ and τ themselves are not computed in this figure |
| Not claimed | An implementation of the judgment |

### #06 Escapement principle
| | |
|---|---|
| Origin | Primary-formula derivation document, Part 3 step 6 (**not yet canonized**): one tooth = one evaluation, the span between teeth = transition between evaluations, the remainder is archived |
| Center | Advance one tooth at a time and archive the remainder instead of discarding it |
| Auxiliary | Particle motion, phase drawing |
| Easily misread | The escapement is a metaphor, not a canonical clause |
| Not claimed | A strict model of a mechanical clock |

### #07 HAN Gate (live)
| | |
|---|---|
| Origin | AXIOMS §10 (state classes), §12 (Fail-Closed) |
| Center | On reaching the threshold, SILENCE (stop autonomous operation) |
| Auxiliary | A **non-canonical** cascade precursor score |
| Easily misread | It is not the canonical R = δ/τ. SILENCE does not change the load itself. |
| Not claimed | Prediction accuracy for cascade failure |

### #08 Band Gate (live)
| | |
|---|---|
| Origin | AXIOMS §5 (R_dir = the larger of upper and lower), §7 (non-spontaneous τ recovery), FORMULA §4 |
| Center | Look at the upper and lower sides separately and take the heavier |
| Auxiliary | EMA, used only to **shrink** the side-specific effective gate width (never to widen it) |
| Easily misread | A width that appears to return is the effective gate width, not τ recovering |
| Not claimed | A physical basis for the coefficients (1/AMP_upper default 0.77, 1/AMP_lower default 0.5) |

### #09 Greenhouse, four indicators
| | |
|---|---|
| Origin | As #08; AXIOMS §6 (τ = 0 is out of the description domain) |
| Center | R per indicator, judged by the heavier |
| Auxiliary | The average is for reference display only |
| Easily misread | When τ = 0, R is not treated as ∞; it is out of the domain |
| Not claimed | Cultivation recommendations |

### #10 Field drought
| | |
|---|---|
| Origin | #08; AXIOMS §10.5 (once in SILENCE, it is held) |
| Center | If even one channel is in SILENCE, the level is Lv.3 or higher |
| Auxiliary | Weighted composite score (reference), look-ahead by momentum |
| Easily misread | Even if the composite is diluted by averaging, the fact of SILENCE does not disappear |
| Not claimed | Agronomic criteria for drought levels |

### #11 Three-phase motor
| | |
|---|---|
| Origin | AXIOMS §6, §15 (site-specific values are declared) |
| Center | Side-specific R per phase, heavier side |
| Auxiliary | Simple relations from rotation speed to ripple and cooling (demo assumptions) |
| Easily misread | 120% or more of the rating is treated as out of the description domain |
| Not claimed | Properties of a real motor |

### #12 Agricultural ion antagonism
| | |
|---|---|
| Origin | AXIOMS §14 (another target's output is used only toward the safe side = narrowing), §7 |
| Center | When the K⁺ excess-side R is high, the lower-side effective gate width of Mg²⁺ is narrowed |
| Auxiliary | Side-specific EMA (shrink only) |
| Easily misread | **The direction is the plant / soil one** (K excess inhibits Mg uptake). In the human body it is the reverse (Mg deficiency leads to hypokalemia). The width returns when R_K falls, so this is a link of the side-specific effective gate width, not τ recovering |
| Not claimed | Agronomic coefficients or fertilizer recommendations |

### #13 Photosynthesis Layer 5
| | |
|---|---|
| Origin | AXIOMS §14 (Cause-Side), §15 (domain-specific physical models are separated from the invariant evaluation structure) |
| Center | Apply R = δ/τ to a δ produced by an external model (FvCB). Latch at R ≥ 1 until "New evaluation" |
| Auxiliary | The nonlinear FvCB model; τ is Pmax |
| Easily misread | FvCB is not the center of the evaluation but an outside device that makes δ |
| Not claimed | Accuracy of the photosynthesis model |

### #14 Power-grid transition
| | |
|---|---|
| Origin | AXIOMS §4.5 (auxiliaries do not lower R), §10.5 |
| Center | δ = the raw frequency deviation; R ≥ 1 gives RUPTURE_BOUNDARY |
| Auxiliary | Residual debt and its stop (**shown separately as AUX_STOP**) |
| Easily misread | A stop by debt is not a substitute for the judgment by R |
| Not claimed | Real grid-operation criteria |

### #15 OR/ICU time-course accumulation
| | |
|---|---|
| Origin | AXIOMS §4 (reference fixed before evaluation), §4.5, §10.5, §7 |
| Center | The maximum of R over channels. During warm-up τ stays at the design value and the rupture judgment is not suppressed |
| Auxiliary | R_total and debt (AUX_STOP). Natural fluctuation does not accumulate |
| Easily misread | Warm-up changes only the elapsed time, not τ or the formula. Intervention is a physical action and does not undo a latched state class |
| Not claimed | Clinical meaning. The vitals are synthetic and cannot be used for diagnosis or treatment |

### #16 Passive safety
| | |
|---|---|
| Origin | AXIOMS §12 (Fail-Closed) |
| Center | On total loss of power, holding force drops to zero and gravity drops the control rod (autonomous operation stops and the system falls to the safe side) |
| Auxiliary | None (R is not computed) |
| Easily misread | This is not an R screen |
| Not claimed | Reactor design |

### #17 Water-to-ice phase transition
| | |
|---|---|
| Origin | AXIOMS §5 (remaining absorption margin M_τ), §6 (handling of τ = 0) |
| Center | Static τ: heat to the boundary. R = 1.0 is the arrival point at 0 °C |
| Auxiliary | Dynamic τ: temperature to the boundary (**corresponds to the remaining absorption margin**). On the flat 0 °C span τ = 0 and R is undefined |
| Easily misread | R ≥ 1 in the dynamic model is a model warning boundary, not the physical phase transition |
| Not claimed | Supercooling, impurity, or pressure effects |

### #18 Chain tension
| | |
|---|---|
| Origin | AXIOMS §5 (thickness differs between upper and lower sides), §4.5, §12 |
| Center | Judge by the heavier of R from raw tension and from smoothed tension. Upper τ = T_MAX − T_OPT, lower τ = T_OPT − T_MIN |
| Auxiliary | Look-ahead adjustment by dR/dt, smoothing, the polygon-effect wave |
| Easily misread | Smoothing is not a reason to miss an upper-limit excess. At RUPTURE the adjustment authority is handed back |
| Not claimed | Specifications of real chains or sprockets |

### #19 Air pressure
| | |
|---|---|
| Origin | FORMULA §4.4, §4.7 (dual fluctuation), THEORY (dual-fluctuation formula) |
| Center | A structure in which δ and τ fluctuate independently. Temperature is a constraint that narrows τ_hi, a side-specific effective gate width |
| Auxiliary | The pressure rise with temperature is counted on the δ side (not counted again on the τ side = no double counting) |
| Easily misread | What returns when it cools is the side-specific effective gate width, not τ. This screen does not itself judge the detection condition Δδ > 0 and Δτ < 0 |
| Not claimed | A measured material-strength law |

### #20 Water pressure
| | |
|---|---|
| Origin | AXIOMS §12, §6 (fixed τ) |
| Center | τ is fixed as for an incompressible fluid. Water hammer is a sudden change of δ |
| Auxiliary | Harmonics of pump pulsation; effective flow when the valve is throttled |
| Easily misread | Throttling the valve reduces the flow meter and the water particles. At RUPTURE autonomous operation stops, as in #19 |
| Not claimed | Properties of real piping |
