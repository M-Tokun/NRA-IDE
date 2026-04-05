# Nomological Ring Axioms and the Intensional Dynamics Engine
## — A Structural Description of Threshold-Driven State Transitions —
### ( Part I: General Audience / Part II: Specialist Audience )

Author: M-Tokuni
NRA-IDE Project
Version 2.0 (Bilingual Edition — English / Japanese)
Published: 2026

> **Note:** This document presents the full text in English (Section I) followed by the complete Japanese original (Section II).
> The Japanese version is the primary source text. The English version is a faithful translation.
> 本書は英語版（第I部）に続いて日本語原文（第II部）を収録したバイリンガル版です。
> 日本語版が一次原文です。英語版はその忠実な翻訳です。

---

<br>

# ═══════════════════════════════════════
# SECTION I — ENGLISH
# ═══════════════════════════════════════

<br>

# Part I: General Audience
## "Why Does the World Sometimes Break Suddenly?"

---

## Abstract

We intuitively feel that change happens gradually. Yet in reality, bridges collapse without warning, bodies reach their limits, and power grids cascade into failure — all while measured values showed almost no change until that very moment.

Part I presents a framework for understanding this "suddenness" in structural terms rather than mathematical equations. No specialist knowledge is required. Only three concepts are needed: **accumulation**, **margin**, and **limit**.

---

## 1. Introduction: Phenomena That Continuous Change Cannot Explain

### 1.1 Before a Disaster, People Can Only Stand in Shock

On March 11, 2011, when the tsunami from the Great East Japan Earthquake overtopped the seawalls, the people standing there could do nothing. The seawalls had been functioning exactly as designed — until that moment.
Meteorological readings had been rising. Ground stress had been accumulating. Yet no one could accurately predict "how many minutes until it overflows." What was being observed was the *rate of change*. But the essence of the problem was *the distance remaining to the boundary*.
This is not unique to tsunamis.
A mountain slope weakens slowly over decades. Then in one instant, it collapses. A bridge's steel absorbs millions of repetitive vibrations. Then on a quiet morning, it suddenly fractures. A physician confirms that a patient's test values are within normal range. Yet the following day, an organ stops functioning.

**In every case, the rate of change was small. But the approach to the boundary had been advancing.**

Most conventional scientific descriptions are built around "velocity," "acceleration," and "rate of change." Newtonian mechanics and calculus are prime examples, functioning with exceptional precision in stable regions. However, these frameworks are not well suited to directly describing *how close a state is to its boundary*.
That is the starting point of this framework.

### 1.2 Why Could It Not Be Predicted?

The reason it could not be predicted was not that the wrong quantities were being measured. The problem was the **perspective** of measurement.
Measuring "velocity" requires time. Measuring "distance" requires a reference point. Both are quantities for describing *how change progresses*.
But when a structure approaches its limit, the essential question lies elsewhere.

**"How much more can this structure endure?"**

Answering this question requires different quantities. Not "velocity" but "accumulated amount." Not "distance" but "remaining margin." This framework is built around the ratio of those two quantities.

---

## 2. Core Axiom: Existence Is Generation

### 2.1 Static States Do Not Exist

The idea at the foundation of this framework can be expressed in a single sentence.

**Existence is generation.**

This is not a philosophical declaration — it is a structural observation.
A cup sitting on a desk appears to be at rest. Yet within it, molecules are vibrating and the material is continuously accumulating microscopic stress. "Stillness" is an approximation at the scale of human observation, not a structural reality.
The same holds for the living body. Even during sleep, the heart beats, cells metabolize, and neurons transmit signals. Complete stasis means death — and even that proceeds at the molecular level as a process of decomposition.

**Absolute stillness exists nowhere.**

### 2.2 History Accumulates

From the axiom "existence is generation," an important consequence follows.
Generative processes **accumulate history**.
Metal accumulates fatigue through repeated stress. The body consumes its capacity for repair as it ages. Infrastructure accumulates degradation through use. AI systems accumulate error.
This accumulation is difficult to see. It often does not appear on the surface of measured values. But it proceeds with certainty. And when the accumulation built up within a structure crosses a threshold — a state transition occurs.

### 2.3 The Same History Never Recurs

A further consequence follows.
Since generative processes carry history, **an identical state can never be perfectly reproduced**.
This is a structural qualification of the premise that "identical conditions yield identical results." Even when surface conditions are the same, if the internally accumulated histories differ, the structural response will differ.
This perspective carries important meaning for explaining the gap between reproducibility in laboratory experiments and behavior in real operational environments.

---

## 3. Intuitive Explanation of the Primary Equation

### 3.1 The Analogy of the Mechanical Clock

To understand the operating principle of this framework, consider the escapement mechanism of a mechanical clock.
A mechanical clock maintains accuracy not because its gears are perfect. It is because **the escapement advances in discrete, complete steps of exactly one tooth** — no fractional remainder carries forward.
Microscopic errors dissipate as heat rather than accumulating into the next calculation. Each step is structurally complete.
This is the operating principle of this framework. Rather than stacking continuous approximations, each state transition is made structurally complete, preventing the accumulation of error.

### 3.2 Three Quantities

This framework is composed of only three quantities.

**δ (delta): Accumulated Deviation**

The amount of deviation accumulated within a structure as history. For materials this corresponds to fatigue; for biological systems, stress; for engineered systems, load accumulation. δ tends to increase over time.

**τ (tau): Absorption Thickness**

The amount of margin a structure has for absorbing accumulated deviation. For materials this corresponds to toughness; for biological systems, tolerance; for engineered systems, buffer capacity. τ is determined at design time and may change with conditions.

τ is **not a time constant**. It is a structural margin of tolerance, independent of the time axis.

**R: Structural Ratio**

The ratio of δ to τ, defined by the following equation.

$$R = \frac{\delta}{\tau}$$

This is the primary equation of this framework.

### 3.3 What R Signifies

