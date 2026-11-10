"""CPU contract checks; no inference or claim of semantic correctness."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/preflight_generated_study.py"
spec = importlib.util.spec_from_file_location("study_preflight", SCRIPT)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


def test_sixty_seconds_is_rejected_without_silent_budget_reduction():
    receipt = preflight.budget_receipt()
    assert receipt["status"] == "rejected"
    assert receipt["requested"] == {"deadline_ms": 60000, "max_tokens": 768}
    assert receipt["errors"][0]["loc"] == ("deadline_ms",)
    assert receipt["errors"][0]["ctx"]["le"] == 50000


def test_receipt_collision_preserves_first_attempt(tmp_path):
    path = tmp_path / "receipt.json"
    preflight.write_new(path, {"first": True})
    original = path.read_bytes()
    with pytest.raises(FileExistsError):
        preflight.write_new(path, {"second": True})
    assert path.read_bytes() == original


def test_existing_attempt_directory_rejected_before_any_measurement(tmp_path, monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("must refuse collision before invoking a subprocess")

    monkeypatch.setattr(preflight.subprocess, "run", forbidden)
    with pytest.raises(FileExistsError):
        preflight.capture(tmp_path)
