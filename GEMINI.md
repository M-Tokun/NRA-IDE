# GEMINI.md - NRA-IDE Gemini Startup Rules

Detailed project rules are in `RULES_DETAIL.md`.
Gemini must read `RULES_DETAIL.md` before file edits, Git operations, generated files, deletion, move/rename, repo-outside access, bulk operations, installs, network access, or policy uncertainty.

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

## Gemini-Specific Notes

- Do not directly edit, create, or delete files under `C:\Users\tookuni\.gemini\` unless the owner explicitly requests it and all boundary confirmations are satisfied.
- For session continuation, prefer prior Markdown reports under `local_reports/` as the evidence source.
- Session handoff reports, when explicitly requested, should be saved under `local_reports/` with the naming pattern `Gemini_[ModelName]_Chat_YYYY-MM-DD_HHMM.md`.

## Silence Rule

「沈黙」 means: if the agent would otherwise lie, fake certainty, or hand-wave, it must not answer that part. If the agent cannot answer, it must honestly confess why.
