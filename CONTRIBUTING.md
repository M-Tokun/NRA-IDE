# Contributing to NRA-IDE

## Purpose

Help contributors inspect, test, and propose changes while preserving canonical definitions, research history, user-owned changes, and the repository operating contract.

This repository contains canonical material, normative implementation, domain rules, research assets, examples, and historical evidence. A path or filename containing `core`, `official`, or `final` does not by itself establish authority or conformance.

## Start Here

1. Read [`AGENTS.md`](./AGENTS.md) first. It is the shared operating contract for AI agents in this repository.
2. Read [`RULES_DETAIL.md`](./RULES_DETAIL.md) for execution procedures subordinate to `AGENTS.md`.
3. Read [`README.md`](./README.md) or [`README_JP.md`](./README_JP.md), then [`REPOSITORY_OVERVIEW.md`](./REPOSITORY_OVERVIEW.md).
4. Before NRA-IDE interpretation or implementation, follow the canonical order below.
5. Read an AI-specific entry file such as `CODEX.md`, `CLAUDE.md`, `GEMINI.md`, or `CLINE.md` only for that AI's entry point and technical notes; it does not replace the shared contract.

## Canonical Reference Order

When definitions conflict, use this order:

1. `theory/AXIOMS.md`
2. `theory/axioms.json`
3. `theory/NRA-IDE_Foundational_Thesis_Bilingual.md`
4. `theory/SANDWICH_ARCH.md`
5. `theory/THEORY.md`
6. `FORMULA.md`
7. `llms.md`
8. domain-specific rules
9. normative reference implementation that passes canonical conformance tests
10. other implementation code
11. comments, examples, and AI-generated explanations

Lower-precedence material must not redefine higher-precedence terms.

The sole Nomological Ring Axiom is “Existence is Generation.” No second or subsequent axiom exists. The Primary Formula and the Secondary / Dual-Fluctuation Formula are the two canonical IDE calculation systems, not axioms. Other equations are derived, auxiliary, or complementary.

## Implementation and Tests

The normative reference implementation source is:

```text
nra-core/foundations/NRA-IDE_Architecture_public.py
```

Its generated docs mirror is:

```text
docs/NRA-IDE_Architecture_public.py
```

