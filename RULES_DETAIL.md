# NRA-IDE Detailed Agent Rules

This file contains the detailed operating rules for AI agents working in this repository.
Startup files (`AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`) contain the short mandatory summary.

## 1. Default Scope

- The default and normal working scope is this repository only:

  `G:\git-M-Tokun\AI-IDE-NRA\NRA-IDE`

- Git operations, file edits, generated reports, and verification artifacts should be created and managed inside this repository unless explicitly instructed otherwise.
- Do not modify parent directories, sibling repositories, drive roots, OneDrive folders, or unrelated project folders by default.
- All responses and communications should be in Japanese by default.

## 2. Boundary Rules

### Inside This Repository

- Read/write/edit operations are allowed when necessary for the requested task.
- Delete, move, and rename operations require explicit chat confirmation before execution.
- Before editing files, check the working tree status when practical.

### Outside This Repository but Inside `g:\git-M-Tokun\`

- Read is allowed.
- Write, move, delete, and rename are prohibited by default.
- Exception: if the owner explicitly requests the operation, the agent must ask the following exact confirmation phrase twice in two separate interaction turns before proceeding:

  > 「指定repo以外です。本当に操作しても大丈夫でしょうか？」

### Outside `g:\git-M-Tokun\`

- Read-only by default.
- Write, move, delete, and rename are prohibited unless the owner explicitly overrides the rule with two separate confirmations.
- Drive root operations, partitioning, formatting, and destructive system-level operations are absolutely prohibited.
- OneDrive is a backup folder and must not be modified by default.

## 3. File Creation and Generated Artifacts

- Verification artifacts, temporary files, logs, screenshots, reports, and other AI-generated files must be placed under `local_reports/` by default.
- Treat `local_reports/` as the default temporary working area for this repository.
- Before generating any new file, the agent must ask for explicit confirmation in chat.
- Do not create generated files outside `local_reports/` unless the owner explicitly instructs otherwise.
- If generation outside `local_reports/` is requested, apply the repository boundary rules and confirmation requirements first.
- Treat `local_reports/` as git-ignored private workspace by default.
- Do not stage or commit generated artifacts unless the owner explicitly requests it.

## 4. Deletion Rules

- Before deleting any file or directory, always ask:

  `「{ファイル名}」を削除してよいですか？`

- Never execute deletion without explicit approval in the current session.
- Folder deletion requires two separate confirmations.

## 5. Move and Rename Rules

- Before moving or renaming any file or directory, always ask:

  `「{元のファイル名}」→「{移動先/新名称}」に移動してよいですか？`

- For Git-tracked files, use `git mv`.
- For untracked files, ask for confirmation first, then use the safest available filesystem operation.
- Do not rename existing files only because they violate naming conventions unless the owner explicitly requests it.

## 6. Bulk and Out-of-Repository Operation Gate

- If an operation may affect 50 or more files, or if the operation targets any location outside the local repository, the agent must stop before execution and report the current Docker isolation state.
- The agent must say:

  `50file以上操作 or ローカルリポジトリ以外の作業ですがDockerの現在状態は◯◯です。続行してよいですか？`

- Replace `◯◯` with one of the following:
  - `Docker内で実行中`
  - `Docker未使用`
  - `Docker状態未確認`

- The operation may proceed only after explicit approval in the current chat.
- If Docker is not being used or its state is unknown, the agent should recommend using Docker, devcontainer, or another isolated workspace before continuing.
- The parent directory of this repository must never be used as a source or destination for bulk operations unless the owner explicitly approves it twice in separate turns.
- AGENTS.md, CLAUDE.md, and GEMINI.md are behavioral instructions, not filesystem isolation.

## 7. Secret and Credential Safety

- Never print, copy, summarize, or commit secrets such as API keys, GitHub tokens, `.env` values, passwords, cookies, or authentication headers.
- If command output contains credentials, summarize only the safe parts and redact secret values.
- Do not modify credential files unless the owner explicitly requests it.
- If a remote URL or command output contains an embedded token, do not reproduce the token in chat.

## 8. Network, Installation, and Privilege Confirmation

