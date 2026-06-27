# WORKFILES_INDEX.md — 作業対象ファイルインデックス
<!-- FILE: WORKFILES_INDEX.md / 2026-06-27 17:12 JST -->
<!-- このファイルは、現在の書込みスコープを明示する。AGENTS.md の権限を拡張しない。 -->

## 0. 運用原則

- 本ファイルは、現在の作業セッションにおける `confirmed` な対象候補を記録する。
- Scope in this file records confirmed candidate targets for the current task session.
- ここに書かれたファイルでも、`AGENTS.md` と `RULES_DETAIL.md` の承認条件は別途必要である。
- Files listed here are not automatically authorized for edit, shell execution, Git operations, network use, or external sending.
- セッション終了後は、対象を Archived Scopes へ移し、Current Scope を空に戻す（人間が行う）。
- AIは、自身の判断でCurrent Scopeを広げてはならない。
- ステータスは `active` / `archived` のみ使用する。承認はユーザーの会話発言が証跡となるため、ファイル上のチェックボックスや proposed 状態は使わない。

`Confirmed: Editable` は、編集対象候補を意味する。実際の編集には、正確な対象、目的、影響範囲を示したうえで確認キー `w` が必要である。

`Confirmed: Read-Only` は読取対象候補を意味する。読取にシェル、スクリプト、外部ツールが必要な場合は、確認キー `r` または該当する確認キーが別途必要である。

## 1. Current Scope

**Task ID:** `AGENT-GOVERNANCE-20260627-V2`  
**Purpose:** AIエージェント共通統治の一本化、公開Web探索境界の新設、および探索方法を固定しない採用条件の明文化。  
**Status:** `active`

### Confirmed: Editable

- `AGENTS.md`
- `RULES_DETAIL.md`
- `WEB_RESEARCH_PROTOCOL.md`
- `CLAUDE.md`
- `GEMINI.md`
- `CLINE.md`
- `CODEX.md`
- `.clinerules`
- `.cursorrules`
- `WORKFILES_INDEX.md`
- `REPOSITORY_OVERVIEW.md`

### Confirmed: Read-Only

- `llms.md`
- `README.md`
- `README_JP.md`
- `CONTRIBUTING.md`

### Explicitly Out of Scope

- `src/`
- `config/`
- `scripts/`
- `.github/`
- package manifests and lockfiles
- medical, multi-physics, parser, example, and theory implementation files
- Git staging area, commits, pushes, releases

## 2. Archived Scopes

### `2026-0624 誤解発生源の修正`

旧スコープとして記録する。再開する場合は、新しいTask IDで対象と目的を再確定する。

- `AGENTS.md`
- `RULES_DETAIL.md`
- `llms.md`
- `note/NRA-IDE_FPGA_Implementation_2026-03-14_2157.md`
- `nra-ide-cancer-treatment-support-system/jp/NRA-IDE_Cancer_Treatment_Support_System/00_Documentation/PHASE_6_FPGA_Spec.md`
- `multi-physics-safety-gate/Multi-Physics_Safety_Gate_Architecture_JP.md`
- `multi-physics-safety-gate/Multi-Physics_Safety_Gate_Architecture_EN.md`

## 3. Scope Change Request

Current Scopeにない対象が必要になった場合、AIは停止し、次を示して利用者へ申請する。

1. 追加したい正確なパス
2. 必要な理由
3. 想定する操作
4. 影響範囲
5. 代替としてREAD-ONLYで済ませられない理由
