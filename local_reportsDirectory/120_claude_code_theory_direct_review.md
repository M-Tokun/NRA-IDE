# Report 120 — Claude Code理論直結ファイル群レビュー

- 実施日: 2026-07-16 JST
- 位置付け: Report 119（Claude Code再精査）完了後、ユーザー指示によるリポジトリ全体精査のうち「NRA-IDE理論直結」優先範囲を対象とした横断レビュー
- 対象: ルートメタ文書、theory/、FORMULA.md、llms.md/llms.txt、参照実装（docs・nra-coreのNRA-IDE_Architecture_public.py、tests/test_nra_ide_reference.py）、docs/en-US・docs/ja-JPのai文書、docs/figures HTML、gate/en・gate/jp、config/、src/、universal-definition/、nra-core/foundations
- スコープ外（ユーザー承認）: examples/、ground/、note/、cascade-failure-prevention/、multi-physics-safety-gate/、nra-ide-cancer-treatment-support-system/、nra-tcm-parser/、tools/、scripts/、local_reportsDirectory/（RAW監査証跡）
- レビュー基準: (1) 12の正式版補正条件（Report 119）の意義との整合性、(2) 文章の誤字・不整合、(3) 式・コードの間違いや記述ミス
- Git stage / commit / push: 実施なし（本Report作成含め、作業ツリーの変更のみ）

## 1. 全体方針

各ファイル・フォルダ単位で検出事項をチャット上に提示し、ユーザーの承認を得てから修正する「1単位質疑形式」を踏襲した。修正後は対象範囲についてMarkdownフェンス偶数性、JSON構文（`json.load`）、Python構文（`ast.parse`）、JS構文（`node --check`）、HTML div/scriptタグ平衡、および`tests/test_nra_ide_reference.py`（17件）の実行を都度行い、副作用がないことを確認した。

## 2. 用語統一（Handoff表現）

`theory/AXIOMS.md`の10.3節・2.2節に残っていた「責任を資格ある人間またはドメイン担当者へ委譲する」という記述が発端。これはReports 40〜114で26のAI解説文書から組織的に除去した「旧因果経路内で人間へ判断権限を渡す」と読める表現と同一パターンであり、最上位正典自身に未修正のまま残っていたことが判明した。

利用者判断: `AXIOMS.md`の原則的記述は文書全体の文脈（第14節のCause-Side/Effect-Side分離規則）で意味的には矛盾しないが、単独で引用される場合の曖昧さを避けるため、「固定Handoff証言を外部人間監査へ提示する」（英: "present predefined fixed Handoff testimony for external human audit"）へ統一する方針を採用。

### 修正対象ファイル

- `theory/AXIOMS.md`（2箇所）
- `theory/axioms.json`（`HANDOFF_REQUIRED.responsibility`フィールド）
- `theory/THEORY.md`（日英状態表2箇所）
- `theory/SANDWICH_ARCH.md`（日英箇条書き2箇所）
- `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`（日英6箇所）
- `FORMULA.md`・`llms.md`（該当箇所、`docs/README.md`は対象外の旧表現なしを確認）
- `docs/figures/M1_NRA_linear_breakdown_simulator.html`・`_EN.html`
- `docs/figures/M2_NRA_residue_tank.html`・`_EN.html`
- `docs/figures/M3_NRA_biomimetic_sandwich_svg.html`
- `docs/figures/NRA_IDE_interactive_docs_all_modules.html`（M1・M2セクション、複数箇所）
- `gate/en/nra_gate_axiom.py`・`gate/jp/nra_gate_axiom_JP.py`（docstring）
- `gate/en/nra_dual_survival_gate_EN.py`・`gate/jp/nra_dual_survival_gate_JP.py`（docstring・メッセージ）
- `nra-core/foundations/Nomological_Ring_Axioms_Code_Annotated_Explanation_Dual_Fluctuation_Stable.md`
- `nra-core/foundations/Nomological_Ring_AxiomsとIntensional_Dynamics_Engine.md`
- `nra-core/foundations/律環公理_コード付き解説_二重ゆらぎ安定版.md`

