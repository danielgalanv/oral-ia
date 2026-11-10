"""Simulated interfaces demonstrate laboratory wiring, not semantic capability."""

import asyncio

import pytest

from oralia.course_dialogue.conversation_lab import LaboratoryConversation, PostReview
from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.rag_lab import ScopeAssessment, SufficiencyAssessment
from oralia.infrastructure.generation.generation_port import GenerationOutcome


class BindingFixture:
    def __init__(self):
        self.active = True
        self.checks = 0

    def revalidate(self, db):
        self.checks += 1
        if not self.active:
            raise ValueError("fixture source withdrawn")
        return {}

    def assert_decision(self, scope, policy):
        pass

    def assert_catalog(self, catalog, units, policy):
        pass


def setup(*, status="supported", reviewer=None, provider=None, sufficiency="sufficient"):
    from test_rag_lab import ProviderFixture, page

    pages = [page("req", "Requisitos\nLa consistencia evita contradicciones.\n")]
    units = build_units(pages)
    binding = BindingFixture()

    async def scope(question, resolved, history):
        return ScopeAssessment("in_scope", reason="simulated scope")

    async def assess(question, evidence):
        return SufficiencyAssessment(sufficiency, "fixture-pre-review", "simulated sufficiency")

    async def review(request, candidate, evidence):
        return PostReview(status, "fixture-post-review", "simulated verdict", simulated=True)

    provider = provider or ProviderFixture(f"Salida ficticia [{units[0].id}].")
    conversation = LaboratoryConversation(
        pages,
        units,
        binding=binding,
        db=None,
        scope_assessor=scope,
        assessor=assess,
        provider=provider,
        post_reviewer=reviewer or review,
        interfaces_are_simulated=True,
    )
    return conversation, binding, provider


@pytest.mark.asyncio
async def test_two_turns_use_only_shown_text_and_sources_remain_separate():
    lab, binding, provider = setup()
    first = await lab.turn("consistencia en requisitos")
    assert lab.history == []  # prepared text has not been acknowledged as shown
    lab.acknowledge_display(first["turn_id"])
    second = await lab.turn("¿Por qué?")
    assert "consistencia" in second["academic_query"]
    assert provider.requests[-1].conversation_history[-1].content == first["displayed_text"]
    assert first["review"].simulated is True
    assert first["publication_allowed"] is False
    assert first["participant_display"] is None
    assert binding.checks >= 6


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["rejected", "unknown"])
async def test_rejected_candidate_never_enters_display_or_followup(status):
    lab, _, provider = setup(status=status)
    row = await lab.turn("consistencia en requisitos")
    assert row["raw_candidate"].startswith("Salida ficticia")
    assert row["laboratory_preview"] is None
    assert row["raw_candidate"] not in row["displayed_text"]
    lab.acknowledge_display(row["turn_id"])
    await lab.turn("¿Por qué?")
    assert all(
        "Salida ficticia" not in message.content for message in provider.requests[-1].conversation_history
    )
    assert "raw_candidate" not in lab.history[0]


@pytest.mark.asyncio
async def test_withdrawal_during_post_review_blocks_preview_and_acknowledgement():
    lab, binding, _ = setup()

    async def review(*args):
        binding.active = False
        return PostReview("supported", "fixture", "simulated", simulated=True)

    lab.post_reviewer = review
    row = await lab.turn("consistencia requisitos")
    assert row["displayed_kind"] == "operational"
    assert row["laboratory_preview"] is None
    assert row["reason"] == "source_or_policy_invalid"
    lab.acknowledge_display(row["turn_id"])
    assert not any(h.get("academic_topic") for h in lab.history)


@pytest.mark.asyncio
async def test_pending_display_revalidates_and_cannot_be_silently_overwritten():
    lab, binding, _ = setup()
    row = await lab.turn("consistencia requisitos")
    with pytest.raises(RuntimeError, match="pending display"):
        await lab.turn("otra pregunta")
    binding.active = False
    with pytest.raises(ValueError, match="withdrawn"):
        lab.acknowledge_display(row["turn_id"])
    assert lab.history == []


