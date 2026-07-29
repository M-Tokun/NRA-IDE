# NRA-IDE 定義式 / NRA-IDE Formal Equations

**Version:** 2.0  
**Author:** M-Tokuni  
**Document role:** Mathematical and computational definitions subordinate to `theory/AXIOMS.md` and `theory/axioms.json`

---

## 0. 文書の役割 / Document Scope

この文書は、NRA-IDEで使用する式、変数、定義域、初期条件、差分条件、数値安定条件を定める。

律環公理は「存在は生成である。」の一つだけであり、第二公理以降は存在しない。本書の一次式と二次式は、公理ではなくIDEの二つの正規計算系である。それ以外の式は、派生式、補助式または補完式として扱う。分類と意味が衝突する場合は、`theory/AXIOMS.md`および機械可読な同期表現`theory/axioms.json`を優先する。

安全工学上の運用判断、権限移譲、出力制御、監査規則は本書の対象外とする。

This document defines the equations, variables, domains, initial conditions, difference conditions, and numerical-stability requirements used in NRA-IDE.

There is exactly one Nomological Ring Axiom: “Existence is Generation.” No second or subsequent axiom exists. The Primary and Secondary Formulas in this document are the two canonical IDE calculation systems, not axioms. Every other equation is treated as a derived, auxiliary, or complementary formula. If classification or meaning conflicts, `theory/AXIOMS.md` and its machine-readable synchronized representation `theory/axioms.json` take precedence.

Operational safety judgment, authority transfer, output control, and audit rules are outside the scope of this document.

ただし、本式で評価する対象は計算開始前に一意に宣言する。`R_target >= 1.0` はその対象構造の完全破断境界を表し、センサー、ロガー、通信経路または外部監査系の破断を自動的には表さない。各経路の生存状態は本式とは別に記録する。

The evaluation target must nevertheless be declared unambiguously before computation. `R_target >= 1.0` denotes the complete-rupture boundary of that target structure; it does not automatically denote rupture of a sensor, logger, communication path, or external audit system. Survival of each path is recorded separately from this formula.

---

# 1. 一次式（基本境界式）  
# 1. Primary Formula — Basic Boundary Formula

一次式は第一公理ではなく、IDEの第一の正規計算系である。

The Primary Formula is not a first axiom; it is the first canonical IDE calculation system.

$$
R = \frac{\delta}{\tau}
$$

### 変数定義 / Variable Definitions

- $\delta$ ：蓄積ズレ  
- $\tau$ ：吸収厚み  
- $R$ ：境界接近比  

- $\delta$: accumulated deviation  
- $\tau$: absorption thickness  
- $R$: boundary-approach ratio  

### 定義域 / Domain

$$
\delta \ge 0
$$

$$
\tau > 0
$$

$$
\delta,\tau \in \mathbb{R}
$$

かつ、 $\delta$ と $\tau$ は有限値でなければならない。

Both $\delta$ and $\tau$ must be finite.

$$
\tau = 0
\Rightarrow
R\ \text{is undefined}
$$

$\tau=0$ を無限大の $R$ へ置換してはならない。

When $\tau=0$, $R$ must not be replaced by infinity.

---

# 2. 残余余白
# 2. Remaining Margins

$$
M_R = 1-R
$$

- $M_R$ ：残存比率余白（無次元）
- $M_R$: remaining ratio margin (dimensionless)

$$
M_{\tau} = \tau - \delta
$$

- $M_{\tau}$ ：残存吸収余白（ $\delta$ および $\tau$ と同じ単位）
- $M_{\tau}$: remaining absorption margin (same unit as $\delta$ and $\tau$)

一次式との関係は次である。

$$
R = 1 - M_R
$$

また、

$$
M_{\tau} = \tau M_R = \tau(1-R)
$$

適用条件：

$$
\tau > 0
$$

---

# 3. 派生計算式：構造感度  
# 3. Derived Formula — Structural Sensitivity

$$
S =
\frac{1}{M_{\tau}}
$$

したがって、

$$
S =
\frac{1}{\tau-\delta}
$$

一次式を用いると、

$$
S =
\frac{1}{\tau(1-R)}
$$

### 定義域 / Domain

$$
\tau > 0
$$

$$
R < 1.0
$$

