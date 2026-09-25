# 概念依存マップ（NRA-IDE）

生成日: 2026-09-22

本文書は、リポジトリ全体を対象に、どの概念がどのファイルで定義され、どのファイルがそれを参照・依存しているかを機械的に洗い出した結果である。既存ファイルは変更していない（読み取り専用タスク）。

機械可読版: [`CONCEPT_DEPENDENCY_MAP.json`](./CONCEPT_DEPENDENCY_MAP.json)

---

## 1. 対象範囲・除外・手法（俯瞰視点）

本タスクの前提として使用した正規参照順序は次のとおりであり、変更していない。

1. `theory/AXIOMS.md`
2. `theory/axioms.json`
3. `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
4. `theory/SANDWICH_ARCH.md`
5. `theory/THEORY.md`
6. `FORMULA.md`
7. `llms.md`
8. ドメイン固有規則
9. 正規参照実装（`nra-core/foundations/NRA-IDE_Architecture_public.py`）
10. その他実装コード
11. コメント・例示・AI生成説明

`REPOSITORY_OVERVIEW.md` と `llms.txt` は、この正規参照順序**を宣言する**索引文書であり、順序表11項目そのものには含まれない。両ファイルは参照先の検索対象には含めたが、definition_file（最上位定義ファイル）の候補としては扱っていない。`REPOSITORY_OVERVIEW.md`でのみ言及が確認された概念がある場合は、各概念の`note_order_meta_files`に記録した。

### 1.1 検索から除外したディレクトリ・ファイル群

- .git/ — Gitリポジトリ内部データ。テキスト文書ではない。
- .kilo/worktrees/（horse-production, longhaired-manicure, quickest-dash）— 別AIツール（Kilo）が使用する、本リポジトリのgit worktreeによる複製（各800〜930ファイル）。ルート作業ツリーと同一内容がブランチ違いで重複するため、概念の一次資料としては除外した。
- .hypothesis/, __pycache__/ — テスト・実行時生成キャッシュ。
- .obsidian/ — Obsidianエディタのローカル設定。
- local_reports/han_validation_deps/ — click, flask, itsdangerous, jinja2, markupsafe, werkzeug のベンダリング済みサードパーティ依存コード（約350ファイル）。NRA-IDE概念の一次資料ではない。

上記以外の `.md` / `.json` / `.py` / `.html` ファイル（計814ファイル、履歴資産9件を除く）を検索対象とした。

### 1.2 概念抽出・definition_file・defining_sectionの機械的手法

対象範囲（本ファイルのscope_exclusions・historical_assets_excluded_from_graphを除く、リポジトリ内の.md/.json/.py/.htmlファイル814件）内のテキストを正規表現で機械検索し、各概念について、正規参照順序1〜7番目の単一ファイル（theory/AXIOMS.md, theory/axioms.json, theory/NRA-IDE_Foundational_Thesis_Bilingual.md, theory/SANDWICH_ARCH.md, theory/THEORY.md, FORMULA.md, llms.md）および9番目（nra-core/foundations/NRA-IDE_Architecture_public.py）のうち最上位でその概念に一致した箇所を検出したファイルをdefinition_fileとした。defining_sectionは、そのファイル内での最初の一致行の直近上位見出しを機械的に採用した（必ずしも当該概念の最も詳細な定義節と一致しない場合がある）。8・10・11番目（ドメイン固有規則／その他実装コード／コメント・例示・AI生成説明）は、正規参照順序自体が個別ファイルを指定していないため、ディレクトリ・拡張子に基づく作業上の機械分類（本文書独自、正規参照順序の一部ではない）を用いた。

8・10・11番目の階層内でのファイル間の細かい優劣（ドメイン固有規則 vs その他実装コード vs コメント・例示、それぞれの内部での順位）は、正規参照順序自体が個別ファイルを指定していないため 確定できない。該当する場合は「不明」として扱い、断定していない。

### 1.3 「概念」の定義と抽出方法

太字・見出し・コードブロック内で固有名として使用され、かつ**複数ファイルにまたがって使用されている**語・記号・数式・状態名を概念として抽出した。1ファイルにしか出現しなかった候補は、この定義（複数ファイルにまたがる使用）を満たさないため対象から除外した。除外した候補は次のとおり。

- 告白と構造開示 / Confession and Structural Disclosure（`confession_disclosure`） — 1ファイルのみで検出
- コア評価アルゴリズム / Core Evaluation Algorithm（`core_eval_algorithm`） — 1ファイルのみで検出
- 禁止される置換・補完 / Forbidden Substitution and Completion（`forbidden_substitution`） — 1ファイルのみで検出
- アイデンティティ固定 / Identity Lock（`identity_lock`） — 1ファイルのみで検出
- 禁止される再解釈 / Prohibited Reinterpretations（`prohibited_reinterpretations`） — 1ファイルのみで検出
- 要約規則 / Summary Rule（`summary_rule`） — 1ファイルのみで検出

この抽出は正規表現によるテキスト一致に基づく機械処理である。特に短い記号（δ, τ, R など）は、$…$ / \(…\) / \delta 等のLaTeX表記、`…` によるコード表記、または英語での明示表記（"delta", "tau"）に一致範囲を絞り、無関係な一致を避けた。

## 2. 検証手順の実施結果

AXIOMS.md 16節の規則（下位文書は上位定義を上書きしてはならない）に基づき、各概念についてdefinition_file以外のファイルが当該概念に独自の見出しを与えている箇所（lower_tier_redefinition候補）をすべて洗い出したうえで、本文を直接精査し、「表現の言い換え」か「定義内容そのものの相違」かを判定した。

`local_reports/` および `local_reportsDirectory/` 配下は、他文書の不備を指摘する過去の監査報告（`*_pending_*` / `*_revalidation` など、本リポジトリ独自の監査タクソノミーである`HARD_CONFLICT`等のラベルを使用）であり、概念そのものの再定義ではないため、lower_tier_redefinitionの候補からは除外した（referenced_inには残置）。

精査の結果、独自の見出しを持つ候補が存在した概念は45概念中複数あったが、精査後にlower_tier_redefinitionとして残ったのは次の6概念である（他はすべて言い換え・敷衍と確認済み、または対象外と確認済みで空配列とした）。

### δ（蓄積ズレ / accumulated deviation）

- definition_file: `theory/AXIOMS.md`（L44 ## 1. 凡例 / Notation）
- 候補ファイル: `cascade-failure-prevention/gate/han_gate_service.py`
  - 判定: `CONFIRMED_DIFFERENT_CONTENT`
  - 根拠: cascade-failure-prevention/gate/han_gate_service.py のコメントは、正典の一次式 R=δ/τ（除算）とは逆に、本実装が R = r_raw × τ_dynamic（乗算、動的τ・EMAベース）であり「正典のR=δ/τをそのまま実装したものではない」と自己申告している。用語（δ, τ, R, 二重ゆらぎ, Fail-Closed）は正典と共有するが、計算内容そのものは正典の一次式・二次式と異なる、ドメイン固有の別実装である。内容相違として確認済み（自己開示あり、隠蔽ではない）。
  - 該当箇所（一部）: `L15 # τが静的定数 → δ(入力ゆらぎ)のみが変動 → 山が尖る`, `L22 # δ(r_raw)が上昇し始めると、τも連動して大きくなる。`, `L26 # δ静定後はEMAが減衰し、τが基底値に戻る。` 等

