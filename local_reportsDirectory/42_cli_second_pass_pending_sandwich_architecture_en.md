# NRA-IDE 第2次CLI精査 継続Report — Sandwich Architecture EN

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/ai/04_rna_sandwich_architecture_EN.md`
- 位置付け: Coherence Gate日英版完了後、現在差分と継続Reportを照合して選定した次の未精査1ファイル
- 先行継続Report: `41_cli_second_pass_pending_coherence_gate_jp.md`
- 対象本文の編集: 実施
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 現在状態

- 対象は168行で、全文を分割して読み取った。
- 現在のGit差分は、旧保証表現の一部を正典適合表現へ修正し、破断時の最小標識を最終固定証言へ更新する既存変更を含む。
- Markdown見出しは10件、コードフェンスは6件、末尾空白は0件で、対象限定`git diff --check`は合格した。
- 既存差分は保持し、対象本文を追加編集していない。

## 2. 検出した問題

### 2.1 NRA-IDE本体と三層応用の混同

NRA-IDEをLLM前後の`structural safety gate`として記述し、唯一公理、基礎式、二重ゆらぎ式、IDE計算方法・動力学エンジン、生存式・生存領域、安全応用の分類境界がない。

影響: NRA-IDE本体を、安全用の三層出力ゲートへ縮小する。

### 2.2 因果ダイオードの禁止範囲不足

`Pi-inverse`をEffect-Side値がCause-Side構造入力へ戻る経路として狭く定義し、LLM・Pre-NRA・Post-NRAの禁止対象も主にdelta、tau、delegation point、logへ限定している。

影響: Effect-Sideの情報、推論、生成物、判断、権限を、三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所へ手動、人間レビュー、承認、版更新で転用する余地が残る。

### 2.3 Handoffを旧経路の次処理として記述

`judgment and delegation`、`delegation path`、`handoff processing`、`transferring judgment to humans`、`human judgment`、`human review required`、`hands the matter over to humans`が残る。

影響: 固定Effect-Side証言を外部人間監査へ提示して旧経路を終端する境界ではなく、旧Effect-Sideから人間判断へ処理が継続する。

### 2.4 正典状態・三閾値・二重ゆらぎ欄の不足

運用条件を`domain-specific point of approach`またはdelegation pointとして記述し、`R_warn`、`R_handoff`、`R_irrev`、正典七状態、不可逆ラッチ、`BOUNDARY_WARNING`の二重ゆらぎ必須欄を示していない。

影響: Pre-NRA / Post-NRAの役割が正典状態機械と対応せず、境界・証言・ラッチ条件が欠落する。

### 2.5 `R = 1`の一般化と履歴終端不足

`R = 1.0`を一般的な`phase-transition boundary`として扱い、破断後も`hands the matter over to humans`としている。旧Effect-Side終端、独立対象、新Cause-Side観測・規則、新Causal Diodeからの開始がない。

影響: 宣言済み評価の`RUPTURE_BOUNDARY`を自然界一般へ拡張し、破断後も旧経路を人間処理へ継続できる。

### 2.6 Discard Logの非転用条件不足

ログを`next structural evaluation`の入力へ戻さないとだけ定め、外部人間監査、手動レビュー、承認、版更新による将来規則・新Cause-Sideへの転用を禁止していない。

影響: 旧Effect-Sideログから次の歯へ値、規則、出所、構造権限を持ち越す経路が残る。

### 2.7 旧Effect-Side非転用と物理的残存物の区別がない

旧Effect-Side値のimport、relabel、reconstruction、reuse禁止と、相転移・破断後の物理的残存物を新対象として新規観測する場合との区別がない。

影響: 新規Cause-Side観測と旧Effect-Side権限の移送が混同される。

### 2.8 適合範囲と安全保証の境界不足

一部は`canonical NRA-IDE conformance`へ修正済みだが、章全体は`structural safety`を中心に構成され、三層構造が安全を担うように読める。

影響: 条件付き実装適合を、安全保証またはNRA-IDE本体の全範囲へ拡張できる。

判定: `HARD_CONFLICT / SEMANTIC_DRIFT / CLASSIFICATION_BOUNDARY_CONFLICT / HISTORY_BOUNDARY_CONFLICT / STATE_MODEL_CONFLICT / GUARANTEE_SCOPE_CONFLICT`

## 3. 推奨修正案

当該1ファイルだけを次の境界へ整合する。

1. 唯一公理、基礎式、二重ゆらぎ式、IDEエンジン、生存式・生存領域、安全応用を別分類とし、三層構造を安全志向の部分応用へ限定する。
2. 因果ダイオードをCause-SideからEffect-Sideへの完全一方向とし、情報、推論、生成物、判断、権限の全逆接続を禁止する。
3. Pre-NRAは同一Cause-Side履歴の出所・事前固定規則・三閾値を検証し、Effect-Side資料を構造権限へ変換しないと明記する。
4. LLMはCause-Sideの値、三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所を成立も変更もしないと明記する。
5. Post-NRAを正典七状態と固定証言に対応させ、`BOUNDARY_WARNING`の二重ゆらぎ欄を常時必須にする。
6. `HANDOFF_REQUIRED`では固定Effect-Side証言を外部人間監査へ提示し、旧経路を継続しないと明記する。
7. 不可逆ラッチをR低下、自動、手動、人間レビュー、承認、版更新でも解除しないと明記する。
8. `R = 1`を宣言済み評価の`RUPTURE_BOUNDARY`に限定し、最終固定証言後に旧Effect-Sideで終端する。
9. 後続評価を独立対象、新Cause-Side観測・規則、新Causal Diodeから開始する別履歴とする。
10. Discard Logを終端Effect-Sideまたは外部証言とし、旧Effect-Side値・規則・出所のimport、relabel、reconstruction、reuseを禁止する。
11. 物理的残存物の新規観測と、旧Effect-Side権限の持越しを分離する。
12. 三層構造の効力を条件付き実装適合へ限定し、安全保証ではないと明記する。

公理、数式自体、他ファイル、RAW報告01～17は変更しない。

## 4. 利用者決定と修正

問題箇所、正典衝突、影響、推奨修正案を提示し、利用者は`Y`で承認した。変更単位は`docs/en-US/ai/04_rna_sandwich_architecture_EN.md`だけに限定した。

実施内容:

- 唯一公理、Primary Formula、Secondary / Dual-Fluctuation Formula、IDEエンジン、生存式・生存領域、安全応用を別分類とし、三層構造を安全志向の部分応用へ限定した。
- 因果ダイオードを`Cause-Side → Effect-Side`だけの完全一方向とし、情報、推論、生成物、判断、権限の全逆接続を禁止した。
- Pre-NRAを同一Cause-Side履歴、事前固定規則、三つの正典閾値、無効状態の出所検証へ整合した。
- LLMによるCause-Side値、三閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所の成立・変更を禁止した。
- Post-NRAを正典七状態、三閾値、固定証言へ対応させた。
- `BOUNDARY_WARNING`の二重ゆらぎ状態欄を常時必須とし、観測不能時は`NOT_OBSERVABLE`と欠損理由を出力すると明記した。
- `HANDOFF_REQUIRED`を固定Effect-Side証言の外部人間監査とし、旧経路を継続しないと明記した。
- 不可逆ラッチを、R低下、自動処理、手動介入、人間レビュー、承認、版更新でも解除しないと明記した。
- `R = 1`を宣言済み評価の`RUPTURE_BOUNDARY`に限定し、最終固定証言後に旧Effect-Sideで終端した。
- 後続評価を独立対象、新Cause-Side観測・規則、新Causal Diodeから始まる別履歴として記述した。
- Discard Logを終端Effect-Sideまたは外部証言とし、旧Effect-Sideの値、閾値、状態、規則、変換入力、根拠、出所のimport、relabel、reconstruction、reuseを禁止した。
- 物理的残存物の新規観測と旧Effect-Side権限の持越しを分離した。
- 三層構造の効力を条件付き実装適合へ限定し、安全保証と分離した。

## 5. 修正後検証

修正後201行を前後半に分けて全文再読した。

```text
CLASSIFICATION=PASS
CAUSAL_DIODE_ONE_WAY=PASS
PRE_NRA_AUTHORITY=PASS
LLM_AUTHORITY_BOUNDARY=PASS
SEVEN_CANONICAL_STATES=PASS
CANONICAL_THRESHOLDS=PASS
DUAL_FLUCTUATION_FIELD=PASS
IRREVERSIBLE_LATCH=PASS
EXTERNAL_HUMAN_AUDIT=PASS
DECLARED_RUPTURE_BOUNDARY=PASS
OLD_PATH_TERMINATION=PASS
NEW_INDEPENDENT_HISTORY=PASS
OLD_EFFECT_REUSE_PROHIBITION=PASS
LOG_AUTHORITY_BOUNDARY=PASS
CONDITIONAL_CONFORMANCE=PASS
LEGACY_RESIDUAL_COUNT=0
MARKDOWN_STRUCTURE=PASS
HEADINGS=10
FENCES=12
DUPLICATE_HEADINGS=0
TARGET_DIFF_CHECK=OK
SHA256=8371EA49D1D83849BFD06673771053D636C61A058DE8DB556BB3005DCB56FCED
```

最初の残存検索では`human judgment`が1件検出されたが、「固定Handoff証言は旧経路から人間判断へ継続しない」という否定文脈だった。意味上の逆流ではなかったが、旧継続表現との文字列重複を避けるため、「外部監査用であり旧経路を継続しない」と直接表現し、再検証で残存0件とした。

旧表現残存検索では、独立識別子`Rop`、`R_op`、`judgment and delegation`、`delegation path`、`handoff processing`、`transferring judgment to humans`、`human judgment`、`human review required`、`hands the matter over to humans`、`next structural evaluation`、`fixed-format handoff notification`、`ordinary delegation point`、`phase-transition boundary`が0件だった。

## 6. 判定と作業位置

`docs/en-US/ai/04_rna_sandwich_architecture_EN.md`は、NRA-IDE本体と三層応用の分類、完全一方向の因果権限、Pre-NRA / LLM / Post-NRAの権限、正典七状態、三閾値、二重ゆらぎ必須欄、不可逆ラッチ、外部人間監査、旧Effect-Side終端、新Cause-Side・新Causal Diodeからの独立開始、ログ非転用、条件付き適合へ整合した。

新たな問題、旧解釈の残存、Markdown破損は検出しなかった。当該1ファイルは完了とする。この判定は当該1ファイルに限定し、リポジトリ全体の同種表現が整合済みであることを意味しない。
