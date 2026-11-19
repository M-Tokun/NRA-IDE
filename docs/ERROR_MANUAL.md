---
id: GUIDE-ERROR-MANUAL-20261116
kind: guide
created: 2026-11-16
author: M-Tokuni
title: "ERROR_MANUAL — エラー分岐・対処マニュアル（オンデマンド・直列ゲート）"
---

# ERROR_MANUAL — エラー分岐・対処マニュアル（オンデマンド・直列ゲート）

**読む条件：コマンド・Git・Hook・検証スクリプトがエラー（非0終了・エラー文字列出力・拒否メッセージ・`STOP`）を返したときだけ読む。**
平常時は読まない（`AGENTS.md` の肥大化および第1段階での不要な推論・トークン消費を防ぐため）。

本書は、エラー発生時の経路選択を固定するための **片道（DAG：有向非巡回）の直列ルックアップ表** である。本書から上位文書（`AGENTS.md`・`RULES_DETAIL.md`）の途中番号へ戻る遷移は行わず、必ず末端の `990 STOP` で呼び出し元へ `STOP` を返して当該ターンを終了する。

---

## 1. 経路設計原則（迷い・読み飛ばし・循環の排除）

1. **抽象語の禁止**:
   経路行に「必要な」「適切な」「状況により」「場合により」を書かない。**観測できる事実（1条件）** と **固定遷移先（`GOTO` / `GOSUB`）** だけを置く。
2. **同列選択（`select`・配列・`|` 並列）の禁止**:
   1つの行に複数の選択肢を横並び（`|`）で置かない。**1番号＝1条件＝1つの `GOTO`（不一致なら次の行番号へ落下）** の直列ふるいとし、行番号の小さい順を絶対の優先順位とする。
3. **循環・再試行ループの禁止（片道終了）**:
   - 本書の戻りは **`STOP` の1値のみ** とする（`DONE` を返して通常経路 `70 → 80 → 90 → 40` へ合流させない）。
   - 本書（エラー経路）の内部で新たなコマンドや代替スクリプトを実行しない。原因と次ターンの正規入口を確定し、`990 STOP` で必ず当該ターンを閉じる。

---

## 2. ERROR_MANUAL 本体経路（`10`〜`990`）

