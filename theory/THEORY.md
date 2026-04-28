# Nomological Ring Axioms / Intensional Dynamics Engine



# 律環公理 / 内包性動力学エンジン



<!-- THEORY.md | updated 2026-04-07 19:14 JST -->



---



# Part I — Core Text（本文）



## Core Axiom / 核公理



### 日本語（原文）



存在は生成である



### English



Existence is Generation.



---



## Fundamental Structure / 基本構造



### 日本語



本体系は存在を固定された実体として扱わない。

存在は状態遷移として現れる。



時間は独立した原因変数として扱わない。

時間は状態遷移の順序として現れる。



距離は因果を生む量として扱わない。

距離は状態変化の観測結果として記述される。



---



### English



This framework does not treat existence as a fixed entity.

Existence appears through state transition.



Time is not treated as an independent causal variable.

Time appears as the ordering of state transitions.



Distance is not treated as a causal driver.

Distance is recorded as an observation of state change.



---



## Structural Ratio / 構造比率



### 日本語



構造状態は次の比率によって判定される。



$$R = \frac{\delta}{\tau}$$



δ : 制約からの偏差

τ : 許容境界（厚み）



R ≥ 1 の場合、構造限界に達したと判定する。



このときシステムは出力を停止し、

最終判断は人間に委ねられる。



---



### English



Structural state is evaluated using the ratio:



$$R = \frac{\delta}{\tau}$$



δ : deviation from constraint

τ : tolerance boundary thickness



When R ≥ 1, the structural limit is reached.



At this point the system ceases output,

and final judgment is delegated to a human operator.



---



## Dynamic τ — Dual-Fluctuation / 動的τ（二重ゆらぎ式）



### 日本語



静的τでは捉えられない非対称な変動に対応するため、動的τを定義する。



$$\mathrm{EMA}_{\text{upper}}(n) = \alpha_u \cdot \delta_u + (1 - \alpha_u) \cdot \mathrm{EMA}_{\text{upper}}(n-1)$$



$$\mathrm{EMA}_{\text{lower}}(n) = \alpha_l \cdot \delta_l + (1 - \alpha_l) \cdot \mathrm{EMA}_{\text{lower}}(n-1)$$



$$\tau_{\text{upper}} = \tau \cdot f\!\bigl(\mathrm{EMA}_{\text{upper}}\bigr) \quad \tau_{\text{lower}} = \tau \cdot g\!\bigl(\mathrm{EMA}_{\text{lower}}\bigr)$$



$$R = \max\!\left(\frac{\delta_{\text{upper}}}{\tau_{\text{upper}}},\ \frac{\delta_{\text{lower}}}{\tau_{\text{lower}}}\right)$$



上側τは拡大し、下側τは縮小する。

この非対称性が本体系の構造的核心である。

この式は閉じた世界で完結し、外部の前提を必要としない。



---



### English



To handle asymmetric fluctuations that a static τ cannot capture,

dynamic τ is defined as above.



The upper τ expands; the lower τ contracts.

This asymmetry is the structural core of this framework.

The formula is self-contained and requires no external assumptions.



---



## Applied Formula — Hybrid Complement / 応用式（ハイブリッド補完）



### 日本語



二重ゆらぎ式が持つ EMA ラグ（追従遅れ）を補完するために、

古典計算層を補助的に組み合わせる。



$$\frac{d^2x}{dt^2} + \gamma\dot{x} = \underbrace{F_{\text{IDE}}(x)}_{\text{根本・全域}} + \underbrace{G(r) \cdot \Phi(x)}_{\text{古典層・補助}}$$



$$G(r) = r \cdot \frac{|r|}{k + |r|} \quad,\quad r = x_{\text{exact}} - x$$



G(r) は 2 次残差ゲートである。

r が小さければ G ≈ 0（沈黙）。

r が大きければ飽和応答（補正）。



古典層は補助である。IDE 項 F_IDE は常に全域で動く。

k（knee 値）一点の調整で、補正の精度と範囲を連続的に変えられる。



---



### English



To compensate for EMA lag in the dual-fluctuation formula,

a classical computation layer is combined as an auxiliary.



G(r) is a second-order residual gate.

When r is small, G ≈ 0 (silence).

When r is large, a saturating response applies the correction.



The classical layer is auxiliary only.

The IDE term F_IDE operates at all times across the full domain.

A single parameter k (knee) continuously adjusts correction strength.



See → [FORMULA.md](../FORMULA.md) for complete equation definitions.

See → [nra-core/](../nra-core/) for architecture implementation detail.



---



## Intensional Dynamics Engine / 内包性動力学エンジン



### 日本語



IDE は律環公理を実装する計算エンジンである。



IDE は意味生成を担当しない。

IDE は構造状態の評価を担当する。



---



### English



The Intensional Dynamics Engine (IDE)

implements the Nomological Ring Axioms.



IDE does not perform meaning generation.

IDE evaluates structural state.



---



# Part II — Explanatory Notes（説明）



## Generation / 生成



### 日本語



ここでいう生成とは無からの創造を意味しない。

存在が状態遷移として現れることを指す。



### English



Generation does not mean creation from nothing.

It refers to the appearance of existence through state transition.



---



## Time / 時間



### 日本語



本体系は時間の存在を否定しない。

ただし時間を独立した原因変数として入力しない。



時間は状態遷移の順序として記述される。



### English



This framework does not deny the existence of time.

However, time is not used as an independent causal variable.



Time is described as the ordering of state transitions.



---



## Distance / 距離



### 日本語



距離の有用性を否定するものではない。

ただし距離を因果の駆動因子として扱わない。



距離は状態変化の観測結果として記述される。



### English



The usefulness of distance is not denied.

However, distance is not treated as a causal driver.



Distance is recorded as an observation of state change.



---



## Tension / 張力



### 日本語



ここでいう張力とは制約境界から生じる復元的傾向を指す。

場合によっては物理的張力として現れることもある。



本体系ではより一般的な構造概念として用いる。



### English



"Tension" refers to the restoring tendency arising from constraint boundaries.

In some cases this may correspond to a physical force.



In this framework the term is used in a broader structural sense.



---



## Optimization / 最適化



### 日本語



本体系は最適化一般を否定しない。

ただしIDEの判定は目的関数最大化ではない。



IDEは構造閾値への接近度を評価する。



### English



This framework does not deny optimization in general.

However, IDE decisions are not based on objective maximization.



IDE evaluates proximity to structural thresholds.



---



## Fail-Closed



### 日本語



Fail-Closed はシステム停止を意味しない。

構造状態を維持したまま出力を抑制する設計を指す。



### English



Fail-Closed does not mean system halt.

It refers to suppressing output while maintaining structural continuity.



---



## Hybrid Complement — Design Note / ハイブリッド補完の設計注記



### 日本語



応用式は定義式 2（動的τ）の拡張であり、代替ではない。



定義式 2 は完結した閉じた式である。

応用式はその精度限界を外部補助で補う構造である。



量子 IDE 層は根本を手放さない。

古典層は「助言」として入力するにとどまる。

この役割分担は NRA-IDE の相互補完原則の計算層での再現である。



### English



The applied formula extends Definition 2 (dynamic τ); it does not replace it.



Definition 2 is a self-contained closed formula.

The applied formula supplements its precision limits through external auxiliary computation.



The quantum IDE layer never yields its foundation.

The classical layer contributes only as "advice."

This role separation is the natural realization of the NRA-IDE complementarity principle

at the computational architecture level.



---



**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**

