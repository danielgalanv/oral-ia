"""Integration test: SC-001 verificado para los 5 modos mediante CognitiveState.mode +
agents_selected + DialogueAction.action_type — nunca comparando output_text."""

from __future__ import annotations

import pytest

from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material
from tests.t090_policy_helpers import minimal_output_policy_columns


def _fresh_activity(app_client) -> dict:
    """Same construction as the `self_study_activity` fixture — a standalone
    Course/RetentionPolicy/ActivityConfiguration, used when a test needs several
    independent activities (one per mode) rather than the single shared fixture
    instance."""

    Session = app_client.__db_sessionmaker__
    db = Session()
    course = models.Course(name="Curso autoestudio SC-001", subject_code="AUT101")
    policy = models.RetentionPolicy(content_scope="session", access_scope="profesor", purge_rule="manual")
    db.add_all([course, policy])
    db.flush()
    activity = models.ActivityConfiguration(
        course_id=course.id,
        name="Autoestudio SC-001",
        subject="Demo",
        objective="practicar autoestudio",
        mode="self_study",
        language="es",
        max_turns=10,
        max_duration_seconds=1800,
        general_knowledge_allowed=False,
        retention_policy_id=policy.id,
        **minimal_output_policy_columns(),
    )
    db.add(activity)
    db.commit()
    result = {"activity_id": activity.id, "course_id": course.id}
    db.close()
    return result


def _session(app_client, self_study_activity, participant_code, enabled_modes):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        enabled_modes,
        participant_code=participant_code,
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": participant_code, "activity_configuration_id": activity_id},
    ).json()["session_id"]
    return session_id


def _last_dialogue_action(app_client, session_id):
    Session = app_client.__db_sessionmaker__
    db = Session()
    turn = (
        db.query(models.Turn)
        .filter(models.Turn.session_id == session_id)
        .order_by(models.Turn.started_at.desc())
        .first()
    )
    action = db.get(models.DialogueAction, turn.dialogue_action_id) if turn and turn.dialogue_action_id else None
    db.close()
    return action.action_type if action else None


def _cognitive_mode(app_client, session_id):
    Session = app_client.__db_sessionmaker__
    db = Session()
    state = db.query(models.CognitiveState).filter(models.CognitiveState.session_id == session_id).one()
    db.close()
    return state.mode


@pytest.mark.integration
def test_doubt_resolution_structural_signature(app_client, self_study_activity):
    session_id = _session(app_client, self_study_activity, "sc001-doubt", ["doubt_resolution"])
    app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Qué contiene el documento?"})
    assert _cognitive_mode(app_client, session_id) == "doubt_resolution"
    assert _last_dialogue_action(app_client, session_id) == "respond"


@pytest.mark.integration
def test_guided_explanation_structural_signature(app_client, self_study_activity):
    session_id = _session(app_client, self_study_activity, "sc001-guided", ["guided_explanation"])
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Explícame paso a paso el documento de prueba"},
    )
    assert _cognitive_mode(app_client, session_id) == "guided_explanation"
    assert _last_dialogue_action(app_client, session_id) in ("ask", "respond")

    Session = app_client.__db_sessionmaker__
    db = Session()
    state = db.query(models.CognitiveState).filter(models.CognitiveState.session_id == session_id).one()
    db.close()
    assert isinstance(state.concepts_pending, list)


@pytest.mark.integration
def test_practice_questions_structural_signature(app_client, self_study_activity):
    session_id = _session(app_client, self_study_activity, "sc001-practice", ["practice_questions"])
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "Ponme una pregunta de práctica"}
    )
    assert _cognitive_mode(app_client, session_id) == "practice_questions"
    assert _last_dialogue_action(app_client, session_id) == "ask"

    Session = app_client.__db_sessionmaker__
    db = Session()
    questions = db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).all()
    db.close()
    assert len(questions) == 1, "practice_questions is the only mode that produces PracticeQuestion rows"


@pytest.mark.integration
def test_presentation_preparation_structural_signature(app_client, self_study_activity):
    session_id = _session(app_client, self_study_activity, "sc001-preso", ["presentation_preparation"])
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Quiero preparar una exposición sobre el documento de prueba"},
    )
    assert _cognitive_mode(app_client, session_id) == "presentation_preparation"
    assert _last_dialogue_action(app_client, session_id) in ("ask", "re_ask")


@pytest.mark.integration
def test_concept_review_structural_signature(app_client, self_study_activity):
    session_id = _session(app_client, self_study_activity, "sc001-review", ["doubt_resolution", "concept_review"])
    app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": "¿Qué contiene el documento?"})
    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns", json={"text": "Quiero repasar los conceptos vistos"}
    )
    assert _cognitive_mode(app_client, session_id) == "concept_review"

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    generation_events = [e for e in trace["trace_events"] if e["event_type"] == "generation_call"]
    assert generation_events[-1]["payload"]["purpose"] == "resumen"


@pytest.mark.integration
def test_all_five_modes_produce_distinct_agents_selected_mode_values(app_client, self_study_activity):
    seen_modes = set()
    for code, modes, text in [
        ("sc001-all-1", ["doubt_resolution"], "¿Qué contiene el documento?"),
        ("sc001-all-2", ["guided_explanation"], "Explícame paso a paso el documento de prueba"),
        ("sc001-all-3", ["practice_questions"], "Ponme una pregunta de práctica"),
        ("sc001-all-4", ["presentation_preparation"], "Quiero preparar una exposición"),
        ("sc001-all-5", ["concept_review"], "Quiero repasar los conceptos vistos"),
    ]:
        session_id = _session(app_client, _fresh_activity(app_client), code, modes)
        app_client.post(f"/api/v1/sessions/{session_id}/study-turns", json={"text": text})
        trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
        agents_selected = next(e for e in trace["trace_events"] if e["event_type"] == "agents_selected")
        seen_modes.add(agents_selected["payload"]["mode"])
        # Feature 001 allows only one active interactive session per instance at a time.
        app_client.post(f"/api/v1/sessions/{session_id}/end")

    assert seen_modes == {
        "doubt_resolution",
        "guided_explanation",
        "practice_questions",
        "presentation_preparation",
        "concept_review",
    }
