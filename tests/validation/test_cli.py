import json
import subprocess
import sys


def test_cli_runs_isolated_catalog_and_replays_then_rejects_existing_output(tmp_path):
    directory = tmp_path / "evidence"
    command = [
        sys.executable,
        "-m",
        "oralia.validation",
        "run",
        "--output",
        str(directory),
        "--repetitions",
        "1",
        "--seed",
        "12",
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    data = json.loads((directory / "results.json").read_text(encoding="utf-8"))
    assert len(data["cells"]) == 34
    replay = subprocess.run(
        [sys.executable, "-m", "oralia.validation", "replay", "--package", str(directory)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert replay.returncode == 0, replay.stderr
    assert '"matched": true' in replay.stdout
    again = subprocess.run(command, capture_output=True, text=True, timeout=10)
    assert again.returncode != 0
    assert "must be new" in again.stderr
