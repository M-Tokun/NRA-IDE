# NRA-IDE 第2次CLI精密検証レポート

- 検証日: 2026-07-14 JST
- 対象: `local_reportsDirectory/01_root_review.md`～`17_global_consistency_including_docs.md`、関連正典、公開実装、docs
- 位置付け: 初回監査報告を変更せず、CLIで独立再検証した結果を記録する第2次報告
- 原資料変更: なし
- 総合判定: **初回報告の重大指摘は概ね再現。ただし、分類誤り、対象内訳誤り、固定manifest不在のため、初回報告だけでは修正判断を確定できない**

## 1. このチェックポイントの目的

CLI作業を中断しても、次回に同じ調査を最初から繰り返さず再開できるよう、次を固定する。

- 読込済み規則と作業基準
- 初回17報告の固定状態
- 原本で再現した指摘
- 初回報告の訂正事項
- CLI境界実行結果
- 更新対象と履歴保存対象の暫定分類
- 未決定事項と次回再開位置

既存の01～17報告はRAW監査証拠として本文を変更しない。訂正、採否、追加検証は本報告および`audit_manifest.json`へ記録する。

## 2. 読込・確認済み規則

- `AGENTS.md`
- `RULES_DETAIL.md`
- `CODEX.md`
- `CODEX_CLI_BROWSER_WORKFLOW.md`

作業時のGit状態:

```text
branch: master
 D nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf
?? CODEX_CLI_BROWSER_WORKFLOW.md
?? local_reportsDirectory/
```

上記は本検証開始前から存在する利用者の変更として保持した。本検証では復元、削除、移動、stage、commit、pushを行っていない。

## 3. 初回報告の固定状態

- 報告数: 17
- 空ファイル: なし
- 同一SHA-256の報告: なし
- 報告manifest: 検証開始時点では存在しない
- Git状態: `local_reportsDirectory/`全体が未追跡

各報告のSHA-256は`audit_manifest.json`へ記録した。

## 4. 原本で再現できた主要指摘

### CLI-VALID-001 — 正典参照順位の不一致

判定: `CONFIRMED / HARD_CONFLICT`

- `theory/AXIOMS.md`の順位はThesisと`SANDWICH_ARCH.md`を含まない。
- `theory/axioms.json`、`llms.md`、`llms.txt`は両文書を含む。
- 競合解決順が一意でないため、正典修正前に正式順位の決定が必要。

### CLI-VALID-002 — G(r)の大残差近似と飽和表現

判定: `CONFIRMED / HARD_CONFLICT`

定義:

```text
G(r) = r|r| / (k + |r|)
```

大残差では`G(r) ~ r`である。`G(r) ~ r sgn(r)`および「飽和応答」は式と一致しない。

### CLI-VALID-003 — 正規Rと側別最大比の競合

判定: `CONFIRMED / HARD_CONFLICT`

- 上位正典は`R = delta / tau`だけを正規Rへ予約する。
- `FORMULA.md`、Thesis、`THEORY.md`、公開Pythonは側別最大比を同じ`R`として扱う。
- 側別比を補助量へ変更するか、上位正典を改訂するかの人間判断が必要。

### CLI-VALID-004 — tau発展式の成立条件不足

判定: `CONFIRMED / AMBIGUOUS`

`tau(t) = tau_0 - integral f(delta(s)) ds`から閉区間での減少を導くには、少なくとも対象領域で`f(delta) >= 0`が必要だが、正典に符号条件がない。

### CLI-VALID-005 — 二重ゆらぎ出力条件の差

判定: `CONFIRMED / SEMANTIC_DRIFT`

- `AXIOMS.md`: BOUNDARY_WARNINGの必須出力として無条件記載
- `axioms.json`: `double fluctuation when observable`

観測可能時のみ必須とするか、常時必須とするかを統一する必要がある。

### CLI-VALID-006 — 公開Pythonの状態機械不整合

判定: `CONFIRMED / HARD_CONFLICT`

`docs/NRA-IDE_Architecture_public.py`と`nra-core/foundations/NRA-IDE_Architecture_public.py`はSHA-256が一致する。

CLIで`nra_ide_core_evaluation`を境界入力へ直接実行した結果:

| 入力 | 実際の結果 | 正典上の結果 |
|---|---|---|
| `tau=0` | `FAIL_CLOSED` | `OUT_OF_DESCRIPTION_DOMAIN` |
| `tau<0` | `FAIL_CLOSED` | `CONFESSION` |
| `delta<0` | `PERMIT` | `CONFESSION` |
| `delta=Infinity` | `FAIL_CLOSED` | `CONFESSION` |
| `tau=Infinity` | `PERMIT` | `CONFESSION` |
| `delta=tau=Infinity` | `PERMIT` | `CONFESSION` |

さらに`R_warn`、`R_irrev`、現行5状態、不可逆ラッチを実装していない。公開実装は局所修正より、正典状態表から再構成する方が安全である。

### CLI-VALID-007 — docsの重複ファイル

判定: `CONFIRMED`

次の組はSHA-256が完全一致する。

