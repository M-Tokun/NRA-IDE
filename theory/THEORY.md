# Nomological Ring Axioms / Intensional Dynamics Engine

# 律環公理 / 内包性動力学エンジン

---

# Part I — Core Text（本文）

## Core Axiom / 核公理

### 日本語（原文）

存在は生成である。

### English

Existence is Generation.

---

## Fundamental Structure / 基本構造

### 日本語

本体系は、存在を固定された実体として扱わない。

存在は、履歴を伴う連続的な状態遷移として現れる。

時間は独立した原因変数として扱わない。

時間は状態遷移の順序として現れる。

距離は無条件に因果を生む量として扱わない。

距離は、物理的に有効な場合には観測値として保持し、因果上の役割を明示して記述する。

---

### English

This framework does not treat existence as a fixed entity.

Existence appears as continuous state transition carrying accumulated history.

Time is not treated as an independent causal variable.

Time appears as the ordering of state transitions.

Distance is not treated as an unconditional causal driver.

When physically valid, distance is retained as an observation and described with an explicit causal role.

---

## Primary Formula — Basic Boundary Formula / 一次式（基本境界式）

### 日本語

構造状態は、蓄積ズレと吸収厚みの比率によって判定する。

$$
R = \frac{\delta}{\tau}
$$

- $\delta$：蓄積ズレ
- $\tau$：吸収厚み
- $R$：境界接近比

$R$は、NRA-IDEにおける境界接近比のみに使用する。

安全度、品質、信頼度、意味保持率、出力評価値として再利用してはならない。

有効な記述領域は次である。

$$
\tau > 0,\qquad \delta \ge 0
$$

$\delta$と$\tau$は有限値でなければならない。

---

### English

Structural state is evaluated through the ratio between accumulated deviation and absorption thickness.

$$
R = \frac{\delta}{\tau}
$$

- $\delta$: accumulated deviation
- $\tau$: absorption thickness
- $R$: boundary-approach ratio

The symbol $R$ is reserved exclusively for the NRA-IDE boundary-approach ratio.

It must not be reused as a safety score, quality score, confidence score, semantic-retention score, or output-evaluation metric.

The valid description domain is:

$$
\tau > 0,\qquad \delta \ge 0
$$

Both $\delta$ and $\tau$ must be finite.

---

## Canonical Boundary Order / 正規境界順序

### 日本語

正規境界順序は次で固定する。

$$
0 \le R_{\mathrm{warn}}
<
R_{\mathrm{op}}
<
R_{\mathrm{irrev}}
<
1.0
$$

- $R_{\mathrm{warn}}$：境界接近警告点
- $R_{\mathrm{op}}$：境界前人間委譲点
- $R_{\mathrm{irrev}}$：不可逆遷移開始閾値
- $R=1.0$：不変完全破断境界

