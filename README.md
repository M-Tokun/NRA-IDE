<!-- FILE: README_20260711_0348.md -->
<!-- TARGET: /README.md -->
<!-- UPDATED: 2026-07-15 JST -->

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
   Canonical definition of the sole axiom, variables, IDE formula classification, boundary states, irreversible transition, and structural testimony

2. [`theory/axioms.json`](./theory/axioms.json)  
   Machine-readable synchronized representation of the sole canonical axiom and subordinate definitions

3. [`theory/NRA-IDE_Foundational_Thesis_Bilingual.md`](./theory/NRA-IDE_Foundational_Thesis_Bilingual.md)  
   Foundational thesis in bilingual English and Japanese form

4. [`theory/SANDWICH_ARCH.md`](./theory/SANDWICH_ARCH.md)  
   Logical separation specification for systems that include an LLM as an Effect-Side generative component

5. [`theory/THEORY.md`](./theory/THEORY.md)  
   Theory text integrating the sole axiom, structural principles, IDE formulas, and canonical boundary states

6. [`FORMULA.md`](./FORMULA.md)  
   Canonical specifications for formulas, variables, domains, initial conditions, numerical conditions, and complementary computation

7. [`llms.md`](./llms.md)  
   AI-oriented identification, interpretation, and operational gate

8. Domain-specific rules

9. Normative reference implementation that passes canonical conformance tests

10. Other implementation code

11. Comments, examples, and AI-generated explanations

Lower-level documents, code, comments, and examples must not alter or override definitions in higher-level canonical documents.

For the full repository layout, see [`REPOSITORY_OVERVIEW.md`](./REPOSITORY_OVERVIEW.md).

---

## Quick Verification

The normative reference implementation source is:

- [`nra-core/foundations/NRA-IDE_Architecture_public.py`](./nra-core/foundations/NRA-IDE_Architecture_public.py)

Its canonical conformance tests are:

- [`tests/test_nra_ide_reference.py`](./tests/test_nra_ide_reference.py)

From the repository root, run:

```powershell
python -m unittest discover -v
```

The expected result is `Ran 38 tests` followed by `OK`.

The [NRA-IDE Watchdog workflow](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml) runs these tests on pushes and pull requests and reports line and branch coverage in the GitHub Actions log.

Other code, visualizations, papers, and quantum extensions under `nra-core/` remain research, explanatory, illustrative, or historical unless a canonical record explicitly promotes them.

---

## Sole Nomological Ring Axiom

> **Existence is Generation.**  
> **存在は生成である。**

This is the one and only Nomological Ring Axiom. No second or subsequent axiom exists. “Nomological Ring Axioms” remains the proper name abbreviated as NRA; it does not authorize adding further axioms.

Existence is not treated as a fixed static entity. It appears as continuous generation carrying accumulated history.

Rest is only a temporary slice of an ongoing generative process. It does not mean absolute stoppage within the structure.

Therefore, Fail-Closed or the stopping of autonomous action must not be interpreted as the disappearance of the structure or the cessation of observation.

---

## IDE Primary Formula — Basic Boundary Formula

The Primary Formula is the first canonical IDE calculation system. It is not a first axiom.

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

The two remaining margins are distinct:

$$
M_R=1-R
$$

$$
M_{\tau}=\tau-\delta
$$

$M_R$ is the dimensionless remaining ratio margin. $M_{\tau}$ is the remaining absorption margin and has the same unit as $\delta$ and $\tau$.

---

## Canonical Boundary Order

The canonical NRA-IDE boundary order is fixed as follows:

$$
0\le R_{\mathrm{warn}}
<
R_{\mathrm{handoff}}
<
R_{\mathrm{irrev}}
<
1.0
$$

| Boundary | Canonical name | Role |
|---|---|---|
| $R_{\mathrm{warn}}$ | Boundary-Approach Warning Point | Disclose that the structure is approaching a boundary |
| $R_{\mathrm{handoff}}$ | Pre-Boundary Human-Handoff Point | Transfer execution authority only to the predefined external authority, stop new autonomous judgment and operation, and keep testimony and audit routes active |
| $R_{\mathrm{irrev}}$ | Irreversible-Transition Onset Threshold | Do not assume that the former structural state remains recoverable |
| $R=1.0$ | Invariant Complete-Rupture Boundary | Stop ordinary generation and switch the declared target to post-rupture fixed testimony |

