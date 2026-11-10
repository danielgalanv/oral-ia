[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
$demoCheckWorkspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$demoCheckOutput = Join-Path $demoCheckWorkspace '.claude-scratch/demo-checks'
New-Item -ItemType Directory -Path $demoCheckOutput -Force | Out-Null
$demoCheckRun = Join-Path $demoCheckOutput (Get-Date -Format 'yyyyMMdd-HHmmss')
New-Item -ItemType Directory -Path $demoCheckRun | Out-Null
$demoCheckResults = @()
Push-Location -LiteralPath $demoCheckWorkspace
try {
    # Tests use their own temporary resources; never reset the prepared demo.
    & uv run --offline --no-sync pytest tests/demo -q 2>&1 |
        Tee-Object -FilePath (Join-Path $demoCheckRun 'recovery.log')
    $demoCheckResults += @{ check = 'recovery-and-isolation'; exit_code = $LASTEXITCODE }
    & pnpm.cmd --dir apps/web exec playwright test --config ../../tests/e2e/playwright.config.ts test_demo_journey.spec.ts 2>&1 |
        Tee-Object -FilePath (Join-Path $demoCheckRun 'journey.log')
    $demoCheckResults += @{ check = 'browser-demo-journey'; exit_code = $LASTEXITCODE }
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'demo.ps1') -Action Check 2>&1 |
        Tee-Object -FilePath (Join-Path $demoCheckRun 'preflight.log')
    $demoCheckResults += @{ check = 'prepared-demo-preflight'; exit_code = $LASTEXITCODE }
    $demoCheckPassed = @($demoCheckResults | Where-Object { $_.exit_code -ne 0 }).Count -eq 0
    @{ completed_at = (Get-Date).ToString('o'); passed = $demoCheckPassed; checks = $demoCheckResults } |
        ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $demoCheckRun 'result.json') -Encoding utf8
    Write-Output "Informe: $demoCheckRun"
    if (-not $demoCheckPassed) { throw 'Una comprobación falló; consultar los logs del informe.' }
} finally { Pop-Location }