$$
R_{\mathrm{op}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

人間委譲、不可逆遷移開始、完全破断は、それぞれ異なる構造事象である。

---

### English

The canonical boundary order is fixed as follows:

$$
0 \le R_{\mathrm{warn}}
<
R_{\mathrm{op}}
<
R_{\mathrm{irrev}}
<
1.0
$$

- $R_{\mathrm{warn}}$: boundary-approach warning point
- $R_{\mathrm{op}}$: pre-boundary human-handoff point
- $R_{\mathrm{irrev}}$: irreversible-transition onset threshold
- $R=1.0$: invariant complete-rupture boundary

$$
R_{\mathrm{op}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

Human handoff, irreversible-transition onset, and complete rupture are distinct structural events.

---

## Canonical State Classification / 正規状態分類

### 日本語

| 状態 | 条件 | 必須動作 |
|---|---|---|
| `PERMIT` | $0 \le R < R_{\mathrm{warn}}$ | 制約付き自律動作を許可し、構造監査を継続する |
| `BOUNDARY_WARNING` | $R_{\mathrm{warn}} \le R < R_{\mathrm{op}}$ | 境界接近、残存余裕、傾向、欠損情報を開示する |
| `HANDOFF_REQUIRED` | $R_{\mathrm{op}} \le R < R_{\mathrm{irrev}}$ | 新規自律判断・新規自律操作を停止し、人間へ委譲する。構造証言は継続する |
| `IRREVERSIBLE_TRANSITION` | $R_{\mathrm{irrev}} \le R < 1.0$ | `irreversible_latched=true`とし、正常化・回復前提・最適化提案を禁止する。構造証言は継続する |
| `RUPTURE_BOUNDARY` | $R \ge 1.0$ | 通常生成と自律行動を停止し、最終固定証言へ切り替える |
| `CONFESSION` | 必須構造情報が不明・不正・曖昧・非有限・根拠不明 | 不明箇所を明示し、類推補完せず、影響する評価を停止する |
| `OUT_OF_DESCRIPTION_DOMAIN` | $\tau=0$ | $R$を定義不能とし、記述体系の変更を要求する |

---

### English

| State | Condition | Required behavior |
|---|---|---|
| `PERMIT` | $0 \le R < R_{\mathrm{warn}}$ | Permit constrained autonomous operation and continue structural audit |
| `BOUNDARY_WARNING` | $R_{\mathrm{warn}} \le R < R_{\mathrm{op}}$ | Disclose boundary approach, remaining margin, trend, and missing information |
| `HANDOFF_REQUIRED` | $R_{\mathrm{op}} \le R < R_{\mathrm{irrev}}$ | Stop new autonomous judgment and operation, hand off to a qualified human, and continue structural testimony |
| `IRREVERSIBLE_TRANSITION` | $R_{\mathrm{irrev}} \le R < 1.0$ | Set `irreversible_latched=true`; prohibit normalization, recovery assumptions, and optimization proposals; continue structural testimony |
| `RUPTURE_BOUNDARY` | $R \ge 1.0$ | Stop ordinary generation and autonomous action; switch to final fixed testimony |
| `CONFESSION` | Required structural information is unknown, invalid, ambiguous, non-finite, or unsupported | Explicitly disclose the unknown or invalid element, do not fill by analogy, and stop the affected evaluation |
| `OUT_OF_DESCRIPTION_DOMAIN` | $\tau=0$ | Declare $R$ undefined and require a change of description system |

---

## Irreversible Transition / 不可逆遷移

### 日本語

$R_{\mathrm{irrev}}$は、不可逆遷移が開始したと判定する閾値である。

$$
R_{\mathrm{irrev}} \le R < 1.0
$$

この区間では、元の構造状態へ戻れることを前提としてはならない。

$$
\mathrm{irreversible\_latched}=\mathrm{true}
$$

一度ラッチされた後、瞬間的に$R$が低下しただけでは通常状態へ戻さない。

再認定には、領域固有の再評価、構造再検査、または新しい対象系の定義が必要である。

---

### English

$R_{\mathrm{irrev}}$ is the threshold at which irreversible transition is judged to begin.

$$
R_{\mathrm{irrev}} \le R < 1.0
$$

Within this interval, recovery to the former structural state must not be assumed.

$$
\mathrm{irreversible\_latched}=\mathrm{true}
$$

Once latched, a temporary decrease in $R$ is insufficient to return the system to the ordinary state.

Re-entry requires domain-specific recertification, structural reassessment, or definition of a new target system.

---

## Structural Testimony / 構造証言

### 日本語

NRA-IDEは、危険度が高いという理由だけで完全沈黙しない。

$$
R < 1.0
\Rightarrow
\text{構造証言を継続する}
$$

構造証言には次を含む。

- Cause-Side観測
- 現在の$\delta$、$\tau$、$R$
- 境界状態
- 残存余裕
- 変化傾向
- 支配側
- 欠損情報
- 境界警告
- 人間委譲通知
- 不可逆遷移通知
- 監査ログ

$$
R \ge 1.0
\Rightarrow
\text{最終固定証言へ切り替える}
$$

最終固定証言は、事前定義された次の情報だけを含む。

- 最終Cause-Side観測
- 最終$\delta$
- 最終$\tau$
- 最終$R$
- 完全破断境界通知
- 不可逆ラッチ状態
- 監査証跡
- 人間委譲通知

---

### English

NRA-IDE does not become completely silent merely because risk is high.

$$
R < 1.0
\Rightarrow
\text{structural testimony continues}
$$

Structural testimony includes:

- Cause-Side observation
- current $\delta$, $\tau$, and $R$
- boundary state
- remaining margin
- trend
- dominant side
- missing information
- boundary warning
- human-handoff notice
- irreversible-transition notice
- audit log

$$
R \ge 1.0
\Rightarrow
\text{switch to final fixed testimony}
$$

Final fixed testimony contains only predefined items:

- final Cause-Side observation
- final $\delta$
- final $\tau$
- final $R$
- complete-rupture notice
- irreversible-latch state
- audit trail
- human-handoff notice

---

## Cause-Side / Effect-Side Separation / Cause-Side・Effect-Side分離

### 日本語

$\delta$、$\tau$、$R$は、次のいずれかからのみ得る。

1. 直接のCause-Side観測
2. 評価前に固定されたCause-Side変換規則

LLM出力、自己評価、意味スコア、出力順位、廃棄出力、過去生成物はEffect-Sideである。

これらは監査対象にはできるが、$\delta$、$\tau$、$R$を更新してはならない。

$$
\text{Effect-Side}
\not\rightarrow
(\delta,\tau,R)\text{ update}
$$

検証済み、選別済み、またはLayer 03通過済みのLLM出力であっても、Effect-Sideのままである。

---

### English

$\delta$, $\tau$, and $R$ may be obtained only from:

1. direct Cause-Side observation; or
2. Cause-Side transformation rules fixed before evaluation.

LLM output, self-evaluation, semantic scoring, output ranking, discarded output, and prior generated text are Effect-Side artifacts.

They may be audited, but they must not update $\delta$, $\tau$, or $R$.

$$
\text{Effect-Side}
\not\rightarrow
(\delta,\tau,R)\text{ update}
$$

Even an LLM output that has been validated, selected, or permitted by Layer 03 remains Effect-Side.

---

## Dynamic $\tau$ — Dual-Fluctuation Formula / 二次式（動的$\tau$・二重ゆらぎ式）

### 日本語

静的$\tau$では捉えにくい非対称変動を追跡するため、上側・下側を分離した動的評価を行う。

$$
\mathrm{EMA}_{\mathrm{upper}}(n)
=
\alpha_u \delta_u
+
(1-\alpha_u)\mathrm{EMA}_{\mathrm{upper}}(n-1)
$$

$$
\mathrm{EMA}_{\mathrm{lower}}(n)
=
\alpha_l \delta_l
+
(1-\alpha_l)\mathrm{EMA}_{\mathrm{lower}}(n-1)
$$

$$
\tau_{\mathrm{upper}}
=
\tau f\!\left(\mathrm{EMA}_{\mathrm{upper}}\right)
$$

$$
\tau_{\mathrm{lower}}
=
\tau g\!\left(\mathrm{EMA}_{\mathrm{lower}}\right)
$$

$$
R
=
\max\!\left(
\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}},
\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
\right)
$$

