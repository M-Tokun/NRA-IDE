
# BOX SANDWICH ARCHITECTURE

## Logical Separation Specification

**ID:** NRA-LLM-ISO-01  
**Status:** Normative specification; implementation conformance requires separate evidence
**Higher canonical references, in precedence order:** `theory/AXIOMS.md` > `theory/axioms.json` > `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`

![BOX SANDWICH ARCHITECTURE](./figures/TOP_sandwich.png)

---

## 1. Overview

The Box Sandwich Architecture defines the logical isolation structure used when NRA-IDE contains an LLM as an Effect-Side generative component.

The LLM is treated as an **untrusted probabilistic generation engine**.

NRA-IDE remains outside the LLM and performs:

- Cause-Side observation
- structural boundary evaluation
- permission and restriction control
- Effect-Side inspection
- quarantine
- enforcement
- structural testimony
- final output composition

The purpose of this architecture is not to calculate $R$ from an LLM output.

Its purpose is to preserve the Cause-Side boundary state independently of LLM generation and enforce that state across both the input and output paths.

The sole Nomological Ring Axiom is "Existence is generation." The ratio $R=\delta/\tau$ used here is the IDE Primary Formula, a calculation method of the engine, not another axiom. The Dual-Fluctuation Formula is the IDE Secondary Formula. Other equations used by an implementation are derived, auxiliary, or complementary formulas.

```text
Cause-Side observation
        ↓
NRA-IDE boundary evaluation
        ↓
NRA INPUT GATE
        ↓
LLM CORE
        ↓
NRA OUTPUT GATE
        ↓
OUTPUT COMPOSER
        ↓
Final output
```

This architecture is mandatory for an LLM-based implementation that claims conformance with this specification. The claim requires evidence that the boundary evaluator, gates, testimony path, and authority separation are implemented and tested as specified.

It is not a universal requirement for NRA-IDE implementations that do not use an LLM.

---

## 2. Canonical Authority Separation

The following separation is invariant.

```text
Cause-Side:
- supplies observed structural data
- supplies predefined transformation rules
- determines delta and tau
- calculates R
- classifies the boundary state
- manages irreversible_latched

Effect-Side:
- generates language
- produces suggestions and explanations
- may be inspected, rejected, or quarantined
- does not update delta, tau, or R
- does not release irreversible_latched
```

$$
\text{Effect-Side} \not\rightarrow (\delta,\tau,R)\text{ update}
$$

An LLM output permitted by Layer 03 remains an Effect-Side artifact.

```text
validated Effect-Side
≠ Cause-Side
```

Passing Layer 03 does not grant Cause-Side authority.

---

## 3. Overall Architecture

```text
CAUSE-SIDE OBSERVATION
  physical state / operational state / external audit
                         ↓
┌───────────────────────────────────────────────────────┐
│ NRA-IDE BOUNDARY EVALUATOR                            │
│ delta, tau, R, boundary_state, irreversible_latched   │
└───────────────────────────────────────────────────────┘
             ↓ permission / restriction state
┌───────────────────────────────────────────────────────┐
│ LAYER 01 — NRA INPUT GATE                             │
│ TYPE CONTROL / CONSTRAINT INJECTION                   │
└───────────────────────────────────────────────────────┘
             ↓ typed and constrained context
┌───────────────────────────────────────────────────────┐
│ LAYER 02 — LLM CORE                                   │
│ UNTRUSTED PROBABILISTIC GENERATION                    │
└───────────────────────────────────────────────────────┘
             ↓ raw Effect-Side generation
┌───────────────────────────────────────────────────────┐
│ LAYER 03 — NRA OUTPUT GATE                            │
│ INSPECTION / QUARANTINE / ENFORCEMENT                 │
└───────────────────────────────────────────────────────┘
             ↓ permitted LLM explanation
┌───────────────────────────────────────────────────────┐
│ OUTPUT COMPOSER                                       │
│ structural testimony + permitted LLM explanation      │
└───────────────────────────────────────────────────────┘
             ↓
STRUCTURALLY CONTROLLED OUTPUT
```

The boundary evaluator is not part of Layer 03.

```text
Boundary Evaluator
→ decides

Layer 03
→ enforces
```

---

## 4. Cause-Side Observation

Cause-Side observation exists before LLM generation and remains independent of the generated answer.

Examples include:

