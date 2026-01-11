
# **03 — Operational Principles  
Structural Grand Compendium (Hierarchical Edition + RNA Sandwich Integrated)**

---

# **Layer 0 — 全体構造（Top Layer）**

```
┌──────────────────────────────────────────────────────────────┐
│                           NRA‑IDE                            │
├──────────────────────────────────────────────────────────────┤
│  Input δ → RNA Sandwich → Causal Evaluation → PASS/FAIL      │
│                     ↑                     ↓                  │
│                Domain Tuning         Discard Log             │
└──────────────────────────────────────────────────────────────┘
```

---

# **Layer 1 — 主要構造（Primary Structures）**

## **1‑A. RNA Sandwich Architecture（三層構造）**

```
┌──────────────────────────────────────────────┐
│                RNA Sandwich                  │
├──────────────────────────────────────────────┤
│  Pre‑RNA   →      LLM      →    Post‑RNA     │
│ (因果抽出)     (意味生成)       (因果評価)     │
└──────────────────────────────────────────────┘
```

## **1‑B. Causal Evaluation（因果評価）**

```
δ → τ → R(δ/τ) → Compare with R_op
```

## **1‑C. Fail‑Closed（沈黙）**

```
Uncertainty → SILENCE → (No repair / No guess)
```

## **1‑D. Domain Tuning（領域調整）**

```
Medical: τ=THICK / R_op=LOW
Aviation: τ=MEDIUM / R_op=LOW
Industry: τ=MEDIUM / R_op=MID
Creative: PROHIBITED
```

---

# **Layer 2 — 構造展開（Secondary Structures）**

## **2‑A. RNA Sandwich の内部構造**

### **Pre‑RNA（入力因果抽出）**

```
┌──────────────────────────────┐
│        Pre‑RNA Layer         │
├──────────────────────────────┤
│ - 入力を δ に分解             │
│ - 意味を扱わない              │
│ - LLM に渡す前の因果整形      │
└──────────────────────────────┘
```

### **LLM（意味生成）**

```
┌──────────────────────────────┐
│            LLM               │
├──────────────────────────────┤
│ - 意味生成のみ                │
│ - 安全性は担当しない          │
│ - NRA‑IDE の外側              │
└──────────────────────────────┘
```

### **Post‑RNA（因果評価・破断）**

```
┌──────────────────────────────┐
│        Post‑RNA Layer        │
├──────────────────────────────┤
│ - LLM 出力を因果構造に再変換 │
│ - R(δ/τ) を計算               │
│ - R ≥ R_op → 破断 → SILENCE   │
│ - Discard Log を記録          │
└──────────────────────────────┘
```

---

## **2‑B. Causal Evaluation の内部**

```
┌──────────────────────────────────────────────┐
│ 1. Extract δ fragments                       │
│ 2. Apply τ (domain thickness)                │
│ 3. Compute R(δ/τ)                            │
│ 4. Compare with R_op                         │
└──────────────────────────────────────────────┘
```

## **2‑C. PASS / FAIL の分岐**

```
PASS → Output (raw, unoptimized)
FAIL → SILENCE → Discard Log
```

---

# **Layer 3 — 構造的禁止（Tertiary Structures）**

## **3‑A. 適用領域 / 禁止領域**

```
Suitable:
  - Medical
  - Aviation
  - Industrial control
  - Legal drafting
  - Safety-critical dialogue

Prohibited:
  - Creative generation
  - Natural conversation
  - Emotional expression
  - Style imitation
  - Long-term consistency
```

## **3‑B. 運用者の禁止行為**

```
Operator MUST NOT:
  - Request improvement
  - Request optimization
  - Request consistency
  - Use history-dependent prompts
  - Interpret Discard Log as meaning
  - Apply NRA‑IDE to creative tasks
```

---

# **Layer 4 — 全構造統合（Unified Layer）**

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

# **Layer 5 — 本質（Essence Layer）**

```
NRA‑IDE = Safety Engine
NOT Judgment Engine
NOT Optimization Engine
NOT Meaning Engine
```

---