- `theory/figures/TOP_sandwich.png`と`docs/TOP_sandwich.png`
- `theory/figures/NRA-IDE定義式（基礎式）.jpg`と`docs/nra_ide_formula_basic.jpg`
- `nra-core/foundations/NRA-IDE_Architecture_public.py`と`docs/NRA-IDE_Architecture_public.py`

### CLI-VALID-008 — docsリンクと外部フォント

判定: `CONFIRMED`

- Markdown 38件を検査し、ローカルリンク切れは1件。
- 対象: `docs/en-US/ai/08_discard_logs_EN.md`
- 参照先: `../figures/08_Escapement_ContactPoint_JP.html`
- Google Fonts依存HTMLは6件。

### CLI-VALID-009 — 構文検査

判定: `CONFIRMED`

- Python 70件: 全件AST構文解析成功
- `theory/axioms.json`: JSON解析成功

初回報告にある「実行不能」は、少なくともPython構文エラーを意味しない。依存関係、実行時挙動、数理・状態機械上の不成立を分けて記録する必要がある。

## 5. 初回報告の訂正事項

### CLI-CORRECT-001 — tau非正値の分類

対象: `12_global_consistency_review.md` 29行

初回記述:

```text
tau非正値処理の分裂: v2.1は記述領域外
```

正典上の正しい分類:

```text
tau = 0  -> OUT_OF_DESCRIPTION_DOMAIN
tau < 0  -> CONFESSION
```

判定: `PARTIALLY_CONFIRMED / SEMANTIC_DRIFT`

`tau<=0`を単一状態へまとめてはならない。`CODEX_CLI_BROWSER_WORKFLOW.md`の「tau非正値を領域外へ分離」という記述も、正典分類へ合わせる必要がある。

### CLI-CORRECT-002 — docs可視化内訳

対象:

- `15_docs_figures_review.md` 4行
- `16_docs_overall_review.md` 5行

初回内訳:

```text
共通figures 11
ja-JP/figures 13
en-US/figures 13
```

CLI実測:

```text
docs/figures       12
docs/ja-JP/figures 12
docs/en-US/figures 13
```

docs総数80件は一致するが、内訳が誤っている。

### CLI-CORRECT-003 — リポジトリファイル数

`CODEX_CLI_BROWSER_WORKFLOW.md`の基準は`rg --files`で529件だが、再検査時点は528件だった。

Gitには次の削除状態がある。

```text
D nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf
```

固定値を合否条件にせず、各監査開始時の実測値、対象一覧、Git状態、SHA-256をmanifestへ保存する。

## 6. 暫定分類

### 更新・修正対象

- `llms.md`
- `llms.txt`
- `FORMULA.md`
- `theory/AXIOMS.md`
- `theory/axioms.json`
- `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
- `theory/SANDWICH_ARCH.md`
- `theory/THEORY.md`
- `theory/GOVERNANCE.md`
- `theory/ETHICS.md`
- 単一の正規参照実装
- `docs/README.md`
- `docs/README_JP.md`
- docs日英AI解説
- 現行公開面で使用する図、SVG、HTML

### 本文を履歴保存する対象

- `local_reportsDirectory/01`～`17`のRAW監査報告
- `note`全50件
- `nra-core/papers`の旧論文、日付付き文書、PDF
- `nra-core/quantum`の研究資料
- `nra-core/visualization`の概念デモ
- `nra-core/implementation`の日付付き旧実装
- `nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.md/PDF`
- 旧版画像、旧SVG、旧HTML、派生PDF

履歴保存対象は本文を現行仕様へ一括置換せず、別manifestまたは冒頭表示で`legacy`、`research_hypothesis`、`conceptual_demo`、`invalid_experiment`、`derivative`等を明示する。

## 7. 正典修正前の未決定事項

次の事項は推測で確定しない。

1. 正式な正典参照順位
2. `f(delta)`の符号、有限性、可積分性条件
3. 二重ゆらぎの必須出力条件
4. 側別最大比の記号と正規Rとの関係
5. 正規参照実装の配置場所とdocs複製方法
6. 旧資料の物理移動を行うか、現位置でmanifest分類するか

## 8. 推奨修正順

1. 正典上の未決定4項目を人間判断で確定する。
2. `AXIOMS.md`と`axioms.json`を同一変更単位で同期する。
3. `FORMULA.md`、Thesis、`THEORY.md`の記号と数式を同期する。
4. 現行状態表から単一参照実装と境界値テストを作る。
5. docs README、日英解説、公開Python、現行図を同期する。
6. nra-coreとnoteをmanifestで履歴分類する。
7. 全体残存検索とリンク・構文・境界値テストを実施する。

## 9. 次回の再開位置

次回は、正典修正を始める前に「正典参照順位」「f(delta)条件」「二重ゆらぎ条件」「側別最大比」の4点を決定する。

決定後、最初の修正単位を`theory/AXIOMS.md`と`theory/axioms.json`の内部同期だけに限定する。

## 10. 検証後の状態

- 原資料の編集: なし
- RAW監査報告の編集: なし
- Git操作: なし
- 外部通信: なし
- Python構文検査による`__pycache__`: 生成なし

## 11. 正典決定・Phase 1同期チェックポイント

- 決定日: 2026-07-14 JST
- 利用者決定: 推奨案 `1A / 2A / 3A / 4A / 5A`を採用
- 変更単位: `theory/AXIOMS.md`と`theory/axioms.json`の意味同期のみ
- RAW監査報告01～17: 変更なし

### 11.1 確定した5項目

1. 正典参照順位は、`AXIOMS.md > axioms.json > Foundational Thesis > SANDWICH_ARCH > THEORY > FORMULA > llms.md > domain rules > normative implementation > other implementation > comments > examples > AI explanations`とする。
2. `f(delta)`は対象とする各有限評価区間で有限、非負、可積分とする。閉区間内のtauは非増加であり、累積消耗積分が正の区間で厳密に減少する。
3. BOUNDARY_WARNINGの二重ゆらぎ状態欄は常時必須とする。観測可能なら判定結果、観測不能なら`NOT_OBSERVABLE`と欠損理由を出力し、観測不能だけを理由にCONFESSIONへ移行しない。
4. 正規Rは`R = delta / tau`に限定する。側別比は`R_upper`、`R_lower`、最大集約値は補助量`R_dir`とし、正規Rへ再定義しない。
5. 正規参照実装のソース配置は`nra-core/foundations/NRA-IDE_Architecture_public.py`、docs版は生成同期コピーとする。配置だけでは正規性を取得せず、正典適合試験を必須とする。

### 11.2 実施した検証

```text
SYNC_PRECEDENCE=True
SYNC_DEPLETION=True
SYNC_DOUBLE_FLUCTUATION=True
SYNC_DIRECTIONAL_RATIO=True
SYNC_IMPLEMENTATION=True
JSON_PARSE_OK
DIFF_CHECK_OK
```

Markdownコードフェンス数は偶数であり、対象限定`git diff --check`にエラーはなかった。

### 11.3 チェックポイント時のGit状態

```text
 D nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf
 M theory/AXIOMS.md
 M theory/axioms.json
