[CmdletBinding()]
param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$resolvedRoot = (Resolve-Path -LiteralPath $RepoRoot).Path.TrimEnd([char[]]@('\', '/'))
$examplesRoot = Join-Path $resolvedRoot 'examples'

if (-not (Test-Path -LiteralPath $examplesRoot)) {
    throw "examples/ ディレクトリが見つかりません: $examplesRoot"
}

$indexFiles = @('README.md', 'README_JP.md', 'index.html')

function Get-LocalHtmlLinks {
    param([Parameter(Mandatory)][string]$Text)

    $links = New-Object System.Collections.Generic.List[string]

    foreach ($m in [regex]::Matches($Text, '\]\(([^)]+?\.html)\)')) {
        $links.Add($m.Groups[1].Value)
    }
    foreach ($m in [regex]::Matches($Text, 'href="([^"]+?\.html)"')) {
        $links.Add($m.Groups[1].Value)
    }

    return $links | Where-Object { $_ -notmatch '^https?://' }
}

$brokenLinks = @()
$referencedNames = New-Object System.Collections.Generic.HashSet[string]

foreach ($indexFile in $indexFiles) {
    $path = Join-Path $examplesRoot $indexFile
    if (-not (Test-Path -LiteralPath $path)) {
        Write-Warning "索引ファイルが見つかりません: $indexFile"
        continue
    }

    $text = Get-Content -LiteralPath $path -Raw -Encoding UTF8
    foreach ($link in (Get-LocalHtmlLinks -Text $text)) {
        $resolvedTarget = Join-Path $examplesRoot $link
        if (-not (Test-Path -LiteralPath $resolvedTarget)) {
            $brokenLinks += [PSCustomObject]@{ IndexFile = $indexFile; Link = $link }
        }

        # examples/ 直下のファイルへの参照だけを孤立検出の対象にする
        # (../docs/... のような examples/ 外へのリンクは対象外)
        if ($link -notmatch '/' -or $link.StartsWith('./')) {
            $baseName = Split-Path -Leaf $link
            [void]$referencedNames.Add($baseName)
        }
    }
}

$actualFiles = Get-ChildItem -LiteralPath $examplesRoot -Filter '*.html' -File |
    Where-Object { $_.Name -ne 'index.html' } |
    Select-Object -ExpandProperty Name

$orphanFiles = $actualFiles | Where-Object { -not $referencedNames.Contains($_) } | Sort-Object

Write-Output '=== examples/ リンク整合性チェック ==='
Write-Output ''

if ($brokenLinks.Count -eq 0) {
    Write-Output "[OK] リンク切れなし(索引3点が参照する examples/ 内リンクは全て実在)"
} else {
    Write-Output "[NG] リンク切れ $($brokenLinks.Count) 件:"
    foreach ($b in $brokenLinks) {
        Write-Output "  - $($b.IndexFile) -> $($b.Link)"
    }
}

Write-Output ''

if ($orphanFiles.Count -eq 0) {
    Write-Output '[OK] 孤立ファイルなし(examples/ 直下の .html は全て索引3点のいずれかから参照されている)'
} else {
    Write-Output "[WARN] 孤立ファイル $($orphanFiles.Count) 件(README.md / README_JP.md / index.html のどこからも参照されていません):"
    foreach ($o in $orphanFiles) {
        Write-Output "  - $o"
    }
}

Write-Output ''
Write-Output "summary: broken=$($brokenLinks.Count) orphan=$($orphanFiles.Count) checked_files=$($actualFiles.Count)"

if ($brokenLinks.Count -gt 0) {
    exit 1
}