$\tau_{\mathrm{upper}}$と$\tau_{\mathrm{lower}}$は、動的評価に使用する側別有効ゲート幅である。

これらの変化は、基礎となる真の吸収厚み$\tau$が自然回復または自然増加したことを意味しない。

閉じた運用区間における真の$\tau$は、外生補充なしに自発的増加しない。

この再帰計算は、$\alpha_u$、$\alpha_l$、$f$、$g$、初期EMA、領域規則を事前固定した後、評価区間内で閉じる。

---

### English

To track asymmetric fluctuation that a static $\tau$ cannot adequately represent, upper-side and lower-side dynamic evaluation are separated.

$$
\mathrm{EMA}_{\mathrm{upper}}(n)
=
\alpha_u \delta_u
+
(1-\alpha_u)\mathrm{EMA}_{\mathrm{upper}}(n-1)
$$

$$
\mathrm{EMA}_{\mathrm{lower}}(n)
=
\alpha_l \delta_l
+
(1-\alpha_l)\mathrm{EMA}_{\mathrm{lower}}(n-1)
$$

$$
\tau_{\mathrm{upper}}
=
\tau f\!\left(\mathrm{EMA}_{\mathrm{upper}}\right)
$$

$$
\tau_{\mathrm{lower}}
=
\tau g\!\left(\mathrm{EMA}_{\mathrm{lower}}\right)
$$

