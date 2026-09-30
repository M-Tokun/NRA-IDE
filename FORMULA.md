# NRA-IDE 定義式 / NRA-IDE Formal Equations

**Version:** 2.2  
**Author:** M-Tokuni  
**Document role:** Mathematical and computational definitions subordinate to `theory/AXIOMS.md` and `theory/axioms.json`

---

## 0. 文書の役割 / Document Scope

この文書は、NRA-IDEで使用する式、変数、定義域、初期条件、差分条件、数値安定条件を定める。

本書の正規IDE計算系は、各領域の支配方程式を置き換えるものではない。Cause-Side観測から\(\delta\)および\(\tau\)を導出する物理式、単位、変換規則および具体的閾値は領域ごとに定義する。不変なのはIDEの境界評価構造であり、現場固有の物理方程式ではない。

律環公理は「存在は生成である。」の一つだけであり、第二公理以降は存在しない。本書の一次式と二次式は、公理ではなくIDEの二つの正規計算系である。それ以外の式は、派生式、補助式または補完式として扱う。分類と意味が衝突する場合は、`theory/AXIOMS.md`および機械可読な同期表現`theory/axioms.json`を優先する。

安全工学上の運用判断、権限移譲、出力制御、監査規則は本書の対象外とする。

This document defines the equations, variables, domains, initial conditions, difference conditions, and numerical-stability requirements used in NRA-IDE.

The canonical IDE calculation systems in this document do not replace the governing equations of individual domains. The physical equations, units, transformation rules, and concrete thresholds used to derive \(\delta\) and \(\tau\) from Cause-Side observations must be defined separately for each domain. The invariant is the IDE boundary-evaluation structure, not the domain-specific physical equation.

There is exactly one Nomological Ring Axiom: “Existence is Generation.” No second or subsequent axiom exists. The Primary and Secondary Formulas in this document are the two canonical IDE calculation systems, not axioms. Every other equation is treated as a derived, auxiliary, or complementary formula. If classification or meaning conflicts, `theory/AXIOMS.md` and its machine-readable synchronized representation `theory/axioms.json` take precedence.

Operational safety judgment, authority transfer, output control, and audit rules are outside the scope of this document.

ただし、本式で評価する対象は計算開始前に一意に宣言する。`R_target >= 1.0` はその対象構造の完全破断境界を表し、センサー、ロガー、通信経路または外部監査系の破断を自動的には表さない。各経路の生存状態は本式とは別に記録する。

The evaluation target must nevertheless be declared unambiguously before computation. `R_target >= 1.0` denotes the complete-rupture boundary of that target structure; it does not automatically denote rupture of a sensor, logger, communication path, or external audit system. Survival of each path is recorded separately from this formula.

---

## 0.5 一次式の前段：評価宣言と導出の鎖 / Pre-Stage of the Primary Formula: Evaluation Declaration and Derivation Chain

本節は、Cause-Side観測から一次式の入力 $\delta$ と $\tau$ を構成するまでの形と条件を定める。定義は `theory/AXIOMS.md` §4・§4.5・§7・§8・§14 による。射影、分解、劣化の進み方、合成の具体的な関数形は領域ごとに定め、本節は形と条件だけを定める。一次式 $R=\delta/\tau$ そのものは変えない。

This section defines the form and conditions by which the inputs $\delta$ and $\tau$ of the Primary Formula are constructed from Cause-Side observations. The definitions follow `theory/AXIOMS.md` §4, §4.5, §7, §8, and §14. The concrete functional forms of projection, decomposition, degradation, and composition are defined per domain; this section defines only their form and conditions. The Primary Formula $R=\delta/\tau$ itself is unchanged.

### 0.5.1 評価宣言 / Evaluation Declaration

計算開始（ $n=0$ ）の前に、評価宣言 $\mathsf{Decl}$ を固定する。 $\mathsf{Decl}$ は評価の結果によって書き換えない。事後の検証結果は、当該評価の前件を遡及的に書き換えず、次の評価スナップショット（§6）へ反映するCause-Side証拠として扱う。

Before computation begins ($n=0$), an evaluation declaration $\mathsf{Decl}$ is fixed. $\mathsf{Decl}$ is not rewritten by the results of the evaluation. Post-hoc verification results do not retroactively rewrite the premises of that evaluation; they are treated as Cause-Side evidence reflected in the next evaluation snapshot (§6).

