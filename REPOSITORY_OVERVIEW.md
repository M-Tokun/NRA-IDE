# NRA-IDE — Repository Overview

Short purpose
- High-level map of the repository: intent, main subsystems, and where to start.

Quick Start (recommended read order)
1. README.md (root) — project thesis and core axiom (R = δ/τ).
2. REPOSITORY_OVERVIEW.md — this file: quick map and pointers.
3. universal-definition/** — Quick Reference and Implementation Guide (read for safety principles).
4. src/** — core implementation and pipelines (see "Implementation points" below).
5. nra-tcm-parser/** — text crystallization tools and examples (large-document processing).
6. nra-ide-cancer-treatment-support-system/** — domain example (medical application).
7. examples/** — interactive demos and use-case samples (HTML).

Top-level layout
- .github/ : CI & issue templates
- docs/ : supplementary documentation and developer guides
- examples/ : interactive demos (HTML)
- gate/ : gating modules (JP/EN)
- nra-core, src/ : core engines and pipelines
- nra-tcm-parser/ : long-document parser utilities
- nra-ide-cancer-treatment-support-system/ : domain project
- universal-definition/ : formal definitions, quick ref, checklist
- local_reports/ : local outputs, logs (git-ignored)

Key concepts to know (Quick Reference)
- Core axiom: R = δ/τ (Structural Ratio). This is the authority for output validation.
- Fail-Closed: Any output that violates structural constraints is silenced and discarded (never reintroduced into LLM context).
- Three-layer architecture: Pre-RNA (input gate/filter) → LLM (generation device) → Post-RNA (validator / CleanContext).
- Silence principle: When structurally impossible, the system must return "structurally impossible" and remain silent (no alternatives or exploration).
- Naming & encoding rules: see CLAUDE.md (no spaces, use _EN/_JP, UTF-8 with LF line endings).

Implementation points (src/ highlights)
- Primary pipeline scripts (EN/JP variants exist):
  - nra_pre_rna_2026-02-13_0135.py / nra_pre_rna_EN_2026-02-13_0135.py — Full integrated pipeline (Pre-RNA + LLM + Post-RNA).
  - nra_llm_pipeline_2026-02-13_0135.py / nra_llm_pipeline_EN_2026-02-13_0135.py — LLM bridge and pipeline (post-RNA validation included).
  - nra_document_structure_2026-02-13_0135.py / nra_document_structure_EN_2026-02-13_0135.py — Post-RNA document structure engine (genesis/axioms, sections, validation).
- Gate / structure modules:
  - structure_gate_bilingual_2026-04-17_210655.py — bilingual gate handling.
  - structure_gate_survival_base_2026-04-18_214422.py — survival/robustness gate logic.
- Utilities and engines:
  - BioDynamic_IDE_Engine_v2_20260406_1947.py — experimental engine (biodynamic variant).
- README files in src/ provide usage examples, API patterns, and quick start commands. Review these before running pipelines.

What to inspect next (recommended)
- Read universal-definition/** (Quick Reference and Implementation Guide) for safety axioms and operational rules.
- Inspect src/*_EN*.py and corresponding README.md to understand configuration variables (domain τ, R_op) and how to run demos (MOCK provider vs real API).
- Review nra-tcm-parser README for large-document processing patterns if you need text-crystallization utilities.

What’s missing / recommended improvements
- Single repository-level quick guide (this file added).
- Add architecture diagram (docs/ARCHITECTURE.md or docs/figures/), and a CONTRIBUTING.md describing development flow and command examples.
- Consider adding small runnable examples (scripts/quickstart.sh or .ps1) that start the MOCK pipeline for new contributors.

If you want, the next steps can be:
- Generate a concise architecture diagram placeholder in docs/ and a PNG stub.
- Create CONTRIBUTING.md with recommended developer steps (branching, testing, running MOCK pipeline).
- Extract concrete configuration keys (e.g., domain τ defaults) into a central config file.

