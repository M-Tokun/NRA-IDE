---
id: GUIDE-PUSH-PROCEDURE-20261105
kind: guide
created: 2026-11-05
author: M-Tokuni
title: "push 手順書（Cline・全AI共通）"
---

# push 手順書（Cline・全AI共通）

**読むのは、push が失敗したときだけ。** 通常は読まない（時間とトークンを使うため）。

対象: NRA-IDE リポジトリで `git push` を行うAIエージェント（特にCline）。
上位規則は `AGENTS.md` §6・§7 と `RULES_DETAIL.md` 300〜370。この文書は、その規則を満たしたうえで
**`scripts/push.py` を入口とする固定経路と、失敗時の確認方法**を書く。規則を緩める文書ではない。

---

## 0. 先に知っておくこと

1. `.githooks/pre-push` が有効な環境では、`git push` はこのフックから `scripts/push_gate.py check` を通る。入口の利用だけでフック設定の有効性を保証するものではない。
2. このゲートは、送信する ref 更新がある場合、**plan ファイルが無いと拒否する**（`PLAN_REQUIRED`）。
   plan なしの拒否は設計上の停止である。送信更新が無い場合は `NO_REF_UPDATES` と区別する。
3. plan は**実行許可ではない**（`is_execution_permission: false`）。利用者の push 確認の代わりにならない。
4. フックを回避しない。次は行わない（`AGENTS.md` §6・§7で禁止）。`git config --show-origin --get core.hooksPath` は読取であり、設定変更とは区別する。読取の通過は自動承認ではなく、ホストの通常の権限確認へ戻る。
   - `git push --no-verify`
   - `git config core.hooksPath ...` などフック設定の変更
   - force / `--force-with-lease` / 先頭`+`付き refspec / remote ref の削除
5. 必要な環境: `python`（PATH上）と `pwsh`（PowerShell 7）。malware/unicode 検査が `pwsh` を使う。
6. **出力を短くする（トークン節約）**。Cline のターミナルでは git が進捗を1%ごとに1行出す（`Counting objects: 1% (4/375)` など）。
   1回の fetch/push で数百行（数万文字）になり、AIの文脈に全部入って、API呼び出しのたびに再送される。
   - 入口スクリプトが fetch に `--quiet`、push に `--no-progress` を付ける。
   - 読取コマンドは `;` でつなげて1回で実行し、1コマンドずつ繰り返さない。
   - 出力が崩れた・空だったときは、同じコマンドを繰り返さず、ログファイルが指されていれば末尾だけ読む（Cline: `proceed-while-running-*.log` の `tail` 相当。全文を読まない）。
   - フックの結果 JSON が長いときは、`status` と `reason` と各ゲートの `status` だけを読む。全文は `local_reports/push_gate/<ID>/result.json` にある。

---

## 1. 手順（入口を統一する）

前提: 変更は commit 済みで、`git status` と差分から今回の対象と既存変更を区別できていること。
作業はリポジトリルートで行う。手作業の plan 作成や直接の `git push` を代替経路にしない。
以下の番号は `scripts/push.py` の経路番号である。

```text
10 PLAN: push.py prepare（fresh fetch・送信範囲確認・plan作成）
   IF STOP: GOTO 90
   ELSE: GOTO 20
20 ASK: 送信先・branch・HEAD・全送信commit・incoming・planを提示して応答終了。未回答は待機
   IF 直後の利用者入力 = git push（前後空白を除いて完全一致）: GOTO 30
   ELSE: push.py decline。GOTO 90
30 PUSH: push.py run（plan指定・ゲート検査・通常push）
   IF STOP: GOTO 90
   ELSE: GOTO 40
40 VERIFY: runが再fetch・送信先OID・HEAD・双方向差分を照合
   IF STOP: GOTO 90
   ELSE: GOTO 50
50 DONE: 最終行 DONE を報告して終了
90 STOP: 最終行 STOP <send_state> を報告して終了。自動で10へ戻らない
```

### 手順1 準備と提示（10 → 20）

`origin/master` を対象とする例:

```text
python -B scripts/push.py prepare --remote origin --branch master
```

- `--branch` は `master` のような branch 名。送信先を変える場合は、確認済みの remote と branch を prepare に指定する。
- fresh fetch、incoming の確認、古い順の全送信 commit の算出、長すぎるパスの確認、固有名の plan 作成を入口が行う。incoming があれば停止し、merge / rebase / cherry-pick を自動で行わない。
- 最終行が `ASK` になったら、出力の送信先・branch・完全な HEAD OID・全送信 commit・incoming・plan を提示する。今回対象外の commit があれば `push.py decline` で停止し、AGENTS.md §7の「4: 選択外」として報告する。
- **提示した応答を終了し、利用者の返答を待つ。同じ応答内で run を実行しない。**

