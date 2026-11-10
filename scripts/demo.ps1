[CmdletBinding()]
param(
    [ValidateSet('Start', 'Check', 'Stop', 'Reset')][string]$Action = 'Start',
    [ValidateRange(1024, 65535)][int]$ApiPort = 8010,
    [ValidateRange(1024, 65535)][int]$WebPort = 5180,
    [switch]$NoBrowser,
    [switch]$TextOnly,
    [switch]$Documentary,
    [ValidateRange(1024, 65535)][int]$DocumentaryPort = 8022,
    [ValidateSet('v1.1', 'v2')][string]$DocumentaryPackage = 'v1.1'
)
$ErrorActionPreference = 'Stop'
$workspacePath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if ($Documentary) {
    if ($Action -ne 'Start') { throw 'El perfil documental se detiene con Ctrl+C en su terminal; no usa Stop ni Reset de la demo.' }
    $documentaryPython = Join-Path $workspacePath '.venv/Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $documentaryPython)) { throw 'Falta el entorno Python local existente.' }
    $documentaryArgs = @('-X', 'utf8', '-m', 'oralia.documentary', '--port', $DocumentaryPort, '--package', $DocumentaryPackage)
    if ($NoBrowser) { $documentaryArgs += '--no-browser' }
    Push-Location -LiteralPath $workspacePath
    try {
        & $documentaryPython @documentaryArgs
        if ($LASTEXITCODE -ne 0) { throw "La consulta documental terminó con código $LASTEXITCODE." }
    } finally { Pop-Location }
    return
}
$demoOriginalPath = $env:PATH
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw 'Falta uv. Instálelo y prepare uv sync --extra dev.' }
if (-not (Test-Path -LiteralPath (Join-Path $workspacePath '.venv/Scripts/python.exe'))) {
    throw 'Falta el entorno local. Ejecute uv sync --extra dev antes de iniciar la demo.'
}
$demoArgs = @('run', '--offline', '--no-sync', 'python', '-X', 'utf8', '-m', 'oralia.demo', $Action.ToLower(), '--api-port', $ApiPort, '--web-port', $WebPort)
if ($NoBrowser) { $demoArgs += '--no-browser' }
if ($TextOnly) { $demoArgs += '--text-only' }
Push-Location -LiteralPath $workspacePath
try {
    # The desktop agent has an augmented PATH; an ordinary terminal may not.
    # Reuse an installed Node only for this invocation. Never install or persist PATH.
    if (-not (Get-Command node.exe -ErrorAction SilentlyContinue)) {
        $demoNodeCandidates = @(
            (Join-Path $env:ProgramFiles 'nodejs/node.exe'),
            (Join-Path $env:LOCALAPPDATA 'Programs/nodejs/node.exe'),
            (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
        )
        $demoNode = $demoNodeCandidates | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
        if ($demoNode) {
            $env:PATH = (Split-Path -Parent $demoNode) + [IO.Path]::PathSeparator + $env:PATH
            Write-Host '[RECURSO LOCAL] Node existente localizado; PATH temporal, sin instalaciones.'
        }
    }
    # Python getpass reads the credential privately, or a process-only ORALIA_DEMO_ADMIN_SECRET.
    # No secret is serialized into arguments, files, logs or frontend configuration.
    & uv @demoArgs
    if ($LASTEXITCODE -ne 0) { throw "La demo terminó con código $LASTEXITCODE. Revise el mensaje anterior." }
} finally {
    $env:PATH = $demoOriginalPath
    Pop-Location
}