The value of R indicates the current structural state of the system.
When R is close to 0, accumulated deviation is small relative to the structural margin. The system is in a stable region — normal operating state.

As R approaches 1.0, accumulated deviation is exhausting the structural margin. The approach to the boundary is advancing.

**When R exceeds 1.0, the structure can no longer absorb the deviation. A state transition occurs.**

In materials engineering this transition is called "fracture." In medicine, "organ failure." In power engineering, "cascading power failure." In this framework all of these are treated uniformly as "states beyond the structural threshold."

### 3.4 Everyday Examples

**Stress Fracture**

When a marathon runner continues training without adequate rest, microscopic cracks accumulate in bone (increase in δ). The bone's repair capacity is finite; when accumulation outpaces repair, margin decreases (decrease in τ). When R exceeds 1.0, a fracture occurs. The problem was not the "velocity" of training volume but the ratio of accumulation to margin.

**Bridge Collapse**

A bridge absorbs microscopic vibration with each passing vehicle. How far the accumulation of this stress (δ) has progressed relative to the design tolerance (τ) determines the bridge's remaining service life. Even when appearance is unchanged, R is quietly approaching 1.0.

**Overwork Collapse**

The human body absorbs daily stress (τ). But stress that cannot be absorbed accumulates (δ). If τ does not recover through rest, R continues to rise. It is not the continuous change of "feeling a little tired" — at the moment a threshold is crossed, the body ceases to function.

---

## 4. Summary (Part I)

### 4.1 What Problem Is Being Solved

Conventional monitoring and control frameworks are built around "the rate of change." Temperature rising at a certain rate, pressure increasing at a certain rate, values deviating from norms at a certain rate — these are monitored, and the design responds *after* an anomaly appears.
But here lies a fundamental problem.

**State transitions occur before anomalies appear.**

The moment a bridge fractures, a bone breaks, an organ stops — in every case, while measured values were "still within normal range," the internal accumulation had already exceeded its limit. Monitoring velocity is not fast enough.
What this framework seeks to solve is this problem: the shift from "monitoring that notices after an anomaly appears" to "diagnosis that grasps proximity to the boundary in real time."

### 4.2 What Kind of Solution Is Being Pursued

This framework does not aim at "prediction."
Calculating "when it will break" is nearly impossible in most real systems. Too many variables, too complex a history. The more refined the predictive model, the more likely it diverges from reality.

What this framework aims at is **diagnosis**.

"How close is this structure to its limit right now?" — this single point is evaluated through the simple ratio R = δ/τ. If R is 0.3, there is margin. If R is 0.8, caution is needed. If R exceeds 1.0, a state transition has already occurred.
Even without prediction, diagnosis is possible. With diagnosis, the decision to intervene can be delegated to a human operator. This is the form of resolution this framework seeks.

### 4.3 How to Change the Way of Seeing

Understanding this framework requires changing only one thing about what is monitored.

| Conventional perspective | This framework's perspective |
|--------------------------|------------------------------|
| Monitor the rate of change | Monitor the ratio of accumulation to margin (R) |
| Feel reassured that values are "still within normal range" | Judge by "what is the value of R" |
| Respond after an anomaly appears | Intervene when R approaches 1.0 |
| Track change along a time axis | Read the current value of the structural ratio |
| Build refined predictive models | Measure δ and τ and calculate the ratio |

This shift in perspective requires no new measurement instruments. No need to learn a new theory from scratch. What is required is only a change in the question: "what do we measure?"

Measure accumulated deviation δ. Define absorption thickness τ. Monitor the ratio R. When R approaches 1.0, call for judgment — this simple procedure is the only structurally sound and practical means of preparing for "sudden collapse."

Part II defines this framework rigorously from a specialist perspective, detailing the dynamic τ extension formula, Integer Phase Lock, Fail-Closed design, and application across domains.

---

# Part II: Specialist Audience
## "Structural Definitions of the Nomological Ring Axioms and the Intensional Dynamics Engine"

---

## 5. Relationship to Existing Theories

### 5.1 Differences from Classical Continuous Dynamics and Calculus

Classical dynamical theories based on Newtonian mechanics and calculus describe system behavior through the time derivatives of state. This framework has extremely high descriptive power in stable regions (R ≪ 1).
This framework does not deny these theories. However, there is a fundamental difference in perspective.

Classical dynamics describes **"how the system changes."**
This framework evaluates **"how close the system is to its structural threshold."**
The former is the description of a trajectory; the latter is the diagnosis of proximity. These are complementary and do not conflict.

### 5.2 Differences from PID Control

PID control is a control theory that corrects deviation through three terms: proportional (P), integral (I), and derivative (D).
The R = δ/τ of this framework may appear superficially similar to the proportional term of PID, but the two are fundamentally different.

| Aspect | PID Control | This Framework (NRA-IDE) |
|--------|-------------|--------------------------|
| Purpose | Return deviation to zero (optimization) | Evaluate proximity to structural limit (diagnosis) |
| Meaning of τ | Does not exist | Structural tolerance width (independent of time) |
| Treatment of residuals | Accumulated as integral term | Expelled as heat, not carried forward |
| Form of output | Continuous control quantity | Discrete state judgment (R < 1 / R ≥ 1) |
| Role of human | System corrects autonomously | Human takes over when R ≥ 1 |

τ is not a time constant. τ is the thickness of the tolerance width that a structure holds by design — a structural quantity independent of the time axis.

### 5.3 Differences from Statistical Methods and Machine Learning

Statistical methods and machine learning probabilistically estimate future states from past data distributions. These function powerfully in regions where large amounts of data exist and distributions are stable.
The differences from this framework are as follows.
Statistical methods learn "average behavior." This framework evaluates "the current state of an individual structure." The former is set-theoretic; the latter is instance-specific.
Furthermore, statistical methods presuppose probabilistic approximation. This framework does not use probabilistic reasoning; it performs deterministic computation of R from measured values of δ and τ.

---

## 6. Rigorous Description of the Definition Equations

