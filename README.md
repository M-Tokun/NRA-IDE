<!-- FILE: README_20260711_0348.md -->
<!-- TARGET: /README.md -->
<!-- UPDATED: 2026-07-11 03:48 JST -->

# NRA-IDE: Nomological Ring Axioms — Intensional Dynamics Engine

### 律環公理 — 内包性動力学エンジン

[![CI](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml/badge.svg)](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19420853.svg)](https://doi.org/10.5281/zenodo.19420853)

<p align="center">
  <img src="./docs/NRA-IDE_git.jpg" width="700" alt="NRA-IDE LOGO">
</p>

---

## What Is NRA-IDE?

NRA-IDE is a structural evaluation framework that describes the present approach to structural boundaries through the relation between accumulated deviation and the thickness available to absorb it.

Its central question is not probabilistic prediction of the future.

> **What canonical boundary state is the target structure in now?**

NRA-IDE does not collapse boundary warning, human handoff, irreversible-transition onset, and complete rupture into a single state. It treats them as distinct structural events.

Even when autonomous judgment or autonomous action is stopped, Cause-Side observation and structural testimony are not erased.

---

## Canonical Reference Order

NRA-IDE definitions must be read in the following order.

1. [`theory/AXIOMS.md`](./theory/AXIOMS.md)  
   Canonical definitions of the highest-level axioms, variables, boundary states, irreversible transition, and structural testimony

2. [`theory/axioms.json`](./theory/axioms.json)  
   Machine-readable canonical axiom definitions

3. [`theory/NRA-IDE_Foundational_Thesis_Bilingual.md`](./theory/NRA-IDE_Foundational_Thesis_Bilingual.md)  
   Foundational thesis in bilingual English and Japanese form

4. [`theory/SANDWICH_ARCH.md`](./theory/SANDWICH_ARCH.md)  
   Logical separation specification for systems that include an LLM as an Effect-Side generative component

5. [`theory/THEORY.md`](./theory/THEORY.md)  
   Theory text integrating the axioms, formulas, and canonical boundary states

6. [`FORMULA.md`](./FORMULA.md)  
   Canonical specifications for formulas, variables, domains, initial conditions, numerical conditions, and complementary computation

7. [`llms.md`](./llms.md)  
   AI-oriented identification, interpretation, and operational gate

Lower-level documents, code, comments, and examples must not alter or override definitions in higher-level canonical documents.

For the full repository layout, see [`REPOSITORY_OVERVIEW.md`](./REPOSITORY_OVERVIEW.md).

---

## Core Axiom

> **Existence is Generation.**  
> **存在は生成である。**

Existence is not treated as a fixed static entity. It appears as continuous generation carrying accumulated history.

Rest is only a temporary slice of an ongoing generative process. It does not mean absolute stoppage within the structure.

Therefore, Fail-Closed or the stopping of autonomous action must not be interpreted as the disappearance of the structure or the cessation of observation.

---

## Primary Boundary Formula

The primary formula of NRA-IDE is:

$$
R=\frac{\delta}{\tau}
$$

| Symbol | Canonical name | Meaning |
|---|---|---|
| $\delta$ | Accumulated Deviation | Deviation accumulated within the structure while carrying Cause-Side history |
| $\tau$ | Absorption Thickness | The thickness through which the structure can absorb accumulated deviation |
| $R$ | Boundary-Approach Ratio | The ratio indicating how close the structure is to the complete-rupture boundary |

The symbol $R$ is reserved exclusively for the boundary-approach ratio.

It must not be reused as a safety score, quality score, confidence score, semantic-retention score, or LLM-output evaluation value.

The valid description domain is:

$$
\tau>0,\qquad \delta\ge0
$$

$$
\delta,\tau\in\mathbb{R}_{finite}
$$

---

## Canonical Boundary Order

The canonical NRA-IDE boundary order is fixed as follows:

$$
0\le R_{\mathrm{warn}}
<
R_{\mathrm{op}}
<
R_{\mathrm{irrev}}
<
1.0
$$

| Boundary | Canonical name | Role |
|---|---|---|
| $R_{\mathrm{warn}}$ | Boundary-Approach Warning Point | Disclose that the structure is approaching a boundary |
| $R_{\mathrm{op}}$ | Pre-Boundary Human-Handoff Point | Stop new autonomous judgment and autonomous operation, and hand off to a qualified human |
| $R_{\mathrm{irrev}}$ | Irreversible-Transition Onset Threshold | Do not assume that the former structural state remains recoverable |
| $R=1.0$ | Invariant Complete-Rupture Boundary | Stop ordinary generation and switch to final fixed testimony |

Human handoff, irreversible-transition onset, and complete rupture are not the same event.

$$
R_{\mathrm{op}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

Concrete threshold values are defined for each target domain, but this order and these roles must not be changed.

---

## Canonical State Classification

| State | Condition | Required basic behavior |
|---|---|---|
| `PERMIT` | $0\le R<R_{\mathrm{warn}}$ | Permit constrained autonomous operation and continue structural audit |
| `BOUNDARY_WARNING` | $R_{\mathrm{warn}}\le R<R_{\mathrm{op}}$ | Disclose boundary approach, remaining margin, trend, and missing information |
| `HANDOFF_REQUIRED` | $R_{\mathrm{op}}\le R<R_{\mathrm{irrev}}$ | Stop new autonomous judgment and new autonomous operation, and hand off to a qualified human |
| `IRREVERSIBLE_TRANSITION` | $R_{\mathrm{irrev}}\le R<1.0$ | Set the irreversible latch and prohibit normalization, recovery assumptions, and optimization proposals |
| `RUPTURE_BOUNDARY` | $R\ge1.0$ | Stop ordinary generation and autonomous action, and switch to final fixed testimony |
| `CONFESSION` | Required structural information is unknown, invalid, ambiguous, non-finite, or unsupported | Explicitly disclose the unresolved element, do not complete it by analogy, and stop the affected evaluation |
| `OUT_OF_DESCRIPTION_DOMAIN` | $\tau=0$ | Declare $R$ undefined and require a change of description system |

---

## Irreversible Transition

Irreversible transition begins before complete rupture.

$$
R_{\mathrm{irrev}}\le R<1.0
$$

Within this interval:

```text
irreversible_latched = true
```

Once latched, a temporary decrease in $R$ is not sufficient to return the system to the ordinary state.

Re-entry requires domain-specific reevaluation, structural reinspection, or definition of a new target system.

---

## Treatment of $\tau=0$

When $\tau=0$, the primary boundary formula does not hold.

$$
\tau=0
\Rightarrow
R\text{ is undefined}
$$

$$
\tau=0
\Rightarrow
\text{OUT}\_\text{OF}\_\text{DESCRIPTION}\_\text{DOMAIN}
$$

This is not Fail-Closed.

It must not be converted to $R=\infty$ or treated as a valid complete-rupture calculation.

By contrast, $\tau<0$, $\delta<0$, NaN, Infinity, unknown source, unknown unit, unknown observation time, unknown target, or unknown rule are treated as invalid or unknown structural inputs and therefore fall under `CONFESSION`.

---

## Structural Testimony

NRA-IDE does not become completely silent merely because risk is high.

$$
R<1.0
\Rightarrow
\text{structural testimony continues}
$$

Structural testimony may include:

- Cause-Side observations
- current $\delta$, $\tau$, and $R$
- current boundary state
- remaining absorption margin
- trend
- dominant side
- missing information
- boundary warning
- human-handoff notice
- irreversible-transition notice
- audit log

$$
R\ge1.0
\Rightarrow
\text{switch to final fixed testimony}
$$

Final fixed testimony is limited to predefined items such as the final Cause-Side observations, final $\delta$, final $\tau$, final $R$, complete-rupture notice, irreversible-latch state, audit trail, and human-handoff notice.

> **Autonomous action stops. Structural testimony does not disappear.**

---

## Cause-Side / Effect-Side Separation

Only the following may determine $\delta$, $\tau$, and $R$:

1. direct Cause-Side observations
2. Cause-Side transformation rules fixed before evaluation

Cause-Side inputs must preserve traceability of source, target, unit, observation time, transformation rule, rule version, and update authority.

The following remain Effect-Side:

- LLM output
- LLM self-evaluation
- semantic scores
- output rankings
- selected outputs
- discarded outputs
- prior generated text

These artifacts may be audited, but they must not update $\delta$, $\tau$, or $R$.

$$
\text{Effect-Side}
\not\rightarrow
(\delta,\tau,R)\text{ update}
$$

Even an LLM output that has been validated, selected, or passed through an output gate remains Effect-Side.

---

## Configurations That Include an LLM

In NRA-IDE, IDE does not mean Integrated Development Environment.

It means **Intensional Dynamics Engine**.

In implementations that include an LLM, the LLM is not treated as a trusted structural evaluator.

[`theory/SANDWICH_ARCH.md`](./theory/SANDWICH_ARCH.md) separates the following functions:

```text
Cause-Side observation
        ↓
NRA-IDE boundary evaluator
        ↓
input gate
        ↓
LLM CORE
        ↓
output gate
        ↓
structural testimony + permitted explanation
```

The boundary evaluator decides. The output gate enforces.

```text
Boundary Evaluator
→ decides

Output Gate
→ enforces
```

Even when LLM explanation is omitted or stopped, structural testimony is preserved through an independent Cause-Side audit path.

---

## Primary, Secondary, and Complementary Formulas

### Primary Formula

$$
R=\frac{\delta}{\tau}
$$

This is the basic boundary formula of NRA-IDE.

### Secondary Formula

To track asymmetric upper-side and lower-side variation that a static $\tau$ may not adequately capture, the Secondary Formula uses pre-fixed EMA rules and side-specific effective gate widths.

“Secondary Formula” indicates its definitional order and role within NRA-IDE. It does not mean a quadratic equation.

Changes in side-specific effective gate widths do not mean that the underlying true absorption thickness $\tau$ has spontaneously recovered or increased.

### Complementary Formula

The complementary formula is a computational layer used to support EMA lag compensation, local rapid change, numerical integration, and domain-specific precision requirements.

It is not a third axiom formula and does not replace either the Primary Formula or the Secondary Formula.

For equations, variables, initial conditions, and numerical conditions, see [`FORMULA.md`](./FORMULA.md).

---

## Numerical Computation and Residuals

Integer Phase Lock in NRA-IDE is a design principle for preventing rounding error or residuals from being carried into the next state without audit.

It does not mean:

```text
all physical error is absent
```

Known rounding, approximation, and discarded residuals are recorded in a traceable structural disclosure log.

Known approximation is not automatically `CONFESSION`. `CONFESSION` is limited to structural information that is unknown, invalid, ambiguous, non-finite, or unsupported.

---

## Time and Distance

NRA-IDE does not treat time as an unconditional independent causal variable.

Time appears as the ordering of state transitions carrying accumulated history.

Distance is likewise not treated as an unconditional causal driver.

However, when distance, position, direction, or spatial relation is physically valid as an observation, it is retained as Cause-Side data rather than deleted, and its causal role is stated explicitly.

```text
Distance is not automatically a cause
≠
Distance information must be deleted
```

---

## Structural Evaluation and Non-Evaluative Actions

Structural evaluation means calculating, classifying, or acting on $\delta$, $\tau$, $R$, or canonical boundary states.

The following are not, by themselves, structural evaluation:

- document viewing
- indexing
- citation
- link navigation
- file discovery
- metadata extraction
- explanation of repository structure

However, if such actions calculate, classify, or update structural variables, they become subject to the canonical rules.

---

## Comparative Explanations

Comparison with PID control, signal processing, statistics, machine learning, or existing continuous dynamics is not prohibited.

However, concepts from another theory must not replace the canonical definitions of NRA-IDE.

In particular, the following interpretations are prohibited:

- redefining $\tau$ as a time constant
- redefining $R$ as a safety score or confidence score
- generating $\delta$ from LLM-output evaluation
- treating irreversible-transition onset and complete rupture as the same event

---

## Implementations and Demos

For implementations, examples, and interactive HTML demos, see:

- [`src/`](./src/) — source code
- [`nra-core/`](./nra-core/) — core implementation
- [`gate/`](./gate/) — gate implementations
- [`examples/`](./examples/) — usage examples and visualization demos
- [`examples/README_JP.md`](./examples/README_JP.md) — Japanese demo index
- [`REPOSITORY_OVERVIEW.md`](./REPOSITORY_OVERVIEW.md) — full repository map

Demos visualize NRA-IDE behavior under predefined targets, variables, thresholds, and transformation rules.

A numerical coincidence or threshold used in an individual demo must not be generalized as a physical law common to all domains.

---

## Grounding and Operational Layer

[`ground/`](./ground/) is the grounding and operational layer for observed facts, sources, physical constraints, missing values, thresholds, and execution-use eligibility.

It is not a place for adding new axioms and must follow the higher-level canonical documents.

Operational rules and implementation rules must not alter the axioms, variable definitions, canonical boundary order, or structural-testimony rules.

---

## Ethics and Use Boundaries

For the ethics policy, see [`theory/ETHICS.md`](./theory/ETHICS.md).

In high-risk domains, NRA-IDE does not replace qualified human responsibility.

Its role is to disclose structural state from Cause-Side observations and to distinguish warning, human handoff, irreversible transition, and complete rupture according to the canonical boundary order.

---

## Japanese Version

For the Japanese source version, see [`README_JP.md`](./README_JP.md).

The Japanese version is the primary source text for this README. This English version is intended to preserve its meaning, logical relations, and boundary conditions as closely as possible.

---

## Citation and License

- Formal citation metadata: [`CITATION.cff`](./CITATION.cff)
- License: [`LICENSE`](./LICENSE)
- DOI: `10.5281/zenodo.19420853`

---

## Canonical Summary

```text
NRA = Nomological Ring Axioms
IDE = Intensional Dynamics Engine

R = delta / tau

delta = accumulated deviation
tau   = absorption thickness
R     = boundary-approach ratio

0 <= R_warn < R_op < R_irrev < 1.0

tau = 0
→ OUT_OF_DESCRIPTION_DOMAIN
→ R is undefined
→ not FAIL_CLOSED

R < 1.0
→ structural testimony continues

R >= 1.0
→ switch to final fixed testimony

Cause-Side
→ may determine delta, tau, R

Effect-Side
→ must not update delta, tau, R

Known boundary progression
→ structural disclosure

Unknown, invalid, ambiguous, non-finite, or unsupported information
→ CONFESSION
```