### 手順2 利用者入力の分岐（20）

- 提示の直後の入力が、前後空白を除き **`git push` と完全一致**した場合だけ手順3へ進む。
- 「pushして」「進めて」「commitまで」など、それ以外の入力では次を実行し、`STOP NOT_STARTED`（記録の step は 20）で停止する。未回答の間は待機し、承認へ読み替えない。

```text
python -B scripts/push.py decline
```

この入力条件の確認はAIが行う。入口・plan・ゲートは利用者の確認記録を機械的に照合する実装ではなく、その機械化は未実装である。

### 手順3 送信と送信後照合（30 → 40 → 50）

```text
python -B scripts/push.py run
```

- 保存済みの remote・branch・plan を使う。`NRA_PUSH_PLAN` の設定と通常 push、送信後の再 fetch と照合は run が行う。
- prepare から run までの間に追加の fetch・commit・規則変更を行い、plan を無効化した場合も停止する。自動で prepare をやり直さない。
- ゲートは unicode / malware / id / dictionary / fileop（正本は scripts/push_gate.py の GATES）。待機時間は入口の `TIMEOUT` と `PREPARE_TIMEOUT_SECONDS` に定義されている。各値は実測による確定前の設定値であり、失敗時に独自に緩和しない。
- 最終行が `DONE` のときだけ完了と報告する。これは送信先 OID が準備時の HEAD と一致し、送信先と現在の HEAD の双方向差分が `0 0` になった結果である。
- 報告には最終行、push 前後の OID、result.json に記録された各ゲートの名前と結果を使う。詳細は次節の記録から確認する。

---

## 2. 失敗したとき（`reason` の読み方）

入口の最終行は `STOP <send_state>`、その直前の行は `reason: <reason>`。止まった場所は `local_reports/push_gate/push_route_log.jsonl` の `step`、原因は `reason` を確認する。最終行に経路番号は出さない。ゲートまで進んだ場合の詳細は `local_reports/push_gate/<ID>/result.json` に残る。

記録の step 30 の TIMEOUT・判定なしの失敗は `STOP UNKNOWN`（送信したか不明）、step 40 は `STOP COMMAND_SUCCEEDED_UNVERIFIED`（push コマンド成功・一致未確認）として扱う。送信していないと決め付けて再実行しない。
以下の対処は原因確認のための案内であり、自動再試行の指示ではない。停止後は原因と影響を報告し、利用者の新しい入力を受けてから prepare で再開する。新しい提示後の push 確認も省略しない。