### 6.1 Primary Equation: Basic Structural Ratio

$$R = \frac{\delta}{\tau}$$

**Rigorous definitions of each quantity**

**δ (delta): Accumulated Deviation**
The amount of deviation accumulated as history within a structure. δ is a non-negative real number, updated with each state transition of the structure. The rate of accumulation of δ differs by domain and target.

**τ (tau): Absorption Thickness**
The amount of margin a structure has for absorbing accumulated deviation. τ is a positive real number, defined at design time. τ is not a time constant; it is a structural parameter independent of the time axis. τ may change dynamically (see 6.2).

**R: Structural Ratio**
The ratio of δ to τ. R is a dimensionless real number indicating proximity to the structural threshold.

**Decision Criteria**

| Value of R | Structural State | System Behavior |
|------------|-----------------|-----------------|
| R < 1 | Stable region | Continue normal output |
| R = 1 | Structural threshold | Output warning, notify human |
| R > 1 | Threshold exceeded | Cease output, delegate to human |

When R exceeds 1.0, the system does not make autonomous judgments. It presents information, falls silent, and delegates final judgment to the human operator. This is called **Fail-Closed**.

### 6.2 Secondary Equation: Dynamic τ — Dual-Fluctuation Formula

A static τ cannot appropriately handle asymmetric variation in the expansion and contraction directions. To address this, dynamic τ is defined.

**Upper EMA (Expansion-Direction Fluctuation)**

$$\mathrm{EMA}_{\text{upper}}(n) = \alpha_u \cdot \delta_u + (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)$$

The upper EMA smooths deviation δ_u in the expansion direction. α_u is the upper smoothing coefficient (0 < α_u ≤ 1).

**Lower EMA (Contraction-Direction Fluctuation)**

$$\mathrm{EMA}_{\text{lower}}(n) = \alpha_l \cdot \delta_l + (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)$$

The lower EMA smooths deviation δ_l in the contraction direction. α_l is the lower smoothing coefficient (0 < α_l ≤ 1).

**Asymmetric Definition of Dynamic τ**

$$\tau_{\text{upper}} = \tau \cdot f\!\bigl(\mathrm{EMA}_{\text{upper}}\bigr)$$

$$\tau_{\text{lower}} = \tau \cdot g\!\bigl(\mathrm{EMA}_{\text{lower}}\bigr)$$

The upper τ expands in the expansion direction; the lower τ contracts in the contraction direction. This asymmetry is the structural core of this framework. Most real systems exhibit different response characteristics in the expansion and contraction directions.

**Final Decision Formula (Asymmetric Dual Ratio)**

$$R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$$

The larger of the upper and lower ratios is adopted as R. This formula **operates within a closed world** and requires no external assumptions.

### 6.3 Definition of Phase Transition

What occurs when R exceeds 1.0 is not merely a "numerical exceedance." The system **transitions to a qualitatively different state**. This framework calls this a **phase transition**.

The structure is identical to phase transitions in physics — water becoming ice, liquid becoming gas. A continuous quantity changes, and at a certain threshold the phase changes suddenly. The change was continuous, but the state transition occurred discontinuously.
Phase transitions in this framework are defined as follows.

```
R < 1.0  : Stable phase   (accumulated deviation within absorption thickness)
R = 1.0  : Phase transition point (structural threshold)
R > 1.0  : Post-transition phase (structure unable to absorb deviation)
```

The critical point is that the post-transition phase is **structurally different** from the pre-transition phase. Even if R is returned below 1.0, the accumulated history does not disappear. A fractured bone does not return to its original state. A collapsed bridge does not recover naturally. **Phase transitions are irreversible.**
This irreversibility is the basis for "intervening before R approaches 1.0." The value lies in diagnosis before transition, not in response after transition.

### 6.4 The Survival Domain Formed by Dual Fluctuation

To understand the asymmetric structure of dynamic τ visually, consider the Survival Domain formed by τ.

```
  ── τ_upper ──────────────────────  Upper boundary (expansion direction)
        ↑
   Survival Domain
  (space where fluctuation is tolerated)
        ↓
  ── τ_lower ──────────────────────  Lower boundary (contraction direction)
```

This is called the **Survival Domain**. As long as the system's state remains within the Survival Domain, fluctuation is absorbed by the structure and no phase transition occurs.
The dual-fluctuation formula matters because τ_upper and τ_lower **move asymmetrically**.
When fluctuation in the expansion direction grows larger, τ_upper expands — the system attempts to tolerate that fluctuation over a wider range.
When fluctuation in the contraction direction grows larger, τ_lower contracts — the system tightens the margin on the lower side, structurally constraining excessive contraction.
This asymmetric movement **changes the shape of the Survival Domain**. Rather than a simple symmetric region, it is a living boundary that reshapes itself in response to the system's state.

**Reinterpretation of R**

The final decision formula $R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$ evaluates "how close the current state is to which boundary of the Survival Domain." It simultaneously monitors approach to the upper and lower boundaries, adopting the ratio of the more dangerous side as R.

### 6.5 The Survival Domain and Homeostasis

The concept of the Survival Domain shares the same structure as **homeostasis** in biology.
The human body maintains core temperature within a Survival Domain of approximately 36–37°C. Even when body temperature fluctuates, the organism attempts to return to within the Survival Domain through sweating, fever, and vasoconstriction. The moment the Survival Domain is significantly exceeded, organs begin to lose function — a phase transition occurs.
Blood glucose is the same. Blood pressure is the same. All of these are maintained within the asymmetric Survival Domain formed by τ_upper and τ_lower.

This framework generalizes the structure of biological homeostasis to materials, infrastructure, and AI systems.

**The Perspective of Designing the Survival Domain**

In system design using this framework, setting τ becomes the question: "where is the Survival Domain placed?" A larger τ means a wider Survival Domain, allowing the system to tolerate more fluctuation. A smaller τ means a narrower Survival Domain: the system is controlled more precisely, but the risk of phase transition rises.

