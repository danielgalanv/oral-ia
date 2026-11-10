"""Preparation recovery has no academic retry allowance or refreshed global clock."""

import importlib.util
import json
from pathlib import Path

import pytest

from oralia.course_dialogue.cached_transformers import cached_provider

SCRIPT = Path(__file__).resolve().parents[2] / "scripts/run_prepared_study_trial.py"
spec = importlib.util.spec_from_file_location("prepared_trial", SCRIPT)
trial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(trial)


def prior(tmp_path):
    (tmp_path / "count.json").write_text(json.dumps({"academic_requests": 0}))
    (tmp_path / "worker-cleanup.json").write_text(json.dumps({"owned_tree_stopped": True}))
    (tmp_path / "worker-stderr.log").write_text('{"stage": "loading_local_weights"}')
    (tmp_path / "gpu-before.json").write_text(json.dumps([{"monotonic": 123.5}]))
    return tmp_path


def test_mechanical_recovery_preserves_original_global_clock(tmp_path):
    assert trial.mechanical_recovery_start(prior(tmp_path)) == 123.5


@pytest.mark.parametrize("kind", ["academic", "ready", "warmup_possible", "not_stopped"])
def test_recovery_refuses_prior_academic_or_ambiguous_warmup_use(tmp_path, kind):
    root = prior(tmp_path)
    if kind == "academic":
        (root / "count.json").write_text(json.dumps({"academic_requests": 1}))
    elif kind == "ready":
        (root / "worker.json").write_text("{}")
    elif kind == "warmup_possible":
        (root / "worker-stderr.log").write_text('{"stage": "weights_loaded"}')
    else:
        (root / "worker-cleanup.json").write_text(json.dumps({"owned_tree_stopped": False}))
    with pytest.raises(ValueError, match="No recovery"):
        trial.mechanical_recovery_start(root)


@pytest.mark.asyncio
@pytest.mark.parametrize("seconds", [0, 181, True, 1.5])
async def test_preparation_ceiling_rejected_before_runtime_or_process(seconds, tmp_path):
    with pytest.raises(ValueError, match="Preparation budget"):
        async with cached_provider(tmp_path, preparation_seconds=seconds):
            pytest.fail("must never start provider")