```text
#ROUTE ERROR_MANUAL v2 ; 番号はこのブロック内だけ（他文書の経路番号とは独立）
#RETURN 990=STOP ; 呼び出し元へは STOP だけを返す（DONE は返さない）
#CONST ; 全経路で常に成立。破れたら 990
E1 推測による回避実行（--no-verify・フック設定変更・NRA_PUSH_PLAN 手動注入・force-push）を禁止する
E2 同じ失敗コマンドを原因変更なしに反復しない
E3 エラー経路の内部で新たなコマンド・スクリプトを実行しない（判定と報告のみ行い 990 STOP で閉じる）
E4 未確認のまま完了・成功へ読み替えない
#END-CONST

10  観測事実の固定：実行コマンド・終了コード・標準出力/標準エラー末尾・JSON の status / reason / send_state を確定する。GOTO 20

20  IF 出力に "現在のAGENTS.md全文の読込を確認できません" を含む: GOTO 100
21  IF 出力に "AGENTS.mdが存在しないか" を含む: GOTO 100
22  IF 出力に "hook入力を検証できません" を含む: GOTO 110
23  IF 出力に "シェルコマンドを文字列として確認できません" を含む: GOTO 110
24  IF 出力に "は実行しません（AGENTS.md §7）" を含む: GOTO 300
25  IF 出力に "git pushは直接実行しません" を含む: GOTO 200
26  IF 出力に "\"reason\": \"PLAN_REQUIRED\"" を含む: GOTO 200
27  IF push.py の最終行が "STOP " で始まる: GOTO 210
28  IF push_gate.py の出力に "\"reason\":" を含む: GOTO 210
29  IF 出力に "error:" または "FAIL" または "UNAVAILABLE" を含む: GOTO 400
30  IF 終了コード != 0: GOTO 400
31  IF nra_depth_guard が停止を返した: GOTO 500
32  GOTO 900

100 セッション読込記録不一致（agents-md-guard 停止）：
    AGENTS.md の再読取では記録は戻らない。
    VS Code / IDE で F1 →「Developer: Reload Window（ウィンドウの再読み込み）」が必要であることを報告する。
    （注：Reload Window が必要な唯一のケース。push の PLAN_REQUIRED とは無関係）
    GOTO 990

110 Hook 入力・構文不正（agents-md-guard 停止）：
    実行しようとしたコマンド文字列と hook の拒否メッセージをそのまま報告し、分割・言い換え再試行をしない。
    GOTO 990

200 push 固定入口未経由 / PLAN_REQUIRED（素の git push による停止）：
    リモート障害・ブランチ先間違い・Reload Window の問題ではない（ローカル .githooks/pre-push → push_gate.py または PreToolUse が素の git push を停止）。
    エラー経路内ではコマンドを実行せず一旦停止し、次ターンで固定入口 python -B scripts/push.py prepare から開始することを報告する（対象外コミットを含む場合は AGENTS.md §7 選択範囲4 として確認）。
    GOTO 990

210 push 経路・ゲート停止（scripts/push.py / scripts/push_gate.py 停止）：
    docs/PUSH_PROCEDURE.md §2 の reason 表を辞書として1回だけ参照する（他文書へ遷移しない）。
    211 IF send_state == "UNKNOWN": 再送禁止。停止した step・reason・send_state を報告する。GOTO 990
    212 IF send_state == "COMMAND_SUCCEEDED_UNVERIFIED": 再送禁止。停止した step・reason・send_state を報告する。GOTO 990
    213 自動再試行・自動 merge/rebase・独自タイムアウト緩和・無断修正を行わず、reason・send_state・該当ファイル（local_reports/push_gate/<ID>/result.json）を報告する。GOTO 990

300 禁止 Git 操作ブロック（履歴改変・強制送信・remote ref 削除）：
    AI 経路では実行しない。対象 OID・影響範囲・拒否メッセージを提示して利用者管理の手順へ返す。
    GOTO 990

400 コマンド・リポジトリ検証・ゲート失敗（verify_repo / check_dictionary / id_gate / unicode_gate / malware_gate / check_links / check_path_case 等）：
    該当ファイル・行番号・規則名（例：DICT-* / BOM / CRLF / KaTeX）またはエラー出力末尾を観測事実として列挙する。
    利用者記述・既存資産を無断修正せず、修正案と影響を提示して承認を待つ。
    GOTO 990

500 探索深度ガード上限（nra-depth-guard 停止）：
    探索ループを即時停止する。ここまでの観測結果・確定事実・未確認範囲を報告する。
    GOTO 990

900 未登録エラー（20〜31 の既知パターンに該当しない失敗）：
    推測による別ルート試行や回避を行わない。
    実行コマンド・終了コード・出力末尾・未確定事項のみを提示する。
    GOTO 990

990 STOP：停止理由・観測事実・send_state・次ターンの正規手順/必要な承認をまとめ、呼び出し元へ STOP を返す（同一ターン内で再実行へ戻らない）
```

---

## 3. 切り分け早見表（何が原因で、何が原因でないか）

| 優先順（行） | 観測されたエラー・停止 | 真の原因（ローカル / 手順） | **関係ないもの（疑わない）** | 確定遷移（報告内容） |
|---|---|---|---|---|
| `20`–`21` | `現在のAGENTS.md全文の読込を確認できません` | `AGENTS.md` 更新またはセッション開始時の記録欠落 | Git リモート・`push_gate.py` | `100` → `990 STOP`（`F1` → `Developer: Reload Window` を案内） |
| `22`–`23` | `hook入力を検証できません` 等 | Hook ペイロードまたはシェル文字列の形式不正 | リモート障害・ブランチ先間違い | `110` → `990 STOP`（コマンド文字列を報告） |
| `24` | `...は実行しません（AGENTS.md §7）` | force / 履歴改変 / フック回避 / remote ref 削除の試行 | リモート障害・Reload Window | `300` → `990 STOP`（利用者管理の手順へ返す） |
| `25`–`26` | `PLAN_REQUIRED` / `git pushは直接実行しません` | 素の `git push` を実行し `NRA_PUSH_PLAN` が未設定 | リモート（GitHub）障害・Reload Window・ブランチ先間違い | `200` → `990 STOP`（次ターンで `python -B scripts/push.py prepare`） |
| `27`–`28` | `STOP <send_state>` / その他の `reason` | `prepare` 後の変更・incoming あり・ゲート不一致・通信中断 | Reload Window | `210` → `990 STOP`（`UNKNOWN`/`UNVERIFIED` は再送禁止、`result.json` 報告） |
| `29`–`30` | `error:` / `FAIL` / `UNAVAILABLE` / 終了コード `!= 0` | 検証スクリプト不一致またはコマンド失敗（`;` 連結時の終了コード `0` を含む） | — | `400` → `990 STOP`（該当箇所を報告し承認待ち） |
| `31` | `nra_depth_guard` 停止 | 多段探索の深度上限到達 | — | `500` → `990 STOP`（探索ループ終了） |