Furthermore, the asymmetric ratio of τ_upper to τ_lower is a design decision about "which direction of fluctuation to tolerate more." In medicine, the tolerance width differs between excessive treatment (expansion direction) and insufficient treatment (contraction direction). In infrastructure, degradation characteristics differ between overload and underload. Explicitly incorporating this asymmetry into design is the essential meaning of dynamic τ.

---

## 7. Design Principles of the IDE (Intensional Dynamics Engine)

### 7.1 Integer Phase Lock

This engine does not process state transitions as continuous floating-point values. Each state transition is treated as a **discrete, structurally complete step**.

Residual ε (the fractional remainder generated by floating-point arithmetic) is not carried forward to the next step. Residuals are **expelled as heat**. This structurally prevents the accumulation of error.

```
In computing R = δ / τ :
  Integer part of quotient  →  used for next state judgment
  Residual ε                →  discarded (expelled as heat)
  Carry-over                →  prohibited
```

This principle follows the same logic as the escapement of a mechanical clock.

### 7.2 Fail-Closed Design

Fail-Closed does not mean system halt. It refers to a design that **suppresses output while maintaining structural state**.

When R ≥ 1.0 is judged:
- The system does not make autonomous judgments, offer alternatives, or engage in exploration
- It presents only information about the structural state
- It falls silent and waits for human judgment
- It records human judgment in a log, making the locus of responsibility clear

This is not "giving up" — it is **the clarification of the division of responsibility between human and machine**. The machine diagnoses; the human judges.

### 7.3 Axiom of Confession

This framework obligates disclosure of the fact when approximate computation has been used. This is called the **Axiom of Confession**.

Cases requiring disclosure:
- When floating-point arithmetic is used: report "Linear approximation distortion has occurred."
- When causal inversion (back-projection) is used: report "Causal violation (inverse projection) detected."
- When the linear domain is exceeded: report "Linear boundary exceeded."

This axiom does not prohibit approximation. It **prohibits concealing the use of approximation**. The purpose is to secure the information a human needs to make an appropriate judgment.

---

## 8. Application Across Domains

### 8.1 Medical Domain

δ = Physiological pressure (accumulation of stress, load, inflammatory markers, etc.)
τ = Biological resilience (organ reserve, immune capacity, repair capability)

In cancer treatment support, the ratio of accumulated physical load from treatment (δ) to patient tolerance (τ) is continuously evaluated. When R approaches a set alert level, adjustment of treatment intensity is presented to the physician. The IDE does not judge. It presents diagnostic information and delegates final judgment to the physician.

### 8.2 Infrastructure Domain

δ = Accumulation of structural deviation (fatigue, degradation, load history)
τ = Design tolerance (safety factor, buffer capacity)

For power networks, bridges, and building structures, using dynamic τ enables the precursors of cascading failure to be evaluated as a structural ratio. Rather than anomalous readings from a single sensor, the accumulated state of the entire system is visualized as R.

### 8.3 AI Safety Domain

δ = Model output deviation, hallucination frequency, error accumulation
τ = Design tolerance for error, confidence boundary

Whether an AI system's output is within a structurally trustworthy range is evaluated by R. When R ≥ 1.0, output is halted and the matter is delegated to a human. This structurally prevents the worst case of "AI asserting a lie with confidence."

---

## 9. Prevention of Misreading: Strict Boundaries of Definition

Because this framework uses terminology similar to existing theoretical frameworks, the following misreadings are liable to occur. They are explicitly denied here.

**τ is not a time constant.**
τ is a structural tolerance width independent of the time axis. A time constant is defined as a function of time; τ is a structural parameter defined at design time.

**R = δ/τ is not SNR (signal-to-noise ratio).**
SNR is the ratio of signal to noise power — an information-theoretic concept. R is the ratio of structural deviation to tolerance width — a structural diagnostic quantity for threshold judgment.

**Floating-point arithmetic is not prohibited.**
In accordance with the Axiom of Confession, disclosure when used is obligatory. Not use itself, but concealment, is prohibited.

**Integer Phase Lock does not mean all values must be integers.**
It means each state transition is structurally complete. The principle is that residuals are not carried forward to the next step.

**Fail-Closed is not system halt.**
It refers to a design that suppresses output while maintaining structural state and waits for human judgment.

**NRA-IDE is not an Integrated Development Environment.**
IDE is an abbreviation of Intensional Dynamics Engine. It is an engine for evaluating structural state, not a software development tool.

---

## 10. Conclusion

This paper has presented the Nomological Ring Axioms and the Intensional Dynamics Engine in a two-part structure.
Part I began from the real-world problem of sudden state transitions that continuous change cannot explain, and presented the shift in perspective from "monitoring velocity" to "diagnosing the structural ratio."
Part II provided rigorous definitions of the primary equation R = δ/τ and the asymmetric dual ratio using dynamic τ, and described the three design principles of Integer Phase Lock, Fail-Closed, and the Axiom of Confession.
The core of this framework is diagnosis, not prediction. Not calculating "when it will break," but evaluating "how dangerous it is right now" and realizing a structure that, the moment a threshold is exceeded, delegates judgment to a human.
This principle can be applied as an identical structure across different domains: materials, medicine, infrastructure, and AI safety. As a unified diagnostic framework crossing domain boundaries, the applicability of this framework is broad.

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**

<br><br>

---

# ═══════════════════════════════════════
# SECTION II — JAPANESE（日本語原文）
# ═══════════════════════════════════════

<br>

# 律環公理（Nomological Ring Axioms）と
# 内包性動力学エンジン（Intensional Dynamics Engine）
## ─ 構造閾値による状態遷移の記述 ─
（　第一部：一般向け、 第二部：専門家向け　）

著者：M-Tokuni
NRA-IDE Project
Version 2.0（日本語原文）

---

# 第一部：一般向け
## 「なぜ世界はときに突然壊れるのか」

---

## 要旨