必須要素 / Required elements:

| 要素 / Element | 内容 / Content | 根拠 / Basis |
|---|---|---|
| 評価対象と破断様式 / target and rupture mode | 評価する構造と、完全破断とみなす様式・経路 / the structure evaluated and the mode and path regarded as complete rupture | §0 |
| 単位 / unit | $\delta$ と $\tau$ に共通の単位 $u$ / the unit $u$ shared by $\delta$ and $\tau$ | §1 |
| 観測の種類と出所 / observations and provenance | 使用するCause-Side観測と、その出所・時点・単位・不確かさ / the Cause-Side observations used, with provenance, time, unit, and uncertainty | §6、AXIOMS §14・§15.1 |
| 閾値 / thresholds | $R_{\mathrm{warn}}$ 、 $R_{\mathrm{handoff}}$ 、 $R_{\mathrm{irrev}}$ | AXIOMS §9 |
| 欠測・観測不能の処理 / handling of missing or unobservable data | 観測不能は`NOT_OBSERVABLE`と欠損理由で示し、0・安定・安全・回復として補完しない / an unobservable channel is reported as `NOT_OBSERVABLE` with the reason and is not filled in as zero, stable, safe, or recovered | AXIOMS §10.2・§11.2・§15.1 |
| 基準状態 / reference state | 蓄積ズレを測る原点。評価中に付け直さない / the origin from which accumulated deviation is measured; not reset during evaluation | AXIOMS §4 |
| 射影規則 $\sigma$ / projection rule $\sigma$ | 観測から蓄積ズレへの変換（0.5.2） / conversion from observations to accumulated deviation (0.5.2) | 本節 / this section |
| 分解規則 $\mathsf{Alloc}$ / allocation rule $\mathsf{Alloc}$ | 観測された変化の計上先（0.5.3） / where each observed change is allocated (0.5.3) | 本節 / this section |
| 宣言厚み $\tau_0$ / declared thickness $\tau_0$ | 評価開始時の構造全体の吸収厚み（0.5.4） / absorption thickness of the whole structure at the start of evaluation (0.5.4) | AXIOMS §7・§8 |
| 合成規則 $\mathrm{Comp}_\tau$ / composition rule $\mathrm{Comp}_\tau$ | 構造要素の厚みから全体の実効厚みを定める規則（0.5.4）。付加がまだない評価でも宣言する / the rule determining the effective thickness of the whole from element thicknesses (0.5.4); declared even before any element is added | AXIOMS §7 |

任意要素 / Optional elements:

- 評価の系列と構造連続性 $\omega$ との対応づけの有無と方法。宣言しない場合は対応づけなしとする。一般規則は定めない。 / Whether and how the sequence of evaluations is mapped to structural continuity $\omega$. If not declared, there is no mapping. No general rule is defined.
- 外部条件の同定：何を制約 $C$ とするか（種類・出所・単位・換算規則）。 $C$ を計器へ入れる場合は、評価前に固定した関数として宣言する（AXIOMS §4.5）。 / Identification of external conditions: what counts as constraint $C$ (kind, source, unit, conversion rule). If $C$ enters the gauge, it is declared as a function fixed before evaluation (AXIOMS §4.5).

要素は省かない。ある成分が存在しない領域では、その成分が0であること、または写像が恒等であることを宣言する（例： $p\equiv0$ ）。 / Elements are not omitted. In a domain where a component does not exist, it is declared to be zero or the mapping to be the identity (for example, $p\equiv0$).

一次式の値は宣言に紐づく。異なる宣言の $R$ は、比較可能性を立証しない限り比較・移植しない。比較可能性の必要条件は、同一対象・同一単位・同一のCause-Side測定規則（基準状態、破断様式、 $\sigma$ 、 $\mathsf{Alloc}$ 、 $\mathrm{Comp}_\tau$ を含む）で $\delta$ と $\tau$ を得ていることである（AXIOMS §8・§15.1）。 / The value of the Primary Formula is bound to its declaration. $R$ values from different declarations are not compared or transferred unless comparability is established. A necessary condition is that $\delta$ and $\tau$ are obtained for the same target, in the same unit, under the same Cause-Side measurement rules (including the reference state, rupture mode, $\sigma$, $\mathsf{Alloc}$, and $\mathrm{Comp}_\tau$) (AXIOMS §8, §15.1).

