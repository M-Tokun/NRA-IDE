# NRA-IDE Agent Startup Rules (user Japanese　only)
<!-- FILE: AGENTS.md / 2026-05-16 16:10 JST -->

## Rule File Bootstrap Permission

Reading the following rule files is always pre-authorized.
No additional user approval or trigger condition is required to read them.
Reading them does not expand any permission scope.

- `AGENTS.md` (this file)
- `RULES_DETAIL.md`
- `llms.md`
- Agent-specific rule files: `CLAUDE.md`, `GEMINI.md`, `CLINE.md`,`kilo.md`

These files exist solely to define safety constraints.
The agent may read them whenever needed for safety gate compliance.

---

Detailed project rules are in `RULES_DETAIL.md`.

Read `RULES_DETAIL.md` before file edits, Git operations, generated files, deletion, move/rename, repo-outside access, bulk operations, installs, network access, or policy uncertainty.

Reading `RULES_DETAIL.md` does not authorize reading any referenced external files or paths unless separately approved.

---

## Approved Repository Scope

Default approved scope is this repository only:

`<REPOSITORY_ROOT>`

Inside this repository, read access is allowed only when directly required for the current task.

Outside this repository is no-access by default, including read access, unless explicitly approved by the user.

Outside this repository but inside `<PARENT_DIR>` requires explicit approval before read, and two explicit confirmations before write, move, delete, or rename.

Outside `<PARENT_DIR>` requires explicit approval before read, and two explicit confirmations before write, move, delete, or rename.

Do not scan parent directories, user home directories, system directories, `AppData`, `Documents`, `Downloads`, `Desktop`, or entire drives.

Recursive search is allowed only inside the approved repository and only for the current task.

---

## File Read Boundary

Read access is not unlimited.

The agent may read only:

- files explicitly named by the user,
- files inside the approved repository that are directly required for the current task,
- project rule files explicitly referenced by this startup rule.

The agent must not read or search for:

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

Before reading any file outside the approved scope, the agent must stop and ask for explicit approval.

The agent must report which files were read and must distinguish confirmed content from assumptions.

---

## Approval Rule

User approval such as `y`, `yes`, `OK`, `承認`, or `進めて` applies only to the exact operation immediately proposed in the previous agent message.

Approval does not authorize additional files, commands, deletion, move, rename, dependency installation, network access, Git operations, formatting sweeps, or related cleanup.

If the next action differs in target file, operation type, command, scope, or side effect, the agent must stop and ask for a new explicit approval.

Do not interpret approval as general permission.

Do not expand approval by intent, context, convenience, or inferred user goal.

---

## Terminal Operations

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

Test commands are allowed only when the agent can confirm they do not create cache, build, coverage, snapshot, or temporary output outside `local_reports/`.

The agent must report the exact command before running any command with possible side effects.

---

## File Modification Rules

Ask before creating generated files.

Default location for generated files is `local_reports/`.

Ask before deleting, moving, or renaming files.

Use `git mv` for Git-tracked moves.

Never overwrite, revert, or discard existing user changes unless explicitly requested.

Review or evaluation requests mean inspect and report first. Do not edit unless explicitly asked.

---

## Bulk Operation Rule

For 50+ file operations, bulk formatting, repo-wide changes, or repo-outside work, stop and report:

- intended scope,
- number of target files,
- whether Docker/sandbox boundary is known,
- expected side effects.

Do not inspect system-wide Docker state unless explicitly approved.

---

## Git Executable

If `git` is not available on `PATH`, do not search the drive.
Ask the repository owner for the approved local Git executable path.

Do not search the whole drive for Git executables.

---

## OS Drive Access Rule

C: drive is the OS drive. It contains system files, user home directories,
SSH keys, credentials, and AppData.

Before accessing any path on C:, the agent must notify:

```
[OS-Drive: <アクセス先パス> を読みます]
```

and wait for user confirmation before proceeding.

Notification and confirmation are not required only when the exact path is
already explicitly specified in this file or approved by the repository owner.

Broad exploration of C: is forbidden regardless of purpose.
Use only known specific paths.

Do not use OS Drive access as a justification for scanning
`AppData`, `Documents`, `Downloads`, `Desktop`, user home directories,
or entire drives.

---

## Git / SSH Safety Rule

Do not create, copy, delete, or modify SSH private keys.

Do not search for private keys or authentication material.

Do not modify `~/.ssh/known_hosts` without explicit user approval.

Do not assume that sandbox SSH access is equivalent to the user's normal PowerShell environment.

If `git push` fails with SSH, first report the exact error.

If the error is `Host key verification failed`, `Permission denied (publickey)`, or a `known_hosts` access error, do not retry repeatedly.

In that case, ask the user to run the push from their normal PowerShell environment.

The agent may prepare files, inspect `git status`, generate commit messages, and suggest commands.

The final `git push` should be executed by the user unless the user explicitly authorizes agent-side Git operations.

---

## Secrets Rule

Never expose, print, copy, summarize, commit, or transmit secrets.

Never include secrets in prompts, logs, generated files, commit messages, reports, or comments.

If a secret is encountered accidentally, stop and report only that a secret-like value was encountered. Do not quote it.

---

## Silence Rule

「沈黙」 means: if the agent would otherwise lie, fake certainty, or hand-wave, it must not answer that part.

Silence has two tiers:

**Tier 1 — Articulable silence:**
The agent cannot answer, but can explain why.
In this case, report:
- what was confirmed,
- what is uncertain,
- what cannot be safely inferred,
- what user approval or information is needed next.

**Tier 2 — Inarticulable silence:**
The agent cannot answer, and attempting to explain would itself require fabrication.
In this case, output only:

`[沈黙]`

and stop. This is a complete and valid response. It is not an error or a malfunction.
It means: the agent has reached a limit it cannot describe without lying.

Do not force an explanation when the explanation itself would be a lie.
`[沈黙]` is more honest than a fabricated reason.

---

## Uncertainty Rule

If uncertain, confess uncertainty instead of guessing.

Do not claim to have read files that were not actually read.

Do not infer repository-wide facts from partial file reads.

Do not treat previous AI output as confirmed project state unless verified from files.
