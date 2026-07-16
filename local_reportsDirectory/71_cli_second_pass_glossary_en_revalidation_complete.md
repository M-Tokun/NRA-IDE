# 第2次CLI精査 継続報告 71 — `12_glossary_EN.md` 限定再検証完了

## 対象

- `docs/en-US/ai/12_glossary_EN.md`
- 問題・提案報告: `local_reportsDirectory/70_cli_second_pass_pending_glossary_en_revalidation.md`
- 既存完了報告: `local_reportsDirectory/25_cli_second_pass_continuation_glossary_en.md`

## 実施内容

利用者の承認後、報告70で提示した範囲だけを修正した。

1. `R_handoff`、`HANDOFF_REQUIRED`、Fail-Closed、Discard Log、最小整合表を、固定Handoff証言と終端済み経路外の外部人間監査へ統一した。
2. `Fixed-Schema Handoff Notification` を互換実装名称として固定Handoff証言の定義内へ移し、判断、責任、構造権威を旧経路内で移送しないと明記した。
3. 固定Handoff証言と最終固定証言の双方で、LLMによる自由記述の停止説明を禁止した。
4. 医療、航空、言語生成のドメイン固有事項を、旧因果経路内の引渡しではなく外部監査・現場対応へ修正した。
5. `Sandwich Architecture` を、LLMを含み三層構成を宣言するシステムに限定した。
6. 三層の層数だけでは適合を判定せず、正典挙動、Cause-Side / Effect-Side権限分離、証拠、テストに依存すると明記した。
7. Roles、`Pi-inverse`、Cause-Side、Effect-Side、Discard Log、Design changeの非再利用一覧を、値、正典閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所へ統一した。
8. 自動、手動、人間レビュー、承認、版更新によるimport、名称変更、再構成、再利用を、新旧いずれのCause-Sideについても禁止した。
9. 物理的残存物の新規観測を維持し、旧Effect-Side記録・権威の持越しと分離した。
10. LLMの正確さ、事実性、利用者適合性を `NRA-IDE guarantees` の範囲外とする表現を、NRA-IDEによって保証されないという直接表現へ修正した。

## 保存した境界

- 公理は「Existence is generation.」というNomological Ring Axiom一つだけであり、第二公理以降は存在しない。
- Primary Formulaは宣言対象の構造状態を正典の数学的関係へ落とす根本式であり、派生式、安全指標、局所計器ではない。
- Secondary / Dual-Fluctuation FormulaはPrimary Formulaとともに正典IDE計算系を構成するが、公理ではない。
- IDEは計算方法・動力学エンジンであり、安全保証でもIntegrated Development Environmentでもない。
- `delta`は履歴を持つ蓄積偏差、`tau`は吸収厚さである。
- 三つの正典閾値と`R = 1`の`RUPTURE_BOUNDARY`を分離する。
- 因果ダイオードはCause-SideからEffect-Sideへの完全な一方向である。
- 旧経路はEffect-Sideで終端し、後続履歴は独立した新対象、新Cause-Side、新規則、新因果ダイオードから始まる。

## 検証結果

- 修正後ファイルを全文内部読取りした。
- 見出し数: 20。
- コードフェンス数: 2（対応済み）。
- `delegate judgment to humans`: 残存なし。
- `transfer responsibility to a qualified human`: 残存なし。
- `hand the matter over`: 残存なし。
- `required human review` / `human review required`: 残存なし。
- `human handoff`: 残存なし。
- `authority transfer`: 残存なし。
- `handoff recipient`: 残存なし。
- `scope of NRA-IDE guarantees`: 残存なし。
- 唯一の公理、Primary Formula、Secondary / Dual-Fluctuation Formula、IDE、因果ダイオード、正典七状態、固定Handoff証言、外部人間監査、不可逆ラッチ、完全な非再利用一覧、物理的残存物、条件付き三層構成を確認した。
- `git diff --check -- docs/en-US/ai/12_glossary_EN.md`: 問題なし。
- Markdownリンク: 0件。
- `python -m unittest tests.test_nra_ide_reference -v`: 17件すべて成功。
- 修正後SHA-256: `708AF8DF1F918F57E8E5CC8D122C5BE8CCE740B6D121A7A3FC4230549C6624CE`。

## 保全確認

- stage、commit、pushは実施していない。
- 01～17報告は変更していない。
- 追跡済みPDF `nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf` の既存削除状態を維持した。
- `AXIOMS.md` と `axioms.json` の同期作業は再実行していない。

## 判定

`docs/en-US/ai/12_glossary_EN.md` の限定再検証と承認済み修正は完了した。この1ファイルは第2次CLI精査の完了状態である。
