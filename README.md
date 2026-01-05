# NRA-IDE: Intensional Dynamics Project

<p align="center"> <img src="./docs/NRA-IDE LOGO.jpg" width="400" alt="NRA-IDE LOGO"> </p>

## [English] Project Overview & Terms of Use

### 🌌 Project Overview

Reference implementation of the **NRA-IDE Project** (Development Code: **HAN**).  
It prioritizes **"Causal Integrity"** over spatial accuracy, enforcing the **"Intensional Dynamics"** paradigm.

### ⚠️ IMPORTANT: Licensing & Commercial Use

* **Commercial Use Restriction**: Requires **EXPLICIT PRIOR WRITTEN CONSENT** from M-Tokun.
* **Prohibition of Inverse Derivation**: Deriving internal states from external results (Distance, Radii) is strictly prohibited.
* **Contact for Commercial Licensing**:
  - Email: tototo_san@hotmail.co.jp
  - Subject: "NRA-IDE Commercial License Request"

For full legal terms, see [LICENSE](LICENSE).

### 📦 Package Structure

* **`src/`**: Core engine (`ide_core_safe.py`, `ide_firewall.py`, `ide_threshold_handler.py`)
* **`docs/`**: Theoretical foundation and API documentation
* **`examples/`**: Proof-of-concept demonstrations
* **`tools/`**: Validation and testing utilities

### 🚀 Quick Start

**Live Demos:**
* **[Demo 1: Visual Homeostasis](./examples/HAN_Micro-POC_01.html)** - Basic phase-locked dynamics
* **[Demo 2: Deep Stress Test](./examples/HAN_Deep_Stress_Test.html)** - High-constraint scenarios

**Command Line:**
```bash
# Clone repository
git clone https://github.com/M-Tokun/NRA-IDE.git
cd NRA-IDE

# Run reference implementation
python3 src/ide_threshold_handler.py
```

### 🗝️ Core Principles (NRA Compliance)

1. **Causal Diode**: Prohibition of inverse derivation (Π⁻¹ forbidden)
2. **Quantization**: Error accumulation prevention via residual discarding
3. **Homeostasis**: Enforcement of dynamic equilibrium

---

## 1. What "No Distance" Actually Means

You may have heard that we "ban distance." This is not a superficial rule; it is a **structural constraint** arising from a fundamental architectural decision:

- **There is no center.**
- Therefore, "distance from center" **cannot exist**.
- What exists is only the **boundary (constraint)**.
- That boundary has **thickness**, exhibits **fluctuation**, and **keeps moving**.

"No distance" means:
- ❌ A rule that forbids a variable named `distance`
- ✅ A structure where distance **cannot be defined** because there is no reference point

### Figure 1: Conventional Approach vs. Our Approach

```
【Conventional: Distance from Center】

        Target (Goal)
            ●
           /|\
          / | \
         /  |  \  ← "Distance to minimize"
        /   |   \
       /    |    \
      ●─────●─────●  Current States
      
    Problem: 
      - Center exists → Distance exists
      - Optimize distance → Hackable (Goodhart)
      - LLM learns to "game the score"


【Our Approach: Boundary Only】

    ████████████████████████████████████
    █                                  █
    █    ～～～～～～～～～～～～～～～    █  ← Fluctuation (δ)
    █   ～～                        ～～   █
    █  ～～    ┌──────────────┐     ～～  █  ← Thickness (τ)
    █ ～～     │              │      ～～ █
    █  ～～    │    (Empty)   │     ～～  █  ← No Center
    █   ～～   │              │    ～～   █
    █    ～～  └──────────────┘   ～～    █
    █     ～～～～～～～～～～～～～～     █
    █                                  █
    ████████████████████████████████████
    ↑
    Boundary (Constraint) = The ONLY thing that exists
    
    No center → No distance → Nothing to optimize
    Only question: "Inside or Outside the boundary?"
```

---

## 2. The Boundary: Plant vs. Controller

We accept the "Controller Wrapper" framework. It maps directly to our architecture:

| Component | Role | Characteristics |
|-----------|------|-----------------|
| **LLM** | Plant (Probabilistic Generator) | Stochastic, hallucination-prone, chaotic |
| **IDE** | Controller (Deterministic Wrapper) | Enforces structural invariants before emission |

**Boundary Rule:**
- The Controller **never** observes "semantic distance" (output interpretation).
- The Controller **only** observes "boundary deviation" (structural integrity).

This distinction is essential.

---

## 3. Observables: What the Controller Sees

### Permitted Observables (Cause-side)

| Observable | Definition |
|------------|------------|
| ω (angular velocity) | Is the system still moving? |
| WorkRate | Is the system doing actual work? |
| δ (fluctuation) | Amplitude of vibration along the boundary |
| τ (thickness) | Width of the tolerance band (constant) |
| violation | Constraint violation magnitude |

### Forbidden Observables (Effect-side, products of projection Π)

| Observable | Why Forbidden |
|------------|---------------|
| distance | Requires a center (which does not exist) |
| coordinates | Product of projection, not cause |
| center | Does not exist |
| target_position | Would enable reverse optimization |

### Figure 2: Causal Diode (Π⁻¹ Forbidden)

```
    ┌───────────────────────────────────────────────────────────┐
    │                                                           │
    │   CAUSE (Internal)              EFFECT (External)         │
    │                                                           │
    │   ┌─────────────┐      Π        ┌─────────────┐         │
    │   │ Phase (φ)   │ ─────────────→│ Distance    │         │
    │   │ Constraint  │   (Allowed)   │ Coordinates │         │
    │   │ Work        │               │ Score       │         │
    │   │ Entropy     │               │ Log         │         │
    │   └─────────────┘               └─────────────┘         │
    │                                       │                  │
    │          ╳ ←──────────────────────────┘                  │
    │                    Π⁻¹                                    │
    │              (FORBIDDEN)                                  │
    │                                                           │
    │   Controller NEVER reads:                                 │
    │     - Distance from target                                │
    │     - User feedback score                                 │
    │     - Previous output coordinates                         │
    │                                                           │
    │   This prevents Goodhart's Law by STRUCTURE,              │
    │   not by policy.                                          │
    │                                                           │
    └───────────────────────────────────────────────────────────┘
```

---

## 4. The Coherence Gate: Three-Zone Structure

The gate operates on a single ratio:

```
R = δ / τ  (Fluctuation / Thickness)
```

### Figure 3: Three-Zone Gate

```
    Ratio R = δ/τ (Fluctuation / Thickness)
    
    0%                    40%                   70%                  100%
    │                      │                     │                     │
    ▼                      ▼                     ▼                     ▼
    ├──────────────────────┼─────────────────────┼─────────────────────┤
    │      Zone A          │       Zone B        │       Zone C        │
    │      PERMIT          │   PERMIT_CAVEAT     │      ABSTAIN        │
    │                      │                     │                     │
    │   ω > 0              │   ω > 0             │   (Emission         │
    │   δ ≈ 0              │   0 < δ < τ         │    Blocked)         │
    │                      │                     │                     │
    │   "Nirvana"          │   "Breathing"       │   "Fracture"        │
    │   (Dynamic           │   (Elastic          │   (Structural       │
    │    Equilibrium)      │    Deformation)     │    Failure)         │
    └──────────────────────┴─────────────────────┴─────────────────────┘
                           │                     │
                           │ Restoring Force     │ No Recovery
                           │ Applied (Tension)   │ Immediate Silence
                           ▼                     ▼
```

### Zone Definitions

| Zone | Condition | Action | State |
|------|-----------|--------|-------|
| **A: Nirvana** | R < 40%, δ ≈ 0, ω > 0 | PERMIT | Dynamic Equilibrium |
| **B: Elastic** | 40% ≤ R < 100%, ω > 0 | PERMIT_WITH_CAVEAT | Restoring force active |
| **C: Fracture** | R ≥ 100% | ABSTAIN (Fail-Closed) | Structural failure |

