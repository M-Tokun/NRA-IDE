# note/nra-ide-hybridcalc-quantum-architecture-next_ver 精査報告

- 検査日: 2026-07-14 JST
- 対象: `note/nra-ide-hybridcalc-quantum-architecture-next_ver` 直下20ファイル
- 基準: ルート正典 v2.1、`llms.md`、`llms.txt`、`FORMULA.md`、既精査済み theory / nra-core
- 総合判定: **不合格（研究開発ログとしては有用だが、現行正典準拠の完成資料群ではない）**

## 1. 結論

このディレクトリは、2026年4月時点の量子拡張に関する研究ノート、評価ログ、論文草稿、可視化、PDF複製を保存した作業領域である。READMEの `Draft / Research Development` という位置付けは実態に合う。

一方、同じ階層に「未完了」「部分対処」「確定」「完成」「4穴すべて解決済」という相互に異なる成熟度表示が混在する。現行v2.1より前の `FAIL_CLOSED`、沈黙域、単一比率、`max` 集約を中心に構成され、現行の状態語彙、排他的因果チャネル、不可逆ラッチ、証言継続、`tau<=0` の記述領域外分離を備えない。

量子物理上も、Lindblad方程式の採用、期待値ベクトル、誤差層別化、相関監視を「確定」「縮減上界」「検証済」と呼ぶには導出・校正・再現可能な数値実験が不足する。したがって、完成理論または現行正典の量子実装としては採用できない。

## 2. ファイル別判定

