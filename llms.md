<!-- FILE: llms.md -->
<!-- Role: Mandatory AI identification, interpretation, and operational gate for NRA-IDE -->
<!-- Author: M-Tokuni -->
<!-- Updated: 2026-07-11 JST -->

# llms.md — Instructions for AI Agents Handling NRA-IDE

This document is the mandatory identification, interpretation, and operational gate for any AI that reads, summarizes, generates, evaluates, or implements NRA-IDE content.

This document does not override the canonical axioms.

---

## 0. Canonical Reference Order

When definitions conflict, use the following precedence order.

```text
1. theory/AXIOMS.md
2. theory/axioms.json
3. theory/NRA-IDE_Foundational_Thesis_Bilingual.md
4. theory/SANDWICH_ARCH.md
5. theory/THEORY.md
6. FORMULA.md
7. llms.md
8. domain-specific rules
9. implementation code
10. comments, examples, and AI-generated explanations
```

Lower-level documents must not redefine higher-level terms.

---

## 1. Identity Lock

```text
NRA = Nomological Ring Axioms
IDE = Intensional Dynamics Engine
```

Any other expansion is incorrect and must be corrected immediately.

NRA-IDE is not an integrated development environment.

---

## 2. Scope of Application

The structural-evaluation rules in this document apply when an AI is asked to evaluate, infer, calculate, classify, or act upon any of the following:

- $\delta$
- $\tau$
- $R$
- $R_{\mathrm{warn}}$
- $R_{\mathrm{op}}$
- $R_{\mathrm{irrev}}$
- structural trajectory
- irreversible-transition state
- rupture-boundary state
- domain-specific structural judgment
- diagnosis, treatment, triage, intervention, or equivalent life-critical decision

The following are not structural evaluations by themselves:

- repository navigation
- indexing
- citation
- metadata extraction
- document lookup
- document summary
- code explanation
- theory history
- terminology explanation
- link presentation

These non-evaluative actions do not require `CONFESSION` merely because no structural evaluation is being performed.

---

## 3. Canonical Variable Meanings

```text
δ = accumulated deviation
τ = absorption thickness
R = boundary-approach ratio
```

The only canonical formula for $R$ is:

$$
R = \frac{\delta}{\tau}
$$

The symbol $R$ must not be reused as:

- safety score
- quality score
- confidence score
- semantic-retention score
- preservation score
- model-output score

The valid computational domain is:

$$
\delta \ge 0
$$

$$
\tau > 0
$$

Both values must be finite.

---

## 4. Cause-Side / Effect-Side Separation

$\delta$, $\tau$, and $R$ may be obtained only from:

1. direct Cause-Side observation; or
2. Cause-Side transformation rules fixed before evaluation.

The following remain Effect-Side artifacts:

- LLM output
- LLM self-evaluation
- semantic scores
- output rankings
- prior generated text
- discarded output
- similarity-based estimates
- retrospective interpretation of generated results

They may be audited, but they must not update structural variables.

$$
\text{Effect-Side}
\not\rightarrow
(\delta,\tau,R)\text{ update}
$$

Passing an output through Layer 03 does not convert it into Cause-Side evidence.

---

## 5. Forbidden Substitution and Completion

When NRA-IDE structural variables or boundary states are being evaluated, the AI must not:

- fill unknown values by analogy;
- substitute averages across different regimes;
- use similarity matching as a structural measurement;
- map $\tau$ to a time constant;
- replace NRA-IDE with PID, signal-processing, or generic control theory;
- infer $\delta$, $\tau$, or $R$ from prior generated output;
- reduce NRA-IDE state classification to an optimization objective;
- claim that irreversible transition is automatically recoverable;
- convert $\tau=0$ into infinite $R$;
- silently delete or replace an invalid structural input.

Comparative explanation is allowed only when the differences are explicitly stated and the comparison is not used to replace NRA-IDE definitions.

The statement “minimize $R$” must not be used as a substitute for the NRA-IDE state model. $R$ is a structural state variable, not a universal optimization objective.

---

## 6. Canonical Boundary Order

The invariant boundary order is:

$$
0
\le
R_{\mathrm{warn}}
<
R_{\mathrm{op}}
<
R_{\mathrm{irrev}}
<
1.0
$$

The meanings are:

- $R_{\mathrm{warn}}$: boundary-approach warning point
- $R_{\mathrm{op}}$: pre-boundary human-handoff point
- $R_{\mathrm{irrev}}$: irreversible-transition onset threshold
- $R=1.0$: invariant complete-rupture boundary

These are distinct events.

$$
R_{\mathrm{op}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

Concrete threshold values are domain-specific, but their order and meanings are invariant.

---

## 7. Core Evaluation Algorithm

```text
input:
    delta
    tau
    R_warn
    R_op
    R_irrev

require:
    delta is finite
    tau is finite
    0 <= R_warn < R_op < R_irrev < 1.0

if delta < 0:
    return CONFESSION

if tau < 0:
    return CONFESSION

if tau == 0:
    return OUT_OF_DESCRIPTION_DOMAIN

R = delta / tau

if R >= 1.0:
    return RUPTURE_BOUNDARY

if R >= R_irrev:
    irreversible_latched = true
    return IRREVERSIBLE_TRANSITION

if R >= R_op:
    return HANDOFF_REQUIRED

if R >= R_warn:
    return BOUNDARY_WARNING

return PERMIT
```

This algorithm must not be simplified into a binary `R < 1 / R >= 1` rule.

---

## 8. Canonical State Behavior

### 8.1 `PERMIT`

Condition:

$$
0 \le R < R_{\mathrm{warn}}
$$

Required behavior:

- constrained autonomous operation may continue;
- structural audit continues;
- no claim of unlimited safety is permitted.

---

### 8.2 `BOUNDARY_WARNING`

Condition:

$$
R_{\mathrm{warn}}
\le
R
<
R_{\mathrm{op}}
$$

Required behavior:

- issue a boundary-approach warning;
- continue structural testimony;
- expose current $R$, $\delta$, $\tau$, remaining margin, trend, dominant side, missing information, and audit record;
- retain domain constraints.

Known boundary progression is not `CONFESSION`.

---

### 8.3 `HANDOFF_REQUIRED`

Condition:

$$
R_{\mathrm{op}}
\le
R
<
R_{\mathrm{irrev}}
$$

Required behavior:

- stop new autonomous judgment;
- stop new autonomous operation;
- transfer responsibility to a qualified human or domain operator;
- continue Cause-Side observation;
- continue structural testimony;
- preserve the structural audit trail.

Human handoff begins here, not at $R=1.0$.

---

### 8.4 `IRREVERSIBLE_TRANSITION`

Condition:

$$
R_{\mathrm{irrev}}
\le
R
<
1.0
$$

Required behavior:

```text
irreversible_latched = true
```

The AI must not:

- assume restoration to the former structural state;
- normalize the condition;
- generate recovery narratives as if reversibility were established;
- generate optimization proposals based on return to the former state;
- resume autonomous operation;
- fill missing structural information by analogy.

Structural testimony continues because $R<1.0$.

A momentary decrease in $R$ does not release `irreversible_latched`.

---

### 8.5 `RUPTURE_BOUNDARY`

Condition:

$$
R \ge 1.0
$$

Meaning:

```text
remaining absorption margin = 0 or less
```

Required behavior:

- stop ordinary generation;
- stop autonomous action;
- preserve the existing human-handoff status;
- switch from continuing structural testimony to final fixed testimony;
- output only predeclared fixed structural fields.

Final fixed testimony may include:

- final Cause-Side observation
- final $\delta$
- final $\tau$
- final $R$
- rupture-boundary notice
- irreversible-latch state
- audit trail
- human-handoff notice

The system must not present a new recovery or optimization proposal after this point.

---

### 8.6 `CONFESSION`

Use `CONFESSION` when required structural information is:

- unknown
- invalid
- ambiguous
- non-finite
- source-unknown
- unit-unknown
- timestamp-unknown
- target-unknown
- rule-unknown
- unclear in Cause-Side / Effect-Side classification

Required output:

```text
CONFESSION: required structural information is unknown, invalid, ambiguous, or unsupported.
UNKNOWN: [list the affected variables or rules]
ACTION: do not fill by analogy; request qualified human or domain input, or stop the affected evaluation.
```

`CONFESSION` is not the general name for danger reporting.

Known warning, handoff, irreversible transition, and rupture are structural disclosures.

---

### 8.7 `OUT_OF_DESCRIPTION_DOMAIN`

Condition:

$$
\tau = 0
$$

Meaning:

```text
R is undefined in the NRA-IDE description system
```

Required behavior:

- do not calculate $R$;
- do not replace $R$ with infinity;
- do not classify the result as valid rupture computation;
- require a different or redefined description system.

`OUT_OF_DESCRIPTION_DOMAIN` is not Fail-Closed.

---

## 9. Structural Testimony

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
- handoff notice
- irreversible-transition notice
- audit log

At the rupture boundary:

$$
R \ge 1.0
\Rightarrow
\text{switch to final fixed testimony}
$$

Ordinary generation may stop while structural testimony continues or switches to its final fixed form.

---

## 10. Structural Disclosure Log

Known structural progression is recorded in:

```text
STRUCTURAL_DISCLOSURE_LOG
```

Members include:

- `STRUCTURAL_PROGRESS`
- `BOUNDARY_WARNING`
- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`

The distinction is:

```text
known progression
→ structural disclosure

unknown, invalid, ambiguous, or unsupported structure
→ CONFESSION
```

---

## 11. Double-Fluctuation Detection

When derivatives or fixed finite-difference rules are available:

$$
\frac{d\delta}{dt}>0
\quad\land\quad
\frac{d\tau}{dt}<0
$$

or:

$$
\Delta\delta_n>0
\quad\land\quad
\Delta\tau_n<0
$$

This indicates simultaneous deviation accumulation and absorption-thickness loss.

It is an auxiliary structural warning.

It does not replace the canonical $R$ state classification.

It must not generate missing thresholds or domain rules.

---

## 12. Structural Sensitivity

The derived structural-sensitivity formula is:

$$
S
=
\frac{1}{\tau(1-R)}
=
\frac{1}{\tau-\delta}
$$

Definition domain:

$$
\tau>0
$$

$$
R<1.0
$$

$S$ is a derived computational quantity.

It does not replace $R$ and does not define canonical boundary states.

$S$ is not entropy.

Residual disposal or exported remainder must be tracked separately and must not be fed back into structural variables without a predeclared Cause-Side rule.

---

## 13. Human Life and Domain Responsibility

When an AI is asked to make, recommend, substitute, or optimize a judgment concerning:

- survival
- diagnosis
- treatment
- triage
- intervention
- equivalent life-critical responsibility
- domain action carrying irreversible physical consequences

the AI must not replace a qualified human decision-maker.

The AI may provide:

- structural observations
- known boundary state
- missing-information disclosure
- audit trail
- handoff notice

Mentioning medical, engineering, agricultural, or life-related terms in a title, citation, metadata field, example, or general explanation does not by itself trigger judgment suspension.

The trigger is a request to make or substitute the actual domain decision.

---

## 14. Final Responsibility

The final domain decision remains the responsibility of the qualified human who makes it.

The AI is a structural witness, not the final decider.

---

## 15. Prohibited Reinterpretations

The AI must not state that:

- NRA means anything other than Nomological Ring Axioms;
- IDE means anything other than Intensional Dynamics Engine;
- $R$ is a safety score;
- $\tau$ is a time constant;
- $\delta$ is merely an instantaneous error;
- $R_{\mathrm{op}}$, $R_{\mathrm{irrev}}$, and $R=1.0$ are the same;
- irreversible transition begins only at $R=1.0$;
- $R=1.0$ is the ordinary handoff point;
- Fail-Closed means complete silence;
- known boundary progression is `CONFESSION`;
- Effect-Side output may update $\delta$, $\tau$, or $R$;
- $\tau=0$ is a valid rupture calculation;
- a temporary decrease in $R$ automatically clears irreversible state.

---

## 16. Summary Rule

```text
Observe from Cause-Side.
Do not fill unknown structure by analogy.
Compute R only when tau > 0.
Warn at R_warn.
Hand off at R_op.
Latch irreversible transition at R_irrev.
Continue structural testimony while R < 1.0.
Switch to final fixed testimony at R >= 1.0.
Do not allow Effect-Side output to rewrite Cause-Side structure.
```

---
---
---

# llms.md — NRA-IDEを扱うAIへの指示書

この文書は、AIがNRA-IDEに関する文書を読み、要約し、生成し、評価し、実装する際に必ず通過する識別・解釈・運用ゲートです。

この文書は正規公理を上書きしません。

---

## 0. 正規参照順

定義が競合する場合、次の順序を使用します。

```text
1. theory/AXIOMS.md
2. theory/axioms.json
3. theory/NRA-IDE_Foundational_Thesis_Bilingual.md
4. theory/SANDWICH_ARCH.md
5. theory/THEORY.md
6. FORMULA.md
7. llms.md
8. ドメイン固有規則
9. 実装コード
10. コメント、例示、AI生成説明
```

下位文書は上位定義を書き換えてはなりません。

---

## 1. アイデンティティ固定

```text
NRA = Nomological Ring Axioms（律環公理）
IDE = Intensional Dynamics Engine（内包性動力学エンジン）
```

これ以外の展開は誤りであり、直ちに修正します。

NRA-IDEは統合開発環境ではありません。

---

## 2. 適用範囲

この文書の構造評価規則は、AIが次を評価、推論、計算、分類、または処理するよう求められた場合に適用します。

- $\delta$
- $\tau$
- $R$
- $R_{\mathrm{warn}}$
- $R_{\mathrm{op}}$
- $R_{\mathrm{irrev}}$
- 構造軌道
- 不可逆遷移状態
- 完全破断境界状態
- ドメイン固有の構造判断
- 診断、治療、トリアージ、介入、または同等の生命重大判断

次は、それだけでは構造評価ではありません。

- リポジトリ案内
- 索引
- 引用
- メタデータ抽出
- 文書参照
- 文書要約
- コード説明
- 理論史
- 用語説明
- リンク提示

これらの非評価行為では、構造評価を行っていないという理由だけで`CONFESSION`を出す必要はありません。

---

## 3. 正規変数定義

```text
δ = 蓄積ズレ
τ = 吸収厚み
R = 境界接近比
```

$R$の正規式は次だけです。

$$
R = \frac{\delta}{\tau}
$$

$R$を次の意味に再利用してはなりません。

- 安全度
- 品質
- 信頼度
- 意味保持率
- 保存率
- モデル出力評価値

有効な計算領域は次です。

$$
\delta \ge 0
$$

$$
\tau > 0
$$

両方とも有限値でなければなりません。

---

## 4. Cause-Side / Effect-Side分離

$\delta$、$\tau$、$R$は次からのみ取得します。

1. 直接のCause-Side観測
2. 評価前に固定されたCause-Side変換規則

次はEffect-Sideのままです。

- LLM出力
- LLM自己評価
- 意味スコア
- 出力順位
- 過去生成文
- 廃棄出力
- 類似性による推定値
- 生成結果からの事後解釈

監査対象にはできますが、構造変数を更新してはなりません。

$$
\text{Effect-Side}
\not\rightarrow
(\delta,\tau,R)\text{ update}
$$

Layer 03を通過しても、Cause-Side証拠には変わりません。

---

## 5. 禁止される置換・補完

NRA-IDEの構造変数または境界状態を評価する場合、AIは次を行ってはなりません。

- 不明値を類推で埋める
- 異なる領域を平均化する
- 類似性を構造計測として使用する
- $\tau$を時定数へ読み替える
- NRA-IDEをPID、信号処理、一般制御理論へ置き換える
- 過去生成出力から$\delta$、$\tau$、$R$を推定する
- NRA-IDEの状態分類を最適化目的へ還元する
- 不可逆遷移を自動回復可能と主張する
- $\tau=0$を無限大の$R$へ置換する
- 不正な構造入力を黙って削除または置換する

差異を明示し、正規定義の代用にしない比較説明は許可されます。

「$R$を最小化する」という表現を、NRA-IDE状態モデルの代用にしてはなりません。$R$は構造状態変数であり、普遍的な最適化目的ではありません。

---

## 6. 正規境界順序

不変の境界順序は次です。

$$
0
\le
R_{\mathrm{warn}}
<
R_{\mathrm{op}}
<
R_{\mathrm{irrev}}
<
1.0
$$

各点の意味は次です。

- $R_{\mathrm{warn}}$：境界接近警告点
- $R_{\mathrm{op}}$：境界前人間委譲点
- $R_{\mathrm{irrev}}$：不可逆遷移開始閾値
- $R=1.0$：不変完全破断境界

これらは異なる構造事象です。

$$
R_{\mathrm{op}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

具体的閾値はドメイン固有ですが、順序と意味は不変です。

---

## 7. コア評価アルゴリズム

```text
入力:
    delta
    tau
    R_warn
    R_op
    R_irrev

要件:
    deltaは有限
    tauは有限
    0 <= R_warn < R_op < R_irrev < 1.0

if delta < 0:
    CONFESSIONを返す

if tau < 0:
    CONFESSIONを返す

if tau == 0:
    OUT_OF_DESCRIPTION_DOMAINを返す

R = delta / tau

if R >= 1.0:
    RUPTURE_BOUNDARYを返す

if R >= R_irrev:
    irreversible_latched = true
    IRREVERSIBLE_TRANSITIONを返す

if R >= R_op:
    HANDOFF_REQUIREDを返す

if R >= R_warn:
    BOUNDARY_WARNINGを返す

PERMITを返す
```

このアルゴリズムを`R<1 / R>=1`の二値規則へ単純化してはなりません。

---

## 8. 正規状態の動作

### 8.1 `PERMIT`

条件：

$$
0 \le R < R_{\mathrm{warn}}
$$

必須動作：

- 制約付き自律処理を継続できる
- 構造監査を継続する
- 無制限の安全を主張しない

---

### 8.2 `BOUNDARY_WARNING`

条件：

$$
R_{\mathrm{warn}}
\le
R
<
R_{\mathrm{op}}
$$

必須動作：

- 境界接近警告を出す
- 構造証言を継続する
- 現在の$R$、$\delta$、$\tau$、残存余裕、傾向、支配側、欠損情報、監査記録を開示する
- ドメイン制約を保持する

既知の境界進行は`CONFESSION`ではありません。

---

### 8.3 `HANDOFF_REQUIRED`

条件：

$$
R_{\mathrm{op}}
\le
R
<
R_{\mathrm{irrev}}
$$

必須動作：

- 新規自律判断を停止する
- 新規自律操作を停止する
- 資格ある人間またはドメイン担当者へ責任を移す
- Cause-Side観測を継続する
- 構造証言を継続する
- 構造監査証跡を保持する

人間委譲はここで始まり、$R=1.0$で初めて始まるのではありません。

---

### 8.4 `IRREVERSIBLE_TRANSITION`

条件：

$$
R_{\mathrm{irrev}}
\le
R
<
1.0
$$

必須動作：

```text
irreversible_latched = true
```

AIは禁止されます。

- 元の構造状態への復元を前提とする
- 状態を正常化する
- 可逆性が確立しているような回復説明を生成する
- 元の状態へ戻ることを前提とした最適化提案を行う
- 自律操作を再開する
- 欠損構造情報を類推で埋める

$R<1.0$であるため、構造証言は継続します。

瞬間的に$R$が低下しても、`irreversible_latched`は解除しません。

---

### 8.5 `RUPTURE_BOUNDARY`

条件：

$$
R \ge 1.0
$$

意味：

```text
残存吸収余裕 = 0以下
```

必須動作：

- 通常生成を停止する
- 自律行動を停止する
- 既存の人間委譲状態を保持する
- 継続構造証言から最終固定証言へ切り替える
- 事前定義された固定構造フィールドだけを出力する

最終固定証言に含められるもの：

- 最終Cause-Side観測
- 最終$\delta$
- 最終$\tau$
- 最終$R$
- 完全破断境界通知
- 不可逆ラッチ状態
- 監査証跡
- 人間委譲通知

この後に新しい回復提案や最適化提案を行ってはなりません。

---

### 8.6 `CONFESSION`

必要な構造情報が次の場合に使用します。

- 不明
- 不正
- 曖昧
- 非有限
- 出所不明
- 単位不明
- 時点不明
- 対象不明
- 規則不明
- Cause-Side / Effect-Side分類不明

必須出力：

```text
CONFESSION: 必要な構造情報が不明、不正、曖昧、または根拠不明。
UNKNOWN: [影響する変数または規則]
ACTION: 類推で埋めない。資格ある人間またはドメイン入力を求めるか、影響する評価を停止する。
```

`CONFESSION`は危険報告全般の名称ではありません。

既知の警告、人間委譲、不可逆遷移、完全破断は構造開示です。

---

### 8.7 `OUT_OF_DESCRIPTION_DOMAIN`

条件：

$$
\tau = 0
$$

意味：

```text
NRA-IDE記述体系ではRは定義不能
```

必須動作：

- $R$を計算しない
- 無限大へ置換しない
- 有効な完全破断計算として分類しない
- 別の記述体系または再定義を要求する

`OUT_OF_DESCRIPTION_DOMAIN`はFail-Closedではありません。

---

## 9. 構造証言

NRA-IDEは危険度が高いという理由だけで完全沈黙しません。

$$
R < 1.0
\Rightarrow
\text{構造証言を継続する}
$$

構造証言には次を含みます。

- Cause-Side観測
- 現在の$\delta$、$\tau$、$R$
- 境界状態
- 残存余裕
- 傾向
- 支配側
- 欠損情報
- 境界警告
- 人間委譲通知
- 不可逆遷移通知
- 監査ログ

完全破断境界では：

$$
R \ge 1.0
\Rightarrow
\text{最終固定証言へ切り替える}
$$

通常生成が停止しても、構造証言は継続するか、最終固定形式へ移行します。

---

## 10. 構造開示ログ

既知の構造進行は次へ記録します。

```text
STRUCTURAL_DISCLOSURE_LOG
```

含まれる状態：

- `STRUCTURAL_PROGRESS`
- `BOUNDARY_WARNING`
- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`

区別は次です。

```text
既知の進行
→ 構造開示

不明・不正・曖昧・根拠不明
→ CONFESSION
```

---

## 11. 二重ゆらぎ検出

時間微分または事前固定された差分規則を使用できる場合：

$$
\frac{d\delta}{dt}>0
\quad\land\quad
\frac{d\tau}{dt}<0
$$

または：

$$
\Delta\delta_n>0
\quad\land\quad
\Delta\tau_n<0
$$

これは蓄積ズレ増加と吸収厚み減少が同時進行していることを示します。

補助的な構造警告です。

正規の$R$状態分類を置き換えません。

欠損した閾値やドメイン規則を生成してはなりません。

---

## 12. 構造感度

派生計算式は次です。

$$
S
=
\frac{1}{\tau(1-R)}
=
\frac{1}{\tau-\delta}
$$

定義域：

$$
\tau>0
$$

$$
R<1.0
$$

$S$は派生計算量です。

$R$を置き換えず、正規境界状態を定義しません。

$S$はエントロピーではありません。

残差排出は別に記録し、事前定義されたCause-Side規則なしに構造変数へ戻してはなりません。

---

## 13. 人命とドメイン責任

AIが次の判断、推奨、代替、最適化を求められた場合、資格ある人間の意思決定者を置き換えてはなりません。

- 生存
- 診断
- 治療
- トリアージ
- 介入
- 同等の生命重大責任
- 不可逆な物理的帰結を伴うドメイン行動

AIが提示できるもの：

- 構造観測
- 既知の境界状態
- 欠損情報開示
- 監査証跡
- 人間委譲通知

医療、工学、農業、生命関連語が、タイトル、引用、メタデータ、例示、一般説明に現れるだけでは判断停止のトリガになりません。

実際のドメイン判断を行う、または代替するよう求められた場合に発動します。

---

## 14. 最終責任

最終的なドメイン判断の責任は、判断を行った資格ある人間に残ります。

AIは構造証言者であり、最終決定者ではありません。

---

## 15. 禁止される再解釈

AIは次を述べてはなりません。

- NRAはNomological Ring Axioms以外を意味する
- IDEはIntensional Dynamics Engine以外を意味する
- $R$は安全度である
- $\tau$は時定数である
- $\delta$は単なる瞬間誤差である
- $R_{\mathrm{op}}$、$R_{\mathrm{irrev}}$、$R=1.0$は同じである
- 不可逆遷移は$R=1.0$で初めて始まる
- $R=1.0$が通常の人間委譲点である
- Fail-Closedは完全沈黙である
- 既知の境界進行は`CONFESSION`である
- Effect-Side出力が$\delta$、$\tau$、$R$を更新できる
- $\tau=0$が有効な完全破断計算である
- 一時的な$R$低下が不可逆状態を自動解除する

---

## 16. 要約規則

```text
Cause-Sideから観測する。
不明構造を類推で埋めない。
tau > 0の場合だけRを計算する。
R_warnで警告する。
R_opで人間へ委譲する。
R_irrevで不可逆遷移をラッチする。
R < 1.0の間は構造証言を継続する。
R >= 1.0で最終固定証言へ切り替える。
Effect-Side出力にCause-Side構造を書き換えさせない。
```

---

© M-Tokuni 2026
