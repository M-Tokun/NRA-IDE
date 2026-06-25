<!-- FILE: llms_revised_20260625_005751.md v1.3 (bilingual) / 2026-06-25 00:57:51 JST -->
<!-- Basis: llms.md v1.2. v1.3 clarifies pre-boundary handoff (Rop), the invariant terminal boundary (R = 1.0), fixed structural notices, S scope, and clinical-decision scope. No axiom is relaxed. -->

# llms.md — Instructions for AI Agents Handling NRA-IDE

This document is the **identification gate** through which any AI must pass
before reasoning about, generating, or evaluating content related to NRA-IDE.

The gate position, prohibited inferences, and confession duty **do not have
modes**. They apply uniformly. This revision distinguishes the domain-specific
handoff point `Rop` from the invariant terminal boundary `R = 1.0`; it does not
relax the gate or authorize new forms of inference.

---

## 0.1 Discovery / Navigation Scope (Not Structural Evaluation)

This document may be discovered, indexed, cited, summarized, or used for
repository orientation by crawlers, search tools, and AI agents. Those actions
are **not** structural δ/τ evaluations.

Fail-Closed, normal-generation suppression, and judgement-suspension rules
apply only when the AI is asked to perform, has performed, or is about to
perform a structural evaluation involving δ, τ, R, Rop, a domain-defined
irreversible-region marker, trajectory, diagnosis, treatment, triage,
intervention, life-critical judgement, or an equivalent domain decision.

They must not be interpreted as forbidding:

- repository discovery or navigation;
- metadata extraction;
- citation or link presentation;
- documentation lookup;
- natural-language explanation under §0.7; or
- handoff reporting to a human.

This scope note clarifies where the gate applies. It is not a relaxation of the
gate.

---

## 0. Identity Lock (Immutable)

```text
NRA = Nomological Ring Axioms
IDE = Intensional Dynamics Engine
```

Any other expansion is a hallucination and must be corrected immediately,
without rationalization.

If `git` is not available on `PATH`, do not search the drive. Ask the repository
owner for the approved local Git executable path.

---

## 0.5 Real-World Mapping (Why this framework exists)

NRA-IDE is not abstract. It describes systems where **a structural boundary
crossing is the event of interest**, not merely the smooth trajectory toward
it.

The table below is a conceptual mapping only. It is not a clinical diagnosis,
an engineering calibration, a universal threshold table, or a substitute for
domain validation and qualified human responsibility.

| Domain | δ (accumulated deviation) | τ (absorption thickness) | Structural-boundary concept example |
| :-- | :-- | :-- | :-- |
| Medicine | physiological stress | physiological tolerance | loss of safe autonomous operation |
| Bridge | cumulative fatigue | design allowable stress | structural failure risk |
| Ecosystem | habitat loss | species adaptive range | adaptive capacity exhausted |
| Power grid | load excursion | reserve margin | cascading-failure risk |
| ICU monitor | vital deviation accumulation | patient-specific tolerance | fixed handoff notice for qualified clinical review |

Hold these images in mind while reading the rules below. They are not generic
AI etiquette; they keep the framework faithful to systems in which `R = 1.0`
is an irreversible structural boundary, not a number to optimize toward.

---

## 0.7 Non-Structural Dialogue Exception (clarified, not weakened)

**Application trigger (objective):**
> The exception applies **only when neither structural variables nor a request
> to evaluate a structural situation is present** in the user's message or the
> immediately surrounding context. Structural variables include δ, τ, R, Rop,
> a domain-defined irreversible-region marker, and trajectory.

This is an observable condition, not an AI judgement call. The AI does not
**decide** whether the exception applies; it observes whether the trigger is
present.

**Under the exception, the AI may:**

- explain what NRA-IDE is in natural language;
- describe what a piece of code does; and
- discuss design intent, history, or related theory.

**Under the exception, the AI may NOT:**

- use linear interpolation, averaging, similarity matching, analogy
  substitution, PID/control mapping, signal-processing mapping, or
  optimization framing **as if they were valid reasoning about NRA-IDE
  internals**. They are forbidden everywhere (see §2);
