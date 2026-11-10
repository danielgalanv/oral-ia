"""CPU-only budget integration. No model, service or semantic quality claims."""

import uuid

import pytest

from oralia.course_dialogue.cached_transformers import CachedTransformersGenerationAdapter
from oralia.course_dialogue.structured_request import structured_request
from oralia.documentary.real_study_provider import RealStudyProvider
from oralia.documentary.study_budget import study_budget
from oralia.documentary.study_lab import DiagnosticStudy, TrialBudget
from tests.course_dialogue.test_structured_prompts import Pipe
from tests.unit.test_study_lab import ProviderFixture, RetrievalFixture


def lab(profile, text):
    provider = ProviderFixture(text=text)
    provider.study_budget_profile = profile
    provider.diagnostic_deadline_seconds = study_budget(profile).deadline_seconds
    retrieval = RetrievalFixture()
    budget = TrialBudget(maximum=6)
    return (
        DiagnosticStudy(
            retrieval, provider, authority=lambda: True, budget=budget, course="test", activity="test"
        ),
        provider,
    )


async def test_expanded_complete_text_reaches_display_ack_and_next_history_without_truncation():
    text = "CPU fixture only. " * 400
    session, provider = lab("study-expanded/v1", text)
    result = await session.turn("question", str(uuid.uuid4()))
    assert result["status"] == "prepared_unverified"
    receipt = session.display(result["id"])
    assert receipt["diagnostic_preview"] == text and len(text) > 4000
    assert receipt["study_budget"]["candidate_characters"] == 16000
    session.acknowledge(result["id"])
    await session.turn("follow-up", str(uuid.uuid4()))
    request = provider.requests[-1]
    assert request.conversation_history[-1].content == text
    assert request.constraints.max_tokens == 2048 and request.constraints.deadline_ms == 180000
    assert session.budget.used == 2


async def test_historical_default_and_expanded_upper_bound_remain_enforced():
    historical, provider = lab("historical/v1", "x" * 4001)
    result = await historical.turn("question", str(uuid.uuid4()))
    assert result["status"] == "oversized_candidate"
    assert provider.requests[0].constraints.max_tokens == 768
    assert provider.requests[0].constraints.deadline_ms == 50000
    expanded, _ = lab("study-expanded/v1", "x" * 16001)
    result = await expanded.turn("question", str(uuid.uuid4()))
    assert result["status"] == "oversized_candidate" and expanded.history == []


async def test_expanded_frame_uses_existing_backend_capability_with_same_global_clock(tmp_path):
    owner = RealStudyProvider(tmp_path, study_budget_profile="study-expanded/v1")
    deadline = owner.deadline
    session, provider = lab("study-expanded/v1", "fixture")
    await session.turn("question", str(uuid.uuid4()))
    converted = structured_request(
        provider.requests[0],
        model_profile="qwen25-14b",
        task="generate",
        didactic_profile="study-dialogue/v1",
    )
    pipe = Pipe()
    await CachedTransformersGenerationAdapter(
        pipe, repair_profile_enabled=True, model_prompt_profile="qwen25-14b"
    ).generate(converted)
    assert pipe.payload["max_tokens"] == 2048 and pipe.payload["deadline_ms"] == 180000
    assert owner.for_session(lambda: None).diagnostic_deadline_seconds == 180
    assert owner.deadline == deadline and owner.trial_budget.maximum == 6


def test_unknown_profile_rejected_and_plain_provider_stays_historical(tmp_path):
    with pytest.raises(ValueError, match="Unknown study budget"):
        RealStudyProvider(tmp_path, study_budget_profile="arbitrary")
    plain = RealStudyProvider(tmp_path)
    assert plain.diagnostic_deadline_seconds == 50


def test_api_exposes_explicit_profile_without_loading_real_provider():
    from fastapi.testclient import TestClient

    from oralia.documentary.__main__ import create_app

    retrieval = RetrievalFixture()
    provider = ProviderFixture(text="x" * 5000)
    provider.study_budget_profile = "study-expanded/v1"
    provider.diagnostic_deadline_seconds = 180
    app = create_app(
        retrieval.package,
        manifest_name="manifest-v2.json",
        retrieval=retrieval,
        study_lab=True,
        study_provider=provider,
    )
    with TestClient(app, base_url="http://127.0.0.1") as client:
        client.post("/documentary/enter")
        catalog = client.get("/api/v1/documentary").json()
        assert catalog["study_workflow_deadline_seconds"] == 180
        assert catalog["study_budget"]["max_tokens"] == 2048
        opened = client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).json()
        assert opened["study_budget"]["candidate_characters"] == 16000


async def test_expanded_turn_still_obeys_shorter_global_budget():
    import asyncio

    session, provider = lab("study-expanded/v1", "not delivered")

    async def wait():
        await asyncio.Event().wait()

    provider.hook = wait
    session.budget.remaining = lambda: 0.03
    result = await asyncio.wait_for(session.turn("question", str(uuid.uuid4())), timeout=2)
    assert result["failure_code"] == "generation_timeout"
    assert session.history == [] and session.pending is None