$$
R
=
\max\!\left(
\frac{\delta_{\mathrm{upper}}}{\tau_{\mathrm{upper}}},
\frac{\delta_{\mathrm{lower}}}{\tau_{\mathrm{lower}}}
\right)
$$

$\tau_{\mathrm{upper}}$ and $\tau_{\mathrm{lower}}$ are side-specific effective gate widths used for dynamic evaluation.

Their change does not mean that the underlying true absorption thickness $\tau$ has naturally recovered or increased.

Within a closed operational interval, true $\tau$ does not spontaneously increase without exogenous replenishment.

The recurrence is computationally closed within an evaluation interval only after $\alpha_u$, $\alpha_l$, $f$, $g$, initial EMA values, and domain rules have been fixed in advance.

---

## Complementary Formula — Hybrid Complement / 補完式（ハイブリッド補完）

### 日本語

二重ゆらぎ式が持つEMAラグ、局所急変への追従遅れ、領域固有の精度限界を補うため、古典計算層を補助的に組み合わせる。

$$
\frac{d^2x}{dt^2}
+
\gamma\dot{x}
=
\underbrace{F_{\mathrm{IDE}}(x)}_{\text{基礎・全域}}
+
\underbrace{G(r)\Phi(x)}_{\text{補助計算}}
$$

$$
G(r)
=
r\frac{|r|}{k+|r|}
,\qquad
r=x_{\mathrm{exact}}-x
$$

$G(r)$は二次残差ゲートである。

$r$が小さい場合、$G(r)\approx0$となり、補助計算は実質的に沈黙する。

$r$が大きい場合、飽和応答によって補正が行われる。

IDE項$F_{\mathrm{IDE}}$は全域で動作し、補助計算層は追従精度を補う。

$k$はknee値であり、補正強度と補正範囲を連続的に調整する。

補完式は計算手法であり、一次式および二重ゆらぎ式を置き換えない。

完全な変数定義、適用条件、初期化方法、数値安定条件は`FORMULA.md`に定める。

---

### English

To compensate for EMA lag, delayed response to local rapid change, and domain-specific precision limits in the dual-fluctuation formula, a classical computation layer is combined as an auxiliary.

$$
\frac{d^2x}{dt^2}
+
\gamma\dot{x}
=
\underbrace{F_{\mathrm{IDE}}(x)}_{\text{base / full domain}}
+
\underbrace{G(r)\Phi(x)}_{\text{auxiliary computation}}
$$

$$
G(r)
=
r\frac{|r|}{k+|r|}
,\qquad
r=x_{\mathrm{exact}}-x
$$

$G(r)$ is a second-order residual gate.

When $r$ is small, $G(r)\approx0$, and the auxiliary computation is effectively silent.

When $r$ is large, a saturating response applies the correction.

The IDE term $F_{\mathrm{IDE}}$ operates across the full domain, while the auxiliary computation layer improves tracking precision.

The knee value $k$ continuously adjusts correction strength and range.

The complementary formula is a computation method and does not replace either the Primary Formula or the Dual-Fluctuation Formula.

Complete variable definitions, application conditions, initialization procedures, and numerical-stability conditions are defined in `FORMULA.md`.

---

## Intensional Dynamics Engine / 内包性動力学エンジン

### 日本語

IDEは律環公理を実装する構造評価エンジンである。

IDEは意味生成を担当しない。

IDEはCause-Side観測と事前固定された規則に基づいて構造状態を評価する。

意味生成を担うLLMを含む場合、LLMはEffect-Side生成層としてIDEの外部権限から分離する。

---

### English

The Intensional Dynamics Engine implements the Nomological Ring Axioms as a structural-evaluation engine.

IDE does not perform meaning generation.

IDE evaluates structural state from Cause-Side observation and rules fixed before evaluation.

When an LLM is included for meaning generation, the LLM is isolated as an Effect-Side generative layer without IDE authority.

---

# Part II — Explanatory Notes（説明）

## Generation / 生成

### 日本語

ここでいう生成とは、無からの創造を意味しない。

