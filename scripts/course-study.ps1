[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$courseWorkspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw 'Falta uv; prepare las dependencias locales.' }
if (-not (Test-Path -LiteralPath (Join-Path $courseWorkspace ".venv/Scripts/python.exe"))) {
    throw "Falta el entorno local. Prepare uv sync --extra dev antes de iniciar el autoestudio."
}
Push-Location -LiteralPath $courseWorkspace
try {
    & uv run --offline --no-sync python -X utf8 -m oralia.course_study
    if ($LASTEXITCODE -ne 0) { throw "El autoestudio terminó con código $LASTEXITCODE; los datos habituales no se han reiniciado." }
} finally { Pop-Location }
