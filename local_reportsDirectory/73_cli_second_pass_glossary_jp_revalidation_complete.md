# 第2次CLI精査 継続報告 73 — `12_glossary_JP.md` 限定再検証完了

## 対象

- `docs/ja-JP/ai/12_glossary_JP.md`
- 問題・提案報告: `local_reportsDirectory/72_cli_second_pass_pending_glossary_jp_revalidation.md`
- 既存完了報告: `local_reportsDirectory/26_cli_second_pass_continuation_glossary_jp.md`
- 対訳側完了報告: `local_reportsDirectory/71_cli_second_pass_glossary_en_revalidation_complete.md`

## 実施内容

利用者の承認後、報告72で提示した範囲だけを修正した。

1. `R_handoff`、`HANDOFF_REQUIRED`、Fail-Closed、廃棄ログ、最小整合表を、固定Handoff証言と終端済み経路外の外部人間監査へ統一した。
2. 「固定スキーマの委譲通知」を旧実装名称として固定Handoff証言の定義内へ移し、判断、責任、構造権威を旧経路内で移送しないと明記した。
3. 固定Handoff証言と最終固定証言の双方で、LLMによる自由記述の停止説明を禁止した。
4. 医療、航空、言語生成のドメイン固有事項を、旧因果経路内の引渡しではなく外部監査・現場対応へ修正した。
5. 「サンドイッチ構造」を、LLMを含み三層構成を宣言するシステムに限定した。
6. 三層の層数だけでは適合を判定せず、正典挙動、Cause-Side / Effect-Side権限分離、証拠、テストに依存すると明記した。
7. 役割、`Pi-inverse`、Cause-Side、Effect-Side、廃棄ログ、設計変更の非再利用一覧を、値、正典閾値、状態、不可逆ラッチ、規則、変換入力、更新根拠、出所へ統一した。
8. 自動、手動、人間レビュー、承認、版更新によるimport、名称変更、再構成、再利用を、新旧いずれのCause-Sideについても禁止した。
9. 物理的残存物の新規観測を維持し、旧Effect-Side記録・権威の持越しと分離した。
10. LLMの正確性、事実性、利用者適合性を「NRA-IDE単独の保証範囲外」とする表現を、NRA-IDEによって保証されないという直接表現へ修正した。

## 保存した境界

- 公理は「存在は生成である。」という律環公理一つだけであり、第二公理以降は存在しない。
- 基礎式は宣言対象の構造状態を正典の数学的関係へ落とす根本式であり、派生式、安全指標、局所計器ではない。
- 第二次式／二重ゆらぎ式は基礎式とともに正典IDE計算系を構成するが、公理ではない。
- IDEは計算方法・動力学エンジンであり、安全保証でも統合開発環境でもない。
- `delta`は履歴を持つ蓄積偏差、`tau`は吸収厚さである。
- 三つの正典閾値と`R = 1`の`RUPTURE_BOUNDARY`を分離する。
- 因果ダイオードはCause-SideからEffect-Sideへの完全な一方向である。
- 旧経路はEffect-Sideで終端し、後続履歴は独立した新対象、新Cause-Side、新規則、新因果ダイオードから始まる。

## 検証結果

- 修正後ファイルを全文内部読取りした。
- 見出し数: 16。
- コードフェンス数: 2（対応済み）。
- 「人間へ判断を渡す」: 残存なし。
- 「資格ある人間へ責任を移す」: 残存なし。
- 「人間へ渡す」: 残存なし。
- 「必要な人間確認」: 残存なし。
- 「人間への委譲」: 残存なし。
- 「権限移譲」: 残存なし。
- 「委譲先」: 残存なし。
- 「NRA-IDE単独の保証範囲外」: 残存なし。
- 唯一の公理、基礎式、第二次式／二重ゆらぎ式、IDE、因果ダイオード、正典七状態、固定Handoff証言、外部人間監査、不可逆ラッチ、完全な非再利用一覧、物理的残存物、条件付き三層構成を確認した。
- 英語版とIntensional Dynamics Engine、Causal Diode、正典七状態、Handoff、Pre-NRA、Post-NRAを照合し、日本語版ではPrimary Formulaに対応する正典名称「基礎式」を確認した。
- `git diff --check -- docs/ja-JP/ai/12_glossary_JP.md`: 問題なし。
- Markdownリンク: 0件。
- `python -m unittest tests.test_nra_ide_reference -v`: 17件すべて成功。
- 修正後SHA-256: `BD4D873627B6EF9CA971C40A78C3D1B1EC6DDA9371D85DFE293B0CFA8EA8E9BA`。

## 保全確認

- stage、commit、pushは実施していない。
- 01～17報告は変更していない。
- 追跡済みPDF `nra-core/foundations/AXIOMS_rewritten_2026-04-24_011508.pdf` の既存削除状態を維持した。
- `AXIOMS.md` と `axioms.json` の同期作業は再実行していない。

## 判定

`docs/ja-JP/ai/12_glossary_JP.md` の限定再検証と承認済み修正は完了した。この1ファイルは第2次CLI精査の完了状態である。