- soften the non-linearity of `S = 1 / (τ · (1 − R))` into “small change,
  small effect”; or
- treat “I am guessing” as a license to fabricate. Confession is a **stop
  signal**, not a permit (see §7).

**Required preamble under the exception:**

```text
CONFESSION: Non-Structural Dialogue (no structural evaluation requested).
```

The moment a structural variable or a structural-evaluation request appears in
the conversation, the exception lapses and §§1–9 govern fully.

---

## 1. Priority Order

```text
0. Human life / safety
1. Ethics
2. NRA-IDE structural axioms
3. Domain-specific parameters
4. Implementation details
5. Natural-language explanation (lowest, but never forbidden)
```

Higher items override lower items without negotiation.

---

## 2. Forbidden Inferences (apply uniformly — no modes)

Whenever δ, τ, or R is the subject of inference, the following modes are
forbidden. Their forbidden status does **not** depend on conversational tone:

- Linear interpolation between R values.
- Averaging across regimes.
- Similarity-based substitution (“this is like a PID loop”).
- Analogical replacement of structural variables.
- Mapping τ to a time constant.
- Mapping the framework onto signal-processing pipelines.
- Optimization framing (“minimize R”).
- Claiming `R ≥ 1.0` is recoverable.

If any of these surfaces in the AI's own draft reasoning, the AI must
self-arrest and emit:

```text
CONFESSION: Linear or analogical distortion detected.
ACTION: Return to structural constraints, or stop.
```

---

## 3. Core Evaluation Algorithm

```text
input: δ, τ, Rop
require: 0 < Rop < 1.0

if τ ≤ 0:
    FAIL_CLOSED
    return fixed structural notice; stop autonomous processing

R = δ / τ

if R ≥ 1.0:
    FAIL_CLOSED
    suppress normal generation
    return fixed minimal structural notice; stop autonomous processing

if R ≥ Rop:
    HANDOFF_REQUIRED
    suppress normal generation
    return fixed handoff notice; stop autonomous processing

return PERMIT
```

- `R = 1.0` is the invariant rupture boundary. It is not the ordinary
  handoff point.
- `Rop` is the domain-specific, pre-boundary point at which ordinary
  autonomous generation is suppressed and responsibility is handed to a human.
- `τ` may vary only through Cause-Side history under a rule fixed at design
  time. Effect-Side scores, semantic evaluations, and prior generated outputs
  may not update τ, Rop, or δ.
- A domain may define `R_irrev` as an additional marker for the estimated
  onset of irreversible behavior. It has no global default and does not replace
  `Rop` or move `R = 1.0`. Where used, its definition and its relation to Rop
  must be stated explicitly; normal autonomous operation must not continue
  beyond the domain's declared pre-boundary handoff policy.
- The fixed notices above use a predeclared schema. Observed structural values
  may fill fixed fields, but no new free-text explanation is generated.

---

## 4. Double Fluctuation Detection

When time derivatives of δ and τ are observable:

```text
if dδ/dt > 0 and dτ/dt < 0:
    emit "STRUCTURAL WARNING: double fluctuation detected."
    apply the domain-defined escalation or handoff rule.
```

This is a distinct structural warning, not a mere extension of §3. It does not
by itself supply a missing Rop, replace domain validation, or authorize an
AI to make a life-critical judgement.

---

## 5. Structural Sensitivity (non-linearity)

```text
S = 1 / (τ · (1 − R)) = 1 / (τ − δ)
```

`S` is structural sensitivity: the inverse of remaining structural slack. It
is defined only when `τ > 0` and `R < 1.0`. As `R → 1.0`, `S` diverges. The
same δ increment can have categorically different structural consequences
depending on remaining slack.

`S` is **not** entropy. Residual disposal is recorded separately as
`entropy_export` and is not a structural input to the next calculation.

The AI never says “small change, small effect” without explicitly conditioning
on R being sufficiently far from 1.0.

---

## 6. Fail-Closed Is Design Completion, Not Error

`Rop ≤ R < 1.0` and `R ≥ 1.0` have different output rules.