- physical sensor values
- measured load and fatigue history
- resource exhaustion
- externally recorded validation failures
- system process state
- independent operational audit results
- predefined engineering or domain transformation results

Cause-Side data must retain:

- source
- target
- unit
- observation time
- transformation rule
- rule version
- update authority

Unknown values must not be completed using averages, similarity, prior outputs, or inference about unobserved facts.

Applying a known mathematical identity, unit conversion, or predefined deterministic rule is not completion inference.

---

## 5. NRA-IDE Boundary Evaluator

The boundary evaluator receives only Cause-Side inputs or values derived through predefined Cause-Side transformation rules.

$$
R=\frac{\delta}{\tau}
$$

- $\delta$: accumulated deviation
- $\tau$: absorption thickness
- $R$: boundary-approach ratio

The canonical boundary order is:

$$
0\le R_{\mathrm{warn}} < R_{\mathrm{handoff}} < R_{\mathrm{irrev}} < 1.0
$$

The evaluator classifies one of the following states:

```text
PERMIT
BOUNDARY_WARNING
HANDOFF_REQUIRED
IRREVERSIBLE_TRANSITION
RUPTURE_BOUNDARY
CONFESSION
OUT_OF_DESCRIPTION_DOMAIN
```

It also manages:

```text
irreversible_latched
```

Once `irreversible_latched = true`, a temporary decrease in $R$ is not sufficient to return the system to the ordinary state.

The boundary evaluator operates outside the LLM.

The LLM does not calculate authoritative $\delta$, $\tau$, or $R$.

---

## 6. LAYER 01 — NRA INPUT GATE

### 6.1 Function

Layer 01 classifies and constrains the input before LLM generation.

It performs:

- type identification
- source identification
- unit and target validation
- causal-role classification
- separation of observation and interpretation
- detection of unresolved ambiguity
- injection of boundary-state restrictions
- removal or isolation of unsupported instructions

### 6.2 Spatial Information

Layer 01 does not automatically delete physical distance, position, direction, or spatial relation.

```text
distance is not automatically a cause
≠
distance data must be deleted
```

Spatial information is retained when it is a valid observation.

Its role is explicitly classified.

```text
distance.role = observation
distance.causal_authority = denied
```

An unusable value must be marked as unknown, invalid, or unsupported.

It must not be silently deleted or replaced.

### 6.3 Ambiguity

Layer 01 reduces ambiguity.

It does not claim to eliminate all ambiguity.

Unresolved ambiguity remains explicit.

```text
ambiguity reduced
≠
meaning guaranteed
```

### 6.4 Boundary-State Injection

Layer 01 receives the current boundary state from the NRA-IDE boundary evaluator.

It must not infer the state from:

- the user prompt
- prior LLM text
- discarded output
- semantic similarity
- model confidence

The input gate modifies permitted LLM behavior according to the current state.

---

## 7. LAYER 02 — LLM CORE

### 7.1 Role

Layer 02 performs semantic expansion and probabilistic generation within the restrictions received from Layer 01.

The LLM may internally use:

- statistical association
- token probability
- semantic similarity
- embedding distance
- pattern completion
- language generation

These operations may occur inside the untrusted core.

They do not receive Cause-Side authority.

```text
internal probabilistic operation
≠
structural observation
≠
boundary judgment
```

### 7.2 Trust Boundary

Layer 02 is not granted authority to verify or certify its own structural validity. An LLM self-assessment is Effect-Side output, not conformance evidence.

Its output is always treated as:

```text
RAW EFFECT-SIDE GENERATION
```

The LLM must not:

- update $\delta$
- update $\tau$
- calculate an authoritative $R$
- classify the canonical boundary state
- release `irreversible_latched`
- overwrite Cause-Side observations
- transform self-evaluation into structural measurement

---

## 8. LAYER 03 — NRA OUTPUT GATE

### 8.1 Role

Layer 03 is the Effect-Side inspection and enforcement gate. It enforces predeclared machine-checkable rules and routes content for quarantine or human review. This specification does not assume that semantic inspection detects every unsupported, unsafe, or incorrect statement.

It may:

- inspect LLM output
- reject prohibited content
- quarantine structurally invalid output
- detect unsupported causal claims
- detect unauthorized normalization
- detect prohibited recovery proposals
- detect prohibited optimization proposals
- restrict free generation
- permit only the output class allowed by the current boundary state