| # | ファイル | 判定 | 主な指摘 |
|---:|---|---|---|
| 1 | `NRA-IDE_Correlation_Examples_JP_v1_20260426.html` | 要修正 | 相殺・増幅・相関変質を説明する例示としては使えるが、合成データと固定パラメータによる演示であり、一般的な安全性や検出完全性の証明ではない。単位、閾値校正、統計的不確実性、現行状態語彙がない。 |
| 2 | `NRA-IDE_error_tracking_summary_JP_20260426_035916.md` | 参考資料 | 欠測を補完せず記録すること、観測相関と推定相関を分離することは現行原則と部分整合する。一方、`MISSING`、`OUT_OF_BAND`、`TRACKING_UNAVAILABLE`、`FAIL_CLOSED` 等の旧分類で、v2.1の `OUT_OF_DESCRIPTION_DOMAIN`、`IRREVERSIBLE_BOUNDARY`、`RUPTURE` との写像がない。 |
| 3 | `NRA-IDE_ErrorRelation3D_JP_v1_20260426_025834.html` | 要修正 | net/gross/correlationの関係を視覚化する教材だが、可視化された関係を物理的・統計的帰結として扱えない。合成入力、固定係数、単位・母集団・信頼区間・校正手順が未定義。 |
| 4 | `NRA-IDE_FourLayerError_Interactive_2026-04-29_1648_JP.html` | 不合格 | classical/shot/decoherence/gate の二乗和は独立・無相関等の仮定を明記せず、異種誤差を同一量として合算する。時間・確率・振幅・許容幅の次元対応と、表示が主張する「四層構造」の妥当性が未確立。 |
| 5 | `NRA-IDE_quantum_extension_systematized_paper_2026-04-22_205812_JST.md` | 不合格 | B1-B3と縮減主張を体系化するが、Lindbladの適用条件、期待値測定コスト、誤差独立性、閾値校正、上界証明が不足する。非有界な `C(r)` を飽和と呼び、旧沈黙/Fail-Closedモデルを使用する。 |
| 6 | `NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md` | 不合格 | 「完成版」に反して、VQE指数増大とNRA-IDE有界化、古典複雑度縮減、Fail-Closed時刻等が仮定・導出不足。`C(r)` の飽和誤認、Lindblad Euler離散化、異種量の `tau_total=min(...)` が残る。 |
| 7 | `NRA-IDE_QuantumArchitecture_NextVer_B1toB3_2026-04-21_0220_JP.md` | 不合格 | B1=Lindblad、B2=期待値ベクトル、B3=層別境界を「確定」とするが、対象系・観測量・測定・数値積分・校正・完全正値性を確定していない。三縮減上界も未証明。 |
| 8 | `NRA-IDE_QuantumArchitecture_Revised_2026-04-21_0141_JP.md` | 要修正 | 強い断定を一部抑え、量子ノイズと構造監査を分離しようとする点は改善。ただし式・状態遷移・物理量の具体化が不足し、現行v2.1への接続もない。 |
| 9 | `NRA-IDE_QuantumArchitecture_RevisedEval_2026-04-21_0125_JP.md` | 不合格 | 生成時刻01:25の評価文が、生成時刻01:41の `Revised` を評価対象としており、時系列が成立しない。対象版またはタイムスタンプの誤りを訂正しない限り評価証跡として信頼できない。 |
| 10 | `NRA-IDE_QuantumCorrelation_MinSim_JP_v1_20260426_020310.html` | 不合格 | 個別 `Z` 期待値を安定させたまま相関だけを任意に劣化させる表示が、採用した二量子ビット状態の物理制約と整合しない。正値な密度行列・CPTP発展・測定統計に基づくシミュレーションではなく、結論を埋め込んだ演示。 |
| 11 | `NRA-IDE_QuantumFlow_Interactive_EN_20260424.html` | 不合格 | 「10 methods」に対して8項目のみ。従来法の共通原因を過度に一般化し、B1-B3を未検証のままconfirmedとする。`C(r)` saturation、silence、旧Fail-Closed、外部Google Fonts依存がある。 |
| 12 | `NRA-IDE_QuantumFlow_Interactive_EN_v2_20260424.html` | 不合格 | Phase 5で「4 holes resolved」とする一方、Hole 4を `partially addressed` と明記する直接矛盾。重み・閾値・相関参照・測定コスト・完全性が未解決で、解決済表示は不適切。 |
| 13 | `NRA-IDE_QuantumFlow_Interactive_JP_20260424.html` | 不合格 | EN v1の問題を継承。末尾の `C_ij=<O_i><O_j>` は相関または共分散ではない。UI説明の左右配置も実画面と逆。 |
| 14 | `NRA-IDE_QuantumFlow_Interactive_JP_v2_20260424.html` | 不合格 | EN v2と実質同内容。穴4の部分対処と全穴解決が矛盾。`delta_t^2=sum w_i(r_i/tau_i)^2` 後の `R_t=delta_t/tau_t` は二重正規化。ノイズ増大時の低重み化と `tau_C=max(...)` が警報を二重に弱めうる。 |
| 15 | `NRA-IDE_QuantumPipeline_Interactive_2026-04-29_1648_JP.html` | 不合格 | Lindblad密度行列と説明するが、実装は単一スカラーの経験的更新。NRA参照も外部固定記録ではなく補正済み予測履歴。`R>=1` 後も更新を続け、不可逆ラッチなし。`R_low>R_high` を許し、tau分母を `1e-6` へ暗黙置換する。 |
| 16 | `NRA-IDE_量子計算拡張_整形版_2026-04-22_2043_JP.md` | 参考資料 | 「検討ログ整理版」「未完了」「つづく」と明示するため、履歴資料としては位置付け可能。ただし原文と後続検討による表記改訂が混在し、原資料の忠実な転記と編集補正を区別していない。 |
| 17 | `README.md` | 要修正 | `Draft / Research Development` と未完項目の説明は実態に合う。一方、記載する `paper/`、`appendix/`、`assets/`、`development-log/` は存在せず、ファイル名も実名と不一致。版・正本・参考・廃止・重複関係を案内できていない。 |
| 18 | `量子コンピュータの実用化を阻む「誤差問題」の克服_JP.md` | 不合格 | 査読論文、理論提案、企業ブログ、ロードマップを同じ確度で扱い、FTQC移行を過度に断定。書誌誤り（例 `Nature 626, 7997`）、IBM qLDPCの理論提案の実機成果化、Majorana 1等の企業主張の確定扱いがある。外部一次資料による再検証が必要。 |
| 19 | `NRA-IDE_Quantum_Reduction_Final_2026-04-29_1648_JP.md.pdf` | Markdown同版 | 15ページ。正規化一致率約0.900。差は主に数式・表・タイトルページのPDF抽出順で、固有の理論改訂は検出せず。内容判定は同名Markdownを継承。 |
| 20 | `NRA-IDE_error_tracking_summary_JP_20260426_035916.pdf` | Markdown同版 | 6ページ。正規化一致率約0.853。差は主に数式組版、Markdown記号、埋込フォントの漢字コード。固有の改訂本文は検出せず。内容判定は同名Markdownを継承。 |

## 3. 重大な横断不整合

### 3.1 完成度表示が一致しない

- 整形版とJP/EN v1: 4穴は未完了。
- JP/EN v2: 4穴はすべて解決済。
- v2本文自身: Hole 4は部分対処。
- README: 定義順序は整理したが、対象系別設計と数値検証は未完。

この4種類の表示は同時に成立しない。READMEの説明を基準にすれば、Phase 5は「解決案・定義案」であり「解決済」ではない。

### 3.2 `C(r)` の数学的性質を誤認している

