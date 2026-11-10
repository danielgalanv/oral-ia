"""A simulated provider death must stop the harness, never fabricate later turns."""

import importlib
import json
from contextlib import asynccontextmanager
from pathlib import Path
from types import SimpleNamespace

import pytest

from oralia.domain.agents.agent_contract import AgentError, AgentResult


@pytest.mark.asyncio
async def test_benchmark_stops_after_worker_death_and_labels_missing_outcomes(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[2] / "scripts"))
    script = importlib.import_module("rehearse_controlled_drafts")
    process = SimpleNamespace(returncode=None)
    port = SimpleNamespace(process=process)
    calls = []

    @asynccontextmanager
    async def provider(*args, **kwargs):
        yield port

    class Agent:
        def __init__(self, **kwargs):
            pass

        async def execute(self, request, cancellation):
            calls.append(request.input["text"])
            process.returncode = 15
            return AgentResult(
                status="error", error=AgentError(code="TEST_PROVIDER_DEATH", message="synthetic")
            )

    monkeypatch.setattr(script, "cached_provider", provider)
    monkeypatch.setattr(script, "StudyIntentInterpreterAgent", Agent)
    monkeypatch.setattr(
        script,
        "DraftCurriculum",
        lambda: SimpleNamespace(
            goals=[],
            units=[],
            corrections=[],
            relations=[],
        ),
    )
    args = SimpleNamespace(model="7b-nf4", semantic_version=3, repetitions=3, observations=None)
    completed = await script.run(
        args, tmp_path, [{"id": "case", "first": "first", "followup": "must not run"}]
    )
    assert completed is False
    assert calls == ["first"]
    receipt = json.loads((tmp_path / "experiment-interrupted.json").read_text(encoding="utf8"))
    assert receipt["automatic_retry"] is False and receipt["worker_returncode"] == 15
    capture = json.loads((tmp_path / "case-0.json").read_text(encoding="utf8"))
    assert len(capture["turns"]) == 1 and capture["provider_outcomes_received"] == 0
    assert not (tmp_path / "case-1.json").exists()