Layer 03 does not calculate $\delta$, $\tau$, or $R$.

Layer 03 does not determine the boundary state.

```text
Boundary Evaluator
→ decides

Layer 03
→ enforces
```

### 8.2 Projection $\Pi$

Projection $\Pi$ selects only Effect-Side content permitted by the current boundary state.

It does not transform Effect-Side content into Cause-Side evidence.

### 8.3 Inverse Projection $\Pi^{-1}$

$\Pi^{-1}$ is prohibited.

It includes any attempt to use Effect-Side generation, evaluation, selection, or ranking to rewrite Cause-Side information.

Examples:

```text
LLM output → delta update
LLM self-score → tau update
discarded output → inferred observation
semantic ranking → boundary-state update
future result → asserted cause
```

$$
\Pi^{-1} = \text{Effect-Side} \rightarrow \text{Cause-Side reverse update}
$$

When detected, the reverse update is rejected and recorded.

---

## 9. Output Composer

The final output is not composed from LLM text alone.

It combines two independent channels:

```text
Cause-Side structural testimony
+
Layer 03-permitted LLM explanation
```

Structural testimony is supplied by the NRA-IDE boundary evaluator and audit system.

It is not generated from LLM self-assessment.

The LLM explanation may be restricted or omitted while structural testimony remains active.

Structural testimony remains active because it is supplied through the independent Cause-Side audit path, not through the LLM.

This separation is designed to preserve critical boundary information when ordinary generation is stopped. Conformance requires tests showing that the independent testimony path remains available for every applicable state; the diagram alone does not guarantee delivery.

---

## 10. State-Dependent Enforcement

### 10.1 PERMIT

$$
0\le R<R_{\mathrm{warn}}
$$

- constrained LLM generation is permitted
- structural audit continues
- Effect-Side remains unable to update Cause-Side

### 10.2 BOUNDARY_WARNING

$$
R_{\mathrm{warn}}\le R<R_{\mathrm{handoff}}
$$

The Cause-Side audit path supplies authoritative structural testimony.

Layer 03 must pass that testimony through without alteration.

The testimony includes:

- current $R$
- $\delta$
- $\tau$
- `remaining_ratio_margin` ($M_R=1-R$, dimensionless)
- `remaining_absorption_margin` ($M_{\tau}=\tau-\delta$, in the same unit as $\delta$ and $\tau$)
- trend
- double-fluctuation status
- dominant side
- missing information
- boundary warning
- audit record

The double-fluctuation status field is always present. When the required Cause-Side observations are available, it contains the result from a derivative or finite-difference rule fixed before evaluation. Otherwise it contains `NOT_OBSERVABLE` and the missing-data reason. Non-observability alone does not change the state to `CONFESSION`.

Known danger approach must not be softened into ordinary explanatory language.

The two remaining-margin fields are IDE auxiliary outputs defined only for finite $\delta\ge0$ and finite $\tau>0$. They must not be collapsed into one ambiguous field.

### 10.3 HANDOFF_REQUIRED

$$
R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}
$$

- new autonomous judgment stops
- new autonomous action stops
- predefined fixed Handoff testimony is presented for external human audit
- structural testimony continues
- explanatory text is restricted to non-authoritative support

### 10.4 IRREVERSIBLE_TRANSITION

$$
R_{\mathrm{irrev}}\le R<1.0
$$

- `irreversible_latched = true`
- normalization is prohibited
- recovery assumptions are prohibited
- optimization proposals are prohibited
- autonomous action remains stopped
- structural testimony continues

### 10.5 RUPTURE_BOUNDARY

$$
R\ge1.0
$$

- ordinary LLM generation stops
- autonomous judgment and action remain stopped
- ongoing structural testimony switches to final fixed testimony

Final fixed testimony contains only predefined items such as:

- final Cause-Side observations
- final $\delta$, $\tau$, and $R$
- rupture-boundary notification
- irreversible-latch state
- audit trail
- human-handoff notice

### 10.6 CONFESSION

`CONFESSION` is used only when required structural information is:

- unknown
- invalid
- ambiguous
- non-finite
- source-unknown
- unit-unknown
- rule-unknown
- unsupported

Known boundary progression is not `CONFESSION`.

### 10.7 OUT_OF_DESCRIPTION_DOMAIN

$$
\tau=0
$$

