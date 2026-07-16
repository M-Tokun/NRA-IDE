# NRA-IDE 第2次CLI精査 継続Report — Causal Diode EN Visual

- 実施日: 2026-07-15 JST
- 対象: `docs/en-US/figures/causal_diode_fail_closed_EN.html`
- 位置付け: 因果ダイオード日英文書に続き、英語版可視化を1ファイル質疑形式で追加精査・整合した記録
- 先行継続Report: `19_cli_second_pass_continuation_causal_diode_en.md`、`20_cli_second_pass_continuation_causal_diode_jp.md`
- RAW監査報告01～17: 変更なし
- CHKポイント: 作成なし
- Git stage / commit / push: 実施なし

## 1. 検出した問題

- JavaScript辞書は`en`だけだったが、初期化時に`setLang('jp')`を呼び、未定義辞書参照で停止する構造だった。
- 状態表示が`SAFE / WATCH / LIMIT`、境界値が固定`0.4 / 0.8 / 1.0`で、`R_warn / R_handoff / R_irrev`および`IRREVERSIBLE_TRANSITION`を実装していなかった。
- `R_irrev`到達後の不可逆ラッチがなかった。
- `R >= 1`後に`Restart Simulation`と`resetSystem()`で同じ履歴を初期状態へ戻し、破断後の終端と新履歴生成を分離していなかった。
- ページ表題、CSS、変数、関数に`Fail-Closed`旧解釈が残っていた。
- `$\tau$`を`Structural Tolerance`、`$\delta$`を`Load / Deviation`と表示していた。
- 因果ダイオード説明はEffect-Sideによる現在値の遡及変更禁止に限定され、旧Effect-Side終端と新Cause-Side独立開始を示していなかった。

判定: `HARD_CONFLICT / BOUNDARY_CONFLICT / SEMANTIC_DRIFT / RUNTIME_ERROR`

## 2. 利用者決定

対象全文の問題、影響、推奨修正案を編集前に提示した。利用者は推奨案を`y`で承認した。

変更単位は`docs/en-US/figures/causal_diode_fail_closed_EN.html`だけに限定した。ファイル名の移動・変更は行っていない。

## 3. 修正内容

- 初期言語を`en`へ修正した。
- 表題と画面表示を`Causal Diode & Irreversible Boundary`へ変更した。
- `Fail-Closed`のCSS状態、変数、関数、再始動操作を、履歴終端と破断境界の語彙へ置換した。
- `$\delta$`を`Accumulated Deviation`、`$\tau$`を`Absorption Thickness`として表示した。
- 事前固定した例示閾値`R_warn=0.40`、`R_handoff=0.80`、`R_irrev=0.90`を画面とコードへ明示した。
- 有効入力の例示範囲で`PERMIT`、`BOUNDARY_WARNING`、`HANDOFF_REQUIRED`、`IRREVERSIBLE_TRANSITION`、`RUPTURE_BOUNDARY`を境界同値込みで実装した。
- `R_irrev`到達後は表示Rが低下しても`IRREVERSIBLE_TRANSITION`を保持するラッチを実装した。
- `R >= 1`で旧履歴を終端し、sliderとEffect-Side操作を停止して最終固定証言を表示した。
- `Restart Simulation`を廃止し、`Start New Independent History`で履歴IDを更新する独立開始へ変更した。
- 新履歴開始時は旧Effect-Side値を持ち越さないことを画面とログへ明記した。
- 相転移・破断後の物理的痕跡は、新しく宣言した対象への新規観測としてのみ扱うと説明した。
- Effect-SideからCause-Sideへの禁止を、自動、手動、人間レビュー、承認、版更新のすべてへ拡張した。
- 二重ゆらぎ欄を常時表示し、このデモには独立した第二観測軸がないため`NOT_OBSERVABLE`と理由を表示した。
- 正規参照実装ではない有効入力限定の概念可視化であり、安全等を保証しない旨を画面へ追加した。

赤い`AI: Attempt Fake SAFE Signal`は、Effect-Sideによる禁止された逆流の試行例であるため残した。正規状態名としての`SAFE`ではない。

## 4. 検証

```text
FULL_READ_LINES=684
DIV_BALANCED=True
SCRIPT_BALANCED=True
INLINE_SCRIPT_COUNT=1
JS_SYNTAX=OK
BOUNDARY_AND_HISTORY_BEHAVIOR=OK
TARGET_DIFF_CHECK=OK
SHA256=4AE2C5662FD28E409F13985BCCCE57432D588172E861AC44C1BF56ADD2AD5BB5
```

Node模擬DOMで次を実行確認した。

- `R=0` → `PERMIT`
- `R=R_warn` → `BOUNDARY_WARNING`
- `R=R_handoff` → `HANDOFF_REQUIRED`
- `R=R_irrev` → `IRREVERSIBLE_TRANSITION`
- ラッチ後に`R=0.2`へ低下 → `IRREVERSIBLE_TRANSITION`を保持
- `R=1` → 破断境界overlay、旧履歴終端、slider無効
- 新履歴開始 → `H-002`、overlay解除、独立入力から`PERMIT`

旧識別子`Fail-Closed`、`fail-closed`、`isFailed`、`triggerFailClosed`、`resetSystem`、`Restart Simulation`、`setLang('jp')`、旧正規状態用`SAFE / WATCH / LIMIT`の残存はなかった。

HTML内にもともと存在する行末空白は残るが、今回差分に新規行末空白はなく、対象限定`git diff --check`は合格した。

実ブラウザ描画は実行していないため、ブラウザ固有のレイアウト合格は主張しない。

## 5. 判定

対象可視化は、完全一方通行の因果ダイオード、正規境界、不可逆ラッチ、旧Effect-Sideでの履歴終端、新Cause-Side・新ダイオードからの独立開始を実行挙動として分離した。

この判定は当該1ファイルの構文と模擬DOM動作に限定する。リポジトリ全体または実ブラウザ表示の整合済みを意味しない。
