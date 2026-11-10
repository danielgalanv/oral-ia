"""AI transcript audit regressions; real public provider, not human utility evidence."""

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


def test_repeat_comparison_is_a_reference_not_a_second_operation(app_client):
    prepared = prepare_guided(app_client, domain="programa")
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    checked(app_client.post(endpoint, json={"text": "¿Qué comprueba almacenamiento?"}))
    previous = checked(app_client.post(endpoint, json={"text": "Una comparación"}))
    repeated = checked(app_client.post(endpoint, json={"text": "Repite la comparación"}))
    assert repeated["dialogue_status"]["primary_act"] == "repeat"
    assert repeated["output_text"] == previous["output_text"]
    assert (
        repeated["dialogue_status"]["rendered_unit_ids"] == previous["dialogue_status"]["rendered_unit_ids"]
    )


def test_comparison_with_another_topic_keeps_the_current_objective(app_client):
    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    checked(app_client.post(endpoint, json={"text": "Explícame paso a paso la condensación"}))
    result = checked(app_client.post(endpoint, json={"text": "compara con evaporación"}))
    assert "condensación" in result["output_text"].lower()
    assert "evaporación" in result["output_text"].lower()
    assert result["dialogue_status"]["rendered_unit_ids"]
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.CognitiveState, sid).dialogue_context["current_topic_ref"] == "condensacion"


def test_confirmed_output_topic_is_not_a_contradiction_of_storage(app_client):
    prepared = prepare_guided(app_client, domain="programa")
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    for text in ["¿Quién guarda los resultados?", "no entiendo, dilo de otra forma", "cambiar de tema"]:
        checked(app_client.post(endpoint, json={"text": text}))
    result = checked(app_client.post(endpoint, json={"text": "confirmo: salida"}))
    assert result["dialogue_status"]["notice"] is None
    assert result["dialogue_status"]["coherence_verdict"] == "approved"
    assert "La salida" in result["output_text"]


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
@pytest.mark.parametrize("requested_format", ["dame un ejemplo", "compara los roles", "dame la solución"])
def test_protected_unsupported_format_has_specific_limit_and_keeps_question(
    app_client, mode, requested_format
):
    prepared = prepare_guided(
        app_client, mode=mode, study_mode="practice_questions" if mode == "self_study" else None
    )
    sid = prepared["session"]["session_id"]
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    checked(
        app_client.post(
            endpoint, json={"text": "pregunta de práctica sobre ebullición" if mode == "self_study" else ""}
        )
    )
    with app_client.__db_sessionmaker__() as db:
        previous = db.get(models.CognitiveState, sid).dialogue_context["pending_question_unit_id"]
    result = checked(app_client.post(endpoint, json={"text": requested_format}))
    assert result["dialogue_status"]["notice"] == "limited"
    assert not result["dialogue_status"]["rendered_unit_ids"]
    assert result["output_text"] and "100" not in result["output_text"]
    assert not result["sources"]
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.CognitiveState, sid).dialogue_context["pending_question_unit_id"] == previous


def test_named_offtopic_answer_requests_confirmation_without_changing_question(app_client):
    prepared = prepare_guided(app_client, mode="oral_defense")
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/defense-sessions/{sid}/defense-turns"
    initial = checked(app_client.post(endpoint, json={"text": ""}))
    result = checked(app_client.post(endpoint, json={"text": "La evaporación ocurre en la superficie"}))
    assert result["dialogue_status"]["notice"] == "confirm_topic"
    assert result["dialogue_status"]["pending_topic"] == "evaporacion"
    assert result["dialogue_status"]["pending_question"] == initial["dialogue_status"]["pending_question"]
    assert not result["dialogue_status"]["rendered_unit_ids"]
    assert result["dialogue_status"]["claim_followup"] is None


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_repeat_hint_is_not_replaced_by_pending_question(app_client, mode):
    prepared = prepare_guided(
        app_client, mode=mode, study_mode="practice_questions" if mode == "self_study" else None
    )
    sid = prepared["session"]["session_id"]
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    initial = checked(
        app_client.post(
            endpoint, json={"text": "pregunta de práctica sobre ebullición" if mode == "self_study" else ""}
        )
    )
    hint = checked(app_client.post(endpoint, json={"text": "dame una pista"}))
    repeated = checked(app_client.post(endpoint, json={"text": "repite la pista"}))
    assert repeated["output_text"] == hint["output_text"]
    assert repeated["dialogue_status"]["repeat_target"] == "hint"
    assert repeated["dialogue_status"]["pending_question"] == initial["dialogue_status"]["pending_question"]
    question = checked(app_client.post(endpoint, json={"text": "repite la pregunta"}))
    assert question["output_text"] == initial["output_text"]