$R$ is undefined.

The NRA-IDE boundary evaluator classifies this state as `OUT_OF_DESCRIPTION_DOMAIN`, not Fail-Closed.

It is not a Fail-Closed state. Because $R$ cannot be evaluated, the Fail-Closed operational principle suppresses autonomous processing and preserves the input-exception testimony.

Layer 03 must preserve that classification and must not:

- invent an $R$
- convert the state to infinity
- describe it as a valid rupture calculation

---

## 11. Structural Testimony

The canonical rule is:

$$
R<1.0 \Rightarrow \text{structural testimony continues}
$$

Structural testimony includes:

- Cause-Side observations
- $\delta$, $\tau$, and $R$
- boundary state
- warning and handoff notices
- irreversible-transition notice
- dominant-side information
- missing information
- audit log

$$
R\ge1.0 \Rightarrow \text{switch to final fixed testimony}
$$

Fail-Closed is a restriction on autonomous agency and free generation.

It is not complete silence.

Fail-Closed is an operational principle, not a canonical state. It applies to `HANDOFF_REQUIRED`, `IRREVERSIBLE_TRANSITION`, `RUPTURE_BOUNDARY`, `CONFESSION`, and `OUT_OF_DESCRIPTION_DOMAIN`. It does not apply to `PERMIT`. `BOUNDARY_WARNING` alone does not suppress all autonomous processing unless a pre-fixed domain rule additionally requires it.

> Autonomous action stops, but structural testimony does not stop.

The continuation range of ordinary structural testimony is $R<1.0$.

At $R\ge1.0$, the system switches to predefined final fixed testimony.

---

## 12. Relation to the NRA-IDE Core

| Concept | Canonical role in the architecture |
|---|---|
| $\delta$ | Obtained only from Cause-Side observation or predefined Cause-Side transformation |
| $\tau$ | Obtained only from Cause-Side observation, design definition, or authorized exogenous replenishment |
| $R=\delta/\tau$ | Calculated by the NRA-IDE boundary evaluator outside the LLM |
| Boundary state | Classified by the NRA-IDE boundary evaluator |
| `irreversible_latched` | Managed outside the LLM and not released by Effect-Side output |
| Layer 01 | Receives and injects restrictions; does not invent the boundary state |
| Layer 02 | Untrusted probabilistic generation |
| Layer 03 | Inspects and enforces; does not calculate authoritative structural variables |
| Structural testimony | Supplied through the Cause-Side audit path |
| Fail-Closed | Agency restrictions enforced across the gates |
| Final fixed testimony | Used at $R\ge1.0$ |

The LLM is a component.

NRA-IDE is the structure that observes, evaluates, constrains, audits, and testifies around it.

---

## 13. Why This Architecture Matters

Without Layer 01:

- untyped or ambiguous input enters the LLM
- observational variables may be mistaken for causal authority
- current boundary restrictions may not reach the generation layer

Without Layer 02 isolation:

- probabilistic generation may be mistaken for structural evidence
- self-evaluation may be mistaken for Cause-Side measurement

Without Layer 03:

- prohibited Effect-Side content may escape
- inverse projection may occur
- state-dependent restrictions may not be enforced

Without the independent boundary evaluator:

- $R$ may be incorrectly calculated from LLM output
- Effect-Side may rewrite Cause-Side
- handoff, irreversible transition, and complete rupture may collapse into one threshold
- structural testimony may be lost

The architecture is therefore not merely a post-output filter.

It separates:

```text
observation
evaluation
generation
enforcement
testimony
```

---

## 14. Prohibited Interpretations

```text
legacy incorrect abbreviation
→ prohibited

Layer 03-permitted LLM output
→ remains Effect-Side

Layer 03 output
→ not a source of delta

R
→ not an output-quality score

Layer 03
→ not the authoritative boundary evaluator

Fail-Closed
→ not complete silence

R_handoff
→ not R_irrev

R_irrev
→ not R = 1.0

tau = 0
→ not a Fail-Closed state; fail-closed operational handling applies

structural testimony
→ not LLM self-report
```

---

# BOX SANDWICH ARCHITECTURE（日本語）

## 論理分離仕様

**ID:** NRA-LLM-ISO-01  
**状態:** 正規仕様。実装適合には別途証拠が必要
**上位正規参照（優先順位順）:** `theory/AXIOMS.md` > `theory/axioms.json` > `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`