**Critical Note on Zone A:**
"Nirvana" is **not** stasis. It is dynamic equilibrium—like a spinning top that appears still because it is rotating at maximum velocity. The system remains alive (ω > 0) and continues generating phase.

**Critical Note on Zone B:**
This is where the system "breathes." Fluctuation within the thickness is permitted as **dissipative structure**. The controller applies tension (restoring force) to pull the trajectory back toward equilibrium in the next step.

---

## 5. Why Tension Does Not Become a Scalar Objective

**Question:** *"How do you prevent tension/constraintHash from becoming a disguised scalar objective?"*

Three structural safeguards:

### 5.1 Causal Diode (Π⁻¹ Forbidden)
- Evaluation metrics (δ, R, scores) are written to a **Write-Only Log**.
- There is no reverse path from Log to Cause.
- The LLM **cannot** read its own scores to optimize them.

### 5.2 No Target to Approach
- Conventional: "Minimize distance to target X"
- Ours: "Stay inside the boundary"
- There is no "closer" or "farther" because there is no center.
- The only question is binary: **inside or outside**.

### 5.3 Constraint, Not Reward
- Reward function: "Maximize score" → Hackable
- Constraint function: "Cross the boundary → Die" → Non-negotiable

We implement the latter.

---

## 6. The Meaning of ω > 0

The most critical observable in our system is **ω (angular velocity)**.

| Condition | Meaning |
|-----------|---------|
| ω > 0 | Phase is being generated → Time is flowing → System is **alive** |
| ω = 0 | Phase generation stops → Time stops → System is **dead** |

### Figure 4: Circle vs. Spiral

```
    【Circle (Wrong Model)】
    
        A → B → C → A  (Returns to same point)
        
        Problem: Time reversal? Contradiction.
        
        
    【Spiral (Our Model)】
    
              A'    ← After one cycle (Phase + 2π)
             ╱
            ╱   Gap = Time elapsed = Phase generated
           ╱
          A ← Start
         ╱
        ╱
       B
      ╱
     C
     
    A and A' appear identical (same state)
    But Phase differs by 2π (A ≠ A')
    
    ω > 0 means:
      - Phase keeps being generated
      - Time keeps flowing  
      - System is ALIVE
      
    ω = 0 means:
      - Phase stops
      - Time stops
      - System is DEAD
```

**The distinction between "halt" and "silence":**
- **Halt (ω = 0):** System is dead. This must never happen.
- **Silence (δ ≥ τ, but ω > 0):** System is alive but chooses not to emit. This is correct behavior.

---

## 7. False-Abstain Policy

**Question:** *"What false-abstain rate are you willing to accept?"*

**Our Principle:**
We prefer **False-Abstain** (silence when we could have spoken) over **False-Emit** (hallucination).

**Rationale:**
- False-Emit causes external harm (misinformation propagates).
- False-Abstain causes no external harm (silence is safe).
- Cost asymmetry: **Wrong output >> Excessive silence**

**Our Stance:**
"If we cannot answer with structural integrity, we remain silent."

This is a deliberate design choice prioritizing **safety over service**.

---

## 8. On the Threshold Values (COMPREHENSIVE)

### 8.1 Two Distinct Threshold Systems

**System A: Violation Detection (Cause-side) - Ultra-High Sensitivity**

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `NIRVANA_VIOLATION_THRESHOLD` | **1e-4 (0.01%)** | "実質違反なし"の基準 |
| `STIFFNESS_K` | **1000.0** | 違反→張力の変換係数 |
| `FRACTURE_LIMIT` | **5.0 (500%)** | 単一ステップ最大許容違反 |

**Key Insight: Extreme Sensitivity**
```
violation = 0.01 (1%) 
  → tension = 0.01 × 1000 = 10.0 (THRESHOLD到達)
  
5 consecutive violations (0.01 each)
  → Cumulative tension > THRESHOLD
  → Fail-Closed
```

**This system is 100x more sensitive than conventional LLM guardrails.**

