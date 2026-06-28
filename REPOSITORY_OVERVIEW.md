# NRA-IDE — Repository Overview

Quick navigation map. Start here if you are new to this repository.

---

## Quick Start (Recommended Read Order)

1. [README.md](./README.md) — Project thesis and core axiom (R = δ/τ)
2. **This file** — Repository map and quick pointers
3. [universal-definition/](./universal-definition/) — Safety principles and formal definitions
4. [ground/](./ground/) — IDE-side grounding and boundary-control layer
5. [src/](./src/) — Core implementation and pipelines
6. [nra-tcm-parser/](./nra-tcm-parser/) — Text crystallization and large-document processing
7. [nra-ide-cancer-treatment-support-system/](./nra-ide-cancer-treatment-support-system/) — Medical domain application
8. [examples/](./examples/) — Interactive HTML demos (50+ simulations)

---

## Directory Map

| Directory | Contents |
|---|---|
| [`.devcontainer/`](./.devcontainer/) | Dev Container / Docker sandbox configuration |
| [`.github/`](./.github/) | CI workflows and GitHub issue templates |
| [`cascade-failure-prevention/`](./cascade-failure-prevention/) | Cascade failure prevention gate modules |
| [`config/`](./config/) | Configuration files |
| [`docs/`](./docs/) | Supplementary documentation and developer guides |
| [`examples/`](./examples/) | Interactive HTML demos (50+ simulations) |
| [`gate/`](./gate/) | Gating modules — EN and JP variants |
| [`ground/`](./ground/) | IDE-side grounding and boundary-control layer; execution-use eligibility, missing-value handling, physical constraints, and threshold checks |
| [`multi-physics-safety-gate/`](./multi-physics-safety-gate/) | Multi-physics safety gate implementation |
| [`note/`](./note/) | Development notes and architecture explorations |
| [`nra-core/`](./nra-core/) | Core NRA engine |
| [`nra-ide-cancer-treatment-support-system/`](./nra-ide-cancer-treatment-support-system/) | Medical domain application (cancer treatment support) |
| [`nra-tcm-parser/`](./nra-tcm-parser/) | TCM / long-document parser and crystallization tools |
| [`scripts/`](./scripts/) | Utility and automation scripts |
| [`src/`](./src/) | Primary pipeline scripts and gate modules |
| [`theory/`](./theory/) | Core axioms, foundational thesis, ethics |
| [`tools/`](./tools/) | Standalone tools and visualizers |
| [`universal-definition/`](./universal-definition/) | Formal definitions, quick reference, safety checklist |

---

## Key Root Files

| File | Description |
|---|---|
| [README.md](./README.md) | Project overview — English |
| [README_JP.md](./README_JP.md) | Project overview — Japanese |
| [FORMULA.md](./FORMULA.md) | Core equations — R = δ/τ and Dual-Fluctuation Formula |
| [REPOSITORY_OVERVIEW.md](./REPOSITORY_OVERVIEW.md) | This file — repository navigation map |
| [AGENTS.md](./AGENTS.md) | AI agent operational guide |
| [CLAUDE.md](./CLAUDE.md) | Claude Code workspace constraints and naming conventions |
| [CLINE.md](./CLINE.md) | Cline Consultant & Architect operational guide |
| [GEMINI.md](./GEMINI.md) | Gemini workspace guide |
| [llms.md](./llms.md) | LLM reasoning gate and structural axioms |
| [llms.txt](./llms.txt) | Plain-text summary for LLM context injection |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines |
| [CITATION.cff](./CITATION.cff) | Citation metadata for formal attribution |
| [LICENSE](./LICENSE) | MIT License |

---

## Key Concepts

| Term | Definition |
|---|---|
| `R = δ/τ` | Structural Ratio — deviation relative to constraint boundary |
| `δ` (delta) | Deviation from structural constraint |
| `τ` (tau) | Tolerance boundary (thickness of tension) — **not** a time constant |
| R ≥ 1.0 | Structure at limit — output must stop (Fail-Closed) |
| Integer Phase Lock | Each state transition is structurally complete; no residual carries forward |
| Silence Principle | When structurally impossible, return silence — never generate alternatives |
| Grounding Boundary Policy | IDE-side execution gate for observed facts, source lineage, missing values, physical constraints, and threshold checks |

---

## Architecture Overview

```
Pre-NRA  (input gate / filter)
    ↓
LLM      (generation device)
    ↓
Post-NRA (validator / CleanContext)
```

- **Fail-Closed**: Outputs violating structural constraints are silenced and discarded — never reintroduced into LLM context.
- **No distance**: State transitions are described without causal distance assumptions.

---

## src/ Implementation Highlights

| Script Pattern | Role |
|---|---|
| `nra_pre_rna_*.py` | Full integrated pipeline (Pre-NRA + LLM + Post-NRA) |
| `nra_llm_pipeline_*.py` | LLM bridge with Post-NRA validation |
| `nra_document_structure_*.py` | Post-NRA document structure engine |
| `structure_gate_bilingual_*.py` | Bilingual gate handling |
| `structure_gate_survival_base_*.py` | Survival / robustness gate logic |
| `BioDynamic_IDE_Engine_*.py` | Experimental biodynamic engine variant |

EN and JP variants exist for primary pipeline scripts. See [src/README.md](./src/README.md) for usage and configuration variables.