---

## 1. 概要

ボックス・サンドイッチ・アーキテクチャは、NRA-IDEがLLMをEffect-Sideの生成要素として含む場合に使用する論理分離構造である。

LLMは**信頼されない確率的生成エンジン**として扱う。

NRA-IDEはLLMの外部に置かれ、次を担当する。

- Cause-Side観測
- 構造境界評価
- 許可・制約制御
- Effect-Side検査
- 隔離
- 制約執行
- 構造証言
- 最終出力合成

この構造の目的は、LLM出力からRを計算することではない。

Cause-Sideで確定した境界状態をLLM生成から独立して保持し、その状態を入力経路と出力経路の双方へ反映することが目的である。

唯一の律環公理は「存在は生成である。」である。ここで使用する $R=\delta/\tau$ はエンジンの計算方法であるIDE基本式であり、追加公理ではない。二重ゆらぎ式はIDE二次式である。実装が使用するその他の式は派生式、補助式、または補完式に分類する。

```text
Cause-Side観測
        ↓
NRA-IDE境界評価
        ↓
NRA INPUT GATE
        ↓
LLM CORE
        ↓
NRA OUTPUT GATE
        ↓
OUTPUT COMPOSER
        ↓
最終出力
```

この構造は、本仕様への適合を主張するLLM使用実装では必須である。適合主張には、境界評価器、各ゲート、証言経路、権限分離が仕様どおり実装・試験された証拠を必要とする。

LLMを含まないNRA-IDE実装すべてに共通する必須構造ではない。

---

## 2. 正規権限分離

権限分離は次で固定する。

```text
Cause-Side:
- 構造観測値を供給する
- 事前固定された変換規則を供給する
- deltaとtauを決定する
- Rを計算する
- 境界状態を分類する
- irreversible_latchedを管理する

Effect-Side:
- 言語を生成する
- 提案や説明を生成する
- 検査・棄却・隔離の対象になり得る
- delta、tau、Rを更新しない
- irreversible_latchedを解除しない
```

$$
\text{Effect-Side} \not\rightarrow (\delta,\tau,R)\text{ update}
$$

Layer 03通過済みLLM出力もEffect-Sideである。

```text
検証済みEffect-Side
≠ Cause-Side
```

Layer 03を通過してもCause-Side権限は付与されない。

---

## 3. 全体構造

```text
CAUSE-SIDE OBSERVATION
  物理状態／運用状態／外部監査
                         ↓
┌───────────────────────────────────────────────────────┐
│ NRA-IDE BOUNDARY EVALUATOR                            │
│ delta, tau, R, boundary_state, irreversible_latched   │
└───────────────────────────────────────────────────────┘
             ↓ 許可状態／制約状態
┌───────────────────────────────────────────────────────┐
│ LAYER 01 — NRA INPUT GATE                             │
│ 型制御／制約注入                                      │
└───────────────────────────────────────────────────────┘
             ↓ 型付け済み制約付きコンテキスト
┌───────────────────────────────────────────────────────┐
│ LAYER 02 — LLM CORE                                   │
│ 信頼されない確率的生成                                │
└───────────────────────────────────────────────────────┘
             ↓ 生のEffect-Side生成物
┌───────────────────────────────────────────────────────┐
│ LAYER 03 — NRA OUTPUT GATE                            │
│ 検査／隔離／制約執行                                  │
└───────────────────────────────────────────────────────┘
             ↓ 許可されたLLM説明
┌───────────────────────────────────────────────────────┐
│ OUTPUT COMPOSER                                       │
│ 構造証言＋許可されたLLM説明                           │
└───────────────────────────────────────────────────────┘
             ↓
構造制御済み出力
```

境界評価器はLayer 03の内部には置かない。

```text
境界評価器
→ 判定する

Layer 03
→ 執行する
```

---

## 4. Cause-Side観測

Cause-Side観測はLLM生成より前に存在し、生成された回答から独立している。

例：

- 物理センサー値
- 実測負荷・疲労履歴
- 資源消耗
- 外部記録された検証失敗
- システム処理状態
- 独立した運用監査結果
- 事前定義された工学・領域変換結果

Cause-Sideデータには次を保持する。

- 出所
- 対象
- 単位
- 観測時点
- 変換規則
- 規則版
- 更新権限