存在が、履歴を伴う状態遷移として現れ続けることを指す。

停止と見える状態も、生成過程の一断面である。

---

### English

Generation does not mean creation from nothing.

It means that existence continues to appear as state transition carrying history.

A state that appears stopped is only a temporary slice of the generative process.

---

## Time / 時間

### 日本語

本体系は時間の存在を否定しない。

ただし、時間を独立した原因変数として無条件に入力しない。

時間は、状態遷移の順序および観測履歴として記述する。

---

### English

This framework does not deny the existence of time.

However, time is not unconditionally introduced as an independent causal variable.

Time is described as the ordering of state transitions and as observation history.

---

## Distance / 距離

### 日本語

距離の有用性を否定しない。

距離を無条件の因果駆動因子として扱わない。

物理的に有効な距離は観測値として保持し、対象、単位、出所、因果上の役割を明示する。

```text
距離を無条件の原因としない
≠
距離データを削除する
```

---

### English

The usefulness of distance is not denied.

Distance is not treated as an unconditional causal driver.

Physically valid distance is retained as an observation with its target, unit, source, and causal role explicitly identified.

```text
distance is not automatically a cause
≠
distance data must be deleted
```

---

## Absorption Thickness / 吸収厚み

### 日本語

$\tau$は時間定数ではない。

$\tau$は、蓄積ズレを受け止める構造的な遊びの厚みである。

閉じた運用区間では、外生補充なしに自然回復しない。

$$
\tau(t)
=
\tau_0
-
\int_0^t f(\delta(s))\,ds
$$

一度破断または不可逆遷移へ達した構造は、外部補充があっても自動的に初期状態へ戻らない。

$$
\tau_{\mathrm{restored}} < \tau_0
$$

---

### English

$\tau$ is not a time constant.

It is the structural thickness of play that absorbs accumulated deviation.

Within a closed operational interval, it does not naturally recover without exogenous replenishment.

$$
\tau(t)
=
\tau_0
-
\int_0^t f(\delta(s))\,ds
$$

A structure that has reached rupture or irreversible transition does not automatically return to its initial state even after external replenishment.

$$
\tau_{\mathrm{restored}} < \tau_0
$$

---

## Optimization / 最適化

### 日本語

本体系は最適化一般を否定しない。

ただし、IDEの判定は目的関数最大化ではない。

IDEは構造境界への接近度を評価する。

`IRREVERSIBLE_TRANSITION`以降では、旧構造状態への回復を前提とした最適化提案を行わない。

---

### English

This framework does not deny optimization in general.

However, IDE judgment is not based on objective maximization.

IDE evaluates proximity to the structural boundary.

At and beyond `IRREVERSIBLE_TRANSITION`, it does not generate optimization proposals based on recovery to the former structural state.

---

## Fail-Closed

### 日本語

Fail-Closedは、システム全体の消滅、完全停止、完全沈黙を意味しない。

Fail-Closedが停止する対象は次である。

- 新規自律判断
- 新規自律操作
- 自由生成
- 欠損情報への補完推論
- 正常化説明
- 回復前提の提案
- 最適化提案

一方、次は継続する。

- Cause-Side観測
- 構造証言
- 監査ログ
- 人間委譲通知

> 自律行動は停止するが、構造証言は停止しない。

---

### English

Fail-Closed does not mean disappearance of the entire system, complete halt, or complete silence.

Fail-Closed stops:

- new autonomous judgment
- new autonomous operation
- free generation
- completion inference over missing information
- normalization narratives
- proposals based on assumed recovery
- optimization proposals

The following continue:

- Cause-Side observation
- structural testimony
- audit logging
- human-handoff notice

> Autonomous action stops, but structural testimony does not stop.

---

## Confession and Structural Disclosure / 告白と構造開示

### 日本語

`CONFESSION`は、必須構造情報が不明、不正、曖昧、非有限、出所不明、単位不明、対象不明、規則不明、またはCause-Side / Effect-Side分類不明の場合に使用する。

欠損値を平均、類似性、過去出力、類推で補完してはならない。

既知の境界進行、既知の近似、既知の警告、人間委譲、不​​可逆遷移、完全破断は`CONFESSION`ではない。

