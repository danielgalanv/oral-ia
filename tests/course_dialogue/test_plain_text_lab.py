"""Measured lab-only text bounds do not change participant generation contracts."""

import hashlib

import pytest
from pydantic import ValidationError

from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.lab_request import LabGenerationConstraints, LabGenerationRequest
from oralia.course_dialogue.runtime import propose
from oralia.infrastructure.generation.generation_port import GenerationConstraints, GenerationOutcome
from scripts.compare_course_chat import run_bc


def _page():
    return {
        "id": "requirements:14",
        "filename": "teacher.pdf",
        "original_sha256": hashlib.sha256(b"teacher").hexdigest(),
        "version": 1,
        "page": 14,
        "text": "Completitud\nLa complejidad impide garantizar completitud y consistencia.\n",
    }


def test_lab_bounds_are_separate_from_normal_constraints():
    assert LabGenerationConstraints().max_tokens == 768
    assert LabGenerationConstraints().deadline_ms == 50000
    assert GenerationConstraints().max_tokens == 256
    with pytest.raises(ValidationError):
        GenerationConstraints(deadline_ms=50000)
    with pytest.raises(ValidationError):
        LabGenerationConstraints(deadline_ms=50001)


@pytest.mark.asyncio
async def test_cited_text_and_negative_paths_never_repair_or_display_invalid_output():
    page = _page()
    unit = build_units([page])[0]
    seen = []

    class Provider:
        def __init__(self, text, finish="stop"):
            self.text = text
            self.finish = finish

        async def generate(self, request):
            seen.append(request)
            return GenerationOutcome(
                ok=True, text=self.text, adapter="transformers_local", finish_reason=self.finish
            )

    prior = [{"input": "Duda", "displayed_text": "Respuesta mostrada", "display_kind": "candidate"}]
    answer = f"La completitud se busca, pero no se garantiza por complejidad [{unit.id}]."
    kwargs = dict(
        variant="documental",
        structured=False,
        plain_text_lab=True,
        document_units=[unit],
    )
    good = await propose([page], "completitud", prior, Provider(answer), **kwargs)
    assert good["displayed_text"] == answer and good["display_kind"] == "candidate"
    assert isinstance(seen[-1], LabGenerationRequest)
    assert seen[-1].constraints.max_tokens == 768 and seen[-1].constraints.deadline_ms == 50000
    assert seen[-1].conversation_history[-1].content == "Respuesta mostrada"
    incomplete = await propose([page], "completitud", prior, Provider(answer, "length"), **kwargs)
    assert incomplete["error"] == "generation_incomplete"
    assert incomplete["display_kind"] == "operational"
    foreign = await propose([page], "completitud", prior, Provider("Afirmación [foreign:1]."), **kwargs)
    assert foreign["error"] == "missing_or_foreign_source_reference"
    assert foreign["display_kind"] == "operational"
    fiction = await propose(
        [page],
        "completitud",
        prior,
        Provider(f"Ejemplo hipotético: una tienda inventada [{unit.id}]."),
        **kwargs,
    )
    assert fiction["error"] == "unlabelled_fictional_assumptions"
    assert fiction["display_kind"] == "operational"


@pytest.mark.asyncio
async def test_runner_does_not_treat_operational_first_turn_as_followup_context():
    page = _page()
    unit = build_units([page])[0]

    class Provider:
        usable = True

        async def generate(self, _request):
            return GenerationOutcome(
                ok=True,
                text=f"Truncated [{unit.id}]",
                adapter="transformers_local",
                finish_reason="length",
            )

    case = {
        "id": "stop-control",
        "stages": ["first", "followup", "switch"],
        "first": "completitud",
        "followup": "No lo entiendo",
        "switch": "Otro tema",
        "stop_if_first_undisplayed": True,
    }
    turns = await run_bc(case, "documental", [page], Provider(), [unit], plain_text_lab=True)
    assert turns[0]["display_kind"] == "operational"
    assert [turn.get("executed") for turn in turns[1:]] == [False, False]
    assert all(turn["reason"] == "first_academic_answer_undisplayed" for turn in turns[1:])