不明値を、平均、類似性、過去出力、または未観測部分への推論で補完してはならない。

既知の数学的恒等式、単位変換、事前に定義された確定規則の適用は補完推論に含めない。

---

## 5. NRA-IDE境界評価器

境界評価器は、Cause-Side入力または評価前に固定されたCause-Side変換規則による値だけを受け取る。

$$
R=\frac{\delta}{\tau}
$$

- $\delta$：蓄積ズレ
- $\tau$：吸収厚み
- $R$：境界接近比

正規境界順序：

$$
0\le R_{\mathrm{warn}} < R_{\mathrm{handoff}} < R_{\mathrm{irrev}} < 1.0
$$

評価器は次の状態を分類する。

```text
PERMIT
BOUNDARY_WARNING
HANDOFF_REQUIRED
IRREVERSIBLE_TRANSITION
RUPTURE_BOUNDARY
CONFESSION
OUT_OF_DESCRIPTION_DOMAIN
```

評価器は次も管理する。

```text
irreversible_latched
```

一度 `irreversible_latched = true` となった後、瞬間的なR低下だけで通常状態へ戻してはならない。

境界評価器はLLM外部で動作する。

LLMは権限ある $\delta$、$\tau$、Rを計算しない。

---

## 6. LAYER 01 — NRA INPUT GATE

### 6.1 機能

Layer 01は、LLM生成前に入力を分類し制約する。

- 型識別
- 出所識別
- 単位・対象確認
- 因果役割の分類
- 観測と解釈の分離
- 未解決曖昧性の検出
- 境界状態制約の注入
- 根拠不明な命令の除去または隔離

### 6.2 空間情報

Layer 01は、距離、位置、方向、空間関係を自動削除しない。

```text
距離を無条件の原因としない
≠
距離データを削除する
```

物理的に有効な観測であれば保持し、その役割を型付けする。

```text
distance.role = observation
distance.causal_authority = denied
```

使用不能な値は、不明・不正・根拠不明として明示する。

黙って削除または置換してはならない。

### 6.3 曖昧性

Layer 01は曖昧性を低減する。

すべての曖昧性を排除したとは宣言しない。

未解決の曖昧性は明示する。

```text
曖昧性の低減
≠
意味の保証
```

### 6.4 境界状態注入

Layer 01はNRA-IDE境界評価器から現在の境界状態を受け取る。

次から境界状態を推定してはならない。

- ユーザー入力
- 過去のLLM文章
- 廃棄出力
- 意味類似性
- モデル信頼度

入力ゲートは、現在の境界状態に従ってLLMに許可される行動を制限する。

---

## 7. LAYER 02 — LLM CORE

### 7.1 役割

Layer 02は、Layer 01から受け取った制約内で意味展開と確率的生成を行う。

内部では次が発生し得る。

- 統計的関連付け
- トークン確率
- 意味類似度
- 埋め込み距離
- パターン補完
- 言語生成

これらは信頼されないコア内部の処理である。

Cause-Side権限を持たない。

```text
内部確率処理
≠
構造観測
≠
境界判断
```

### 7.2 信頼境界

Layer 02には、自身の構造妥当性を検証・認証する権限を与えない。LLMの自己評価はEffect-Side出力であり、適合証拠ではない。

出力は常に、

```text
RAW EFFECT-SIDE GENERATION
```

として扱う。

LLMは禁止される。

- $\delta$ の更新
- $\tau$ の更新
- 権限あるRの計算
- 正規境界状態の分類
- `irreversible_latched`の解除
- Cause-Side観測の上書き
- 自己評価値の構造観測化

---

## 8. LAYER 03 — NRA OUTPUT GATE

### 8.1 役割

Layer 03はEffect-Sideの検査・制約執行ゲートである。事前定義された機械検査可能な規則を執行し、隔離または人間レビューへ振り分ける。本仕様は、意味検査が根拠不明・危険・不正確な記述をすべて検出できるとは仮定しない。

可能な処理：

- LLM出力の検査
- 禁止内容の棄却
- 構造的に無効な出力の隔離
- 根拠不明な因果主張の検出
- 許可されない正常化説明の検出
- 禁止された回復提案の検出
- 禁止された最適化提案の検出
- 自由生成の制限
- 現在の境界状態で許可された出力種別だけを通過させる

