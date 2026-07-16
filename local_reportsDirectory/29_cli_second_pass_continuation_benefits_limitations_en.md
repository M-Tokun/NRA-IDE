# NRA-IDE 第2次CLI精査 継続Report — Benefits and Limitations EN

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai/10_benefits_and_limitations_EN.md`
- 位置付け: Domain Tuning日英版に続き、英語Benefits and Limitations文書を1ファイル質疑形式で追加精査・整合した記録
- 先行継続Report: `28_cli_second_pass_continuation_domain_tuning_jp.md`
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 検出した問題

- NRA-IDEを通常生成抑止・人間委譲の枠組みへ縮小し、本体である生存式・生存領域とIDE計算方法・動力学エンジンの位置付けを失っていた。
- guaranteeという語が広く残り、条件付き実装適合動作と安全・正しさの保証との境界が曖昧だった。
- Effect-Side禁止を自動更新に限定し、手動、人間レビュー、承認、版更新を介する逆接続を残していた。
- Discard Logを次の構造計算へ自動的に戻さないとだけ定め、人間参照後の将来規則・新Cause-Sideへの転用を禁止していなかった。
- Effect-Side更新禁止の列挙が`delta`、`tau`、`R_handoff`だけで、`R_warn`、`R_irrev`、不可逆状態、規則、出所を取りこぼしていた。
- 設計変更に、旧履歴終端、新対象・新Cause-Side・新Causal Diodeからの独立開始がなかった。
- `R=1`を自然界一般の不変相転移境界へ一般化していた。
- `RUPTURE_BOUNDARY`とFail-Closed運用動作を同じ状態分類として扱う余地があった。
- 元状態へ戻る保証がないという説明だけで、旧履歴終端、物理的残留物の新規観測、新履歴生成を説明していなかった。
- 適合前提が`R_handoff`中心で、3つの正典閾値を扱っていなかった。

判定: `HARD_CONFLICT / SEMANTIC_DRIFT / CLASSIFICATION_BOUNDARY_CONFLICT / HISTORY_BOUNDARY_CONFLICT`

## 2. 利用者決定

問題箇所、影響、推奨修正案を編集前に提示した。利用者は推奨案を`y`で承認した。

変更単位は`docs/en-US/ai/10_benefits_and_limitations_EN.md`だけに限定した。

## 3. 修正内容

- NRA-IDEの本体を単数のsurvival equationとsurvival domainとし、NRA-IDE計算方法・動力学エンジンを通じて実装すると明記した。
- safety domainを、生存領域を事故防止運用制御へ適用した部分領域として分離した。
- 通常生成抑止・人間委譲は安全応用の動作であり、NRA-IDE本体を出力ゲートへ縮小しないと明記した。
- guaranteeを、明示条件下のoperational applicationに対するconditional conformance propertyへ限定し、対象系の安全保証ではないと明記した。
- 適合前提へ`R_warn < R_handoff < R_irrev < 1`の正典順序を追加した。
- Effect-Sideから`delta`、`tau`、正典閾値、不可逆状態、構造規則、出所への、自動、手動、人間レビュー、承認、版更新の全逆接続を禁止した。
- Effect-Sideから旧Cause-Sideまたは新Cause-Sideへ、情報、推論、成果物、判断、権威を戻さないと明記した。
- Discard LogをEffect-Sideまたは外部記録とし、人間監査を終端済み経路の外部へ限定した。
- Discard Logを新旧Cause-Sideの入力、更新根拠、規則根拠、出所へ変換しないと明記した。
- `RUPTURE_BOUNDARY`を正規状態、Fail-Closedを運用上の強制動作として分離した。
- 設計可能な規則を、将来の独立して宣言した対象・Cause-Side履歴に対する外部活動へ限定した。
- 旧経路はEffect-Sideで終端し、旧Effect-Side値のimport、名称変更、再構成、再利用を禁止した。
- `R=1`を宣言済み評価の`RUPTURE_BOUNDARY`とし、自然界のすべての相転移をNRA-IDE破断と宣言しないと明記した。
- 物理的残留物、周辺構造、後続世代は新対象として固有のCause-Side・新Causal Diodeから新規観測できるが、旧Effect-Side値・構造権威を持ち越さないと明記した。
- 結論で、条件付き適合動作は生存式・生存領域を置き換えず、安全保証を構成しないと再確認した。

## 4. 検証

```text
FULL_READ_LINES=168
FENCES=2
TRAILING_WHITESPACE=0
RESIDUAL_OLD_INTERPRETATION=0
SURVIVAL_EQUATIONS_PLURAL=0
SURVIVAL_EQUATION_SINGULAR=2
TARGET_DIFF_CHECK=OK
SHA256=A79B951C7F5AF2F0946594683F5A1FFC475F327F0F522325207579F53BAEF2A8
```

残存検索対象:

- `framework that structurally determines when ordinary generation`
- `NRA-IDE guarantees do not hold`
- `Prerequisites for Guarantees to Hold`
- `grounds for automatically updating`
- `not automatically returned to the next structural computation`
- `invariant phase-transition boundary`
- `is the phase-transition boundary`
- `changes to tau or R_handoff must be treated as design changes`
- `FAIL-CLOSED caused`
- `Grounds for setting tau and R_handoff`
- `R_op`
- `survival equations`

必要境界として、単数の生存式、生存領域、安全応用の部分領域分類、条件付き実装適合、非安全保証、完全一方向のEffect-Side権限境界、旧Effect-Side終端、新Cause-Side・新Causal Diodeからの独立開始、物理的残留物の新規観測、旧Effect-Side値・構造権威の持越し禁止が存在することを確認した。

コードフェンスは2件で偶数、対象限定`git diff --check`は合格した。

## 5. 判定

対象文書は、NRA-IDE本体を生存式・生存領域として保持し、安全域の運用制御をその部分応用として分離した。条件付き適合動作を安全保証へ拡張せず、旧Effect-Sideの歯を次の規則・新Cause-Sideへ持ち越さない境界へ整合した。

この判定は当該1ファイルに限定する。リポジトリ全体の同種表現が整合済みであることは意味しない。