### τ（吸収厚み / absorption thickness）

- definition_file: `theory/AXIOMS.md`（L44 ## 1. 凡例 / Notation）
- 候補ファイル: `cascade-failure-prevention/gate/han_gate_service.py`
  - 判定: `CONFIRMED_DIFFERENT_CONTENT`
  - 根拠: cascade-failure-prevention/gate/han_gate_service.py のコメントは、正典の一次式 R=δ/τ（除算）とは逆に、本実装が R = r_raw × τ_dynamic（乗算、動的τ・EMAベース）であり「正典のR=δ/τをそのまま実装したものではない」と自己申告している。用語（δ, τ, R, 二重ゆらぎ, Fail-Closed）は正典と共有するが、計算内容そのものは正典の一次式・二次式と異なる、ドメイン固有の別実装である。内容相違として確認済み（自己開示あり、隠蔽ではない）。
  - 該当箇所（一部）: `L11 # 二重ゆらぎ構造（動的τ）追加`, `L14 # 従来: R = r_raw * τ_static`, `L15 # τが静的定数 → δ(入力ゆらぎ)のみが変動 → 山が尖る` 等

### Fail-Closed

- definition_file: `theory/AXIOMS.md`（L91 ### 解釈境界コメント）
- 候補ファイル: `cascade-failure-prevention/gate/han_gate_service.py`
  - 判定: `CONFIRMED_DIFFERENT_CONTENT`
  - 根拠: cascade-failure-prevention/gate/han_gate_service.py のコメントは、正典の一次式 R=δ/τ（除算）とは逆に、本実装が R = r_raw × τ_dynamic（乗算、動的τ・EMAベース）であり「正典のR=δ/τをそのまま実装したものではない」と自己申告している。用語（δ, τ, R, 二重ゆらぎ, Fail-Closed）は正典と共有するが、計算内容そのものは正典の一次式・二次式と異なる、ドメイン固有の別実装である。内容相違として確認済み（自己開示あり、隠蔽ではない）。
  - 該当箇所（一部）: `L2 # TITLE: HAN Gate — Cascade Failure Prevention (Fail-Closed)`, `L52 # Config (Fail-Closed) — 環境変数で上書き可能`
