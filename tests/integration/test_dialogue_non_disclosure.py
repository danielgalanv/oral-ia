"""Incorrect teacher hint labels do not bypass independent no-solution checks."""

import pytest

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
@pytest.mark.parametrize("advanced", [False, True])
def test_reviewed_hint_that_contains_solution_is_not_disclosed_anywhere(app_client, mode, advanced):
    prepared = prepare_guided(
        app_client,
        mode=mode,
        start=False,
        screenless=advanced,
        pedagogy=advanced,
        advanced=advanced,
    )
    aid = prepared["activity"]["id"]
    with app_client.__db_sessionmaker__() as db:
        from oralia.application.services.teaching_unit_service import unit_input

        original = db.get(models.TeachingUnit, prepared["units"]["agua-ebullicion-question"])
        successor_payload = unit_input(original).model_dump(mode="json")
        source_refs = original.source_refs
        course_id = original.course_id
        question_id = original.id
        hints = original.relations["hints"]
    bad_hint = checked(
        app_client.post(
            "/api/v1/governance/teaching-units",
            json={
                "course_id": course_id,
                "kind": "hint",
                "topic_ref": "ebullicion",
                "subgoal_ref": "ebullicion",
                "reviewed_content": (
                    "A presión atmosférica, el agua hierve aproximadamente a 100 grados Celsius."
                ),
                "reveal_policy": "safe_hint",
                "source_refs": source_refs,
                "activity_refs": [aid],
            },
        ),
        201,
    )
    checked(
        app_client.post(
            f"/api/v1/governance/teaching-units/{bad_hint['id']}/publish", json={"reviewed": True}
        )
    )
    successor_payload["relations"]["hints"] = [bad_hint["id"], *hints[1:]]
    successor = checked(
        app_client.post(f"/api/v1/governance/teaching-units/{question_id}/versions", json=successor_payload),
        201,
    )
    checked(
        app_client.post(
            f"/api/v1/governance/teaching-units/{successor['id']}/publish", json={"reviewed": True}
        )
    )
    checked(app_client.post(f"/api/v1/governance/teaching-units/{question_id}/retire"))
    sid = checked(
        app_client.post(
            "/api/v1/sessions", json={"participant_code": "synthetic-010", "activity_configuration_id": aid}
        ),
        201,
    )["session_id"]
    endpoint = (
        f"/api/v1/sessions/{sid}/study-turns"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-turns"
    )
    initial = "Ponme una pregunta de práctica sobre ebullición" if mode == "self_study" else ""
    checked(app_client.post(endpoint, json={"text": initial}))
    response = checked(app_client.post(endpoint, json={"text": "ayuda"}))
    assert response["dialogue_status"]["non_disclosure_verdict"] != "approved"
    assert response["dialogue_status"]["rendered_unit_ids"] == []
    assert "100" not in response["output_text"]
    assert response["sources"] == []
    with app_client.__db_sessionmaker__() as db:
        proposals = (
            db.query(models.GeneratedProposal)
            .join(models.Turn, models.GeneratedProposal.turn_id == models.Turn.id)
            .filter(models.Turn.session_id == sid)
            .all()
        )
        assert all("100" not in proposal.content.get("text", "") for proposal in proposals)
        assert all(
            "internal_expected_answer" not in event.payload
            for event in db.query(models.TraceEvent).filter_by(session_id=sid)
        )
    end = (
        f"/api/v1/sessions/{sid}/study-end"
        if mode == "self_study"
        else f"/api/v1/defense-sessions/{sid}/defense-end"
    )
    checked(app_client.post(end, json={"retain": True, "scope": ["transcript", "summary"]}))
    review = checked(app_client.get(f"/api/v1/governance/sessions/{sid}"))
    import re

    def strings(value):
        if isinstance(value, str):
            yield value
        elif isinstance(value, dict):
            for key, item in value.items():
                if not key.endswith(("_id", "_sha256")):
                    yield from strings(item)
        elif isinstance(value, list):
            for item in value:
                yield from strings(item)

    assert all(not re.search(r"(?<![\w-])100(?![\w-])", text) for text in strings(review))
