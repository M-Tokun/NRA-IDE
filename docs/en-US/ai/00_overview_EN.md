# 00 Overall Structure — A Map for Navigating Boundaries

<!-- 00_overview_EN.md -->

---

## Position of This Chapter

This chapter serves as a guide to the overall structure of NRA-IDE, the role of each chapter, and the design principles shared across them.

For a first reading, proceed from this chapter in numerical order. After completing the individual chapters, return here to verify where each concept is positioned within the whole.

---

## Document Structure and Philosophy

This document follows a single question.

**“When a dynamic system that includes AI approaches an irreversible regime, can it avoid continuing output beyond its limits and delegate judgment to humans?”**

NRA-IDE begins from the design premise that **“Existence is generation.”** IDE describes structural states through the computational principle of fluctuation $\delta$, the structural thickness $\tau$ that absorbs that fluctuation, and their ratio, $R = \delta / \tau$. The axiom and the computational principle belong to different layers.

---

## Chapter Structure

### 1. Entry Point for Structural Transformation (01)

This chapter shows the difference between judging safety through meaning or scores after output, and handling structural states before and after output. It confirms the three design decisions established by NRA-IDE.

* **Experience:** [M1: Linear Breakdown Simulator](../../figures/M1_NRA_linear_breakdown_simulator.html)

### 2. Limits of Optimization and Computational Principles (02)

This chapter organizes the problems that optimization objectives introduce into safety judgment. It also introduces structural sensitivity, $S = 1 / (\tau \cdot (1 - R))$, and confirms the structure in which sensitivity diverges as $R$ approaches the phase-transition boundary.

* **Experience:** [M2: Residue Tank](../../figures/M2_NRA_residue_tank.html)

### 3. Structure of Isolation (03–04)

This chapter explains the Causal Diode, which blocks $\Pi^{-1}$—the backward inference of causes from effects—and the Sandwich Architecture, which separates the responsibilities of Pre-NRA / LLM / Post-NRA.

* **Experience:** [M3: Biomimetic Sandwich](../../figures/M3_NRA_biomimetic_sandwich_svg.html)

### 4. Honest Silence (05–08)

This chapter covers state classification through the ratio $R$, observable quantities, Fail-Closed, and Discard Logs. It presents a structure that stops autonomous output at a domain-specific point of approach to an irreversible regime and delegates judgment to humans. $R = 1.0$ is not an ordinary delegation point; it is the phase-transition boundary at which the structure itself can no longer remain established.

* **Experience:** [M4: Confession Debugger](../../figures/M4_NRA_confession_debugger.html)

### 5. Practice and Limits (09–11)

This chapter addresses patterns of misuse, the scope of what can be guaranteed, and domain tuning for $\tau$ and operating thresholds. Chapter 12 is a glossary. The Operational Checklist serves as a reference for implementation and operation.

* **Experience:** [M5: Glossary Flip Cards](../../figures/M5_NRA_IDE_flip_glossary.html)

---

## Structural Invariants

The following six principles remain unchanged throughout all chapters.

* **Non-Semantic**: Handles Cause-Side observables and structural states, rather than the naturalness of outputs or their semantic correctness.
* **Non-Optimization**: Does not set a center or score as an optimization objective; instead, it defines structural boundaries.
* **Causal Diode (prohibition of $\Pi^{-1}$)**: Does not infer causes (inputs) backward from effects (evaluation values).
* **Three-Layer Separation**: Strictly separates the boundaries of Pre-NRA / LLM / Post-NRA.
* **Fail-Closed**: Stops autonomous output at a domain-specific point of approach to an irreversible regime and delegates judgment to humans. The delegation-point value is determined according to the context, but the principle of delegation before the phase-transition boundary of $R = 1.0$ does not change.
* **Logs as Testimony**: Records the observables used at the time of stopping, the decision, and what was discarded, and does not use them in subsequent calculations.

---

## Related Resources

* **[README (Portal)](../../README_JP.md)**
* **[Design Philosophy of the Sandwich Architecture](../../Sandwich-ARCHITECTURE.md)**
* **[Complete Collection of Interactive Demonstrations](../../figures/NRA_IDE_interactive_docs_all_modules.html)**

---

### Copyright (c) 2026 M-Tokuni

### SPDX-License-Identifier: MIT
