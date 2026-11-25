---
id: INDEX-README-20261022
kind: doc
created: 2026-10-22
title: obsidian-index：ID索引（Obsidian Bases）の説明
status: record
---

# obsidian-index

Obsidian の標準機能「Bases」で、frontmatter の `id` から文書を探す索引と、`id` 未付与の作業リストを見るためのフォルダ。

- `ID索引.base`：3つのビューを持つ。Obsidian で開く（保管庫 `NRA-IDE` が前提。Basesコアプラグインは有効）。
  - **ID一覧（idあり）**：ID・種別・状態・題名・パスを、IDの昇順で表示
  - **ID未付与の作業リスト**：`id` がない文書を、領域（上位フォルダ）ごとに表示
  - **領域別（idあり）**：`id` がある文書を、領域ごとに表示
- 対象は `.md` のみ。`local_reports`、`local_reportsDirectory`、`obsidian-map` は除外する。

## 確認状況（2026-10-22、利用者の実機）

| ビュー | 結果 |
|---|---|
| ID一覧 | 21件、ID昇順で動作（スクリプトの集計と一致） |
| ID未付与の作業リスト | 312件、領域別に動作（スクリプトの集計と一致） |
| 領域別（idあり） | 22件（ID一覧の21件＋本READMEのid）、領域別に動作 |

## 注意

- **見る側の道具である。** IDの一意性や書式は保証しない。重複・書式の検査は ID Gate（`scripts/id_gate.py`）が行う。
- **`.base` はObsidianが保存のたびに書式を整える**（コメントは残らない）。説明はこのファイルに書く。
- **表のセルを編集すると、そのファイルの frontmatter が書き換わる。** 既存の文書への id の付与は、ファイルごとの許可を得てから行う。
- Obsidian が作る「無題のファイル」（`.canvas`、`.base`、`.md`）が保管庫の直下にできることがある。コミットしない。
- GitHub 上では `.base` は表示されない（Obsidian 専用）。
- 「ID未付与」の件数は、Obsidian が作る空の「無題のファイル.md」などで増えることがある。