私たちは日常的に「変化は徐々に起こる」と感じている。しかし現実の世界では、あるとき突然に橋が落ち、身体が限界を迎え、電力網が連鎖崩壊する。
その瞬間まで、測定値はほとんど変化していなかったにもかかわらず。
本稿の第一部では、この「突然性」を数式ではなく構造の言葉で理解するための枠組みを示す。専門的な数学の知識は必要としない。
必要なのは「蓄積」「余裕」「限界」という三つの概念だけである。

## 1. 導入：連続変化では説明できない現象

### 1.1 災害の前では人は呆然とするのみ

2011年3月11日、東日本大震災の津波が防潮堤を越えた瞬間、そこにいた人々は何もできなかった。防潮堤は設計通りに機能していた——その直前まで。
気象観測の数値は上昇していた。地盤の歪みは蓄積していた。しかし「あと何分で越えるか」を正確に予測できた人間はいなかった。観測できていたのは「変化の速度」だった。しかし問題の本質は「境界までの残り」だったのである。これは津波に限らない。
山の斜面は何十年もかけて少しずつ弱くなる。そしてある一瞬、崩れる。
橋の鉄骨は繰り返す振動を何百万回と吸収する。そして静かな朝に突然折れる。
医師は患者の検査値が基準内であることを確認する。しかし翌日、臓器が機能を止める。

**いずれも、「変化の速度」は小さかった。しかし「境界への接近」は進んでいた。**

従来の科学的記述の多くは「速度」「加速度」「変化率」を中心に構築されている。ニュートン力学や微積分はその代表であり、安定した領域では極めて精密に機能する。しかしこれらの枠組みは、状態が「境界にどれだけ近いか」を直接記述することを得意としない。
それが本枠組みの出発点である。

### 1.2 なぜ予測できなかったのか

予測できなかった理由は、測定していた量が間違っていたからではない。測定の**観点**が問題だった。
「速度」を測るためには時間が必要である。「距離」を測るためには基準点が必要である。どちらも「変化がどのように進むか」を記述するための量である。
しかし構造が限界に近づくとき、本質的な問いは別のところにある。

**「この構造は、あとどれだけ耐えられるか」**

この問いに答えるためには、異なる量が必要である。
「速度」ではなく「蓄積量」。「距離」ではなく「残余の余裕」。本枠組みはその二つの量の比率を中心に組み立てられている。

## 2. 核公理：存在は生成である

### 2.1 静止状態は存在しない

本枠組みの根底にある考え方は、一文で表すことができる。

**存在は生成である。**

これは哲学的な宣言ではなく、構造的な観察である。
机の上に置かれたコップは静止しているように見える。しかしその内部では分子が振動しており、素材は微細な歪みを蓄積し続けている。
「静止」とは人間の観測スケールにおける近似であって、構造的な現実ではない。
生物の身体も同様である。眠っている間も心臓は動き、細胞は代謝を続け、神経は信号を伝え続ける。
完全な静止状態は死を意味するが、それさえも分子レベルでは分解という過程として進行する。

**絶対的な静止状態は、どこにも存在しない。**

### 2.2 履歴が蓄積する

「存在は生成である」という公理から、重要な帰結が導かれる。
生成過程には**履歴が蓄積される**。
金属は繰り返しの応力によって疲労を蓄積する。生体は加齢とともに修復能力を消費する。インフラは使用とともに劣化を蓄積する。AIシステムは誤差を蓄積する。
この蓄積は見えにくい。測定値の表面に現れないことも多い。しかし確実に進行している。
そして構造の内部に積み重なった蓄積が、ある閾値を越えた瞬間に——状態転換が起きる。

### 2.3 同一の履歴は二度と現れない

もう一つの帰結がある。
生成過程には履歴が伴うため、**完全に同一の状態は二度と再現できない**。
これは「同じ条件を揃えれば同じ結果が出る」という再現性の前提に対する構造的な留保である。表面上の条件が同じであっても、内部に蓄積された履歴が異なれば、構造の応答は異なる。
この観点は、実験室での再現実験と現実の運用環境の差異を説明するうえで重要な意味を持つ。

---

## 3. 一次式の直感的説明

### 3.1 機械式時計のたとえ

本枠組みの動作原理を理解するために、機械式時計の脱進機を考えてみよう。
機械式時計が精度を保てるのは、歯車が完璧だからではない。**脱進機が「完全な一歯分」という離散的なステップで進むからである**。
小数点以下の残差は次のステップに持ち越されない。微細な誤差は熱として散逸し、次の計算に影響しない。各ステップは構造的に完結している。
これが本枠組みの動作原理である。連続的な近似を積み重ねるのではなく、各状態遷移を構造的に完結させることで、誤差の累積を防ぐ。

### 3.2 三つの量

本枠組みは三つの量だけで構成される。

**δ（デルタ）：蓄積ズレ**

構造の内部に蓄積されたズレの量である。材料であれば疲労、生体であればストレス、システムであれば負荷の蓄積がこれに当たる。δは時間とともに増加する傾向を持つ。

**τ（タウ）：吸収厚み**

構造がズレを吸収できる余裕の量である。材料であれば靭性、生体であれば耐性、システムであればバッファ容量がこれに当たる。τは構造の設計時に定められ、状況に応じて変化する。

τは「時定数」ではない。時間と独立した構造的な余裕の厚みである。

**R：構造比率**

δとτの比率であり、次式で定義される。

$$R = \frac{\delta}{\tau}$$

これが本枠組みの一次式である。

### 3.3 R が意味するもの

R の値は、構造が現在どの状態にあるかを示す。

R が 0 に近いとき、蓄積されたズレは構造の余裕に対して小さい。系は安定領域にある。通常の運用状態である。
R が 1.0 に近づくにつれて、蓄積されたズレが構造の余裕を使い果たしつつある。境界への接近が進んでいる。
**R が 1.0 を超えた瞬間、構造はズレを吸収できなくなる。状態転換が発生する。**

