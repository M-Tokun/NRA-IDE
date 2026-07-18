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

The current suite contains 27 tests covering boundary states, invalid inputs, threshold aliases, irreversible latching, testimony, double fluctuation, two remaining margins, log separation, warning behavior, directional auxiliary calculation, extreme numeric inputs, the Pre-NRA input gate, end-to-end pipeline output suppression, Effect-Side output marking, DiscardVault copy behavior, reserved-status protection, strict latch/trend/threshold type validation, DynamicTauEngine configuration and directional-input rejection, directional output integration, public helper and legacy alias behavior, and source/mirror identity.

Add focused regression tests when changing behavior. Do not introduce an external dependency unless its need, scope, licensing, and reproducibility impact have been reviewed.

Other scripts, demos, papers, and visualizations are research, explanatory, illustrative, domain-specific, or historical unless a higher-precedence canonical record explicitly promotes them.

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