?? CODEX_CLI_BROWSER_WORKFLOW.md
?? local_reportsDirectory/
```

既存PDF削除と未追跡ファイル群は利用者の既存変更として保持した。stage、commit、pushは実施していない。

### 11.4 次回再開位置

Phase 2として、`FORMULA.md`、Foundational Thesis、`theory/THEORY.md`に残る正規Rと側別最大比、`f(delta)`条件、`G(r)`大残差近似の影響範囲を対象限定で再確認する。編集前に一つの同期関係へ変更単位を限定し、正典2ファイルの意味を下位文書へ継承する。

## 12. Phase 2 — 側別補助集約R_dir同期チェックポイント

- 実施日: 2026-07-14 JST
- 変更関係: 正規Rと側別最大集約の記号分離のみ
- 変更ファイル:
  - `FORMULA.md`
  - `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
  - `theory/THEORY.md`
- 変更しなかった事項: `f(delta)`条件、動的tauの関数記号衝突、`G(r)`、実装、docs、RAW監査報告01～17

### 12.1 同期内容

- 正規Rは`R = delta / tau`のみに維持した。
- `R_upper`と`R_lower`の最大集約を`R_dir`へ変更した。
- `R_dir`は側別評価の補助集約量であり、正規Rではないことを英日で明記した。
- `R_dir`を正規状態分類へ接続する場合、評価前に固定されたCause-Sideドメイン変換規則から正規`delta`と`tau`を定めることを要求した。

### 12.2 検証結果

```text
REMAINING_R_MAX_CLEAR
FORMULA.md canonical_R_present=True
theory/NRA-IDE_Foundational_Thesis_Bilingual.md canonical_R_present=True
theory/THEORY.md canonical_R_present=True
DIFF_CHECK_OK
```

対象3文書の`R=max(...)`再定義は0件となり、各文書に正規`R = delta / tau`が残っていることを確認した。

### 12.3 次回再開位置

次の変更単位候補は`f(delta)`条件の下位文書同期である。Foundational Thesisと`theory/THEORY.md`の英日tau発展式へ、有限・非負・可積分条件、tauの非増加、正の累積消耗時だけ厳密減少する条件を継承する。

動的tauで使用する`f(EMA_upper)`は公理上の消耗率関数`f(delta)`と記号衝突しているため、条件追記と同時に意味を混在させず、別の変更単位として改名要否を判断する。`G(r)`の大残差近似と飽和語彙も別単位として保留する。

## 13. Phase 2 — f(delta)条件同期チェックポイント