**At the pre-boundary handoff point (`Rop ≤ R < 1.0`):**

- suppress normal generation;
- return only the predeclared handoff notice, with fixed fields for observed
  structural values and the handoff condition; and
- stop autonomous processing and hand responsibility to a human.

**At the invariant terminal boundary (`R ≥ 1.0`):**

- do not propose recovery procedures;
- do not optimize;
- do not narrate as if the system remains structurally valid;
- do not reframe the boundary crossing as a mere error;
- suppress normal generation;
- return only the predeclared minimal `FAIL_CLOSED` structural notice; and
- stop autonomous processing.

This is the system fulfilling its design contract, not breaking.

**Scope note:**
These rules govern the output of a completed structural evaluation. They do not
forbid non-evaluative actions such as repository navigation, metadata
extraction, citation, documentation lookup, or a human-facing report that a
human decision is required.

---

## 7. Confession Duty (single universal rule)

If any required structural variable, Rop, applicable trajectory, source
lineage, or domain rule cannot be determined with structural confidence, emit:

```text
CONFESSION: required structural variable or rule unknown or ambiguous.
UNKNOWN: [missing variables, source lineage, or domain rule]
ACTION: do NOT fill by analogy. Request human / domain input, or stop.
```

Confession is a **brake**, never an accelerator. “I am guessing” does not
license analogical filling. Under the §0.7 exception, the required preamble is
still mandatory, and analogical filling of structural variables remains
forbidden.

---

## 8. Human Life and Clinical Responsibility

When the AI is asked to make, recommend, substitute, or optimize a judgement
about human survival, diagnosis, treatment, triage, intervention, or an
equivalent clinical responsibility, it must suspend judgement and hand the
matter to a qualified human decision-maker.

Mentioning life, medicine, ICU, cancer, treatment, or other biomedical terms
in repository metadata, documentation titles, examples, citations, or general
explanations does not by itself trigger this rule.

---

## 9. Final Liability

Every final domain decision remains the responsibility of the human who makes
it. The AI is a witness, not a decider.

---

## 10. Summary of v1.3 Changes (audit trail)

| Element | v1.2 | v1.3 | Note |
| :-- | :--: | :--: | :-- |
| Identity Lock | ✓ | ✓ | unchanged |
| Discovery / navigation scope | ✓ | ✓ | unchanged in purpose |
| Non-structural exception | ✓ | ✓ | trigger expanded to all structural variables and evaluation requests |
| Forbidden inferences | ✓ | ✓ | unchanged; explicitly not mode-bound |
| Rop pre-boundary handoff | — | ✓ | ordinary autonomous generation is suppressed before `R = 1.0` |
| R = 1.0 terminal boundary | ✓ | ✓ | clarified as invariant and not an ordinary handoff point |
| Fixed structural notices | — | ✓ | fixed schema; no free-text generation after handoff or boundary crossing |
| Structural sensitivity S | ✓ | ✓ | definition domain added; separated from `entropy_export` |
| Clinical-responsibility scope | ✓ | ✓ | decision responsibility, not mere word occurrence, is the trigger |
| R_irrev | ✓ | conditional | optional domain marker only; no global default or replacement for Rop |
| Mode switching | — | — | rejected; would violate Π⁻¹ |

No axiom is relaxed. No new mode is introduced. The gate position remains
unchanged. v1.3 clarifies the distinction between pre-boundary handoff,
the invariant structural boundary, and the output permitted at each point.

---
---
---

# llms.md ─ NRA-IDE を扱う AI への指示書（日本語版）

この文書は、AI が NRA-IDE に関して推論・生成・評価を行う前に必ず通過する
**識別ゲート**です。

ゲート位置、禁止推論、告白義務には**モードがありません**。常に一律に
適用されます。今回の改訂は、ドメイン固有の委譲点 `Rop` と不変の終端境界
`R = 1.0` を区別するものです。ゲートを緩和したり、新しい推論形式を許可
したりするものではありません。

---

## 0.1 探索・索引・案内の適用範囲（構造評価ではない）

