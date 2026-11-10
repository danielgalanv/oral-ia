import json
from unittest.mock import patch

import pytest

from oralia.validation.protocol import Protocol
from oralia.validation.reporting import render_report, replay, run_experiment, verify_package, write_package


@pytest.mark.asyncio
async def test_package_replays_structurally_and_rejects_tampering(tmp_path):
    protocol = Protocol(conditions=["full"], repetitions=1)
    result = await run_experiment(protocol)
    directory = tmp_path / "new-package"
    write_package(directory, result)
    assert verify_package(directory)["protocol"] == protocol.model_dump()
    reproduced = await replay(directory)
    assert reproduced["matched"]
    with patch("oralia.validation.reporting.code_manifest", return_value={"modified": "code"}):
        with pytest.raises(ValueError, match="code/protocol integrity"):
            verify_package(directory)
    manifest = directory / "manifest.json"
    original_manifest = manifest.read_bytes()
    manifest.write_text(json.dumps({"../outside": "hash"}))
    with pytest.raises(ValueError, match="allowlist"):
        verify_package(directory)
    manifest.write_bytes(original_manifest)
    with pytest.raises(FileExistsError):
        write_package(directory, result)
    f = directory / "protocol.json"
    data = json.loads(f.read_text())
    data["seed"] += 1
    f.write_text(json.dumps(data))
    with pytest.raises(ValueError, match="integrity"):
        verify_package(directory)


@pytest.mark.asyncio
async def test_report_does_not_turn_missing_human_data_into_success_or_rank_people():
    result = await run_experiment(Protocol(conditions=["baseline", "full"], repetitions=1))
    report = render_report(result)
    assert "No demuestra superioridad" in report
    assert "determinista" in report
    assert "no comparable" in report
    assert "Resultados negativos" in report
    assert result["human_indicators"]["perceived_utility"]["value"] is None
    assert result["human_indicators"]["teacher_review_seconds"]["missing_reason"]
    assert result["aggregates"]["full"]["cells"] == 17
    assert result["aggregates"]["baseline"]["cells"] == 17
    assert result["aggregates"]["baseline"]["reconstructable_cells"] is None
    assert result["aggregates"]["baseline"]["reconstruction_missing_reason"]
    assert result["aggregates"]["full"]["reconstructable_cells"] == 17
