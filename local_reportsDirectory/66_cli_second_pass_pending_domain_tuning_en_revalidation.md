# 第2次CLI精査 継続報告 66 — `11_domain_tuning_EN.md` 限定再検証（承認待ち）

## 対象

- `docs/en-US/ai/11_domain_tuning_EN.md`
- 既存完了報告: `local_reportsDirectory/27_cli_second_pass_continuation_domain_tuning_en.md`

## 現在位置の確認

- 対象ファイルを前後半に分割して全文確認した。
- 現在のSHA-256は `2157C00281AC7975D9BBA797272DBA2688C7C9A9AE9701244DEFC99C28EEA9B0` であり、報告27の完了時ハッシュと一致する。
- `git diff --check -- docs/en-US/ai/11_domain_tuning_EN.md` は問題なし。
- 報告27で確定した、Domain Tuningを評価前の外部設計活動とする境界、旧Effect-Side終端、新対象・新Cause-Side・新因果ダイオードからの独立開始、三つの正典閾値と破断境界の分離、物理的残存物の新規観測、不可逆ラッチの維持は保存されている。

## 新たに検出した問題

### 1. 条件付き適合を「NRA-IDEが保証できること」としている

問題箇所:

- 冒頭で `what NRA-IDE can guarantee` と `prerequisites under which those guarantees hold` と記述している。

正典境界との衝突:

- 運用応用が示せるのは明示条件下の適合特性であり、対象系の安全、正しさ、復旧を保証しない。
- 生存領域の安全応用は安全保証理論ではない。

影響:

- Domain Tuningが条件付き実装適合ではなく、保証成立条件を設計する作業だと誤読される。

推奨修正案:

- 冒頭を、Chapter 10が条件付き適合特性と非保証範囲を分離した説明へ修正する。
- Domain Tuningが安全保証を生成しないことを維持する。

### 2. Handoffを人間への判断・権限移譲として扱う表現が広く残る

問題箇所:

- `judgment is handed over to humans`、`delegates judgment to humans`、`matter is handed over to humans` が残る。
- `handoff paths`、`handoff arrangements`、通知の `recipient`、`human review required` が旧経路内の引渡しに読める。
- 医療の `emergency handoff paths`、航空の `authority transfer`、言語生成の `handoff recipient` が同じ経路として混在する。
- 自由記述禁止は `R >= 1` の最終固定証言だけに限定され、固定Handoff証言に適用されていない。

正典境界との衝突:

- Handoffは旧因果経路内から人間へ判断権限を渡し、旧Effect-Sideから処理を継続する経路ではない。
- Fail-Closed後に提示できるのは固定Effect-Side証言であり、人間が行うのは終端済み経路外の外部監査または現場対応である。

影響:

- 人間レビュー、権限移送、通知受領を介して旧Effect-Sideから更新を継続できるように読める。
- 固定Handoff証言で自由記述の停止説明を生成する余地が残る。

推奨修正案:

- Handoff設計を、Handoff閾値、固定Handoff証言のスキーマ、外部人間監査・現場対応の連絡経路へ修正する。
- `human review required` を、外部人間監査へ提示する固定Effect-Side証言へ置換する。
- 固定Handoff証言と最終固定証言の双方で、LLMによる自由記述の停止説明を禁止する。
- ドメイン固有の現場権限・責任は、旧因果ダイオード外の運用事項として分離する。

### 3. LLM三層構成を普遍的な不変原則としている

問題箇所:

- 不変原則として `Separation of responsibilities among Pre-NRA / LLM / Post-NRA` を全実装へ要求している。

正典境界との衝突:

- Pre-NRA / LLM / Post-NRA は、LLMを含み当該構成を宣言するシステムに対する実装形態であり、NRA-IDE本体または全実装の普遍的要件ではない。
- 普遍的に不変なのはCause-SideとEffect-Sideの権限分離、正典状態挙動、証拠、テストである。

影響:

- NRA-IDEを特定のLLM三層実装へ縮小し、LLMを含まない適合実装を誤って排除する。

推奨修正案:

- 普遍的不変原則を権限分離と正典挙動へ修正する。
- 三層責務の分離は、LLMを含み三層構成を宣言したシステムに限って適用する。

### 4. Effect-Sideからの非再利用禁止が不完全

問題箇所:

- 不変原則に `irreversible state` が残り、状態と不可逆ラッチが分離されていない。
- Discard Logの禁止対象が入力、更新根拠、規則、出所に限定されている。
- 物理的残存物の段落では、旧Effect-Side値の禁止用途を変換入力と出所に限定している。
- 変更記録とログ監査の禁止対象が、値、規則根拠、将来規則根拠、Cause-Side資料など一部用途に限定されている。

正典境界との衝突:

- 旧Effect-Sideの値、正典三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所は、旧Cause-Sideにも新Cause-Sideにも戻せない。
- import、名称変更、再構成、再利用のすべてを禁止する必要がある。

影響:

- 列挙されていない要素や名称へ変換すれば、旧Effect-Sideを将来設計・新Cause-Sideへ持ち越せるとの解釈が残る。

推奨修正案:

- すべての遮断一覧を、値、正典三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所へ統一する。
- 自動、手動、人間レビュー、承認、版更新のいずれにも、import、名称変更、再構成、再利用の禁止を適用する。
- 物理的残存物の新規観測は維持し、旧Effect-Side記録・権威の再利用と分離する。

## 保存すべき既存内容

- Domain Tuningは適用評価前に完了する外部設計活動であり、終端済みダイオード経路を継続しない。
- 三つの正典閾値は評価前に根拠とともに固定し、`R = 1` の破断境界と分離する。
- `R = 1` は宣言済み評価の `RUPTURE_BOUNDARY` であり、自然界一般の相転移境界ではない。
- 不可逆ラッチは同一履歴内で解除できない。
- 後続評価は独立した新対象、新Cause-Side、新規則、新因果ダイオードから始まる。
- 物理的残存物は独立した新対象の一部として新たに観測できる。

## 判定

対象ファイルは報告27完了時の内容が保存されているが、確定済みの非安全保証、Handoff、履歴境界、構成条件に照らして上記4項目を検出した。現時点では対象ファイルを編集していない。利用者の承認後、上記範囲だけを修正し、全文構造、旧表現、因果方向、分類境界、Markdown形式、リンクおよびテストを再検証する。