意図的に据え置いた表現: 「R_handoffで人間委譲が始まる」等、タイミング／名称としての言及（例: llms.md「Human handoff begins here, not at R=1.0」、`docs/figures/NRA_IDE_interactive_docs_all_modules.html`941行目・1233行目、`M5_NRA_IDE_flip_glossary.html`129行目）は、しきい値の名称・発生タイミングを述べるだけで因果方向を含意しないため据え置いた。

### 別途確認した境界事例

`docs/en-US/ai/09_risks_and_misuse_EN.md`等の26文書は既にReports 19〜118で修正済みのため対象外とし、残存検索のみ実施（該当なし）。`universal-definition/`の"Report facts only, delegate to human"（一般的なEnterprise Risks章の例示）はHANDOFF_REQUIREDの正式定義文ではないと判断し、変更しなかった。

## 3. 用語統一（τの旧称）

CITATION.cffの`"tau=tolerance boundary"`を発端に、τの正式名称「Absorption Thickness / 吸収厚み」への統一を実施。

- `CITATION.cff`
- `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`（日英2箇所、比較表・本文）
- `universal-definition/en/NRA-IDE_Universal_Definition_v1_0_full_EN.md`（3箇所）
- `universal-definition/jp/NRA-IDE_Universal_Definition_v1_0_full_JP.md`（3箇所）

`theory/AXIOMS.md`150行目の「許容幅」は否定文脈（τは許容幅ではない、の意）であり問題なしと判定。`nra-core/foundations/NRA-IDE_SecondAxiom_Journey_2026-04-22_0039_v2.md`（履歴資料指定済み）の用語選定の記述、および`Nomological_Ring_AxiomsとIntensional_Dynamics_Engine.md`の「吸収厚み（構造的許容幅、時間独立）」という correct-term-first の括弧併記は、利用者の指示により現状維持とした。

## 4. 正典・設計上の矛盾

### 4.1 用語統一とは別に発見した「正典」と「正規」の混在（本Report以前、同一セッション内で対応済み）

`docs/ja-JP/ai/`13ファイル、`FORMULA.md`、`theory/ETHICS.md`、`theory/GOVERNANCE.md`、`theory/NRA-IDE_Foundational_Thesis_Bilingual.md`、`docs/Sandwich-ARCHITECTURE.md`、`docs/README_JP.md`、`README_JP.md`、`llms.md`に混在していた「正典」（本来は文書間の優先順位を指す語）と「正規」（canonical状態・R・閾値を指す語）を、`AXIOMS.md`・`THEORY.md`自身の用法に合わせて「正規」へ統一した。`CODEX_CLI_BROWSER_WORKFLOW.md`・`REPOSITORY_OVERVIEW_PATCH.md`・`note/`・`nra-core`の日付付き旧文書は対象外（文書優先順位の意味で正しい用法、または履歴保存対象）とした。

### 4.2 R の二重定義

`nra-core/foundations/Nomological_Ring_AxiomsとIntensional_Dynamics_Engine.md`は17行目で「核心方程式」として`R = δ/τ`を定義しながら、35行目で同じ`R`を`max(δ_upper/τ_upper, δ_lower/τ_lower)`と再定義していた（Report 18のCLI-VALID-003と同型の不整合）。`R_dir`（補助集約量、正規Rを再定義しない）へ修正した。

### 4.3 Zone境界の記述矛盾

`config/structural_zones.md`・`_JP.md`は、図の目盛り（0.00/0.40/0.99/1.00）と本文の「Zone C: R ≥ 1.00」という記述が矛盾しており、`config/ide_foundation_config.json`の`zone_C.ratio_max=1.00`（`ratio<1.00`でZone C判定）とも整合していなかった。利用者判断により「Zone C: 0.99 ≤ R < 1.00」＋「Zone Cを超えて: R ≥ 1.00（アルファベットのZoneではない）」という3区分（A/B/C）設計に統一した。

### 4.4 未使用の非正規用語

`config/ide_foundation_config.json`の`physics_constants.nirvana_violation_threshold`は、`nra-core/README.md`の権威区分（Report 19）で「正規状態ではない」と明示分類された"NIRVANA"の残存であり、かつ`gate/`・`src/`のどこからも参照されない未使用値だったため削除した。

## 5. コードバグ（実害あり）

