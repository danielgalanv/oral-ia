"""Frozen source and display guards for the isolated generator diagnosis."""

import json
from contextlib import asynccontextmanager

import pytest

from oralia.infrastructure.generation.generation_port import GenerationOutcome
from scripts import diagnose_fixed_source_generator as diagnosis
from scripts.diagnose_fixed_source_generator import display_decision, load_frozen


def outcome(text, finish="stop"):
    return GenerationOutcome(
        ok=True,
        text=text,
        adapter="transformers_local",
        finish_reason=finish,
    )


def test_frozen_units_still_match_original_teacher_pages():
    protocol, frozen = load_frozen()
    assert len(frozen["units"]) == 5
    assert len(protocol["stages"]) == 4
    assert protocol["source_ids"]["switch"] == [
        "testing:4:16:665:list",
        "testing:7:30:450:list",
        "testing:8:22:513:list",
    ]


def test_corrected_label_protocols_are_separate_and_frozen():
    root = diagnosis.EVIDENCE
    exposed, exposed_units = load_frozen(
        root / "chat-fixed-source-14b-exposed-regression-protocol.json",
        root / "chat-fixed-source-14b-exposed-regression-units.json",
    )
    fresh, fresh_units = load_frozen(
        root / "chat-fixed-source-14b-fresh-capacity-protocol.json",
        root / "chat-fixed-source-14b-fresh-capacity-units.json",
    )
    old, _ = load_frozen()
    assert exposed["evidence_class"] == "exposed-regression"
    assert fresh["evidence_class"] == "fresh-capacity"
    assert exposed["questions"] == old["questions"]
    assert fresh["questions"] != old["questions"]
    assert exposed_units["units"] == fresh_units["units"]


def test_mistral_protocol_is_frozen_and_local_model_choice_is_explicit():
    root = diagnosis.EVIDENCE
    protocol, frozen = load_frozen(
        root / "chat-mistral24b-protocol.json", root / "chat-mistral24b-units.json"
    )
    assert protocol["evidence_class"] == "fresh_last_local_candidate"
    assert len(frozen["units"]) == 5
    assert diagnosis.local_model_profile("mistral24b") == (
        diagnosis.CACHED_MODEL_MISTRAL_24B,
        "mistral_regex_local",
    )
    with pytest.raises(ValueError, match="Unknown local"):
        diagnosis.local_model_profile("remote")


def test_citation_and_completion_gate_keeps_invalid_text_undisplayed():
    ids = ["requirements:14:42:403:list"]
    good = "La complejidad impide una garantía [requirements:14:42:403:list]."
    assert display_decision(outcome(good), ids, "first") == (good, None)
    assert display_decision(outcome(good, "length"), ids, "first")[0] is None
    assert display_decision(outcome("Una respuesta sin fuente."), ids, "first")[0] is None
    assert display_decision(outcome("Otro documento [foreign:1]."), ids, "first")[0] is None


def test_fictional_scenario_needs_labels_but_not_source_for_invented_facts():
    ids = ["requirements:14:42:403:list"]
    text = (
        "Ejemplo hipotético: hay una sala imaginaria. Supuestos ficticios: existe una reserva. "
        "La contradicción entre obligaciones ilustra el principio [requirements:14:42:403:list]."
    )
    assert display_decision(outcome(text), ids, "example") == (text, None)
    assert display_decision(outcome(text.replace("Supuestos ficticios:", "")), ids, "example") == (
        None,
        "missing_fiction_label",
    )


@pytest.mark.asyncio
async def test_first_undisplayed_answer_stops_without_followup(monkeypatch, tmp_path):
    protocol, frozen = load_frozen()

    class Provider:
        usable = True
        last_exchange = {"stage": "complete"}

        def __init__(self):
            self.requests = []

        async def generate(self, request):
            self.requests.append(request)
            return outcome("Sin cita válida.")

    provider = Provider()

    @asynccontextmanager
    async def fake_provider(*_args, **_kwargs):
        yield provider

    async def fake_gpu():
        return {"gpu": "test"}

    monkeypatch.setattr(diagnosis, "cached_provider", fake_provider)
    monkeypatch.setattr(diagnosis, "gpu_snapshot", fake_gpu)
    await diagnosis.run(tmp_path, protocol, frozen)
    result = json.loads((tmp_path / "conversation.json").read_text(encoding="utf8"))
    assert len(provider.requests) == 1
    assert [item.document_id for item in provider.requests[0].evidence] == protocol["source_ids"]["first"]
    assert all(" | " not in item.document_id for item in provider.requests[0].evidence)
    assert all(
        frozen["units"][item.document_id]["document_id"].endswith(".pdf")
        for item in provider.requests[0].evidence
    )
    assert len(result["turns"]) == 1
    assert result["turns"][0]["display_kind"] == "operational"
    assert not result["complete"]