$$
\tau-\delta > 0
$$

### 極限 / Limit

$$
R \to 1.0^{-}
\Rightarrow
S \to \infty
$$

$S$ は単位付きの残存吸収余白 $M_{\tau}$ の逆数である。無次元の $M_R$ の逆数ではない。

$S$ is the inverse of the dimensional remaining absorption margin $M_{\tau}$, not the inverse of dimensionless $M_R$.

---

# 4. 二次式（二重ゆらぎ式）  
# 4. Secondary Formula — Dual-Fluctuation Formula

二次式は第二公理ではなく、IDEの第二の正規計算系である。その正規核は、上側・下側の蓄積ズレ、側別境界接近比、および二重ゆらぎ検出条件から成る。4.2から4.4のEMA、初期条件、形状変換関数は、評価前に固定する補助的実現であり、それ自体を公理または独立した正規式へ昇格させてはならない。4.6の集約量も補助量である。

The Secondary Formula is not a second axiom; it is the second canonical IDE calculation system. Its canonical core consists of upper/lower accumulated deviations, side-specific boundary-approach ratios, and the double-fluctuation detection condition. The EMA, initial conditions, and shape-transformation functions in 4.2–4.4 are auxiliary realizations fixed before evaluation; they must not be elevated into axioms or independent canonical formulas. The aggregate in 4.6 is auxiliary as well.

## 4.1 上側・下側蓄積ズレ  
## 4.1 Upper-Side and Lower-Side Accumulated Deviation

$$
\delta_{\mathrm{upper}}(n) \ge 0
$$

$$
\delta_{\mathrm{lower}}(n) \ge 0
$$

$\delta_{\mathrm{upper}}$ は、基準から上側方向へ生じたCause-Side蓄積ズレ成分である。

$\delta_{\mathrm{lower}}$ は、基準から下側方向へ生じたCause-Side蓄積ズレ成分である。

$\delta_{\mathrm{upper}}$ is the Cause-Side accumulated-deviation component in the upper direction from the reference state.

$\delta_{\mathrm{lower}}$ is the Cause-Side accumulated-deviation component in the lower direction from the reference state.

上側・下側という名称は方向を示す。危険・安全を自動的に意味しない。

The labels upper and lower indicate direction only. They do not automatically mean dangerous or safe.

---

## 4.2 非対称EMA  
## 4.2 Asymmetric EMA

$$
\mathrm{EMA}_{\mathrm{upper}}(n) =
\alpha_u\delta_{\mathrm{upper}}(n)
+
(1-\alpha_u)\mathrm{EMA}_{\mathrm{upper}}(n-1)
$$

$$
\mathrm{EMA}_{\mathrm{lower}}(n) =
\alpha_l\delta_{\mathrm{lower}}(n)
+
(1-\alpha_l)\mathrm{EMA}_{\mathrm{lower}}(n-1)
$$

### 平滑係数 / Smoothing Coefficients

$$
0 < \alpha_u \le 1
$$

$$
0 < \alpha_l \le 1
$$

$\alpha_u$ と $\alpha_l$ は独立に設定できる。

$\alpha_u$ and $\alpha_l$ may be set independently.

---

## 4.3 初期条件  
## 4.3 Initial Conditions

標準初期条件は次とする。

$$
\mathrm{EMA}_{\mathrm{upper}}(0) =
\delta_{\mathrm{upper}}(0)
$$

$$
\mathrm{EMA}_{\mathrm{lower}}(0) =
\delta_{\mathrm{lower}}(0)
$$

領域固有の初期値を使用する場合、その値と取得規則を計算開始前に固定する。

When domain-specific initial values are used, both the values and their acquisition rules must be fixed before computation begins.

---

## 4.4 側別有効ゲート幅  
## 4.4 Side-Specific Effective Gate Widths

$$
\tau_{\mathrm{upper}}(n) =
\tau(n)
h_{\mathrm{upper}}\!\left(
\mathrm{EMA}_{\mathrm{upper}}(n)
\right)
$$

$$
\tau_{\mathrm{lower}}(n) =
\tau(n)
h_{\mathrm{lower}}\!\left(
\mathrm{EMA}_{\mathrm{lower}}(n)
\right)
$$

