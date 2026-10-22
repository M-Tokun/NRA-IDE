# 量子ハイブリッド用語集 / Quantum-Hybrid Glossary

[日本語]

## 範囲

- 入れるもの：量子計算・SPSA・極低温ハードウェア・QEC などの外部の技術用語と、NRA-IDE との接続で生まれた用語。
- 入れないもの：NRA-IDE の理論用語（`../NRA-IDE_Dictionary_JP.md`・`_EN.md` の範囲）。同じ語が両方にあるときは、正典側の定義を複製せず、リンクで参照する。
- この用語集は非規範である。正典の定義を作らず、変えない。意味または記号が競合する場合は、`theory/AXIOMS.md` 第16節と `FORMULA.md` 第7節に従う。

## 運用の約束（参照切れを防ぐ）

1. 見出しIDは `qh-` で始め、一度公開したら付け直さない。語の訳や説明を変えてもIDは固定する。廃止する語は削除せず、「廃止、代替は #…」と残す。
2. 各項目に、GitHub用のアンカー（`<a id="ID"></a>`）と、Obsidian用のブロックID（最初のリスト行の末尾に ` ^ID`）の両方を置く。Obsidianは見出しの文字かブロックIDでしか移動できず、見出しの文言を直すとリンクが切れるため、項目間のリンクは `#^ID` の形にする。ブロックIDは英字・数字・ハイフンだけ（`_` や日本語は不可）。
3. ファイルの場所とファイル名を変えない。ファイル名は英数字で、空白や `# ^ [ ] |` を含めない（Obsidianでのリンクの不具合を避ける）。フォルダ名は領域名のままとし、版や日付を入れない。
4. 日本語と英語は対で作る。英語は訳語の対応表（`Translation_Map.md`）に従って書く。食い違いを見つけたら、両方を直し、理由を日付つきで残す。確認が済むまで、どちらも「骨格」「概念未照合」の印を外さない。意味・訳語の照合（概念照合済み）と、全欄の英訳の一対一の確認（全文対訳確認済み）は、別の状態として記す。
5. 変更のたびに `python scripts/check_dictionary.py` を実行する（日英のIDの対、アンカーのリンク、IDの不変を検査する）。新しいIDを足したら `--update` で `dictionary/ids.json` に記録する。
6. 考え方の変化は `note/03_…/nra-ide-hybridcalc-quantum-architecture-next_ver/変遷記録.md`（QH-…）に、語の意味と経過はこの用語集に置く。相互にIDで参照する。
7. 記述は、第三者の視点で読める研究用の辞書として書く。「利用者の指摘」のように、人や対話への帰属は書かず、根拠は日付・出典・文書の箇所で示す。

## ファイル

- `Glossary_JP.md`／`Glossary_EN.md`：用語集（見出しIDで対）
- `Translation_Map.md`：訳語の対応表と、すり合わせの経過

[English]

## Scope

- Included: external technical terms (quantum computing, SPSA, cryogenic hardware, QEC, etc.) and terms created where they connect to NRA-IDE.
- Excluded: NRA-IDE theory terms (the scope of `../NRA-IDE_Dictionary_JP.md` / `_EN.md`). When the same word appears in both, link to the canonical side instead of copying its definition.
- This glossary is non-normative. It neither creates nor changes canonical definitions. Where meaning or notation conflicts, `theory/AXIOMS.md` section 16 and `FORMULA.md` section 7 govern.

## Rules (to prevent broken references)

1. Heading IDs start with `qh-` and are never renamed once published. Changing a translation or explanation does not change the ID. A retired term is not deleted; mark it "retired, replaced by #…".
2. Each entry carries both a GitHub anchor (`<a id="ID"></a>`) and an Obsidian block ID (` ^ID` at the end of the entry's first list line). Obsidian can jump only by heading text or block ID, so editing a heading breaks heading-based links; links between entries use the `#^ID` form. Block IDs use only Latin letters, digits, and hyphens (no `_` or Japanese).
3. Do not move or rename files. Use alphanumeric file names with no spaces or `# ^ [ ] |` (avoids link problems in Obsidian). The folder keeps its domain name, with no version or date.
4. Japanese and English are made as a pair. The English follows the translation map (`Translation_Map.md`). When a mismatch is found, fix both sides and record the reason with a date. Until reconciled, neither side drops the "skeleton" / "concepts unreconciled" marks. Reconciling the meaning and terms (concepts reconciled) and checking the English of every field one to one (full text checked) are recorded as separate states.
5. After every change, run `python scripts/check_dictionary.py` (checks JP/EN ID pairs, anchor links, and ID stability). Record new IDs with `--update` in `dictionary/ids.json`.
6. Changes of thought go to `note/03_…/nra-ide-hybridcalc-quantum-architecture-next_ver/変遷記録.md` (QH-…); meanings and history of terms stay here. Cross-reference by ID.
7. Write as a research dictionary readable from a third-party viewpoint. Do not attribute statements to a person or a conversation (for example, "the user's remark"); give the basis by date, source, and location in the documents.

## Files

- `Glossary_JP.md` / `Glossary_EN.md`: the glossary (paired by heading ID)
- `Translation_Map.md`: the translation map and reconciliation log
