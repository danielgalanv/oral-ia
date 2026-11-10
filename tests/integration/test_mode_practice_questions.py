"""Integration test: `practice_questions` genera una pregunta acotada a la sesión, nunca
califica la respuesta del estudiante (SC-001, US4 AC1/AC3)."""

from __future__ import annotations

import pytest

from oralia.application.orchestration import self_study_agency_composer as composer
from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.practice_question_agent import PracticeQuestionAgent
from oralia.domain.policies.output_authorization_policy import (
    AllowedScope,
    OutputAuthorizationPolicy,
    TemplateReference,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    OutputTemplateEntry,
)
from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material

_QUESTION_TEXT = "Explica con tus propias palabras qué sabes sobre: el tema tratado."
_QUESTION_ENTRY = OutputTemplateEntry.from_text(
    template_id="practice-question-session-bounded",
    version=1,
    message_type="normal",
    text=_QUESTION_TEXT,
    topic_ref="activity",
    purpose_ref="practice_question",
    action_ref="ask",
)


async def _fixed_practice_question(self, request, cancellation):
    return AgentResult(
        status="ok",
        output={
            "question_type": "explicacion",
            "question_text": _QUESTION_TEXT,
            "internal_expected_answer": "Contenido interno no publicable.",
            "difficulty_hint": "media",
            "reveals_solution": False,
            "generation_trace": {
                "adapter": "deterministic",
                "model": None,
                "fallback_used": False,
            },
        },
        confidence=None,
        trace={"question_type": "explicacion", "adapter": "deterministic"},
    )


def _authorize_practice_question(app_client, activity_id: str, participant_code: str) -> None:
    entry = _QUESTION_ENTRY
    policy = OutputAuthorizationPolicy(
        schema_version=1,
        policy_id="practice-question-integration",
        policy_version=1,
        allowed_recipients=(participant_code,),
        allowed_disclosures=(),
        allowed_scopes=AllowedScope(
            topics=(entry.topic_ref,),
            purposes=(entry.purpose_ref,),
            actions=(entry.action_ref,),
        ),
        general_knowledge_allowed=False,
        allowed_templates=(TemplateReference(entry.template_id, entry.version),),
        allowed_operational_messages=(),
    )
    raw_policy = canonical_policy_json(policy)
    db = app_client.__db_sessionmaker__()
    try:
        activity = db.get(models.ActivityConfiguration, activity_id)
        activity.output_authorization_policy_json = raw_policy
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(raw_policy)
        db.commit()
    finally:
        db.close()


@pytest.mark.integration
def test_practice_questions_generates_bounded_session_question_never_grades(
    app_client,
    self_study_activity,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(PracticeQuestionAgent, "execute", _fixed_practice_question)
    monkeypatch.setattr(
        composer,
        "DEFAULT_OUTPUT_TEMPLATE_CATALOG",
        DEFAULT_OUTPUT_TEMPLATE_CATALOG.extended((_QUESTION_ENTRY,)),
    )
    activity_id = _setup_activity_with_material(app_client, self_study_activity, ["practice_questions"])
    _authorize_practice_question(app_client, activity_id, "est-practice-001")
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-practice-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Ponme una pregunta de práctica"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "practice_questions"
    assert body["dialogue_action"] == "ask"
    assert body["output_text"]
    assert body.get("blocked") is not True

    # The student "answers" — the system MUST NOT ever produce a grade/score anywhere.
    answer_response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "Mi respuesta a la pregunta anterior"},
    )
    assert answer_response.status_code == 200

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    for event in trace["trace_events"]:
        payload_str = str(event.get("payload", {})).lower()
        for forbidden in ("grade", "calificaci", "nota:", "puntuacion", "puntuación"):
            assert forbidden not in payload_str, (
                f"trace event {event['event_type']} MUST NOT contain a grade/score"
            )

    Session = app_client.__db_sessionmaker__
    db = Session()
    questions = (
        db.query(models.PracticeQuestion).filter(models.PracticeQuestion.session_id == session_id).all()
    )
    db.close()
    assert len(questions) == 2, (
        "one PracticeQuestion per practice_questions turn, acotada a la sesión (FR-011a)"
    )
    assert all(q.session_id == session_id for q in questions)
