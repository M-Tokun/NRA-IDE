# prompt-gate — 合言葉の機械判定

AGENTS.md §7「合言葉の完全一致」の機械側。利用者の入力を受け取る hook が、合言葉（`git push`・`commit まで`）との完全一致を判定し、1回限りの承認ファイルを書く。AI は判定せず、承認を作らない。承認を使うのは `scripts/push.py run` と `scripts/commit.py run`。

設計の理由：`local_reports/route_design_20261126/RATIONALE.md`（git 管理外。要旨は下の「前提」と「限界」）。

## ファイル

| ファイル | 役割 |
|---|---|
| `_prompt_gate.py` | 共通判定（経路 10〜99）。`decide()` は副作用なし、`apply()` が承認の書込み・消去と decline を行う |
| `claude_prompt_gate.py` | Claude Code の UserPromptSubmit hook のラッパー |
| `cline_prompt_gate.py` | Cline の UserPromptSubmit hook のラッパー（`.clinerules/hooks/UserPromptSubmit.ps1` が呼ぶ）。入力は平坦 `{"prompt"}` と入れ子 `{"userPromptSubmit":{"prompt"}}` の両方を受ける。解釈できなければ承認を消し errorMessage で知らせる |
| `gemini_prompt_gate.py` | Gemini CLI の BeforeAgent hook のラッパー（`.gemini/settings.json` の `hooks.BeforeAgent` が呼ぶ）。`{"prompt"}` を受け、注入文脈は `hookSpecificOutput.additionalContext`（`hookEventName: "BeforeAgent"`）、該当なし・解釈不能時は `{}` を返す |
| `antigravity_prompt_gate.py` | Antigravity IDE の PreInvocation hook のラッパー（`.agents/hooks.json` の `nra-prompt-gate.PreInvocation` が呼ぶ）。`invocationNum == 0` のときだけ `lastUserInput` を判定し、注入文脈は `injectSteps.systemMessage`、該当なし・再呼び出し・解釈不能時は `{}` を返す |
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

Cline（2026-11-26 追加、2026-11-27 実機で確認）：Cline で commit・push が `NO_APPROVAL` で止まった原因は2つ。(1) hook が未登録だった。(2) Cline は入力を `<user_input mode="act">…</user_input>`（Plan では `mode="plan"`）で包んで渡すため、完全一致しなかった。
- 確認済み：`UserPromptSubmit.ps1` は Cline 4.1.22 で発火する。入力は入れ子 `{"userPromptSubmit":{"prompt"}}`。
- 対処：`cline_prompt_gate.py` が、全体がこの包みの形のときだけ中身を取り出して判定する。それ以外は手を加えない。
- 未確認：contextModification の注入が AI に届くか。承認の書込みとは別。
- 記録：発火ごとに `.agent_state/hooks/prompt_gate_cline.jsonl`（入力のキー構造・文字数・判定。本文は記録しない）と `prompt_gate_cline_ps1.log`（呼出し時刻）に追記する。
前提3（承認への AI の書込み拒否）と前提4（セッション開始時の消去）は、既存の agents-md-guard（Cline の PreToolUse・TaskStart）が担う。

Gemini CLI（2026-11-27 追加、実機は未確認）：`.gemini/settings.json` の `hooks.BeforeAgent`（`matcher: "*"`）から `gemini_prompt_gate.py` を呼ぶ。
- 記録：発火ごとに `.agent_state/hooks/prompt_gate_gemini.jsonl`（入力のキー構造・文字数・判定結果。本文は記録しない）に追記する。
- 未確認：Gemini CLI 実機での `BeforeAgent` 発火、stdin JSON の `prompt` キー・包みタグ有無、`additionalContext` の到達。
- 前提3・前提4は既存の agents-md-guard（Gemini の `BeforeTool`・`SessionStart`）が担う。

Antigravity IDE（2026-11-27 追加・実機 commit/push 通過確認済み）：`.agents/hooks.json` の `nra-prompt-gate.PreInvocation` から `antigravity_prompt_gate.py` を呼ぶ。
- 1回限り保証：`PreInvocation` はツール実行後の再呼出しやバックグラウンドタスク完了の自動再開でも発火する。そのため、`invocationNum == 0` かつ `transcriptPath` 内の最後の `USER_EXPLICIT` / `USER_INPUT` の `step_index` が前回処理値から進んだときだけ判定・承認発行を行い、それ以外は再発行せず `{}` を返す（状態保存先：`.agent_state/hooks/prompt_gate_antigravity_state.json`）。
- 記録：発火ごとに `.agent_state/hooks/prompt_gate_antigravity.jsonl`（`invocation_num`・`user_step`・入力のキー構造・文字数・判定結果。本文は記録しない）に追記する。

## 限界

- 承認ファイルはリポジトリ内のファイルで、OS の境界ではない。スクリプト経由の書込みは文字列ガードで見えない。
- Claude Code の登録先は `.claude/settings.json` の `hooks.UserPromptSubmit`。2026-11-26 に実機で、承認の書込み（「commitまで」）・消去（その他の入力）・NOT_EXACT の注入を確認した。
- hook の入力は UTF-8 のバイト列で届く。Windows の標準入力の既定（cp932）で読むと日本語の合言葉が一致しないため、ラッパーはバイト列から UTF-8 で読む。
