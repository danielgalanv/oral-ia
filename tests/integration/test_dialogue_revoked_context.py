"""A retired objective cannot survive as an active conversational reference."""

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


def test_retired_goal_is_not_replayed_or_used_as_current_context(app_client):
    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    first = checked(app_client.post(endpoint, json={"text": "¿A qué temperatura hierve el agua?"}))
    assert "100" in first["output_text"]
    with app_client.__db_sessionmaker__() as db:
        unit_ids = [
            unit.id
            for unit in db.query(models.TeachingUnit).filter_by(
                course_id=prepared["document"]["course_id"], topic_ref="ebullicion"
            )
        ]
    for unit_id in unit_ids:
        checked(app_client.post(f"/api/v1/governance/teaching-units/{unit_id}/retire"))
    result = checked(app_client.post(endpoint, json={"text": "repite"}))
    assert "100" not in result["output_text"]
    assert result["dialogue_status"]["rendered_unit_ids"] == []
    assert "ebullicion" not in result["dialogue_status"]["available_topics"]
    count = checked(app_client.get("/api/v1/governance/active-session"))["session"]["turn_count"]
    refused = app_client.post(
        endpoint,
        json={
            "text": "",
            "dialogue_control": {
                "schema_version": 2,
                "action": "topic_switch",
                "requested_topic": "ebullicion",
            },
        },
    )
    assert refused.status_code == 409
    assert checked(app_client.get("/api/v1/governance/active-session"))["session"]["turn_count"] == count
    with app_client.__db_sessionmaker__() as db:
        context = db.get(models.CognitiveState, sid).dialogue_context
        assert context["current_topic_ref"] is None
        assert context["last_approved_turn_id"] is None
        assert context["last_approved_unit_ids"] == []
