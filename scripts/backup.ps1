# Copia de seguridad: bundle de git (todo el historial) + binarios docentes y registro de avisos que git no guarda.
# Uso: .\scripts\backup.ps1 [-Destino 'E:\copias-oralia']   (por defecto ..\ORALIA-backup\<fecha>)
# Mejor copia final en OTRO disco o servicio: esta misma carpeta en el mismo disco no protege de un fallo del disco.
param([string]$Destino)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
if (-not $Destino) { $Destino = Join-Path (Split-Path -Parent $root) ('ORALIA-backup\' + (Get-Date -Format 'yyyy-MM-dd')) }
New-Item -ItemType Directory -Force $Destino | Out-Null
Push-Location $root
try {
    if (git status --porcelain) { Write-Warning 'Hay cambios sin commit: el bundle solo incluye lo ya confirmado. Haz commit antes.' }
    git bundle create (Join-Path $Destino 'oralia.bundle') --all
    $files = @(Get-ChildItem -Recurse -File -Path 'materiales' | Where-Object { $_.FullName -match '\originales\' -or $_.Extension -eq '.zip' }) +
             @(Get-ChildItem -Recurse -File -Path 'registro-avisos' -ErrorAction SilentlyContinue)
    $zip = Join-Path $Destino 'materiales-originales.zip'
    if (Test-Path $zip) { Remove-Item $zip }
    Compress-Archive -Path ($files | ForEach-Object { $_.FullName }) -DestinationPath $zip -CompressionLevel Optimal
    Get-FileHash (Join-Path $Destino 'oralia.bundle'), $zip -Algorithm SHA256 | ForEach-Object { "$($_.Hash.ToLower())  $(Split-Path -Leaf $_.Path)" } | Set-Content (Join-Path $Destino 'SHA256SUMS.txt')
    "Copia en $Destino"
} finally { Pop-Location }