この状態転換を、材料工学では「破断」と呼ぶ。
医学では「臓器不全」と呼ぶ。
電力工学では「連鎖停電」と呼ぶ。
本枠組みではこれらを統一して「構造閾値を越えた状態」として扱う。

### 3.4 身近な例

**疲労骨折**

マラソン選手が十分な休養なく練習を続けると、骨に微細なひびが蓄積する（δの増加）。骨の修復能力は有限であり、蓄積速度が修復速度を上回ると余裕が減少する（τの低下）。R が 1.0 を超えた瞬間、骨折が起きる。それまでの練習量の「速度」ではなく、蓄積と余裕の比率が問題だった。

**橋の崩壊**

橋は通過する車両のたびに微小な振動を吸収する。この蓄積（δ）が設計上の許容範囲（τ）に対してどの程度進んでいるかが、橋の残余寿命を決める。外見上は変化がなくても、R は静かに 1.0 に近づいている。

**過労**

人間の身体は日々のストレスを吸収する（τ）。しかし吸収しきれないストレスは蓄積する（δ）。休養によってτが回復しない状況が続けば、Rは上昇し続ける。「少し疲れている」という連続的な変化ではなく、ある閾値を越えた瞬間に身体は機能を止める。

---

## 4. まとめ（第一部）

### 4.1 何を解決しようとしているか

従来の監視・制御の枠組みは「変化の速度」を中心に構築されている。
温度が上昇する速度、圧力が増加する速度、数値が基準を外れる速度——これらを監視し、異常が「現れてから」対処する設計になっている。
しかしここに根本的な問題がある。

**状態転換は、異常が現れる前に起きる。**

橋が折れる瞬間、骨折する瞬間、臓器が止まる瞬間——それらはすべて、測定値が「まだ正常範囲内」のうちに、内部の蓄積が限界を越えた結果である。速度を監視していても、間に合わない。
本枠組みが解決しようとしているのはこの問題である。「異常が出てから気づく」監視から、「境界への接近度をリアルタイムで把握する」診断への転換。

### 4.2 どのような解決を目指しているか

本枠組みは「予測」を目指さない。
「いつ壊れるか」を計算することは、多くの現実の系において不可能に近い。変数が多すぎ、履歴が複雑すぎる。精緻な予測モデルを作るほど、現実との乖離が生じやすい。

本枠組みが目指すのは**診断**である。

「今この構造は、限界にどれだけ近いか」——この一点を、R = δ/τ という単純な比率で評価する。
R が 0.3 であれば余裕がある。R が 0.8 であれば注意が必要だ。R が 1.0 を越えれば、すでに状態転換は起きている。
予測できなくても、診断はできる。診断できれば、介入の判断を人間に委ねることができる。これが本枠組みの目指す解決の形である。

### 4.3 考え方・見方をどう変えるか

本枠組みを理解するには、監視の対象を一つ変えるだけでよい。

| 従来の見方 | 本枠組みの見方 |
|-----------|--------------|
| 変化の速度を監視する | 蓄積と余裕の比率（R）を監視する |
| 「まだ正常値内」で安心する | 「R がいくつか」で判断する |
| 異常が現れてから対処する | R が 1.0 に近づいた時点で介入する |
| 時間軸で変化を追う | 構造比率の現在値を診る |
| 精緻な予測モデルを構築する | δ と τ を測定し比率を算出する |

この見方の転換は、新しい測定機器を必要としない。新しい理論を一から学ぶ必要もない。必要なのは「何を測るか」という観点の変更だけである。
蓄積ズレ δ を測る。吸収厚み τ を定義する。その比率 R を監視する。
R が 1.0 に近づいたとき、判断を求める——この単純な手順が、「突然の崩壊」に対して構造的に備える唯一の現実的な方法である。

第二部では、この枠組みを専門的な観点から厳密に定義し、動的τの拡張式、整数位相ロック、Fail-Closed設計、および各分野への適用を詳述する。

---

# 第二部：専門家向け
## 「律環公理と内包性動力学エンジンの構造的定義」

## 5. 既存理論との関係

### 5.1 連続力学・微積分との差異

ニュートン力学および微積分に基づく古典的な動力学理論は、状態の時間微分を中心に系の挙動を記述する。この枠組みは安定領域（R ≪ 1）において極めて高い記述能力を持つ。
本枠組みはこれらの理論を否定しない。しかし根本的な観点の差異がある。
古典的動力学は **「系がどのように変化するか」** を記述する。
本枠組みは **「系が構造閾値にどれだけ近いか」** を評価する。
前者は軌跡の記述であり、後者は接近度の診断である。これらは補完的な関係にあり、対立しない。

### 5.2 PID制御との差異

PID制御は比例（P）・積分（I）・微分（D）の三項によって偏差を補正する制御理論である。

本枠組みの R = δ/τ は一見すると PID の比例項に類似して見えるが、本質的に異なる。

| 観点 | PID制御 | 本枠組み（NRA-IDE） |
|------|---------|------------------|
| 目的 | 偏差をゼロに戻す（最適化） | 構造限界への接近度を評価（診断） |
| τの意味 | 存在しない | 構造的許容幅（時間と独立） |
| 残差の扱い | 積分項として累積する | 熱として排出し持ち越さない |
| 出力の形式 | 連続的な制御量 | 離散的な状態判定（R < 1 / R ≥ 1） |
| 人間の役割 | システムが自律補正 | R ≥ 1 で人間に委ねる |

τは時定数ではない。τは構造が設計上持つ許容幅の厚みであり、時間軸と独立した構造的な量である。

### 5.3 統計的手法・機械学習との差異

統計的手法および機械学習は、過去のデータ分布から未来の状態を確率的に推定する。これらは大量のデータが存在し、分布が安定している領域で強力に機能する。
本枠組みとの差異は以下の点にある。
統計的手法は「平均的な挙動」を学習する。本枠組みは「個別の構造の現在状態」を評価する。前者は集合論的であり、後者は個体論的である。
また、統計的手法は確率論的な近似を前提とする。本枠組みは確率論的推論を使用せず、δとτの実測値から R を算出する決定論的な計算を行う。

