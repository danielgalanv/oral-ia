# Arranca/para los servicios locales del chat, solo en 127.0.0.1: generador 14B :8090, revisor Mistral-24B :8089
# (llama.cpp) y servicio de ranking bge-m3 + reranker :8092 (Python con CUDA; variable ORALIA_RANKER_PYTHON).
# Uso: .\scripts\llama-servers.ps1 start | stop | status
# Requiere .tools\llama.cpp\bin y los GGUF de .tools\models (ver docs/CONTINUAR.md); no descarga nada.
param(
    [ValidateSet('start', 'stop', 'status')][string]$Action = 'status',
    [ValidateRange(1,8)][int]$Slots = 4  # turnos simultáneos (alumnos a la vez); 1 = servidores de un solo hueco
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$bin = Join-Path $root '.tools\llama.cpp\bin\llama-server.exe'
$models = Join-Path $root '.tools\models'
# Entorno propio del ranking (.venv-ranker: torch CUDA); ai-toolkit solo como respaldo.
$ownRanker = Join-Path (Split-Path $PSScriptRoot -Parent) '.venv-ranker\Scripts\python.exe'
$rankerPython = if ($env:ORALIA_RANKER_PYTHON) { $env:ORALIA_RANKER_PYTHON } elseif (Test-Path $ownRanker) { $ownRanker } else { 'D:\ai-toolkit\venv\Scripts\python.exe' }
$rankerScript = Join-Path $PSScriptRoot 'ranker_server.py'
# Orden de arranque: el modelo más grande primero y uno a uno; llama.cpp ajusta las capas a la memoria libre
# y, si arrancara con la GPU más llena, descargaría capas a la CPU (el revisor pasó de 75 a 15 tok/s).
$servers = @(
    @{ Name = 'revisor'; Port = 8089; Model = 'mistral-small-24b-Q4_K_M.gguf'; PerSlot = 12288 },
    @{ Name = 'generador'; Port = 8090; Model = 'qwen25-14b-Q4_K_M.gguf'; PerSlot = 12288 },
    @{ Name = 'ranking'; Port = 8092; Ranker = $true }
)
function Test-Health($port) {
    try { return (Invoke-RestMethod "http://127.0.0.1:$port/health" -TimeoutSec 3).status -eq 'ok' } catch { return $false }
}
switch ($Action) {
    'status' { foreach ($s in $servers) { '{0,-10} :{1}  {2}' -f $s.Name, $s.Port, $(if (Test-Health $s.Port) { 'activo' } else { 'parado' }) } }
    'stop' {
        # Solo procesos lanzados desde esta carpeta de herramientas y el servicio de ranking de este proyecto.
        Get-CimInstance Win32_Process -Filter "Name = 'llama-server.exe'" | Where-Object { $_.ExecutablePath -eq $bin } |
            ForEach-Object { Stop-Process -Id $_.ProcessId -Force; "parado PID $($_.ProcessId)" }
        Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Where-Object { $_.CommandLine -like "*$rankerScript*" } |
            ForEach-Object { Stop-Process -Id $_.ProcessId -Force; "parado PID $($_.ProcessId)" }
    }
    'start' {
        if (-not (Test-Path $bin)) { throw "Falta $bin (ver docs/CONTINUAR.md)" }
        foreach ($s in $servers) {
            if (Test-Health $s.Port) { "$($s.Name): ya activo en :$($s.Port)"; continue }
            if ($s.Ranker) {
                if (-not (Test-Path $rankerPython)) { throw "Falta $rankerPython (Python con CUDA; ORALIA_RANKER_PYTHON)" }
                $log = Join-Path $models 'server-ranker.log'
                Start-Process -FilePath $rankerPython -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError "$log.err" `
                    -ArgumentList @("`"$rankerScript`"", '--port', $s.Port)
            } else {
                $model = Join-Path $models $s.Model
                if (-not (Test-Path $model)) { throw "Falta el modelo $model" }
                $log = Join-Path $models "server-$($s.Port).log"
                $serverArgs = @('-m', "`"$model`"", '-ngl', '99', '-fa', 'on', '--port', $s.Port, '--host', '127.0.0.1', '--jinja', '--cache-reuse', '256')
                if ($Slots -eq 1) { $serverArgs += @('-c', $s.PerSlot, '--parallel', '1') }
                else {
                    # Caché de contexto compartida entre huecos y cuantizada a 8 bits: la memoria total queda como con un hueco.
                    $serverArgs += @('-c', [int]($s.PerSlot * $Slots / 2), '--parallel', $Slots, '--kv-unified', '-ctk', 'q8_0', '-ctv', 'q8_0')
                }
                Start-Process -FilePath $bin -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError "$log.err" -ArgumentList $serverArgs
            }
            $t0 = Get-Date
            while (-not (Test-Health $s.Port)) {
                if (((Get-Date) - $t0).TotalSeconds -gt 300) { throw "$($s.Name) no arrancó; ver el registro" }
                Start-Sleep 2
            }
            if ($s.Ranker) { "$($s.Name): listo en :$($s.Port)"; continue }
            # Comprobación de velocidad: si llama.cpp arrancó con la GPU llena descarga capas a la CPU y va 10 veces más lento
            # sin avisar (el 14B pasó de 120 a 13 tok/s y las respuestas caducaban a los 180 s).
            $body = @{ messages = @(@{ role = 'user'; content = 'Cuenta del 1 al 40 separado por comas.' }); max_tokens = 100; temperature = 0 } | ConvertTo-Json -Depth 4
            $t1 = Get-Date
            $r = Invoke-RestMethod "http://127.0.0.1:$($s.Port)/v1/chat/completions" -Method Post -ContentType 'application/json' -Body $body -TimeoutSec 180
            $rate = [math]::Round($r.usage.completion_tokens / [math]::Max(0.1, ((Get-Date) - $t1).TotalSeconds))
            if ($rate -lt 40) { Write-Warning "$($s.Name): lento ($rate tok/s; lo normal es 90-120). Pare los servicios, libere la GPU y arranque de nuevo." }
            "$($s.Name): listo en :$($s.Port) ($rate tok/s)"
        }
    }
}


