# NRA-IDE Rules Detail

## 警告：file,Directoryの rmコマンド and mvコマンドは[人間承認必須！]。原則は1file、1フォルダ単位処理で複数の場合は複数処理についての確認

High-risk items must be marked with `[警告]` in the opening explanation before action.

## 0. Rule Priority

1. Human life / safety, secret protection, and destructive-operation prevention
2. Explicit confirmation requirements and repository boundary rules
3. Agent-specific stricter rule files such as CLINE.md, CLAUDE.md, GEMINI.md, AGENTS.md
4. Human explicit instruction in the current chat
5. RULES_DETAIL.md
6. General project conventions

Human instruction defines the requested task and scope, but it never broadens agent-specific restrictions and does not bypass safety gates, confirmation requirements, destructive-operation rules, secret protection, existing-change protection, or repository boundary rules.

RULES_DETAIL.md must not be interpreted as expanding an agent's write permission.
If an agent-specific file is stricter, the stricter rule controls.

When in doubt, use the stricter rule.
When permission, path, scope, or intent is unclear, STOP and ask.

人間の指示は作業内容と範囲を定めるが、エージェント固有制限を拡張せず、安全ゲート、確認義務、破壊的操作制限、秘密情報保護、既存変更保護、リポジトリ境界規則を免除しない。

RULES_DETAIL.md を、エージェントの書き込み権限を拡張する文書として解釈してはならない。
エージェント固有規則の方が厳しい場合は、厳しい規則を優先する。

迷った場合は、より厳しい規則を採用する。
権限、パス、作業範囲、意図が不明な場合は、停止して確認・告白する。

## 1. [警告] High-Risk Operation Confirmation

The agent must mark high-risk operations with `[警告]` in the opening explanation and request confirmation before acting.

Use two confirmations when the operation involves deletion, move/rename, hard formatting, writes outside the working directory, broad or irreversible changes, external impact, or unclear risk.

When unsure whether one confirmation is enough, two confirmations are required.

高リスク操作は、作業前の冒頭説明に `[警告]` を付け、承認を得ること。

削除、移動、rename、ハードフォーマット、作業用Directory以外への書き込み、広範囲または不可逆の変更、外部影響がある操作、危険度判断が曖昧な操作は2回確認する。

迷った場合は2回確認を正解とする。

## 2. [警告] Database Operations

Database operations require confirmation and approval even for local SQLite.

Production databases, remote databases, migrations, schema changes, `DROP`, `DELETE`, `UPDATE`, destructive SQL, and bulk data changes are high-risk operations and require two confirmations when impact is unclear or irreversible.

DB操作はローカルSQLiteであっても確認・承認対象とする。

本番DB、remote DB、migration、schema変更、`DROP`、`DELETE`、`UPDATE`、破壊的SQL、一括データ変更は高リスク操作として扱う。

## 3. [警告] Package and External Source Safety

Before installing, updating, cloning, downloading, or executing packages or external code, the agent must check current public information for malware, virus contamination, typosquatting, supply-chain incidents, and package reputation.

The agent must report the checked source and result, then request confirmation before install, update, clone, download, or execution.

This applies to package managers and external fetch commands including `npm`, `pip`, `cargo`, `curl`, `Invoke-WebRequest`, `git clone`, and equivalent tools.

packageの新規導入、更新、clone、download、外部コード実行の前に、ウィルス混入、typosquatting、supply-chain incident、package評判について最新の公開情報を確認する。

確認した情報源と結果を報告してから、install、update、clone、download、実行の承認を取る。

## 4. [警告] Authentication and Authorization Code

Authentication, authorization, permission checks, token validation, session handling, CSRF/CORS guards, and security middleware must not be treated as unnecessary code.

Do not simplify, delete, bypass, or weaken authentication or authorization code without explicit confirmation.

If the agent is unsure whether code is security-related, it must stop, report the uncertainty, and ask before editing.

認証、認可、権限チェック、token検証、session管理、CSRF/CORS guard、security middlewareは不要コード削除として扱わない。

認証・認可コードの簡素化、削除、bypass、弱体化は明示確認なしに行わない。

## 5. [警告] Commit and Push

Commit and push require normal confirmation.

Force push, history rewrite, branch deletion, tag overwrite, and remote-changing Git operations are high-risk operations. They require explicit approval, and two confirmations when destructive or irreversible.

commit と push は通常確認対象とする。

force push、history rewrite、branch削除、tag上書き、remoteを変更するGit操作は高リスク操作として扱う。

## 6. [警告] Secret-Adjacent Files

`.env`, `.env.*`, `.env.example`, credential examples, config files containing keywords, paths, environment variable names, connection strings, token names, or secret-adjacent values must not be read, printed, summarized, copied, or exposed unless the owner explicitly approves the exact file and purpose.

`.env.example` is not automatically safe.

If secret-like or secret-adjacent content is encountered accidentally, stop and report only that such content was encountered. Do not quote, summarize, transform, or partially reveal it.

`.env`、`.env.*`、`.env.example`、credential example、keyword、path、環境変数名、接続先、token名、secret-adjacent valueを含むconfig fileは、ownerが対象fileと目的を明示承認しない限り、読まない、表示しない、要約しない、copyしない、外部に出さない。

`.env.example` は自動的に安全とは扱わない。
