"""Actual HTTP/T090/CAS with simulated intent and fictional published units only."""

import pytest

from oralia.application.services.reviewed_semantic_runtime import ReviewedSemanticRuntime
from oralia.infrastructure.db import models
from tests.course_dialogue.semantic_api_fixture import SyntheticIntentPort, prepare_semantic_activity


@pytest.mark.parametrize("entrypoint", ["study-turns", "conversation-controls"])
@pytest.mark.parametrize("greeting", [False, True])
def test_normal_api_renders_authorized_units_tracks_real_question_and_receives_without_grade(
    app_client, entrypoint, greeting
):
    prepared = prepare_semantic_activity(app_client)
    port = SyntheticIntentPort(
        [
            {"act": "explain", "goal_ref": "entrada"},
            {"act": "rephrase", "goal_ref": "entrada", "greet": greeting},
            {"act": "respond", "goal_ref": "entrada"},
        ]
    )
    app_client.app.state.semantic_runtime = ReviewedSemanticRuntime(
        engine=app_client.__db_sessionmaker__.kw["bind"],
        activity_id=prepared["activity"]["id"],
        generation_port=port,
    )
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/{entrypoint}"
    first = app_client.post(endpoint, json={"text": "Necesito una explicación del componente de entrada."})
    assert first.status_code == 200, first.text
    first = first.json()
    assert first["dialogue_status"]["rendered_unit_ids"] == [
        prepared["bindings"]["entrada"][role] for role in ["root", "cause", "process"]
    ]
    assert first["dialogue_status"]["semantic_contract_version"] == "8.0.0"
    assert first["dialogue_status"]["turn_budget_ms"] == 32000
    second = app_client.post(
        endpoint, json={"text": ("Hola. " if greeting else "") + "Otra explicación, por favor."}
    )
    assert second.status_code == 200, second.text
    second = second.json()
    if greeting:
        assert second["output_text"].startswith("Hola. ")
    question = prepared["bindings"]["entrada"]["question"]
    with app_client.__db_sessionmaker__() as db:
        from oralia.application.services.reviewed_unit_renderer import render_plan
        from oralia.domain.dialogue.contracts import ProposalPlan
        from oralia.domain.dialogue.semantic_templates import SEMANTIC_TEMPLATE_CATALOG
        from oralia.domain.policies.output_template_catalog import MATERIAL_FRAGMENT_RESPONSE_3 as entry

        if greeting:
            from oralia.domain.dialogue.semantic_templates import SEMANTIC_GREETED_3 as entry

        _, rebuilt = render_plan(
            db,
            db.get(models.Session, sid),
            ProposalPlan(
                template_id=entry.template_id,
                template_version=str(entry.version),
                template_sha256=entry.sha256,
                action="repeat",
                unit_refs=tuple(second["dialogue_status"]["rendered_unit_ids"]),
                transformation="compose_reviewed_units",
            ),
            catalog=SEMANTIC_TEMPLATE_CATALOG,
        )
        assert rebuilt.text == second["output_text"]
    assert second["dialogue_status"]["pending_question"] is not None, second
    assert second["output_text"].endswith(second["dialogue_status"]["pending_question"]["text"])
    third = app_client.post(endpoint, json={"text": "Respondo con una observación sintética de la entrada."})
    assert third.status_code == 200, third.text
    third = third.json()
    assert third["output_text"].startswith("Mensaje recibido.")
    assert third["dialogue_status"]["pending_question"] is None
    assert third["dialogue_status"]["response_received_question_id"] == question
    assert len(port.requests) == 3
    with app_client.__db_sessionmaker__() as db:
        turn = db.get(models.Turn, third["turn_id"])
        assert db.get(models.VerificationResult, turn.verification_result_id).verdict == "approved"
        state = db.get(models.CognitiveState, sid)
        assert state.dialogue_context["current_subgoal_ref"] == "entrada"
        assert state.dialogue_context["pending_question_unit_id"] is None


def test_semantic_policy_without_explicit_runtime_fails_without_creating_output(app_client):
    prepared = prepare_semantic_activity(app_client)
    sid = prepared["session"]["session_id"]
    response = app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": "Explica entrada."})
    assert response.status_code == 409, response.text
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.Turn).filter_by(session_id=sid).count() == 0


def test_semantic_profile_keeps_normal_confirmed_close_without_model_call(app_client):
    prepared = prepare_semantic_activity(app_client)
    sid = prepared["session"]["session_id"]
    port = SyntheticIntentPort([])
    app_client.app.state.semantic_runtime = ReviewedSemanticRuntime(
        engine=app_client.__db_sessionmaker__.kw["bind"],
        activity_id=prepared["activity"]["id"],
        generation_port=port,
    )
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    prompt = app_client.post(endpoint, json={"text": "Quiero terminar."})
    assert prompt.status_code == 200, prompt.text
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "active"
    closed = app_client.post(endpoint, json={"text": "Lo confirmo."})
    assert closed.status_code == 200, closed.text
    assert closed.json()["session_closed"] is True
    assert port.requests == []


