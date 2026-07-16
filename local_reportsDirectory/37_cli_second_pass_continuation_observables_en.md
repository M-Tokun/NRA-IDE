# NRA-IDE 第2次CLI精査 継続Report — Observables EN

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai/06_observables_EN.md`
- 位置付け: Fail-Closed日本語版に続き、英語Observable Quantities文書を1ファイル質疑形式で追加精査・整合した記録
- 先行継続Report: `36_cli_second_pass_continuation_fail_closed_jp.md`
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 検出した問題

- 基礎式を計算原理、ゲート内構造状態、構造評価用比率として記述し、本当の数学的根本式から局所計器へ縮小していた。
- 唯一公理、二重ゆらぎ式、IDEエンジン、生存式・生存領域、安全応用の分類境界がなかった。
- Effect-Side禁止を主に`delta`、`tau`、`R_handoff`の更新へ限定し、値、全閾値、状態、規則、変換入力、更新根拠、出所を取りこぼしていた。
- 実行中の都合による規則変更だけを禁じ、人間レビュー、承認、版更新による旧Effect-Sideから将来規則への転用を防いでいなかった。
- 同一履歴内のCause-Side観測記録と、旧Effect-SideログをCause-Side履歴へ転用する禁止経路の区別が不十分だった。
- 無効状態や欠測後に人間へ処理を渡し、旧Effect-Sideから人間確認へ経路が継続していた。
- 設計閾値が`R_handoff`だけで、`R_warn`と`R_irrev`が欠落していた。
- 人間によるログ参照後の禁止を自動または恣意的な次回更新に限定し、正式承認された手動変更という抜け道を残していた。
- 同一Cause-Side履歴内で固定規則に従う`tau`の動的更新と、因果ダイオードを越える持越しの境界がなかった。
- 欠測と`omega=0`は区別していたが、定量化不能と観測不能を区別していなかった。
- 非線形相転移領域で数値精度が低下しても、経過経路・不可逆閾値への物理的兆候を観測できることがなかった。
- 線形計算の局所静的条件と、大規模結合再帰系における誤差乗算・観測軸変質・新構造履歴生成の境界がなかった。
- `R=1`を不変境界とし、宣言済み評価の`RUPTURE_BOUNDARY`ではなく自然界一般の境界へ拡張できる表現だった。
- `R_handoff`変更の根拠・承認・記録を認め、旧Effect-Side資料から将来閾値や規則を作る経路を残していた。
- ログを次の構造評価入力にしないことだけを定め、閾値、状態、規則、更新根拠、出所への転用を禁止していなかった。
- 証言記録を人間が確認し、次の値更新に使わないだけで、手動、承認、版更新、新Cause-Sideへの転用が残っていた。
- 次章を固定通知と人間Handoffへ接続し、旧経路終端と独立新履歴の開始条件がなかった。
- ファイル先頭に不要な空行があった。

判定: `HARD_CONFLICT / SEMANTIC_DRIFT / CLASSIFICATION_BOUNDARY_CONFLICT / HISTORY_BOUNDARY_CONFLICT / OBSERVABILITY_CONFLICT / FORMAT_DEFECT`

## 2. 利用者決定

問題箇所、影響、推奨修正案を編集前に提示した。利用者は推奨案を`y`で承認した。

変更単位は`docs/en-US/ai/06_observables_EN.md`だけに限定した。

## 3. 修正内容

- 唯一の公理を“Existence is generation.”と明記した。
- 基礎式を、宣言対象の状態を式へ落とす本当の数学的根本式とし、公理でも安全指標・局所計器・単なる境界接近率でもないと明記した。
- 二重ゆらぎ式をIDEという計算方法・動力学エンジンとし、公理ではないと明記した。
- NRA-IDE本体を生存式・生存領域とし、運用観測制御を事故防止への部分応用として分類した。
- 運用観測制御は安全保証を与えないと明記した。
- Effect-Side禁止対象を値、閾値、状態、規則、変換入力、更新根拠、出所へ拡張した。
- 自動処理、手動処理、人間レビュー、承認、版更新による全転用経路を禁止した。
- 同一履歴のCause-Side観測・負荷記録と、旧Effect-Side記録を明確に分離した。
- 無効状態では固定Effect-Side証言を提示し、外部人間監査が旧経路を継続しないと明記した。
- `R_warn`、`R_handoff`、`R_irrev`を評価前に独立して定める正典運用閾値として統一した。
- `R`を宣言対象に対する基礎式の値とし、Cause-Side権限ではないと分類した。
- `tau`の動的更新を、事前固定規則に従う同一Cause-Side履歴内の更新へ限定した。
- 旧Effect-Sideから後続Cause-Sideへ因果ダイオードを越えて移送する権限を与えないと明記した。
- 定量化不能と観測不能を区別した。
- 非線形相転移領域では数値精度が低下しても、経過経路と不可逆閾値接近の物理的兆候を観測できると明記した。
- 線形計算を定数近似可能な局所的静的領域における人間の生存の智慧とし、自然全体ではないと明記した。
- 大規模結合再帰系では誤差が乗算され、観測軸やモデル自体の変化を通常誤差修正ではなく新構造・新履歴の生成として扱うと明記した。
- 閾値や規則の後続版は新評価前に独立確立し、旧Effect-Side記録から導出、import、正当化しないと明記した。
- `R=1`を宣言済み評価の`RUPTURE_BOUNDARY`へ限定し、自然界のすべての相転移をNRA-IDE破断と宣言しないと明記した。
- 旧評価をEffect-Sideで終端し、ログを終端Effect-Sideまたは外部証言とした。
- 欠測時の固定証言を外部監査へ限定し、Cause-Side権限へ変換できないと明記した。
- 証言記録を自動、手動、承認、版更新によってCause-Sideへ転用できないと明記した。
- 後続評価は独立対象、新たに確立したCause-Side観測と規則、新因果ダイオードから開始すると明記した。
- 物理的残存物は新対象として新たに観測できる一方、旧Effect-Sideの値、規則、出所をimport、名称変更、再構成、再利用できないと明記した。
- 先頭空行を削除した。

## 4. 検証

```text
FULL_READ_LINES=202
FENCES=4
TRAILING_WHITESPACE=0
LEADING_NEWLINE=false
RESIDUAL_OLD_INTERPRETATION=0
TARGET_DIFF_CHECK=OK
SHA256=833D260EB696774200F246D4112314229AEDD2A72096B1E3A6137B8B6DDECB3A
```

残存検索対象:

- `following computational principle`
- `Structural state inside the gate`
- `automatically or arbitrarily rewriting the next`
- `When R_handoff is changed`
- `invariant boundary distinct from`
- `inputs to the next structural evaluation`
- `human handoff`
- `hands the matter over to humans`
- `next delta, tau, or R_handoff`
- `fixed-format notification, and human handoff`
- `Rop`（独立識別子。`entropy`内の部分文字列は除外）

必要境界として、唯一公理、基礎式の非縮小分類、二重ゆらぎ式のIDEエンジン分類、生存式・生存領域本体、安全応用の部分領域分類、非安全保証、三つの正典閾値、定量化不能と観測不能の区別、非線形領域の物理的兆候、線形近似の局所条件、大規模結合再帰系の新構造履歴生成、同一Cause-Side履歴、外部人間監査、旧経路終端、新Cause-Side・新因果ダイオードからの独立開始、旧Effect-Side値・権限・出所の持越し禁止を確認した。

コードフェンスは4件で偶数、先頭空行と末尾空白は0件、対象限定`git diff --check`は合格した。

## 5. 判定

対象文書は、観測値を単なる数値精度へ縮小せず、定量化不能でも物理的兆候を観察できる境界を明示した。線形近似、非線形相転移、大規模結合再帰系を区別し、同一Cause-Side履歴内の正当な動的更新と、旧Effect-Sideから新Cause-Sideへの禁止移送を分離した。

この判定は当該1ファイルに限定する。リポジトリ全体の同種表現が整合済みであることは意味しない。