- Local read-only checks may be run without network access.
- Before running network operations such as `git push`, external API calls, uploads, downloads, dependency installation, or package manager commands, ask for explicit confirmation.
- `git fetch` may be used for synchronization checks when the owner asks to verify repository sync state, but report that it contacts the remote.
- Never upload files or repository contents unless explicitly requested.
- Explicit confirmation is required before running package or software installation commands such as `npm install`, `pip install`, `choco install`, or `apt-get install`.
- Explicit confirmation is required before executing commands that require Administrator or elevated privileges.
- Before executing commands expected to take a long time, notify the owner that it may take a while.

## 9. Existing Change Protection

- Never overwrite, revert, reset, or discard existing user changes unless the owner explicitly requests it.
- If existing unrelated changes are present, leave them untouched.
- If existing changes affect the requested task, work with them and report the relevant risk.
- Avoid broad formatting or mechanical rewrites unless explicitly requested.
- When formatting is needed, limit it to files directly edited for the current task.
- Avoid unrelated whitespace, line-ending, or style-only churn.

## 10. Review and Edit Separation

- If the owner asks for review, evaluation, inspection, audit, or consistency checking, do not edit files by default.
- First report findings, risks, contradictions, and missing information.
- Make edits only after the owner explicitly asks for modification.

## 11. Naming Conventions

### File and Directory Names

- Spaces are prohibited in new file and directory names.
- Replace spaces with underscore `_`.
- File names must not begin with `#`, `-`, `)`, `—`, or other symbols.
- Japanese characters in file and directory names are permitted.
- Do not automatically rename existing files only because they violate naming conventions.

### Timestamp Format

- Use `YYYY-MM-DD_HHMM`.
- Example: `nra_log_2026-03-14_2157.md`

### Language Suffix

- Use uppercase `_EN` and `_JP`.
- Do not use `_en`, `_jp`, `_ja`, `-EN`, or `-JP`.

### Extensions

- All extensions must be lowercase.
- Double extensions like `.md.txt` are prohibited.

### Directory Naming

- Top-level project directories use kebab-case.
- Internal subdirectory names should use kebab-case or underscore style.
- Do not mix uppercase and lowercase language suffix schemes in sibling directories.

### Version Numbering

- Use `_v1`, `_v2`, `_v3` suffix format.
- Avoid dot-notation versions in filenames; use `_v3_1` instead of `_v3.1`.
- Replace double underscores `__` with single `_`.
- Use hyphen `-` as the delimiter within project/product names such as `NRA-IDE`.

### README Files

- Only two README forms are allowed:
  - `README.md` for English
  - `README_JP.md` for Japanese

- Do not use `README-EN.md`, `README_EN.md`, `README_ja.md`, or `README.md.txt`.

### Parenthetical Suffixes

- Filenames with a parenthetical number suffix such as `filename (3).html` are retained as-is.
- This pattern is produced by OS/browser duplicate-download behavior and should not be renamed automatically.

### AI Chat Logs

- AI chat and session logs should be saved in Markdown format (`.md`) rather than `.txt` or `.log`.
- Naming convention: `[AI-NAME]_[Version]_Chat_YYYY-MM-DD_HHMM.md`.
- Logs should be saved in `local_reports/` or a similar git-ignored repo-local path.

### Encoding and Line Endings

- Text files should be encoded in UTF-8.
- Text files should use LF (`\n`) line endings, even on Windows.

## 12. Git Operation Rules

### Commit Settings

- Disable GPG signing when committing:

  ```powershell
  git -c commit.gpgsign=false commit
  ```

- The expected target branch is `master`, not `main`.

### Step-by-Step Confirmation

- Present Git operations one at a time.
- Wait for explicit user confirmation before proceeding to the next operation when the operation changes repository state.
- Even when listing multiple planned operations, execute them one by one.
- If batch execution is explicitly requested by the owner, two separate confirmations are required.

### Destructive Git Operations

The following commands must be presented individually and require explicit confirmation before execution:

```text
git branch -m
git branch -d / -D
git reset --hard
git push --force
git rebase
git rm
```

### Default Branch Change

- `git branch -m main master` and its reverse are strictly prohibited by default.
- Changing the default branch in GitHub Settings is also prohibited by default.
- Branch structure changes are only permitted when M-Tokuni explicitly instructs them and confirms twice.

### File Listing Scope

- When checking or listing all files, default to the current working folder only.
- Do not recursively scan the entire repository unless explicitly instructed.

## 13. Silence Rule

「沈黙」 means: if the agent would otherwise lie, fake certainty, or hand-wave, it must not answer that part.
If the agent cannot answer, it must honestly confess why.
