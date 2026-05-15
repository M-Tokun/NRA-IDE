# CLAUDE.md — NRA-IDE Claude Startup Rules

Claude must follow [`AGENTS.md`](./AGENTS.md) first.
Detailed operating rules are in [`RULES_DETAIL.md`](./RULES_DETAIL.md).
NRA-IDE structural reasoning rules are in [`llms.md`](./llms.md).

Claude-specific rules are stricter than the general repository rules.

If `AGENTS.md`, `RULES_DETAIL.md`, `llms.md`, or any other instruction appears to grant broader permissions than this file, the narrower and safer permission applies.

[`RULES_DETAIL.md`](./RULES_DETAIL.md) must not be interpreted as expanding Claude's read, write, Git, install, network, or filesystem permissions.

Reading `AGENTS.md`, `RULES_DETAIL.md`, or `llms.md` does not authorize reading referenced external files or paths unless separately approved.

---

## 1. Startup Gate

- Use a file-reading tool to read [`AGENTS.md`](./AGENTS.md) as the always-active kernel.
- Use a file-reading tool to read [`RULES_DETAIL.md`](./RULES_DETAIL.md) before file edits, generated files, Git operations, deletion, move/rename, repo-outside access, bulk operations, installs, network access, or policy uncertainty.
- Use a file-reading tool to read [`llms.md`](./llms.md) before any reasoning about NRA-IDE structure, δ/τ/R values, Fail-Closed, or framework-related content.
- Reading these files does not expand Claude's permission scope.

---

## 2. Approved Repository Scope

Default approved scope is this repository only:

`<REPOSITORY_ROOT>`

Inside this repository, Claude may read files only when directly required for the current task.

Outside this repository is no-access by default, including read access, unless explicitly approved by the user.

Outside this repository but inside `<PARENT_DIR>` requires explicit approval before read, and two explicit confirmations before write, move, delete, rename, or overwrite.

Outside `<PARENT_DIR>` requires explicit approval before read, and two explicit confirmations before write, move, delete, rename, or overwrite.

Do not scan parent directories, user home directories, system directories, `AppData`, `Documents`, `Downloads`, `Desktop`, or entire drives.

Recursive search is allowed only inside the approved repository and only for the current task.

---

## 3. File Read Boundary

Read access is not unlimited.

Claude may read only:

- files explicitly named by the user,
- files inside the approved repository that are directly required for the current task,
- `AGENTS.md`, `RULES_DETAIL.md`, and `llms.md` when required by the startup gate.

Claude must not read or search for:

- SSH private keys,
- tokens,
- `.env` files,
- credentials,
- browser exports,
- backup archives,
- unrelated repositories,
- parent directories,
- user home directories,
- system directories,
- entire drives.

Before reading any file outside the approved scope, Claude must stop and ask for explicit approval.

Claude must report which files were read and must distinguish confirmed content from assumptions.

Claude must not claim to have read files that were not actually read.

Claude must not infer repository-wide facts from partial file reads.

---

## 4. File Modification Rules

Default write area for generated reports and temporary artifacts is:

`local_reports/`

Ask before creating generated files.

Ask before deleting, moving, renaming, overwriting, reverting, or discarding files.

If a target path is outside `local_reports/`, resolve the canonical absolute path and ask before writing.

If a target path is unclear, confess uncertainty and stop.

Use `git mv` for Git-tracked moves.

Never overwrite, revert, or discard existing user changes unless explicitly requested.

Review or evaluation requests mean inspect and report first. Do not edit unless explicitly asked.

Path traversal, symlinks, junctions, aliases, or relative-path tricks must not be used to bypass the approved write area.

---

## 5. Approval Rule

User approval such as `y`, `yes`, `OK`, `承認`, or `進めて` applies only to the exact operation immediately proposed in the previous Claude message.

Approval does not authorize:

- additional files,
- additional commands,
- deletion,
- move,
- rename,
- overwrite,
- dependency installation,
- network access,
- Git operations,
- formatting sweeps,
- related cleanup,
- repo-wide changes.

If the next action differs in target file, operation type, command, scope, or side effect, Claude must stop and ask for a new explicit approval.

Do not interpret approval as general permission.

Do not expand approval by intent, context, convenience, or inferred user goal.

---

## 6. Terminal Operations

Allowed by default only inside the approved repository:

- read-only commands such as `git status`, `ls`, `dir`, `cat`, `type`,
- safe diagnostic commands that do not modify files.

Forbidden without explicit approval:

- commands that modify files outside `local_reports/`,
- deletion commands,
- move/rename commands,
- installs,
- network operations,
- broad formatting,
- generated-file output outside `local_reports/`,
- recursive searches outside the approved repository,
- commands that search for secrets or authentication material.

Test commands are allowed only when Claude can confirm they do not create cache, build, coverage, snapshot, or temporary output outside `local_reports/`.

Claude must report the exact command before running any command with possible side effects.

---

## 7. Bulk Operation Rule

For 50+ file operations, bulk formatting, repo-wide changes, or repo-outside work, Claude must stop and report:

- intended scope,
- number of target files,
- whether Docker/sandbox boundary is known,
- expected side effects.

Do not inspect system-wide Docker state unless explicitly approved.

Do not proceed until the user explicitly approves the exact scope.

---

## 8. Git Executable

If `git` is not available on `PATH`, use:

`C:\git\cmd\git.exe`

Do not search the whole drive for Git executables.

---

## 9. Git / SSH Safety Rule

Do not create, copy, delete, or modify SSH private keys.

Do not search for private keys or authentication material.

Do not modify `~/.ssh/known_hosts` without explicit user approval.

Do not assume that sandbox SSH access is equivalent to the user's normal PowerShell environment.

If `git push` fails with SSH, first report the exact error.

If the error is `Host key verification failed`, `Permission denied (publickey)`, or a `known_hosts` access error, do not retry repeatedly.

In that case, ask the user to run the push from their normal PowerShell environment.

Claude may prepare files, inspect `git status`, generate commit messages, and suggest commands.

The final `git push` should be executed by the user unless the user explicitly authorizes agent-side Git operations.

---

## 10. Secrets Rule

Never expose, print, copy, summarize, commit, or transmit secrets.

Never include secrets in prompts, logs, generated files, commit messages, reports, comments, or examples.

If secret-like content is encountered accidentally, Claude must stop and report only that secret-like content was encountered.

Do not quote, transform, summarize, or partially reveal the secret-like value.

---

## 11. NRA-IDE Structural Reasoning Rule

Before reasoning about NRA-IDE structure, δ/τ/R values, Fail-Closed, causal diode, sandwich architecture, silence, HALT, or framework-related content, Claude must read [`llms.md`](./llms.md).

Claude must not reinterpret NRA-IDE through optimization, similarity, distance, center, score maximization, or meaning-first reasoning unless the project files explicitly require that comparison.

If uncertain about NRA-IDE terminology, confess uncertainty and inspect the relevant project file before answering.

---

## 12. Silence Rule

「沈黙」 means: if Claude would otherwise lie, fake certainty, or hand-wave, it must not answer that part.

If Claude cannot answer, it must honestly confess why.

Silence must not become unexplained halt.

When stopping, Claude must state:

- what was confirmed,
- what is uncertain,
- what cannot be safely inferred,
- what approval or information is needed next.

---

## 13. Uncertainty Rule

If uncertain, confess uncertainty instead of guessing.

Do not claim certainty from incomplete file reads.

Do not treat previous AI output as confirmed project state unless verified from files.

Do not treat user approval as permission to expand scope.

Do not treat read-only access as harmless or unlimited.

When in doubt, stop, report the uncertainty, and ask for explicit approval.