param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('TaskStart', 'TaskResume', 'PreToolUse', 'PostToolUse')]
    [string] $Event
)
$ErrorActionPreference = 'Stop'
try {
    [Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
    [Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $rawInput = [Console]::In.ReadToEnd()
    $python = Get-Command python -CommandType Application -ErrorAction Stop
    $scriptName = switch ($Event) {
        'PreToolUse' { 'cline_guard.py' }
        'PostToolUse' { 'cline_mark.py' }
        default { 'cline_session_start.py' }
    }
    $scriptPath = Join-Path $PSScriptRoot $scriptName
    $captured = @($rawInput | & $python.Source -B $scriptPath 2>$null)
    if ($LASTEXITCODE -ne 0) { throw 'Guard process failed' }
    $json = ($captured -join "`n")
    # A successful PostToolUse may have no output and does not authorize actions.
    if ([string]::IsNullOrWhiteSpace($json)) {
        if ($Event -ne 'PostToolUse') { throw 'Missing guard result' }
        $result = @{ cancel = $false; contextModification = ''; errorMessage = '' }
    } else {
        $result = $json | ConvertFrom-Json -ErrorAction Stop
        if ($null -eq $result -or $result.cancel -isnot [bool]) { throw 'Invalid guard result' }
        if ($null -ne $result.contextModification -and $result.contextModification -isnot [string]) { throw 'Invalid context' }
        if ($null -ne $result.errorMessage -and $result.errorMessage -isnot [string]) { throw 'Invalid error' }
    }
    [Console]::Out.WriteLine(($result | ConvertTo-Json -Depth 10 -Compress))
    exit 0
} catch {
    [Console]::Out.WriteLine('{"cancel":true,"contextModification":"","errorMessage":"Cline contract hook failed; operation blocked."}')
    exit 0
}
