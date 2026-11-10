"""Real PowerShell launcher checks; no generative model or GPU invocation."""

import json
import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
POWERSHELL = shutil.which("pwsh")


@pytest.mark.skipif(not POWERSHELL, reason="PowerShell required")
@pytest.mark.parametrize("missing", ["python", "vite"])
def test_missing_dependencies_fail_before_scratch_or_environment_changes(tmp_path, missing):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copyfile(ROOT / "scripts/study-chat.ps1", scripts / "study-chat.ps1")
    if missing == "vite":
        interpreter = tmp_path / ".venv/Scripts/python.exe"
        interpreter.parent.mkdir(parents=True)
        interpreter.write_text("not executed: dependency preflight only", encoding="utf8")
    harness = tmp_path / "check.ps1"
    harness.write_text(
        "$env:PYTHONPATH = 'CALLER_PYTHONPATH'\n"
        "$env:ORALIA_DEMO_CACHE_DIR = 'CALLER_CACHE'\n"
        "$before = (Get-Location).Path\n"
        "$errorText = $null\n"
        "try { & (Join-Path $PSScriptRoot 'scripts/study-chat.ps1') -PrepareOnly -NoBrowser }\n"
        "catch { $errorText = $_.Exception.Message }\n"
        "@{ error=$errorText; python=$env:PYTHONPATH; cache=$env:ORALIA_DEMO_CACHE_DIR; "
        "sameLocation=((Get-Location).Path -eq $before) } | ConvertTo-Json\n",
        encoding="utf8",
    )
    result = subprocess.run(
        [POWERSHELL, "-NoProfile", "-File", str(harness)],
        capture_output=True,
        text=True,
        check=True,
        timeout=20,
    )
    row = json.loads(result.stdout)
    assert ("Python" if missing == "python" else "Vite") in row["error"]
    assert row["python"] == "CALLER_PYTHONPATH" and row["cache"] == "CALLER_CACHE"
    assert row["sameLocation"] and not (tmp_path / ".claude-scratch").exists()


@pytest.mark.skipif(not POWERSHELL, reason="PowerShell required")
@pytest.mark.parametrize("value", [None, "", "CALLER_VALUE"])
def test_failed_build_restores_present_or_absent_environment_without_running_python(tmp_path, value):
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copyfile(ROOT / "scripts/study-chat.ps1", scripts / "study-chat.ps1")
    interpreter = tmp_path / ".venv/Scripts/python.exe"
    interpreter.parent.mkdir(parents=True)
    interpreter.write_text("must never be executed", encoding="utf8")
    vite = tmp_path / "apps/web/node_modules/vite/bin/vite.js"
    vite.parent.mkdir(parents=True)
    vite.write_text("process.exit(7);", encoding="utf8")
    initialize = (
        "Remove-Item -LiteralPath Env:PYTHONPATH,Env:ORALIA_DEMO_CACHE_DIR -ErrorAction SilentlyContinue\n"
        if value is None
        else f"$env:PYTHONPATH = '{value}'\n$env:ORALIA_DEMO_CACHE_DIR = '{value}'\n"
    )
    harness = tmp_path / "check.ps1"
    harness.write_text(
        initialize + "$beforePythonExists = Test-Path Env:PYTHONPATH\n"
        "$beforeCacheExists = Test-Path Env:ORALIA_DEMO_CACHE_DIR\n"
        "$beforePython = [Environment]::GetEnvironmentVariable('PYTHONPATH','Process')\n"
        "$beforeCache = [Environment]::GetEnvironmentVariable('ORALIA_DEMO_CACHE_DIR','Process')\n"
        "$before = (Get-Location).Path\n$errorText = $null\n"
        "try { & (Join-Path $PSScriptRoot 'scripts/study-chat.ps1') -PrepareOnly -NoBrowser }\n"
        "catch { $errorText = $_.Exception.Message }\n"
        "@{ error=$errorText; python=[Environment]::GetEnvironmentVariable('PYTHONPATH','Process'); "
        "cache=[Environment]::GetEnvironmentVariable('ORALIA_DEMO_CACHE_DIR','Process'); "
        "samePresence=((Test-Path Env:PYTHONPATH) -eq $beforePythonExists -and "
        "(Test-Path Env:ORALIA_DEMO_CACHE_DIR) -eq $beforeCacheExists); "
        "sameValues=([Environment]::GetEnvironmentVariable('PYTHONPATH','Process') -ceq $beforePython "
        "-and [Environment]::GetEnvironmentVariable('ORALIA_DEMO_CACHE_DIR','Process') -ceq $beforeCache); "
        "sameLocation=((Get-Location).Path -eq $before) } | ConvertTo-Json\n",
        encoding="utf8",
    )
    completed = subprocess.run(
        [POWERSHELL, "-NoProfile", "-File", str(harness)],
        capture_output=True,
        text=True,
        check=True,
        timeout=20,
    )
    # Ignore the host progress line, retaining the harness's structured result.
    row = json.loads(completed.stdout[completed.stdout.index("{") :])
    assert row["error"] == "Interface build failed."
    assert row["samePresence"] and row["sameValues"]
    assert row["sameLocation"]
    assert len(list((tmp_path / ".claude-scratch").glob("study-chat-*"))) == 1


@pytest.mark.skipif(
    not POWERSHELL or not os.environ.get("ORALIA_STUDY_PREPARATION_TESTS"),
    reason="Explicit real CPU index/build preparation, no generative models",
)
def test_real_prepare_only_restores_caller_environment(tmp_path):
    harness = ROOT / "docs/audits/2026-11-02-cpu-launcher/check-environment.ps1"
    result_path = tmp_path / "preparation-result.json"
    result = subprocess.run(
        [POWERSHELL, "-NoProfile", "-File", str(harness), "-Output", str(result_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=180,
    )
    row = json.loads(result_path.read_text(encoding="utf-8-sig"))
    assert result.returncode == 0, result.stdout + result.stderr
    assert row["scriptError"] is None
    assert row["pythonPathRestored"] and row["cacheRestored"] and row["locationRestored"]
    assert "No GPU or generative model loaded" in result.stdout
    prepared = Path(re.findall(r"Output: (.+)", result.stdout)[-1].strip())
    from oralia.documentary.study_preparation import artifacts

    before = artifacts(prepared)
    reused = subprocess.run(
        [
            POWERSHELL,
            "-NoProfile",
            "-File",
            str(ROOT / "scripts/study-chat.ps1"),
            "-PrepareOnly",
            "-NoBrowser",
            "-PreparedRun",
            str(prepared),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=90,
    )
    assert reused.returncode == 0, reused.stdout + reused.stderr
    assert "Reusing verified" in reused.stdout and "Preparing isolated" not in reused.stdout
    assert "Loading weights" not in reused.stderr and not (prepared / "runtime").exists()
    assert artifacts(prepared) == before
    launch = json.loads((prepared / "launch.json").read_text(encoding="utf-8-sig"))
    assert "--experimental-limits" not in launch["arguments"]
    assert "--local-first-provider" in launch["arguments"]
    assert "--activity-policy" in launch["arguments"]
