# note — 研究・草稿・セッション記録 / Research, Drafts, and Session Records

`note/`は、NRA-IDEの着想、検討過程、AIセッション、公開稿候補、応用案、量子拡張案を保存する研究領域である。ここにあるファイルは、ファイル名に`Official`、`Final`、`確定`、`原則`などを含む場合でも、現在の正典性・現行性・適合性を自動的には持たない。

`note/` preserves ideas, deliberation history, AI sessions, publication candidates, application proposals, and quantum-extension research. A filename containing words such as `Official`, `Final`, or `confirmed` does not make an artifact currently canonical, current, or conforming.

## 現行分類 / Current Classification

- 律環公理は「存在は生成である。」の一つだけであり、第二公理以降は存在しない。
- 一次式と二次式（二重ゆらぎ式）は、公理ではなくIDEの二つの正典計算系である。
- その他の式は派生式、補助式または補完式である。
- `note/`本文にある複数公理、旧公理番号、旧状態、旧Fail-Closed、未検証の応用主張は、現行分類ではなく当時の研究来歴である。

- There is exactly one Nomological Ring Axiom: “Existence is Generation.” No second or subsequent axiom exists.
- The Primary and Secondary / Dual-Fluctuation Formulas are the two canonical IDE calculation systems, not axioms.
- Every other equation is derived, auxiliary, or complementary.
- Multiple axioms, historical axiom numbers, legacy states, legacy Fail-Closed descriptions, and unvalidated application claims inside `note/` preserve research provenance rather than current classification.

## 権威順位 / Authority

- 正典参照順: `../theory/AXIOMS.md` > `../theory/axioms.json` > `../theory/NRA-IDE_Foundational_Thesis_Bilingual.md` > `../theory/SANDWICH_ARCH.md` > `../theory/THEORY.md` > `../FORMULA.md` > `../llms.md` > ドメイン固有規則 > 正典適合試験に合格した正規参照実装 > その他の実装 > コメント・例示・AI生成説明
- 機械可読な正典同期表現: `../theory/axioms.json`
- 正規参照実装ソース: `../nra-core/foundations/NRA-IDE_Architecture_public.py`
- docs同期ミラー: `../docs/NRA-IDE_Architecture_public.py`（正規ソースとSHA-256一致が必要）
- 正典適合試験: `../tests/test_nra_ide_reference.py`（現行17試験）
- `note/`内の資産: 個別に正典へ昇格した記録がない限り、すべて非正規の研究・草稿・履歴資料

- Canonical order: `../theory/AXIOMS.md` > `../theory/axioms.json` > `../theory/NRA-IDE_Foundational_Thesis_Bilingual.md` > `../theory/SANDWICH_ARCH.md` > `../theory/THEORY.md` > `../FORMULA.md` > `../llms.md` > domain-specific rules > normative reference implementation passing canonical conformance tests > other implementation > comments, examples, and AI-generated explanations
- Machine-readable synchronized canonical representation: `../theory/axioms.json`
- Normative reference implementation source: `../nra-core/foundations/NRA-IDE_Architecture_public.py`
- Synchronized docs mirror: `../docs/NRA-IDE_Architecture_public.py` (its SHA-256 must match the normative source)
- Canonical conformance suite: `../tests/test_nra_ide_reference.py` (currently 17 tests)
- Artifacts under `note/`: noncanonical research, draft, or historical material unless a canonical record explicitly promotes one

## 取扱い / Handling

- 歴史的主張、旧語彙、当時の誤りや過大表現は、研究来歴として本文に残り得る。
- 現行仕様の根拠として引用する前に、正典との一致を再検証する。
- 医療、量子、社会、金融などの応用記述は、個別の妥当性検証を経た運用仕様ではない。
- 履歴資料の修正が必要な場合は本文を黙って上書きせず、注記または後続の訂正文書で扱う。

- Historical claims, legacy vocabulary, errors, and overstatements may remain in the body as provenance.
- Revalidate against the canon before citing any note as a current specification.
- Medical, quantum, social, financial, and other application descriptions are not domain-validated operational specifications.
- Correct historical material through a notice or subsequent correction record rather than silently rewriting provenance.

*Authority classification updated: 2026-07-15 JST*
