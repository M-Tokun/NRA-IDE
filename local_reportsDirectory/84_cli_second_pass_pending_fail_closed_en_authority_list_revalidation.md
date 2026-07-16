# NRA-IDE 第2次CLI精査 継続Report — Fail-Closed EN 権限列挙再検証（修正待ち）

- 実施日: 2026-07-16 JST
- 対象: `docs/en-US/ai/07_fail_closed_EN.md`
- 現在SHA-256: `C1447673E180BCD5A27F2BDFC3942D2A80DF6A658179BBA6A847EDE46D7F70F9`
- 既存限定再検証Report: `53_cli_second_pass_pending_fail_closed_en_revalidation.md`
- 直前完了Report: `79_cli_second_pass_fail_closed_en_state_latch_revalidation_complete.md`
- 状態: 利用者判断待ち（対象本文は未編集）
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 照合結果

Report 79で修正した正典状態表は現在本文に保存され、`IRREVERSIBLE_TRANSITION`状態と不可逆ラッチは分離されている。

今回の全26文書横断履歴検査で、状態表とは別の旧Effect-Side権限列挙を機械抽出し、本文内の完全列挙と照合した。Report 53および79で完了した他の境界は再編集対象にしない。

## 2. 検出した残存問題

### 問題箇所A

現在の99行目は、旧Effect-Sideからimport、relabel、reconstruct、reuseできない対象を、value、threshold、state、rule、transformation input、update ground、provenanceとしている。

この列挙だけ不可逆ラッチが欠落している。同文書131行目の適合条件は、values、three canonical thresholds、states、irreversible latch、rules、transformation inputs、update grounds、provenanceを完全に分離している。

### 問題箇所B

現在の107行目は、外部監査が旧Effect-Side証言をCause-Sideのvalue、rule、provenanceへ変換できないとしている。

正典閾値、状態、不可逆ラッチ、変換入力、更新根拠が欠落しており、外部監査経路だけに不完全な禁止集合が残る。

## 3. 正典境界との衝突

- 旧Effect-Sideの値、正典閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所を、新旧Cause-Sideへimport、名称変更、再構成、再利用してはならない。
- 外部人間監査は旧経路外の調査であり、どの正典対象にもCause-Side権限を付与しない。
- 状態と不可逆ラッチは別対象として列挙する。

判定: `INCOMPLETE_PROHIBITION_SET / HISTORY_BOUNDARY_CONFLICT`

## 4. 影響

99行目だけを履歴開始条件として実装すると、旧Effect-Sideの不可逆ラッチを新Cause-Sideへ持ち越す余地が残る。107行目だけを外部監査の権限制約として実装すると、閾値、状態、不可逆ラッチ、変換入力、更新根拠をCause-Sideへ転用する余地が残る。

## 5. 推奨修正案

対象本文の2文だけを限定修正する。

1. 99行目の列挙を、value、canonical threshold、state、irreversible latch、rule、transformation input、update ground、provenanceへ完全化する。
2. 107行目の外部監査による変換禁止対象も同じ完全な列挙へ変更する。
3. 状態表、固定Handoff証言、外部人間監査、旧経路終端、新履歴独立開始、omegaの補助証言分類は変更しない。

利用者承認前に`docs/en-US/ai/07_fail_closed_EN.md`は編集しない。
