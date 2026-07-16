# NRA-IDE 第2次CLI精査 継続Report — Sandwich Architecture EN ラッチ・権限列挙再検証（修正待ち）

- 実施日: 2026-07-16 JST
- 対象: `docs/en-US/ai/04_rna_sandwich_architecture_EN.md`
- 現在SHA-256: `8371EA49D1D83849BFD06673771053D636C61A058DE8DB556BB3005DCB56FCED`
- 既存個別Report: `42_cli_second_pass_pending_sandwich_architecture_en.md`
- 状態: 利用者判断待ち（対象本文は未編集）
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 照合結果

現在SHA-256はReport 42の修正後SHA-256と一致する。同Reportで確定した三層応用の部分分類、完全一方向の因果ダイオード、三閾値、七状態、不可逆ラッチ解除禁止、外部人間監査、旧経路終端、独立新履歴は保存されている。

今回、全26文書の履歴権限列挙を横断抽出し、同文書29行目、41行目、61行目の完全列挙と他の権限列挙を照合した。Report 42の完了範囲全体を再編集対象にしない。

## 2. 検出した残存問題

### 問題箇所A

80行目のPre-NRA除外対象は、Cause-Side values、thresholds、states、`latch state`、rules、transformation inputs、update grounds、provenanceとしている。

`latch state`が正典状態と不可逆ラッチを混同し、thresholdsもcanonical thresholdsと明示されていない。

### 問題箇所B

151行目の旧Effect-Side非再利用対象は、values、thresholds、states、rules、transformation inputs、grounds、provenanceとしている。

不可逆ラッチが欠落し、thresholdsとgroundsもcanonical thresholds、update groundsとして明示されていない。

### 問題箇所C

164行目のLLM権限境界は、values、canonical thresholds、states、`latch state`、rules、transformation inputs、update grounds、provenance、logsとしている。

ここでも`latch state`が正典状態と不可逆ラッチを混同している。

### 問題箇所D

191行目の外部監査によるCause-Side確立禁止対象は、rules、values、thresholds、provenanceだけである。

canonical thresholds、states、irreversible latch、transformation inputs、update groundsが完全な正典対象として列挙されていない。

## 3. 正典境界との衝突

- 正典状態と不可逆ラッチは別対象である。
- 不可逆ラッチは`latch state`という追加状態または状態の別名ではない。
- Effect-Sideから確立・変更・再利用できない対象は、values、canonical thresholds、states、irreversible latch、rules、transformation inputs、update grounds、provenanceである。
- 外部人間監査も同じCause-Side権限境界に従う。

判定: `TERMINOLOGY_CONFLICT / STATE_MODEL_CONFLICT / INCOMPLETE_PROHIBITION_SET`

## 4. 影響

80行目または164行目だけを実装すると、不可逆ラッチを状態へ統合する余地が残る。151行目だけを新履歴境界として読む場合、旧Effect-Sideの不可逆ラッチを新Cause-Sideへ持ち越す余地が残る。191行目だけを外部監査の権限契約として読む場合、状態、ラッチ、変換入力、更新根拠を後続Cause-Sideへ転用する余地が残る。

## 5. 推奨修正案

対象本文の4文だけを限定修正する。

1. 80行目の`thresholds, states, latch state`を`canonical thresholds, states, the irreversible latch`へ変更する。
2. 151行目の列挙を、values、canonical thresholds、states、the irreversible latch、rules、transformation inputs、update grounds、provenanceへ完全化する。
3. 164行目の`latch state`を`the irreversible latch`へ変更する。
4. 191行目の外部監査による確立禁止対象を、values、canonical thresholds、states、the irreversible latch、rules、transformation inputs、update grounds、provenanceへ完全化する。
5. Report 42で整合済みの三層構造、状態機械、履歴構造、Markdownは変更しない。

利用者承認前に`docs/en-US/ai/04_rna_sandwich_architecture_EN.md`は編集しない。
