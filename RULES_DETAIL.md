# NRA-IDE Rules Detail

## 警告：file,Directoryの rmコマンド and mvコマンドは[人間承認必須！]。原則は1file、1フォルダ単位処理で複数の場合は複数処理についての確認

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
