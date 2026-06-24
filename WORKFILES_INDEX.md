# WORKFILES_INDEX.md — 作業対象ファイルインデックス

このファイルは、エージェントがアクセス・編集を許可された「確定（Confirmed）」スコープを定義します。ここに記載のないファイルへの書き込みは原則禁止（Fail-Closed）されます。

## 1. 現在の作業セッション (Current Session Scope)
*期間・タスク名: 2026-0624 誤解発生源の修正*

### 編集許可ファイル (Confirmed: Editable)
- [ ] `AGENTS.md` — エージェント最小限カーネルの管理
- [ ] `RULES_DETAIL.md` — 詳細規則の管理
- [ ] `llms.md` — NRA-IDE構造推論規則の管理
- [ ] `note/NRA-IDE_FPGA_Implementation_2026-03-14_2157.md` — 「浮動小数点禁止」をFPGA実装限定に修正
- [ ] `nra-ide-cancer-treatment-support-system/jp/NRA-IDE_Cancer_Treatment_Support_System/00_Documentation/PHASE_6_FPGA_Spec.md` — 「浮動小数点不使用」をFPGA実装限定に修正
- [ ] `multi-physics-safety-gate/Multi-Physics_Safety_Gate_Architecture_JP.md` — δ_SNR/τ_SNR にR≡SNR否定の注記追加
- [ ] `multi-physics-safety-gate/Multi-Physics_Safety_Gate_Architecture_EN.md` — 同上（英語版）

### 読み取り専用ファイル (Confirmed: Read-Only)
- [ ] `README.md`
- [ ] `package.json` (存在する場合、構造確認用)

## 2. 完了済みスコープ (Archived Scopes)
*(過去のセッションで解放され、現在は保護対象に戻ったファイル群をここに記録)*

## 3. 免責・運用ルール
1. 本ファイルに明記されたファイル以外の編集が必要になった場合、エージェントは必ず事前に停止し、「とおくに」さんに本ファイルの更新を申請すること。
2. セッション終了時、または新しいタスクへ移行する際は、本ファイルの「現在の作業セッション」を更新（あるいはクリア）し、不要な書き込み権限を速やかに剥奪すること。
