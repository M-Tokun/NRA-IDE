# 完全破断後の観測・記録・通信経路 正規化完了報告

**作成日:** 2026-07-29 JST
**対象:** NRA-IDE正典、機械可読正典、参照実装、決定論的テスト、公開説明、派生文書
**先行監査:** `audit/RUPTURE_OBSERVATION_BOUNDARY_AUDIT_20260729.md`

## 1. 変更したファイル

### 上位正典・理論

- `theory/AXIOMS.md`
- `theory/axioms.json`
- `FORMULA.md`
- `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
- `theory/SANDWICH_ARCH.md`
- `theory/THEORY.md`
- `llms.md`

### 参照実装・テスト・公開入口

- `nra-core/foundations/NRA-IDE_Architecture_public.py`
- `docs/NRA-IDE_Architecture_public.py`
- `tests/test_nra_ide_reference.py`
- `README.md`
- `README_JP.md`

### 派生文書・図版ソース

- `docs/Sandwich-ARCHITECTURE.md`
- `docs/en-US/ai/` 内の関連10文書
- `docs/ja-JP/ai/` 内の関連11文書
- `docs/en-US/figures/causal_diode_fail_closed_EN.html`
- `docs/ja-JP/figures/causal_diode_fail_closed_JP.html`
- `docs/ja-JP/figures/domain_tuning_structure_pure.html`
- `docs/figures/M3_NRA_biomimetic_sandwich_svg.html`
- `docs/figures/M5_NRA_IDE_flip_glossary.html`
- `docs/figures/M5_NRA_IDE_flip_glossary_EN.html`
- `docs/figures/NRA_IDE_interactive_docs_all_modules.html`
- `theory/figures/sources/NRA-IDE_core_formula.svg`
- `theory/figures/sources/TOP_sandwich.svg`
- `theory/figures/NRA-IDE定義式（基礎式）.jpg`
- `theory/figures/TOP_sandwich.png`
- `docs/TOP_sandwich.png`
- `examples/README_Demo15_OR_ICU_2026-03-21.md`
- `multi-physics-safety-gate/NRA-IDE_08_Multi-Physics-Safety-Gate_EN.html`
- `multi-physics-safety-gate/NRA-IDE_08_Multi-Physics-Safety-Gate_JP.html`

### 英語解説三部作

- `note/note掲載英文AIと海外向け/The Canonical Interpretation of NRA-IDE.md`
- `note/note掲載英文AIと海外向け/Humans_Are_Training_Dangerous_AI_Capabilities.md`
- `note/note掲載英文AIと海外向け/Preventing_Misinterpretation_of_NRA-IDE.md`

### 監査記録

- `audit/RUPTURE_OBSERVATION_BOUNDARY_AUDIT_20260729.md`
- 本報告書

## 2. 各ファイル群の変更理由

- 上位正典: `R_target >= 1.0` の対象限定、Handoffの実行権限限定、破断後固定証言の継続性、Cause-Side正規更新と評価スナップショット固定を定義するため。
- 機械可読正典: 対象、観測、記録、通信、実行権限、証言モードを別次元として決定論的に読めるようにするため。
- 参照実装: 個別観測チャネルと最終有効観測メタデータを保持し、対象破断後も生存チャネルを停止しないため。
- テスト: 指定された20境界を含む38件で、権限・チャネル・証言・ラッチ・欠測・定義域外を検証するため。
- README・派生文書・図版ソース・英語三部作: 上位正典の修正後も旧「一回限りの最終固定証言」解釈が公開層へ残らないよう同期するため。

## 3. 変更しなかった関連ファイルと理由

- `AGENTS.md`: 作業開始前から存在した利用者差分を保持し、今回の境界修正対象ではないため変更していない。
- `RULES_DETAIL.md`、`CODEX.md`: 作業規則として全文確認したが、正典境界の内容を保持する文書ではないため変更していない。
- `ground/` の既存・未追跡文書、`note/AIがNRA-IDEを誤解しないための正典的解釈文.md`: 利用者の既存作業であり、指定された同期順序の正典・参照実装・派生文書とは分離して保持した。
- `examples/session_handoff_2026-03-08_0237.md`: 旧版の履歴的引継ぎ記録であり、現行正典へ改変すると履歴性を失うため変更していない。
- 既存デモ・ドメイン実装の `FAIL_CLOSED` 表示: 旧デモ固有の運用ラベルであり、正規参照APIの状態追加ではない。全デモの状態機械再設計は今回の「最小分離」を超えるため変更していない。
- `theory/AXIOMS.md` と `theory/axioms.json` の変更履歴内にある旧「最終固定証言」表現: 旧版の記録として用途が明示されているため保持した。

## 4. 新しく固定した境界

```text
R_target >= 1.0
→ declared target reaches RUPTURE_BOUNDARY
→ testimony_mode = POST_RUPTURE_FIXED
```

次は独立であり、対象破断から自動導出しない。

```text
TargetBoundaryState
ObservationChannelState
LoggingChannelState
CommunicationChannelState
ExecutionAuthorityState
StructuralTestimonyMode
```

Handoffで変更するのは `execution_authority` だけである。構造証言経路、監査ログ経路、監査ログ保管主体、責任、法的責任、結果責任は暗黙に移転しない。

観測喪失は `OBSERVATION_LOST`、記録喪失は `LOGGING_LOST`、通信喪失は `COMMUNICATION_LOST` として対象破断から分離する。欠測値をゼロ、安全、安定、回復、破断へ補完しない。

破断後固定証言は一回限りの終端メッセージではない。生存する観測・記録・通信・証言経路が利用可能な間、事前固定形式で継続する。

## 5. 既存正典との互換性

次は変更していない。

- 唯一の律環公理「存在は生成である。」
- `R = delta / tau`
- `0 <= R_warn < R_handoff < R_irrev < 1.0`
- Cause-SideからEffect-Sideへの一方向生成
- Effect-SideからCause-Sideへの逆流禁止
- `R` を一般安全度、品質、確率、信頼度、最適化目的として扱わないこと
- `tau = 0` を `OUT_OF_DESCRIPTION_DOMAIN`、`R` を未定義とすること
- `R_irrev <= R < 1.0` の不可逆ラッチ
- 既存の正規状態順序

参照実装の既存呼出し互換フィールドと旧補助aliasは維持し、新しい独立状態を追加契約として返す。

## 6. 追加・更新したテスト

指定20項目を次のまとまりで網羅した。

- Handoffは実行権限だけを移し、責任・証言・監査経路を移さない。
- 対象破断はセンサー・ロガー・通信の破断を意味しない。
- `POST_RUPTURE_FIXED` へ切り替わり、自由生成を抑止しても固定証言は残る。
- 一つの観測喪失が他チャネルを停止せず、最終有効値・時刻・欠測開始・理由不明を保持する。
- 観測喪失と通信喪失は独立であり、欠測をゼロまたは安全へ変換しない。
- `tau = 0`、非有限値、不正閾値順序、Effect-Side書換え、不可逆ラッチを決定論的に処理する。
- 機械可読正典と参照実装／公開mirrorの同期を検証する。

## 7. 実行した検証コマンド

- `python -m py_compile ...`
- `python -m unittest tests.test_nra_ide_reference -v`
- `python -m pytest tests/test_nra_ide_reference.py -q`
- Python `json.loads` と正規フィールドassertによるJSON構文・構造検査
- `python scripts/check_links.py`
- `python scripts/check_path_case.py`
- `python scripts/verify_repo.py`
- `Get-FileHash -Algorithm SHA256 ...`
- 修正対象旧語と正規状態名の `rg` 監査
- `git diff --check`
- `git diff --stat`、`git status --short`、個別差分精査

## 8. テスト結果

- Python構文検査: 成功
- `unittest`: **38件すべて成功**
- `pytest`: **38テスト、21サブテストすべて成功**
- JSON構文・構造検査: `JSON_SCHEMA_OK`
- 内部リンク: 成功
- パス大文字小文字: 675追跡ファイルで成功
- 参照実装／公開mirror: SHA-256一致
  `C2EF08438C1FAD9CFF769F3FE16BB5D9D4FFB5CDB4965B6BC0D893AE6D10ED01`
- 修正対象旧語grep: 現行対象では該当なし。上位正典の変更履歴だけ旧語を履歴として保持
- `git diff --check`: エラーなし（Gitの将来改行正規化警告のみ）

## 9. 残存する未解決事項

今回の正典境界・参照実装・決定論的テストについて、既知の未解決不整合はない。

検証環境または別作業範囲として次が残る。

- `scripts/verify_repo.py` は14ファイルの既存問題を報告した。内容は `ground/`、利用者の未追跡 `note/`、癌治療支援サブシステム等のBOM・KaTeX・Markdown隣接文字であり、今回変更した正典・参照実装・派生文書に起因しない。
- 旧デモ群の `FAIL_CLOSED` 表示は、正典状態への全面移行を行う別作業として残る。

## 10. 利用者の判断が必要な箇所

今回の境界修正を採用するための追加判断はない。次は任意の後続作業である。

1. 旧デモ固有の `FAIL_CLOSED` 表示を正規状態名へ移行する別タスクを開始するか。
2. `verify_repo.py` が報告した今回対象外の14ファイルを別途修正するか。

## 11. 二視点および俯瞰精査

### 視点1 — 概念・正典

対象破断、実行権限、証言、監査、観測可能性を別概念として固定した。これにより「対象が破断したから観測も終了する」「Handoffしたから責任も移る」という誤推論を正典上拒否できる。

### 視点2 — 実装・運用

通知schemaと観測チャネル台帳で独立状態を保持し、喪失チャネルの最終有効メタデータを残す。自由生成・自律操作の抑止と、固定構造証言・監査ログの継続を同時に実装した。

### 俯瞰視点 — 文書・機械可読正典・コード・テスト

上位正典から機械可読正典、参照実装、mirror、テスト、README、AI解説、可視化HTML、英語三部作まで同じ直積状態モデルへ同期した。旧語は変更履歴と旧デモ互換範囲に限定され、現行の正典APIへ新しい別名状態は追加していない。