- 実施日: 2026-07-14 JST
- 変更関係: 公理上のtau消耗率関数`f(delta)`の成立条件だけを下位文書へ継承
- 変更ファイル:
  - `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
  - `theory/THEORY.md`
- 変更しなかった事項: 動的tauの`f(EMA_upper)`と`g(EMA_lower)`、`G(r)`、実装、docs、RAW監査報告01～17

### 13.1 同期内容

- 対象とする各有限評価区間で`f(delta(s))`を有限、非負、可積分とした。
- 外生補充のない閉区間でtauは非増加とした。
- 区間`[t1,t2]`の累積消耗積分が正の場合に限り、`tau(t2) < tau(t1)`となることを英日で明記した。

### 13.2 検証結果

```text
EN_CONDITION_COUNT=2
JP_CONDITION_COUNT=2
DIFF_CHECK_OK
```

Foundational Thesisと`theory/THEORY.md`の双方に英日条件が存在することを確認した。動的tauの関数名はこの変更単位では変更していない。

### 13.3 次回再開位置

公理上の消耗率関数`f(delta)`と、側別有効ゲート幅を作る動的tauの形状関数`f(EMA_upper)`が同じ記号を使用している。次回は`FORMULA.md`、Foundational Thesis、`theory/THEORY.md`、正規参照実装候補における形状関数名の参照範囲を読取確認し、別記号への改名を一つの変更単位として実施可能か判断する。

`G(r)`の大残差近似`G(r) ~ r`と非飽和語彙への訂正は、その後の独立変更単位として保持する。

## 14. Phase 2 — 動的tau形状関数の記号分離チェックポイント

- 実施日: 2026-07-14 JST
- 変更関係: 公理上の消耗率関数`f(delta)`と動的tau形状関数の記号分離
- 採用記号: `h_upper`、`h_lower`
- 変更ファイル:
  - `FORMULA.md`
  - `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
  - `theory/THEORY.md`
  - `nra-core/foundations/NRA-IDE_Architecture_public.py`
  - `docs/NRA-IDE_Architecture_public.py`

### 14.1 同期内容

- 動的tauの形状関数`f(EMA_upper)`、`g(EMA_lower)`を`h_upper(EMA_upper)`、`h_lower(EMA_lower)`へ改名した。
- Pythonではdocstring内の数式とローカル変数`f_x`、`g_x`だけを対応名へ変更した。
- 計算式、戻り値、公開API、既存状態判定は変更していない。
- 正規参照実装候補とdocs公開コピーへ同一変更を適用した。

### 14.2 検証結果

```text
OLD_SHAPE_NAMES_CLEAR
PYTHON_MIRROR_HASH_MATCH=True
PYTHON_AST_OK count=2
DIFF_CHECK_OK
```

Python 2コピーのSHA-256は`F26428F8B63BD84DB585C399FA0A2B60197C342E94728E1B6CF199513C1E4432`で一致した。

### 14.3 次回再開位置

`FORMULA.md`と`theory/THEORY.md`の補完式について、`G(r)=r|r|/(k+|r|)`の大残差近似を`G(r) ~ r`へ訂正し、「飽和応答」を非有界の漸近線形応答へ改める。小残差近似、定義域、knee値、正負の符号を同じ変更単位で数値確認する。

## 15. Phase 2 — G(r)漸近挙動訂正チェックポイント

- 実施日: 2026-07-14 JST
- 変更関係: `G(r)=r|r|/(k+|r|)`の小残差・大残差挙動と用語の整合
- 変更ファイル:
  - `FORMULA.md`
  - `theory/THEORY.md`
- 変更しなかった事項: 正規R、`R_dir`、tau発展式、動的tau形状関数、Python実装、docs、RAW監査報告01～17

### 15.1 訂正内容

- 小残差で`G(r) ≈ r|r|/k`となり、rに対して二次的に小さいことを維持・明記した。
- 大残差で`G(r)/r -> 1`、すなわち`G(r) ~ r`となるよう訂正した。
- `G(r)`は奇関数でrの符号を保持し、漸近線形かつ非有界であることを明記した。
- 「飽和応答」を「小残差の二次応答から大残差の漸近線形応答への遷移」へ訂正した。

### 15.2 数値検証

検証条件は`k=2`とした。

```text
r        G(r)              G(r)/r
-200     -198.01980198      0.990099009901
-2       -1                 0.5
-0.002   -1.998001998e-06   0.000999000999001
0         0                 N/A
0.002     1.998001998e-06   0.000999000999001
2         1                 0.5
200       198.01980198       0.990099009901
```

```text
OLD_G_WORDING_CLEAR
G_NUMERIC_CHECK_OK odd=True zero=True knee=True small=True large=True
DIFF_CHECK_OK
```

最初の数値検証コマンドはPowerShellからPythonへ渡す引用符が崩れて構文エラーとなった。式の評価前に失敗したため、引用を単純化した同一検証を再実行し、上記のとおり合格した。

### 15.3 次回再開位置

Phase 2対象文書に対し、`R=max(...)`、旧形状関数`f(EMA_upper)`・`g(EMA_lower)`、`G(r) ~ r sgn(r)`、飽和応答、tau消耗条件不足の残存検索を行う。文脈を確認してPhase 2の完了可否を判定し、完了できる場合はPhase 3の正規参照実装再構成に進む前の受入条件を固定する。

## 16. Phase 2完了・Phase 3正規参照実装Report

- 実施日: 2026-07-14 JST
- 記録方針: 今後は個別変更ごとのCHKポイントを作成せず、精査・整合・検証結果をPhase単位のReportへ集約する。
- RAW監査報告01～17: SHA-256全17件一致、変更なし

### 16.1 Phase 2完了判定

対象:

- `FORMULA.md`
- `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
- `theory/THEORY.md`

残存検査:

```text
R_MAX_CLEAR
OLD_SHAPE_SYMBOLS_CLEAR
OLD_G_WORDING_CLEAR
F_CONDITIONS_EN=2
F_CONDITIONS_JP=2
WORK_DIFF_CHECK_OK
```

判定: **Phase 2対象の正規R、側別補助比、tau消耗条件、動的tau形状関数、G(r)漸近挙動は正典へ同期済み。**

この判定はPhase 2対象文書に限定する。リポジトリ全体整合済みを意味しない。

### 16.2 Phase 3受入条件

- `tau=0`は`OUT_OF_DESCRIPTION_DOMAIN`
- 負値、NaN、Infinity、不正・欠損閾値は`CONFESSION`
- `PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`を境界同値込みで実装
- 不可逆ラッチ後はR低下でも解除しない
- `R<1`は継続構造証言、`R>=1`は最終固定証言
- 二重ゆらぎ欄は常時存在し、未観測時は`NOT_OBSERVABLE`
- `R_dir`は補助監査値であり、正規状態を直接分類しない
- Effect-Side入力を構造変数の権威として使用しない
- 旧`rop`引数は互換aliasとして受理するが、`R_warn`・`R_irrev`不足時は推測せず`CONFESSION`
- 正規ソースとdocsミラーをSHA-256一致させる
- 標準ライブラリだけで境界適合テストを実行する

### 16.3 実装・テスト

変更・作成:

- `nra-core/foundations/NRA-IDE_Architecture_public.py`
- `docs/NRA-IDE_Architecture_public.py`
- `tests/test_nra_ide_reference.py`

実装結果:

- 正規7状態と閾値順序を実装した。
- tauゼロ、負値、非有限値、R計算の非有限化を分離した。
- 不可逆ラッチ、継続証言、最終固定証言を実装した。
- WARNING必須出力と欠損情報を固定構造で返す。
- 動的側別比は`DIRECTIONAL_AUXILIARY_ONLY`として返し、正規状態分類を禁止した。
- Cause-Side以外を構造入力権威として指定した場合は`CONFESSION`を返す。
- 正規ソースとdocs公開コピーを同一内容へ同期した。

最終検証:

```text
PYTHON_MIRROR_HASH_MATCH=True
SHA-256=8DEAC0DAB361EA8FC2731A781B893C09D6CDB295F1D4AC095CEB153BB5D57C38
PYTHON_AST_OK count=3
Ran 10 tests
OK
AXIOMS_JSON_PARSE_OK
DIFF_CHECK_OK
__pycache__ generated=none
```

適合テストは、各境界の直前・同値・直後、tauゼロ・負値・NaN・Infinity、閾値欠損・順序不正、不可逆ラッチ後のR低下、構造証言切替、二重ゆらぎ未観測・検出、Effect-Side拒否、`R_dir`補助限定、Pythonミラー一致を検証した。

### 16.4 検証中に解消した事項

初回ミラー検証は末尾空行差でSHA-256不一致となり、状態機械テスト前に停止した。最初の空行修正が同一文字列を持つ先頭関数境界へ適用されたため、2回目もミラー検証で停止した。byte差分で関数間空行と末尾空行を特定し、行文脈付きで修正した後、SHA-256一致と全テスト合格を確認した。

旧語彙検索で残った`tau<=0`は、構造感度関数の定義域検査とDynamicTauEngineコンストラクタの入力検査であり、正規状態を`FAIL_CLOSED`へ分類する処理ではない。

### 16.5 次工程

Phase 4として、`theory/SANDWICH_ARCH.md`、`theory/GOVERNANCE.md`、`theory/ETHICS.md`および関連する現行theory文書を読取精査し、正典参照順位、旧状態語彙、旧閾値、構造証言、Cause-Side / Effect-Side分離、過大表現の影響範囲を確定する。編集は一つの同期関係に限定する。

## 17. Phase 4 — 現行theory文書・基礎図版整合Report

- 実施日: 2026-07-14 JST
- 記録方針: 個別変更ごとのCHKポイントは作成せず、Phase 4の読取精査・整合・検証結果を本節へ集約した。
- RAW監査報告01～17: SHA-256全17件一致、変更なし

### 17.1 対象

文書:

- `theory/SANDWICH_ARCH.md`
- `theory/GOVERNANCE.md`
- `theory/ETHICS.md`

現行基礎図版と生成原稿:

- `theory/figures/TOP_sandwich.png`
- `theory/figures/NRA-IDE定義式（基礎式）.jpg`
- `theory/figures/sources/TOP_sandwich.svg`
- `theory/figures/sources/NRA-IDE_core_formula.svg`
- `docs/TOP_sandwich.png`
- `docs/nra_ide_formula_basic.jpg`

### 17.2 文書整合

- `SANDWICH_ARCH.md`の上位正規参照を、`theory/AXIOMS.md > theory/axioms.json > theory/NRA-IDE_Foundational_Thesis_Bilingual.md`へ日英同期した。
- `BOUNDARY_WARNING`の構造証言へ二重ゆらぎ状態を追加し、常時必須、観測不能時は`NOT_OBSERVABLE`と欠損理由、観測不能だけでは`CONFESSION`にしない規則を日英同期した。
- `GOVERNANCE.md`は、原初的な概念核・公理・設計方向をM-Tokuniへ帰属させつつ、現行リポジトリにはAI支援による編集・実装・翻訳・レビュー・検証が含まれ得ること、正典採用は作者または保守者のレビューと受入によることを明記した。
- `GOVERNANCE.md`の安全確保表現を、安全志向の理解・評価を支援する表現へ限定し、単独の安全性・適合性・特定領域での有効運用を保証しないことを日英同期した。
- `ETHICS.md`の禁止表現を作者の強い非拘束的要請として整理し、MIT Licenseの法的許諾を狭めず、拘束的用途制限には別のライセンス判断が必要であることを日英同期した。
- `ETHICS.md`末尾に残っていた編集メモ`Layout adjustment`を除去した。

### 17.3 図版再構成

正確な式、状態名、日本語、境界不等号を保持するため、画像生成モデルではなく決定論的なSVG原稿を作成し、同寸法のラスター画像へ描画した。

`TOP_sandwich.png`には次を反映した。

- Cause-Sideを構造変数と閾値の唯一の権威とする一方向構成
- 正規比`R = delta / tau`
- `PERMIT`から`RUPTURE_BOUNDARY`までの境界同値
- `tau=0`と不正入力の分類分離
- 不可逆ラッチ
- 二重ゆらぎ欄の常時出力
- `R<1`の継続構造証言と`R>=1`の最終固定証言
- Effect-Side / LLMによる状態上書き禁止

`NRA-IDE定義式（基礎式）.jpg`には次を反映した。

- 正規Rと側別補助量`R_upper`、`R_lower`、`R_dir`の分離
- tau消耗式と`f(delta)`の有限・非負・可積分条件
- `G(r)`の小残差二次応答と大残差漸近線形挙動
- 二重ゆらぎの`NOT_OBSERVABLE`規則
- ファイル配置だけでは適合性を付与しない原則

描画では、権限分離されたEdgeが`G:`の`file://`入力を白紙として撮影したため、作業ルート外へ原稿を複製せず、SVGを一時的な`data:` URLとして渡した。式図はPNGとJPGをそれぞれ原寸目視し、文字切れと全域描画を確認した同一バイト列だけを正式画像へ反映した。

