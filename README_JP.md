<!-- TARGET: /README_JP.md -->
<!-- UPDATED: 2026-07-15 JST -->

# NRA-IDE：律環公理 — 内包性動力学エンジン

### Nomological Ring Axioms — Intensional Dynamics Engine

[![CI](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml/badge.svg)](https://github.com/M-Tokun/NRA-IDE/actions/workflows/nra_check.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19420853.svg)](https://doi.org/10.5281/zenodo.19420853)

<p align="center">
  <img src="./docs/NRA-IDE_git.jpg" width="700" alt="NRA-IDE LOGO">
</p>

---

## NRA-IDEとは

NRA-IDEは、構造に蓄積するズレと、それを吸収できる厚みの関係から、現在の境界接近状態を記述する構造評価体系です。

中心となる問いは、将来を確率的に予測することではありません。

> **対象構造が、現在どの境界状態にあるのか。**

NRA-IDEは、境界接近警告、人間委譲、不可逆遷移開始、完全破断を同一状態へまとめず、それぞれ異なる構造事象として扱います。

また、自律判断や自律行動を停止した場合も、Cause-Sideの観測と構造証言を失わせません。

---

## 正規文書の参照順

NRA-IDEの定義は、次の順序で参照します。

1. [`theory/AXIOMS.md`](./theory/AXIOMS.md)  
   唯一の公理、変数定義、IDE式分類、境界状態、不可逆遷移、構造証言の正規定義

2. [`theory/axioms.json`](./theory/axioms.json)  
   唯一の正規公理と下位定義を同期した機械可読表現

3. [`theory/NRA-IDE_Foundational_Thesis_Bilingual.md`](./theory/NRA-IDE_Foundational_Thesis_Bilingual.md)  
   基礎論文の英日バイリンガル版

4. [`theory/SANDWICH_ARCH.md`](./theory/SANDWICH_ARCH.md)  
   LLMをEffect-Side生成要素として含む場合の論理分離仕様

5. [`theory/THEORY.md`](./theory/THEORY.md)  
   唯一の公理、構造原則、IDE式、境界状態をまとめた理論本文

6. [`FORMULA.md`](./FORMULA.md)  
   式、変数、定義域、初期条件、数値条件、補完計算の正規仕様

7. [`llms.md`](./llms.md)  
   AI向けの識別、解釈、運用ゲート

8. ドメイン固有規則

9. 正規適合試験に合格した正規参照実装

10. その他の実装コード

11. コメント、例示、AI生成説明

下位文書、コード、コメント、例示は、上位正規文書の定義を変更または上書きできません。

リポジトリ全体の配置は [`REPOSITORY_OVERVIEW.md`](./REPOSITORY_OVERVIEW.md) を参照してください。

---

## 唯一の律環公理

> **存在は生成である。**
> **Existence is Generation.**

律環公理はこの一つだけであり、第二公理以降は存在しません。「Nomological Ring Axioms」はNRAと略す固有名称であり、追加公理を認める意味ではありません。

存在は固定された静的実体ではなく、履歴を伴う連続的な生成として現れます。

静止は生成過程の一時的な切り取りであり、構造内部の絶対停止を意味しません。

このため、Fail-Closedや自律行動停止も、構造そのものの消滅や観測停止とは解釈しません。

---

## IDE一次式 — 基本境界式

一次式はIDEの第一の正規計算系であり、第一公理ではありません。

$$
R=\frac{\delta}{\tau}
$$

| 記号 | 正規名称 | 意味 |
|---|---|---|
| $\delta$ | 蓄積ズレ | Cause-Sideの履歴を伴って構造内部に蓄積したズレ |
| $\tau$ | 吸収厚み | 構造が蓄積ズレを吸収できる厚み |
| $R$ | 境界接近比 | 完全破断境界へどの程度接近しているかを示す比率 |

$R$ は境界接近比のみに予約されます。

安全スコア、品質スコア、信頼度、意味保持率、LLM出力評価値として再利用してはいけません。

有効な記述領域は次です。

$$
\tau>0,\qquad \delta\ge0
$$

$$
\delta,\tau\in\mathbb{R}_{finite}
$$

二つの残余余白は区別します。

$$
M_R=1-R
$$

$$
M_{\tau}=\tau-\delta
$$

$M_R$ は無次元の残存比率余白です。 $M_{\tau}$ は残存吸収余白であり、 $\delta$ および $\tau$ と同じ単位を持ちます。

---

## 正規境界順序

NRA-IDEの境界状態は、次の順序で固定されます。

$$
0\le R_{\mathrm{warn}}
<
R_{\mathrm{handoff}}
<
R_{\mathrm{irrev}}
<
1.0
$$

| 境界 | 正規名称 | 役割 |
|---|---|---|
| $R_{\mathrm{warn}}$ | 境界接近警告点 | 境界接近を開示する |
| $R_{\mathrm{handoff}}$ | 境界前人間委譲点 | 新規自律判断・自律操作を停止し、人間へ委譲する |
| $R_{\mathrm{irrev}}$ | 不可逆遷移開始閾値 | 元の構造状態へ戻れることを前提にしない |
| $R=1.0$ | 不変完全破断境界 | 通常生成を停止し、最終固定証言へ切り替える |

人間委譲、不可逆遷移開始、完全破断は同一ではありません。

$$
R_{\mathrm{handoff}}
\neq
R_{\mathrm{irrev}}
\neq
R=1.0
$$

具体的な閾値は対象ドメインごとに定めますが、この順序と役割は変更しません。

`R_handoff`が正規名です。`R_op`、`Rop`、`rop`は同じ閾値へ正規化する後方互換aliasに限り、別の境界や状態を定義しません。

---

## 正規状態分類

| 状態 | 条件 | 基本動作 |
|---|---|---|
| `PERMIT` | $0\le R<R_{\mathrm{warn}}$ | 制約付き自律動作を許可し、構造監査を継続する |
| `BOUNDARY_WARNING` | $R_{\mathrm{warn}}\le R<R_{\mathrm{handoff}}$ | 境界接近、二つの残余余白、傾向、二重ゆらぎ状態、欠損情報を開示する |
| `HANDOFF_REQUIRED` | $R_{\mathrm{handoff}}\le R<R_{\mathrm{irrev}}$ | 新規自律判断・新規自律操作を停止し、人間へ委譲する |
| `IRREVERSIBLE_TRANSITION` | $R_{\mathrm{irrev}}\le R<1.0$ | 不可逆ラッチを設定し、正常化・回復前提・最適化提案を禁止する |
| `RUPTURE_BOUNDARY` | $R\ge1.0$ | 通常生成と自律行動を停止し、最終固定証言へ切り替える |
| `CONFESSION` | 必須構造情報が不明・不正・曖昧・非有限・根拠不明 | 不明箇所を明示し、類推補完せず、影響する評価を停止する |
| `OUT_OF_DESCRIPTION_DOMAIN` | $\tau=0$ | $R$ を定義不能とし、記述体系の変更を要求する |

---

## 不可逆遷移

不可逆遷移は、完全破断より前に始まります。

$$
R_{\mathrm{irrev}}\le R<1.0
$$

この区間では、

```text
irreversible_latched = true
```

とします。

一度ラッチされた後は、瞬間的に $R$ が低下しただけでは通常状態へ戻しません。

再認定には、対象ドメイン固有の再評価、構造再検査、または新しい対象系の定義が必要です。

---

## $\tau=0$ の扱い

$\tau=0$ では、基本境界式は成立しません。

$$
\tau=0
\Rightarrow
R\text{は定義不能}
$$

$\tau=0$ → `OUT_OF_DESCRIPTION_DOMAIN`

また、 $R=\infty$ へ置き換えたり、有効な完全破断計算として扱ったりしてはいけません。

`OUT_OF_DESCRIPTION_DOMAIN`は完全破断計算とは異なります。ただし正規 $R$ を利用できないため、影響する評価にはFail-Closed運用原則を適用します。

一方、 $\tau<0$ 、 $\delta<0$ 、NaN、Infinity、出所不明、単位不明、時点不明、対象不明、規則不明などは、不正または不明な構造入力として`CONFESSION`の対象になります。

---

## Fail-Closed運用原則

Fail-Closedは、次の状態で影響する新規自律判断と自律操作を抑止します。

- `HANDOFF_REQUIRED`
- `IRREVERSIBLE_TRANSITION`
- `RUPTURE_BOUNDARY`
- `CONFESSION`
- `OUT_OF_DESCRIPTION_DOMAIN`

必要な固定構造証言とログは抑止しません。`PERMIT`はFail-Closedではありません。`BOUNDARY_WARNING`だけでは、事前固定されたドメイン規則が要求しない限り出力を全面抑止しません。

---

## 構造証言

NRA-IDEは、危険度が高いという理由だけで完全沈黙しません。

$$
R<1.0
\Rightarrow
\text{構造証言を継続する}
$$

構造証言には、必要に応じて次を含みます。

- Cause-Side観測
- 現在の $\delta$ 、 $\tau$ 、 $R$
- 境界状態
- 残存比率余白 $M_R$
- 残存吸収余白 $M_{\tau}$
- 変化傾向
- 支配側
- 欠損情報
- 二重ゆらぎの判定結果、または`NOT_OBSERVABLE`と欠損理由
- 境界警告
- 人間委譲通知
- 不可逆遷移通知
- 構造開示ログ

$$
R\ge1.0
\Rightarrow
\text{最終固定証言へ切り替える}
$$

最終固定証言は、事前定義された最終Cause-Side観測、最終 $\delta$ 、最終 $\tau$ 、最終 $R$ 、完全破断通知、不可逆ラッチ状態、監査証跡、人間委譲通知などに限定されます。

> **自律行動は止める。しかし、構造証言は消さない。**

---

## Cause-Side / Effect-Side分離

$\delta$ 、 $\tau$ 、 $R$ を決定できるのは、次のいずれかだけです。

1. 直接のCause-Side観測
2. 評価前に固定されたCause-Side変換規則

Cause-Side入力には、出所、対象、単位、観測時点、変換規則、規則版、更新権限を追跡できることが求められます。

一方、次はEffect-Sideです。

- LLM出力
- LLMの自己評価
- 意味スコア
- 出力順位
- 選別済み出力
- 廃棄出力
- 過去生成物

これらは監査対象にはできますが、 $\delta$ 、 $\tau$ 、 $R$ を更新してはいけません。

$$
\text{Effect-Side}
\not\rightarrow
(\delta,\tau,R)\text{ update}
$$

検証済み、選別済み、または出力ゲートを通過したLLM出力であっても、Effect-Sideのままです。

---

## LLMを含む構成

NRA-IDEは統合開発環境を意味するIDEではありません。

ここでのIDEは、**Intensional Dynamics Engine（内包性動力学エンジン）**です。

LLMを含む実装では、LLMを信頼済みの構造評価器として扱いません。

[`theory/SANDWICH_ARCH.md`](./theory/SANDWICH_ARCH.md)では、次を分離します。

```text
Cause-Side観測
        ↓
NRA-IDE境界評価器
        ↓
入力ゲート
        ↓
LLM CORE
        ↓
出力ゲート
        ↓
構造証言 + 許可された説明
```

境界評価器が判定し、出力ゲートが制約を執行します。

```text
Boundary Evaluator
→ decides

Output Gate
→ enforces
```

LLM説明を省略または停止しても、独立したCause-Side監査経路から構造証言を維持します。

---

## IDE式の分類

### 一次式

$$
R=\frac{\delta}{\tau}
$$

IDEの第一の正規計算系であり、公理ではありません。

### 二次式

二次式（二重ゆらぎ式）はIDEの第二の正規計算系であり、第二公理ではありません。その正規核は、上側・下側の蓄積ズレ、側別境界接近比、および蓄積ズレ増加と吸収厚み減少の同時進行を扱います。

事前固定したEMA、初期条件、側別形状変換は、この計算系の補助的実現です。独立した正規式または公理ではありません。

二次式は、NRA-IDE内の定義順序と役割を示す名称です。数学的な二次方程式を意味しません。

側別有効ゲート幅の変化は、基礎となる真の吸収厚み $\tau$ が自然回復または自然増加したことを意味しません。

### 補完式

補完式は、EMA遅延、局所急変、数値積分、対象ドメイン固有の精度条件を補助する計算層です。

補完式は公理でも第三の正規IDE計算系でもなく、一次式または二次式を置き換えません。

数式、変数、初期条件、数値条件は [`FORMULA.md`](./FORMULA.md) を参照してください。

---

## 数値計算と残差

NRA-IDEの整数位相ロックは、丸め誤差や残差を無監査のまま次状態へ持ち越さないための設計原則です。

これは、

```text
あらゆる物理誤差が存在しない
```

ことを意味しません。

値と由来が確立した既知の数値的構造進行、丸め、近似、廃棄残差は`STRUCTURAL_DISCLOSURE_LOG`へ記録します。

既知の近似は自動的に`CONFESSION`ではありません。`CONFESSION`は、不明・不正・曖昧・非有限・根拠不明な構造情報に限定されます。

`CONFESSION`と`OUT_OF_DESCRIPTION_DOMAIN`は`INPUT_EXCEPTION_LOG`へ分離して記録します。既知の数値的進行として`STRUCTURAL_DISCLOSURE_LOG`へ混入させません。

---

## 時間と距離

NRA-IDEでは、時間を無条件な独立原因変数として扱いません。

時間は、履歴を伴う状態遷移の順序として現れます。

距離も、無条件に因果を生む駆動量として扱いません。

ただし、距離、位置、方向、空間関係が物理的に有効な観測値である場合は削除せず、Cause-Side観測として保持し、その因果上の役割を明示します。

```text
距離が自動的な原因ではない
≠
距離情報を削除する
```

---

## 構造評価と非評価行為

構造評価とは、 $\delta$ 、 $\tau$ 、 $R$ または正規境界状態を計算、分類し、その結果に基づいて作用することです。

一方、次は、それ自体では構造評価ではありません。

- 文書の閲覧
- 索引作成
- 引用
- リンク案内
- ファイル探索
- メタデータ抽出
- リポジトリ構造の説明

ただし、これらの行為の中で構造変数を計算、分類、更新する場合は、正規規則の対象になります。

---

## 比較説明について

PID制御、信号処理、統計、機械学習、既存の連続力学と比較すること自体は禁止しません。

ただし、比較対象の概念によってNRA-IDEの正規定義を置き換えてはいけません。

特に、

- $\tau$ を時間定数へ読み替える
- $R$ を安全スコアや信頼度へ読み替える
- LLM出力評価から $\delta$ を生成する
- 不可逆開始と完全破断を同一視する

ことは禁止されます。

---

## 実装・デモ

実装、使用例、インタラクティブなHTMLデモは、次を参照してください。

- [`src/`](./src/) — ソースコード
- [`nra-core/`](./nra-core/) — コア実装
- [`gate/`](./gate/) — ゲート実装
- [`examples/`](./examples/) — 使用例・可視化デモ
- [`examples/README_JP.md`](./examples/README_JP.md) — 日本語デモ一覧
- [`REPOSITORY_OVERVIEW.md`](./REPOSITORY_OVERVIEW.md) — リポジトリ全体マップ

デモは、事前定義された対象、変数、閾値、変換規則の下でNRA-IDEの挙動を可視化するものです。

個別デモ内の数値一致や閾値を、全ドメイン共通の物理法則として一般化してはいけません。

---

## 接地・運用層

[`ground/`](./ground/) は、観測事実、出所、物理制約、欠損値、閾値、実行使用可否を扱う接地・運用層です。

`ground/`は第二公理以降を追加する場所ではなく、上位正規文書の定義に従います。

運用規則や実装規則は、唯一の公理、変数定義、IDE式分類、境界順序、構造証言規則を変更できません。

---

## 倫理・利用境界

倫理方針は [`theory/ETHICS.md`](./theory/ETHICS.md) を参照してください。

高リスク領域では、NRA-IDEは人間の専門的責任を置き換えるものではありません。

NRA-IDEの役割は、Cause-Side観測に基づく構造状態を明示し、正規境界順序に従って警告、委譲、不可逆遷移、完全破断を分離することです。

---

## 英語版

英語の概要は [`README.md`](./README.md) を参照してください。

---

## 引用・ライセンス

- 正式な引用情報：[`CITATION.cff`](./CITATION.cff)
- ライセンス：[`LICENSE`](./LICENSE)
- DOI：`10.5281/zenodo.19420853`

---

## 正規要点

```text
NRA = Nomological Ring Axioms
IDE = Intensional Dynamics Engine

R = delta / tau

delta = accumulated deviation
tau   = absorption thickness
R     = boundary-approach ratio

0 <= R_warn < R_handoff < R_irrev < 1.0

M_R   = 1 - R
M_tau = tau - delta

tau = 0
→ OUT_OF_DESCRIPTION_DOMAIN
→ R is undefined
→ affected evaluation is Fail-Closed

Fail-Closed applies to
→ HANDOFF_REQUIRED
→ IRREVERSIBLE_TRANSITION
→ RUPTURE_BOUNDARY
→ CONFESSION
→ OUT_OF_DESCRIPTION_DOMAIN

BOUNDARY_WARNING alone
→ does not require full suppression without a pre-fixed domain rule

R < 1.0
→ structural testimony continues

R >= 1.0
→ switch to final fixed testimony

Cause-Side
→ may determine delta, tau, R

Effect-Side
→ must not update delta, tau, R

Known boundary progression
→ structural disclosure

Unknown, invalid, ambiguous, non-finite, or unsupported information
→ CONFESSION
→ INPUT_EXCEPTION_LOG
```
