# NRA-IDE 第2次CLI精査 継続Report — AI章横断整合検証

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai`および`docs/ja-JP/ai`のMarkdown全26ファイル
- 位置付け: 個別精査一巡後の横断整合・終了判定
- 先行継続Report: `47_cli_second_pass_pending_overview_jp.md`
- 対象本文の編集: 未実施
- RAW監査報告01～17: 変更なし、manifest記録と全17件一致
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 対象・Report・Git実体の照合

- 英語AI章は00～12の13件、日本語AI章も00～12の13件で、章番号対応は一致した。
- 26件すべてに現在の追跡済み差分が存在する。
- 継続Report 19～47は29件存在し、AI章26件のほか因果ダイオード日英HTML 2件と、ハング後に再検証した`06_observables_JP.md`の追加Report 1件を含む。
- Report 20～47で記録された最終対象ハッシュは現在実体と一致した。Report 19は対象SHA-256自体を記録していないため、ハッシュ不一致ではなく比較対象なしである。現在の`03_causal_diode_EN.md`は対象限定`git diff --check`に合格した。
- RAW報告01～17は`audit_manifest.json`記録のSHA-256と17件すべて一致し、欠落・不一致は0件だった。
- stage済みファイルは0件である。
- 追跡済みPDF `nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf`の既存削除は復元せず保持されている。

## 2. 構造・リンク検証

```text
EN_COUNT=13
JP_COUNT=13
CHAPTER_NUMBER_PARITY=PASS
ODD_FENCE_FILES=0
DUPLICATE_HEADING_COUNT=0
LOCAL_LINKS_CHECKED=24
MISSING_LOCAL_LINKS=0
ALL_AI_DIFF_CHECK=OK
```

Markdownフェンス、重複見出し、ローカルリンク、対象全体の`git diff --check`では問題を検出しなかった。

## 3. 横断検索で検出した旧境界候補

終了判定前の旧表現検索で、外部人間監査へ置換されていない可能性がある`human handoff`、`delegate judgment to humans`、`人間委譲`、`人間への委譲`、文脈依存の`委譲点`、全体必須条件として読める`three-layer separation`／`三層分離`が複数ファイルに残った。

候補が存在する英語ファイル:

- `02_limits_of_ai_optimization_EN.md`
- `08_discard_logs_EN.md`
- `09_risks_and_misuse_EN.md`
- `10_benefits_and_limitations_EN.md`
- `11_domain_tuning_EN.md`
- `12_glossary_EN.md`

候補が存在する日本語ファイル:

- `02_limits_of_ai_optimization_JP.md`
- `05_coherence_gate_JP.md`
- `07_fail_closed_JP.md`
- `08_discard_logs_JP.md`
- `09_risks_and_misuse_JP.md`
- `10_benefits_and_limitations_JP.md`
- `11_domain_tuning_JP.md`
- `12_glossary_JP.md`

この一覧は機械検索による候補であり、語が現れただけで全件を衝突と確定しない。一方、`fixed-schema human handoff`、`delegate judgment to humans`、`人間へ判断を渡す`など、固定Effect-Side証言の外部人間監査ではなく旧経路内の引渡しとして読める表現が実在するため、横断終了を宣言できない。

## 4. 判定と再開位置

個別Reportの存在とMarkdown形式だけでは横断整合を確定できない。古い書式のReport 19～38で合格したファイルにも、その後確定・強化された履歴境界に照らすと残存候補がある。

完了済み作業を推測で再実行せず、残存候補の実文だけを章番号順・1ファイル質疑形式で限定再検証する。

次の直接対象は、残存候補のうち最初の`docs/en-US/ai/02_limits_of_ai_optimization_EN.md`とする。現在本文とReport 23を照合し、新たな問題が確定した場合は勝手に編集せず、問題箇所、正典衝突、影響、推奨修正案を提示して利用者決定を待つ。