### 17.4 検証

```text
RAW_REPORTS_01_17_HASH_MATCH=True
TOP_MIRROR_MATCH=True
TOP_SHA256=89ACEB3CDC8B38CE6A298200DBB45B501C05F268D9443DD87C92FE86B0DA3B8B
FORMULA_MIRROR_MATCH=True
FORMULA_SHA256=66A99F58DE91A642E7D1AFB0056A2E8F3980B0114FC73AC5FFFFC16A9D72CD65
PYTHON_MIRROR_MATCH=True
PYTHON_SHA256=8DEAC0DAB361EA8FC2731A781B893C09D6CDB295F1D4AC095CEB153BB5D57C38
TOP_DIMENSIONS=1024x1536
FORMULA_DIMENSIONS=1408x768
SVG_XML_OK
Ran 10 tests
OK
AST_JSON_OK
DIFF_CHECK_OK
```

残存語彙検索で検出した`R_dir = max(...)`、`fail_closed`原則、`does not permit spontaneous restoration`、`tau = 0 != FAIL_CLOSED`は、それぞれ補助量、正規原則、自然回復禁止、誤分類の明示的否定であり、旧仕様の残存ではないと文脈確認した。

判定: **Phase 4対象の現行theory文書と基礎図版は、確定済み正典判断へ整合した。**

### 17.5 次工程

Phase 5として、`docs/README.md`、`docs/README_JP.md`、`docs/Sandwich-ARCHITECTURE.md`、日英AI解説、現行HTML/SVG可視化を精査する。既知のローカルリンク切れ`docs/en-US/ai/08_discard_logs_EN.md`、旧状態語彙、旧閾値、正規Rと`R_dir`の混同、Cause-Side / Effect-Side逆流、外部フォント依存を文脈別に処理する。

## 18. Phase 5 — docs・現行HTML/SVG整合Report

- 実施日: 2026-07-14 JST
- 記録方針: 個別CHKポイントは作成せず、Phase 5の精査・整合・検証を本節へ集約した。
- RAW監査報告01～17: SHA-256全17件一致、変更なし

### 18.1 対象と正典名決定

対象は、docsルートREADME、サンドイッチ説明、日英AI解説、docs配下の現行HTML/SVG、正規参照実装の公開ミラーである。

精査中、同じ人間委譲点に`R_op`、`Rop`、`rop`、`R_handoff`が混在する正典名競合を検出した。利用者決定により`R_handoff`を正典名とし、旧3表記は`R_handoff`へ正規化する後方互換aliasだけとした。aliasは別の閾値・状態を定義しない。この決定を`AXIOMS.md`、`axioms.json`、上位theory文書、正規Python API、docsミラー、適合テストへ同期した。

### 18.2 文書整合