@pytest.mark.parametrize("invalidation", ["retire_unit", "state_version"])
def test_invalidation_before_semantic_revalidation_cannot_emit_selected_content(app_client, invalidation):
    prepared = prepare_semantic_activity(app_client)
    sid = prepared["session"]["session_id"]

    class RetiringRuntime(ReviewedSemanticRuntime):
        async def propose(self, db, session, text, context, *, deadline_ms):
            proposal = await super().propose(db, session, text, context, deadline_ms=deadline_ms)
            if invalidation == "retire_unit":
                unit = db.get(models.TeachingUnit, prepared["bindings"]["entrada"]["root"])
                unit.status = "retired"
            else:
                db.get(models.CognitiveState, session.id).version += 1
            db.flush()
            return proposal

    port = SyntheticIntentPort([{"act": "explain", "goal_ref": "entrada"}])
    app_client.app.state.semantic_runtime = RetiringRuntime(
        engine=app_client.__db_sessionmaker__.kw["bind"],
        activity_id=prepared["activity"]["id"],
        generation_port=port,
    )
    response = app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": "Explica entrada."})
    assert response.status_code == 409, response.text
    assert len(port.requests) == 1
    with app_client.__db_sessionmaker__() as db:
        assert (
            db.query(models.GeneratedProposal).join(models.Turn).filter(models.Turn.session_id == sid).count()
            == 0
        )


def test_teacher_credentials_do_not_grant_semantic_participant_ownership(app_client):
    prepared = prepare_semantic_activity(app_client)
    sid = prepared["session"]["session_id"]
    port = SyntheticIntentPort([])
    app_client.app.state.semantic_runtime = ReviewedSemanticRuntime(
        engine=app_client.__db_sessionmaker__.kw["bind"],
        activity_id=prepared["activity"]["id"],
        generation_port=port,
    )
    app_client.cookies.clear()
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    assert app_client.post(endpoint, json={"text": "Explica entrada."}).status_code == 401
    assert (
        app_client.post(
            "/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"}
        ).status_code
        == 200
    )
    assert app_client.post(endpoint, json={"text": "Explica entrada."}).status_code == 403
    assert port.requests == []
    with app_client.__db_sessionmaker__() as db:
        assert (
            db.query(models.GeneratedProposal).join(models.Turn).filter(models.Turn.session_id == sid).count()
            == 0
        )


@pytest.mark.parametrize("retain", [False, True])
def test_semantic_session_privacy_export_erase_and_fresh_context(app_client, retain):
    prepared = prepare_semantic_activity(app_client)
    sid = prepared["session"]["session_id"]
    port = SyntheticIntentPort([{"act": "explain", "goal_ref": "entrada"}])
    app_client.app.state.semantic_runtime = ReviewedSemanticRuntime(
        engine=app_client.__db_sessionmaker__.kw["bind"],
        activity_id=prepared["activity"]["id"],
        generation_port=port,
    )
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    actual = app_client.post(endpoint, json={"text": "Explica el componente de entrada."})
    assert actual.status_code == 200, actual.text
    source = app_client.post(endpoint, json={"text": "Qué fuente usaste"})
    assert source.status_code == 200, source.text
    if retain:
        for text in ["conservar resumen y transcripción", "confirmo conservar resumen y transcripción"]:
            response = app_client.post(endpoint, json={"text": text})
            assert response.status_code == 200, response.text
    for text in ["Quiero terminar.", "Lo confirmo."]:
        response = app_client.post(endpoint, json={"text": text})
        assert response.status_code == 200, response.text
    assert response.json()["session_closed"] is True
    review = app_client.get(f"/api/v1/governance/sessions/{sid}")
    assert review.status_code == (200 if retain else 404), review.text
    for format in ["json", "markdown"]:
        exported = app_client.post(
            "/api/v1/governance/exports", json={"session_ids": [sid], "format": format}
        )
        assert exported.status_code == (200 if retain else 409), exported.text
        assert "dialogue_context" not in exported.text
        assert "planner_trace" not in exported.text
        assert "synthetic-010" not in exported.text
    deleted = app_client.request("DELETE", f"/api/v1/sessions/{sid}/content", json={"confirm": True})
    assert deleted.status_code == 200, deleted.text
    assert app_client.get(f"/api/v1/governance/sessions/{sid}").status_code == 404
    assert app_client.post("/api/v1/governance/exports", json={"session_ids": [sid]}).status_code == 409
    fresh = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "synthetic-010", "activity_configuration_id": prepared["activity"]["id"]},
    )
    assert fresh.status_code == 201, fresh.text
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, fresh.json()["session_id"])
        context = (state.dialogue_context or {}) if state is not None else {}
        assert context.get("current_subgoal_ref") is None
        assert context.get("pending_question_unit_id") is None
    assert len(port.requests) == 1
