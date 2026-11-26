# Cline 4.1.22 Windows hook: 利用者の入力を合言葉の機械判定（skills/prompt-gate）へ渡す。
# Resolve helper independently of the current directory.
# 入力は止めない（cancel は常に false）。失敗時は承認が作られないだけで、commit・push は止まる（安全側）。
$ErrorActionPreference = 'Stop'
try {
    [Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
    # 診断用：呼ばれたことだけを記録する（入力の本文は記録しない）。記録の失敗は無視する。
    try {
        $logDir = Join-Path $repoRoot '.agent_state\hooks'
        New-Item -ItemType Directory -Force -Path $logDir | Out-Null
        Add-Content -Path (Join-Path $logDir 'prompt_gate_cline_ps1.log') -Value ((Get-Date -Format 'o') + ' invoked') -Encoding UTF8
    } catch { }
    $rawInput = [Console]::In.ReadToEnd()
    $python = Get-Command python -CommandType Application -ErrorAction Stop
    $gate = Join-Path $repoRoot 'skills\prompt-gate\cline_prompt_gate.py'
    $json = (@($rawInput | & $python.Source -B $gate 2>$null) -join "`n")
    if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($json)) { throw 'Gate failed' }
    $result = $json | ConvertFrom-Json -ErrorAction Stop
    if ($null -eq $result -or $result.cancel -isnot [bool]) { throw 'Invalid gate result' }
    [Console]::Out.WriteLine(($result | ConvertTo-Json -Depth 10 -Compress))
    exit 0
} catch {
    [Console]::Out.WriteLine('{"cancel":false,"contextModification":"","errorMessage":"prompt_gate hook unavailable; no approval was created."}')
    exit 0
}