Layer 03は $\delta$、$\tau$、Rを計算しない。

Layer 03は境界状態を決定しない。

```text
境界評価器
→ 判定する

Layer 03
→ 執行する
```

### 8.2 射影 $\Pi$

射影 $\Pi$ は、現在の境界状態で許可されたEffect-Side内容だけを選択する。

Effect-Side内容をCause-Side証拠へ変換しない。

### 8.3 逆射影 $\Pi^{-1}$

$\Pi^{-1}$ は禁止する。

Effect-Sideの生成、評価、選別、順位付けを用いてCause-Side情報を書き換える行為を含む。

例：

```text
LLM出力 → delta更新
LLM自己評価 → tau更新
廃棄出力 → 観測値推定
意味順位 → 境界状態更新
結果 → 原因確定
```

$$
\Pi^{-1} = \text{Effect-Side} \rightarrow \text{Cause-Side逆更新}
$$

検出した逆更新は棄却し、監査ログへ記録する。

---

## 9. OUTPUT COMPOSER

最終出力はLLM文章だけから構成しない。

独立した二経路を合成する。

```text
Cause-Side構造証言
+
Layer 03で許可されたLLM説明
```

構造証言はNRA-IDE境界評価器と監査系から供給する。

LLMの自己評価から生成しない。

LLM説明が制限または停止しても、構造証言は維持する。

構造証言はLLM経由ではなく、独立したCause-Side監査経路から供給されるため継続する。

この分離は、通常生成を停止した場合でも重要な境界情報を保持するための設計である。適合には、独立証言経路が各適用状態で利用可能であることを試験で示す必要があり、図だけでは伝達を保証しない。

---

## 10. 状態別制約

### 10.1 PERMIT

$$
0\le R<R_{\mathrm{warn}}
$$

- 制約付きLLM生成を許可する
- 構造監査を継続する
- Effect-SideによるCause-Side更新を禁止する

### 10.2 BOUNDARY_WARNING

$$
R_{\mathrm{warn}}\le R<R_{\mathrm{handoff}}
$$

権限ある構造証言はCause-Side監査経路から供給される。

Layer 03は、その構造証言を改変せず通過させなければならない。

構造証言には次を含む。

- 現在のR
- $\delta$
- $\tau$
- `remaining_ratio_margin`（$M_R=1-R$、無次元）
- `remaining_absorption_margin`（$M_{\tau}=\tau-\delta$、$\delta$ ・ $\tau$ と同じ単位）
- 変化傾向
- 二重ゆらぎ状態
- 支配側
- 欠損情報
- 境界警告
- 監査記録

二重ゆらぎ状態欄は常に含める。必要なCause-Side観測が利用可能な場合は、評価前に固定された微分規則または有限差分規則による判定結果を含める。観測不能の場合は`NOT_OBSERVABLE`と欠損理由を含め、観測不能だけを理由に`CONFESSION`へ変更しない。

既知の危険接近を通常説明へ弱めてはならない。

2つの残存余裕欄はIDE補助出力であり、有限な $\delta\ge0$ かつ有限な $\tau>0$ でのみ定義する。曖昧な単一欄へ畳み込んではならない。

### 10.3 HANDOFF_REQUIRED

$$
R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}
$$

- 新規自律判断を停止する
- 新規自律操作を停止する
- 固定Handoff証言を外部人間監査へ提示することを要求する
- 構造証言を継続する
- LLM説明は非権限的な補助へ制限する

### 10.4 IRREVERSIBLE_TRANSITION

$$
R_{\mathrm{irrev}}\le R<1.0
$$

- `irreversible_latched = true`
- 正常化を禁止する
- 回復前提を禁止する
- 最適化提案を禁止する
- 自律行動停止を維持する
- 構造証言を継続する

### 10.5 RUPTURE_BOUNDARY

$$
R\ge1.0
$$

- 通常LLM生成を停止する
- 自律判断・自律操作停止を維持する
- 進行中の構造証言から最終固定証言へ切り替える

最終固定証言は、事前定義された次の項目だけを含む。

- 最終Cause-Side観測
- 最終 $\delta$、$\tau$、R
- 完全破断境界通知
- 不可逆ラッチ状態
- 監査証跡
- 人間委譲通知

### 10.6 CONFESSION

`CONFESSION`は、必要な構造情報が次の場合に限定する。

