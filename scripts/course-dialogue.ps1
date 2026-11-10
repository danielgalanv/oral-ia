[CmdletBinding()]
param([switch]$InspectCandidates, [switch]$NaturalProbe, [switch]$ControlledDrafts, [ValidateSet("cached-cuda","ollama")][string]$Provider="cached-cuda", [ValidateRange(1024,65535)][int]$Port=11436, [ValidateSet("7b-nf4","14b-nf4")][string]$DraftModel="7b-nf4", [ValidateSet(1,2,3,4,5,6,7)][int]$SemanticVersion=1)
$ErrorActionPreference='Stop'
if (-not $InspectCandidates) { throw 'Perfil generativo no aprobado. Para revisar candidatas sintéticas use -InspectCandidates; no es una sesión de participante.' }
$dialogueWorkspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw 'Falta uv local; no se descargará nada.' }
Push-Location -LiteralPath $dialogueWorkspace
try {
    $dialogueArgs=@("--inspect-candidates","--provider",$Provider)
    if ($PSBoundParameters.ContainsKey("Port")) { $dialogueArgs+=@("--port",$Port) }
    if ($NaturalProbe) { $dialogueArgs+="--natural-probe" }
    if ($ControlledDrafts) { $dialogueArgs+="--controlled-drafts" }
    if ($PSBoundParameters.ContainsKey("DraftModel")) { $dialogueArgs+=@("--draft-model",$DraftModel) }
    if ($PSBoundParameters.ContainsKey("SemanticVersion")) { $dialogueArgs+=@("--semantic-version",$SemanticVersion) }
    & uv run --offline --no-sync python -X utf8 -m oralia.course_dialogue @dialogueArgs
    if ($LASTEXITCODE -ne 0) { throw "La inspección terminó con código $LASTEXITCODE; revise el diagnóstico propio." }
} finally { Pop-Location }