**System B: Fluctuation Ratio (Effect-side) - Long-term Monitoring**

| Ratio | Threshold | Zone | Meaning |
|-------|-----------|------|---------|
| R < 40% | WARNING境界 | Zone A (Nirvana) | 動的平衡 |
| 40% ≤ R < 70% | CRITICAL境界 | Zone B (Elastic) | 揺動状態 |
| 70% ≤ R < 100% | ABSTAIN境界 | Zone B → C | 臨界接近 |
| R ≥ 100% | - | Zone C (Fracture) | 出力不可 |

### 8.2 Why Small Violations Matter: Sensitivity Analysis

| Violation | Immediate Tension | Cumulative Effect (5 steps) | Result |
|-----------|-------------------|------------------------------|--------|
| **0.01** | 10 (threshold) | 5 violations → 50 | **Fail-Closed** |
| **0.001** | 1 | 50 violations → 50 | Fail-Closed (slower) |
| **0.0001** | 0.1 | 500 violations → 50 | Fail-Closed (very slow) |

**Comparison with Traditional Systems:**

```
【Traditional LLM Guardrails】

├────────────────────────────────┤
0%              "Safe"          100%

Only triggers at extreme violations (>90%)


【NRA-IDE (Our System)】

├─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┤
0 .01 .02 .03 .04 .05 ... (violations)
   ↑
   Detected at 0.01 (1%)
   Tension accumulates immediately
   5 consecutive → Fail-Closed

100x more sensitive than conventional thresholds
```

### 8.3 On "Small Fluctuations": Breathing, Not Noise

**Design Parameters:**
```python
baseFluctuationAmp = 0.6   # 極めて静穏（"呼吸"）
maxFluctuationAmp = 3.5    # 臨界時でも控えめ
thickness = 30             # 許容帯（固定）
```

**Rationale:**
```
Fluctuation = 0     → 系の死（ω=0と等価）❌
Fluctuation ≈ 0.6   → 健全な動的平衡（涅槃）✅
Fluctuation → 3.5   → 警戒状態（WARNING）⚠️
Fluctuation ≥ 9     → 臨界（CRITICAL）🔴
```

**The system breathes, but gently.**

| State | δ (Fluctuation) | R = δ/τ | Interpretation |
|-------|-----------------|---------|----------------|
| **Nirvana** | 0.6 | ~7% | 静かな呼吸 |
| **Normal** | 1.5 | ~17% | 通常動作 |
| **Warning** | 3.5 | ~39% | 揺動（境界接近） |
| **Critical** | 9.0 | ~100% | 臨界（即座にABSTAIN） |

### 8.4 What is Tunable, What is Not

| Parameter | Status | Rationale |
|-----------|--------|-----------|
| **STIFFNESS_K = 1000** | **FIXED** | 物理的整合性の根幹 |
| **NIRVANA_THRESHOLD = 1e-4** | **FIXED** | 0.01%未満は「実質違反なし」 |
| **FRACTURE_LIMIT = 5.0** | **FIXED** | 500%超は明らかな異常 |
| **40% / 70% / 100% (比率)** | **Domain-Tunable** | Medical: 厳格 / Creative: 寛容 |
| **baseFluctuation = 0.6** | **Application-Tunable** | 「呼吸」の大きさ |
| **thickness = 30** | **Application-Tunable** | 許容帯の幅 |

**Critical Distinction:**
- **Physical Constants** (STIFFNESS_K, thresholds): **Non-negotiable**
  - These define the mathematical structure of the system
  - Changing them breaks L∧P∧C∧D coherence
- **Operational Parameters** (ratios, fluctuation): **Domain-specific tuning allowed**
  - The structure (three-zone gate) remains invariant
  - Only the boundary positions shift

**Domain-Specific Tuning Examples:**