$h_{\mathrm{upper}}$ と $h_{\mathrm{lower}}$ は、評価開始前に固定された側別形状変換関数である。

$h_{\mathrm{upper}}$ and $h_{\mathrm{lower}}$ are directional shape-transformation functions fixed before evaluation begins.

### 必須条件 / Required Conditions

$$
h_{\mathrm{upper}}(x) > 0
$$

$$
h_{\mathrm{lower}}(x) > 0
$$

したがって、

$$
\tau_{\mathrm{upper}} > 0
$$

$$
\tau_{\mathrm{lower}} > 0
$$

$\tau_{\mathrm{upper}}$ と $\tau_{\mathrm{lower}}$ は、動的評価に用いる側別有効ゲート幅である。

これらは、基礎吸収厚み $\tau$ そのものの自然回復を意味しない。

$\tau_{\mathrm{upper}}$ and $\tau_{\mathrm{lower}}$ are side-specific effective gate widths used for dynamic evaluation.

They do not mean that the underlying absorption thickness $\tau$ has naturally recovered.

---

## 4.5 側別境界接近比  
## 4.5 Side-Specific Boundary-Approach Ratios

$$
R_{\mathrm{upper}} =
\frac{\delta_{\mathrm{upper}}}
{\tau_{\mathrm{upper}}}
$$

$$
R_{\mathrm{lower}} =
\frac{\delta_{\mathrm{lower}}}
{\tau_{\mathrm{lower}}}
$$

### 定義域 / Domain

$$
\tau_{\mathrm{upper}} > 0
$$

$$
\tau_{\mathrm{lower}} > 0
$$

すべての入力値および中間値は有限でなければならない。

All input and intermediate values must be finite.

---

## 4.6 側別補助集約
## 4.6 Directional Auxiliary Aggregate

$$
R_{\mathrm{dir}} =
\max
\left(
R_{\mathrm{upper}},
R_{\mathrm{lower}}
\right)
$$

展開形：

$$
R_{\mathrm{dir}} =
\max
\left(
\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}},
\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
\right)
$$

$R_{\mathrm{dir}}$ は側別評価の補助集約量であり、正規の境界接近比 $R=\delta/\tau$ ではない。

$R_{\mathrm{dir}}$ を正規状態分類へ接続する場合、評価前に固定されたCause-Sideのドメイン変換規則によって、正規の $\delta$ と $\tau$ を定めなければならない。

$R_{\mathrm{dir}}$ is an auxiliary aggregate for directional evaluation, not the canonical boundary-approach ratio $R=\delta/\tau$.

To connect $R_{\mathrm{dir}}$ to canonical state classification, a Cause-Side domain transformation rule fixed before evaluation must determine the canonical $\delta$ and $\tau$.

支配側は次で定義する。

$$
D =
\operatorname*{arg\,max}
\left\{
R_{\mathrm{upper}},
R_{\mathrm{lower}}
\right\}
$$

- $D=\mathrm{upper}$ ：上側が支配  
- $D=\mathrm{lower}$ ：下側が支配  
- $R_{\mathrm{upper}}=R_{\mathrm{lower}}$ ：同率支配  

---

## 4.7 二重ゆらぎ検出条件  
## 4.7 Double-Fluctuation Detection Condition

連続時間表現：

$$
\frac{d\delta}{dt} > 0
\quad\land\quad
\frac{d\tau}{dt} < 0
$$

離散時間表現：

$$
\Delta\delta_n =
\delta_n-\delta_{n-1}
$$

$$
\Delta\tau_n =
\tau_n-\tau_{n-1}
$$

$$
\Delta\delta_n > 0
\quad\land\quad
\Delta\tau_n < 0
$$

時間微分または差分は、直接観測値または事前固定された差分規則から計算する。

Time derivatives or finite differences must be computed from direct observations or a difference rule fixed in advance.

---

# 5. 補完式（ハイブリッド補完）  
# 5. Complementary Formula — Hybrid Complement

二重ゆらぎ式におけるEMAラグ、局所急変への追従遅れ、領域固有の精度限界を補うため、補助計算項を組み合わせる。

この補完式は公理ではなく、IDEの第三の正規計算系でもない。領域固有に採用・検証する派生的な補完モデルである。

An auxiliary computation term is combined to compensate for EMA lag, delayed tracking of local rapid change, and domain-specific precision limits.