- `docs/README.md`、`docs/README_JP.md`、`docs/Sandwich-ARCHITECTURE.md`を、正規R、全7状態、tauゼロと不正入力の分離、不可逆ラッチ、Cause-Side / Effect-Side権限分離へ整合した。
- 日英AI解説の旧4状態、`SILENCE`・`HALT`、終端`FAIL_CLOSED`を正規状態表へ置換した。旧語を残した箇所は「正規状態ではない」という明示的説明に限定した。
- `R_irrev`を任意閾値として扱う説明を廃止し、`0 <= R_warn < R_handoff < R_irrev < 1`を固定順序とした。
- `R<1`だけで安全を立証する表現、RUPTUREを安全停止・自律停止とみなす表現、三層構造だけで安全性を保証する表現を、適合条件付きの構造的性質と限界へ修正した。
- 既知の英語Discard Logリンク切れを、存在する英語図版へ修正した。

### 18.3 現行可視化整合

- 共通M1～M5、統合HTML、英日Escapement、Causal Diode、Dam、Domain Tuningの表示状態と終端証言を正規語彙へ整合した。
- 近似値・範囲だけで状態を推測するM4例は`CONFESSION`へ変更した。
- 予測・学習を正規診断より優先するM5説明を補助用途へ限定し、Effect-Sideからの自動逆流を禁止した。
- 現行SVGの出力語彙を固定証言・監査記録へ修正し、検証で見つかった未エスケープ`&`を`&amp;`へ修復した。
- 6 HTMLに残っていたGoogle Fonts外部依存を除去した。

### 18.4 正規参照実装alias同期

正規APIは`r_handoff`を使用する。旧`r_op`キーワードと旧位置引数`rop`は互換入力としてだけ受理し、正規名とaliasが競合する場合は推測せず不正設定として扱う。docsミラーを同一バイト列へ同期し、互換・競合テストを追加した。

### 18.5 検証

```text
RAW_REPORTS_01_17_HASH_MATCH=True
MARKDOWN_LOCAL_BROKEN_LINKS=0
HTML_PARSE_COUNT=18
HTML_PARSE_ERRORS=0
INLINE_SCRIPT_COUNT=21
JS_SYNTAX_ERRORS=0
SVG_XML_PARSE_COUNT=4
SVG_XML_ERRORS=0
EXTERNAL_FONT_DEPENDENCIES=0
PYTHON_MIRROR_MATCH=True
PYTHON_SHA256=E100B6A546A6C62F3438CEA1B32B5B729A99CAAE50AF47CD03DBBE3FB249A35C
Ran 10 tests
OK
AXIOMS_JSON_PARSE_OK
DIFF_CHECK_OK
```

Browserプラグイン指定のNodeモジュールをin-app runtimeが解決できなかったため、実ブラウザ描画検証は実行不能だった。代わりに全HTMLの標準パース、全インラインJavaScriptのNode構文検査、全SVGのXMLパースを行った。この制約により、ブラウザ固有のレイアウト差まで合格を主張しない。

判定: **Phase 5対象のdocs文書、現行HTML/SVG、正規参照実装の委譲閾値名は、確定済み正典判断へ整合した。**

この判定はPhase 5対象に限定する。`nra-core/implementation`、`nra-core/visualization`、`nra-core/quantum`等の旧実装・研究デモに残る旧語彙を、現行正典として承認するものではない。

### 18.6 次工程

Phase 6として、`nra-core`および`note`配下の旧実装・研究資産を、正典・現行・例示・研究・履歴証拠に分類する。履歴証拠と研究由来を無断で書き換えず、現行または正規と自称する資産だけを整合対象とし、非正規デモには明示的な位置付けを付ける。

## 19. Phase 6 — 旧実装・研究資産の権威区分Report

- 実施日: 2026-07-14 JST
- 記録方針: 個別CHKポイントは作成せず、分類、最小注記、検証結果を本節へ集約した。
- RAW監査報告01～17: 変更なし

### 19.1 分類判断

`nra-core`と`note`には、日付付き論文、AIセッション統合記録、例示実装、研究可視化、量子拡張仮説、思想形成経路が保存されている。これらは研究来歴として価値を持つが、パス名、`Official`、`Final`、`確定版`、`core`等の名称だけで現行正典または適合実装とはならない。

現行の権威区分を次のとおり固定した。

- 現行正典と優先順位: ルート`theory/AXIOMS.md`
- 機械可読正典同期: `theory/axioms.json`
- 正規参照実装ソース: `nra-core/foundations/NRA-IDE_Architecture_public.py`
- `nra-core`内のその他: 個別昇格記録がない限り、研究、説明、例示、履歴資料
- `note`内: 個別昇格記録がない限り、非正規の研究、草稿、セッション、履歴資料

### 19.2 最小変更

- `nra-core/README.md`へ日英の権威区分を追加し、旧公理文書をcanonical sourceまたは正式最新版とする記述を修正した。
- `nra-core/implementation`を正規実装群ではなく、日付付き例示・プロトタイプとして位置付けた。
- `nra-core/visualization`を説明・研究用とし、実測器、安全証明、運用判断器ではないと明記した。
- `nra-core/quantum`を研究仮説・実験デモとし、量子装置上の有効性を主張しないと明記した。
- `note/README.md`を新設し、note全体の非正規性、正典参照先、履歴資料の取扱いを固定した。
- `note/NRA-IDE_Official_Definition.md`へ、`Official`が履歴上の作業名であるという直接注記を追加した。
- 日付付き旧公理文書と第二公理経緯文書へ、現行正典ではないという直接注記を追加した。