### 0.5.2 観測事象と射影 / Observation Events and Projection

$n$ は構造更新番号であり、事象の順序を表す（時刻ではない。時刻は各事象の記録に持つ）。更新番号 $n$ の観測事象 $\mathrm{Ev}_n$ は、対象・値・単位・出所・時点・不確かさ・順序・観測経路を持つ記録であり、状態を $n-1$ から $n$ へ進める。その値を観測値 $o_n$ と書く（多変数でよい。§5の計算状態 $x$ とは別の記号である）。

$n$ is the structural update number and denotes the order of events (not time; time is kept in each event record). The observation event $\mathrm{Ev}_n$ at update number $n$ is a record with target, value, unit, provenance, time, uncertainty, order, and observation path, and advances the state from $n-1$ to $n$. Its value is written as the observation value $o_n$ (it may be multivariate; it is distinct from the computational state $x$ of §5).

$$
\delta_n=\sigma(o_n)\ \ge 0
$$

$\sigma$ は、観測値を、基準状態から宣言した破断方向へ測ったズレへ移す規則である。領域の支配方程式または実証された変換規則がここに入る。 / $\sigma$ maps an observation value to the deviation measured from the reference state in the declared rupture direction. The governing equations or validated transformation rules of the domain enter here.

対象・単位・時点・出所のいずれかが不明な事象、値が不正または非有限な事象は、一次式へ入力せず`CONFESSION`とする（AXIOMS §6・§10.6）。観測チャネルから値が得られないだけの場合は、`NOT_OBSERVABLE`と欠損理由を示し、評価宣言の欠測処理に従う（AXIOMS §10.2・§11.2）。 / An event whose target, unit, time, or provenance is unknown, or whose value is invalid or non-finite, is not input to the Primary Formula and results in `CONFESSION` (AXIOMS §6, §10.6). When a value is merely unavailable from an observation channel, `NOT_OBSERVABLE` and the reason are reported, and the declared handling of missing data applies (AXIOMS §10.2, §11.2).

### 0.5.3 分解 / Decomposition

$$
\delta_n=q_n+p_n,\qquad q_n\ge0,\quad p_n\ge0
$$

- $q_n$ ：可逆成分。作用を除けば0へ戻る / reversible component; returns to 0 when the action is removed
- $p_n$ ：不可逆成分（残留ズレ）。評価中に減らない（AXIOMS §7） / irreversible component (residual deviation); does not decrease during evaluation (AXIOMS §7)

分解規則 $\mathsf{Alloc}$ は、各事象を次の四つへ分ける。 / The allocation rule $\mathsf{Alloc}$ divides each event into the following four.

$$
\mathsf{Alloc}(\mathrm{Ev}_n)=\bigl(a_n,\ \Delta p_n,\ \Delta\lambda_n,\ \mathrm{ctx}_n\bigr)
$$

- $a_n$ ：作用（可逆成分を生む） / applied action (produces the reversible component)
- $\Delta p_n\ge0$ ：残留ズレの増分 / increment of residual deviation
- $\Delta\lambda_n\ge0$ ：劣化度の増分（0.5.4。要素が複数なら要素ごと） / increment of degradation (0.5.4; per element when there are several)
- $\mathrm{ctx}_n$ ：文脈・権限・出所。計上先ではない / context, authority, and provenance; not an allocation target

観測された一つの物理的変化は、 $a_n$ ・ $\Delta p_n$ ・ $\Delta\lambda_n$ の**ちょうど一つ**に計上する。どの変化をどれに計上するかは $\mathsf{Alloc}$ の中で事前に固定する。制約 $C$ の時点の値 $C_n$ は観測値 $o_n$ の成分であり、計上先ではなく、事前固定の規則の引数としてだけ効く（AXIOMS §4.5）。 / Each observed physical change is allocated to **exactly one** of $a_n$, $\Delta p_n$, $\Delta\lambda_n$. Which change is allocated where is fixed within $\mathsf{Alloc}$ in advance. The value $C_n$ of constraint $C$ is a component of the observation value $o_n$; it is not an allocation target and acts only as an argument of pre-fixed rules (AXIOMS §4.5).

