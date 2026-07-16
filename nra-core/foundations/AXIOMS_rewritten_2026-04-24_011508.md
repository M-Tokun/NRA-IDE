# AXIOMS.md — 律環公理・公理群定義書

> [!CAUTION]
> **2026-04-24履歴版 / Historical revision dated 2026-04-24 — 非正規 / Noncanonical**
>
> この文書は改訂経過を保存する履歴資料であり、現行正典ではない。旧状態名、旧終端動作、現行正典と異なる公理構成を含み得る。現行規則はリポジトリルートの`theory/AXIOMS.md`と`theory/axioms.json`を参照すること。履歴証拠を保つため、以下の本文は遡及修正しない。
>
> This document preserves revision history and is not the current canonical source. It may contain superseded state names, terminal behavior, and an axiom structure that differs from the current canon. Consult root `theory/AXIOMS.md` and `theory/axioms.json`. The body below is not retroactively rewritten so that historical evidence remains intact.
>
> **現行分類:** 律環公理は「存在は生成である。」の一つだけであり、第二公理以降は存在しない。以下の`Axiom 0`～`Axiom 13`は2026-04-24時点の失効した旧分類であり、現行公理番号ではない。一次式と二次式（二重ゆらぎ式）は、公理ではなくIDEの二つの正典計算系である。旧`Axiom 4`等のその他の式は、現行では派生式、補助式または補完式としてのみ評価する。
>
> **現行状態:** `PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`の7状態を使用する。以下の旧状態語、`tau=0`の存在否定、`R>=1`の単純なOutput Halt、停止だけに限定した旧Fail-Closed説明を現行実装または運用へ適用してはならない。
>
> **使用禁止:** 以下の履歴本文を、現行仕様、正規実装要件、適合証拠、安全証明、測定結果、または特定ドメインでの運用判断根拠として使用してはならない。対応PDFの存在はこのMarkdown履歴の有効性または完全性の条件ではない。
>
> **Current classification:** There is exactly one Nomological Ring Axiom: “Existence is Generation.” No second or subsequent axiom exists. `Axiom 0` through `Axiom 13` below are a superseded classification dated 2026-04-24, not current axiom numbers. The Primary and Secondary / Dual-Fluctuation Formulas are the two canonical IDE calculation systems, not axioms. Other equations, including former `Axiom 4`, are evaluated only as derived, auxiliary, or complementary formulas under the current canon.
>
> **Current states:** Use the seven states `PERMIT`, `BOUNDARY_WARNING`, `HANDOFF_REQUIRED`, `IRREVERSIBLE_TRANSITION`, `RUPTURE_BOUNDARY`, `CONFESSION`, and `OUT_OF_DESCRIPTION_DOMAIN`. Do not apply the historical state terms, the denial of existence at `tau=0`, simple Output Halt at `R>=1`, or the halt-only historical Fail-Closed description to current implementation or operation.
>
> **Do not use:** The historical body below must not be used as a current specification, normative implementation requirement, conformance evidence, safety proof, measurement result, or basis for operational decisions in any domain. A corresponding PDF is not required for this Markdown record to remain valid or complete as historical evidence.

---

> [!NOTE]
> **以下は凍結した履歴本文です。正典同期を目的とする文言修正を行いません。 / The body below is a frozen historical record and is not rewritten for canonical synchronization.**

## Nomological Ring Axioms — Formal Axiom Set

**著者 / Author：** M-Tokuni

**プロジェクト / Project：** NRA-IDE

**版 / Version：** 1.2 Revised

**日付 / Date：** 2026-04-24

---

## 凡例 / Notation

| 記号 | 意味                 | Symbol  | Meaning                       |

| ---- | -------------------- | ------- | ----------------------------- |

| δ   | 蓄積ズレ             | delta   | Accumulated Deviation         |

| τ   | 吸収厚み             | tau     | Absorption Thickness          |

| R    | 接近比               | R       | Structural Approach Ratio     |

| ω   | 構造連続性           | omega   | Structural Continuity         |

| ε   | 最小閾値（ゼロ近傍） | epsilon | Minimum threshold (near-zero) |

| ∅   | 定義域外             | ∅      | Out of domain                 |

---

## Part I — 基底公理 / Foundational Axioms

### Axiom 0：状態の生成 / State Generation

> **存在は生成である。**

> **Existence is Generation.**

存在は静的実体ではなく，履歴を伴って連続する生成である。

静止は生成過程の一時的切り取りにすぎず，構造内部に絶対停止は存在しない。

