# NRA-IDE 第2次CLI精査 継続Report — Overview EN

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai/00_overview_EN.md`
- 位置付け: `01_paradigm_shift_JP.md`完了後、残る未精査AI章から選定した次の1ファイル
- 先行継続Report: `45_cli_second_pass_pending_paradigm_shift_jp.md`
- 対象本文の編集: 実施
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 現在状態

- 対象本文を1～140行と141行以降に分けて全文読取りし、141行以降に本文がないことまで確認した。
- 対象限定の`git status --short`と`git diff`は出力なしで、追跡済み本文に既存差分はない。
- 現在のSHA-256は`55260A034EA5C1169A3BC1C07D0A9D8B4810A9AABD4BE3B77634FA685D0F6ACD`である。
- `docs/en-US/ai`の00～12章が実在することを確認し、本文内の相対リンク8件はすべて実在した。
- Markdown見出しは13件、コードフェンスは0件で、現在構造に破損はない。
- 対象本文は編集していない。

## 2. 検出した問題

### 2.1 起点の問いがAIと人間委譲へ縮小されている

中心質問を、AIを含む動的系が限界を超える出力を止めて`delegate judgment to humans`できるか、としている。

影響: NRA-IDE本体をAI出力制御へ狭め、`HANDOFF_REQUIRED`を固定Effect-Side証言の外部人間監査ではなく、旧経路内の人間判断への引渡しとして扱う。

### 2.2 唯一公理を設計前提と呼び、計算系の分類が不完全

「存在は生成である。」を`design premise`とし、`delta`、`tau`、`R`を一つの`computational principle`として説明している。唯一公理であること、第二公理以降がないこと、基礎式と第二次／二重ゆらぎ式が二つのIDE計算系で公理ではないことを明記していない。

影響: 公理を任意の設計前提へ弱め、基礎式とIDEエンジンの分類境界を曖昧にし、二重ゆらぎ式を全体地図から欠落させる。

### 2.3 生存式・生存領域と安全域の部分関係がない

Overview全体がAI安全判定を中心にし、NRA-IDE本体である生存式・生存領域、IDEという計算方法・動力学エンジン、安全域という事故防止・運用・制御への部分応用を分類していない。動的な生存の定義もない。

影響: 生存領域を安全域へ縮小し、生存を同じ形の保存と誤読させ、揺らぎ、相転移、破断、淘汰、消滅、再構成を通じた新構造・新履歴の生成を取りこぼす。

### 2.4 基礎式を比率説明へ縮小し、宣言対象境界がない

`R = delta / tau`を構造状態を表す比率としてだけ説明し、宣言対象の状態を式へ落とす本当の数学的根本式であることを示していない。`R = 1.0`を`the phase-transition boundary at which the structure itself can no longer remain established`と一般化している。

影響: 基礎式を局所指標・境界接近率へ縮小し、宣言済み評価の`RUPTURE_BOUNDARY`を自然一般の単一相転移境界へ拡張する。

### 2.5 三閾値・七状態・不可逆ラッチがない

`domain-specific point`や文脈に応じて決める`delegation-point value`だけを記述し、`R_warn < R_handoff < R_irrev < 1`、七つの正典状態、`R_irrev`到達後の解除不能ラッチを示していない。

影響: Handoff、不可逆遷移、破断境界、入力不足、記述領域外を区別できず、人間判断で閾値や状態を後から変更できる余地が残る。

### 2.6 因果ダイオードを逆推論禁止へ縮小している

因果ダイオードを`blocks Pi^-1—the backward inference of causes from effects`および評価値から入力を逆推論しない原則として説明している。

影響: 禁止対象を推論へ限定し、旧Effect-Sideから値、閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所を自動・手動・人間レビュー・承認・版更新で逆接続する余地を残す。

### 2.7 旧経路終端と独立新履歴がない

古いEffect-Sideで旧経路が終端すること、外部人間監査・事故後分析・将来規則作成が旧因果ダイオード外であること、後続評価が独立対象、新Cause-Side観測・事前固定規則、新Causal Diodeから始まることを示していない。

影響: 古いEffect-Sideを旧Cause-Sideまたは新Cause-Sideへ戻し、別履歴の境界を消失させる。

### 2.8 三層構成を全体不変条件にしている

`Three-Layer Separation`を全章で不変な原則とし、Pre-NRA / LLM / Post-NRAを厳密分離すると記述している。

影響: LLMを含まないNRA-IDE評価や別の部品構成を誤って排除し、構成図の層数を正典適合条件へ変える。必要な不変条件である権限分離、正典挙動、証拠、試験から焦点が外れる。

### 2.9 Fail-Closedを人間委譲としている

05～08章の説明と構造的不変条件の両方で、停止後に`delegates judgment to humans`すると記述している。固定Handoff証言、最終固定証言、Fail-Closed対象状態、通常説明の許可境界を示していない。

影響: 旧経路を人間判断で継続したり、固定証言へ自由生成説明を追加したり、必要な証言まで沈黙させたりできる。

### 2.10 ログの非転用条件が不足している

ログを`does not use them in subsequent calculations`とするだけで、終端Effect-Sideまたは外部証言であること、旧Effect-Side資料のimport、relabel、reconstruction、reuse禁止を示していない。

影響: 「計算」以外の手動レビュー、承認、版更新、将来規則作成を介して、ログの値・判断・出所をCause-Side権限へ転用できる。

### 2.11 観測可能性・定量化可能性と線形計算境界がない

観測量には触れるが、非線形相転移領域で定量精度が低下しても物理的兆候を観測できる区別がない。線形計算が局所的静的領域で定数近似できる場合の智慧であり、大規模・結合・再帰系で誤差が乗算され、観測軸やモデルの変質が新構造履歴の生成となる境界もない。

影響: 定量化不能を観測不能と同一視し、線形近似を自然全体へ一般化する全体地図になる。

### 2.12 保証範囲の章説明が誤解を残す

09～11章を`the scope of what can be guaranteed`として案内し、本章自身には非安全保証の上位注意書きがない。

影響: 安全保証を与えない理論に、調整によって保証可能になる範囲が存在するように読める。

判定: `HARD_CONFLICT / SEMANTIC_DRIFT / CLASSIFICATION_BOUNDARY_CONFLICT / HISTORY_BOUNDARY_CONFLICT / GUARANTEE_SCOPE_CONFLICT`

## 3. 推奨修正案

当該1ファイルだけを、完了済み00以外の英語AI章と確定済み正典境界を案内できる全体地図へ整合する。

1. Important欄で唯一公理、二つのIDE計算系、上位正典への従属、非安全保証を明記する。
2. 起点をAI固有の人間委譲問題から、生存式・生存領域と安全志向部分領域における事故前Cause-Side経路の観測へ改める。
3. NRA-IDE本体、生存領域、IDEエンジン、安全域、動的生存の分類を示す。
4. 基礎式を宣言対象の状態を式へ落とす数学的根本式とし、安全指標、局所計器、単なる境界接近率へ縮小しない。
5. 二重ゆらぎ式をIDEの計算方法・動力学エンジンとして位置付け、公理にしない。
6. 三閾値の不変順序、七状態、不可逆ラッチ、宣言済み評価の`RUPTURE_BOUNDARY`を全体地図へ置く。
7. Handoffを固定Effect-Side証言の外部人間監査とし、旧経路内の人間判断への委譲表現を除く。
8. 因果ダイオードを完全一方向とし、Effect-Sideから値、閾値、状態、ラッチ、規則、変換入力、更新根拠、出所への全逆接続を禁止する。
9. 旧経路を古いEffect-Sideで終端し、後続評価を独立対象、新Cause-Side観測・事前固定規則、新Causal Diodeから始める。
10. 古いEffect-Sideのimport、relabel、reconstruction、reuse禁止と、物理的残存物の新規観測を区別する。
11. Pre-NRA / LLM / Post-NRAをLLM採用時の構成例へ限定し、層数ではなく権限分離、正典挙動、証拠、適用試験を適合条件とする。
12. Fail-Closed後の固定証言・ログと、許可された通常説明の境界を示す。
13. 観測可能性と定量化可能性、線形近似と非線形な新構造履歴生成の境界を全体不変条件へ加える。
14. 章案内を現在の各章内容に合わせ、保証ではなく利益・限界・適用条件を扱う表現へ修正する。
15. 現在有効な相対リンク8件、著作権、SPDX表記は保持する。

公理や数式自体、他ファイル、RAW報告01～17は変更しない。対象本文は利用者の決定まで編集しない。

## 4. 利用者決定と修正

問題箇所、正典境界との衝突、影響、推奨修正案を提示し、利用者は`Y`で承認した。変更単位は`docs/en-US/ai/00_overview_EN.md`だけに限定した。

実施内容:

- Important欄で唯一公理、二つのIDE計算系、上位正典への従属、非安全保証を明記した。
- 「遊びのない厳密さは崩壊する」を第二公理ではなく構造持続原理として分類した。
- NRA-IDE本体を生存式・生存領域、IDEを計算方法・動力学エンジン、安全域を事故防止・運用・制御への部分応用として分離した。
- 生存を、同じ形の永久保存ではなく、揺らぎ、相転移、破断、淘汰、消滅、再構成を通じて新構造と履歴を生成する動的存続として明記した。
- 基礎式を宣言対象の状態を式へ落とす数学的根本式とし、安全指標、局所計器、単なる境界接近率へ縮小しないとした。
- 第二次／二重ゆらぎ式をIDEの計算方法・動力学エンジンとして分類した。
- 三閾値の不変順序、七つの正典状態、不可逆ラッチ、宣言済み評価の`RUPTURE_BOUNDARY`を全体地図へ追加した。
- 低いEffect-Sideの`R`を理由とする`tau`拡大、`delta`再定義、閾値・状態条件変更を禁止した。
- 各章案内を現在の完了済み章内容へ合わせ、構造感度を補完・派生式として基礎式および公理から分離した。
- 線形計算を局所的静的領域の近似へ限定し、大規模・結合・再帰系の誤差乗算と、観測軸・モデル変質による新構造履歴生成を明記した。
- 観測可能性と定量化可能性、測定値・単位・不確かさ・機器限界・変換規則・欠落情報を分離した。
- Handoffを固定Effect-Side証言の外部人間監査とし、人間判断への旧経路内委譲を除いた。
- 因果ダイオードを完全一方向の権限境界とし、旧Effect-Sideで旧経路を終端した。
- 後続評価を独立対象、新Cause-Side観測・事前固定規則、新Causal Diodeから始まる別履歴とした。
- 古いEffect-Sideのimport、relabel、reconstruction、reuse禁止と、物理的残存物の新規観測を分離した。
- 外部人間監査、事故後分析、将来規則作成を終端済み旧因果ダイオードの外側へ置いた。
- Fail-Closed対象状態、固定証言・ログ、通常説明の許可境界を明記した。
- Pre-NRA / LLM / Post-NRAをLLM採用時の構成例へ限定し、権限分離、正典挙動、証拠、適用試験を適合条件とした。
- 相対リンク8件、著作権、SPDX表記を保持した。

## 5. 修正後検証

修正後197行を前後半へ分けて全文再読し、線形計算境界の一文を確定済み表現へ厳密化した。その後、正典条件、旧表現、リンク、Markdown、Git差分を集計検証した。

```text
AXIOM_AND_FORMULA_CLASSIFICATION=PASS
STRUCTURAL_PERSISTENCE_PRINCIPLE=PASS
SURVIVAL_AND_SAFETY_SCOPE=PASS
DYNAMIC_SURVIVAL=PASS
PRIMARY_FORMULA_NON_REDUCTION=PASS
DUAL_FLUCTUATION_ENGINE=PASS
LINEAR_SCOPE=PASS
OBSERVABILITY_VS_QUANTIFICATION=PASS
CANONICAL_THRESHOLDS=PASS
SEVEN_CANONICAL_STATES=PASS
IRREVERSIBLE_LATCH=PASS
EXTERNAL_HUMAN_AUDIT=PASS
EFFECT_AUTHORITY_SCOPE=PASS
OLD_PATH_TERMINATION=PASS
NEW_INDEPENDENT_HISTORY=PASS
OLD_EFFECT_REUSE_PROHIBITION=PASS
PHYSICAL_REMNANTS_NEW_OBSERVATION=PASS
FAIL_CLOSED_TESTIMONY=PASS
LLM_CONDITIONAL=PASS
NON_GUARANTEE=PASS
LEGACY_RESIDUAL_COUNT=0
LINKS=8
MISSING_LINKS=0
HEADINGS=18
DUPLICATE_HEADINGS=0
FENCES=10
FENCES_EVEN=PASS
TARGET_DIFF_CHECK=OK
LINES=197
SHA256=F05AC9809C0E9836BA73D79444873A99FDF61BDAFA947E873F0CA7D85F558CE2
```

旧表現残存検索では、`delegate judgment to humans`、`ordinary delegation point`、`delegation-point value`、`scope of what can be guaranteed`、`Three-Layer Separation`、`does not use them in subsequent calculations`が0件だった。

## 6. 判定と作業位置

`docs/en-US/ai/00_overview_EN.md`は、唯一公理、二つのIDE計算系、生存領域と安全域、動的存続、基礎式の非縮小、線形境界、観測可能性、三閾値、七状態、不可逆ラッチ、外部人間監査、完全一方向の因果ダイオード、旧Effect-Side終端、独立新履歴、Fail-Closed、LLM条件付き構成を案内する全体地図へ整合した。

新たな問題、旧解釈の残存、リンク切れ、Markdown破損は検出しなかった。当該1ファイルは完了とする。この判定は当該1ファイルに限定し、未精査ファイルが整合済みであることを意味しない。
