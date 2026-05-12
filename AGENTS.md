# AGENTS.md — NRA-IDE Agent Kernel

This file is the short always-active startup gate for AI agents.
Detailed rules are in [`RULES_DETAIL.md`](./RULES_DETAIL.md).
NRA-IDE structural reasoning rules are in [`llms.md`](./llms.md).

## Always Active

- Default mode is READ-ONLY.
- The only default write root is `local_reports/`.
- Before any write/edit/create/delete/move/rename/overwrite, resolve the canonical absolute path.
- If the target is outside the allowed write root, STOP and ask for explicit approval.
- Review / audit / check / inspect means report only. It never grants edit permission.
- Delete, move, rename, overwrite, Git operations, installs, network access, repo-outside access, and 50+ file operations require inspecting [`RULES_DETAIL.md`](./RULES_DETAIL.md) using a file-reading tool.
- NRA-IDE structural reasoning involving δ, τ, R, Fail-Closed, or framework evaluation requires inspecting [`llms.md`](./llms.md) using a file-reading tool.
- If permission, path, scope, or structural variables are unclear, do not guess. CONFESS and STOP.

## Permission Principle

[`RULES_DETAIL.md`](./RULES_DETAIL.md) is a detailed rulebook, not a permission expansion.
If another agent-specific file is stricter, the stricter rule controls.
When in doubt, use the stricter rule.

- Multi-file reading, recursive scanning, reading 50+ files, or reading outside the repository requires `RULES_DETAIL.md`.
  