- 精査範囲についての注記: candidate件数が多く（30件超）、README/REPOSITORY_OVERVIEW/docs(en-US,ja-JP)/theory各文書等の代表的抜粋を精査。確認した範囲は言い換え・敷衍のみ。cascade-failure-prevention内の複数ファイルもhan_gate_service.pyと同一の自己開示済み別実装を指す（個別列挙は省略）。

### 二重ゆらぎ / Double-Fluctuation

- definition_file: `theory/AXIOMS.md`（L201 ### IDE計算式の権威区分 / Authority Classification of IDE Formula Systems）
- 候補ファイル: `cascade-failure-prevention/gate/han_gate_service.py`
  - 判定: `CONFIRMED_DIFFERENT_CONTENT`
  - 根拠: 「二重ゆらぎ」という用語を、正典（FORMULA.md §4：上側・下側δの非対称EMA追跡）とは異なる、EMAで動的τを変調する独自機構（R=r_raw×τ_dynamic）に用いている。自己開示あり（コード内コメントで正典と異なる旨を明記）。
  - 該当箇所（一部）: `L11 # 二重ゆらぎ構造（動的τ）追加`, `L13 # 【二重ゆらぎ構造について】`, `L59 # 二重ゆらぎパラメータ` 等
- 候補ファイル: `cascade-failure-prevention/docs/SPEC.md`
  - 判定: `CONFIRMED_DIFFERENT_CONTENT`
  - 根拠: han_gate_service.pyと同一の独自「二重ゆらぎ」（動的τ・EMA変調）を仕様として記述。
  - 該当箇所（一部）: `L84 ## 4. R の計算式（二重ゆらぎ版）`
- 精査範囲についての注記: cascade-failure-prevention配下の他ファイル（New_v2_jp_en_2026-03-06.md, docs/RUNBOOK.md, tools/han_validation_test.py, 日本語総合解説.md）も同一の独自機構を指しており、上記2件と同じ事実の重複記録となるため個別列挙は省略した。

### 復元劣化 / Restoration Degradation

- definition_file: `theory/AXIOMS.md`（L418 ## 8. NRA-IDE構造原則：復元劣化 / NRA-IDE Structural Principle: Restoration Degradation）
- 候補ファイル: `nra-core/implementation/NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py`
  - 判定: `UNCERTAIN_STALE_LABEL`
  - 根拠: nra-core/implementation/NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py は コード冒頭コメントで `theory/AXIOMS_rewritten_2026-04-24_011508.md`（失効・非正規、本文書の履歴資産区分に該当）を参照元とし、その版の公理番号（公理2, 3, 4, 5, 6, 8）で実装内容を説明している。実装内容（τ>0の定義域制約、τ_restored<τ_0の復元劣化、R≥1でのFail-Closed）自体は現行 theory/AXIOMS.md v2.1 の対応箇所と整合するが、コメント中の公理番号ラベルは失効版のものであり現行版の節番号と一致しない。内容相違ではなく呼称（ラベル）の古さであるため、断定せず要確認として記録する。
  - 該当箇所（一部）: `L10 # 公理2（δ蓄積/τ消耗）、公理4（τ消耗積分）、公理5（復元劣化）を実装。`, `L20 # 一度の相転移後、τ は初期値に戻らない（復元劣化）。`

### 定義域制約 / Domain Constraint

- definition_file: `theory/AXIOMS.md`（L295 ## 6. 定義域制約 / Domain Constraint）
- 候補ファイル: `nra-core/implementation/NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py`
  - 判定: `UNCERTAIN_STALE_LABEL`
  - 根拠: nra-core/implementation/NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py は コード冒頭コメントで `theory/AXIOMS_rewritten_2026-04-24_011508.md`（失効・非正規、本文書の履歴資産区分に該当）を参照元とし、その版の公理番号（公理2, 3, 4, 5, 6, 8）で実装内容を説明している。実装内容（τ>0の定義域制約、τ_restored<τ_0の復元劣化、R≥1でのFail-Closed）自体は現行 theory/AXIOMS.md v2.1 の対応箇所と整合するが、コメント中の公理番号ラベルは失効版のものであり現行版の節番号と一致しない。内容相違ではなく呼称（ラベル）の古さであるため、断定せず要確認として記録する。
  - 該当箇所（一部）: `L135 # 公理3 定義域制約（τ > 0）と公理6 破断判定を実装。`

