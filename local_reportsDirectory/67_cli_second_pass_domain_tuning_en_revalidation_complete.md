# 第2次CLI精査 継続報告 67 — `11_domain_tuning_EN.md` 限定再検証完了

## 対象

- `docs/en-US/ai/11_domain_tuning_EN.md`
- 問題・提案報告: `local_reportsDirectory/66_cli_second_pass_pending_domain_tuning_en_revalidation.md`
- 既存完了報告: `local_reportsDirectory/27_cli_second_pass_continuation_domain_tuning_en.md`

## 実施内容

利用者の承認後、報告66で提示した範囲だけを修正した。

1. Chapter 10の接続を、「保証が成立する前提」から条件付き適合特性と非保証範囲の分離へ修正した。
2. Domain Tuningが安全保証を生成せず、適用評価前に完了する外部設計活動である境界を保持した。
3. 人間へ判断・権限を委譲する表現を、Handoff閾値、固定Handoff証言、終端済み経路外の外部人間監査・現場対応へ修正した。
4. 固定Handoff証言と最終固定証言の双方で、LLMによる自由記述の停止説明を禁止した。
5. 医療、航空、言語生成のドメイン固有事項を、旧因果経路内の引渡しではなく外部監査・現場対応へ修正した。
6. 普遍的不変原則を、Cause-SideとEffect-Sideの権限分離、正典状態挙動、証拠、テストへ修正した。
7. Pre-NRA / LLM / Post-NRA の責務分離を、LLMを含み当該構成を宣言するシステムに限定した。
8. 旧Effect-Sideから戻せない要素を、値、正典閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所へ統一した。
9. 自動、手動、人間レビュー、承認、版更新によるimport、名称変更、再構成、再利用を、新旧いずれのCause-Sideについても禁止した。
10. 物理的残存物の新規観測を維持し、旧Effect-Side記録・権威の再利用と分離した。

## 保存した境界

- Domain Tuningは適用評価前に完了する外部設計活動であり、終端済みダイオード経路を継続しない。
- 三つの正典閾値は評価前に根拠とともに固定し、`R = 1` の破断境界と分離する。
- `R = 1` は宣言済み評価の `RUPTURE_BOUNDARY` であり、自然界一般の相転移境界ではない。
- 不可逆ラッチは同一履歴内で、自動、手動、人間レビュー、承認、版更新のいずれでも解除できない。
- 後続評価は独立した新対象、新Cause-Side、新規則、新因果ダイオードから始まる。
- 物理的残存物は独立した新対象の一部として新たに観測できる。

## 検証結果

- 修正後ファイルを全文内部読取りした。
- 見出し数: 20。
- コードフェンス数: 4（対応済み）。
- `what NRA-IDE can guarantee`: 残存なし。
- `those guarantees hold`: 残存なし。
- `delegates judgment to humans`: 残存なし。
- `handed over to humans`: 残存なし。
- `human review required`: 残存なし。
- `authority transfer`: 残存なし。
- `handoff recipient`: 残存なし。
- `irreversible state`: 残存なし。
- 条件付き適合、外部設計活動、固定Handoff証言、外部人間監査、自由記述禁止、正典三閾値、`RUPTURE_BOUNDARY`、不可逆ラッチ、完全な非再利用一覧、物理的残存物、条件付き三層構成、層数に依存しない権限分離を確認した。
- `git diff --check -- docs/en-US/ai/11_domain_tuning_EN.md`: 問題なし。
- Markdownリンク: 0件。
- `python -m unittest tests.test_nra_ide_reference -v`: 17件すべて成功。
- 修正後SHA-256: `6654F9CA8AD2D2512ED8F1D96F76AB21CE9F0EF7CBC8E7C3A71BEB117B8D172D`。

## 保全確認

- stage、commit、pushは実施していない。
- 01～17報告は変更していない。
- 追跡済みPDF `nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf` の既存削除状態を維持した。
- `AXIOMS.md` と `axioms.json` の同期作業は再実行していない。

## 判定

`docs/en-US/ai/11_domain_tuning_EN.md` の限定再検証と承認済み修正は完了した。この1ファイルは第2次CLI精査の完了状態である。