| # | ファイル | 内容 | 対応 |
|---|---|---|---|
| 1 | `docs/figures/M1_NRA_linear_breakdown_simulator.html`（日英）、`NRA_IDE_interactive_docs_all_modules.html` | R_handoff到達時（HANDOFF_REQUIRED）の状態表示が誤って`RUPTURE_BOUNDARY`と表示される（3箇所） | 表示ラベルを`HANDOFF_REQUIRED`／`HANDOFF`へ修正 |
| 2 | `gate/en/nra_gate_spatial.py`・`gate/jp/nra_gate_spatial_JP.py` | `SpatialContext.measure_distortion()`が3次元(x,y,z)のうちzを無視して距離計算 | `(x²+y²+z²)**0.5`へ修正 |
| 3 | `gate/en/nra_gate_threshold.py`・`gate/jp/nra_gate_threshold_JP.py` | フォールバック設定でlevel_3（EMERGENCY_BRAKE）とlevel_4（SYSTEM_HALT）が同名"Zone C"になり、現行config（`ide_foundation_config.json`にzone_Dが存在しない）で実際に到達する不具合 | `"Beyond Zone C"`へ改名し、コード内コメント`[ZONE-D]`も整合させた |
| 4 | `gate/en/nra_dual_survival_gate_EN.py`・`gate/jp/nra_dual_survival_gate_JP.py` | `NraStateDual.__post_init__`が範囲外・非有限の`value`/`threshold`を無条件でclampし、NRA-IDEの「不明値を類推・既定値で補完しない」原則に反する沈黙補正を行っていた | `_clamp_unit`を`_validate_unit`に置換し、範囲外・非有限値は`ValueError`で明示的に拒否するよう変更 |
| 5 | `gate/en/nra_gate_axiom.py`・`gate/jp/nra_gate_axiom_JP.py` | `_AUTHORITY`が`"HUMAN_DOCTOR_OF_AGRICULTURE"`という特定ドメイン固定文字列だった | `"QUALIFIED_HUMAN_DOMAIN_OPERATOR"`へ汎用化 |

## 6. ルート文書の精査漏れ

`docs/README.md`・`docs/README_JP.md`はCODEX_CLI_BROWSER_WORKFLOW.md Phase 5で修正済みだった一方、**リポジトリ直下の`README.md`・`REPOSITORY_OVERVIEW.md`はPhase 5の対象ファイル一覧に明記されておらず、第2次CLI精査を一度も受けていなかった**。結果として、Reports 44・46・49・66・70等で明示的に除去された`"hand off to a qualified human"`、および構成図の`"structural testimony + permitted explanation"`（Report 44で問題視され修正済みの曖昧表現）がそのまま残存していた。両ファイルとも修正した。

## 7. 検証結果サマリ

```text
MARKDOWN_FENCE_PARITY=OK（全編集ファイル）
JSON_PARSE=OK（axioms.json, ide_foundation_config.json, ide_presets.json）
PYTHON_AST_PARSE=OK（gate/en, gate/jp, docs/NRA-IDE_Architecture_public.py, nra-core/foundations/NRA-IDE_Architecture_public.py 相当）
JS_SYNTAX_CHECK（node --check）=OK（docs/figures 配下の抽出スクリプト全件）
HTML_TAG_BALANCE（div/script）=OK
REFERENCE_TEST_SUITE=Ran 17 tests / OK（本Reportの編集それぞれの後に再実行）
GATE_DEMO_EXECUTION=OK（nra_gate_threshold.py, nra_dual_survival_gate_EN/JP.py の実行確認）
```

## 8. 未実施・スコープ外

- stage、commit、pushは実施していない。
- `note/`、`cascade-failure-prevention/`、`multi-physics-safety-gate/`、`nra-ide-cancer-treatment-support-system/`、`nra-tcm-parser/`、`tools/`、`scripts/`は「NRA-IDE理論直結優先」の方針によりスコープ外とした（未精査）。
- `src/`は分量（5783行、9ファイル）のためgrep横断検査に留め、最小の`biodynamic_ide_engine_v2_2026-04-06_1947.py`のみ全文精読した。残り8ファイルの全文精読は未実施。

## 9. 次工程

残りのサブプロジェクト群（note/以下等）を精査するか、ここでいったん区切ってGit差分の確認・棚卸しに進むかは利用者判断待ちとする。
