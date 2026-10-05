# Cline 4.1.22 Windows hook; resolve helper independently of the current directory.
$ErrorActionPreference = 'Stop'
try {
    $repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
    $helper = Join-Path $repoRoot 'skills\agents-md-guard\cline_hook.ps1'
    & $helper -Event PostToolUse
} catch {
    [Console]::Out.WriteLine('{"cancel":true,"contextModification":"","errorMessage":"Cline contract hook unavailable; operation blocked."}')
    exit 0
}
