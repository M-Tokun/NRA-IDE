[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'

# Git はリポジトリ内のパスを UTF-8 で出力する。コンソール出力エンコーディングが
# UTF-8 でない環境（例: Windows の日本語ロケールで CP932）では、その出力が別の
# エンコーディングとしてデコードされ、日本語ファイル名が文字化けする。
# 読み取り側を UTF-8 に固定し、後段のパス存在確認と合わせて文字化けの混入を防ぐ。
try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
} catch {
    Write-Warning "Could not switch console output encoding to UTF-8: $($_.Exception.Message)"
}
$resolvedRoot = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd([char[]]@('\', '/'))
$mapRoot = Join-Path $resolvedRoot 'obsidian-map'
$sectionsRoot = Join-Path $mapRoot 'sections'
$utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function ConvertTo-EncodedMarkdownPath {
    param([Parameter(Mandatory)][string]$Path)

    return (($Path -split '/') | ForEach-Object {
        [System.Uri]::EscapeDataString($_)
    }) -join '/'
}

function ConvertTo-MarkdownLabel {
    param([Parameter(Mandatory)][string]$Text)

    return $Text.Replace('\', '\\').Replace('[', '\[').Replace(']', '\]')
}

function Write-GeneratedFile {
    param(
        [Parameter(Mandatory)][string]$Path,
        [Parameter(Mandatory)][AllowEmptyString()][string[]]$Lines
    )

    $content = ($Lines -join "`n") + "`n"
    [System.IO.File]::WriteAllText($Path, $content, $utf8NoBom)
}

$markdownFiles = @(
    git -c core.quotepath=false -C $resolvedRoot ls-files -- '*.md' |
        Where-Object {
            -not $_.StartsWith('obsidian-map/', [System.StringComparison]::OrdinalIgnoreCase)
        } |
        Sort-Object
)

if ($LASTEXITCODE -ne 0) {
    throw 'Git could not enumerate tracked Markdown files.'
}

# 復号に失敗したパスは作業ツリー上に存在しない。文字化けした索引を書き出す前に停止する。
$undecodablePaths = @($markdownFiles | Where-Object {
    -not (Test-Path -LiteralPath (Join-Path $resolvedRoot $_.Replace('/', [System.IO.Path]::DirectorySeparatorChar)))
})

if ($undecodablePaths.Count -gt 0) {
    throw "Git listed $($undecodablePaths.Count) path(s) that do not exist in the working tree (first: $($undecodablePaths[0]))."
}

New-Item -ItemType Directory -Path $sectionsRoot -Force | Out-Null

$grouped = $markdownFiles | Group-Object {
    $slash = $_.IndexOf('/')
    if ($slash -lt 0) { '_root' } else { $_.Substring(0, $slash) }
} | Sort-Object Name

$masterLines = @(
    '# NRA-IDE Markdown 接続図',
    '',
    '> このノートと `sections/` は `scripts/generate_obsidian_map.ps1` による生成物です。既存の Markdown 本文は変更しません。',
    '',
    "対象 Markdown: $($markdownFiles.Count) ファイル",
    '',
    '## セクション',
    ''
)

$index = 1
$generatedSections = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)

foreach ($group in $grouped) {
    $displayName = if ($group.Name -eq '_root') { 'リポジトリ直下' } else { $group.Name }
    $safeName = ($group.Name -replace '[<>:"/\\|?*]', '_')
    $sectionFileName = '{0:D2}_{1}.md' -f $index, $safeName
    $generatedSections.Add($sectionFileName) | Out-Null
    $encodedSectionPath = ConvertTo-EncodedMarkdownPath "sections/$sectionFileName"
    $masterLines += "- [$displayName]($encodedSectionPath) — $($group.Count) ファイル"

    $sectionLines = @(
        "# $displayName",
        '',
        '[← NRA-IDE Markdown 接続図](../00_NRA-IDE%E6%8E%A5%E7%B6%9A%E5%9B%B3.md)',
        '',
        "対象 Markdown: $($group.Count) ファイル",
        ''
    )

    foreach ($relativePath in $group.Group) {
        $label = ConvertTo-MarkdownLabel $relativePath
        $encodedTarget = ConvertTo-EncodedMarkdownPath "../../$relativePath"
        $sectionLines += "- [$label]($encodedTarget)"
    }

    Write-GeneratedFile -Path (Join-Path $sectionsRoot $sectionFileName) -Lines $sectionLines
    $index++
}

# セクション番号はトップレベルディレクトリ名の並び順に依存するため、ディレクトリの
# 追加・削除で以前の番号のファイルが残る。生成対象から外れたものは削除して重複を防ぐ。
$staleSections = @(Get-ChildItem -LiteralPath $sectionsRoot -File -Filter '*.md' | Where-Object {
    -not $generatedSections.Contains($_.Name)
})

foreach ($staleSection in $staleSections) {
    Remove-Item -LiteralPath $staleSection.FullName -Force
    Write-Output "removed stale section: $($staleSection.Name)"
}

$masterLines += @(
    '',
    '## 表示方法',
    '',
    '1. Obsidian でこのリポジトリを保管庫として開きます。',
    '2. リボンの「グラフビューを開く」を選びます。',
    '3. グラフ設定で「既存ファイルのみ」を有効にします。',
    '4. 必要に応じて `path:theory`、`path:nra-core`、`path:note`、`path:examples` などをグループへ追加します。',
    '',
    '[生成・運用ガイド](README.md)'
)

Write-GeneratedFile -Path (Join-Path $mapRoot '00_NRA-IDE接続図.md') -Lines $masterLines

Write-Output "obsidian-map generated: source_markdown=$($markdownFiles.Count) sections=$($grouped.Count) stale_removed=$($staleSections.Count)"
