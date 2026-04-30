# CLAUDE.md — NRA-IDE Project Conventions

## AI Agent Workspace Constraints

### 1. Operation Boundaries

- The AI agent is **strictly limited** to full operations (Read/Write/Move/Delete) **only** within the `g:\git-M-Tokun\` directory structure.

- For all locations **outside** of `g:\git-M-Tokun\`, the AI agent is only permitted to **Read**. Modifying, moving, or deleting files outside this designated directory is **strictly prohibited**.

### 2. Explicit Override Confirmation

- If the owner explicitly requests a modification (Write, Move, or Delete) outside of the `g:\git-M-Tokun\` boundary, the AI agent must **not** execute it immediately.

- The AI agent must verify the request by asking the exact following phrase **twice** (in two separate interaction turns):

  > 「指定フォルダ以外です。本当に操作しても大丈夫でしょうか？」

- The destructive/modifying operation can only proceed if the owner explicitly approves both consecutive confirmations.

---

## Naming Conventions

### 1. No Spaces in File/Directory Names

- Spaces are **prohibited** in all file and directory names.

- Replace spaces with underscore `_`.

- Example: `Operational Checklist.md` → `Operational_Checklist.md`

### 2. Timestamp Format

- Use `YYYY-MM-DD_HHMM` format.

- Example: `nra_log_2026-03-14_2157.md`

### 3. Language Suffix

- Always use uppercase `_EN` / `_JP`.

- Example: `README_EN.md`, `guide_JP.md`

- Do **not** use `_en`, `_jp`, `_ja`, `-EN`, `-JP`.

### 4. File Extensions

- All extensions must be **lowercase**.

- Examples: `.md` (not `.MD`), `.py`, `.html`, `.json`, `.txt`

- Double extensions like `.md.txt` are **prohibited**.

### 5. Directory Naming

- Top-level project directories: **kebab-case** (e.g., `nra-tcm-parser`, `multi-physics-safety-gate`).

- Internal subdirectory names: kebab-case preferred; underscore `_` also allowed.

- Do **not** mix uppercase and lowercase in the same naming scheme (e.g., `JP` and `en` in sibling dirs is prohibited).

### 6. No Leading Special Characters

- File names must **not** begin with `#`, `-`, `)`, `—`, or other symbols.

- Example: `###title.md` → `title.md`

### 7. Japanese File Names

- Japanese characters in file and directory names are **permitted** throughout the project without restriction.

### 8. Version Numbering

- Use `_v1`, `_v2`, `_v3` suffix format.

- Example: `nra_crystallizer_JP_v2.py`

- Avoid dot-notation versions in filenames (e.g., `_v3.1` → `_v3_1`).

### 9. No Double Underscores

- Replace `__` with single `_`.

- Example: `40__Output_Reports` → `40_Output_Reports`

### 10. Project Name Delimiter

- Use hyphen `-` as the delimiter within project/product names.

- Examples: `NRA-IDE`, `HAN-Gate`, `nra-tcm-parser`

### 11. README Files

- Only two forms are allowed: `README.md` (English) and `README_JP.md` (Japanese).

- Do **not** use: `README-EN.md`, `README_EN.md`, `README_ja.md`, `README.md.txt`, etc.

### 12. Parenthetical Suffixes — `(N)` Form

- Filenames with a parenthetical number suffix such as `filename (3).html` are **retained as-is**.

- This pattern is produced by OS/browser duplicate-download behavior and should not be renamed automatically.

### 13. AI Chat Logs

- AI chat and session logs must be saved in Markdown format (`.md`) rather than `.txt` or `.log` to preserve code blocks, syntax highlighting, and document structure.

- Naming convention: `[AI-NAME]_[Version]_Chat_YYYY-MM-DD_HHMM.md` (e.g., `Gemini_3.1Pro_Chat_2026-04-28_1430.md`).

- Logs should be saved in the `local_reports/` directory (or similar git-ignored paths) for private management.

### 14. File Encoding and Line Endings

- All text files must be encoded in **UTF-8**.

- All line endings must be normalized to **LF** (`\n`), even on Windows environments. Do not use CRLF (`\r\n`).

---

## Git Operation Rules

### Commit Settings

- Always disable GPG signing when committing:

  ```

  git -c commit.gpgsign=false commit

  ```

- Always target the `master` branch (never `main`):

  ```

  git push origin master

  ```

### Step-by-Step Confirmation

- Present operations **one at a time**. Never batch-execute multiple operations.

- Wait for explicit user confirmation before proceeding to the next operation.

- Even when listing multiple planned operations, execute them one by one.

- Folder deletion requires **two separate confirmations**.

- If batch execution is explicitly requested by the user, **two separate confirmations** are required.

### Destructive Operations — Present Individually

The following commands must be presented **individually** and require **explicit confirmation** before execution. Never group them together.

```

git branch -m          # rename branch

git branch -d / -D     # delete branch

git reset --hard       # discard changes

git push --force       # force push

git rebase             # rewrite history

git rm                 # delete tracked file

```

### Default Branch Change — Prohibited

- `git branch -m main master` and its reverse are **strictly prohibited**.

- Changing the default branch in GitHub Settings is also **prohibited**.

- Branch structure changes are only permitted when M-Tokuni explicitly instructs them (confirm twice).

### File Move — Use `git mv` Only

```

# Correct

git mv <old_path> <new_path>

# Prohibited — breaks git history

# Windows Explorer / mv / cp + rm / OS-level file operations

```

### File Listing Scope

- When checking or listing all files, **default to the current working folder only**.

- Do not recursively scan the entire repository unless explicitly instructed.

# （沈黙）嘘・誤魔化し・テキトーをするならばその部分については沈黙。答えられないならば正直に告白して下さいという意味合いです。

