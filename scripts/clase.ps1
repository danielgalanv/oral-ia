# Arranca el autoestudio para una clase con UN comando y lo vigila hasta que termine.
#   .\scripts\clase.ps1                 -> usa config\clase.json (hosts publicos, minutos, huecos)
#   .\scripts\clase.ps1 -Minutes 150    -> fuerza la duracion
#   .\scripts\clase.ps1 -SoloLocal      -> sin acceso publico (alumnos delante de este ordenador)
# Comprueba GPU libre, registro de avisos vacio, servicios sanos (velocidad), servicio de Cloudflare y acceso publico.
# No para ningun proceso ajeno. Ctrl+C termina la clase y para los servicios del proyecto.
param(
    [int]$Minutes = 0,
    [int]$Slots = 0,
    [switch]$SoloLocal,
    [switch]$IgnorarGpu
)
$ErrorActionPreference = 'Stop'
$env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')  # Node recien instalado
$repo = Split-Path -Parent $PSScriptRoot
$python =Join-Path $repo '.venv\Scripts\python.exe'
$configPath = Join-Path $repo 'config\clase.json'
$config = if (Test-Path $configPath) { Get-Content $configPath -Raw | ConvertFrom-Json } else { $null }
$port = if ($config -and $config.port) { [int]$config.port } else { 8037 }
if ($Minutes -le 0) { $Minutes = if ($config -and $config.minutes) { [int]$config.minutes } else { 120 } }
if ($Slots -le 0) { $Slots = if ($config -and $config.slots) { [int]$config.slots } else { 4 } }
$public = (-not $SoloLocal) -and $config -and $config.hosts -and $config.team -and $config.aud
$log = Join-Path $env:TEMP 'oralia-clase.log'

function Fail($text) { Write-Host "ERROR: $text" -ForegroundColor Red; exit 1 }
function Ok($text) { Write-Host "  [OK] $text" -ForegroundColor Green }
function Warn($text) { Write-Host "  [!!] $text" -ForegroundColor Yellow }
function Health { try { Invoke-RestMethod "http://127.0.0.1:$port/health" -TimeoutSec 5 } catch { $null } }

Write-Host "== Preparando la clase (duracion $Minutes min, $Slots alumnos a la vez) =="
if (-not (Test-Path $python)) { Fail 'Falta el entorno .venv del proyecto.' }
if (-not (Get-Command node.exe -ErrorAction SilentlyContinue)) { Fail 'Node no esta en el PATH (abre una terminal nueva).' }