def test_repeat_named_component_of_composition_keeps_approved_unit(app_client):
    prepared = prepare_guided(app_client, study_mode="presentation_preparation")
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    composed = checked(
        app_client.post(endpoint, json={"text": "Quiero preparar una exposición sobre congelación"})
    )
    assert len(composed["dialogue_status"]["rendered_unit_ids"]) == 3
    repeated = checked(app_client.post(endpoint, json={"text": "repite la comparación"}))
    assert repeated["dialogue_status"]["repeat_target"] == "comparison"
    assert repeated["dialogue_status"]["coherence_verdict"] == "approved"
    assert len(repeated["dialogue_status"]["rendered_unit_ids"]) == 1
    assert repeated["output_text"] in composed["output_text"]
    assert repeated["output_text"] != composed["output_text"]


def test_concept_review_support_can_use_allowed_example_without_losing_question(app_client):
    prepared = prepare_guided(app_client, domain="programa", study_mode="concept_review")
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    initial = checked(app_client.post(endpoint, json={"text": "Quiero repasar validación"}))
    result = checked(app_client.post(endpoint, json={"text": "dame un ejemplo"}))
    assert result["dialogue_status"]["notice"] is None
    assert result["dialogue_status"]["pending_question"] == initial["dialogue_status"]["pending_question"]
    with app_client.__db_sessionmaker__() as db:
        assert (
            db.get(models.TeachingUnit, result["dialogue_status"]["rendered_unit_ids"][0]).kind == "example"
        )


@pytest.mark.parametrize("reveal,disclose", [(False, True), (True, True), (True, False)])
def test_teacher_practice_reveal_flag_and_source_permissions_are_independent(app_client, reveal, disclose):
    prepared = prepare_guided(
        app_client,
        study_mode="practice_questions",
        practice_reveals_solution=reveal,
        material_disclosure=disclose,
    )
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    initial = checked(app_client.post(endpoint, json={"text": "pregunta de práctica sobre ebullición"}))
    result = checked(app_client.post(endpoint, json={"text": "dame un ejemplo"}))
    assert result["dialogue_status"]["pending_question"] == initial["dialogue_status"]["pending_question"]
    if reveal:
        assert result["dialogue_status"]["notice"] is None
        with app_client.__db_sessionmaker__() as db:
            assert (
                db.get(models.TeachingUnit, result["dialogue_status"]["rendered_unit_ids"][0]).kind
                == "example"
            )
        if not disclose:
            assert all(not source.get("fragment_text") for source in result["sources"])
    else:
        assert result["dialogue_status"]["notice"] == "limited"
        assert not result["dialogue_status"]["rendered_unit_ids"]


def test_request_for_absent_question_does_not_repeat_an_explanation(app_client):
    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    previous = checked(app_client.post(endpoint, json={"text": "¿A qué temperatura hierve el agua?"}))
    result = checked(app_client.post(endpoint, json={"text": "repite la pregunta"}))
    assert result["dialogue_status"]["notice"] == "orientation"
    assert not result["dialogue_status"]["rendered_unit_ids"]
    assert result["output_text"] != previous["output_text"]


def test_confirmed_entry_is_not_storage_with_an_omitted_subject(app_client):
    prepared = prepare_guided(app_client, domain="programa")
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    checked(app_client.post(endpoint, json={"text": "¿Quién guarda los resultados?"}))
    checked(app_client.post(endpoint, json={"text": "Cambiar de tema"}))
    result = checked(app_client.post(endpoint, json={"text": "confirmo: entrada"}))
    assert result["dialogue_status"]["notice"] is None
    assert result["dialogue_status"]["coherence_verdict"] == "approved"
    assert result["dialogue_status"]["rendered_unit_ids"]
