# NRA-IDE Obsidian 接続図

このディレクトリは、NRA-IDEリポジトリ内のMarkdownをObsidianのグラフビューで俯瞰するための索引を置きます。

既存のMarkdown本文にはリンクを追加しません。`00_NRA-IDE接続図.md`と`sections/`から既存文書へリンクすることで、原文を維持したまま構造上の接続を作ります。

## 開き方

1. Obsidianを起動します。
2. 「保管庫としてフォルダーを開く」を選びます。
3. `G:\git-M-Tokun\AI-IDE-NRA\NRA-IDE`を指定します。
4. `obsidian-map/00_NRA-IDE接続図.md`を開きます。
5. リボンから「グラフビューを開く」を選びます。

## 再生成

リポジトリルートで次を実行します。

```powershell
pwsh -File scripts/generate_obsidian_map.ps1
```

スクリプトはGitで追跡されているMarkdownを取得し、`obsidian-map/`を除外したうえで、トップレベルディレクトリ単位に索引化します。未追跡の作業用Markdownは接続図へ混入しません。

## グラフの色分け例

グラフ設定の「グループ」で、次の検索条件を追加すると領域別に色分けできます。

- `path:theory`
- `path:nra-core/foundations`
- `path:nra-core`
- `path:note`
- `path:ground`
- `path:examples`
- `path:obsidian-map`

色はObsidian側のグラフ設定で割り当てます。`.obsidian/`はローカル設定としてGitの追跡対象から除外します。
