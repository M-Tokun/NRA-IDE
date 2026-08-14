# NRA-IDE — Repository Overview

Quick navigation and authority map. Start here if you are new to this repository.

> [!IMPORTANT]
> A directory name such as `core`, `src`, `official`, or `final` does not by itself make an artifact canonical, current, normative, validated, safe, or suitable for operational use. Follow the canonical reference order and the explicit authority classification below.

---

## Canonical Read Order

When definitions conflict, use this order:

1. [`theory/AXIOMS.md`](./theory/AXIOMS.md) — sole axiom and highest-precedence canonical definitions
2. [`theory/axioms.json`](./theory/axioms.json) — machine-readable synchronized canonical representation
3. [`theory/NRA-IDE_Foundational_Thesis_Bilingual.md`](./theory/NRA-IDE_Foundational_Thesis_Bilingual.md) — bilingual foundational thesis
4. [`theory/SANDWICH_ARCH.md`](./theory/SANDWICH_ARCH.md) — Cause-Side / Effect-Side separation specification
5. [`theory/HORIZONTAL_AXIS.md`](./theory/HORIZONTAL_AXIS.md) — External Horizontal Axis practice specification (evidence inheritance and multi-agent isolation)
6. [`theory/THEORY.md`](./theory/THEORY.md) — integrated theory text
7. [`FORMULA.md`](./FORMULA.md) — mathematical and computational definitions
8. [`llms.md`](./llms.md) — AI interpretation and operational gate
9. Domain-specific rules
10. Normative reference implementation that passes canonical conformance tests
11. Other implementation code
12. Comments, examples, and AI-generated explanations

Lower-precedence material must not redefine higher-precedence terms.

For an introductory explanation, read [`README.md`](./README.md) or [`README_JP.md`](./README_JP.md).

---

## Current Authority Classification

- Sole Nomological Ring Axiom: “Existence is Generation.” / 「存在は生成である。」
- No second or subsequent axiom exists.
- Primary and Secondary / Dual-Fluctuation Formulas: the two canonical IDE calculation systems, not axioms
- Other equations: derived, auxiliary, or complementary formulas
- Normative reference implementation source: [`nra-core/foundations/NRA-IDE_Architecture_public.py`](./nra-core/foundations/NRA-IDE_Architecture_public.py)
- Generated docs mirror: [`docs/NRA-IDE_Architecture_public.py`](./docs/NRA-IDE_Architecture_public.py)
- Conformance tests: [`tests/test_nra_ide_reference.py`](./tests/test_nra_ide_reference.py)
- Other code, papers, demos, visualizations, and dated definitions: research, explanatory, illustrative, domain-specific, or historical unless a higher-precedence canonical record explicitly promotes them

The normative source and docs mirror must have identical SHA-256 values. Location alone does not confer conformance; the reference tests must pass.

---

## Directory Map

| Directory | Contents and authority |
|---|---|
| [`.devcontainer/`](./.devcontainer/) | Dev Container and sandbox configuration |
| [`.github/`](./.github/) | CI workflows and GitHub templates |
| [`cascade-failure-prevention/`](./cascade-failure-prevention/) | Domain or experimental gate modules; not canonical by location |
| [`config/`](./config/) | Configuration files; domain values do not redefine canonical order |
| [`docs/`](./docs/) | Public documentation, generated mirrors, and explanatory assets |
| [`examples/`](./examples/) | Illustrative demos under predefined assumptions; not measuring instruments or safety proofs |
| [`gate/`](./gate/) | Gate implementations and historical variants; conformance must be established separately |
| [`ground/`](./ground/) | Grounding and operational rules for facts, provenance, missing values, physical constraints, and thresholds |
| [`multi-physics-safety-gate/`](./multi-physics-safety-gate/) | Domain implementation; name does not guarantee safety or canonical conformance |
| [`note/`](./note/) | Development history, conversations, and architecture exploration; non-canonical unless explicitly promoted |
| [`nra-core/`](./nra-core/) | Research history, papers, examples, visualizations, extensions, and the explicitly identified normative reference source |
| [`nra-ide-cancer-treatment-support-system/`](./nra-ide-cancer-treatment-support-system/) | High-risk domain research/application material; not a substitute for qualified clinical judgment and not validated by location |
| [`nra-tcm-parser/`](./nra-tcm-parser/) | Text-processing and long-document tools; not a structural measurement authority |
| [`scripts/`](./scripts/) | Utility and automation scripts |
| [`src/`](./src/) | Implementation and pipeline variants; non-normative unless explicitly promoted and tested |
| [`tests/`](./tests/) | Conformance and regression tests |
| [`theory/`](./theory/) | Canonical and high-precedence theory documents; internal precedence still follows the order above |
| [`tools/`](./tools/) | Standalone tools and visualizers; non-normative by default |
| [`universal-definition/`](./universal-definition/) | Explanatory and operational reference material subordinate to root canonical documents |

