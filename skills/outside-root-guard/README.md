---
id: SKILL-OUTSIDE-ROOT-GUARD-20261121
kind: guide
created: 2026-11-21
author: M-Tokuni
title: "作業ルート外ガード（outside-root-guard）"
---

# 作業ルート外ガード（outside-root-guard）

AI が作業ルートの外のパスに触れる操作を、PreToolUse hook で機械的に止める。AGENTS.md §2（ルート外の読み書きは「警告:」付きで事前提示）と §6（ルート外への書込みは個別確認）を、AI の記憶に頼らず守るための第2層（AGENTS.md §11）である。

## 判定

| 状況 | Claude Code | Codex・Gemini・Cline |
|---|---|---|
| ルート内・許可リスト内だけ | 何も出さない（通常の権限確認へ。自動許可はしない） | 同じ |
| ルート外のパスを含む | ask：確認画面に「警告: {パス}: 作業ルート外の…」を出す | deny：止めて警告を返す |
| 許可リストのファイルを AI が書き換える | deny | deny |
| ガード自体が入力を確認できない | ask | deny |

Codex・Gemini・Cline で止まった操作を通すには、利用者が `.agent_state/outside_root_allow.txt` にパスを書き足してから再実行する。

## 見る場所

- ファイル系ツールの引数：`file_path`・`path`・`absolute_path`・`notebook_path`・`paths`・`cwd`・`workdir` など。Glob の `pattern` は絶対パスのときだけ
- Codex の `apply_patch`：`*** Add/Update/Delete File:`・`*** Move to:` の行
- シェルコマンドの文字列：ドライブ文字のパス（`C:\`）、git-bash 形式（`/c/`）、`/tmp`、`~`・`$HOME`・`%USERPROFILE%`・`$env:APPDATA` など、`..` で始まる相対パス、`cd`・`pushd`・`Set-Location` の行き先

## 許可リスト

| ファイル | 内容 | 管理 |
|---|---|---|
| `allow_default.txt` | 全環境共通の既定値（環境変数・ワイルドカード可）。Claude Code のメモリの置き場 | git 管理。利用者が編集 |
| `.agent_state/outside_root_allow.txt` | この PC だけの場所（作業用の一時フォルダなど） | git 管理外。利用者が編集 |

どちらも AI は書き換えない。ガードが書込みを止める。

## 限界

- シェルコマンドは文字列から典型的なパス表記だけを拾う。変数で組み立てたパスや、スクリプトの中で開くファイルは見えない。AGENTS.md §2 の文章規則と二重で使う。
- hook が未信頼・無効・非対応の経路では動かない（AGENTS.md §11）。
- 止めた操作は `.agent_state/hooks/outside_root.jsonl` に記録する（git 管理外）。

## 構成

- `_outside.py`：共通の判定
- `claude_outside.py`・`codex_outside.py`・`gemini_outside.py`・`cline_outside.py`：ホストごとの薄い入口
- `cline_pre_chain.py`：Cline の PreToolUse で、AGENTS.md 読込ガードの後にこのガードを続けて呼ぶ
- テスト：`tests/test_outside_root_guard.py`