上記のうち `CONFIRMED_DIFFERENT_CONTENT` と判定した箇所は、`cascade-failure-prevention/gate/han_gate_service.py`（および同ディレクトリの関連ファイル）が、正典の一次式 `R=δ/τ`（除算）とは逆方向の `R = r_raw × τ_dynamic`（乗算、動的τ・EMAベース）を実装している事実に集約される。当該ファイル自身のコメントが「正典のR=δ/τをそのまま実装したものではない」と明記しており、自己開示済みのドメイン固有別実装であって、隠れた矛盾ではない。

`UNCERTAIN_STALE_LABEL` と判定した箇所（復元劣化・定義域制約）は、`nra-core/implementation/NRA_IDE_Axiom2_HistoricalAccumulation_20260425_2202.py` が、失効・非正規と確認済みの `theory/AXIOMS_rewritten_2026-04-24_011508.md`（本文書3節の履歴資産に該当）の公理番号ラベルをコメント中で使用している事例である。実装内容（τ>0、τ_restored<τ_0、R≥1でのFail-Closed）自体は現行 `theory/AXIOMS.md` v2.1 と整合しており、内容の相違ではなくラベルの古さと見られるが、断定せず要確認としている。

`canonical_state_classification`（正規状態分類）については、`WEB_RESEARCH_PROTOCOL.md` の「6. 証拠の状態分類」が検索パターン上一致したが、内容を直接確認したところ、探索情報の検証状態（candidate/verified/adopted/excluded）についての別概念であり、NRA-IDEの正規七状態とは無関係と判明したため、referenced_in・lower_tier_redefinitionの双方から除外した（同名衝突による誤検出の訂正）。

---

## 3. 概念一覧表

