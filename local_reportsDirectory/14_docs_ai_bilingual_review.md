# docs 日英AI解説 精査報告

- 検査日: 2026-07-14 JST
- 対象: `docs/ja-JP/ai` 13件、`docs/en-US/ai` 13件
- 総合判定: **要全面同期（2026-06中間仕様としては改善あり）**

## 1. 日英対応

00～12の章構成、主要式、状態名、保証範囲は概ね対応する。重大な翻訳由来の意味反転は確認しなかった。問題は両言語が共通して現行v2.1より古い状態仕様を採用することである。

## 2. 章別判定

| 章 | 判定 | 主な指摘 |
|---:|---|---|
| 00 Overview | 要修正 | Cause/Effect分離は整合。`R_warn`なし、旧状態体系を全章の基礎にする。 |
| 01 Paradigm Shift | 要修正 | 最適化と安全指標の区別は改善。三層が最小十分との保証条件は形式化されない。 |
| 02 Optimization | 要修正 | `S=1/(tau-delta)`の代数は条件付きで正しいが、R=1を物理的相転移と一般化。SILENCE語彙が旧式。 |
| 03 Causal Diode | 概ね有用・要同期 | Effect-Sideによるdelta/tau更新禁止は整合。距離・ログ等の分類を対象別にする必要がある。 |
| 04 Sandwich | 要修正 | 定型通知継続は改善。現行5状態、三境界、CONFESSION、領域外が不足。 |
| 05 Coherence Gate | 不合格 | NIRVANA/ELASTIC/CRITICAL/SILENCE/HALT、0.4/0.7固定値。`R_irrev`を任意補助へ格下げ。 |
| 06 Observables | 概ね有用・要同期 | provenance、単位、更新経路の分離は有用。無効状態の正規分類と状態遷移が不足。 |
| 07 Fail-Closed | 要修正 | 通常生成停止と定型通知を分ける改善あり。`R_op`一段とR=1終端だけで現行三境界を表現しない。 |
| 08 Discard Logs | 要修正 | ログ非還流と監査を分離。整数化残差`entropy_export`を一般原理化できず、保存量・量子化誤差が未定義。 |
| 09 Risks | 概ね有用・要同期 | 誤用と責任分界は慎重。無効値をOUT_OF_DESCRIPTION_DOMAIN等へ分類しない。 |
| 10 Benefits/Limits | 概ね有用・要同期 | 保証しない範囲を明示する点は良い。保証表現には適合試験・脅威モデルが必要。 |
| 11 Domain Tuning | 不合格 | 必須の`R_warn`を欠き、`R_irrev`を任意とするためv2.1と直接矛盾。 |
| 12 Glossary | 不合格 | 旧状態・固定閾値を規範用語集として固定し、現行状態語彙を欠く。 |

## 3. 主要不整合

1. 現行必須順序 `R_warn < R_op < R_irrev < 1` がない。
2. `R_irrev`を任意補助標識とし、不可逆ラッチを定義しない。
3. WARNING、CONFESSION、OUT_OF_DESCRIPTION_DOMAIN、IRREVERSIBLE_BOUNDARY、RUPTUREを持たない。
4. tau非正値、NaN、欠測、単位不一致を「invalid-state handling」へ一括し、因果別状態を失う。
5. R=1をあらゆる対象の物理的「相転移」と呼ぶ。Rの定義上の境界と実対象の相転移は別に検証が必要。
6. `entropy_export`は一実装の丸め残差で、全ドメイン共通の状態遷移原理ではない。
7. `docs/en-US/ai/08_discard_logs_EN.md` が存在しない `../figures/08_Escapement_ContactPoint_JP.html` を参照する。

## 4. 最終判定

全面沈黙を避け、定型構造証言を残す方向への改善は評価できる。しかし現行正典より前の中間仕様であり、公開用の規範解説としては不合格。英日を同時にv2.1へ移行する必要がある。