この一変化一計上は、作用・残留ズレ・劣化へ配分する変化に適用する。構造要素の付加・除去そのものはこれら三つへ計上せず、§0.5.4の構成 $\mathsf{Active}_n$ の更新として扱い、事象として記録する。付加・除去に伴う別個の作用・残留ズレ・劣化には、一変化一計上を適用する。 / This one-change-one-allocation rule applies to changes allocated as action, residual deviation, or degradation. Addition or removal of a structural element itself is not allocated to these three destinations; it updates the composition $\mathsf{Active}_n$ under §0.5.4 and is recorded as an event. If separate action, residual deviation, or degradation accompanies an addition or removal, the rule applies to each such change.

増分は§4.7と同じ後退差分で書く： $p_n=p_{n-1}+\Delta p_n$ 。分解は射影の値を分けるものであり、 $q_n+p_n=\sigma(o_n)$ を満たす。したがって $q_n=\sigma(o_n)-p_n\ge0$ である。これを満たさないことは、 $\sigma$ か $\mathsf{Alloc}$ の宣言が対象に合っていないことを示す。 / Increments use the backward difference of §4.7: $p_n=p_{n-1}+\Delta p_n$. Decomposition divides the value of the projection and satisfies $q_n+p_n=\sigma(o_n)$; hence $q_n=\sigma(o_n)-p_n\ge0$. A violation shows that the declared $\sigma$ or $\mathsf{Alloc}$ does not fit the target.

作用や条件で一時的に狭まり、条件が去れば戻る受け止め幅は、実効厚みから差し引かず、一時的な可逆成分 $q^{\mathrm{temp}}_n\ge0$ として作用 $a_n$ に計上し、 $q_n$ に含める（AXIOMS §7）。条件が残した恒久的な傷みは $\Delta\lambda_n$ に計上する。 / A receiving width temporarily narrowed by an action or condition, which returns when the condition ends, is not subtracted from the effective thickness; it is allocated to the action $a_n$ as the temporary reversible deviation $q^{\mathrm{temp}}_n\ge0$ and included in $q_n$ (AXIOMS §7). Permanent damage left by the condition is allocated to $\Delta\lambda_n$.

### 0.5.4 厚み / Thickness

宣言時の構造を要素 $e=0$ 、後に付加した要素を $e=1,2,\dots$ とする。時点 $n$ に評価対象に含まれている要素（付加され、まだ除去されていない要素）の集合を構成 $\mathsf{Active}_n$ とする。 / The structure at declaration is element $e=0$; elements added later are $e=1,2,\dots$. The set of elements included in the evaluation target at step $n$ (added and not yet removed) is the active elements $\mathsf{Active}_n$.

$$
\tau^{[e]}_n=(1-\lambda^{[e]}_n)\,\tau^{[e]}_0,\qquad 0\le\lambda^{[e]}_n\le1\quad(e\in\mathsf{Active}_n)
$$

$$
\tau_n=\mathrm{Comp}_\tau\bigl((\tau^{[e]}_n)_{e\in\mathsf{Active}_n}\bigr)
$$

要素が一つの場合は $\tau_n=(1-\lambda_n)\,\tau_0$ である。 / For a single element, $\tau_n=(1-\lambda_n)\,\tau_0$.

$\lambda^{[e]}_n$ は要素の劣化度であり、評価中に減らない。 $\mathrm{Comp}_\tau$ は、各引数について非減少、値は有限・非負で単位 $u$ を保ち、要素一つならその厚みに等しく、全要素が0または構成が空なら0とする。評価の中で除去を扱う場合は、要素を外しても値が増えない形でなければならない（直列の連結 $\min_e$ のように、外すと全体が強くなる形では、除去を評価宣言の変更とする）。 / $\lambda^{[e]}_n$ is the degradation fraction of the element and does not decrease during evaluation. $\mathrm{Comp}_\tau$ is non-decreasing in each argument, finite and non-negative in the unit $u$, equal to the element's thickness for a single element, and zero when all elements are zero or there are no active elements. If removal is handled within an evaluation, removing an element must not increase the value (for forms such as a series link $\min_e$, where removal strengthens the whole, removal is treated as a change of the declaration).