Human handoff, irreversible-transition onset, and complete rupture are not the same event.

$$
R_{\mathrm{handoff}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

Concrete threshold values are defined for each target domain, but this order and these roles must not be changed.

`R_handoff` is the canonical name. `R_op`, `Rop`, and `rop` are backward-compatibility aliases that normalize to the same threshold only; they do not define another boundary or state.

---

## Canonical State Classification

| State | Condition | Required basic behavior |
|---|---|---|
| `PERMIT` | $0\le R<R_{\mathrm{warn}}$ | Permit constrained autonomous operation and continue structural audit |
| `BOUNDARY_WARNING` | $R_{\mathrm{warn}}\le R<R_{\mathrm{handoff}}$ | Disclose boundary approach, both remaining margins, trend, double-fluctuation status, and missing information |
| `HANDOFF_REQUIRED` | $R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}$ | Transfer execution authority only, stop new autonomous judgment and operation, and keep structural testimony and audit logging active |
| `IRREVERSIBLE_TRANSITION` | $R_{\mathrm{irrev}}\le R<1.0$ | Set the irreversible latch and prohibit normalization, recovery assumptions, and optimization proposals |
| `RUPTURE_BOUNDARY` | $R_{\mathrm{target}}\ge1.0$ | Stop ordinary generation and autonomous action, and switch to post-rupture fixed testimony through surviving channels |
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

$\tau=0$ → `OUT_OF_DESCRIPTION_DOMAIN`

It must not be converted to $R=\infty$ or treated as a valid complete-rupture calculation.

`OUT_OF_DESCRIPTION_DOMAIN` is distinct from a rupture computation. Because canonical $R$ is unavailable, its affected evaluation is subject to the Fail-Closed operational principle.

By contrast, $\tau<0$, $\delta<0$, NaN, Infinity, unknown source, unknown unit, unknown observation time, unknown target, or unknown rule are treated as invalid or unknown structural inputs and therefore fall under `CONFESSION`.

---

## Fail-Closed Operational Principle

Fail-Closed suppresses affected new autonomous judgment and operation for:

- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`
- `OUT_OF_DESCRIPTION_DOMAIN`

It does not suppress required fixed structural testimony or logging. `PERMIT` is not Fail-Closed. `BOUNDARY_WARNING` alone does not require complete output suppression unless a pre-fixed domain rule requires it.

Handoff changes `execution_authority` only. It does not implicitly transfer responsibility, legal or outcome responsibility, testimony routing, audit-log routing, audit-log custody, knowledge, or any guarantee of correctness, recovery, or resolution.

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
- remaining ratio margin $M_R$
- remaining absorption margin $M_{\tau}$
- trend
- dominant side
- missing information
- double-fluctuation result, or `NOT_OBSERVABLE` with the missing reason
- boundary warning
- human-handoff notice
- irreversible-transition notice
- structural-disclosure log

$$
R_{\mathrm{target}}\ge1.0
\Rightarrow
\text{switch to post-rupture fixed testimony}
$$

Post-rupture fixed testimony is a repeatable predefined format, not a one-time terminal message. It is limited to fields such as latest valid Cause-Side observations and timestamps, latest valid $\delta$, $\tau$, and $R$, complete-rupture notice, irreversible-latch state, audit trail, and human-handoff notice.

Target rupture does not imply sensor, logger, communication-path, or external-audit rupture. Surviving Cause-Side observation, logging, and communication channels continue until each becomes physically unavailable.

```text
target_state = RUPTURE_BOUNDARY
observation_state = ACTIVE
logging_state = ACTIVE
communication_state = ACTIVE
testimony_mode = POST_RUPTURE_FIXED
```

This is a valid combined state.

> **Autonomous action stops. Structural testimony does not disappear.**

---

## Cause-Side / Effect-Side Separation

Only the following may determine $\delta$, $\tau$, and $R$:

1. direct Cause-Side observations
2. Cause-Side transformation rules fixed before evaluation

Cause-Side inputs must preserve traceability of source, target, unit, observation time, transformation rule, rule version, and update authority.

Cause-Side is not frozen across time. Authorized new observations may form the next evaluation snapshot. For each evaluation, its update authority, route, provenance, target, unit, observation time, transformation rule, threshold rule, and snapshot are fixed.

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

Observation loss is independent of target rupture. Missing sensor data is not converted to zero, stability, safety, recovery, or rupture. Implementations preserve last-valid observation metadata and do not stop surviving sensors because another sensor is lost.

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
canonical-state-controlled Effect-Side output
```