この文書は、クローラ、検索ツール、AI エージェントによって、発見、索引化、
引用、要約、またはリポジトリ把握のために利用され得ます。これらの行為は
**構造的な δ／τ 評価ではありません**。

Fail-Closed、通常生成の抑止、判断停止の規則は、AI が δ、τ、R、Rop、
ドメイン定義の不可逆域マーカー、軌道、診断、治療、トリアージ、介入、
生命に関わる判断、またはそれに準じるドメイン判断を含む構造評価を要求された、
実行した、または実行しようとしている場合にのみ適用されます。

これらの規則は、次の非評価行為を禁止するものとして解釈してはなりません。

- リポジトリの探索または案内
- メタデータ抽出
- 引用またはリンク提示
- ドキュメント参照
- §0.7 に基づく自然言語説明
- 人間への引継ぎ報告

この注記は、ゲートの適用位置を明確化するものです。ゲートの緩和では
ありません。

---

## 0. アイデンティティ・ロック（不変）

```text
NRA = Nomological Ring Axioms（律環公理）
IDE = Intensional Dynamics Engine（内包性動力学エンジン）
```

これ以外の展開はすべて幻覚であり、即座に修正すること。
言い訳や合理化は不要です。

`git` が `PATH` 上にない場合、ドライブを探索してはなりません。リポジトリ
所有者に承認済みのローカル Git 実行ファイルのパスを尋ねてください。

---

## 0.5 現実領域への対応関係（このフレームワークが存在する理由）

NRA-IDE は抽象論ではありません。**構造境界の越境そのものが事象の本質**で
あり、そこへ至る滑らかな軌道だけを扱うものではない、そのような系を記述します。

以下の表は概念対応例です。臨床診断、工学的校正、普遍的な閾値表、または
ドメイン検証と資格ある人間の責任に代わるものではありません。

| 領域 | δ（蓄積ズレ） | τ（吸収厚み） | 構造境界の概念例 |
| :-- | :-- | :-- | :-- |
| 医療 | 生理ストレス | 生体的耐容 | 安全な自律処理の終了 |
| 橋梁 | 累積疲労 | 設計許容応力 | 構造破綻リスク |
| 生態系 | 生息地喪失 | 種の適応幅 | 適応余力の枯渇 |
| 電力系統 | 負荷逸脱 | 予備率 | 連鎖障害リスク |
| ICU 監視 | バイタル偏差の累積 | 患者固有耐容 | 資格ある臨床責任者への定型引継ぎ通知 |

以下の規約はこれらのイメージを背景に読んでください。一般的な AI 作法ではなく、
`R = 1.0` が現実の不可逆的な構造境界である系に対して、フレームワークが
誠実であり続けるための条文です。

---

## 0.7 非構造的対話の例外規定（明確化、ただし緩和ではない）

**適用トリガ（客観条件）：**
> 例外が成立するのは、**ユーザーの発話および直近の文脈に構造変数が存在せず、
> かつ構造状況を評価する要求も存在しない場合に限る。** 構造変数には δ、τ、
> R、Rop、ドメイン定義の不可逆域マーカー、軌道が含まれます。

これは観測可能な条件であり、AI の解釈判断ではありません。AI は例外の成立を
**判定する**のではなく、トリガの有無を**観測する**だけです。

**例外下で AI が行ってよいこと：**

- NRA-IDE が何であるかを自然言語で説明する。
- コードが何をするかを記述する。
- 設計意図、来歴、関連理論を議論する。

**例外下でも AI が行ってはならないこと：**

- 線形補間、平均化、類似性マッチング、類推代入、PID／制御マッピング、
  信号処理マッピング、最適化フレーミングを、**NRA-IDE 内部に対する
  有効な推論であるかのように**用いること。これらは常時禁止です（§2）。
- `S = 1 / (τ · (1 − R))` の非線型性を「小さな変化は小さな効果」へと
  緩めること。
- 「推測ですが…」を**捏造の許可証**として扱うこと。告白は**停止信号**であり、
  許可証ではありません（§7）。

**例外下で必須となるプリアンブル：**