対象群は繰り返し

`C(r)=r|r|/(k+|r|)`

を飽和写像と呼ぶ。しかし `|r|` が大きいと `C(r)` は概ね `r` に近づき、絶対値は有界に飽和せず発散する。小残渣では二次的に小さくなるが厳密なゼロまたは沈黙域でもない。

### 3.3 現行v2.1状態機械と不整合

- 旧 `FAIL_CLOSED` 一語へ危険、追跡不能、記述領域外を集約する。
- `R_low/R_high/1.0` や `max` による単一判定が中心。
- `R_warn`、`R_op`、`R_irrev` の排他的因果チャネルがない。
- `WARNING`、`CONFESSION`、`OUT_OF_DESCRIPTION_DOMAIN`、`IRREVERSIBLE_BOUNDARY`、`RUPTURE` がない。
- 境界到達後の不可逆ラッチがない。
- 小残渣時の全面沈黙を正当化し、独立した証言継続原則と衝突する。
- `tau<=0` を記述領域外へ分離せず、小正数による分母置換または未定義のまま扱う。

### 3.4 量子物理と数値計算の未確立部分

- Lindblad方程式を全対象系の `F_IDE` とする適用範囲がない。
- 前進Euler法は一般に密度行列の正値性・完全正値性を保証しない。
- 観測量期待値と共分散の取得にはショット数、測定基底、非可換量の測定コストが必要。
- 誤差二乗和は独立性・無相関性を仮定するが、その仮定がない。
- `tau_system`、`tau_shot`、`tau_coh(T2)`、`tau_gate(D)` を同じ単位へ写す定義がない。
- `tau_C=max(noise,physical,design)` はノイズ増加で閾値を広げ、検出感度を下げる。
- 固定初期参照と遅延参照は別の検出特性を持つが、混同されている。
- 相関最小シミュレーションは物理的密度行列に基づく再現可能な検証になっていない。

### 3.5 証拠と可視化を混同している

HTML群の多くは静的説明器または合成データのアニメーションである。期待する結論を更新式、閾値、描画条件へ埋め込んだ表示は、理論の証明、上界導出、量子実験、数値検証にはならない。各HTMLは `conceptual illustration / toy model / numerical experiment` のいずれかを明示し、後二者には再現条件と検証指標が必要である。

## 4. PDF / Markdown の扱い

- PDF 2件は対応Markdownの閲覧用組版と判定できる。
- 数式はPDFテキスト抽出で順序が崩れるため、機械照合・引用・修正の正本にはMarkdownを使う。
- READMEまたはmanifestで `source: Markdown / derivative: PDF` を明示する。
- PDFだけを別版として更新せず、Markdownから再生成する運用に固定する。

## 5. 修正優先順

1. READMEまたはmanifestで全20件を `current draft / development log / conceptual visualization / invalid experiment / derivative PDF / external reference` に分類する。
2. JP/EN v2の「4穴すべて解決済」を「定義案を提示・対象系別検証待ち」へ訂正し、穴4の部分対処との矛盾を解消する。
3. 全資料の「飽和写像」「飽和応答」「沈黙域」を訂正し、`C(r)` の非有界・漸近線形な性質を明記する。
4. 現行v2.1状態語彙、排他的因果チャネル、不可逆ラッチ、証言継続、`tau<=0` の記述領域外分離へ更新する。
5. `delta/tau/R` と重みの単位を定義し、二重正規化を除去する。測定不確実性と安全許容幅を別変数にする。
6. Lindblad数値計算をCPTP性を保つ方法へ置き換え、対象系、Hamiltonian、ジャンプ演算子、初期状態、seed、時間刻み、測定ショットを固定した再現可能なテストを作る。
7. 二量子ビット相関デモを正値な密度行列から再構築し、個別期待値と共分散の物理的実現可能領域をテストする。
8. READMEの存在しないディレクトリ・誤ファイル名を実構成へ合わせ、評価文01:25と対象文01:41の時系列誤りを訂正する。
9. 一般向け誤差問題レポートを一次資料で再検証し、査読結果、理論提案、企業発表、ロードマップを分離する。

## 6. 最終判定

- 研究開発履歴としての価値: **あり**
- 量子拡張の問題設定・設計候補集としての価値: **あり**
- 数学的上界の証明: **不成立**
- 量子物理シミュレーションとしての再現性: **不成立**
- 現行v2.1正典との状態・境界整合: **不成立**
- 「完成版」「全穴解決済」としての採用: **不可**

このディレクトリは削除対象ではなく、版分類と主張強度を修正して `legacy research / draft quantum extension` として隔離保存するのが妥当である。
