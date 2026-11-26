# prompt-gate — 合言葉の機械判定

AGENTS.md §7「合言葉の完全一致」の機械側。利用者の入力を受け取る hook が、合言葉（`git push`・`commit まで`）との完全一致を判定し、1回限りの承認ファイルを書く。AI は判定せず、承認を作らない。承認を使うのは `scripts/push.py run` と `scripts/commit.py run`。

設計の理由：`local_reports/route_design_20261126/RATIONALE.md`（git 管理外。要旨は下の「前提」と「限界」）。

## ファイル

| ファイル | 役割 |
|---|---|
| `_prompt_gate.py` | 共通判定（経路 10〜99）。`decide()` は副作用なし、`apply()` が承認の書込み・消去と decline を行う |
| `claude_prompt_gate.py` | Claude Code の UserPromptSubmit hook のラッパー |
| `../../scripts/approval.py` | 承認ファイルの書込み・消費（1回限り）・消去 |

承認ファイル：`.agent_state/approvals/push.json`・`commit.json`（git 管理外）。

## 注入する文脈

| 語 | 条件 | AI の動き |
|---|---|---|
| PUSH_RUN | 「git push」かつ push 計画が保留中 | AGENTS.md 55：push.py run |
| PUSH_PREPARE | 「git push」で計画なし | AGENTS.md 57：push.py prepare |
| COMMIT_RUN | 「commit まで」（間の空白は1個か無し） | AGENTS.md 58・59 |
| NOT_EXACT | commit・push を含む不一致 | 「完全一致していません」と返し、実行しない |
| PUSH_DECLINED | 計画が保留中で、git push 以外の入力 | 計画は取り消し済み |

AI が文脈を読み違えても、承認がなければ push.py・commit.py は STOP する。

## 前提（各ホストで確かめること）

1. 入力が AI に渡る前に、入力の原文を受け取る hook がある。
2. その hook がファイルを書き、AI の文脈へ文を注入できる。
3. ツール実行の前に、`.agent_state/approvals/` への AI の書込みを拒否できる。
4. セッション開始時に動く hook がある（保留中の計画・承認を消す）。

Claude Code 以外のホストは未確認。対応する hook がなければ承認は作られず、push・commit は止まる（安全側）。

## 限界

- 承認ファイルはリポジトリ内のファイルで、OS の境界ではない。スクリプト経由の書込みは文字列ガードで見えない。
- 登録（settings の hooks）は P-ORDER 30 で行う。登録前は何も動かない。