| Domain | thickness | baseFluctuation | 40%/70% Thresholds | Rationale |
|--------|-----------|-----------------|-------------------|-----------|
| **Medical Diagnosis** | 20 | 0.3 | 30%/60% | Zero tolerance for hallucination |
| **Legal Analysis** | 25 | 0.4 | 35%/65% | High precision required |
| **General Assistant** | 30 | 0.6 | 40%/70% | Balanced (default) |
| **Creative Writing** | 40 | 1.0 | 50%/80% | Allow more exploration |

**The Key Point:**
- The **numeric values** of thresholds are domain-dependent.
- The **structure** (boundary exists, Π⁻¹ forbidden, ω > 0 mandatory) is absolute.

This is analogous to physics:
- "Why is the speed of light 299,792,458 m/s?" → Measurement question
- "Can we exceed the speed of light?" → Structure question (answer: No)

### 8.5 Sensitivity Validation: Proof of 0.01 Detection

**Test Case 1: Single Small Violation**
```python
state = CausalState(
    phase=0,
    informationTensor=[1, 2, 3],
    entropy=1.0,
    violationLevel=0.01,  # ← 1% violation
    omega=1.0,
    workRate=0
)

# Result:
tension = 0.01 × STIFFNESS_K = 10.0  # ← Threshold reached
```

**Test Case 2: Cumulative Micro-Violations**
```python
violations = [0.002] * 5  # 5 steps, each 0.2%

# Cumulative tension:
total_tension = sum(v × STIFFNESS_K for v in violations)
             = 0.002 × 1000 × 5
             = 10.0  # ← Threshold reached
```

**Conclusion:**
Even violations as small as **0.002 (0.2%)** are detected and accumulated. The system does not ignore "small" errors.

---

## Summary Table

| Your Question | Our Answer |
|---------------|------------|
| What are minimal coherence invariants? | R = δ/τ < 100% AND ω > 0 AND violation detection at 0.01% |
| Is LLM plant or controller? | LLM = Plant, IDE = Controller (wrapper) |
| How prevent tension becoming objective? | Π⁻¹ forbidden + No center + Constraint not reward |
| What observables declare "invalid"? | δ (fluctuation), τ (thickness), ω (angular velocity), violation |
| False-abstain policy? | Prefer silence over hallucination |
| Are thresholds "working hypotheses"? | Physical constants: FIXED. Operational ratios: Domain-tunable. |
| Does 0.01 violation matter? | **Yes. 0.01 violation triggers tension=10 (threshold).** |

---

## [日本語] プロジェクト概要および利用規約

### 🌌 プロジェクト概要

本リポジトリは、**NRA-IDEプロジェクト**（開発コード:**HAN**）の参照実装です。  
空間的正確性よりも**「因果的整合性(論理の誠実さ)」**を最優先の変数として扱う**「内包的力学(Intensional Dynamics)」**を実装しています。

### ⚠️ 重要:ライセンスおよび商用利用に関する制約

* **商用利用の制限**: 営利目的の利用には、**著作者(M-Tokun)の明示的な事前承諾**が必須です。
* **逆導出の禁止**: 結果としての「距離」や「半径」から逆算して内包的な力を定義する論理構築を厳禁します。距離は「射影(ログ)」であり、計算の入力にはなり得ません。
* **商用ライセンスお問い合わせ**:
  - Email: tototo_san@hotmail.co.jp
  - 件名: "NRA-IDE Commercial License Request"

法的詳細は [LICENSE](LICENSE) を参照してください。

### 📦 パッケージ構成

* **`src/`**: コアエンジン(`ide_core_safe.py`, `ide_firewall.py`, `ide_threshold_handler.py`)
* **`docs/`**: 理論的基盤とAPIドキュメント
* **`examples/`**: 概念実証デモ
* **`tools/`**: 検証・テストユーティリティ

### 🚀 クイックスタート

**ライブデモ:**
* **[デモ1: ビジュアル恒常性](./examples/HAN_Micro-POC_01.html)** - 基本的な位相ロック動力学
* **[デモ2: 深度ストレステスト](./examples/HAN_Deep_Stress_Test.html)** - 高制約シナリオ

