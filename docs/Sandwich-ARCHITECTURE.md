# NRA-IDE Architecture Overview

Purpose
- Provide a concise architecture summary and diagram placeholders for NRA-IDE (system boundaries, main subsystems, data flow).

High-level Architecture
- Three-layer "Sandwich" (Pre-RNA → LLM → Post-RNA)
  - Pre-RNA (Input Gate): sanitize/convert inputs, detect Pi-1 patterns (P1-P4), convert or block when needed.
  - LLM (Generation Device): language generation only; isolated from safety logic.
  - Post-RNA (Output Gate / CleanContext): validate outputs via R = δ/τ, enforce Fail-Closed, and log results.

Major components
- Input Gate (gate/ and structure_gate_*.py)
  - Pattern detectors (P1-P4), converters, warnings, and block actions.
- LLM Bridge (src/nra_llm_pipeline_*.py)
  - Provider abstraction (MOCK / ANTHROPIC / OPENAI / GOOGLE), system prompts, turn handling.
- Document Engine (src/nra_document_structure_*.py)
  - GenesisBlock (axioms), SectionNodes, validation pipeline, integrity scoring.
- Full Pipeline (src/nra_pre_rna_*.py)
  - Composition of Pre-RNA + LLM + Post-RNA for integrated operation.
- DiscardVault / CleanContext
  - Storage for FAIL-CLOSED outputs; guarantees they never re-enter LLM history.

Data flow (ASCII)

User -> Pre-RNA(Input Gate) -> LLM -> Post-RNA(Validator) -> User
                                 |                        |
                                 v                        v
                              (raw output)           (PASS / FAIL-CLOSED)

Security & Safety properties
- Fail-Closed: R >= R_op => output sealed and omitted from LLM history.
- No Exploration: system must not initiate boundary-crossing search or suggest external tools.
- Human-in-the-loop: AI presents facts; humans make final decisions; all changes logged.

Diagram placeholders
- docs/figures/NRA-IDE_architecture.svg (TODO)
- docs/figures/NRA-IDE_architecture.png (TODO)

Operational notes
- Running MOCK pipeline: see src README for quick commands.
- Configuration: domain τ and R_op are domain-specific; change only by human operators and log adjustments.

Next steps (recommended)
- Generate architecture diagram (SVG) and place in docs/figures/.
- Add CONTRIBUTING.md describing how to run MOCK pipeline, tests, and commit policy.