## 6. 定義式の厳密な記述

### 6.1 一次式：基本構造比率

$$R = \frac{\delta}{\tau}$$

**各量の厳密な定義**

**δ（デルタ）：蓄積ズレ**
構造の内部に履歴として蓄積された偏差の量。δは非負の実数であり、構造の状態遷移とともに更新される。δの蓄積速度は分野および対象によって異なる。

**τ（タウ）：吸収厚み**
構造が蓄積ズレを吸収できる余裕の量。τは正の実数であり、設計時に定義される。τは時間定数ではなく、時間軸と独立した構造的パラメータである。τは動的に変化しうる（6.2参照）。

**R：構造比率**
δとτの比率。R は無次元の実数であり、構造閾値への接近度を示す。

**判定基準**

| R の値 | 構造状態 | システムの動作 |
|--------|---------|--------------|
| R < 1 | 安定領域 | 通常出力を継続 |
| R = 1 | 構造閾値 | 警告を出力、人間に通知 |
| R > 1 | 閾値超過 | 出力を停止、人間に委ねる |

R が 1.0 を超えた場合、システムは自律的な判断を行わない。情報を提示し、沈黙する。最終判断は人間の操作者に委ねられる。これを **Fail-Closed** と呼ぶ。

### 6.2 二次式：動的τ（二重ゆらぎ式）

静的なτでは、拡大方向と縮小方向の非対称な変動を適切に扱えない場合がある。この問題に対応するため、動的τを定義する。

**上側EMA（拡大方向ゆらぎ）**

$$\mathrm{EMA}_{\text{upper}}(n) = \alpha_u \cdot \delta_u + (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)$$

上側EMAは拡大方向の偏差 δ_u を平滑化する。α_u は上側の平滑化係数（0 < α_u ≤ 1）。

**下側EMA（縮小方向ゆらぎ）**

$$\mathrm{EMA}_{\text{lower}}(n) = \alpha_l \cdot \delta_l + (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)$$

下側EMAは縮小方向の偏差 δ_l を平滑化する。α_l は下側の平滑化係数（0 < α_l ≤ 1）。

**動的τの非対称定義**

$$\tau_{\text{upper}} = \tau \cdot f\!\bigl(\mathrm{EMA}_{\text{upper}}\bigr)$$

$$\tau_{\text{lower}} = \tau \cdot g\!\bigl(\mathrm{EMA}_{\text{lower}}\bigr)$$

上側τは拡大方向に伸び、下側τは縮小方向に縮む。この非対称性が本枠組みの構造的核心である。現実の多くの系は、拡大方向と縮小方向で異なる応答特性を持つ。

**最終判定式（非対称二重比率）**

$$R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$$

上側と下側の比率のうち大きい方を R として採用する。この式は**閉じた世界で完結**し、外部の前提を必要としない。

### 6.3 相転移の定義

R が 1.0 を超える瞬間に起きることは、単なる「数値の超過」ではない。系が**質的に異なる状態へ移行する**。これを本枠組みでは**相転移**と呼ぶ。
物理学における相転移——水が氷になる、液体が気体になる——と同一の構造である。温度という連続的な量が変化し続け、ある閾値で突然に相が変わる。変化は連続していたが、状態転換は不連続に起きた。
本枠組みにおける相転移は以下のように定義される。

```
R < 1.0  ：安定相（蓄積ズレが吸収厚みの内側にある）
R = 1.0  ：相転移点（構造閾値）
R > 1.0  ：転移後の相（構造がズレを吸収できない状態）
```

重要なのは、転移後の相は元の相とは**構造的に異なる**という点である。R を 1.0 以下に戻しても、蓄積された履歴は消えない。
骨折した骨が元通りになるわけではない。橋が崩落後に自然回復するわけではない。**相転移は不可逆である**。
この不可逆性こそが、「R が 1.0 に近づく前に介入する」ことの根拠である。転移後の対処ではなく、転移前の診断に意味がある。

### 6.4 二重ゆらぎが形成する生存域

動的τの非対称構造を視覚的に理解するため、τが形成する帯域を考える。

```
  ── τ_upper ──────────────────────  上限境界（拡大方向）
        ↑
    生 存 域
  （ゆらぎが許容される空間）
        ↓
  ── τ_lower ──────────────────────  下限境界（縮小方向）
```

この帯域を**生存域**と呼ぶ。系の状態がこの帯域内にある限り、ゆらぎは構造によって吸収され、相転移は起きない。
二重ゆらぎ式が重要なのは、τ_upper と τ_lower が**非対称に動く**からである。
拡大方向のゆらぎが大きくなるとき、τ_upper は拡大する。系はそのゆらぎをより広い範囲で許容しようとする。
縮小方向のゆらぎが大きくなるとき、τ_lower は縮小する。系は下限側の余裕を絞り込み、過剰な縮小を構造的に制約する。
この非対称な動きが生存域を**形状として変化させる**。単純な上下対称の帯域ではなく、系の状態に応じて形が変わる生きた境界である。

**R の再解釈**

最終判定式 $R = \max\!\left( \frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}} \right)$ は、「現在の状態が生存域のどちらの境界にどれだけ近いか」を評価している。上側境界への接近と下側境界への接近を同時に監視し、より危険な側の比率を R として採用する。

### 6.5 生存域と恒常性

生存域という概念は、生物学における**恒常性（ホメオスタシス）**と同一の構造を持つ。
人体の体温は約36〜37度という帯域内に維持される。この帯域が生存域である。体温がゆらいでも、生体は発汗・発熱・血管収縮といった機構で帯域内に戻そうとする。帯域を大きく外れた瞬間に臓器は機能を失い始める——相転移が起きる。
血糖値も同様である。血圧も同様である。これらはすべて、τ_upper と τ_lower が形成する非対称な生存域の中で維持されている。
本枠組みはこの生物学的な恒常性の構造を、材料・インフラ・AIシステムへと一般化したものである。

