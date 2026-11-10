param(
    [ValidateRange(1024,65535)][int]$Port = 8037,
    [switch]$PrepareOnly,
    [switch]$NoBrowser,
    [string]$PreparedRun,
    [switch]$ExperimentalLimits,
    [Alias('ActivityPolicy')][string]$WebPolicy,
    [switch]$Offline,
    [ValidateSet('v2','v3')][string]$Package = 'v3',  # v3 = v2 + estándar IEEE 830 y capítulo STSE (aceptados por el docente el 07-11-2026)
    [ValidateRange(1,240)][int]$Minutes = 30,  # duración de la sesión del servidor (un turno de clase)
    [ValidateRange(1,8)][int]$Slots = 4,  # alumnos a la vez (huecos de los servidores llama.cpp)
    [switch]$InProcess  # modelos cargados en el propio proceso (ruta anterior, lenta); por defecto llama.cpp + ranking
)
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
$python = Join-Path $repo '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $python -PathType Leaf)) { throw 'Local Python not found in .venv. Prepare the project environment before starting.' }
$vite = Join-Path $repo 'apps\web\node_modules\vite\bin\vite.js'
if (-not (Test-Path -LiteralPath $vite -PathType Leaf)) { throw 'Local Vite not found. Prepare apps/web dependencies before starting.' }
$nodeCommand = Get-Command node.exe -ErrorAction SilentlyContinue
$node = if ($nodeCommand) { $nodeCommand.Source } else {
    @((Join-Path $env:ProgramFiles 'nodejs/node.exe'), (Join-Path $env:LOCALAPPDATA 'Programs/nodejs/node.exe'), (Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')) | Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } | Select-Object -First 1
}
if (-not $node) { throw 'Local Node not found. Install dependencies before starting.' }
if ($Offline -and $WebPolicy) { throw 'Choose -Offline or an explicit -ActivityPolicy, not both.' }
if (-not $WebPolicy) {
    $policyName = if ($Offline) { 'requirements-study-policy-offline.json' } else { 'requirements-study-policy.json' }
    $WebPolicy = Join-Path $repo ('config/' + $policyName)
}
$run = Join-Path $repo ('.claude-scratch\study-chat-' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8))
if ($PreparedRun) { $run = (Resolve-Path -LiteralPath $PreparedRun).Path }
else { New-Item -ItemType Directory -Path $run | Out-Null }
$web = Join-Path $run 'web-dist'
$index = Join-Path $run 'retrieval-index'
$savedEnvironment = @{}
foreach ($name in @('PYTHONPATH', 'ORALIA_DEMO_CACHE_DIR', 'ORALIA_PACKAGE')) {
    $savedEnvironment[$name] = @{
        Exists = Test-Path -LiteralPath "Env:$name"
        Value = [Environment]::GetEnvironmentVariable($name, 'Process')
    }
}
Push-Location $repo
try {
    $env:PYTHONPATH = Join-Path $repo 'src'
    $env:ORALIA_DEMO_CACHE_DIR = Join-Path $run 'vite-cache'
    $env:ORALIA_PACKAGE = $Package
    if ($PreparedRun) {
        & $python -m oralia.documentary.study_preparation validate $run
        if ($LASTEXITCODE -ne 0) { throw 'Prepared run invalid or stale. Prepare again explicitly.' }
        Write-Host '[CPU] Reusing verified interface and retrieval index; no rebuild.'
    } else {
        Write-Host '[CPU] Preparing isolated interface and retrieval index.'
        Push-Location (Join-Path $repo 'apps\web')
        try { & $node 'node_modules/vite/bin/vite.js' build --outDir $web }
        finally { Pop-Location }
        if ($LASTEXITCODE -ne 0) { throw 'Interface build failed.' }
        & $python -c 'import sys; from pathlib import Path; from oralia.documentary.retrieval import Retrieval; Retrieval(root=Path(sys.argv[1]), build=True, selection_profile=sys.argv[2])' $index 'comparison-coverage/v1'
        if ($LASTEXITCODE -ne 0) { throw 'CPU retrieval preparation failed.' }
        & $python -m oralia.documentary.study_preparation create $run
        if ($LASTEXITCODE -ne 0) { throw 'Preparation receipt failed.' }
    }
    $runtimeOutput = if ($PrepareOnly) { Join-Path $run 'runtime' } else { Join-Path $run ('launches/' + [guid]::NewGuid().ToString('N') + '/runtime') }
    if (-not $PrepareOnly) {
        $workingIndex = Join-Path (Split-Path -Parent $runtimeOutput) 'retrieval-index'
        & $python -m oralia.documentary.study_preparation materialize $run $workingIndex
        if ($LASTEXITCODE -ne 0) { throw 'Working index could not be copied from verified preparation.' }
        $index = $workingIndex
    }
    $launchArgs = @('-m','oralia.documentary','--package',$Package,'--retrieval','--retrieval-root',$index,'--study-lab','--study-chat','--study-coverage','--runtime-output',$runtimeOutput,'--runtime-seconds',"$($Minutes * 60)",'--web-root',$web,'--port',"$Port")
    $launchArgs += if ($InProcess) { '--reviewed-provider' } else { @('--llama-provider','--modern-retrieval','--llama-concurrency',"$Slots") }
    if ($ExperimentalLimits) { $launchArgs += '--experimental-limits' }
    if ($WebPolicy) {
        $policyPath = (Resolve-Path -LiteralPath $WebPolicy).Path
        $activityPolicy = Get-Content -LiteralPath $policyPath -Raw -Encoding utf8 | ConvertFrom-Json
        if (-not $activityPolicy.activity_scope) { throw 'The activity policy must declare its explicit scope.' }
        $launchArgs += @('--activity-policy', $policyPath, '--local-first-provider')
    }
    if ($NoBrowser) { $launchArgs += '--no-browser' }
    if (-not $PreparedRun) { @{ python=$python; arguments=$launchArgs; run=$run; requires_gpu=$true } | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $run 'launch.json') -Encoding utf8 }
    if ($PrepareOnly) { Write-Host "[CPU] Ready. No GPU or generative model loaded. Output: $run"; return }
    if ($InProcess) { Write-Host '[GPU] Starting generator and reviewer in-process. Requires free GPU capacity; no foreign process will be stopped.' }
    else {
        Write-Host '[GPU] Starting local services (reviewer Mistral-24B, generator Qwen2.5-14B, ranking); no foreign process will be stopped.'
        & (Join-Path $PSScriptRoot 'llama-servers.ps1') start -Slots $Slots
    }
    Write-Host "Open http://127.0.0.1:$Port/estudio ; Ctrl+C stops owned services."
    & $python @launchArgs
    if ($LASTEXITCODE -ne 0) { throw "Study chat ended with code $LASTEXITCODE. Output: $run" }
}
finally {
    Pop-Location
    foreach ($name in $savedEnvironment.Keys) {
        if ($savedEnvironment[$name].Exists) {
            [Environment]::SetEnvironmentVariable($name, $savedEnvironment[$name].Value, 'Process')
        } else {
            Remove-Item -LiteralPath "Env:$name" -ErrorAction SilentlyContinue
        }
    }
}