This complementary formula is neither an axiom nor a third canonical IDE calculation system. It is a derived complementary model that must be adopted and validated for its domain.

$$
\frac{d^2x}{dt^2}
+
\gamma\frac{dx}{dt} =
F_{\mathrm{IDE}}(x)
+
G(r)\Phi(x)
$$

残差：

$$
r =
x_{\mathrm{exact}}-x
$$

二次残差ゲート：

$$
G(r) =
r\frac{|r|}{k+|r|}
$$

---

## 5.1 変数定義  
## 5.1 Variable Definitions

- $x$ ：現在の計算状態  
- $x_{\mathrm{exact}}$ ：由来と不確かさを記録した事前定義の高精度参照状態（絶対的真値を意味しない）
- $r$ ：参照状態との差  
- $\gamma$ ：減衰係数  
- $k$ ：knee値  
- $F_{\mathrm{IDE}}(x)$ ：領域固有の基礎動力学項（IDE一次式ではない）
- $\Phi(x)$ ：補助計算項  
- $G(r)$ ：二次残差ゲート  

- $x$: current computational state  
- $x_{\mathrm{exact}}$: predefined high-precision reference state with recorded provenance and uncertainty (not guaranteed absolute ground truth)
- $r$: residual relative to the reference state  
- $\gamma$: damping coefficient  
- $k$: knee value  
- $F_{\mathrm{IDE}}(x)$: domain-specific base-dynamics term (not the IDE Primary Formula)
- $\Phi(x)$: auxiliary computation term  
- $G(r)$: second-order residual gate  

---

## 5.2 パラメータ条件  
## 5.2 Parameter Conditions

$$
\gamma \ge 0
$$

$$
k > 0
$$

$x$ 、 $x_{\mathrm{exact}}$ 、 $r$ 、 $F_{\mathrm{IDE}}(x)$ 、 $\Phi(x)$ は有限値でなければならない。

$x$, $x_{\mathrm{exact}}$, $r$, $F_{\mathrm{IDE}}(x)$, and $\Phi(x)$ must be finite.

$x_{\mathrm{exact}}$ 、 $F_{\mathrm{IDE}}(x)$ 、 $\Phi(x)$ および各パラメータは、領域固有の根拠、適用範囲、不確かさ、検証方法を計算開始前に固定し、追跡可能にしなければならない。

For $x_{\mathrm{exact}}$, $F_{\mathrm{IDE}}(x)$, $\Phi(x)$, and each parameter, domain-specific evidence, applicability, uncertainty, and validation method must be fixed before computation and remain traceable.

---

## 5.3 小残差領域  
## 5.3 Small-Residual Region

$$
|r| \ll k
$$

このとき、

$$
G(r)
\approx
\frac{r|r|}{k}
$$

したがって、 $G(r)$ は $r$ に対して二次的に小さくなる。

Therefore, $G(r)$ becomes second-order small with respect to $r$.

---

## 5.4 大残差領域  
## 5.4 Large-Residual Region

$$
|r| \gg k
$$

このとき、

$$
G(r) =
\frac{r}{1+k/|r|}
$$

したがって、

$$
\lim_{|r|/k\to\infty}\frac{G(r)}{r}=1
$$

すなわち、

$$
G(r)\sim r
$$

$G(r)$ は奇関数であり、 $r$ の符号を保持する。大残差で有界値へ飽和せず、漸近的に線形かつ非有界である。

$G(r)$ is odd and preserves the sign of $r$. For large residuals it is asymptotically linear and unbounded; it does not saturate to a bounded value.

---

## 5.5 knee値  
## 5.5 Knee Value

$$
|r| = k
$$

の近傍は、小残差の二次応答と大残差の漸近線形応答の遷移領域である。

The neighborhood of $|r|=k$ is the transition region between the quadratic small-residual response and the asymptotically linear large-residual response.

---

## 5.6 初期条件  
## 5.6 Initial Conditions

二階微分方程式を解くため、少なくとも次を与える。

$$
x(0)=x_0
$$

$$
\dot{x}(0)=v_0
$$

$x_0$ と $v_0$ は計算開始前に固定する。

$x_0$ and $v_0$ must be fixed before computation begins.

---