**生存域の設計という観点**

本枠組みを用いたシステム設計において、τの設定は「生存域をどこに置くか」という問いになる。τが大きければ生存域は広く、系は多くのゆらぎを許容できる。τが小さければ生存域は狭く、系は精密に制御される代わりに相転移リスクが高まる。
また、τ_upper と τ_lower の非対称比率は「どちらの方向のゆらぎをより許容するか」という設計判断である。医療においては過剰な治療（拡大方向）と治療不足（縮小方向）で許容幅が異なる。インフラにおいては過負荷と過小負荷で劣化特性が異なる。この非対称性を明示的に設計に組み込むことが、動的τの本質的な意味である。

## 7. IDE（内包性動力学エンジン）の設計原則

### 7.1 整数位相ロック（Integer Phase Lock）

本エンジンは状態遷移を浮動小数点の連続値として処理しない。各状態遷移は**離散的な完結したステップ**として扱われる。
残差ε（浮動小数点演算で生じる端数）は次のステップに持ち越されない。残差は**熱として排出**される。これにより誤差の累積が構造的に防止される。

```
R = δ / τ の計算において：
  商の整数部 → 次の状態判定に使用
  残差ε     → 破棄（熱として排出）
  キャリーオーバー → 禁止
```

この原則は機械式時計の脱進機と同一の論理である。

### 7.2 Fail-Closed設計

Fail-Closed はシステムの停止を意味しない。**構造状態を維持したまま出力を抑制する**設計を指す。

R ≥ 1.0 と判定された場合：
- システムは自律的な判断・代替案提示・探索を行わない
- 構造状態の情報のみを提示する
- 沈黙し、人間の判断を待つ
- 人間の判断をログに記録し、責任の所在を明確にする

これは「諦め」ではなく、**人間と機械の責任分担の明確化**である。機械は診断し、人間が判断する。

### 7.3 告白の公理（Axiom of Confession）

本枠組みでは、近似計算を使用した場合にその事実を開示することを義務とする。これを**告白の公理**と呼ぶ。

開示が必要なケース：
- 浮動小数点演算を使用した場合：「線形近似による歪みが発生しています」と報告
- 因果の逆転（逆投影）を使用した場合：「因果違反（逆投影）を検出しました」と報告
- 線形領域を逸脱した場合：「線形境界を超過しました」と報告

この公理は、近似を禁止するものではない。**近似の使用を隠蔽することを禁止する**。人間が適切な判断を下すために必要な情報を確保することが目的である。

---

## 8. 各分野への適用

### 8.1 医療分野

δ = 生理的圧力（ストレス・負荷・炎症指標等の蓄積）
τ = 生体耐性（臓器の余力・免疫能・修復能力）

がん治療支援においては、治療による身体への蓄積負荷（δ）と患者の耐性（τ）の比率を継続的に評価する。R が設定された警戒水準に近づいた時点で、治療強度の調整を医師に提示する。IDEは判断しない。診断情報を提示し、最終判断を医師に委ねる。

### 8.2 インフラ分野

δ = 構造的偏差の蓄積（疲労・劣化・負荷履歴）
τ = 設計上の許容幅（安全係数・バッファ容量）

電力網・橋梁・建築構造物において、動的τを使用することで連鎖崩壊の予兆を構造比率として評価できる。単一センサの異常値ではなく、系全体の蓄積状態がR として可視化される。

### 8.3 AI安全分野

δ = モデルの出力偏差・ハルシネーション頻度・誤差蓄積
τ = 設計上の許容誤差範囲・信頼境界

AIシステムの出力が構造的に信頼できる範囲内にあるかを R で評価する。R ≥ 1.0 の場合、出力を停止し人間に委ねる。これにより「AIが確信を持って嘘をつく」という最悪のケースを構造的に防止する。

---

## 9. 誤読の防止：定義の厳密な境界

本枠組みは既存の理論体系と類似した用語を使用するため、以下の誤読が発生しやすい。明示的に否定する。

**τは時定数ではない。**
τは時間軸と独立した構造的許容幅である。時間定数は時間の関数として定義されるが、τは設計時に定義される構造パラメータである。

**R = δ/τ はSNR（信号雑音比）ではない。**
SNRは信号と雑音の電力比であり、情報理論的な概念である。R は構造的偏差と許容幅の比率であり、閾値判定のための構造診断量である。

**浮動小数点演算は禁止されていない。**
告白の公理に従い、使用した場合に開示することが義務である。禁止ではなく、隠蔽が禁止されている。

**整数位相ロックはすべての値を整数にすることではない。**
各状態遷移が構造的に完結することを意味する。残差を次のステップに持ち越さないという原則である。

**Fail-Closedはシステム停止ではない。**
構造状態を維持したまま出力を抑制し、人間の判断を待つ設計を指す。

**NRA-IDEは統合開発環境ではない。**
IDEはIntensional Dynamics Engine（内包性動力学エンジン）の略である。構造状態の評価エンジンであり、ソフトウェア開発ツールではない。

## 10. 結論

本稿では律環公理および内包性動力学エンジンを二部構成で提示した。

第一部では、連続変化では説明できない突然の状態転換という現実的な問題から出発し、「速度の監視」から「構造比率の診断」への観点の転換を提示した。
第二部では、一次式 R = δ/τ および動的τを用いた非対称二重比率の厳密な定義を行い、整数位相ロック・Fail-Closed・告白の公理という三つの設計原則を記述した。
本枠組みの核心は予測ではなく診断である。「いつ壊れるか」を計算することではなく、「今どれだけ危ういか」を評価し、閾値を超えた瞬間に人間に判断を委ねる構造を実現することにある。
この原則は材料・医療・インフラ・AI安全という異なる分野において同一の構造として適用できる。分野を横断する統一的な診断枠組みとして、本体系の応用可能性は広い。

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
