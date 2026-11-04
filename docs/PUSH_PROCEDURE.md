# push 手順書（Cline・全AI共通）

対象: NRA-IDE リポジトリで `git push` を行うAIエージェント（特にCline）。
上位規則は `AGENTS.md` §6・§7 と `RULES_DETAIL.md`「通常のGit操作」。この文書は、その規則を満たしたうえで
**pre-push フックを通すための実行手順**だけを書く。規則を緩める文書ではない。

---

## 0. 先に知っておくこと

1. `git push` は `.githooks/pre-push` → `scripts/push_gate.py check` を必ず通る。
2. このゲートは **確認済みの plan ファイルが無いと必ず拒否する**（`PLAN_REQUIRED`）。
   「何も渡さずに `git push`」は、設計上、必ず失敗する。壊れているのではない。
3. plan は**実行許可ではない**（`is_execution_permission: false`）。利用者の push 確認の代わりにならない。
4. フックを回避しない。次は行わない（`AGENTS.md` §6・§7で禁止。Claudeの環境では `git config core.hooksPath` が実行前に拒否されることを確認済み）。
   - `git push --no-verify`
   - `git config core.hooksPath ...` などフック設定の変更
   - force / `--force-with-lease` / 先頭`+`付き refspec / remote ref の削除
5. 必要な環境: `python`（PATH上）と `pwsh`（PowerShell 7）。malware/unicode 検査が `pwsh` を使う。

---

## 1. 手順（この順番を崩さない）

前提: 変更は commit 済みで、`git status` が今回の対象だけ（または clean）であること。

### 手順1 fresh fetch
```text
git fetch origin
```
- **plan 作成の直前**に行う。fetch の記録（`.git/FETCH_HEAD`）が plan に焼き込まれるため、
  plan 作成後にもう一度 fetch すると plan が無効になる（手順5の注意参照）。

### 手順2 送信範囲の確認（読取のみ）
```text
git rev-parse HEAD
git branch -vv
git log --oneline origin/master..HEAD
git log --oneline HEAD..origin/master
```
- 1つ目: 送信する HEAD の commit ID。
- 3つ目（outgoing）: 送信される全 commit。今回対象外の commit が混ざっていたら **push しない**（`RULES_DETAIL.md` の専用 branch 手順へ）。
- 4つ目（incoming）: **1件でもあれば停止**し、利用者へ報告する。merge / rebase / cherry-pick を自動で行わない。

### 手順3 plan を作る
リポジトリルートで実行する。

```text
python -B scripts/push_gate.py prepare --remote origin --branch refs/heads/master --output local_reports/push_gate/plan_YYYYMMDD.json --timeout-seconds 180
```
- `--branch` は `refs/heads/...` の完全名。master 以外へ push するときは対象 branch 名に変える。
- `--output` はリポジトリ内のパスのみ可。`local_reports/push_gate/` は Git 管理外なので commit に混ざらない。
- **同名ファイルは上書きされず失敗する**（`PREPARATION_FAILED`）。やり直すときは日付に連番を付けるなど別名にする（例: `plan_20261105_2.json`）。古い plan は削除せず、そのままにする（削除は利用者確認が必要な操作）。
- `--timeout-seconds` は必須。目安は 180。各ゲートに適用される。
- 出力 JSON の `context` を読み、次が手順2と一致することを確認する。
  `remote_oid`（= 現在の `origin/master`）、`source_oid`（= HEAD）、`outgoing`（= 送信 commit 一覧）。

### 手順4 利用者に push 確認を取る（ここで停止）
次の形式で提示し、**同じ応答内では push を実行せず、利用者の返答を待つ**。

```text
origin/master: {HEAD の commit ID 先頭7桁}…{送信 commit 件数}件を通常 push（force なし）
送信 commit: {commit ID} {題名} （全件）
incoming: なし
plan: local_reports/push_gate/plan_YYYYMMDD.json
```
- 「進めて」「commit まで」などの包括的な指示は push 確認ではない（`AGENTS.md` §6）。
- 利用者が「push して」と返したら手順5へ。

### 手順5 plan を指定して push
plan のパスを環境変数 `NRA_PUSH_PLAN` で渡す。

bash / Git Bash:
```text
NRA_PUSH_PLAN=local_reports/push_gate/plan_YYYYMMDD.json git push origin master
```
PowerShell:
```text
$env:NRA_PUSH_PLAN = "local_reports/push_gate/plan_YYYYMMDD.json"
git push origin master
Remove-Item Env:NRA_PUSH_PLAN
```
- 手順3〜5の間に **`git fetch`・commit・ファイル編集をしない**。HEAD・fetch 記録・規則ファイルのどれかが変わると plan が無効になる（`PLAN_OR_RULES_CHANGED`）。その場合は手順1からやり直す。
- フックは unicode / malware / id / dictionary の4ゲートを順に実行する。数十秒〜数分かかることがある。タイムアウトを短く設定したツールから呼ぶ場合は、180秒以上待てるようにする。
- 成功時は末尾に `11304d6..964b8e5  master -> master` のような行が出る。

