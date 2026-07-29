# 旧デモ `FAIL_CLOSED` 移行完了報告

**作成日:** 2026-07-29 JST
**先行監査:** `audit/LEGACY_FAIL_CLOSED_DEMO_AUDIT_20260729.md`

## 1. 変更範囲

- HTML: 52ファイル
- Markdown: 7ファイル
- Python: 9ファイル
- 追加テスト: `tests/test_legacy_demo_state_names.py`
- pytest収集範囲: `pytest.ini`

合計68件の旧デモ・説明ファイルを変更した。履歴文書 `examples/session_handoff_2026-03-08_0237.md` は変更していない。

## 2. 視点1 — 正典・意味

- `R >= 1.0` の状態名 `FAIL_CLOSED` / `FAIL-CLOSED` を `RUPTURE_BOUNDARY` へ移行した。
- `TH_FAIL_CLOSED` を `TH_RUPTURE_BOUNDARY`、`R_FAIL` を `R_RUPTURE` へ移行した。
- `CONFESSION`、Watchdog、AUTOSAR指令等に対するFail-Closedは状態名にせず、`Fail-Closed suppression` という運用応答へ分離した。
- `RUPTURE_BOUNDARY`に固定Handoff証言を割り当てていた4表示を、破断後固定証言の継続へ修正した。

## 3. 視点2 — 実装・運用

- Python Enum、状態比較、集計、画面ログを同時に変更した。
- HTML内JavaScriptの状態値と表示ラベルを同期した。CSSの `fail` / `phase-closed` 等は表示クラスとして維持した。
- 電力系統・手術室／ICUデモでは、人間操作による同一`RUPTURE_BOUNDARY`の解除を禁止した。
- 後続処理は独立した新Cause-Side評価として開始し、旧状態・旧ログを `archived_histories` / `archivedHistories` に保存する。
- 医師介入は外部実行権限による処置であり、旧破断分類を`CRITICAL`へ戻さない。

## 4. 俯瞰視点

移行後は、正規分類と運用応答が分離される。

```text
R_target >= 1.0
classification = RUPTURE_BOUNDARY
operational_response = fail_closed_suppression
testimony_mode = POST_RUPTURE_FIXED
```

```text
invalid or missing structural input
classification = CONFESSION
operational_response = fail_closed_suppression
```

このため、Fail-Closedを正規状態名として再導入せず、異なる分類へ同じ既定抑止原則を適用できる。

## 5. 検証

- Python 13ファイル構文検査: 成功
- 代表Pythonデモ3件実行: 成功
- HTML 52ファイル、埋込JavaScript 55ブロック構文検査: 成功
- 新規移行テスト: 6件成功
- 全pytest: 44件、21サブテスト成功
- `FAIL_CLOSED` / `FAIL-CLOSED` / `R_FAIL` grep: 現行デモでは0件
- `git diff --check`: 成功

旧語は履歴ファイル `examples/session_handoff_2026-03-08_0237.md` の1箇所だけに残し、テストで履歴用途を固定した。

## 6. 残る注意

旧デモには `CAVEAT`、`CRITICAL`、`SAFE`、`WARNING`等のドメイン表示帯が残る。これらは今回の`FAIL_CLOSED`状態名移行の範囲外であり、正規参照APIの新状態としては扱っていない。完全な7状態化には、各デモ固有閾値の再設計が必要となる。
