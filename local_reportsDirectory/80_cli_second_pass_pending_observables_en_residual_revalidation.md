# NRA-IDE 第2次CLI精査 継続Report — Observables EN 残存再検証（修正待ち）

- 実施日: 2026-07-16 JST
- 対象: `docs/en-US/ai/06_observables_EN.md`
- 現在SHA-256: `833D260EB696774200F246D4112314229AEDD2A72096B1E3A6137B8B6DDECB3A`
- 既存個別Report: `37_cli_second_pass_continuation_observables_en.md`
- 状態: 利用者判断待ち（対象本文は未編集）
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 照合結果

現在SHA-256はReport 37の完了時SHA-256と一致する。同Reportで確定した次の境界は保存されている。

- 基礎式は宣言対象の状態を式へ落とす本当の数学的根本式であり、安全指標、局所計器、単なる境界接近率ではない。
- 定量化不能と観測不能を区別し、非線形相転移領域の物理的兆候を観測可能としている。
- 線形計算を定数近似可能な局所静的領域へ限定し、大規模・結合・再帰系の誤差乗算と新構造履歴生成を区別している。
- 三つの正典閾値、同一Cause-Side履歴内の更新、Effect-Sideからの逆流禁止を記述している。
- 旧経路はEffect-Sideで終端し、後続評価は独立対象、新Cause-Side、新規則、新因果ダイオードから開始する。

## 2. 検出した残存問題

### 問題箇所A

現在の184行目は、終端証言を次のように記述している。

```text
external human audit of the grounds for stopping or handoff
```

`handoff`が、正典状態`HANDOFF_REQUIRED`における固定Handoff証言ではなく、人間への判断移送または旧経路内の次工程として読める。Fail-Closed英語版で確定した`grounds for suppression and fixed Handoff testimony`とも不一致である。

### 問題箇所B

現在の200行目は、固定Effect-Side証言の提示先を`external human review`としている。文書内の他箇所および確定済みFail-Closed境界は`external human audit`で統一されている。

同じ文の旧Effect-Side非再利用対象は`values, rules, and provenance`だけであり、正典閾値、状態、不可逆ラッチ、変換入力、更新根拠が欠落している。

## 3. 正典境界との衝突

- 固定Effect-Side証言は外部人間監査へ提示する。旧経路内のreview、approval、handoff工程へ継続しない。
- `HANDOFF_REQUIRED`で提示するものは固定Handoff証言であり、人間への判断移送ではない。
- 旧Effect-Sideの値、正典閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所を、新旧Cause-Sideへimport、名称変更、再構成、再利用してはならない。

判定: `TERMINOLOGY_CONFLICT / INCOMPLETE_PROHIBITION_SET / HISTORY_BOUNDARY_CONFLICT`

## 4. 影響

章終端だけを次章への実装契約として読む場合、外部監査が旧経路内のレビューまたは人間への判断移送として実装される余地がある。また、旧Effect-Sideの閾値、状態、不可逆ラッチ、変換入力、更新根拠を新Cause-Sideへ転用できる余地が残る。

## 5. 推奨修正案

対象本文の2段落だけを限定修正する。

1. 184行目の`grounds for stopping or handoff`を`grounds for suppression and fixed Handoff testimony`へ変更する。
2. 200行目の`external human review`を`external human audit`へ変更する。
3. 200行目の旧Effect-Side非再利用対象を、values, canonical thresholds, states, irreversible latch, rules, transformation inputs, update grounds, provenanceへ完全化する。
4. 既に整合済みの観測・定量化境界、線形計算、三閾値、旧経路終端、新履歴独立開始は変更しない。

利用者承認前に`docs/en-US/ai/06_observables_EN.md`は編集しない。
