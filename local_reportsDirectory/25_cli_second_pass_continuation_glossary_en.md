# NRA-IDE 第2次CLI精査 継続Report — Glossary EN

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai/12_glossary_EN.md`
- 位置付け: AI最適化限界文書に続き、英語Glossaryを1ファイル質疑形式で追加精査・整合した記録
- 先行継続Report: `24_cli_second_pass_continuation_ai_optimization_jp.md`
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 検出した問題

- Primary Formulaの`R`を`S`等と同じ派生量・状態指標に分類し、対象状態を式へ落とす数学的根本式を局所計器へ縮小していた。
- `R_irrev`を任意採用のように扱い、3つの正典閾値を一貫して列挙していなかった。
- Effect-Side更新禁止を自動更新に限定し、人間レビュー、承認、版更新を介する逆接続の余地を残していた。
- Causal Diode、`Pi-inverse`、Cause-Side、Effect-Sideの各定義に、旧経路終端、新履歴の独立開始、新ダイオード、旧Effect-Sideの持越し禁止がなかった。
- Discard Logの人間監査と設計変更が、旧Effect-Sideを将来のCause-Side権威へ変換する経路になり得た。
- 公理を複数形とし、Primary FormulaとSecondary / Dual-Fluctuation Formulaの分類境界を明示していなかった。
- `delta`と`tau`の用語が、履歴を持つ蓄積偏差と吸収厚さから逸脱していた。
- `R=1`を自然界一般の不変相転移境界へ一般化し、宣言対象に対するNRA-IDEの`RUPTURE_BOUNDARY`との境界を失っていた。
- LLM権限境界とCause-Side利用条件が`R_handoff`だけを列挙し、`R_warn`と`R_irrev`を取りこぼしていた。

判定: `HARD_CONFLICT / SEMANTIC_DRIFT / CLASSIFICATION_BOUNDARY_CONFLICT`

## 2. 利用者決定

問題箇所、影響、推奨修正案を編集前に提示した。利用者は推奨案を`y`で承認した。

変更単位は`docs/en-US/ai/12_glossary_EN.md`だけに限定した。

## 3. 修正内容

- `R=delta/tau`を、宣言対象の構造状態を正典の数学的関係へ落とすPrimary Formulaとして分類した。
- Primary Formulaは安全指標、局所計器、単なる境界接近率ではなく、派生式・補助式・補完式にも分類されないと明記した。
- `S`、`M_R`、`M_tau`だけを派生・補完量として分離した。
- `R_warn < R_handoff < R_irrev < 1`を正典閾値順序とし、設計値、LLM権限境界、Cause-Side条件、Domain Tuningへ3閾値を反映した。
- `delta`を履歴を持つ蓄積偏差、`tau`を吸収厚さとして定義した。
- `R=1`を宣言済みNRA-IDE評価の`RUPTURE_BOUNDARY`とし、自然界のすべての相転移を同一視しないと明記した。
- 公理を単数のNomological Ring Axiomとし、「Existence is generation.」以外に第二公理以降は存在しないと明記した。
- Primary FormulaとSecondary / Dual-Fluctuation Formulaを、唯一の公理とは別の2つの正典IDE計算系として分類した。
- IDEをNRA-IDEの計算方法・動力学エンジンとし、公理、安全保証、Integrated Development Environmentではないと明記した。
- Causal DiodeをCause-SideからEffect-Sideへの完全な一方向とし、旧経路はEffect-Sideで終端すると明記した。
- 後続履歴は独立して宣言した対象、固有のCause-Side観測・規則、新しいCausal Diodeから始まると明記した。
- 旧Effect-Sideの情報、推論、成果物、判断、権威を、新旧いずれのCause-Sideにも戻さないと明記した。
- `Pi-inverse`に自動、手動、人間レビュー、承認、版更新の全逆接続を含めた。
- 事故後調査と将来規則設計を終端済み旧経路の外部活動とし、旧Effect-Side値のimport、名称変更、再構成、再利用を禁止した。
- 物理的残留物は独立した新対象として新規観測できる一方、旧Effect-Side値はCause-Side変換入力にならないと分離した。
- Effect-Sideを終端側とし、その記録は新旧いずれのCause-Sideも更新、seed、変換しないと明記した。
- Discard Logは外部監査で読めても、手動・自動を問わずCause-Sideへ再導入されないと明記した。
- Design changeを将来の独立した対象・Cause-Side履歴のための外部活動とし、旧ダイオードの継続ではないと明記した。
- 状態名と最小整合表を、`PERMIT`から`RUPTURE_BOUNDARY`までの正典状態・出力経路へ統一した。

## 4. 検証

```text
FULL_READ_LINES=259
FENCES=2
TRAILING_WHITESPACE=0
RESIDUAL_OLD_INTERPRETATION=0
TARGET_DIFF_CHECK=OK
SHA256=97FB0715E83972F40E13F039AD5B3AB5CD531389BE6933AD4978B1753DD7E47E
```

残存検索対象:

- `Four Layers`
- `State indicators calculated`
- `R_irrev when required`
- `Automatic updates`
- `automatically reintroduced`
- `Nomological Ring Axioms`
- `design axioms`
- `invariant phase-transition and terminal boundary`
- `structural tolerance or thickness`
- `deviation or fluctuation`
- `R_op`

`must not automatically`は、制約名`C`だけから`delta`または`tau`の変化を自動決定してはならないというCause-Side定義内の正当な禁止表現だけが残った。Effect-Side逆流を自動経路だけへ限定する旧解釈ではない。

必要境界として、唯一の公理、Primary Formulaの非縮小分類、Dual-Fluctuation FormulaのIDE計算系分類、完全一方向のCausal Diode、旧Effect-Sideでの終端、新Cause-Side・新Causal Diodeからの独立開始、旧Effect-Side値の持越し禁止、3つの正典閾値が存在することを確認した。

コードフェンスは2件で偶数、対象限定`git diff --check`は合格した。

## 5. 判定

対象Glossaryは、公理、Primary Formula、IDEエンジン、正典状態、完全一方向のCausal Diodeを別分類として保持し、物理的残留物の新規観測可能性を認めつつ、旧Effect-Sideの構造権威・状態・値を次の歯へ持ち越さない境界へ整合した。

この判定は当該1ファイルに限定する。リポジトリ全体の同種表現が整合済みであることは意味しない。