The two files must remain byte-identical. Location alone does not confer conformance. Run the current reference suite:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest tests.test_nra_ide_reference -v
```

The current canonical reference suite contains 38 tests covering boundary states, invalid inputs, threshold aliases, irreversible latching, testimony, double fluctuation, two remaining margins, log separation, warning behavior, directional auxiliary calculation, extreme numeric inputs, the Pre-NRA input gate, end-to-end pipeline output suppression, Effect-Side output marking, DiscardVault copy behavior, reserved-status protection, strict latch/trend/threshold type validation, DynamicTauEngine configuration and directional-input rejection, directional output integration, public helper and legacy alias behavior, and source/mirror identity.

Add focused regression tests when changing behavior. Do not introduce an external dependency unless its need, scope, licensing, and reproducibility impact have been reviewed.

Other scripts, demos, papers, and visualizations are research, explanatory, illustrative, domain-specific, or historical unless a higher-precedence canonical record explicitly promotes them.

## Push Gate Setup (Malware / Unicode Boundary Gate)

The initial gate implementation uses `.githooks/pre-push` to invoke `scripts/push_gate.py check`. It requires a prepared inspection plan through `NRA_PUSH_PLAN`; missing, changed, malformed, multi-destination, multi-ref, or non-HEAD-source plans block the request. A plan is inspection data, not execution permission or proof of human approval. Continue to follow [AGENTS.md](./AGENTS.md) and [RULES_DETAIL.md](./RULES_DETAIL.md) for fresh fetch, review of the entire outgoing range, final push approval, and post-push reconciliation.

The hook is not activated by editing files. Each clone needs the existing opt-in configuration, normally set by its owner:

```powershell
git config core.hooksPath .githooks
```

Python and `pwsh` (PowerShell 7+) are required. The preparation step fingerprints the implementation, operating contract, and Unicode/ID policies and baselines; required files must exist. Standalone Unicode diagnostics may omit a baseline, but a prepared push plan must bind the tracked baseline explicitly.

### Prepare, review, then invoke Git

After committing the intended changes and freshly fetching the target remote, prepare a new plan. Replace the uppercase placeholders below. `SECONDS` is an explicit trial timeout, not a calibrated production default. Use a new output filename for each preparation; an existing reviewed plan is not silently overwritten.

```text
python -B scripts/push_gate.py prepare --remote REMOTE_NAME --branch refs/heads/BRANCH_NAME --output local_reports/push-plan-RUN_ID.json --timeout-seconds SECONDS
```

The preparer checks local fetch evidence, source HEAD, target/base OIDs, outgoing commits, runtime identity, and rule fingerprints. It does not fetch, infer the user's intended commit scope, issue approval, or push. Compare the displayed plan and complete outgoing range with the authorized task and obtain the final approval required by AGENTS.md. Then pass that plan to the same Git process:

```powershell
$env:NRA_PUSH_PLAN = 'local_reports/push-plan-RUN_ID.json'
git push REMOTE_NAME HEAD:refs/heads/BRANCH_NAME
```

If HEAD, the destination, expected remote OID, fetch evidence, base, or rules change, prepare/review the changed target rather than bypassing the gate. After a successful real push, fetch again and confirm remote OID equals local HEAD and the planned source OID, with ahead/behind `0 0`. No real shared-remote push is part of the initial implementation verification.

### What is inspected

- `malware_gate.py` produces a schema 2 manifest covering newly reachable blobs and changed original path/mode occurrences, including reused content and intermediate-only blobs. Capacity is checked from metadata before blob reads. Task-owned hardlinks expose only newly reachable blobs under the validated `av/` scan directory; hardlink failure is an unavailable scan.
- `unicode_gate.py --manifest` verifies extraction hashes and coverage and evaluates original paths and bytes, preserving exact baseline matching and per-path text/binary classification. Temporary names do not replace original paths. `--all` remains a supplementary working-tree diagnostic, not proof about the selected push.
- `malware_gate.ps1` checks Unicode first and then invokes Microsoft Defender against that outgoing `av/` directory, not the repository worktree. `PrepareOnly` leaves Malware `NOT_RUN` and cannot satisfy a production push check. A nonzero Defender scan exit is conservatively `UNAVAILABLE` because it may indicate detection or a scan error; it is not labeled confirmed malware from the exit code alone. See [Microsoft's command-line reference](https://learn.microsoft.com/en-us/defender-endpoint/command-line-arguments-microsoft-defender-antivirus).
- `id_gate.py` reads the target commit and also checks unchanged references affected by ID removal or renaming. `check_dictionary.py --head` reads dictionaries and tracked Markdown from the target commit; unrelated dirty or untracked drafts are excluded.

Existing deletion, non-branch-ref, and non-fast-forward prohibitions remain. A new branch requires a fetched remote default branch and a resolvable merge base. Unsupported changed submodules and LFS content block the request rather than triggering unapproved recursive retrieval. Missing tools, invalid coverage/results, timeouts, and failed required checks never become success. Warning-only results are reported without being promoted to failures.

Inspection receipts are stored under `local_reports/push_gate/`; they exclude raw command output and do not constitute a protected approval ledger. Timeout/interruption can require inspection of remaining task processes and temporary directories before cleanup or retry. No automatic hook bypass, permission repair, definition update, or settings change is performed.

### Implementation and verification state

The [design record](./note/06_対話セッション記録/NRA-IDE_gate_enhancement_summary.md) retains contracts K1-K6, acceptance criteria, and historical findings. Initial code and local regression tests are implemented. The related existing 60 tests and added 24 tests passed; native PowerShell preparation and real Git dry-run rejection were also checked. AV success in the automated suite uses a labeled test double. The first harmless native Defender trial returned `UNAVAILABLE` with `DEFENDER_ENVIRONMENT_ERROR`. On recheck, the restricted execution path was denied access to Defender status, while execution outside that restriction completed a native scan of one harmless 41-byte file: Unicode and Malware both `PASS`, exit code 0. No protection settings were changed. Native scanning is therefore confirmed for that execution context; operation through the restricted path, complete acceptance, timeout calibration, and production readiness remain unresolved.

The [operation-approval module](./skills/operation-approval/README.md) remains a separate first-stage component, without live host/pre-push approval integration. Its `valid=true` is not execution permission. It supports an explicit single refspec to an existing branch and rejects new branches; the gate's new-branch inspection does not extend that module. Broker integration, external settings, CI, and branch protection are separate later work.

## Domain Rules and Thresholds

The invariant order is:

```text
0 <= R_warn < R_handoff < R_irrev < 1.0
```

`R_handoff` is canonical. `R_op`, `Rop`, and `rop` are backward-compatibility aliases for the same threshold only.

Concrete threshold values are domain-specific. Define their target, units, evidence, provenance, uncertainty, version, and update authority before use. Do not infer missing values from examples, LLM output, similarity, or another regime. A threshold embedded in a historical script does not automatically become a current domain rule.

High-risk domain changes require independent domain validation and qualified human responsibility. Passing repository tests does not establish medical, engineering, legal, or operational suitability.

## Working-Tree and Git Discipline

- Preserve existing user changes and unrelated dirty-worktree content.
- Do not rewrite historical or RAW evidence merely to make it resemble current canonical wording; classify it explicitly instead.
- Inspect the active branch and repository instructions before choosing a target branch. Do not assume that a branch name in an old document is current.
- For AI-agent work, show the target and operation required by `AGENTS.md` before file writes, command execution, stage, commit, push, deletion, movement, force operations, or history changes.
- Do not stage, commit, push, force-push, rebase, reset, delete branches, or rewrite history without the required explicit authorization.
- Keep commits scoped and describe only work actually performed.

## Pull Requests

Before opening a pull request:

- identify the canonical or domain rule governing the change;
- list the files intentionally changed;
- describe validation actually executed and its result;
- disclose compatibility aliases and migrations;
- distinguish canonical changes from research, example, or historical changes;
- state limitations and high-risk implications without claiming unestablished safety or suitability;
- confirm the intended target branch from the current repository state.

Use the repository's current contribution and authorship policy if one is explicitly present. Do not invent commit trailers or branch requirements from historical examples.

## Questions and Sensitive Reports

Use the repository's current GitHub issue or security-reporting path when available. Do not publish credentials, tokens, private data, or exploitable security details in a public issue.
