
# **03 — Operational Principles  
Structural Grand Compendium (Hierarchical Edition + RNA Sandwich Integrated)**

---

# **Layer 0 — Top Layer (Overall Structure)**

```
┌──────────────────────────────────────────────────────────────┐
│                           NRA‑IDE                            │
├──────────────────────────────────────────────────────────────┤
│  Input δ → RNA Sandwich → Causal Evaluation → PASS / FAIL    │
│                     ↑                     ↓                  │
│                Domain Tuning         Discard Log             │
└──────────────────────────────────────────────────────────────┘
```

---

# **Layer 1 — Primary Structures**

## **1‑A. RNA Sandwich Architecture (Three‑Layer Structure)**

```
┌──────────────────────────────────────────────┐
│                RNA Sandwich                  │
├──────────────────────────────────────────────┤
│  Pre‑RNA   →      LLM      →    Post‑RNA     │
│ (Causal Extraction) (Meaning Generation) (Causal Evaluation) │
└──────────────────────────────────────────────┘
```

## **1‑B. Causal Evaluation**

```
δ → τ → R(δ/τ) → Compare with R_op
```

## **1‑C. Fail‑Closed (Silence)**

```
Uncertainty → SILENCE → (No repair / No guess)
```

## **1‑D. Domain Tuning**

```
Medical:   τ = THICK   / R_op = LOW
Aviation:  τ = MEDIUM  / R_op = LOW
Industry:  τ = MEDIUM  / R_op = MID
Creative:  PROHIBITED
```

---

# **Layer 2 — Secondary Structures (Structural Expansion)**

## **2‑A. Internal Structure of the RNA Sandwich**

### **Pre‑RNA (Input Causal Extraction)**

```
┌──────────────────────────────┐
│        Pre‑RNA Layer         │
├──────────────────────────────┤
│ - Decompose input into δ      │
│ - No meaning handled          │
│ - Structural shaping before LLM │
└──────────────────────────────┘
```

### **LLM (Meaning Generation)**

```
┌──────────────────────────────┐
│            LLM               │
├──────────────────────────────┤
│ - Meaning generation only     │
│ - No safety responsibility     │
│ - Exists outside NRA‑IDE       │
└──────────────────────────────┘
```

### **Post‑RNA (Causal Evaluation & Fracture Detection)**

```
┌──────────────────────────────┐
│        Post‑RNA Layer        │
├──────────────────────────────┤
│ - Reconvert LLM output into causal structure │
│ - Compute R(δ/τ)                              │
│ - R ≥ R_op → Fracture → SILENCE              │
│ - Record Discard Log                          │
└──────────────────────────────┘
```

---

## **2‑B. Internal Flow of Causal Evaluation**

```
┌──────────────────────────────────────────────┐
│ 1. Extract δ fragments                       │
│ 2. Apply τ (domain thickness)                │
│ 3. Compute R(δ/τ)                            │
│ 4. Compare with R_op                         │
└──────────────────────────────────────────────┘
```

## **2‑C. PASS / FAIL Branch**

```
PASS → Output (raw, unoptimized)
FAIL → SILENCE → Discard Log
```

---

# **Layer 3 — Tertiary Structures (Structural Prohibitions)**

## **3‑A. Suitable / Prohibited Domains**

```
Suitable:
  - Medical
  - Aviation
  - Industrial control
  - Legal drafting
  - Safety‑critical dialogue

Prohibited:
  - Creative generation
  - Natural conversation
  - Emotional expression
  - Style imitation
  - Long‑term consistency
```

## **3‑B. Operator Prohibitions**

```
Operator MUST NOT:
  - Request improvement
  - Request optimization
  - Request consistency
  - Use history‑dependent prompts
  - Interpret Discard Log as meaning
  - Apply NRA‑IDE to creative tasks
```

---

# **Layer 4 — Unified Layer (Full Structural Integration)**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                                NRA‑IDE (Unified)                             │
├──────────────────────────────────────────────────────────────────────────────┤
│  Input δ                                                                     │
│     │                                                                         │
│     ▼                                                                         │
│  RNA Sandwich (Pre‑RNA → LLM → Post‑RNA)                                      │
│     │                                                                         │
│     ▼                                                                         │
│  Causal Evaluation (δ → τ → R → R_op)                                         │
│     │                                                                         │
│     ├────────────── PASS ───────────────► Output (raw, unoptimized)          │
│     │                                                                         │
│     └────────────── FAIL ───────────────► SILENCE → Discard Log              │
│                                                                               │
│  Domain Tuning (τ, R_op)                                                      │
│  Responsibility Boundary                                                      │
│  Prohibited Domains                                                           │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

# **Layer 5 — Essence Layer**

```
NRA‑IDE = Safety Engine
NOT Judgment Engine
NOT Optimization Engine
NOT Meaning Engine
```

---
