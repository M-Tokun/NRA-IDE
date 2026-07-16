# NRA-IDE 第2次CLI精査 継続Report — Causal Diode JP Visual

- 実施日: 2026-07-15 JST
- 対象: `docs/ja-JP/figures/causal_diode_fail_closed_JP.html`
- 位置付け: 英語版可視化に続き、日本語版可視化を1ファイル質疑形式で追加精査・整合した記録
- 先行継続Report: `21_cli_second_pass_continuation_causal_diode_en_visual.md`
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 検出した問題

- 表題、CSS、変数、関数、再始動操作に`Fail-Closed`旧実装が残っていた。
- `$\delta$`を`Load / Deviation`、`$\tau$`を`Structural Tolerance / 構造的許容限界`と表示していた。
- 状態表示が`SAFE / WATCH / LIMIT`、境界値が固定`0.4 / 0.8 / 1.0`で、`R_irrev`と`IRREVERSIBLE_TRANSITION`がなかった。
- `R_irrev`到達後の不可逆ラッチがなかった。
- `R >= 1`後に`シミュレーションをリセット / resetSystem()`で同じ履歴を初期状態へ戻していた。
- 因果ダイオード説明が現在値への逆流禁止に限定され、旧Effect-Side終端と新Cause-Side独立開始を示していなかった。
- 二重ゆらぎ必須欄がなかった。

日本語版には`jp`と`en`の両辞書があり、初期言語`jp`は有効だったため、英語版で確認した未定義辞書エラーはなかった。

判定: `HARD_CONFLICT / BOUNDARY_CONFLICT / SEMANTIC_DRIFT`

## 2. 利用者決定

対象全文の問題、影響、推奨修正案を編集前に提示した。利用者は推奨案を`y`で承認した。

変更単位は`docs/ja-JP/figures/causal_diode_fail_closed_JP.html`だけに限定した。ファイル名の移動・変更は行っていない。

## 3. 修正内容

- 日英切替機能を保持したまま、画面と挙動を英語版可視化の確定内容へ同期した。
- 表題を`Causal Diode & Irreversible Boundary`へ変更した。
- `Fail-Closed`のCSS状態、変数、関数、再始動操作を、履歴終端と破断境界の語彙へ置換した。
- `$\delta$`を`Accumulated Deviation / 蓄積ズレ`、`$\tau$`を`Absorption Thickness / 吸収厚み`として表示した。
- 事前固定した例示閾値`R_warn=0.40`、`R_handoff=0.80`、`R_irrev=0.90`を日英画面とコードへ明示した。
- 有効入力の例示範囲で`PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`を境界同値込みで実装した。
- `R_irrev`到達後は表示Rが低下しても`IRREVERSIBLE_TRANSITION`を保持するラッチを実装した。
- `R >= 1`で旧履歴を終端し、sliderとEffect-Side操作を停止して最終固定証言を表示した。
- resetを廃止し、日英の`Start New Independent History / 独立した新履歴を開始`へ変更した。
- 新履歴開始時は履歴IDを更新し、旧Effect-Side値を持ち越さないことを日英画面とログへ明記した。
- 相転移・破断後の物理的痕跡を、新しく宣言した対象への新規観測としてのみ扱うと日英で説明した。
- Effect-SideからCause-Sideへの禁止を、自動、手動、人間レビュー、承認、版更新のすべてへ適用した。
- 二重ゆらぎ欄を常時表示し、独立した第二観測軸がないため`NOT_OBSERVABLE`と理由を日英で表示した。
- 正規参照実装ではない有効入力限定の概念可視化であり、安全等を保証しない旨を日英で追加した。

赤い偽装`SAFE`ボタンは、Effect-Sideによる禁止された逆流の試行例であるため残した。正規状態名としての`SAFE`ではない。

## 4. 検証

```text
FULL_READ_LINES=719
DIV_BALANCED=True
SCRIPT_BALANCED=True
INLINE_SCRIPT_COUNT=1
JS_SYNTAX=OK
BOUNDARY_HISTORY_AND_LANGUAGE=OK
TARGET_DIFF_CHECK=OK
SHA256=FD6CBFA5AE8036C139ABCEB0B08428C3D8EC79C2BD8B93319C811F0022387C82
```

Node模擬DOMで次を実行確認した。

- `R=0` → `PERMIT`
- `R=R_warn` → `BOUNDARY_WARNING`
- `R=R_handoff` → `HANDOFF_REQUIRED`
- `R=R_irrev` → `IRREVERSIBLE_TRANSITION`
- ラッチ後に`R=0.2`へ低下 → `IRREVERSIBLE_TRANSITION`を保持
- `R=1` → 破断境界overlay、旧履歴終端
- 新履歴開始 → `H-002`、独立入力から`PERMIT`
- `jp → en → jp`切替後も因果方向表示と状態更新が正常

旧識別子`Fail-Closed`、`fail-closed`、`isFailed`、`triggerFailClosed`、`resetSystem`、`Restart Simulation`、`シミュレーションをリセット`、旧正規状態用`SAFE / WATCH / LIMIT`の残存はなかった。

対象限定`git diff --check`は合格した。実ブラウザ描画は実行していないため、ブラウザ固有のレイアウト合格は主張しない。

## 5. 判定

対象可視化は、日英表示を保持したまま、完全一方通行の因果ダイオード、正規境界、不可逆ラッチ、旧Effect-Sideでの履歴終端、新Cause-Side・新ダイオードからの独立開始を実行挙動として分離した。

この判定は当該1ファイルの構文と模擬DOM動作に限定する。リポジトリ全体または実ブラウザ表示の整合済みを意味しない。