### 手順6 push 後の確認
```text
git fetch origin
git rev-list --left-right --count origin/master...HEAD
git rev-parse origin/master HEAD
```
- `0	0` が出て、2つの commit ID が一致すれば成功（`RULES_DETAIL.md` の成功条件）。
- 報告には、push 前後の commit ID、4ゲートの結果、確認した事項を書く。

---

## 2. 失敗したとき（`reason` の読み方）

フックは JSON を出力し、`"reason"` に原因を書く。ゲートごとの詳細は `local_reports/push_gate/<ID>/result.json` にも残る。

| reason | 意味 | 対処 |
|---|---|---|
| `PLAN_REQUIRED` | `NRA_PUSH_PLAN` が未設定 | 手順3→5。環境変数の綴りと設定忘れを確認 |
| `PLAN_OR_RULES_CHANGED` | plan 作成後に HEAD・fetch・規則ファイル（AGENTS.md、ゲートのスクリプト等）が変わった | 手順1からやり直し（別名の plan を作る） |
| `UPDATE_DIFFERS_FROM_PLAN` | push しようとしている branch/commit が plan と違う | `git push origin <branch>` の指定と plan の `--branch` を揃える |
| `DESTINATION_DIFFERS_FROM_PLAN` | push 先 URL が plan と違う | remote 名・URL を確認。変更が必要なら利用者に返す |
| `INCOMING_COMMITS_PRESENT` | remote 側に手元に無い commit がある | 停止して利用者へ報告（自動で統合しない） |
| `FETCH_EVIDENCE_MISSING` | fetch の記録に remote の現在位置が無い | 手順1の `git fetch origin` をやり直してから手順3 |
| `PREPARATION_FAILED`（prepare 時） | plan の出力先が既存、パスがリポジトリ外、remote 名不正など | 別名の `--output`、ルートでの実行、`--remote`/`--branch` を確認 |
| `SINGLE_REF_REQUIRED` | 1回の push で複数 ref を送ろうとした | branch を1つずつ push する（`--all`・`--tags` は使わない） |
| `SOURCE_MUST_EQUAL_HEAD` | HEAD 以外の commit を送ろうとした | 現在 branch の HEAD を送る |
| `MALWARE_OR_UNICODE_BLOCKED` | malware または unicode 検査が失敗 | `result.json` の findings を読み、該当ファイルを利用者へ報告。無視して再実行しない |
| `ID_BLOCKED` / `DICTIONARY_BLOCKED` | ID ゲート / 辞書ゲートが失敗 | 同上。findings を報告し、修正は利用者の承認後 |
| `GATE_TIMEOUT` | ゲートが `--timeout-seconds` 内に終わらなかった | 一時出力が残る場合があるので報告。timeout を大きくした別名 plan で再実行 |
| `non-fast-forward or unresolved remote base` | 履歴が分岐している | 通常 push では扱わない。利用者管理の手順へ返す |
| `remote ref deletion is blocked` | remote branch の削除 | 実行しない |
| `new branch requires a fetched remote default branch` | 新規 branch で `origin/HEAD` が無い | `git fetch origin` 後も出る場合は利用者へ報告 |

`status` が `UNAVAILABLE` でも、`unicode`/`malware` などが `NOT_RUN` と表示されることがある。これは**ゲートの手前（plan 検証）で止まった**という意味で、検査が通ったわけではない。

---

## 3. 新規 branch の push（補足）

remote に同名 branch が無い場合、`remote_oid` は全て `0` になり、送信範囲は「remote 既定 branch との merge-base..HEAD」になる。
手順は同じだが、`refs/remotes/origin/HEAD` が必要。merge-base を確定できない場合は push しない（`RULES_DETAIL.md`）。

---

## 4. やってはいけないことの早見表

- plan なしで push して、失敗したからといってフックを迂回する。
- 利用者の返答前に push する（手順4で止まる）。
- plan 作成後に `git fetch` / commit / 編集をして、そのまま push する。
- 失敗の原因を調べず、同じ plan で繰り返す。
- ゲートの findings を無視する、または対象ファイルを黙って修正して再実行する。
- 作成済みの plan や `local_reports/` の記録を、確認なしに削除する。

---

## 5. 根拠

| 内容 | 参照 |
|---|---|
| push は個別確認が必要な操作 | `AGENTS.md` §6 |
| fresh fetch、incoming 時は停止、force 禁止 | `AGENTS.md` §7、`RULES_DETAIL.md`「通常のGit操作」 |
| plan の仕様（実行許可ではない、1 ref のみ、再検証） | `scripts/push_gate.py` の `prepare`・`check`・`unchanged` |
| フック本体 | `.githooks/pre-push` |