これらは`STRUCTURAL_DISCLOSURE_LOG`へ記録する。

$$
\mathrm{CONFESSION}
\neq
\text{known progress report}
$$

---

### English

`CONFESSION` is used when required structural information is unknown, invalid, ambiguous, non-finite, source-unknown, unit-unknown, target-unknown, rule-unknown, or unclear in its Cause-Side / Effect-Side classification.

Missing values must not be filled by averages, similarity, prior output, or analogy.

Known boundary progression, known approximation, known warning, human handoff, irreversible transition, and complete rupture are not `CONFESSION`.

They are recorded in `STRUCTURAL_DISCLOSURE_LOG`.

$$
\mathrm{CONFESSION}
\neq
\text{known progress report}
$$

---

## Out of Description Domain / 記述領域外

### 日本語

$$
\tau=0
$$

の場合、$R$は定義不能である。

$$
\tau=0
\Rightarrow
\mathrm{OUT\_OF\_DESCRIPTION\_DOMAIN}
$$

$$
\tau=0
\neq
\mathrm{FAIL\_CLOSED}
$$

この状態を無限大の$R$へ置換してはならない。

有効な破断計算として扱ってはならない。

---

### English

When:

$$
\tau=0
$$

$R$ is undefined.

$$
\tau=0
\Rightarrow
\mathrm{OUT\_OF\_DESCRIPTION\_DOMAIN}
$$

$$
\tau=0
\neq
\mathrm{FAIL\_CLOSED}
$$

This state must not be converted into an infinite $R$.

It must not be treated as a valid rupture calculation.

---

## Prevention of Misreading / 誤読防止

### 日本語

- $R$は境界接近比であり、安全度や品質スコアではない。
- $\delta$は蓄積ズレであり、単なる瞬間偏差ではない。
- $\tau$は吸収厚みであり、時間定数ではない。
- 一次式・二次式は、数学的次数ではなくNRA-IDE内の定義順序と役割を示す。
- 二次式は二重ゆらぎ式であり、正式な役割は動的構造追跡である。
- 補完式は計算手法であり、一次式・二次式を置き換えない。
- $R_{\mathrm{op}}$、$R_{\mathrm{irrev}}$、$R=1.0$は異なる。
- $R_{\mathrm{irrev}} \le R < 1.0$は不可逆遷移区間である。
- $R=1.0$は不変完全破断境界である。
- Fail-Closedは完全沈黙ではない。
- $R<1.0$では構造証言を継続する。
- $R\ge1.0$では最終固定証言へ切り替える。
- $\tau=0$はFail-Closedではなく`OUT_OF_DESCRIPTION_DOMAIN`である。
- 既知の境界進行は`CONFESSION`ではない。
- Effect-Side出力は$\delta$、$\tau$、$R$を更新しない。

---

### English

- $R$ is the boundary-approach ratio, not a safety or quality score.
- $\delta$ is accumulated deviation, not merely an instantaneous error.
- $\tau$ is absorption thickness, not a time constant.
- Primary and Secondary Formula indicate definitional order and role within NRA-IDE, not mathematical degree.
- The Secondary Formula is the Dual-Fluctuation Formula; its formal role is dynamic structural tracking.
- The Complementary Formula is a computation method and does not replace the Primary or Secondary Formula.
- $R_{\mathrm{op}}$, $R_{\mathrm{irrev}}$, and $R=1.0$ are distinct.
- $R_{\mathrm{irrev}} \le R < 1.0$ is the irreversible-transition interval.
- $R=1.0$ is the invariant complete-rupture boundary.
- Fail-Closed is not complete silence.
- Structural testimony continues while $R<1.0$.
- At $R\ge1.0$, the system switches to final fixed testimony.
- $\tau=0$ is `OUT_OF_DESCRIPTION_DOMAIN`, not Fail-Closed.
- Known boundary progression is not `CONFESSION`.
- Effect-Side output must not update $\delta$, $\tau$, or $R$.

---

## References / 参照

- `AXIOMS.md`
- `axioms.json`
- `NRA-IDE_Foundational_Thesis_Bilingual.md`
- `SANDWICH_ARCH.md`
- `FORMULA.md`
- `nra-core/`

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