## 5.7 数値積分条件  
## 5.7 Numerical Integration Conditions

数値積分を用いる場合、次を事前固定する。

- 積分法  
- 時間刻み $\Delta t$  
- 最大反復回数  
- 収束判定  
- 発散判定  
- 非有限値の処理  
- 丸め規則  
- 計算精度  

When numerical integration is used, the following must be fixed in advance:

- integration method  
- time step $\Delta t$  
- maximum iteration count  
- convergence criterion  
- divergence criterion  
- handling of non-finite values  
- rounding rule  
- computational precision  

---

## 5.8 数値安定条件  
## 5.8 Numerical-Stability Conditions

各計算ステップで次を確認する。

$$
x_n \in \mathbb{R}
$$

$$
\dot{x}_n \in \mathbb{R}
$$

$$
r_n \in \mathbb{R}
$$

$$
G(r_n) \in \mathbb{R}
$$

すべて有限値でなければならない。

All values must be finite.

非有限値が発生した計算結果を次のステップへ渡してはならない。

A computation producing non-finite values must not be propagated to the next step.

---

# 6. 計算入力規則  
# 6. Computational Input Rules

$\delta$ 、 $\tau$ 、 $\delta_{\mathrm{upper}}$ 、 $\delta_{\mathrm{lower}}$ 、 $x_{\mathrm{exact}}$ は、次のいずれかから取得する。

1. 直接のCause-Side観測  
2. 計算開始前に固定されたCause-Side変換規則  

各入力には、取得元、取得時刻または版、単位、不確かさ、適用範囲および変換履歴を結び付ける。 $x_{\mathrm{exact}}$ という記号名は真値保証を意味せず、参照状態としての妥当性を領域固有の証拠で検証しなければならない。

新しい権限あるCause-Side観測は、次の評価スナップショットを更新できる。各評価中は、対象、更新権限、更新経路、出所、単位、観測時刻、変換規則、閾値規則、および当該評価スナップショットを固定する。Cause-Side全体を時間的に更新不能と解釈してはならない。

$\delta$, $\tau$, $\delta_{\mathrm{upper}}$, $\delta_{\mathrm{lower}}$, and $x_{\mathrm{exact}}$ must be obtained from either:

1. direct Cause-Side observation; or  
2. a Cause-Side transformation rule fixed before computation begins.  

Each input must be linked to its source, acquisition time or version, unit, uncertainty, applicability, and transformation history. The symbol name $x_{\mathrm{exact}}$ does not guarantee ground truth; its validity as a reference state must be supported by domain-specific evidence.

New authorized Cause-Side observations may update the next evaluation snapshot. During each evaluation, the target, update authority, update route, provenance, unit, observation time, transformation rule, threshold rule, and evaluation snapshot remain fixed. Cause-Side as a whole must not be interpreted as temporally immutable.

次の値を計算入力へ使用してはならない。

- LLM自己評価  
- 意味スコア  
- 出力順位  
- 過去生成出力  
- 廃棄出力  
- 類似性による推定値  
- Effect-Sideから逆算した値  

The following must not be used as computational inputs:

- LLM self-evaluation  
- semantic scores  
- output rankings  
- prior generated output  
- discarded output  
- similarity-based estimates  
- values reverse-estimated from Effect-Side artifacts  

---

# 7. 記号予約  
# 7. Reserved Symbols

- $R$ ：境界接近比のみ  
- $S$ ：構造感度のみ  
- $M_R$ ：残存比率余白のみ
- $M_{\tau}$ ：残存吸収余白のみ
- $\delta$ ：蓄積ズレのみ  
- $\tau$ ：吸収厚みのみ  

- $R$: boundary-approach ratio only  
- $S$: structural sensitivity only  
- $M_R$: remaining ratio margin only
- $M_{\tau}$: remaining absorption margin only
- $\delta$: accumulated deviation only  
- $\tau$: absorption thickness only  

同一文書または同一実装内で、これらの記号を別の意味に再利用してはならない。

These symbols must not be reused with different meanings within the same document or implementation.

---

# 8. 参照文書  
# 8. References

- `theory/AXIOMS.md`
- `theory/axioms.json`
- `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
- `theory/THEORY.md`
- `theory/SANDWICH_ARCH.md`

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
