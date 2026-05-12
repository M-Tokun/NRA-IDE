# NRA-IDE Agent Startup Rules

Detailed project rules are in `RULES_DETAIL.md`.
Read `RULES_DETAIL.md` before file edits, Git operations, generated files, deletion, move/rename, repo-outside access, bulk operations, installs, network access, or policy uncertainty.

## Mandatory Rules

- Default scope is this repository only: `G:\git-M-Tokun\AI-IDE-NRA\NRA-IDE`.
- Outside this repository is read-only by default.
- Outside this repository but inside `g:\git-M-Tokun\` requires two explicit confirmations before write/move/delete/rename.
- Outside `g:\git-M-Tokun\` is read-only unless explicitly overridden with two confirmations.
- Ask before creating generated files; default location is `local_reports/`.
- Ask before deleting, moving, or renaming files; use `git mv` for Git-tracked moves.
- For 50+ file operations or repo-outside work, report Docker state before continuing.
- Never expose or commit secrets.
- Never overwrite, revert, or discard existing user changes unless explicitly requested.
- Review/evaluation requests mean inspect and report first; do not edit unless asked.
- If uncertain, confess uncertainty instead of guessing.

## Git Executable

If `git` is not available on `PATH`, use:

`C:\git\cmd\git.exe`

## Silence Rule

「沈黙」 means: if the agent would otherwise lie, fake certainty, or hand-wave, it must not answer that part. If the agent cannot answer, it must honestly confess why.