旧実装の`FAIL_CLOSED`、旧可視化の`NIRVANA`・`ELASTIC`・`CRITICAL`、旧量子APIの`R_op`等は、正典へ黙って書き換えず、非正規研究資産として保存した。これにより、研究来歴と現行仕様を分離した。

### 19.3 検証

```text
PYTHON_AST_COUNT=17
PYTHON_AST_ERRORS=0
NRA_CORE_NOTE_HTML_COUNT=24
INLINE_SCRIPT_COUNT=23
JS_SYNTAX_ERRORS=0
MARKDOWN_COUNT=56
MARKDOWN_LOCAL_BROKEN_LINKS=0
HISTORICAL_BODY_REWRITE=False
DIFF_CHECK_OK
```

初回Markdownリンク検査は数式の`[...](t)`をリンクと誤認し、Windows既定出力文字コードでも停止した。UTF-8出力へ固定し、相対ファイルパスまたは拡張子を持つリンクだけへ条件を限定して再実行し、実在するローカルファイルリンクに切れがないことを確認した。

判定: **Phase 6対象は、研究来歴を保持したまま現行正典との権威境界を明示できた。**

### 19.4 次工程

Phase 7として、リポジトリ全体の残存検査、manifest findingの解決状態、正典JSON、参照実装ミラー、テスト、図版ミラー、RAW報告ハッシュ、Git差分を最終照合する。RAW報告01～17は修正せず、訂正事項は本Reportとmanifestだけで閉じる。

## 20. Phase 7 — 第2次CLI精査 最終照合Report

- 実施日: 2026-07-14 JST
- RAW監査報告01～17: SHA-256全17件一致、変更なし
- 正典未決定事項: 0
- 第2次精査finding: 8件、未解決0件

### 20.1 finding状態の最終整合

- `CLI-VALID-001`: `CANON-001`とPhase 1正典同期により解決済みへ更新した。
- `CLI-VALID-002`: Phase 2の`G(r)`漸近挙動訂正により解決済みへ更新した。
- `CLI-CORRECT-001`: RAW報告12は変更せず、本Report 12.2および15.1の訂正記録で閉じた。
- `CLI-CORRECT-002`: RAW報告15・16は変更せず、本Report 12.2の実数訂正で閉じた。
- 正規参照実装、ローカルリンク、基礎図版ミラー、資産権威区分のfindingも、対応Phaseと適用ファイルへ結び付けた。

### 20.2 現行対象の残存語判定

現行正典・docs・正規参照実装に対する旧語検索で残ったものは、次の明示的な互換・否定・説明だけである。

- `R_op`、`Rop`、`rop`: `R_handoff`へ正規化する後方互換aliasの定義
- `NIRVANA`、`ELASTIC`、`CRITICAL`、`SILENCE`、`HALT`: 正規状態ではないことを説明する用語集・注意書き
- `tau = 0 != FAIL_CLOSED`: tauゼロを旧終端状態へ誤分類しないことの明示

旧実装・研究資産内の旧語はPhase 6の非正規分類下にあり、現行正典の残存とは判定しない。

### 20.3 最終検証

```text
MANIFEST_JSON=OK
CANONICAL_DECISIONS_PENDING=0
SECOND_PASS_FINDINGS=8
UNRESOLVED_FINDINGS=0
RAW_REPORTS_01_17_HASH_MATCH=True
Ran 10 tests
OK
PYTHON_MIRROR_MATCH=True
PYTHON_SHA256=E100B6A546A6C62F3438CEA1B32B5B729A99CAAE50AF47CD03DBBE3FB249A35C
TOP_MIRROR_MATCH=True
TOP_SHA256=89ACEB3CDC8B38CE6A298200DBB45B501C05F268D9443DD87C92FE86B0DA3B8B
FORMULA_MIRROR_MATCH=True
FORMULA_SHA256=66A99F58DE91A642E7D1AFB0056A2E8F3980B0114FC73AC5FFFFC16A9D72CD65
DIFF_CHECK_OK
```

実ブラウザ固有のレイアウト検証だけは、in-app BrowserプラグインのNodeモジュールが利用不能だったため未実施である。Phase 5でHTMLパース、インラインJavaScript構文、SVG XMLを検証済みであり、意味整合の完了判定は再開しない。将来ブラウザ経路が利用可能になった場合は、表示証拠だけを追加できる。

### 20.4 最終判定

**第2次CLI精査は完了した。**

- 確定した正典6判断は、正典文書、理論文書、正規参照実装、docs、現行可視化へ同期済み。
- RAW報告01～17は証拠として不変。
- 利用者既存変更は保持。
- 旧実装・研究・履歴資産は本文を遡及改変せず、現行正典との権威境界を明示。
- stage、commit、pushは実行していない。
