# NRA-IDE 定義式 / NRA-IDE Formal Equations

**Version:** 2.0  
**Author:** M-Tokuni  
**Document role:** Mathematical and computational definitions only

---

## 0. 文書の役割 / Document Scope

この文書は、NRA-IDEで使用する式、変数、定義域、初期条件、差分条件、数値安定条件を定める。

安全工学上の運用判断、権限移譲、出力制御、監査規則は本書の対象外とする。

This document defines the equations, variables, domains, initial conditions, difference conditions, and numerical-stability requirements used in NRA-IDE.

Operational safety judgment, authority transfer, output control, and audit rules are outside the scope of this document.

---

# 1. 一次式（基本境界式）  
# 1. Primary Formula — Basic Boundary Formula

$$
R = \frac{\delta}{\tau}
$$

### 変数定義 / Variable Definitions

- $\delta$：蓄積ズレ  
- $\tau$：吸収厚み  
- $R$：境界接近比  

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

かつ、$\delta$と$\tau$は有限値でなければならない。

Both $\delta$ and $\tau$ must be finite.

$$
\tau = 0
\Rightarrow
R\ \text{is undefined}
$$

$\tau=0$を無限大の$R$へ置換してはならない。

When $\tau=0$, $R$ must not be replaced by infinity.

---

# 2. 残存吸収余裕  
# 2. Remaining Absorption Margin

$$
M = \tau - \delta
$$

- $M$：残存吸収余裕  
- $M$: remaining absorption margin  

一次式との関係は次である。

$$
R = 1 - \frac{M}{\tau}
$$

または、

$$
M = \tau(1-R)
$$

適用条件：

$$
\tau > 0
$$

---

# 3. 派生計算式：構造感度  
# 3. Derived Formula — Structural Sensitivity

$$
S
=
\frac{1}{M}
$$

したがって、

$$
S
=
\frac{1}{\tau-\delta}
$$

一次式を用いると、

$$
S
=
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

$S$は残存吸収余裕の逆数である。

$S$ is the inverse of the remaining absorption margin.

---

# 4. 二次式（二重ゆらぎ式）  
# 4. Secondary Formula — Dual-Fluctuation Formula

## 4.1 上側・下側蓄積ズレ  
## 4.1 Upper-Side and Lower-Side Accumulated Deviation

$$
\delta_{\mathrm{upper}}(n) \ge 0
$$

$$
\delta_{\mathrm{lower}}(n) \ge 0
$$

$\delta_{\mathrm{upper}}$は、基準から上側方向へ生じたCause-Side蓄積ズレ成分である。

$\delta_{\mathrm{lower}}$は、基準から下側方向へ生じたCause-Side蓄積ズレ成分である。

$\delta_{\mathrm{upper}}$ is the Cause-Side accumulated-deviation component in the upper direction from the reference state.

$\delta_{\mathrm{lower}}$ is the Cause-Side accumulated-deviation component in the lower direction from the reference state.

上側・下側という名称は方向を示す。危険・安全を自動的に意味しない。

The labels upper and lower indicate direction only. They do not automatically mean dangerous or safe.

---

## 4.2 非対称EMA  
## 4.2 Asymmetric EMA

$$
\mathrm{EMA}_{\mathrm{upper}}(n)
=
\alpha_u\delta_{\mathrm{upper}}(n)
+
(1-\alpha_u)\mathrm{EMA}_{\mathrm{upper}}(n-1)
$$

$$
\mathrm{EMA}_{\mathrm{lower}}(n)
=
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

$\alpha_u$と$\alpha_l$は独立に設定できる。

$\alpha_u$ and $\alpha_l$ may be set independently.

---

## 4.3 初期条件  
## 4.3 Initial Conditions

標準初期条件は次とする。

$$
\mathrm{EMA}_{\mathrm{upper}}(0)
=
\delta_{\mathrm{upper}}(0)
$$

$$
\mathrm{EMA}_{\mathrm{lower}}(0)
=
\delta_{\mathrm{lower}}(0)
$$

領域固有の初期値を使用する場合、その値と取得規則を計算開始前に固定する。

When domain-specific initial values are used, both the values and their acquisition rules must be fixed before computation begins.

---

## 4.4 側別有効ゲート幅  
## 4.4 Side-Specific Effective Gate Widths

$$
\tau_{\mathrm{upper}}(n)
=
\tau(n)
f\!\left(
\mathrm{EMA}_{\mathrm{upper}}(n)
\right)
$$

$$
\tau_{\mathrm{lower}}(n)
=
\tau(n)
g\!\left(
\mathrm{EMA}_{\mathrm{lower}}(n)
\right)
$$

$f$と$g$は、評価開始前に固定された変換関数である。

$f$ and $g$ are transformation functions fixed before evaluation begins.

### 必須条件 / Required Conditions

$$
f(x) > 0
$$

$$
g(x) > 0
$$

したがって、

$$
\tau_{\mathrm{upper}} > 0
$$

$$
\tau_{\mathrm{lower}} > 0
$$

$\tau_{\mathrm{upper}}$と$\tau_{\mathrm{lower}}$は、動的評価に用いる側別有効ゲート幅である。