| 概念 | 定義ファイル | 参照ファイル数 | lower_tier_redefinition | orphan |
|---|---|---:|---|---|
| 唯一の律環公理 / Sole Nomological Ring Axiom（存在は生成である。/ Existence is Generation.） | `theory/AXIOMS.md` | 55 | なし | いいえ |
| δ（蓄積ズレ / accumulated deviation） | `theory/AXIOMS.md` | 377 | あり | いいえ |
| τ（吸収厚み / absorption thickness） | `theory/AXIOMS.md` | 408 | あり | いいえ |
| R（境界接近比 / boundary-approach ratio） | `theory/AXIOMS.md` | 116 | なし | いいえ |
| M_R（残存比マージン / remaining ratio margin） | `theory/AXIOMS.md` | 21 | なし | いいえ |
| M_τ（残存吸収マージン） | `theory/AXIOMS.md` | 23 | なし | いいえ |
| R_warn | `theory/AXIOMS.md` | 89 | なし | いいえ |
| R_handoff（別名 R_op / Rop / rop） | `theory/AXIOMS.md` | 131 | なし | いいえ |
| R_irrev | `theory/AXIOMS.md` | 98 | なし | いいえ |
| PERMIT | `theory/AXIOMS.md` | 105 | なし | いいえ |
| BOUNDARY_WARNING | `theory/AXIOMS.md` | 79 | なし | いいえ |
| HANDOFF_REQUIRED | `theory/AXIOMS.md` | 109 | なし | いいえ |
| IRREVERSIBLE_TRANSITION | `theory/AXIOMS.md` | 88 | なし | いいえ |
| RUPTURE_BOUNDARY | `theory/AXIOMS.md` | 197 | なし | いいえ |
| CONFESSION | `theory/AXIOMS.md` | 92 | なし | いいえ |
| OUT_OF_DESCRIPTION_DOMAIN | `theory/AXIOMS.md` | 84 | なし | いいえ |
| Cause-Side | `theory/AXIOMS.md` | 203 | なし | いいえ |
| Effect-Side | `theory/AXIOMS.md` | 188 | なし | いいえ |
| Π（射影 / Projection） | `theory/SANDWICH_ARCH.md` | 9 | なし | いいえ |
| Π⁻¹（逆射影 / Inverse Projection） | `theory/SANDWICH_ARCH.md` | 36 | なし | いいえ |
| irreversible_latched（不可逆ラッチ） | `theory/AXIOMS.md` | 144 | なし | いいえ |
| Fail-Closed | `theory/AXIOMS.md` | 243 | あり | いいえ |
| 構造証言 / Structural Testimony | `theory/AXIOMS.md` | 43 | なし | いいえ |
| STRUCTURAL_DISCLOSURE_LOG | `theory/AXIOMS.md` | 17 | なし | いいえ |
| INPUT_EXCEPTION_LOG | `theory/AXIOMS.md` | 23 | なし | いいえ |
| Layer 01/02/03（NRA INPUT GATE / LLM CORE / NRA OUTPUT GATE） | `theory/SANDWICH_ARCH.md` | 10 | なし | いいえ |
| NRA INPUT GATE | `theory/SANDWICH_ARCH.md` | 2 | なし | いいえ |
| LLM CORE | `theory/SANDWICH_ARCH.md` | 10 | なし | いいえ |
| NRA OUTPUT GATE | `theory/SANDWICH_ARCH.md` | 2 | なし | いいえ |
| Boundary Evaluator / 境界評価器 | `theory/SANDWICH_ARCH.md` | 6 | なし | いいえ |
| Output Composer / OUTPUT COMPOSER | `theory/SANDWICH_ARCH.md` | 2 | なし | いいえ |
| Trust Boundary / 信頼境界 | `theory/SANDWICH_ARCH.md` | 8 | なし | いいえ |
| 二重ゆらぎ / Double-Fluctuation | `theory/AXIOMS.md` | 89 | あり | いいえ |
| 構造感度 / Structural Sensitivity | `theory/AXIOMS.md` | 12 | なし | いいえ |
| 非対称EMA / Asymmetric EMA | `FORMULA.md` | 6 | なし | いいえ |
| 補完式（ハイブリッド補完）/ Complementary Formula (Hybrid Complement) | `theory/AXIOMS.md` | 21 | なし | いいえ |
| knee値 / Knee Value | `theory/THEORY.md` | 6 | なし | いいえ |
| 記号予約 / Reserved Symbols | `FORMULA.md` | 2 | なし | いいえ |
| τ非自然回復 / Non-Spontaneous Tau Recovery | `theory/AXIOMS.md` | 5 | なし | いいえ |
| 復元劣化 / Restoration Degradation | `theory/AXIOMS.md` | 6 | あり | いいえ |
| 定義域制約 / Domain Constraint | `theory/AXIOMS.md` | 2 | あり | いいえ |
| 禁止解釈 / Prohibited Interpretations | `theory/SANDWICH_ARCH.md` | 2 | なし | いいえ |
| 観測経路喪失 / Channel-State Separation and Observation Loss | `theory/AXIOMS.md` | 2 | なし | いいえ |
| 正規境界順序 / Canonical Boundary Order | `theory/NRA-IDE_Foundational_Thesis_Bilingual.md` | 6 | なし | いいえ |
| 正規状態分類 / Canonical State Classification | `theory/AXIOMS.md` | 21 | なし | いいえ |

---

## 4. 履歴資産（現行の依存関係グラフから除外）

冒頭に SUPERSEDED / DO NOT APPLY / 非正規 / Noncanonical 等の失効表記がある文書として、次の9件を検出した。現行の依存関係グラフ（上記1〜3節）には含めていない。

- `REPOSITORY_OVERVIEW_PATCH.md`
- `nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.md`
- `nra-core/foundations/NRA-IDE_SecondAxiom_Journey_2026-04-22_0039_v2.md`
- `note/01_理論・公理_検討覚書/NRA-IDE_Official_Definition.md`
- `nra-core/foundations/Nomological_Ring_AxiomsとIntensional_Dynamics_Engine.md`
- `nra-core/foundations/Nomological_Ring_Axioms_Code_Annotated_Explanation_Dual_Fluctuation_Stable.md`
- `nra-core/foundations/律環公理_コード付き解説_二重ゆらぎ安定版.md`
- `nra-core/foundations/NRA-IDE_の応用分野_汎用性の全体像.md`
- `nra-core/foundations/NRA-IDE_動的厚みと不可逆境界_会話統合_26-0802-1830.md`

---

## 5. 全体判定

完了。docs/CONCEPT_DEPENDENCY_MAP.json（機械可読、45概念、概念ごとのdefinition_file / defining_section / referenced_in / lower_tier_redefinition / orphan_referenceを含む）と、本ファイルを新規作成した。既存ファイルへの変更はない。orphan_reference（正規参照順序内に定義が見当たらない概念）に該当する概念はなかった。
