# NRA-IDE 第2次CLI精査 継続Report — Causal Diode EN 再検証（修正待ち）

- 実施日: 2026-07-16 JST
- 対象: `docs/en-US/ai/03_causal_diode_EN.md`
- 現在SHA-256: `BD15D3DC95CFD770AE71B3E537CCF58FD6797F2D57A13BDEBE66F24CF46084FE`
- 位置付け: Report 48以後の横断残存検査で検出した表現を、Report 19の完了状態と照合した再検証記録
- 状態: 利用者判断待ち（対象本文は未編集）
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 照合結果

Report 19で確定した次の主要境界は、現在の対象ファイルにも保存されている。

- 因果ダイオードは`Cause-Side → Effect-Side`だけの一方向経路である。
- 古い経路はOld Effect-Sideで終端する。
- Old Effect-Sideから新旧いずれのCause-Sideにも矢印はない。
- 新履歴は独立した新対象、新しいCause-Side観測・履歴・事前固定規則、新しい因果ダイオードから開始する。
- 旧Effect-Side値のimport、relabel、reconstruction、およびCause-Side測定・構造変数・provenanceへの転換を禁止している。

見出し15件、コードフェンス12件で、コードフェンス数は偶数だった。

## 2. 検出した残存問題

### 問題箇所A

現在の49行目は、Effect-Side成果物が書き換える権限を持たない対象を、`δ`, `τ`, `R`, thresholds, `irreversible state`として列挙している。

`irreversible state`は、正典の`state`と`irreversible latch`を一語に結合しており、両者の区別を曖昧にする。また、規則、変換入力、更新根拠、出所が禁止対象の列挙から欠落している。

### 問題箇所B

現在の165行目は、LLM出力が`τ`を拡大し、`δ`を縮小し、`irreversible state`を解除できないと記述している。

ここでも`state`と`irreversible latch`が分離されていない。さらに、禁止対象が`δ`, `τ`と不可逆状態だけに見えるため、`R`、正典閾値、状態、規則、変換入力、更新根拠、出所に対するEffect-Sideからの書換え禁止が要約部で不完全になる。

## 3. 正典境界との衝突

- `state`と`irreversible latch`は別の正典対象として保持する必要がある。
- Effect-Sideの値、判断、成果物は、`R`, `δ`, `τ`, 正典閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所を書き換える権限を持たない。
- これらを旧履歴内で更新することも、新履歴へimport、名称変更、再構成、再利用することもできない。

判定: `SEMANTIC_DRIFT / INCOMPLETE_PROHIBITION_SET`

## 4. 影響

現在の主要な一方向境界と履歴終端は維持されているが、禁止対象の列挙が不完全なため、Effect-Sideから規則・更新根拠・出所などを変更できる余地、または`state`と`irreversible latch`を同一対象として扱う余地が残る。

## 5. 推奨修正案

対象本文だけを限定編集する。

1. 49行目の`irreversible state`を`canonical state or irreversible latch`へ分離し、禁止対象へrules, transformation inputs, update grounds, provenanceを追加する。
2. 165行目を、LLM出力が`R`, `δ`, `τ`, canonical thresholds, states, irreversible latch, rules, transformation inputs, update grounds, provenanceのいずれも書き換えられない要約へ置き換える。
3. 既に整合済みの一方向ダイオード、旧経路終端、新履歴独立開始の記述は変更しない。

利用者承認前に`docs/en-US/ai/03_causal_diode_EN.md`は編集しない。