これらは、基礎吸収厚み$\tau$そのものの自然回復を意味しない。

$\tau_{\mathrm{upper}}$ and $\tau_{\mathrm{lower}}$ are side-specific effective gate widths used for dynamic evaluation.

They do not mean that the underlying absorption thickness $\tau$ has naturally recovered.

---

## 4.5 側別境界接近比  
## 4.5 Side-Specific Boundary-Approach Ratios

$$
R_{\mathrm{upper}}
=
\frac{\delta_{\mathrm{upper}}}
{\tau_{\mathrm{upper}}}
$$

$$
R_{\mathrm{lower}}
=
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

## 4.6 最終判定式  
## 4.6 Final Dual-Fluctuation Ratio

$$
R
=
\max
\left(
R_{\mathrm{upper}},
R_{\mathrm{lower}}
\right)
$$

展開形：

$$
R
=
\max
\left(
\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}},
\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
\right)
$$

支配側は次で定義する。

$$
D
=
\operatorname*{arg\,max}
\left\{
R_{\mathrm{upper}},
R_{\mathrm{lower}}
\right\}
$$

- $D=\mathrm{upper}$：上側が支配  
- $D=\mathrm{lower}$：下側が支配  
- $R_{\mathrm{upper}}=R_{\mathrm{lower}}$：同率支配  

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
\Delta\delta_n
=
\delta_n-\delta_{n-1}
$$

$$
\Delta\tau_n
=
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

An auxiliary computation term is combined to compensate for EMA lag, delayed tracking of local rapid change, and domain-specific precision limits.

$$
\frac{d^2x}{dt^2}
+
\gamma\frac{dx}{dt}
=
F_{\mathrm{IDE}}(x)
+
G(r)\Phi(x)
$$

残差：

$$
r
=
x_{\mathrm{exact}}-x
$$

二次残差ゲート：

$$
G(r)
=
r\frac{|r|}{k+|r|}
$$

---

## 5.1 変数定義  
## 5.1 Variable Definitions

- $x$：現在の計算状態  
- $x_{\mathrm{exact}}$：事前定義された高精度参照状態  
- $r$：参照状態との差  
- $\gamma$：減衰係数  
- $k$：knee値  
- $F_{\mathrm{IDE}}(x)$：IDE基礎計算項  
- $\Phi(x)$：補助計算項  
- $G(r)$：二次残差ゲート  

- $x$: current computational state  
- $x_{\mathrm{exact}}$: predefined high-precision reference state  
- $r$: residual relative to the reference state  
- $\gamma$: damping coefficient  
- $k$: knee value  
- $F_{\mathrm{IDE}}(x)$: IDE base computation term  
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

$x$、$x_{\mathrm{exact}}$、$r$、$F_{\mathrm{IDE}}(x)$、$\Phi(x)$は有限値でなければならない。

$x$, $x_{\mathrm{exact}}$, $r$, $F_{\mathrm{IDE}}(x)$, and $\Phi(x)$ must be finite.

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

したがって、$G(r)$は$r$に対して二次的に小さくなる。

Therefore, $G(r)$ becomes second-order small with respect to $r$.

---

## 5.4 大残差領域  
## 5.4 Large-Residual Region

$$
|r| \gg k
$$

このとき、

$$
G(r)
\approx
r\frac{|r|}{|r|}
$$

したがって、

$$
G(r)
\approx
r\,\operatorname{sgn}(r)
$$

ただし、符号設計は$\Phi(x)$の定義と組み合わせて確認する必要がある。

The sign behavior must be checked together with the definition of $\Phi(x)$.

---

## 5.5 knee値  
## 5.5 Knee Value

$$
|r| = k
$$

の近傍は、小残差応答と飽和応答の遷移領域である。

The neighborhood of $|r|=k$ is the transition region between small-residual response and saturation response.

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

$x_0$と$v_0$は計算開始前に固定する。

$x_0$ and $v_0$ must be fixed before computation begins.

---

## 5.7 数値積分条件  
## 5.7 Numerical Integration Conditions

数値積分を用いる場合、次を事前固定する。

- 積分法  
- 時間刻み$\Delta t$  
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

$\delta$、$\tau$、$\delta_{\mathrm{upper}}$、$\delta_{\mathrm{lower}}$、$x_{\mathrm{exact}}$は、次のいずれかから取得する。

1. 直接のCause-Side観測  
2. 計算開始前に固定されたCause-Side変換規則  

$\delta$, $\tau$, $\delta_{\mathrm{upper}}$, $\delta_{\mathrm{lower}}$, and $x_{\mathrm{exact}}$ must be obtained from either:

1. direct Cause-Side observation; or  
2. a Cause-Side transformation rule fixed before computation begins.  

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

- $R$：境界接近比のみ  
- $S$：構造感度のみ  
- $M$：残存吸収余裕のみ  
- $\delta$：蓄積ズレのみ  
- $\tau$：吸収厚みのみ  

- $R$: boundary-approach ratio only  
- $S$: structural sensitivity only  
- $M$: remaining absorption margin only  
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
