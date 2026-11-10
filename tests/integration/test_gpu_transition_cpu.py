"""Use the actual reviewed runtime composition; substitute only GPU/worker boundaries."""

import json
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from oralia.course_dialogue.web_control_request import WebControlRequest
from oralia.documentary.__main__ import create_app
from oralia.documentary.real_study_provider import RealStudyProvider
from oralia.documentary.web_evidence import load_web_evidence
from oralia.infrastructure.generation.generation_port import GenerationOutcome
from tests.integration.test_connected_web_chat import Controls, PublicTransport, request_with_notice
from tests.integration.test_study_presentation_delivery import enter
from tests.unit.test_study_lab import RetrievalFixture


def runtime(monkeypatch, tmp_path, *, fail_critic=False, repair=False):
    import oralia.documentary.real_study_provider as module

    opened = []
    closed = []
    requests = []
    controls = Controls()
    final_reviews = []

    class Adapter:
        usable = True
        last_exchange = None

        def __init__(self, profile):
            self.profile = profile

        async def generate(self, request):
            requests.append(request)
            assert request.model_profile == self.profile
            if self.profile == "qwen3-8b-thinking":
                if repair and not isinstance(request, WebControlRequest) and not final_reviews:
                    final_reviews.append(True)
                    return GenerationOutcome(
                        ok=True,
                        adapter="deterministic",
                        finish_reason="stop",
                        text=json.dumps(
                            {
                                "status": "issues_found",
                                "issues": [
                                    {
                                        "kind": "unsupported",
                                        "claim": "generated response",
                                        "explanation": "CPU fixture obligation, not an academic judgement",
                                        "evidence": [],
                                    }
                                ],
                            }
                        ),
                    )
                return await controls.generate(request)
            return GenerationOutcome(
                ok=True,
                text=(
                    "FIXTURE CPU — corrected response"
                    if request.prompt_task == "repair"
                    else "FIXTURE CPU — generated response"
                ),
                finish_reason="stop",
                adapter="deterministic",
            )

    @asynccontextmanager
    async def worker(folder, **options):
        opened.append(options)
        if fail_critic and len(opened) == 2:
            raise RuntimeError("controlled critic startup failure")
        try:
            yield Adapter(options["model_prompt_profile"])
        finally:
            closed.append(options["model_prompt_profile"])

    monkeypatch.setattr(module, "cached_provider", worker)
    monkeypatch.setattr(
        module, "gpu", lambda: {"total_mib": 32000, "used_mib": 1000, "utilization_percent": 0}
    )
    owner = RealStudyProvider(tmp_path / "owned-runtime", reviewed=True, seconds=300)
    owner.diagnostic_label = "FIXTURE_CPU_REAL_RUNTIME_CLASS"
    return owner, opened, closed, requests, controls


@pytest.mark.parametrize("repair", [False, True])
def test_real_runtime_class_loads_expected_workers_and_runs_web_flow_cpu(monkeypatch, tmp_path, repair):
    owner, opened, closed, requests, _ = runtime(monkeypatch, tmp_path, repair=repair)
    retrieval = RetrievalFixture()
    root = Path(__file__).resolve().parents[2]
    web = load_web_evidence(root / "docs/audits/2026-11-03-cpu-completion/policy-requirements-lab-v2.json")
    transport = PublicTransport()
    web.acquisition = transport
    with TestClient(
        create_app(
            retrieval.package,
            manifest_name="manifest-v2.json",
            retrieval=retrieval,
            study_lab=True,
            study_chat=True,
            study_provider=owner,
            web_evidence=web,
        ),
        base_url="http://127.0.0.1",
    ) as client:
        enter(client)
        key, result = request_with_notice(client, transport)
        assert result.json()["status"] == "prepared_unverified"
        client.post(f"/api/v1/study-lab/{key}/shown", json={})
        assert client.get("/api/v1/study-lab/export").json()["counts"]["shown_answers"] == 1
        assert [r.prompt_task for r in requests if r.model_profile == "qwen25-14b"] == (
            ["generate", "repair"] if repair else ["generate"]
        )
        if repair:
            assert (
                client.get("/api/v1/study-lab/export").json()["turns"][0]["answer"]
                == "FIXTURE CPU — corrected response"
            )
        assert owner.trial_budget.maximum is None and owner.review_budget.maximum is None
        assert [x["model_prompt_profile"] for x in opened] == ["qwen25-14b", "qwen3-8b-thinking"]
        assert all(x["quantization"] == "nf4" and x["repair_profile_enabled"] for x in opened)
        assert (
            opened[1]["thinking_review_enabled"]
            and opened[1]["sampling_profile"] == "qwen3-thinking-sampling/v1"
        )
    assert closed == ["qwen3-8b-thinking", "qwen25-14b"] and not owner.ready


def test_critic_startup_failure_closes_the_generator(monkeypatch, tmp_path):
    owner, _, closed, _, _ = runtime(monkeypatch, tmp_path, fail_critic=True)
    retrieval = RetrievalFixture()
    with pytest.raises(RuntimeError, match="critic startup"):
        with TestClient(
            create_app(
                retrieval.package,
                manifest_name="manifest-v2.json",
                retrieval=retrieval,
                study_lab=True,
                study_chat=True,
                study_provider=owner,
            )
        ):
            pass
    assert closed == ["qwen25-14b"] and not owner.ready


def test_insufficient_gpu_capacity_blocks_before_any_worker(monkeypatch, tmp_path):
    import oralia.documentary.real_study_provider as module

    owner, opened, closed, _, _ = runtime(monkeypatch, tmp_path)
    monkeypatch.setattr(
        module, "gpu", lambda: {"total_mib": 32000, "used_mib": 29000, "utilization_percent": 90}
    )
    retrieval = RetrievalFixture()
    with pytest.raises(ValueError, match="free GPU capacity"):
        with TestClient(
            create_app(
                retrieval.package,
                manifest_name="manifest-v2.json",
                retrieval=retrieval,
                study_lab=True,
                study_chat=True,
                study_provider=owner,
            )
        ):
            pass
    assert not opened and not closed and not owner.ready