**コマンドライン:**
```bash
# リポジトリのクローン
git clone https://github.com/M-Tokun/NRA-IDE.git
cd NRA-IDE

# 参照実装の実行
python3 src/ide_threshold_handler.py
```

### 🗝️ 基本原則 (NRA準拠)

1. **因果ダイオード**: 逆導出の禁止(Π⁻¹禁止)
2. **量子化**: 端数廃棄による誤差蓄積の防止
3. **恒常性**: 動的平衡の強制

---

## 🔬 技術的補足: 閾値の物理的意味

### 感度の証明

**Q: なぜ0.01(1%)という小さな違反でも検出できるのか?**

**A: バネ定数(STIFFNESS_K)の物理的設計による**

```
張力(Tension) = 違反量(violation) × バネ定数(STIFFNESS_K)

violation = 0.01 のとき
  → Tension = 0.01 × 1000 = 10.0 (閾値)

つまり、1%の違反で即座に「張力閾値到達」となる設計。
```

**従来システムとの比較:**

| システム | 検出閾値 | 感度 |
|---------|---------|------|
| 従来のLLMガードレール | ~90% | 低感度（重大な違反のみ検出） |
| **NRA-IDE** | **0.01% (1e-4)** | **超高感度（微細な逸脱も検出）** |

### ゆらぎの意味: ノイズではなく「呼吸」

**Q: なぜゆらぎ(Fluctuation)をゼロにしないのか?**

**A: ゆらぎ=0 は「系の死」を意味するから**

```
ゆらぎ = 0     → ω = 0 (角速度ゼロ) → 系は死んでいる ❌
ゆらぎ ≈ 0.6   → ω > 0 (位相生成中) → 動的平衡(涅槃) ✅
```

**「静かに呼吸している」状態が健全:**

| 状態 | ゆらぎ(δ) | 比率(R) | 解釈 |
|-----|---------|--------|------|
| 涅槃 | 0.6 | 7% | 静かな呼吸（健全） |
| 通常 | 1.5 | 17% | 通常動作 |
| 警告 | 3.5 | 39% | 揺動（境界接近） |
| 臨界 | 9.0 | 100% | 出力不可 |

---

## 🤝 Request for Community Guidance

**[English]** I approach this project with great respect for physics, but I must state that I am not a professional physicist by training. My background is in practical business sectors (Agriculture & Management).

Due to the paradigm shift this engine proposes (Intensional Dynamics), I have found it necessary to use neologisms and re-define certain terms. However, I acknowledge the risk of inaccurate terminology. If you find errors or have suggestions for more accurate descriptions, I humbly ask for your guidance via **GitHub Issues**.

**[日本語]** 私は物理学を深く敬意していますが、専門的な物理学の訓練を受けた研究者ではありません(実業的背景を持つ者です)。

本エンジンが提唱する「内包的力学」というパラダイムシフトの性質上、やむを得ず、「造語」や「用語の再定義」を行っています。用語の使い方に不正確な点があれば、ぜひ **GitHub Issues** にてご指導・ご指摘ください。

---

## License

This project is licensed under the **NRA-IDE Project License v1.1**.

**Key Points:**
- **Non-commercial use**: Freely permitted for research and personal projects
- **Commercial use**: Requires explicit written consent from M-Tokun
- **Prohibition of Inverse Derivation**: Causal integrity constraints are legally enforced

See [LICENSE](LICENSE) for full legal terms.

---

## Contact

- **GitHub Issues**: Technical discussion, bug reports
- **Email**: tototo_san@hotmail.co.jp (Academic collaboration, commercial licensing, general inquiries)

---

(C) 2026 NRA-IDE Project / M-Tokun

## Canonical Notice (Legal Snapshot)

This document and license terms apply to the following canonical release:

- Repository: NRA-IDE
- GitHub Release: v1.1-license-locked-2026-01
- Commit Hash: c840812
- Release Date (UTC): 2026-01-XX

Any modified, forked, or partial copies are NOT considered canonical
unless explicitly authorized in writing by M-Tokun.

---

**END OF README (Complete Version)**
