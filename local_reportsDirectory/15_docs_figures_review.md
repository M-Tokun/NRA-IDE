# docs 可視化・画像精査報告

- 検査日: 2026-07-14 JST
- 対象: 共通figures 11件、ja-JP/figures 13件、en-US/figures 13件、logo_bak 6件
- 総合判定: **不合格（ブランド資産を除く）**

## 1. 共通figures

- M1: NRAをRop=0.97で停止、線形系を1.06で必ずcrashさせる。比較結果を実装へ埋め込んだ演示で、優位性の実験ではない。
- M2: `S=1/(tau-delta)`の視覚化は可能だが、0.70/0.85/0.97を無根拠に固定し、R=1を一般的物理破断とする。
- M3: 構造層と生命科学の同型性を図示だけで主張し、検証しない。
- M4: fixed tauと固定シナリオによる告白表示で、現行CONFESSION状態・領域外条件を実装しない。
- M5: Fail-Closedを「設計の完成形」、R=1を自己委譲境界と一般化する。
- 統合HTMLは上記問題を複製する。
- `NRA-IDE_architecture.svg`は単一Fail-Closed/DiscardVaultモデルで現行状態を欠く。

## 2. 言語別figures

- `DOMAIN_TUNING.png`: 0.40/0.99/1.00旧区分、Silence、DOMAIN_C重複、崩れた添字、未定義alpha等を含む。
- `fig1_approach_comparison.png`: 「中心なし→距離なし→攻撃不能」は誤り。境界自体が最適化・攻撃対象になり得る。
- `fig2_causal_diode.png`: 距離、座標、ログを一律Effect-Sideへ置き、対象別因果分類を許さない。
- `fig3_coherence_gate.png`: 旧0/40/70/100%、NIRVANA/ELASTIC/CRITICAL/ABSTAIN。
- `fig4_circle_vs_spiral.png`: 大判画像としてデコーダ表示に失敗。理論上も円環を一律「誤り」とする根拠がない。
- Sandwich画像: `RNA INPUT/OUTPUT`表記、距離一律排除、旧三層。日本語版に文字崩れ・言語混在。
- `01_Code_Generated_Image.jpg`: 離散側も原点誤差が0～20で振動し、誤差ゼロを証明しない。生成条件なし。
- `RNA-BI.jpg`: 調和振動の粗い離散化比較で、NRA固有性・保存性を証明しない。式が切れている。
- `han_rasen_202512.gif`: v1.3旧散逸仮説。現行仕様図ではない。
- ダムHTML: 経験的tau劣化と旧状態を使う概念デモ。実ダム評価・予測には使用不可。
- 因果ダイオード、脱進機HTML: 期待する遮断・排出を描画した説明器で、保証試験ではない。
- `figures_Directory.txt`: 概念図を`Proves`と記載し、図示と証明を混同する。

## 3. リソース問題

- 英語08章から日本語脱進機HTMLへのローカル参照が切れている。
- 言語別HTML 6件がGoogle Fontsへ依存し、完全オフラインでは同一表示にならない。
- EN/JPで同一バイナリの画像が多く、言語別配置の意味が不明なものがある。

## 4. logo_bak

6件はいずれも同一ブランドのサイズ・構図違いで、正式英語名称は正しい。理論主張を含まないため問題なし。バックアップ資産としての位置も明確。

## 5. 最終判定

可視化群は概念説明と実験証拠を分離し、全図へ`legacy / conceptual illustration / not validated`等の表示が必要。現行v2.1図は別に再生成すべきである。
