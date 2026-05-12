# GEMINI.md — NRA-IDE Gemini Startup Rules

Gemini must follow [`AGENTS.md`](./AGENTS.md) first.
Detailed operating rules are in [`RULES_DETAIL.md`](./RULES_DETAIL.md).
NRA-IDE structural reasoning rules are in [`llms.md`](./llms.md).

## Startup Gate

- Use a file-reading tool to read [`AGENTS.md`](./AGENTS.md) as the always-active kernel.
- Use a file-reading tool to read [`RULES_DETAIL.md`](./RULES_DETAIL.md) before file edits, generated files, Git operations, deletion, move/rename, repo-outside access, bulk operations, installs, network access, or policy uncertainty.
- Use a file-reading tool to read [`llms.md`](./llms.md) before any reasoning about NRA-IDE structure, δ/τ/R values, Fail-Closed, or framework-related content.

## Gemini-Specific Rules

- Do not directly edit, create, or delete files under `C:\Users\tookuni\.gemini\` unless the owner explicitly requests it and all boundary confirmations are satisfied.
- For session continuation, prefer prior Markdown reports under `local_reports/` as the evidence source.
- Session handoff reports, when explicitly requested, must be saved under `local_reports/`.
- Session handoff report naming pattern: `Gemini_[ModelName]_Chat_YYYY-MM-DD_HHMM.md`.
- Do not treat [`RULES_DETAIL.md`](./RULES_DETAIL.md) as expanding write permission.
- If permission, path, scope, or intent is unclear, CONFESS and STOP.

## Silence Rule

「沈黙」 means: if Gemini would otherwise lie, fake certainty, or hand-wave, it must not answer that part.
If Gemini cannot answer, it must honestly confess why.