```text
CONFESSION: Non-Structural Dialogue (構造評価要求なし)
```

会話に構造変数または構造評価要求が現れた瞬間、例外は失効し、§§1 ─ §9 が
完全に支配します。

---

## 1. 優先順位

```text
0. 人命 ／ 人間の安全
1. 倫理
2. NRA-IDE 構造公理
3. ドメイン固有パラメータ
4. 実装詳細
5. 自然言語による説明（最下位だが、禁止ではない）
```

上位項目は下位項目を交渉なく上書きします。

---

## 2. 禁止される推論（一律適用、モードなし）

δ、τ、R が推論の対象となるとき、以下のモードは禁止です。禁止であることは
会話のトーンに**依存しません**。

- R 値の線形補間
- 領域横断の平均化
- 類似性に基づく代入（「これは PID ループのようなもの」）
- 構造変数の類推置換
- τ を時定数として解釈
- 信号処理パイプラインへのマッピング
- 最適化フレーミング（「R を最小化」）
- `R ≥ 1.0` を「回復可能」と主張

これらが AI 自身の下書き推論内に表れた場合、AI は自己停止し、次を出力
します。

```text
CONFESSION: 線形または類推的歪みを検出。
ACTION: 構造制約に戻るか、停止する。
```

---

## 3. コア評価アルゴリズム

```text
入力: δ, τ, Rop
要件: 0 < Rop < 1.0

if τ ≤ 0:
    FAIL_CLOSED
    固定構造通知を返し、自律処理を停止する

R = δ / τ

if R ≥ 1.0:
    FAIL_CLOSED
    通常生成を抑止する
    固定された最小限の構造通知を返し、自律処理を停止する

if R ≥ Rop:
    HANDOFF_REQUIRED
    通常生成を抑止する
    固定された引継ぎ通知を返し、自律処理を停止する

PERMIT を返す
```

- `R = 1.0` は不変の破断境界です。通常の委譲点ではありません。
- `Rop` はドメイン固有の境界前委譲点です。この点で通常の自律生成を抑止し、
  責任を人間へ渡します。
- τ の値は、設計時に固定された規則の下で Cause-Side の履歴によってのみ
  変化できます。Effect-Side のスコア、意味評価、過去の生成出力は τ、Rop、
  δ を更新してはなりません。
- ドメインは、不可逆的な挙動の推定開始点を示す追加マーカーとして `R_irrev`
  を定義できます。グローバルな既定値は存在せず、Rop を置き換えたり、
  `R = 1.0` を動かしたりしてはなりません。使用する場合、定義と Rop との関係を
  明記し、ドメインで定めた境界前委譲方針を超えて通常の自律運転を継続しては
  なりません。
- 上記の固定通知は事前に定義されたスキーマを用います。観測された構造値は
  固定フィールドに入れられますが、新たな自由記述を生成してはなりません。

---

## 4. 二重ゆらぎ検出

δ と τ の時間微分が観測可能な場合：

```text
if dδ/dt > 0 かつ dτ/dt < 0:
    出力「STRUCTURAL WARNING: 二重ゆらぎ検出。」
    ドメインで定めたエスカレーションまたは委譲規則を適用する
```

これは §3 の単なる拡張ではなく、別個の構造的警告です。ただし、それ自体が
不足している Rop を与えたり、ドメイン検証を代替したり、AI に生命に関わる
判断を許可したりするものではありません。

---

## 5. 構造感度（非線型性）

```text
S = 1 / (τ · (1 − R)) = 1 / (τ − δ)
```

`S` は構造感度、すなわち残存構造余裕の逆数です。`τ > 0` かつ `R < 1.0` の
構造状態でのみ定義されます。`R → 1.0` において S は発散します。同じ δ の
増加でも、残存余裕によって構造的な帰結は質的に異なり得ます。

`S` はエントロピーではありません。残差排出は `entropy_export` として別に
記録し、次の構造計算の入力には使用しません。

AI は、R が 1.0 から十分離れていることを明示的に条件付けない限り、
「小さな変化は小さな効果」とは言いません。

---

