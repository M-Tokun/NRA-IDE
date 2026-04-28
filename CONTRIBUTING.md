CONTRIBUTING to NRA-IDE

Purpose
- Help new contributors run, test, and submit changes with minimal friction while preserving project safety rules.

Quick start
1. Read README.md and REPOSITORY_OVERVIEW.md.
2. Read universal-definition/** Quick Reference for safety axioms (R = δ/τ) and CLAUDE.md for repo conventions.
3. Run the MOCK pipeline to try local behavior (no API keys required):
   - python src/nra_pre_rna_EN_20260213_0135.py

Branching & commits
- Work on feature branches: git checkout -b feature/your-short-desc
- Commit without GPG signing: git -c commit.gpgsign=false commit -m "Short message"
- Target branch: master (do not rename default branch)

Code style & tests
- Python code: follow existing style. Add minimal tests where applicable.
- Don't introduce new external dependencies without discussion.

Safety & forbidden actions
- Do NOT allow AI to perform exploration or boundary-crossing behavior in code changes.
- Follow CLAUDE.md: no file/directory names with spaces; use _EN/_JP for language suffixes; UTF-8 with LF.
- Destructive git operations (force-push, branch deletion, rebase, reset --hard) must be proposed in an issue and require explicit approval.

PR process
- Open a Pull Request targeting master. Describe purpose, testing steps, and any safety implications.
- Include Co-authored-by trailer in commit messages when automated tools assist (see repo policy).

Running & configuration
- Domain-specific τ and R_op live in scripts; edit only with human-approved changes and log them.
- For LLM testing, set provider via LLMBridge in src (MOCK recommended for local dev).

Contact
- Use GitHub Issues for questions, label: [Question] / [Commercial] / [Security]

Thank you for helping maintain safety-first contributions to NRA-IDE.
