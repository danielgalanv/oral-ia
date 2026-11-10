"""Protocol and literal isolation controls; no semantic model acceptance."""

import json
from types import SimpleNamespace

import pytest

from oralia.course_dialogue.scope_classifier import ScopeSelection, bind_selection, classify_scope
from oralia.infrastructure.generation.generation_port import GenerationOutcome

POLICY = {
    "included_blocks": ["pruebas"],
    "excluded_as_standalone_blocks_for_this_activity": ["seguridad"],
}
TEXT = "Explica pruebas y un curso de seguridad"
BASE = dict(
    status="mixed",
    included_block="pruebas",
    excluded_block="seguridad",
    standalone=True,
    included=dict(start=0, end=15, quote="Explica pruebas"),
    excluded=dict(start=18, end=len(TEXT), quote="un curso de seguridad"),
    referent_turn=None,
)


def test_mixed_only_delivers_literal_allowed_span_without_history():
    selection = ScopeSelection.model_validate(BASE)
    assessment, query = bind_selection(selection, TEXT, [], POLICY, "hash")
    assert query == "Explica pruebas"
    assert "seguridad" not in query
    assert assessment.excluded_part == "un curso de seguridad"


@pytest.mark.parametrize(
    "patch",
    [
        {"included": {"start": 0, "end": 999, "quote": "Explica pruebas"}},
        {"included": {"start": 0, "end": 15, "quote": "Texto inventado"}},
        {"excluded": {"start": 0, "end": len(TEXT), "quote": TEXT}},
        {"included": None},
        {"excluded_block": "foreign"},
        {"included_block": "foreign"},
        {"standalone": False},
        {"referent_turn": 0},
        {"extra": True},
        {"included": {"start": True, "end": 15, "quote": "Explica pruebas"}},
    ],
)
def test_malformed_mixed_never_produces_rag_query(patch):
    with pytest.raises(ValueError):
        bind_selection(ScopeSelection.model_validate({**BASE, **patch}), TEXT, [], POLICY, "hash")


@pytest.mark.asyncio
@pytest.mark.parametrize("failure", ["none", "before", "during", "incomplete", "json", "hidden"])
async def test_classifier_revalidates_and_records_real_request(failure):
    calls = []
    state = {"active": failure != "before"}

    def revalidate(_db):
        if not state["active"]:
            raise ValueError("withdrawn policy")
        return POLICY

    class Provider:
        async def generate(self, request):
            calls.append(request)
            if failure == "during":
                state["active"] = False
            return GenerationOutcome(
                ok=True,
                text="bad" if failure == "json" else json.dumps(BASE),
                adapter="deterministic",
                finish_reason="length" if failure == "incomplete" else "stop",
            )

    binding = SimpleNamespace(revalidate=revalidate, policy_sha256="hash", assert_decision=lambda *_: None)
    history = [{"input": "hidden", "raw_candidate": "not shown"}] if failure == "hidden" else []
    if failure == "none":
        result = await classify_scope(TEXT, history, provider=Provider(), binding=binding, db=None)
        assert result.rag_question == "Explica pruebas"
        assert result.publication_allowed is False
        payload = json.loads(calls[0].student_input)
        assert "expected" not in payload and "retrieval" not in payload
    else:
        with pytest.raises(ValueError):
            await classify_scope(TEXT, history, provider=Provider(), binding=binding, db=None)
    assert len(calls) == (0 if failure in {"before", "hidden"} else 1)
