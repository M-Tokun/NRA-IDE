# 第2次CLI精査 継続報告 70 — `12_glossary_EN.md` 限定再検証（承認待ち）

## 対象

- `docs/en-US/ai/12_glossary_EN.md`
- 既存完了報告: `local_reportsDirectory/25_cli_second_pass_continuation_glossary_en.md`

## 現在位置の確認

- 対象ファイルを3区間に分割して全文確認した。
- 現在のSHA-256は `97FB0715E83972F40E13F039AD5B3AB5CD531389BE6933AD4978B1753DD7E47E` であり、報告25の完了時ハッシュと一致する。
- `git diff --check -- docs/en-US/ai/12_glossary_EN.md` は問題なし。
- 報告25で確定した、唯一の公理、基礎式の非縮小分類、二重ゆらぎ式のIDE計算系分類、完全一方向の因果ダイオード、三つの正典閾値、`RUPTURE_BOUNDARY`、旧経路終端、物理的残存物の新規観測は保存されている。

## 新たに検出した問題

### 1. Handoffを人間への判断・責任移譲として定義している

問題箇所:

- `delegate judgment to humans`、`transfer responsibility to a qualified human`、`hand the matter over` が残る。
- `handoff paths`、`fixed-schema handoff notification`、通知の `recipient` が旧経路内の引渡しに読める。
- Final Fixed Testimonyに `required human review` が残る。
- Discard Logに `human handoff` が残る。
- 医療の `emergency handoff paths`、航空の `authority transfer`、言語生成の `handoff recipient` が同じ経路として混在する。
- 最小整合表の `HANDOFF_REQUIRED` が固定通知を返すだけで、外部人間監査と旧経路終端外の位置が不明確である。

正典境界との衝突:

- Handoffは旧因果経路内から人間へ判断・責任・権限を移し、旧Effect-Sideから処理を継続する経路ではない。
- Fail-Closed後に提示できるのは固定Effect-Side証言であり、人間が行うのは終端済み経路外の外部監査または現場対応である。

影響:

- Glossaryの定義自体が、旧Effect-Sideから人間判断を介して次のCause-Sideへ進む逆流経路を正典化する。
- 固定Handoff証言を単なる通知として扱い、外部監査証言と自由記述禁止の境界を失う。

推奨修正案:

- `R_handoff`、`HANDOFF_REQUIRED`、Fail-Closed、固定通知、Discard Log、最小整合表を、固定Handoff証言と外部人間監査へ統一する。
- `Fixed-Schema Handoff Notification` を互換名称として残す場合も、正典名称を固定Handoff証言とし、旧経路内の引渡しではないと明記する。
- 固定Handoff証言と最終固定証言の双方で、LLMによる自由記述の停止説明を禁止する。
- ドメイン固有の現場責任・対応は終端済み因果ダイオード外の運用事項として分離する。

### 2. Pre-NRA / LLM / Post-NRA三層を普遍的な構造として定義している

問題箇所:

- `Sandwich Architecture` 節が条件なしで三層を定義している。
- Pre-NRA、LLM、Post-NRAの記述が、すべてのNRA-IDE実装に必要な普遍構造として読める。

正典境界との衝突:

- 三層はLLMを含み当該構成を宣言するシステムに対する実装形態であり、NRA-IDE本体または全実装の普遍的要件ではない。
- 普遍的に必要なのはCause-SideとEffect-Sideの権限分離、正典状態挙動、証拠、テストである。

影響:

- GlossaryがNRA-IDEを特定のLLM三層実装へ縮小し、LLMを含まない適合実装を誤って排除する。

推奨修正案:

- 節名と導入で、LLMを含み三層構成を宣言する場合に限ると明記する。
- 層数だけでは適合性を判定せず、権限分離、正典挙動、証拠、テストに依存すると明記する。

### 3. Effect-Sideから戻せない要素の列挙が不完全

問題箇所:

- Roles、`Pi-inverse`、Cause-Side、Effect-Side、Discard Log、Design changeの各定義で禁止対象が異なる。
- 値、正典三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所の一部が各所で欠落する。
- 旧Effect-Side値だけを対象とし、閾値、状態、ラッチ、規則、出所などのimport、名称変更、再構成、再利用を明示しない箇所がある。

正典境界との衝突:

- 旧Effect-Sideの値、正典三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所は、旧Cause-Sideにも新Cause-Sideにも戻せない。
- 自動、手動、人間レビュー、承認、版更新のすべてで、import、名称変更、再構成、再利用を禁止する必要がある。

影響:

- Glossary内の定義差を利用して、列挙されていない要素や名称を将来設計・新Cause-Sideへ持ち越せるとの解釈が生じる。

推奨修正案:

- すべての非再利用一覧を、値、正典三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所へ統一する。
- import、名称変更、再構成、再利用の禁止を、新旧いずれのCause-Sideにも適用する。
- 物理的残存物の新規観測は維持し、旧Effect-Side記録・権威の持越しと分離する。

### 4. `NRA-IDE guarantees` という保証分類が残る

問題箇所:

- LLM定義で、意味上の正確さ等を `outside the scope of NRA-IDE guarantees` としている。

正典境界との衝突:

- NRA-IDEの運用応用が示せるのは条件付き適合特性であり、対象系の安全や出力の正しさを保証しない。

影響:

- 正確さ以外にはNRA-IDEによる保証領域が存在するとの誤読を生む。

推奨修正案:

- 意味上の正確さ、事実性、利用者適合性はNRA-IDEによって保証されない、と直接記述する。

## 保存すべき既存内容

- 公理は「存在は生成である。」という律環公理一つだけである。
- 基礎式は宣言対象の構造状態を正典の数学的関係へ落とす根本式であり、派生安全指標ではない。
- 二重ゆらぎ式は基礎式とともに正典IDE計算系を構成するが、公理ではない。
- IDEは計算方法・動力学エンジンであり、安全保証でもIntegrated Development Environmentでもない。
- `delta`は履歴を持つ蓄積偏差、`tau`は吸収厚さである。
- 三つの正典閾値と`R = 1`の破断境界を分離する。
- 因果ダイオードはCause-SideからEffect-Sideへの完全な一方向である。
- 旧経路はEffect-Sideで終端し、後続履歴は独立した新対象、新Cause-Side、新規則、新因果ダイオードから始まる。
- 物理的残存物は独立した新対象の一部として新たに観測できる。

## 判定

対象ファイルは報告25完了時の内容が保存されているが、確定済みの非安全保証、Handoff、履歴境界、構成条件に照らして上記4項目を検出した。現時点では対象ファイルを編集していない。利用者の承認後、上記範囲だけを修正し、全文構造、分類、旧表現、因果方向、最小整合表、Markdown形式、リンクおよびテストを再検証する。
