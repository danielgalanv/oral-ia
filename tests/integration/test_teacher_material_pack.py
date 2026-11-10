"""Acceptance of the delivered fictional teacher material through real HTTP services."""

from pathlib import Path

import pytest

from oralia.demo.fixtures import output_policy


def checked(response, expected=200):
    assert response.status_code == expected, response.text
    return response.json()


@pytest.mark.parametrize(
    "filename", ["01-agua-autorizado.txt", "04-caso-largo-incidencia.txt", "generated-long-block.txt"]
)
@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
@pytest.mark.parametrize("scopes", [[], ["transcript"], ["summary"], ["transcript", "summary"]])
def test_teacher_pack_upload_publish_session_review_export_delete(app_client, mode, scopes, filename):
    client = app_client
    retain = bool(scopes)
    course = checked(
        client.post(
            "/api/v1/governance/courses",
            json={
                "name": "Paquete docente ficticio",
                "subject_code": "DOCENTE-AGUA",
            },
        ),
        201,
    )
    policy = checked(
        client.post(
            "/api/v1/governance/retention-policies",
            json={
                "retention_days": 1,
                "content_scope": "transcript,summary",
                "access_scope": "local_teacher",
            },
        ),
        201,
    )
    material = Path(__file__).resolve().parents[2] / "materiales/docente" / filename
    content = (
        ("El agua hierve a 100 grados Celsius. " + "El calentamiento produce vapor de agua. " * 30).encode()
        if filename == "generated-long-block.txt"
        else material.read_bytes()
    )
    document = checked(
        client.post(
            "/api/v1/materials/documents",
            data={"course_id": course["id"]},
            files={"file": (material.name, content, "text/plain")},
        ),
        201,
    )
    assert document["status"] == "processed"
    checked(client.post(f"/api/v1/materials/documents/{document['id']}/activate"))
    mode_config = (
        {
            "initial_questions": ["¿A qué temperatura hierve el agua?"],
            "topics": ["agua"],
            "summary_authorized": True,
            "transcript_retention_authorized": True,
        }
        if mode == "oral_defense"
        else {
            "enabled_modes": ["doubt_resolution", "guided_explanation"],
            "summary_authorized": True,
            "retention_authorized": True,
        }
    )
    activity = checked(
        client.post(
            "/api/v1/governance/activities",
            json={
                "activity": {
                    "course_id": course["id"],
                    "name": "Paquete docente agua",
                    "subject": "Agua",
                    "objective": "Explicar el agua con fuentes autorizadas",
                    "mode": mode,
                    "language": "es",
                    "max_turns": 8,
                    "max_duration_seconds": 600,
                    "retention_policy_id": policy["id"],
                    "output_authorization_policy": output_policy(mode).model_dump(mode="json"),
                },
                "material_versions": [{"document_id": document["id"], "version": document["version"]}],
                "mode_config": mode_config,
            },
        ),
        201,
    )
    checked(client.post(f"/api/v1/governance/activities/{activity['id']}/activate"))
    session = checked(
        client.post(
            "/api/v1/sessions",
            json={"participant_code": "demo-007", "activity_configuration_id": activity["id"]},
        ),
        201,
    )
    sid = session["session_id"]
    consent = {"retain": retain, "scope": scopes}
    prefix = f"/api/v1/defense-sessions/{sid}" if mode == "oral_defense" else f"/api/v1/sessions/{sid}"
    turn_route = "defense-turns" if mode == "oral_defense" else "study-turns"
    if mode == "self_study":
        greeting = checked(
            client.post(f"{prefix}/{turn_route}", json={"text": "Hola", "closure_consent": consent})
        )
        assert not greeting.get("session_closed", False), greeting
    answer = checked(
        client.post(
            f"{prefix}/{turn_route}",
            json={
                "text": "¿A qué temperatura hierve el agua?",
                "closure_consent": consent,
            },
        )
    )
    assert answer["output_text"] is not None, answer
    assert not answer.get("blocked", False), answer
    if mode == "self_study":
        assert "100" in answer["output_text"]
        assert answer["sources"]
        second = checked(
            client.post(
                f"{prefix}/{turn_route}",
                json={"text": "¿Cómo pasa el agua líquida a vapor?", "closure_consent": consent},
            )
        )
        assert second["output_text"] is not None, second
        assert not second.get("blocked", False) and not second.get("session_closed", False), second
        if filename == "generated-long-block.txt":
            with client.__db_sessionmaker__() as db:
                from oralia.infrastructure.db import models

                assert (
                    db.query(models.TraceEvent)
                    .filter_by(session_id=sid, event_type="material_excerpt_bound")
                    .count()
                )

    end_route = "defense-end" if mode == "oral_defense" else "study-end"
    checked(client.post(f"{prefix}/{end_route}", json=consent))
    review_url = f"/api/v1/governance/sessions/{sid}"
    if not retain:
        assert client.get(review_url).status_code == 404
        assert client.post("/api/v1/governance/exports", json={"session_ids": [sid]}).status_code == 409
        return
    review = checked(client.get(review_url))
    assert set(review["scopes"]) == set(scopes)
    assert bool(review["turns"]) is ("transcript" in scopes)
    assert (review["summary"] is not None) is ("summary" in scopes)
    for fmt in ("json", "markdown"):
        exported = client.post(
            "/api/v1/governance/exports",
            json={"session_ids": [sid], "format": fmt, "include_free_text": True, "reviewed_free_text": True},
        )
        assert exported.status_code == 200, exported.text
        assert "demo-007" not in exported.text and sid not in exported.text
    checked(client.request("DELETE", f"/api/v1/sessions/{sid}/content", json={"confirm": True}))
    assert client.get(review_url).status_code == 404
    assert client.post("/api/v1/governance/exports", json={"session_ids": [sid]}).status_code == 409
