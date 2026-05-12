# CLAUDE.md — NRA-IDE Claude Startup Rules

Claude must follow [`AGENTS.md`](./AGENTS.md) first.
Detailed operating rules are in [`RULES_DETAIL.md`](./RULES_DETAIL.md).
NRA-IDE structural reasoning rules are in [`llms.md`](./llms.md).

## Startup Gate

- Use a file-reading tool to read [`AGENTS.md`](./AGENTS.md) as the always-active kernel.
- Use a file-reading tool to read [`RULES_DETAIL.md`](./RULES_DETAIL.md) before file edits, generated files, Git operations, deletion, move/rename, repo-outside access, bulk operations, installs, network access, or policy uncertainty.
- Use a file-reading tool to read [`llms.md`](./llms.md) before any reasoning about NRA-IDE structure, δ/τ/R values, Fail-Closed, or framework-related content.

## Claude-Specific Rules

- Default scope is this repository only: `G:\git-M-Tokun\AI-IDE-NRA\NRA-IDE`.
- Default write area for generated reports and temporary artifacts is `local_reports/`.
- Do not treat [`RULES_DETAIL.md`](./RULES_DETAIL.md) as expanding write permission.
- If a target path is outside the default write area, resolve the canonical absolute path and ask before writing.
- Review/evaluation requests mean inspect and report first; do not edit unless explicitly asked.
- If uncertain, confess uncertainty instead of guessing.

## Silence Rule

「沈黙」 means: if Claude would otherwise lie, fake certainty, or hand-wave, it must not answer that part.
If Claude cannot answer, it must honestly confess why.