# 1. GPU libre (los servicios de otros proyectos no se tocan: se pide cerrarlos)
$used = [int](nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
if ($used -gt 3000 -and -not $IgnorarGpu) { Fail "La GPU tiene $used MiB ocupados por otros procesos (ComfyUI, otro llama-server...). Cierralos y repite; el sistema no cabe junto a ellos." }
Ok "GPU libre ($used MiB en uso)"

# 2. Registro de avisos vacio (solo datos reales de la clase)
$registro = Join-Path $repo 'registro-avisos\avisos.jsonl'
if ((Test-Path $registro) -and ((Get-Content $registro | Measure-Object -Line).Lines -gt 0)) {
    Warn "registro-avisos tiene entradas: si son de prueba, vacialo con  python scripts\avisos_docente.py purgar todo"
} else { Ok 'Registro de avisos vacio' }

# 3. Entorno de acceso publico
if ($public) {
    $env:ORALIA_PUBLIC_HOSTS = ($config.hosts -join ',')
    $env:ORALIA_ACCESS_TEAM = $config.team
    $env:ORALIA_ACCESS_AUD = $config.aud
    if ($config.email_suffix) { $env:ORALIA_EMAIL_SUFFIX = $config.email_suffix }
    Ok "Acceso publico configurado para $($config.hosts -join ', ')"
} else {
    Warn 'Sin acceso publico (modo local: http://127.0.0.1 solo en este ordenador).'
}

# 4. Arranque con reintento si el generador sale lento (GPU compartida)
$proc = $null
for ($attempt = 1; $attempt -le 3; $attempt++) {
    & (Join-Path $PSScriptRoot 'llama-servers.ps1') stop | Out-Null
    Start-Sleep 8
    Write-Host "== Arrancando servicios (intento $attempt) =="
    $proc = Start-Process powershell -WindowStyle Hidden -PassThru -RedirectStandardOutput $log -RedirectStandardError "$log.err" -ArgumentList @(
        '-NoProfile', '-File', ('"' + (Join-Path $PSScriptRoot 'study-chat.ps1') + '"'), '-NoBrowser', '-Port', $port, '-Slots', $Slots, '-Minutes', ($Minutes + 10))
    $deadline = (Get-Date).AddMinutes(8)
    while ((Get-Date) -lt $deadline -and -not $proc.HasExited -and -not (Health)) { Start-Sleep 5 }
    if ($proc.HasExited) { Warn 'El servidor se paro al arrancar; ultimas lineas del registro:'; Get-Content "$log.err" -Tail 5; continue }
    $slow = Select-String -Path $log -Pattern 'ADVERTENCIA' -Quiet
    if ($slow) { Warn 'Un servidor arranco lento (GPU compartida); reinicio.'; Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue; continue }
    break
}
$h = Health
if (-not $h -or $h.status -ne 'ok') {
    $detalle = if ($h) { ($h.services | ConvertTo-Json -Compress) } else { 'sin respuesta' }
    Fail "El sistema no esta sano ($detalle). Revisa $log"
}
Ok "Servicios sanos: $($h.services | ConvertTo-Json -Compress)"

# 5. Tunel y acceso publico
if ($public) {
    $svc = Get-Service -Name 'Cloudflared' -ErrorAction SilentlyContinue
    if ($svc -and $svc.Status -eq 'Running') { Ok 'Servicio Cloudflared en marcha' } else { Fail 'El servicio Cloudflared no esta en marcha (inicialo y repite).' }
    foreach ($hostName in $config.hosts) {
        try {
            $r = Invoke-WebRequest "https://$hostName/estudio" -MaximumRedirection 0 -UseBasicParsing -TimeoutSec 15 -ErrorAction Stop
            $code = [int]$r.StatusCode
        } catch { $code = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 0 } }
        if ($code -in 301, 302, 303, 307, 401, 403) { Ok "https://$hostName responde (codigo $code, pide identificacion de Cloudflare Access)" }
        elseif ($code -eq 200) { Warn "https://$hostName responde 200 SIN pedir identificacion: revisa la politica de Access antes de abrir la clase." }
        else { Fail "https://$hostName no responde (codigo $code): revisa la ruta del tunel hacia http://localhost:$port" }
    }
}

$fin = (Get-Date).AddMinutes($Minutes)
Write-Host ''
Write-Host '=================================================================' -ForegroundColor Green
if ($public) { Write-Host "  LISTO. Los alumnos entran en: https://$($config.hosts[0])/estudio" -ForegroundColor Green }
else { Write-Host "  LISTO (local). Abre http://127.0.0.1:$port/estudio" -ForegroundColor Green }
Write-Host "  La sesion termina sobre las $($fin.ToString('HH:mm')). Ctrl+C para terminar antes." -ForegroundColor Green
Write-Host '=================================================================' -ForegroundColor Green

# 6. Vigilancia
$bad = 0
try {
    while (-not $proc.HasExited) {
        Start-Sleep 30
        $h = Health
        $alumnos = if ($null -ne $h.students) { $h.students } else { 'n/d (modo local)' }
        $turnos = if ($null -ne $h.turns_in_progress) { $h.turns_in_progress } else { 'n/d' }
        $line = if ($h) { "{0}  estado={1} alumnos={2} turnos_en_curso={3}" -f (Get-Date -Format 'HH:mm:ss'), $h.status, $alumnos, $turnos } else { "{0}  SIN RESPUESTA" -f (Get-Date -Format 'HH:mm:ss') }
        if ($h -and $h.status -eq 'ok') { $bad = 0; Write-Host $line } else {
            $bad++
            Write-Host "$line  <-- PROBLEMA ($bad)" -ForegroundColor Red
            if ($bad -ge 2) { [console]::beep(1000, 600); Write-Host '  Un servicio no responde. Mira docs\CLASE.md (que hacer si algo falla).' -ForegroundColor Red }
        }
    }
    Write-Host 'La sesion del servidor ha terminado.' -ForegroundColor Yellow
}
finally {
    if (-not $proc.HasExited) { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue }
    & (Join-Path $PSScriptRoot 'llama-servers.ps1') stop | Out-Null
    Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'oralia\.documentary' -and $_.Name -match 'python' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
    Write-Host 'Servicios del proyecto parados.'
}