Existence is not a static entity but a continuous generation with history.

Rest is only a temporary slice of an ongoing generative process;

absolute stoppage does not exist within the structure.

**帰結 / Corollaries**

1. 絶対的静止状態は存在しない。 / No absolute rest state exists.

2. 同一履歴の完全再現は不可能である。 / Exact reproduction of identical history is impossible.

3. 世界は静的状態の集合ではなく，履歴を伴う生成構造である。 / The world is a generative structure with accumulated history, not a set of static states.

### Axiom 1：遊びのない厳密さは崩壊する / Rigidity Without Play Collapses

生成構造が現実系として持続するためには，吸収の余裕が必要である。

遊び（structural play）のない厳密な構造は，わずかな逸脱に対しても破断に至る。

For a generative structure to persist as a real system, absorption margin is necessary.

A structure with no play collapses under even slight deviation.

この公理は Axiom 0 から派生するものではなく，Axiom 0 を前提として現実系の持続条件を付加する。

This axiom does not derive from Axiom 0 but presupposes it, adding the condition required for persistence in real systems.

### Axiom 2：履歴蓄積と吸収厚み / Historical Accumulation and Absorption Thickness

生成が続く限り構造には履歴が蓄積する。その蓄積が δ であり，それを受け止める構造の余裕が τ である。

As long as generation continues, history accumulates within the structure.

That accumulation is δ, and the structural margin that receives it is τ.

任意の生成構造は，履歴に応じたズレの蓄積を持つ。

構造状態は，蓄積ズレと吸収厚みの関係によって記述される。

Any generative structure possesses deviation accumulated through history.

Structural state is described by the relation between accumulated deviation and absorption thickness.

---

## Part II — 構造計量公理 / Structural Metric Axioms

### Axiom 3：構造状態追跡式 / Structural State Tracking Formula

$$

R = \delta / \tau

$$

- δ（蓄積ズレ）：構造内部に蓄積された逸脱量。 / Accumulated deviation within structure.

- τ（吸収厚み）：構造がズレを吸収できる余裕。 / Structural tolerance capacity.

- R（接近比）：構造破断への接近度。 / Ratio of approach to structural break.

**定義域制約 / Domain Constraint**

$$

\tau > 0

$$

τ = 0 は定義域外である。

これは単なる危険状態ではなく，構造そのものが成立していない状態を意味する。

τ = 0 is out of the domain.

It does not indicate mere danger, but the non-existence of the structure itself.

### Axiom 4：τ 状態遷移式 / τ State Transition Formula

外部補充のない閉じた運用区間において，τ は時間とともに減少する。

Within a closed operational interval without external replenishment, τ decreases with time.

$$

\tau(t) = \tau_0 - \int_0^t f(\delta(s))\,ds

$$

- τ₀：初期吸収厚み。 / Initial absorption thickness.

- f(δ)：蓄積ズレに応じた τ の消耗率関数。 / Depletion-rate function of τ driven by accumulated deviation.

τ の増加は，自然回復ではなく外生的な補充操作によってのみ生じる。

したがって，減少と補充は同一過程として扱わない。

Increase of τ arises only through exogenous replenishment, not spontaneous reversal.

Therefore depletion and replenishment are not treated as the same process.

### Axiom 5：復元劣化 / Restoration Degradation

$$

\tau_{restored} < \tau_0

$$

一度，破断または相転移に至った構造は，外部補充を受けても初期値 τ₀ を回復しない。

復元後の τ は，原初構造と同一ではない。

Once a structure has reached break or phase transition, external replenishment never restores τ to the original τ₀.

The restored τ is not identical to the primordial structure.

これは履歴の非可逆性を定量的に記述する。

This quantitatively expresses the irreversibility of structural history.

---

## Part III — 破断境界公理 / Break Boundary Axioms

### Axiom 6：破断点・相転移点 / Break Point and Phase Transition Point

$$

R \geq 1 \; \Longrightarrow \; \text{Break / Phase Transition / Output Halt}

$$

R = 1 は警告値ではない。

R = 1 は破断点であり，相転移点であり，運用判断の開始点ではない。

この点への到達後，構造は内部補正による通常復帰経路を持たない。

R = 1 is not a warning value.

R = 1 is the break point and phase transition point, not the starting point of operational judgment.

After this point, the structure no longer possesses an ordinary recovery path through internal correction.

### Axiom 7：理論崩壊接近域 / Theoretical Collapse-Approach Region

