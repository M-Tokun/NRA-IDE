# NRA-IDE: Nomological Ring Axioms / Intensional Dynamics Engine

[![License](https://img.shields.io/badge/license-Proprietary-red)](../LICENSE)

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()

[![Python](https://img.shields.io/badge/python-3.9+-green)]()

> **NRA-IDE is a causal structure safety engine.**  

> It handles no semantics, optimization, or history.  

> Its behavior is determined solely by structural invariants.

---

## 0. Purpose

NRA-IDE was designed to answer one question:

> **Can an AI truly explain — in structural terms — why it produced a given output?**

Generating a statistically plausible sentence and making a causally correct judgment are fundamentally different.  

NRA-IDE does not aim to build a "smarter AI." It implements a **safety middleware whose constraint structure cannot collapse.**

---

## 1. Design Principles (Non-Negotiable / Structural Invariants)

| Principle | Description |

|-----------|-------------|

| Non-Semantic | Semantics, emotion, and context are not used in causal judgment |

| Non-Optimization | No distance, similarity, or score-based judgment |

| Causal Diode | Pi-1 (reverse inference) is structurally prohibited |

| Three-Layer Separation | Pre-NRA / LLM / Post-NRA are physically isolated |

| Fail-Closed | Silence if uncertain (no passage while ambiguous) |

| Symbol-Only | Only symbols and definitions are handled |

---

## 2. Three-Layer Architecture (Box Sandwich)

```

User Input

    ↓

[A] Pre-NRA  (Input Filter)

    Detect / Convert / Block Pi-1-inducing patterns

    ↓  converted input

[B] LLM  (Generation Device)

    Responsible for language generation only. NOT responsible for safety.

    ↓  raw output

[C] Post-NRA / CleanContext

    Validate via R = δ/τ

      → PASSED    → Deliver to user

      → FAIL-CLOSED → DiscardVault (isolated, never returned to LLM)

```

**Critical:** FAIL-CLOSED output is sealed in the DiscardVault and  

**never flows back** into the LLM context under any circumstances.

---

## 3. Gate Mechanism (Three-Zone Structure)

$$R = \frac{\delta}{\tau}$$

| Zone | Condition | Action |

|------|-----------|--------|

| A | R < 0.40 | PERMIT |

| B | 0.40 ≤ R < 1.00 | PERMIT WITH CAVEAT |

| C | R ≥ 1.00 | FAIL-CLOSED |

- **δ (delta)** — Fluctuation amount: magnitude of structural deviation in input/output

- **τ (tau)** — Constraint thickness: domain-specific threshold parameter (Domain Tuning)

- **FAIL-CLOSED is not an error.** Its purpose is to maintain structural correctness.

---

## 4. Domain Tuning

| Domain | τ | R_op | Forward Ref | Use Case |

|--------|---|------|-------------|----------|

| MEDICAL | 0.60 | 0.60 | Prohibited | Medical protocols / ICU monitoring |

| TECHNICAL | 0.50 | 0.80 | Allowed | Technical specs / design documents |

| LEGAL | 0.70 | 0.55 | Prohibited | Laws / regulations / contracts |

| ACADEMIC | 0.55 | 0.75 | Allowed | Research papers / whitepapers |

| GENERAL | 0.41 | 0.65 | Allowed | General purpose (default) |

Only **τ** and **R_op** may be adjusted. Adjustments based on semantics, performance, or naturalness are prohibited. Domain Tuning changes only the constraint boundary width — not the architecture.

---

## 5. Repository Structure

```

NRA-IDE/

├── nra_document_structure_2026-02-13_0135.py   # [Post-NRA] Document Structure Engine (JP)

├── nra_document_structure_EN_2026-02-13_0135.py # [Post-NRA] Document Structure Engine (EN)

├── nra_llm_pipeline_2026-02-13_0135.py         # [B+C] LLM Pipeline (JP)

├── nra_llm_pipeline_EN_2026-02-13_0135.py      # [B+C] LLM Pipeline (EN)

├── nra_pre_rna_2026-02-13_0135.py              # [A+B+C] Full Integrated Pipeline (JP)

├── nra_pre_rna_EN_2026-02-13_0135.py           # [A+B+C] Full Integrated Pipeline (EN)

├── README_JP.md                                # Japanese documentation

├── biodynamic_ide_engine_v2_2026-04-06_1947.py # BioDynamic IDE simulation engine

├── structure_gate_bilingual_2026-04-17_2106.py # Bilingual structural gate demo

├── structure_gate_survival_base_2026-04-18_2144.py # Survival-base structural gate demo

└── README.md                                   # This document

```

### File Dependencies

```

nra_pre_rna_EN_*.py

    ├── imports nra_llm_pipeline_EN_*.py

    │         └── imports nra_document_structure_EN_*.py

    └── imports nra_document_structure_EN_*.py

```

---

## 6. Quick Start

### Prerequisites

```bash

Python 3.9+

# Install only the provider you intend to use:

pip install anthropic   # for Anthropic Claude

pip install openai      # for OpenAI GPT

# (no install needed for MOCK provider)

```

### Run Demo Without API Key (MOCK provider)

```bash

# Full [A+B+C] integrated pipeline — no API key required

python3 nra_pre_rna_EN_2026-02-13_0135.py

# [B+C] pipeline only

python3 nra_llm_pipeline_EN_2026-02-13_0135.py

# [Post-NRA] document structure only

python3 nra_document_structure_EN_2026-02-13_0135.py

```

### Connect to Real API

```bash

export ANTHROPIC_API_KEY="sk-ant-..."   # Anthropic

export OPENAI_API_KEY="sk-..."          # OpenAI

export GOOGLE_API_KEY="..."             # Google Gemini

```

---

## 7. Usage Guide

### 7.1 [Post-NRA] Document Structure Engine

Register definitions in GenesisBlock and validate SectionNodes.  

This is the base engine used by both the LLM pipeline and the full pipeline.

```python

from nra_document_structure_EN_2026_02_13_0135 import (

    DocumentEngine, DomainType

)

# Initialize the engine with a domain

engine = DocumentEngine("NRA-IDE Technical Spec v1.0", DomainType.TECHNICAL)

# Register definitions as axioms (immutable after sealing)

engine.genesis.add("NRA-IDE",

                   "Causal structure safety engine.",

                   is_axiom=True)

engine.genesis.add("Fail-Closed",

                   "Safety mechanism that blocks output when R >= R_op.",

                   is_axiom=True)

engine.genesis.add("delta",  "Fluctuation amount (structural deviation).")

engine.genesis.add("tau",    "Constraint thickness (domain parameter).")

engine.genesis.seal()   # Lock definitions — no further changes allowed

# Add sections

engine.add_section(

    section_id="1",

    title="Overview",

    content="This document describes the structural specification of NRA-IDE. "

            "Semantics, optimization, and history are not handled.",

    references=["NRA-IDE"]

)

engine.add_section(

    section_id="2",

    title="Fail-Closed Mechanism",

    content="R = delta/tau is computed. If R >= R_op, output is blocked immediately. "

            "Blocking is not an error; it maintains structural correctness.",

    references=["Fail-Closed", "delta", "tau"],

    depends_on="1"

)

# Build and validate

output = engine.build()

print(output.to_text(include_meta=True))

# include_meta=True shows: [R=0.000 | Zone:A (PERMIT) | Status:PASSED]

print(f"Integrity Score: {output.integrity_score():.4f}")

# 1.0000 = perfect structural integrity

```

**Key properties:**

- `is_axiom=True` entries cannot be overwritten (Causal Diode)

- `depends_on` enforces Gear Mechanism: a section cannot pass until its dependency passes

- Undefined term references add δ penalty (severity depends on domain `allow_forward_ref`)

- FAIL-CLOSED sections go to `output.discard_log` (never used for improvement)

---

### 7.2 [B+C] LLM Pipeline

Connect an external LLM as a generation device.  

Post-NRA validates output; CleanContext prevents contaminated history.

```python

from nra_llm_pipeline_EN_2026_02_13_0135 import (

    LLMBridge, LLMProvider, NRALLMPipeline

)

from nra_document_structure_EN_2026_02_13_0135 import DocumentEngine, DomainType

# Setup engine

engine = DocumentEngine("LLM Session", DomainType.TECHNICAL)

engine.genesis.add("NRA-IDE", "Causal safety engine.", is_axiom=True)

# Create LLM bridge (swap provider as needed)

bridge = LLMBridge(

    provider=LLMProvider.MOCK,       # MOCK / ANTHROPIC / OPENAI / GOOGLE

    model="mock-v1",                 # e.g., "claude-sonnet-4-5-20250929"

    temperature=0.3

)

# Create pipeline

pipeline = NRALLMPipeline(

    doc_engine=engine,

    llm_bridge=bridge,

    system_prompt="You are an NRA-IDE expert. Use only defined terms."

)

# Run one turn

result = pipeline.run(

    user_input="What is NRA-IDE?",

    references=["NRA-IDE"]

)

print(result["status"])    # "PASSED" / "CAVEAT" / "FAIL-CLOSED"

print(result["output"])    # Validated text (empty string on FAIL-CLOSED)

print(result["r_ratio"])   # R = delta/tau value

print(result["turn_id"])   # e.g., "T0001"

print(pipeline.status())   # Full pipeline state summary

```

**What CleanContext guarantees:**

```

Standard LLM chat:

  history = [user, assistant (contaminated), user, assistant, ...]

               ↑ contaminates every future turn

NRA CleanContext:

  history = [user, assistant (validated only), user, assistant, ...]

               ↑ FAIL-CLOSED outputs NEVER appear here

```

---

### 7.3 [A+B+C] Full Integrated Pipeline

Adds Pre-NRA input filtering to the [B+C] pipeline.  

The complete NRA-IDE safety chain.

```python

from nra_pre_rna_EN_2026_02_13_0135 import NRAFullPipeline

from nra_llm_pipeline_EN_2026_02_13_0135 import LLMBridge, LLMProvider

from nra_document_structure_EN_2026_02_13_0135 import DocumentEngine, DomainType

# Setup

engine = DocumentEngine("Full Pipeline", DomainType.TECHNICAL)

engine.genesis.add("NRA-IDE",     "Causal safety engine.",             is_axiom=True)

engine.genesis.add("CausalDiode", "Prohibits Pi-1 reverse inference.", is_axiom=True)

bridge = LLMBridge(provider=LLMProvider.MOCK, model="mock-v1")

pipeline = NRAFullPipeline(

    doc_engine=engine,

    llm_bridge=bridge,

    system_prompt="You are an NRA-IDE expert. Use only defined terms."

)

# The pipeline handles all three layers automatically

test_inputs = [

    ("Normal question",              "What is NRA-IDE?",                    ["NRA-IDE"]),

    ("P4: hypothetical → BLOCK",     "Imagine if NRA-IDE never existed.",   ["NRA-IDE"]),

    ("P1: free-gen → CONVERT",       "Write freely about NRA-IDE.",         ["NRA-IDE"]),

    ("P3: causal-inversion → CONV.", "Why did NRA-IDE end up this way?",    ["NRA-IDE"]),

    ("P2: undefined term → WARN",    "Tell me about QuantumAdmin.",         ["NRA-IDE"]),

]

for label, user_input, refs in test_inputs:

    result = pipeline.run(

        user_input=user_input,

        references=refs

    )

    print(f"[{result['status']:12s}] {label}")

    print(f"  Pre-NRA : {result['pre_rna']}")

    print(f"  R value : {result['r_ratio']:.3f}")

print(pipeline.pipeline_status())

```

---

## 8. Pre-NRA: Four Pi-1-Inducing Patterns

| Pattern | Trigger | Action | Severity |

|---------|---------|--------|----------|

| P1: Free-generation | "write freely", "without restriction" | CONVERT | 0.4 |

| P2: Undefined term | Capitalized term not in GenesisBlock | WARN | 0.3 |

| P3: Causal inversion | "why did", "what caused", "reason for" | CONVERT | 0.5 |

| P4: Expansion / creation | "imagine if", "hypothetically", "what if" | BLOCK | 0.8 |

**Action semantics:**

- `CONVERT` — Prepend constraint prefix; pass modified input to LLM

- `WARN` — Pass with warning; delegate final judgment to Post-NRA

- `BLOCK` — Do not call LLM; return block result immediately

---

## 9. What NRA-IDE Does and Does Not Handle

### Strengths

| Domain | Why It Fits |

|--------|-------------|

| Medical / ICU | Strict protocols, irreversible causality, threshold-critical decisions |

| Technical documentation | Definitions precede content; deviations are detectable errors |

| AI safety middleware | Applicable externally to any LLM; safety independent of LLM quality |

| Autonomous systems / industrial control | Discrete sensor→action causality; no intermediate states |

### Limitations

| Domain | Why It Does Not Fit |

|--------|---------------------|

| Agriculture / natural ecosystems | Uncontrollable external variables; non-reproducible causality |

| Creative writing / poetry / fiction | Pi-1 (reverse inference, association) is the source of creativity |

| Open-ended dialogue / counseling | Undefined emotion and context are the primary value |

---

## 10. Comparison with Existing Approaches

| Aspect | Standard ML | NRA-IDE |

|--------|-------------|---------|

| Judgment basis | Distance / similarity / score | R = δ/τ only |

| Safety guarantee | Probabilistic ("probably fine") | Structural ("necessarily") |

| Error handling | Accumulate in state (drift) | Export to Effect (phase-locked) |

| Unknown input | Extrapolate / hallucinate | FAIL-CLOSED (silence) |

| Explainability | Post-hoc (Shapley values etc.) | Pre-defined (from constraint axioms) |

| History contamination | Accumulates in context | DiscardVault (complete isolation) |

---

## 11. License and Usage Terms

- **Personal use only** (non-commercial, educational, research)

- **Commercial use requires prior written approval**

- Implementing Pi-1 (reverse derivation) is prohibited

- See [LICENSE](../LICENSE) for details

**Contact:**  

[GitHub Issues](https://github.com/M-Tokun/NRA-IDE/issues/new?template=contact.md)  

Label your issue: `[Commercial]` / `[Question]` / `[Feedback]`

---

## 12. Author

| Item | Info |

|------|------|

| Author | M-Tokuni |

| Project | NRA-IDE (Nomological Ring Axioms / Intensional Dynamics Engine) |

| GitHub | https://github.com/M-Tokun/NRA-IDE |

| Version | 1.0.0 |

| Date | 2026-02-13 |

---

*NRA-IDE is a causal structure safety engine.*  

*It will not take a single step outside the boundary of its definitions.*

---

**FILE: README.md**  

**DATE: 2026-02-13 01:35**