吸収厚みが増えるのは構造要素の付加だけである（AXIOMS §7）。付加した要素の宣言厚み $\tau^{[e]}_0$ は、加えた時点のCause-Side測定で定め、評価出力から定めない。壊れていない要素の計画的な除去は劣化ではないので $\lambda$ に計上しない。付加と除去は事象として記録する。 / Absorption thickness increases only through the addition of a structural element (AXIOMS §7). The declared thickness $\tau^{[e]}_0$ of an added element is determined by Cause-Side measurement at the time of addition, not from evaluation outputs. Planned removal of an undamaged element is not degradation and is not counted in $\lambda$. Additions and removals are recorded as events.

| 層 / Layer | 記号 / Symbol | 性質 / Property | 使う場所 / Used in |
|---|---|---|---|
| 宣言厚み / declared thickness | $\tau_0$ | 評価宣言で固定 / fixed by the declaration | 各評価の出発点 / start of each evaluation |
| 実効厚み / effective thickness | $\tau_n$ | 構造要素の付加がない限り非増加 / non-increasing unless a structural element is added | 一次式 / Primary Formula |
| 側別有効ゲート幅 / side-specific effective gate widths | $\tau_{\mathrm{upper}}(n)$ 、 $\tau_{\mathrm{lower}}(n)$ | 増減してよい / may increase or decrease | 二次式（§4.4）だけ / Secondary Formula (§4.4) only |

$\tau_n=0$ のときは§1のとおり $R$ を定義せず、`OUT_OF_DESCRIPTION_DOMAIN`とする。動的な $\tau$ を用いる実装は、その増減がどの層に属するかを明示する（AXIOMS §7）。 / When $\tau_n=0$, $R$ is undefined as stated in §1, and the result is `OUT_OF_DESCRIPTION_DOMAIN`. An implementation using a dynamic $\tau$ states which layer each increase or decrease belongs to (AXIOMS §7).

### 0.5.5 一次式への到達 / Arrival at the Primary Formula

$$
R_n=\frac{\delta_n}{\tau_n}=\frac{q_n+p_n}{\mathrm{Comp}_\tau\bigl(((1-\lambda^{[e]}_n)\,\tau^{[e]}_0)_{e\in\mathsf{Active}_n}\bigr)}
$$

要素が一つの場合は $R_n=(q_n+p_n)/\bigl((1-\lambda_n)\,\tau_0\bigr)$ である。分子は構造へどれだけ入り込んだか、分母は構造の器が今どれだけ残っているかを表す。 / For a single element, $R_n=(q_n+p_n)/\bigl((1-\lambda_n)\,\tau_0\bigr)$. The numerator expresses how far the structure has been penetrated; the denominator expresses how much of the structure's capacity currently remains.

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

# 2. 残存余白
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
M_{\tau}\to 0^{+}
\Rightarrow
S \to +\infty
$$

同値に、

$$
\tau-\delta\to0^{+}
\Rightarrow
S\to+\infty
$$

一次式を用いて極限をRで表す場合は、次の条件を確認しなければならない。

$$
R\to1.0^{-}
\quad\land\quad
\tau(1-R)\to0^{+}
\Rightarrow
S\to+\infty
$$

\(\tau\)が極限近傍で正かつ有限な上界を持つ場合、\(R\to1.0^{-}\)から\(\tau(1-R)\to0^{+}\)が従う。\(\tau\)がRとともに変化する一般の場合、\(R\to1.0^{-}\)だけでは\(S\to+\infty\)を保証しない。

Equivalently, \(S\to+\infty\) when \(\tau-\delta\to0^{+}\). When the limit is expressed through the Primary Formula, \(R\to1.0^{-}\) implies divergence only when \(\tau(1-R)\to0^{+}\). This condition follows when \(\tau\) is positive and bounded above near the limit. If \(\tau\) varies with \(R\) without that condition, \(R\to1.0^{-}\) alone does not guarantee \(S\to+\infty\).

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
\tau(n)\in\mathbb{R}_{\mathrm{finite}},
\qquad
\tau(n)>0
$$

$$
\mathrm{EMA}_{\mathrm{upper}}(n),
\mathrm{EMA}_{\mathrm{lower}}(n)
\in\mathbb{R}_{\mathrm{finite}}
$$