@pytest.mark.asyncio
@pytest.mark.parametrize("sufficiency", ["insufficient", "conflict", "unknown"])
async def test_evidence_limit_does_not_call_generator(sufficiency):
    lab, _, provider = setup(sufficiency=sufficiency)
    row = await lab.turn("consistencia requisitos")
    assert row["displayed_kind"] == "operational"
    assert row["scope_result"] != "out_of_scope"
    assert provider.requests == []


@pytest.mark.asyncio
async def test_cancelled_generation_leaves_history_untouched_and_records_cancellation():
    started = asyncio.Event()

    class WaitingProvider:
        async def generate(self, request):
            started.set()
            await asyncio.Event().wait()

    lab, _, _ = setup(provider=WaitingProvider())
    task = asyncio.create_task(lab.turn("consistencia requisitos"))
    await started.wait()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert lab.history == []
    assert lab.receipts[-1]["reason"] == "cancelled"
    assert lab.receipts[-1]["displayed_text"] is None


@pytest.mark.asyncio
async def test_provider_failure_preserves_state_and_can_continue():
    class BrokenProvider:
        async def generate(self, request):
            raise RuntimeError("simulated backend failure")

    lab, _, _ = setup(provider=BrokenProvider())
    row = await lab.turn("consistencia requisitos")
    assert row["reason"] == "pipeline_error"
    assert lab.history == []
    lab.acknowledge_display(row["turn_id"])
    assert lab.history[0]["displayed_kind"] == "operational"


@pytest.mark.asyncio
async def test_unfinished_response_does_not_reach_post_review():
    class TruncatedProvider:
        async def generate(self, request):
            return GenerationOutcome(
                ok=True, text="incompleto", adapter="deterministic", finish_reason="length"
            )

    async def must_not_review(*args):
        pytest.fail("unfinished candidate reviewed")

    lab, _, _ = setup(provider=TruncatedProvider(), reviewer=must_not_review)
    row = await lab.turn("consistencia requisitos")
    assert row["laboratory_preview"] is None


@pytest.mark.asyncio
async def test_transcript_labels_simulation_and_preserves_passages_and_shown_text():
    lab, _, _ = setup(status="unknown")
    row = await lab.turn("consistencia requisitos")
    lab.acknowledge_display(row["turn_id"])
    rendered = lab.transcript()
    assert "SIMULADO" in rendered
    assert "La consistencia evita contradicciones." in rendered
    assert row["displayed_text"] in rendered
    assert "fixture-post-review" in rendered
    assert "Salida ficticia" not in rendered  # rejected candidate is not shown text


@pytest.mark.asyncio
async def test_mixed_excluded_part_never_enters_later_generation_history():
    lab, _, provider = setup()

    async def mixed(*args):
        return ScopeAssessment(
            "mixed",
            reason="simulated mixed",
            authority_ref="fixture",
            in_scope_question="consistencia requisitos",
            excluded_part="tema externo",
        )

    lab.scope_assessor = mixed
    row = await lab.turn("consistencia requisitos y tema externo")
    assert "otra parte" in lab.prepare_display(row["turn_id"])
    lab.acknowledge_display(row["turn_id"])
    await lab.turn("¿Por qué?")
    assert provider.requests[-1].student_input == "consistencia requisitos"
    assert all(
        "tema externo" not in message.content for message in provider.requests[-1].conversation_history
    )


@pytest.mark.asyncio
async def test_invalid_reviewer_verdict_is_not_misreported_as_source_withdrawal():
    async def invalid(*args):
        return PostReview("invalid", "fixture", "simulated", simulated=True)

    lab, _, _ = setup(reviewer=invalid)
    row = await lab.turn("consistencia requisitos")
    assert row["reason"] == "pipeline_error"
    assert row["laboratory_preview"] is None
