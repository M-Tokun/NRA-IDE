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
# 33番の内部案内も検査する。他のサブプロジェクトを再帰走査する指定ではない。
$documentFiles = $indexFiles + @(
    '33_boundary_and_history/README.md',
    '33_boundary_and_history/01_simultaneous_boundary_JP.html',
    '33_boundary_and_history/02_pre_rupture_history_JP.html'
)

function Get-LocalDocumentLinks {
    param([Parameter(Mandatory)][AllowEmptyString()][string]$Text)

    $links = New-Object System.Collections.Generic.List[string]

    foreach ($m in [regex]::Matches($Text, '\]\(([^)]+)\)')) {
        $links.Add($m.Groups[1].Value)
    }
    foreach ($m in [regex]::Matches($Text, '(?i)\bhref\s*=\s*["'']([^"'']+)["'']')) {
        $links.Add($m.Groups[1].Value)
    }

    foreach ($raw in $links) {
        $link = [System.Net.WebUtility]::HtmlDecode($raw.Trim())
        # Markdownの <path> と任意の引用符付きタイトルを分離する。
        if ($link -match '^<([^>]+)>') {
            $link = $Matches[1]
        } else {
            $link = $link -replace '\s+["''].*$', ''
        }
        # 外部URLやページ内アンカーはローカルファイルの存在検査に含めない。
        if ($link -match '^(?:[a-z][a-z0-9+.-]*:|//|#)') { continue }
        $pathPart = ($link -split '[?#]', 2)[0]
        if ($pathPart -notmatch '\.(?:html|md)$') { continue }
        [PSCustomObject]@{
            Link = $raw
            Path = [System.Uri]::UnescapeDataString($pathPart)
        }
    }
}

$brokenLinks = @()
$referencedNames = New-Object System.Collections.Generic.HashSet[string]
$checkedDocuments = 0
$checkedLinks = 0

foreach ($documentFile in $documentFiles) {
    $path = Join-Path $examplesRoot $documentFile
    # 検査対象が欠落したまま「リンク切れなし」と報告しない。
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        $brokenLinks += [PSCustomObject]@{ IndexFile = $documentFile; Link = '(検査対象ファイルがありません)' }
        continue
    }

    $checkedDocuments++
    $sourceDirectory = Split-Path -Parent $path
    $text = Get-Content -LiteralPath $path -Raw -Encoding UTF8
    # Get-Content -Raw は空ファイルで null を返すことがある。
    foreach ($link in (Get-LocalDocumentLinks -Text ([string]$text))) {
        $checkedLinks++
        $resolvedTarget = [System.IO.Path]::GetFullPath((Join-Path $sourceDirectory $link.Path))
        if (-not (Test-Path -LiteralPath $resolvedTarget -PathType Leaf)) {
            $brokenLinks += [PSCustomObject]@{ IndexFile = $documentFile; Link = $link.Link }
        }

        # 孤立検出の意味は維持する。索引3点から直下HTMLへの参照だけを数える。
        if (($indexFiles -contains $documentFile) -and
            ([System.IO.Path]::GetDirectoryName($resolvedTarget) -eq $examplesRoot) -and
            ([System.IO.Path]::GetExtension($resolvedTarget) -eq '.html')) {
            $baseName = Split-Path -Leaf $resolvedTarget
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
    Write-Output "[OK] リンク切れなし(索引3点と33番の3文書から参照するローカルHTML/MD)"
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
Write-Output "summary: broken=$($brokenLinks.Count) orphan=$($orphanFiles.Count) checked_files=$($actualFiles.Count) checked_documents=$checkedDocuments checked_links=$checkedLinks"

if ($brokenLinks.Count -gt 0) {
    exit 1
}