$$
h_{\mathrm{upper}}(x)\in\mathbb{R}_{\mathrm{finite}},
\qquad
h_{\mathrm{upper}}(x)>0
$$

$$
h_{\mathrm{lower}}(x)\in\mathbb{R}_{\mathrm{finite}},
\qquad
h_{\mathrm{lower}}(x)>0
$$

形状変換関数の出力は無次元の倍率でなければならない。関数へ入力する量の単位と変換規則は、領域ごとに評価開始前に固定する。

The shape-transformation functions must return finite, positive, dimensionless scale factors. The unit of each function input and its transformation rule must be fixed for the domain before evaluation begins.

形状変換関数への入力は、Cause-Sideの側別蓄積ズレとその事前固定された平滑値、および評価宣言で計器への入力と定めた制約 $C$ （AXIOMS §4.5）に限る。 $R$ 、 $R_{\mathrm{upper}}$ 、 $R_{\mathrm{lower}}$ 、 $R_{\mathrm{dir}}$ 、正規状態、およびそれらの平均・集約を入力にしてはならない（`theory/AXIOMS.md` §14、逆導出B）。本節の $\tau(n)$ は§0.5.4の実効厚み $\tau_n$ である。

Inputs to the shape-transformation functions are limited to Cause-Side directional accumulated deviations, their pre-fixed smoothed values, and constraint $C$ where the evaluation declaration designates it as a gauge input (AXIOMS §4.5). $R$, $R_{\mathrm{upper}}$, $R_{\mathrm{lower}}$, $R_{\mathrm{dir}}$, canonical states, and their averages or aggregates must not be used as inputs (`theory/AXIOMS.md` §14, reverse derivation B). $\tau(n)$ in this section is the effective thickness $\tau_n$ of §0.5.4.

したがって、

$$
\tau_{\mathrm{upper}}(n)\in\mathbb{R}_{\mathrm{finite}},
\qquad
\tau_{\mathrm{upper}}(n)>0
$$

$$
\tau_{\mathrm{lower}}(n)\in\mathbb{R}_{\mathrm{finite}},
\qquad
\tau_{\mathrm{lower}}(n)>0
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

解説：一次式の増分は次のように分けられる。

$$
R_n-R_{n-1}=\frac{\Delta\delta_n}{\tau_n}+\delta_{n-1}\left(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\right)
$$

第1項は蓄積ズレの増加による寄与（進入項）、第2項は厚みの減少による寄与（縮小項）である。 $\delta_{n-1}>0$ のとき、本節の検出条件 $\Delta\delta_n>0\land\Delta\tau_n<0$ は、両項がともに正であることと一致する。これは二次式の検出条件が一次式の変化と整合することを示す解説であり、二次式を一次式の帰結として位置づけるものではない。二次式はIDEの第二の正規計算系である。

Note: the increment of the Primary Formula decomposes as follows.

$$
R_n-R_{n-1}=\frac{\Delta\delta_n}{\tau_n}+\delta_{n-1}\left(\frac{1}{\tau_n}-\frac{1}{\tau_{n-1}}\right)
$$

The first term is the contribution of increasing accumulated deviation (penetration term); the second is the contribution of decreasing thickness (contraction term). When $\delta_{n-1}>0$, the detection condition $\Delta\delta_n>0\land\Delta\tau_n<0$ of this section coincides with both terms being positive. This note shows that the detection condition of the Secondary Formula is consistent with the change of the Primary Formula; it does not position the Secondary Formula as a consequence of the Primary Formula. The Secondary Formula is the second canonical IDE calculation system.

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
G(\xi)\Phi(x)
$$

残差：

$$
\xi =
x_{\mathrm{exact}}-x
$$

二次残差ゲート：

$$
G(\xi) =
\xi\frac{|\xi|}{k+|\xi|}
$$

---

## 5.1 変数定義  
## 5.1 Variable Definitions

- $x$ ：現在の計算状態  
- $x_{\mathrm{exact}}$ ：由来と不確かさを記録した事前定義の高精度参照状態（絶対的真値を意味しない）
- $\xi$ ：参照状態との差  
- $\gamma$ ：減衰係数  
- $k$ ：knee値  
- $F_{\mathrm{IDE}}(x)$ ：領域固有の基礎動力学項（IDE一次式ではない）
- $\Phi(x)$ ：補助計算項  
- $G(\xi)$ ：二次残差ゲート  