| reason | 意味 | 対処 |
|---|---|---|
| `PLAN_REQUIRED` | `NRA_PUSH_PLAN` が未設定 | 入口を経由していたか確認。手作業で環境変数を補い直接 push しない |
| `PLAN_OR_RULES_CHANGED` | plan 作成後に HEAD・fetch・規則ファイル（AGENTS.md、ゲートのスクリプト等）が変わった | 変更を確認して停止。新しい入力後に入口で再準備 |
| `UPDATE_DIFFERS_FROM_PLAN` | push しようとしている branch/commit が plan と違う | 提示した送信先と対象範囲を確認し、停止 |
| `DESTINATION_DIFFERS_FROM_PLAN` | push 先 URL が plan と違う | remote 名・URL を確認。変更が必要なら利用者に返す |
| `INCOMING_COMMITS_PRESENT` | remote 側に手元に無い commit がある | 停止して利用者へ報告（自動で統合しない） |
| `FETCH_EVIDENCE_MISSING` | fetch の記録に remote の現在位置が無い | 取得状態を報告して停止。新しい入力後の prepare に fresh fetch を任せる |
| `PREPARATION_FAILED`（prepare 時） | plan の出力先が既存、パスがリポジトリ外、remote 名不正など | ルートでの実行、送信先、書込可否を確認。手作業の plan 作成へ切り替えない |
| `SINGLE_REF_REQUIRED` | 1回の push で複数 ref を送ろうとした | 入口と対象 branch を確認して停止（`--all`・`--tags` は使わない） |
| `SOURCE_MUST_EQUAL_HEAD` | HEAD 以外の commit を送ろうとした | 現在 branch の HEAD を送る |
| `MALWARE_OR_UNICODE_BLOCKED` | malware または unicode 検査が失敗、または検査を実行できなかった（`result.json` の `malware.status` が `UNAVAILABLE`、`reason` が `DEFENDER_ENVIRONMENT_ERROR`・`DEFENDER_NONZERO_AMBIGUOUS` など） | `result.json` の findings または `malware.reason` を読み、利用者へ報告。検出がないのに UNAVAILABLE の場合は Defender の環境を疑う（2026-11-19 の Platform\Temp 誤選択の例）。無視して再実行しない |
| `ID_BLOCKED` / `DICTIONARY_BLOCKED` / `FILEOP_BLOCKED` | ID ゲート / 辞書ゲート / ファイル操作報告ゲートが失敗 | 同上。findings を報告し、修正は利用者の承認後 |
| `GATE_TIMEOUT` | ゲートが plan の上限時間内に終わらなかった | 一時出力と経過を報告して停止。上限調整は別途相談し、独自に大きくして再実行しない |
| `NOTHING_TO_SEND` | step 10・NOT_STARTED。送信する commit がない | 送信対象の commit の有無を報告 |
| `PATH_TOO_LONG` | step 10・NOT_STARTED。名前が255バイト超、またはパスが200文字超。記録の `detail` にパス | 該当パスを報告。改名は利用者の承認後 |
| `DIFF_FAILED` | step 10・NOT_STARTED。パス長検査の `git diff` が失敗 | 出力末尾を報告 |
| `NO_CURRENT_BRANCH` | step 10・NOT_STARTED。現在の branch を取得できない（detached HEAD など） | branch の状態を報告 |
| `FETCH_FAILED` | step 10（NOT_STARTED）または step 40（COMMAND_SUCCEEDED_UNVERIFIED）。fetch の失敗 | step 40 は送信済みの可能性があるので再送しない |
| `TIMEOUT` | step 10（NOT_STARTED）・30（UNKNOWN）・40（COMMAND_SUCCEEDED_UNVERIFIED）。入口の `TIMEOUT` を超過 | 30・40 は再送しない。上限の緩和は相談事項 |
| `DECLINED` | step 20・NOT_STARTED。提示の直後の入力が `git push` 以外 | 次の入力で prepare からやり直す |
| `NO_PREPARED_PLAN` | step 30・NOT_STARTED。prepare を経ていない、または停止後に run した | prepare からやり直す |
| `PUSH_FAILED` | step 30・UNKNOWN。push が失敗し、ゲートの判定もない | 送信の有無が不明なので再送しない |
| `MISMATCH` | step 40・COMMAND_SUCCEEDED_UNVERIFIED。送信後の照合で送信先 OID または差分が不一致 | 再送しない。照合結果を報告 |
| `OBSERVE_FAILED` | step 40・COMMAND_SUCCEEDED_UNVERIFIED。照合用の `rev-parse`/`rev-list` が失敗 | 再送しない |
| 上記以外 | `push_gate.py` の内部検査（`INVALID_*`・`GIT_OBSERVATION_FAILED`・`GATE_INPUT_OR_EXECUTION_ERROR`・`INTERRUPTED` など） | 意味を推測せず、reason の文字列と `result.json` をそのまま報告する |
| `non-fast-forward or unresolved remote base` | 履歴が分岐している | 通常 push では扱わない。利用者管理の手順へ返す |
| `remote ref deletion is blocked` | remote branch の削除 | 実行しない |
| `new branch requires a fetched remote default branch` | 新規 branch で `origin/HEAD` が無い | prepare の fresh fetch 後の不足として利用者へ報告 |

`status` が `UNAVAILABLE` でも、`unicode`/`malware` などが `NOT_RUN` と表示されることがある。これは**ゲートの手前（plan 検証）で止まった**という意味で、検査が通ったわけではない。

---

## 3. 新規 branch の push（補足）

remote に同名 branch が無い場合、`remote_oid` は全て `0` になり、送信範囲は「remote 既定 branch との merge-base..HEAD」になる。
手順は同じだが、`refs/remotes/origin/HEAD` が必要。merge-base を確定できない場合は push しない（`RULES_DETAIL.md`）。

---

## 4. やってはいけないことの早見表

- plan なしで push して、失敗したからといってフックを迂回する。
- 入口を使わず、手作業の plan と直接 push で送信する。
- 利用者の返答前に push する（手順1の提示で止まる）。
- plan 作成後に `git fetch` / commit / 編集をして、そのまま push する。
- 失敗の原因を調べず、同じ plan で繰り返す。
- ゲートの findings を無視する、または対象ファイルを黙って修正して再実行する。
- 作成済みの plan や `local_reports/` の記録を、確認なしに削除する。

---

## 5. 根拠

| 内容 | 参照 |
|---|---|
| push は個別確認が必要な操作 | `AGENTS.md` §6 |
| fresh fetch、incoming 時は停止、force 禁止 | `AGENTS.md` §7、`RULES_DETAIL.md` 300〜370 |
| plan の仕様（実行許可ではない、1 ref のみ、再検証） | `scripts/push_gate.py` の `prepare`・`check`・`unchanged` |
| 固定入口、利用者入力の分岐、停止・完了の語彙、送信後照合 | `scripts/push.py`、`RULES_DETAIL.md` 20・360・370 |
| フック本体 | `.githooks/pre-push` |
