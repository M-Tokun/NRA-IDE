[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
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
foreach ($group in $grouped) {
    $displayName = if ($group.Name -eq '_root') { 'リポジトリ直下' } else { $group.Name }
    $safeName = ($group.Name -replace '[<>:"/\\|?*]', '_')
    $sectionFileName = '{0:D2}_{1}.md' -f $index, $safeName
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

Write-Output "obsidian-map generated: source_markdown=$($markdownFiles.Count) sections=$($grouped.Count)"