- $x$: current computational state  
- $x_{\mathrm{exact}}$: predefined high-precision reference state with recorded provenance and uncertainty (not guaranteed absolute ground truth)
- $\xi$: residual relative to the reference state  
- $\gamma$: damping coefficient  
- $k$: knee value  
- $F_{\mathrm{IDE}}(x)$: domain-specific base-dynamics term (not the IDE Primary Formula)
- $\Phi(x)$: auxiliary computation term  
- $G(\xi)$: second-order residual gate  

---

## 5.2 パラメータ条件  
## 5.2 Parameter Conditions

$$
\gamma \ge 0
$$

$$
k > 0
$$

$$
\gamma,k\in\mathbb{R}_{\mathrm{finite}}
$$

$x$ 、 $x_{\mathrm{exact}}$ 、 $\xi$ 、 $F_{\mathrm{IDE}}(x)$ 、 $\Phi(x)$ は有限値でなければならない。

$x$, $x_{\mathrm{exact}}$, $\xi$, $F_{\mathrm{IDE}}(x)$, and $\Phi(x)$ must be finite.

$x_{\mathrm{exact}}$ 、 $F_{\mathrm{IDE}}(x)$ 、 $\Phi(x)$ および各パラメータは、領域固有の根拠、適用範囲、不確かさ、検証方法を計算開始前に固定し、追跡可能にしなければならない。

For $x_{\mathrm{exact}}$, $F_{\mathrm{IDE}}(x)$, $\Phi(x)$, and each parameter, domain-specific evidence, applicability, uncertainty, and validation method must be fixed before computation and remain traceable.

### 次元整合条件 / Dimensional Consistency

\([x]=X\)、\([t]=T\)とする。残差 \(\xi=x_{\mathrm{exact}}-x\) と残差ゲートの加算 \(k+|\xi|\) を成立させるため、次を満たさなければならない。

$$
[x_{\mathrm{exact}}]=[\xi]=[k]=X
$$

このとき、

$$
[G(\xi)]=X
$$

である。補完式の各項を同次元にするため、次を満たさなければならない。

$$
[\gamma]=T^{-1}
$$

$$
[F_{\mathrm{IDE}}(x)]=XT^{-2}
$$

$$
[\Phi(x)]=T^{-2}
$$

したがって、

$$
\left[\frac{d^2x}{dt^2}\right]
=
\left[\gamma\frac{dx}{dt}\right]
=
[F_{\mathrm{IDE}}(x)]
=
[G(\xi)\Phi(x)]
=
XT^{-2}
$$

Let \([x]=X\) and \([t]=T\). Dimensional validity of \(\xi=x_{\mathrm{exact}}-x\) and \(k+|\xi|\) requires \([x_{\mathrm{exact}}]=[\xi]=[k]=X\), which gives \([G(\xi)]=X\). The complementary equation is dimensionally homogeneous only when \([\gamma]=T^{-1}\), \([F_{\mathrm{IDE}}(x)]=XT^{-2}\), and \([\Phi(x)]=T^{-2}\). A domain may choose its own units, but it must establish these dimensional relations before computation.

---

## 5.3 小残差領域  
## 5.3 Small-Residual Region

$$
|\xi| \ll k
$$

このとき、

$$
G(\xi)
\approx
\frac{\xi|\xi|}{k}
$$

したがって、 $G(\xi)$ は $\xi$ に対して二次的に小さくなる。

Therefore, $G(\xi)$ becomes second-order small with respect to $\xi$.

---

## 5.4 大残差領域  
## 5.4 Large-Residual Region

$$
|\xi| \gg k
$$

このとき、

$$
G(\xi) =
\frac{\xi}{1+k/|\xi|}
$$

したがって、

$$
\lim_{|\xi|/k\to\infty}\frac{G(\xi)}{\xi}=1
$$

すなわち、

$$
G(\xi)\sim \xi
$$

$G(\xi)$ は奇関数であり、 $\xi$ の符号を保持する。大残差で有界値へ飽和せず、漸近的に線形かつ非有界である。

$G(\xi)$ is odd and preserves the sign of $\xi$. For large residuals it is asymptotically linear and unbounded; it does not saturate to a bounded value.