R < 1 であっても，構造が内部補正経路を失い，R = 1 への接近以外に有効な進路を持たない状態が存在する。

これを理論崩壊接近域と呼ぶ。

Even when R < 1, there exists a state in which the structure has lost its internal correction path and retains no effective course except approach toward R = 1.

This state is called the theoretical collapse-approach region.

理論崩壊接近域は破断点ではない。

しかし，自律系にとっては最終運用域であり，この領域を越えて 1.0 に到達した時点で，人間介入を含む後続操作は事後対応となる。

The theoretical collapse-approach region is not the break point.

However, for an autonomous system it is the final operational domain; once 1.0 is reached beyond this region, any subsequent action, including human intervention, becomes post-event response.

---

## Part IV — 演算制御公理 / Operational Control Axioms

### Axiom 8：Fail-Closed 原理 / Fail-Closed Principle

破断点に到達した構造ノードは，以後の演算対象から排除される。

許される応答は停止，遮断，不能性出力に限られる。

A structural node that has reached the break point is excluded from further computation.

The only permitted responses are halt, block, or output of incapability.

**禁止事項 / Prohibitions**

- 逆算の禁止：R から δ または τ を一意復元してはならない。Reverse calculation is prohibited: δ or τ must not be uniquely reconstructed from R.

- 二重推定連鎖の禁止：推定値を再び入力として再推定してはならない。

  Double-estimation chains are prohibited: an estimate must not be used as the basis of a further estimate.

### Axiom 9：全変数動的化原則 / All-Variables-Dynamic Principle

すべての主要変数は時間関数として扱われる。

All principal variables are treated as functions of time.

$$

\delta = \delta(t), \quad \tau = \tau(t), \quad R = R(t) = \delta(t)/\tau(t)

$$

定数固定は，運用上の近似としてのみ許される。

構造真理として固定することはできない。

Constant fixing is permitted only as an operational approximation.

It cannot be treated as structural truth.

### Axiom 10：誤差種別分離原則 / Error-Class Separation Principle

誤差には，通常誤差と変質誤差がある。

Errors are divided into ordinary error and metamorphic error.

- 通常誤差（ordinary error）：δ として蓄積され，R で評価できる誤差。Error that accumulates as δ and can be evaluated through R.

- 変質誤差（metamorphic error）：誤差の評価軸そのものを破壊する事象。

  発生した時点で，以後の系列は誤差として扱えない別構造となる。

  An event that destroys the evaluation axis of error itself.

  From the moment it occurs, the subsequent series can no longer be treated as error — it becomes a different structural class.

---

## Part V — 構造境界公理 / Structural Boundary Axioms

### Axiom 11：距離非因果原則 / Distance Is Not a Cause

距離は構造変化の結果として観測される量であり，原因ではない。

NRA-IDE は距離量を構造因果の基礎に置かない。

Distance is an observable quantity that appears as a result of structural change, not as a cause.

NRA-IDE does not place distance metrics at the basis of structural causality.

### Axiom 12：現象独立原則 / Phenomenon Independence Principle

見かけ上，符号反転または逆方向として理解される現象であっても，構造的に同一事象であるとは限らない。

凍結と融解のような現象は，同一過程の正負反転ではなく，それぞれ独立の生成事象として扱われる。

Even when phenomena appear to be sign inversion or reverse direction, they are not necessarily the same structural event.

Phenomena such as freezing and melting are treated not as positive/negative inversion of one process but as independent generative events.

各現象はそれぞれ固有の δ と τ を持つ。

したがって，一方を他方の逆算で表現してはならない。

Each phenomenon possesses its own δ and τ.

Therefore one must not be represented as the reverse calculation of the other.

### Axiom 13：信頼と安全の分離原則 / Trust–Safety Separation Principle

信頼と安全は同一式で記述してはならない。

Trust and safety must not be described by the same formula.

- 安全：破断接近および破断到達を遮断する構造規則。Safety: structural rules that block break-approach and break arrival.

- 信頼：別軸で評価される性質。

  Trust: a property evaluated on a separate axis.

安全判定を信頼評価に代用してはならず，信頼評価を安全保証に読み替えてはならない。

Safety judgment must not be substituted by trust evaluation, and trust evaluation must not be reinterpreted as safety guarantee.

---

## Document Info

  ©M-Tokuni 2026

- 改訂版 / Revised edition：2026-04-24

- ライセンス / License：MIT

- リポジトリ / Repository：https://github.com/M-Tokun/NRA-IDE
