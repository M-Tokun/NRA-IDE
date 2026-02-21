# THEORY_EN.md — NRA-IDE: Nomological Ring Axioms & Intensional Dynamics Engine
# Full English Theory Definition | Authoritative Source
# Author: M-Tokuni | 2026-02-21
# GitHub: https://github.com/M-Tokun/NRA-IDE

---

## Abstract

NRA-IDE is an original axiomatic framework proposed by M-Tokuni (2026).
It redefines the structure of dynamic systems by rejecting spatial coordinates and
distance as causal factors, and instead grounds all behavior in structural constraint,
tension, and irreversible causality.

The framework provides a deterministic, fully explainable control architecture
for high-risk AI domains where probabilistic models are insufficient:
medical AI, autonomous systems, and critical infrastructure.

---

## 1. Foundational Axioms

### Axiom 1 — State Primacy
Time is not an independent dimension. It is a derived sequence of state transitions.
The system does not move through time; it transitions between states.

### Axiom 2 — Distance Negation
Distance is not a causal driver. It is a post-observation log only.
No calculation may use distance as an input to force or transition.

> Formally: `force ≠ f(distance)` — distance may only appear in observation output.

### Axiom 3 — Causal Irreversibility (Causal Diode)
Causality flows strictly forward: cause → effect.
Inverse derivation (deriving cause from effect, Π⁻¹) is structurally forbidden.

> Permitted: forward inference, feedback to future input
> Forbidden: reverse inference of past cause from present state

### Axiom 4 — Structural Constraint Primacy
All dynamics are driven by constraint (Law), tension (restoring force),
and energy dissipation — never by optimization targets.

### Axiom 5 — Fail-Closed with Continuity
When structural limits are exceeded (R ≥ 1.0), output is silenced.
The system does not halt — structural continuity (ω > 0) is maintained.
Final judgment is delegated to a human operator.

> Fail-Closed ≠ System Halt
> Fail-Closed = Silent output + Alive structure + Human delegation

### Axiom 6 — Duty of Testimony
Any approximation, linear invasion of a non-linear domain, or inverse derivation
performed by a computational process must be explicitly declared.
Results must not be presented as ground truth when approximation is involved.

---

## 2. Core Formula: Structural Ratio R

$$R = \frac{\delta}{\tau}$$

| Symbol | Meaning | Notes |
| :--- | :--- | :--- |
| **δ (Delta)** | Deviation from constraint | Directly measured physical displacement |
| **τ (Tau)** | Tolerance thickness | Design-time defined boundary width |
| **R** | Structural Ratio | Dimensionless stability index |

### Zone Structure

| Zone | Condition | Action | Structural State |
| :--- | :--- | :--- | :--- |
| A | R < 0.40 | PERMIT | Stable continuity |
| B | 0.40 ≤ R < 1.00 | PERMIT_WITH_CAVEAT | Elastic fluctuation |
| C | R ≥ 1.00 | FAIL_CLOSED | Structural fracture point |

**Zones carry no value judgment.** Zone A is not "good"; Zone C is not "bad."
They are structural classifications only.

---

## 3. System Architecture: Three-Layer Isolation

```
┌─────────────────────────────────────────────────────┐
│  INPUT                                              │
│    ↓                                                │
│  [ Pre-RNA Gate ]  ← Causal unit extraction (δ)    │
│    ↓                                                │
│  [ LLM / Inference Engine ]  ← Meaning generation  │
│    ↓   (no safety responsibility)                   │
│  [ Post-RNA Gate ]  ← Structural evaluation (R)    │
│    ↓                                                │
│  OUTPUT  or  FAIL_CLOSED (if R ≥ 1.0)              │
└─────────────────────────────────────────────────────┘
```

Each layer is isolated. Observation does not influence processing.
The LLM layer holds no safety responsibility — all structural validation
occurs in the Post-RNA gate.

---

## 4. DynamicState: The Medium-Independent Container

All force calculations operate on a normalized state container `DynamicState`.
The container shape is fixed; medium-specific behavior is injected via `Law` (transition functions).

| Field | Range | Meaning |
| :--- | :--- | :--- |
| `value` | [0.0, 1.0] | Current state (0 = stable, 1 = structural limit) |
| `rate` | ℝ | Rate of change dv/dt |
| `buffer` | ℝ≥0 | Dissipated energy accumulator — never discarded |
| `tension` | ℝ≥0 | Restoring force from constraint boundary |
| `history` | List | Instantaneous record — never averaged |

**Buffer principle:** Approximation residuals and excess energy are accumulated in `buffer`,
never zeroed. This implements Axiom 6 (Duty of Testimony) at the data structure level.

---

## 5. Key Distinctions from Existing Theories

| Concept | Conventional Physics / ML | NRA-IDE |
| :--- | :--- | :--- |
| **Space** | Absolute or relative container | Undefined — result of state projection only |
| **Distance** | Causal factor (inverse square law) | Post-observation log only — no causal power |
| **Time** | Independent dimension (t) | Derived sequence of state transitions |
| **Optimization** | Minimize objective function | Prohibited — viability, not optimality |
| **Failure** | Exception → halt | Fail-Closed → silence + continuity + human delegation |
| **Approximation** | Implicit, often hidden | Must be explicitly declared (Duty of Testimony) |
| **Safety** | Probabilistic confidence | Structural determinism (R threshold) |

---

## 6. Application Domains

### Medical AI
- δ = tumor resistance to drug delivery
- τ = pump infusion capacity
- R ≥ 1.0 → "Physically unreachable — physician judgment required"

### Autonomous Systems
- δ = time-to-collision margin
- τ = braking capability
- R ≥ 1.0 → "Collision structural risk — emergency stop"

### Critical Infrastructure
- δ = load overflow
- τ = buffer capacity
- R ≥ 1.0 → "Cascade failure risk — circuit breaker"

---

## 7. Prohibitions (Structural)

The following are structurally forbidden in NRA-IDE:

- Deriving force or state from distance (violates Axiom 2)
- Inverse derivation Π⁻¹ (violates Axiom 3)
- Optimization of output (violates Axiom 4)
- System halt when Fail-Closed is triggered (violates Axiom 5)
- Discarding buffer or averaging history (violates Axiom 6)
- Using `R` as a physical length or metric distance

---

## 8. Mathematical Foundations (Alignment)

NRA-IDE is mathematically aligned with, but distinct from:

- **Viability Theory** (Aubin, 1991) — differential inclusions, viability kernels
- **Thermodynamic irreversibility** — entropy as the basis of causal direction
- **Hysteresis control** — threshold bands, not point thresholds (Axiom 5 implementation)

NRA-IDE does not extend these theories. It derives independently from structural axioms
and finds alignment as a consequence.

---

## 9. Citation

```
M-Tokuni (2026). NRA-IDE: Nomological Ring Axioms — Intensional Dynamics Engine.
GitHub. https://github.com/M-Tokun/NRA-IDE
```

**Author:** M-Tokuni (とおくに)
**License:** See LICENSE.txt
**Principle verification:** L∧P∧C∧D (Logic ∧ Physics ∧ Causality ∧ Determinism)