---

## 5.5 knee値  
## 5.5 Knee Value

$$
|\xi| = k
$$

の近傍は、小残差の二次応答と大残差の漸近線形応答の遷移領域である。

The neighborhood of $|\xi|=k$ is the transition region between the quadratic small-residual response and the asymptotically linear large-residual response.

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
\xi_n \in \mathbb{R}
$$

$$
G(\xi_n) \in \mathbb{R}
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

§0.5の観測値 $o_n$ 、付加した要素の宣言厚み $\tau^{[e]}_0$ 、制約の値 $C_n$ も、上の取得規則に従う。

「Effect-Sideから逆算した値」の禁止は、Cause-Side内で事前固定規則に従って行う数値的な逆演算・逆問題を禁止しない。その場合は、近似と不確かさを開示し、変換規則として計算開始前に固定する。逆導出の定義は `theory/AXIOMS.md` §14、分類は `theory/SANDWICH_ARCH.md` §8.4 による。

The observation value $o_n$, the declared thickness $\tau^{[e]}_0$ of an added element, and the constraint value $C_n$ in §0.5 follow the same acquisition rules.

The prohibition of "values reverse-estimated from Effect-Side artifacts" does not prohibit numerical inverse computation or inverse problems performed within Cause-Side under pre-fixed rules. In that case, approximation and uncertainty are disclosed and the procedure is fixed as a transformation rule before computation begins. The definition of reverse derivation follows `theory/AXIOMS.md` §14, and its classification follows `theory/SANDWICH_ARCH.md` §8.4.

---

# 7. 記号予約  
# 7. Reserved Symbols

- $R$ ：境界接近比のみ  
- $S$ ：構造感度のみ  
- $M_R$ ：残存比率余白のみ
- $M_{\tau}$ ：残存吸収余白のみ
- $\delta$ ：蓄積ズレのみ  
- $\tau$ ：吸収厚みのみ  
- $\omega$ ：構造連続性のみ（theory/AXIOMS.md §4.5）
- $C$ ：制約（外部から加わる負荷・拘束・環境条件）のみ。蓄積ズレ・吸収厚みの計上先にしない（使う場合、theory/AXIOMS.md §4.5）
- $\mathrm{entropy}$ ：ドメイン固有のエントロピー相当量のみ（使う場合、theory/AXIOMS.md §4.5）。$S$ と混同しない

- $R$: boundary-approach ratio only  
- $S$: structural sensitivity only  
- $M_R$: remaining ratio margin only
- $M_{\tau}$: remaining absorption margin only
- $\delta$: accumulated deviation only  
- $\tau$: absorption thickness only  
- $\omega$: structural continuity only (theory/AXIOMS.md §4.5)
- $C$: constraint (external load, restraint, or environmental condition) only; never an allocation target of accumulated deviation or absorption thickness (when used, theory/AXIOMS.md §4.5)
- $\mathrm{entropy}$: domain-specific entropy-like quantity only, when used (theory/AXIOMS.md §4.5); not to be confused with $S$

同一文書または同一実装内で、これらの記号を別の意味に再利用してはならない。$W$（仕事量）は、使う場合だけドメインが定義・単位・観測方法を明記する任意量であり（theory/AXIOMS.md §4.5）、この予約表には含めない。位相は $\mathrm{Phase}$ と綴りで表し、FORMULA.md §5.1の $\Phi(x)$ と大小文字だけで区別しない。

同一文書または同一実装内では、字体・大小文字・書体・装飾の違いだけで、別の意味の記号を区別してはならない。別の意味には別の基底名を使う。標準の数学演算子、名前・説明を表す添字（ラベル）、次元の記号は、この規則の対象外とする。

These symbols must not be reused with different meanings within the same document or implementation. $W$ (Work) is an optional quantity used only when a domain fixes its definition, unit, and observation method (theory/AXIOMS.md §4.5), and is not included in this reserved list. The transition phase is written $\mathrm{Phase}$ (spelled), not distinguished from $\Phi(x)$ in §5.1 by case alone.

Within the same document or implementation, symbols with different meanings must not be distinguished only by font, letter case, typeface, or decoration. Distinct meanings use distinct base names. Standard mathematical operators, subscripts that are names or descriptions (labels), and dimension symbols are outside this rule.

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
