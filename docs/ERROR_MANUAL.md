# ERROR_MANUAL — エラー分岐・対処マニュアル（オンデマンド専用）

**読む条件：コマンド・Git・Hook・検証スクリプトがエラー（非0終了・拒否メッセージ・`STOP`）を返したときだけ読む。**
平常時は読まない（`AGENTS.md` の肥大化および第1段階での不要な推論・トークン消費を防ぐため）。

上位規則は `AGENTS.md`（特に §6・§7・§8・§11）および `RULES_DETAIL.md`（特に `C1`〜`C7`・`700`）。本書は、エラー発生時の経路選択を固定するための確定ルックアップ表であり、上位規則の承認や禁止事項を緩和しない。

---

## 1. 呼び出し元との経路結線仕様（88 BASIC 形式）

経路の分岐行では抽象語（「必要な」「適切な」「状況により」「必要に応じて」）を禁止し、**観測できる事実（トリガー）**・**固定ファイル名（遷移先）**・**戻り語（`DONE` / `ASK` / `STOP`）** の3要素だけを結合する。

```text
原則: IF <観測事実> : GOSUB docs/ERROR_MANUAL.md (戻り: DONE / ASK / STOP)
```

### 呼び出し元への最小結線パターン

`AGENTS.md` や `RULES_DETAIL.md` にエラー原因ごとの分岐を書かず、次の固定結線のみを置く。

1. **`AGENTS.md` 側（経路 `60`〜`95` 間への結線例）**:
   ```text
   65 IF 実行結果 == ERROR OR 終了コード != 0 OR Hook拒否:
         GOSUB docs/ERROR_MANUAL.md (戻り: DONE / ASK / STOP)
         IF 戻り=ASK OR 戻り=STOP: GOTO 95
         ELSE: GOTO 70
   ```
   ※ `AGENTS.md` 側には原因別分岐を持たせず、エラー時のみ本書へ渡す（第1段階の推論発生を遮断する）。

2. **`RULES_DETAIL.md` 側（経路 `700` への結線例）**:
   ```text
   700 成功と報告しない。GOSUB docs/ERROR_MANUAL.md ; §7
       IF 戻り=ASK GOTO 998 ELSE GOTO 990
   ```

---

## 2. ERROR_MANUAL 本体経路（`10`〜`999`）