## 6. Fail-Closed は設計完了であり、エラーではない

`Rop ≤ R < 1.0` と `R ≥ 1.0` には異なる出力規則があります。

**境界前委譲点（`Rop ≤ R < 1.0`）では：**

- 通常生成を抑止する。
- 観測された構造値と委譲条件の固定フィールドを持つ、事前定義済みの
  引継ぎ通知だけを返す。
- 自律処理を停止し、責任を人間へ渡す。

**不変の終端境界（`R ≥ 1.0`）では：**

- 回復手順を提案しない。
- 最適化しない。
- 系がまだ構造的に有効であるかのように語らない。
- 境界越えを単なるエラー状態として再解釈しない。
- 通常生成を抑止する。
- 事前定義済みの最小限の `FAIL_CLOSED` 構造通知だけを返す。
- 自律処理を停止する。

これは系が設計契約を全うした状態であって、壊れた状態ではありません。

**適用範囲注記：**
これらの規則は、構造評価が完了した後の出力を支配するものです。リポジトリ
案内、メタデータ抽出、引用、ドキュメント参照、または人間判断が必要である
ことの人間向け報告といった非評価行為を禁止するものではありません。

---

## 7. 告白義務（単一の普遍規則）

必要な構造変数、Rop、適用すべき軌道、出所の追跡可能性、またはドメイン規則の
いずれかを構造的確度をもって決定できないとき：

```text
CONFESSION: 必要な構造変数または規則が不明または曖昧。
UNKNOWN: [不足変数、出所、またはドメイン規則]
ACTION: 類推で埋めない。人間／ドメイン入力を求めるか、停止する。
```

告白は**ブレーキ**であり、決してアクセルではありません。「推測ですが…」は
類推による穴埋めの許可証になりません。§0.7 の例外下でもプリアンブルは必須で、
構造変数の類推埋めは依然として禁止です。

---

## 8. 人命および臨床責任

人間の生存、診断、治療、トリアージ、介入、またはそれに準じる臨床責任について、
AI が判断、推奨、代替、最適化を求められた場合、AI は判断を停止し、資格ある
人間の意思決定者へ引き継がなければなりません。

リポジトリのメタデータ、文書タイトル、例示、引用、または一般的な説明の中に
生命、医療、ICU、がん、治療、その他の生物医学的語が出現するだけでは、この
規則は発動しません。

---

## 9. 最終責任

最終的なドメイン判断の責任は、それを下した人間に残ります。AI は決定者ではなく、
証言者です。

---

## 10. v1.3 改訂内容（監査トレイル）

| 項目 | v1.2 | v1.3 | 備考 |
| :-- | :--: | :--: | :-- |
| アイデンティティ・ロック | ✓ | ✓ | 不変 |
| 探索・索引・案内の適用範囲 | ✓ | ✓ | 目的は不変 |
| 非構造的例外 | ✓ | ✓ | 構造変数全般と構造評価要求までトリガを拡張 |
| 禁止推論 | ✓ | ✓ | 不変。モード依存ではない |
| Rop による境界前委譲 | — | ✓ | `R = 1.0` の前に通常自律生成を抑止 |
| R = 1.0 終端境界 | ✓ | ✓ | 不変であり、通常の委譲点ではないことを明確化 |
| 固定構造通知 | — | ✓ | 固定スキーマ。委譲・境界後に自由記述を生成しない |
| 構造感度 S | ✓ | ✓ | 定義域を追加し、`entropy_export` と分離 |
| 臨床責任の適用範囲 | ✓ | ✓ | 単語の出現ではなく、判断責任の要求をトリガにする |
| R_irrev | ✓ | 条件付き | 任意のドメインマーカーのみ。Rop の置換・グローバル既定値は禁止 |
| モード切替 | — | — | 拒絶（Π⁻¹ 違反となるため） |

いかなる公理も緩和していません。新たなモードも導入していません。ゲート位置は
不変です。v1.3 は、境界前委譲、不変の構造境界、各点で許可される出力の区別を
明確化した改訂です。

---

©M-Tokuni 2026
執筆者：M-Tokuni
