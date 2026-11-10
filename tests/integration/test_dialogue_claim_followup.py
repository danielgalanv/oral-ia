"""Participant claims remain distinct from reviewed source assertions, without grades."""

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize(
    "domain,answer,focus",
    [
        ("agua", "a los 99 grados", "condiciones"),
        ("agua", "aproximadamente 100 grados Celsius", "condiciones"),
        ("agua", "100 grados Fahrenheit", "condiciones"),
        ("agua", "a presión atmosférica, aproximadamente 99 grados Celsius", "condiciones"),
        ("programa", "La validación conserva los registros recibidos", "responsabilidad"),
    ],
)
def test_condition_question_links_actual_claim_without_numeric_judgment(app_client, domain, answer, focus):
    fixture = prepare_guided(app_client, domain=domain, mode="oral_defense")
    sid = fixture["session"]["session_id"]
    endpoint = f"/api/v1/defense-sessions/{sid}/defense-turns"
    initial = checked(app_client.post(endpoint, json={"text": ""}))
    result = checked(app_client.post(endpoint, json={"text": answer}))
    anchor = result["dialogue_status"]["claim_followup"]
    assert anchor["participant_turn_id"] == result["turn_id"]
    assert anchor["question_unit_id"] == initial["dialogue_status"]["rendered_unit_ids"][0]
    assert anchor["followup_unit_id"] == result["dialogue_status"]["rendered_unit_ids"][0]
    assert anchor["assessment"] == "not_assessed"
    assert focus in result["output_text"].lower()
    assert "100" not in result["output_text"]
    assert not any(
        word in result["output_text"].lower() for word in ["incorrecto", "correcto", "nota", "aprobado"]
    )
    with app_client.__db_sessionmaker__() as db:
        context = db.get(models.CognitiveState, sid).dialogue_context
        assert context["claim_followup"] == anchor
        assert db.get(models.Turn, anchor["participant_turn_id"]).input_text == answer
        unit = db.get(models.TeachingUnit, anchor["followup_unit_id"])
        original = db.get(models.TeachingUnit, anchor["question_unit_id"])
        assert unit.subgoal_ref == original.subgoal_ref == anchor["subgoal_ref"]
        assert unit.id in original.relations["rephrases"]
        assert anchor["source_fragment_ids"]
    help_result = checked(app_client.post(endpoint, json={"text": "dame una pista"}))
    assert help_result["dialogue_status"]["claim_followup"] == anchor
    checked(
        app_client.post(f"/api/v1/defense-sessions/{sid}/defense-end", json={"retain": False, "scope": []})
    )
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, sid)
        assert state is None or state.dialogue_context in ({}, None)


@pytest.mark.parametrize(
    "field", ["participant_turn_id", "question_unit_id", "followup_unit_id", "source_fragment_ids"]
)
def test_claim_anchor_cannot_forge_owned_input_or_teacher_relationship(app_client, field):
    from uuid import uuid4

    from oralia.application.services.dialogue_context_service import update_context
    from oralia.domain.agents.agent_contract import CancellationToken
    from oralia.domain.dialogue.contracts import DialogueContext

    fixture = prepare_guided(app_client, mode="oral_defense")
    sid = fixture["session"]["session_id"]
    endpoint = f"/api/v1/defense-sessions/{sid}/defense-turns"
    checked(app_client.post(endpoint, json={"text": ""}))
    result = checked(app_client.post(endpoint, json={"text": "a los 99 grados"}))
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, sid)
        values = dict(state.dialogue_context)
        values["claim_followup"] = {
            **values["claim_followup"],
            field: [str(uuid4())] if field == "source_fragment_ids" else str(uuid4()),
        }
        with pytest.raises(ValueError):
            update_context(
                db, sid, state.version, DialogueContext.model_validate(values), CancellationToken()
            )
        db.rollback()
        assert (
            db.get(models.CognitiveState, sid).dialogue_context["claim_followup"]
            == result["dialogue_status"]["claim_followup"]
        )