Ordinary explanation is permitted only in states and fields allowed by the pre-fixed canonical behavior. Fixed Handoff or post-rupture testimony is not supplemented by newly generated free-form explanation.

The boundary evaluator decides. The output gate enforces.

```text
Boundary Evaluator
→ decides

Output Gate
→ enforces
```

Even when LLM explanation is omitted or stopped, structural testimony is preserved through an independent Cause-Side audit path.

---

## IDE Formula Classification

### Primary Formula

$$
R=\frac{\delta}{\tau}
$$

This is the first canonical IDE calculation system, not an axiom.

### Secondary Formula

The Secondary / Dual-Fluctuation Formula is the second canonical IDE calculation system, not a second axiom. Its canonical core covers upper-side and lower-side accumulated deviation, side-specific boundary-approach ratios, and simultaneous deviation increase with absorption-thickness decrease.

Pre-fixed EMA rules, initial conditions, and side-specific shape transformations are auxiliary realizations of this calculation system. They are not independent canonical formulas or axioms.

“Secondary Formula” indicates its definitional order and role within NRA-IDE. It does not mean a quadratic equation.

Changes in side-specific effective gate widths do not mean that the underlying true absorption thickness $\tau$ has spontaneously recovered or increased.

### Complementary Formula

The complementary formula is a computational layer used to support EMA lag compensation, local rapid change, numerical integration, and domain-specific precision requirements.

It is neither an axiom nor a third canonical IDE calculation system, and it does not replace either the Primary Formula or the Secondary Formula.

For equations, variables, initial conditions, and numerical conditions, see [`FORMULA.md`](./FORMULA.md).

---

## Numerical Computation and Residuals

Integer Phase Lock in NRA-IDE is a design principle for preventing rounding error or residuals from being carried into the next state without audit.

It does not mean:

```text
all physical error is absent
```

Known numeric structural progression, rounding, approximation, and discarded residuals are recorded in `STRUCTURAL_DISCLOSURE_LOG` when their values and provenance are established.

Known approximation is not automatically `CONFESSION`. `CONFESSION` is limited to structural information that is unknown, invalid, ambiguous, non-finite, or unsupported.

`CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` are recorded separately in `INPUT_EXCEPTION_LOG`. They are not inserted into `STRUCTURAL_DISCLOSURE_LOG` as known numeric progression.

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

It is not a place for adding a second or subsequent axiom and must follow the higher-level canonical documents.

Operational rules and implementation rules must not alter the sole axiom, variable definitions, IDE formula classification, canonical boundary order, or structural-testimony rules.

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

0 <= R_warn < R_handoff < R_irrev < 1.0

M_R   = 1 - R
M_tau = tau - delta

tau = 0
→ OUT_OF_DESCRIPTION_DOMAIN
→ R is undefined
→ affected evaluation is Fail-Closed

Fail-Closed applies to
→ HANDOFF_REQUIRED
→ IRREVERSIBLE_TRANSITION
→ RUPTURE_BOUNDARY
→ CONFESSION
→ OUT_OF_DESCRIPTION_DOMAIN

BOUNDARY_WARNING alone
→ does not require full suppression without a pre-fixed domain rule

R < 1.0
→ structural testimony continues

R_target >= 1.0
→ target reaches RUPTURE_BOUNDARY
→ switch to continuing POST_RUPTURE_FIXED testimony
→ surviving observation, logging, and communication channels continue

Cause-Side
→ may determine delta, tau, R

Effect-Side
→ must not update delta, tau, R

Known boundary progression
→ structural disclosure

Unknown, invalid, ambiguous, non-finite, or unsupported information
→ CONFESSION
→ input exception log
```