---

## Key Root Files

| File | Description |
|---|---|
| [README.md](./README.md) | Project overview — English |
| [README_JP.md](./README_JP.md) | Project overview — Japanese |
| [FORMULA.md](./FORMULA.md) | IDE formula classification, equations, domains, and numerical conditions |
| [REPOSITORY_OVERVIEW.md](./REPOSITORY_OVERVIEW.md) | This repository navigation and authority map |
| [AGENTS.md](./AGENTS.md) | Shared AI-agent operating contract |
| [RULES_DETAIL.md](./RULES_DETAIL.md) | Detailed execution procedures subordinate to `AGENTS.md` |
| [CODEX.md](./CODEX.md) | Codex-specific entry and technical notes |
| [CLAUDE.md](./CLAUDE.md) | Claude-specific entry and technical notes |
| [CLINE.md](./CLINE.md) | Cline-specific entry and technical notes |
| [GEMINI.md](./GEMINI.md) | Gemini-specific entry and technical notes |
| [llms.md](./llms.md) | AI interpretation and operational gate subordinate to higher canonical documents |
| [llms.txt](./llms.txt) | Compact plain-text AI context entry |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines |
| [CITATION.cff](./CITATION.cff) | Citation metadata |
| [LICENSE](./LICENSE) | MIT License |

---

## Canonical Structural Summary

The sole axiom is:

```text
Existence is Generation.
存在は生成である。
```

The IDE Primary Formula is:

$$
R=\frac{\delta}{\tau}
$$

| Symbol | Canonical meaning |
|---|---|
| $\delta$ | accumulated deviation |
| $\tau$ | absorption thickness; not a time constant |
| $R$ | boundary-approach ratio; not a safety or confidence score |
| $M_R=1-R$ | dimensionless remaining ratio margin |
| $M_{\tau}=\tau-\delta$ | remaining absorption margin, in the same unit as $\delta$ and $\tau$ |

The canonical boundary order is:

$$
0\le R_{\mathrm{warn}}<R_{\mathrm{handoff}}<R_{\mathrm{irrev}}<1.0
$$

`R_handoff` is canonical. `R_op`, `Rop`, and `rop` are backward-compatibility aliases for the same threshold only.

The seven canonical states are:

1. `PERMIT`
2. `BOUNDARY_WARNING`
3. `HANDOFF_REQUIRED`
4. `IRREVERSIBLE_TRANSITION`
5. `RUPTURE_BOUNDARY`
6. `CONFESSION`
7. `OUT_OF_DESCRIPTION_DOMAIN`

When $\tau=0$, $R$ is undefined. Do not convert it to infinity or treat it as a valid rupture computation.

---

## Fail-Closed, Testimony, and Logs

The Fail-Closed operational principle suppresses affected new autonomous judgment and operation for:

- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`
- `OUT_OF_DESCRIPTION_DOMAIN`

It does not mean complete silence and does not suppress required fixed structural testimony or logging. `PERMIT` is not Fail-Closed. `BOUNDARY_WARNING` alone is not full suppression unless a pre-fixed domain rule requires it.

A `BOUNDARY_WARNING` must report the double-fluctuation result when observable, or `NOT_OBSERVABLE` with the missing reason.

- Known numeric structural progression → `STRUCTURAL_DISCLOSURE_LOG`
- `CONFESSION` and `OUT_OF_DESCRIPTION_DOMAIN` → `INPUT_EXCEPTION_LOG`

---

## Cause-Side / Effect-Side Architecture

```text
Cause-Side observation or pre-fixed transformation
        ↓
canonical NRA-IDE boundary evaluator
        ↓
input gate
        ↓
LLM CORE (optional Effect-Side generation device)
        ↓
output gate
        ↓
canonical-state-controlled Effect-Side output
```

Ordinary explanation is permitted only in states and fields allowed by the pre-fixed canonical behavior. Fixed Handoff or final testimony is not supplemented by newly generated free-form explanation.

Only Cause-Side observation or a Cause-Side transformation fixed before evaluation may determine $\delta$, $\tau$, or $R$. LLM output, semantic scores, selected output, discarded output, and prior generated text remain Effect-Side and must not update structural variables.

---

## Implementations and Demos

Implementation variants in [`src/`](./src/), [`gate/`](./gate/), and other directories may be useful for research or explanation, but they do not outrank the normative reference source or acquire conformance from their names.

Interactive assets in [`examples/`](./examples/), [`docs/`](./docs/), and [`nra-core/visualization/`](./nra-core/visualization/) illustrate predefined scenarios. They are not measurement devices, safety guarantees, or automatic domain decision-makers.

High-risk domain material requires independent domain validation and qualified human responsibility. NRA-IDE state classification does not itself establish medical, engineering, legal, or operational suitability.
