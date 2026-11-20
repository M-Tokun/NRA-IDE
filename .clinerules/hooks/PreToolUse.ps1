# Cline 4.1.22 Windows hook: AGENTS.md 読込ガード → 作業ルート外ガードの順に実行する。
# Resolve helper independently of the current directory. Any failure blocks the operation.
$ErrorActionPreference = 'Stop'
try {
    [Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
    $rawInput = [Console]::In.ReadToEnd()
    $python = Get-Command python -CommandType Application -ErrorAction Stop
    $chain = Join-Path $repoRoot 'skills\outside-root-guard\cline_pre_chain.py'
    $json = (@($rawInput | & $python.Source -B $chain 2>$null) -join "`n")
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($json)) { throw 'Guard chain failed' }
    $result = $json | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $result -or $result.cancel -isnot [bool]) { throw 'Invalid guard result' }
    [Console]::Out.WriteLine(($result | ConvertTo-Json -Depth 10 -Compress))
    exit 0
} catch {
    [Console]::Out.WriteLine('{"cancel":true,"contextModification":"","errorMessage":"Cline contract hook unavailable; operation blocked."}')
    exit 0
}