```text
#ROUTE ERROR_MANUAL v1 ; 番号はこのブロック内だけ（AGENTS.md / RULES_DETAIL.md / push.py の番号とは別）
#RETURN 990=STOP 998=ASK 999=DONE ; 呼び出し元へは語だけを返す
#CONST ; 全経路で常に成立。破れたら 990
E1 推測による回避実行（--no-verify・フック設定変更・NRA_PUSH_PLAN 手動注入・force-push）を禁止する
E2 同じ失敗コマンドを原因変更なしに反復しない
E3 未確認のまま完了・成功へ読み替えない
#END-CONST

10  観測事実の固定：実行コマンド・終了コード・標準出力/標準エラー末尾・JSON の status / reason / send_state を確定する。GOTO 20

20  観測文字列による1対1分岐（推論で選ばない）：
    IF 出力に "現在のAGENTS.md全文の読込を確認できません" OR "AGENTS.mdが存在しないか" GOTO 100
    | 出力に "hook入力を検証できません" OR "シェルコマンドを文字列として確認できません" GOTO 110
    | 出力に "git pushは直接実行しません" OR reason="PLAN_REQUIRED" GOTO 200
    | push.py 最終行="STOP ..." OR push_gate.py の reason あり GOTO 210
    | 出力に "は実行しません（AGENTS.md §7）" GOTO 300
    | 検証スクリプト（verify_repo / check_dictionary / id_gate / unicode_gate / malware_gate / check_links / check_path_case）が非0 GOTO 400
    | nra_depth_guard 停止 GOTO 500
    ELSE GOTO 900

100 セッション読込記録不一致（agents-md-guard 停止）：
    AGENTS.md の再読取では記録は戻らない。
    VS Code / IDE で F1 →「Developer: Reload Window（ウィンドウの再読み込み）」が必要であることを報告する。
    （注：Reload Window が必要な唯一のケース。push の PLAN_REQUIRED とは無関係）
    GOTO 990

110 Hook 入力・構文不正（agents-md-guard 停止）：
    実行しようとしたコマンド文字列と hook の拒否メッセージをそのまま報告し、無理に分割・言い換え再試行しない。
    GOTO 990

200 push 固定入口未経由 / PLAN_REQUIRED（素の git push による停止）：
    リモート障害・ブランチ間違い・Reload Window の問題ではない（ローカル .githooks/pre-push → push_gate.py が plan 未指定で停止）。
    素の git push をやめ、対象確認済みなら python -B scripts/push.py prepare を実行する。
    IF prepare の最終行 == "STOP ..." GOTO 210
    ELSE 送信先・HEAD・送信先現在位置・全送信コミット・incoming=0・plan を提示し GOTO 998

210 push 経路・4ゲート停止（scripts/push.py / scripts/push_gate.py 停止）：
    詳細は docs/PUSH_PROCEDURE.md §2 を参照する。
    IF send_state == "UNKNOWN" OR send_state == "COMMAND_SUCCEEDED_UNVERIFIED":
       再送禁止。stop した step・reason・send_state を報告する。GOTO 990
    ELSE (PLAN_OR_RULES_CHANGED / UPDATE_DIFFERS_FROM_PLAN / INCOMING_COMMITS_PRESENT /
          MALWARE_OR_UNICODE_BLOCKED / ID_BLOCKED / DICTIONARY_BLOCKED / GATE_TIMEOUT 等):
       自動再試行・自動 merge/rebase・独自タイムアウト緩和・無断修正を行わず、
       reason・send_state・該当ファイル（local_reports/push_gate/<ID>/result.json）を報告する。GOTO 990

300 禁止 Git 操作ブロック（履歴改変・強制送信・remote ref 削除）：
    AI 経路では実行しない（AGENTS.md §7 / RULES_DETAIL.md C3）。
    対象 OID・影響範囲・拒否メッセージを提示して利用者管理の手順へ返す。GOTO 990

400 リポジトリ検証・ゲート失敗（verify_repo / check_dictionary / id_gate / unicode_gate / malware_gate / check_links / check_path_case）：
    該当ファイル・行番号・規則名（例：DICT-* / BOM / CRLF / KaTeX）を観測事実として列挙する。
    利用者記述・既存資産を無断修正せず、修正案と影響を提示して承認を待つ。GOTO 990

500 探索深度ガード上限（nra-depth-guard 停止）：
    探索ループを即時停止する。ここまでの観測結果・確定事実・未確認範囲を報告する。GOTO 990

900 未登録エラー（20 の既知パターンに該当しない失敗）：
    推測による別ルート試行や回避を行わない。
    実行コマンド・終了コード・出力末尾・未確定事項のみを提示する。GOTO 990

990 STOP：不足・停止理由・send_state・必要な承認/操作をまとめ、呼び出し元へ STOP を返す
998 ASK：push 実行確認（直後の入力が git push 完全一致なら run へ）を待ち、呼び出し元へ ASK を返す
999 END：呼び出し元へ DONE を返す
```

---

## 3. 切り分け早見表（何が原因で、何が原因でないか）

エラー発生時に「どこを疑うべきか」で迷わないための切り分け表。

| 観測されたエラー・停止 | 真の原因（ローカル / 手順） | **関係ないもの（疑わない）** | 次の一手（確定遷移） |
|---|---|---|---|
| `PLAN_REQUIRED`（`push_gate.py`） | ローカル `.githooks/pre-push` が `NRA_PUSH_PLAN` 未設定を検出 | リモート（GitHub）障害・Reload Window・ブランチ先間違い | `python -B scripts/push.py prepare`（`200`） |
| `git pushは直接実行しません` | `agents-md-guard` が素の `git push` をブロック | リモート障害・Reload Window・ブランチ先間違い | `python -B scripts/push.py prepare`（`200`） |
| `現在のAGENTS.md全文の読込を確認できません` | `AGENTS.md` 更新またはセッション開始時の記録欠落 | Git リモート・`push_gate.py` | VS Code `F1` → `Developer: Reload Window`（`100`） |
| `PLAN_OR_RULES_CHANGED` / `UPDATE_DIFFERS_FROM_PLAN` | `prepare` 後に commit・fetch・規則ファイル変更が発生 | Reload Window・GitHub 障害 | 停止報告し、利用者の新入力後に `prepare` やり直し（`210`） |
| `INCOMING_COMMITS_PRESENT` | リモートに手元へ未反映の commit がある | フック不具合・Reload Window | merge/rebase せず停止報告（`210`） |
| `MALWARE_OR_UNICODE_BLOCKED` / `ID_BLOCKED` / `DICTIONARY_BLOCKED` | 送信範囲内のファイルにゲート検査違反あり | リモート障害・ブランチ先間違い | `result.json` の該当箇所を報告し承認待ち（`210` / `400`） |