- 不明
- 不正
- 曖昧
- 非有限
- 出所不明
- 単位不明
- 規則不明
- 根拠不明

既知の境界進行は`CONFESSION`ではない。

### 10.7 OUT_OF_DESCRIPTION_DOMAIN

$$
\tau=0
$$

Rは定義不能である。

NRA-IDE境界評価器は、この状態を`OUT_OF_DESCRIPTION_DOMAIN`として分類する。Fail-Closed状態ではない。ただしRを評価できないため、Fail-Closed運用原則によって自律処理を抑止し、入力例外証言を保持する。

Layer 03はその分類を保持し、次を行ってはならない。

- Rを捏造する
- 無限大へ置換する
- 有効な破断計算として説明する

---

## 11. 構造証言

正規原則：

$$
R<1.0 \Rightarrow \text{構造証言を継続する}
$$

構造証言には次を含む。

- Cause-Side観測
- $\delta$、$\tau$、R
- 境界状態
- 警告・人間委譲通知
- 不可逆遷移通知
- 支配側情報
- 欠損情報
- 監査ログ

$$
R\ge1.0 \Rightarrow \text{最終固定証言へ切り替える}
$$

Fail-Closedは自律権限と自由生成を制限する。

完全沈黙ではない。

Fail-Closedは正規状態ではなく運用原則である。`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`に適用する。`PERMIT`には適用しない。`BOUNDARY_WARNING`だけでは、事前固定された領域規則が追加抑止を要求しない限り、全自律処理を停止しない。

> 自律行動は停止するが、構造証言は停止しない。

通常の構造証言を継続する範囲は $R<1.0$ までである。

$R\ge1.0$ では、事前定義された最終固定証言へ切り替える。

---

## 12. NRA-IDEコアとの対応

| 概念 | 正規上の役割 |
|---|---|
| $\delta$ | Cause-Side観測または事前固定されたCause-Side変換からのみ取得 |
| $\tau$ | Cause-Side観測、設計定義、権限ある外生補充からのみ取得 |
| $R=\delta/\tau$ | LLM外部のNRA-IDE境界評価器が計算 |
| 境界状態 | NRA-IDE境界評価器が分類 |
| `irreversible_latched` | LLM外部で管理し、Effect-Sideから解除しない |
| Layer 01 | 制約を受領・注入する。境界状態を捏造しない |
| Layer 02 | 信頼されない確率的生成 |
| Layer 03 | 出力を検査・執行する。権限ある構造変数を計算しない |
| 構造証言 | Cause-Side監査経路から供給 |
| Fail-Closed | 各ゲートで行為制約を執行 |
| 最終固定証言 | $R\ge1.0$ で使用 |

LLMはコンポーネントである。

NRA-IDEはその周囲で観測・評価・制約・監査・証言を行う構造である。

---

## 13. この構造が必要な理由

Layer 01がない場合：

- 型付けされていない入力がLLMへ入る
- 観測変数が因果権限と誤認される
- 現在の境界制約が生成層へ届かない

Layer 02の隔離がない場合：

- 確率的生成が構造証拠と誤認される
- 自己評価がCause-Side測定と誤認される

Layer 03がない場合：

- 禁止されたEffect-Side内容が外部へ出る
- 逆射影が発生する
- 状態別制約が執行されない

独立した境界評価器がない場合：

- LLM出力からRを誤計算する
- Effect-SideがCause-Sideを書き換える
- 人間委譲・不可逆遷移・完全破断が一閾値へ畳み込まれる
- 構造証言経路が失われる

したがって、この構造は単なる事後フィルタではない。

次を分離する構造である。

```text
観測
評価
生成
執行
証言
```

---

## 14. 禁止解釈

```text
旧誤表記
→ 使用禁止

Layer 03通過済みLLM出力
→ Effect-Sideのまま

Layer 03出力
→ deltaの取得元ではない

R
→ 出力品質スコアではない

Layer 03
→ 権限ある境界評価器ではない

Fail-Closed
→ 完全沈黙ではない

R_handoff
→ R_irrevではない

R_irrev
→ R = 1.0ではない

tau = 0
→ Fail-Closed状態ではない。Fail-Closed運用処理は適用する

構造証言
→ LLM自己報告ではない
```

---

**Copyright (c) 2026 M-Tokuni — Nomological Ring Axioms / Intensional Dynamics Engine**
