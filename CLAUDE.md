# CLAUDE.md — NRA-IDE Project Conventions

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