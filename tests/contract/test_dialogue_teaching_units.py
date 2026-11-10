"""Teacher publication, source validity and immutable version successors."""

import pytest

from oralia.infrastructure.db import models
from tests.unit.test_cognitive_state import seeded_session as _seeded_session

seeded_session = _seeded_session


def test_teacher_units_require_review_and_valid_sources(db_session, seeded_session):
    from oralia.application.services.teaching_unit_service import (
        TeachingUnitInput,
        create,
        publish,
        retire,
        successor,
    )

    session = seeded_session
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    doc = models.MaterialDocument(
        course_id=activity.course_id,
        filename="ficticio.txt",
        content_hash="a" * 64,
        mime_type="text/plain",
        size_bytes=10,
        status="active",
        activity_configuration_ids=[activity.id],
    )
    db_session.add(doc)
    db_session.flush()
    frag = models.MaterialFragment(
        document_id=doc.id,
        document_version=1,
        text="Contenido ficticio revisable.",
        location_ref="p1",
        sequence_index=0,
        embedding_ref="test",
        course_id=activity.course_id,
        activity_configuration_ids=[activity.id],
    )
    db_session.add(frag)
    db_session.flush()
    payload = TeachingUnitInput(
        course_id=activity.course_id,
        kind="explanation",
        topic_ref="tema",
        subgoal_ref="objetivo",
        reviewed_content="Contenido docente revisado.",
        source_refs=[{"document_id": doc.id, "document_version": 1, "fragment_id": frag.id}],
        activity_refs=[activity.id],
        reveal_policy="study_only",
    )
    unit = create(db_session, payload)
    with pytest.raises(ValueError, match="review"):
        publish(db_session, unit.id, reviewed=False)
    publish(db_session, unit.id, reviewed=True)
    assert unit.status == "published"
    following = successor(
        db_session, unit.id, payload.model_copy(update={"reviewed_content": "Otra formulación revisable."})
    )
    assert following.family_id == unit.family_id and following.version == 2 and following.status == "draft"
    assert unit.reviewed_content == "Contenido docente revisado."
    doc.status = "inactive"
    db_session.flush()
    with pytest.raises(ValueError, match="source"):
        publish(db_session, following.id, reviewed=True)
    retire(db_session, unit.id)
    assert unit.status == "retired"


def test_used_activity_requires_successor_for_new_unit(db_session, seeded_session):
    from oralia.application.services.teaching_unit_service import TeachingUnitInput, validate_sources
    from oralia.infrastructure.db.timeutil import utcnow

    activity = db_session.get(models.ActivityConfiguration, seeded_session.activity_configuration_id)
    activity.immutable_since = utcnow()
    data = TeachingUnitInput(
        course_id=activity.course_id,
        kind="hint",
        topic_ref="tema",
        subgoal_ref="objetivo",
        reviewed_content="Pista sintética.",
        reveal_policy="safe_hint",
        activity_refs=[activity.id],
        source_refs=[
            {
                "document_id": "00000000-0000-0000-0000-000000000001",
                "document_version": 1,
                "fragment_id": "00000000-0000-0000-0000-000000000002",
            }
        ],
    )
    with pytest.raises(ValueError, match="successor"):
        validate_sources(db_session, data, authoring=True)


def test_public_teacher_authoring_and_participant_write_denied(app_client, seeded_course):
    uploaded = app_client.post(
        "/api/v1/materials/documents",
        data={"course_id": seeded_course},
        files={
            "file": (
                "unidad-sintetica.txt",
                "La entrada recibe registros ficticios para validación.".encode(),
                "text/plain",
            )
        },
    )
    assert uploaded.status_code == 201
    document = uploaded.json()
    assert app_client.post(f"/api/v1/materials/documents/{document['id']}/activate").status_code == 200
    with app_client.__db_sessionmaker__() as db:
        fragment = db.query(models.MaterialFragment).filter_by(document_id=document["id"]).one()
        fragment_id = fragment.id
    data = {
        "course_id": seeded_course,
        "kind": "explanation",
        "topic_ref": "entrada",
        "subgoal_ref": "recepcion",
        "reviewed_content": "La entrada recibe registros y los entrega a validación.",
        "reveal_policy": "study_only",
        "source_refs": [
            {
                "document_id": document["id"],
                "document_version": document["version"],
                "fragment_id": fragment_id,
            }
        ],
    }
    endpoint = "/api/v1/governance/teaching-units"
    created = app_client.post(endpoint, json=data)
    assert created.status_code == 201
    unit = created.json()
    assert unit["status"] == "draft"
    assert app_client.post(f"{endpoint}/{unit['id']}/publish", json={"reviewed": False}).status_code == 409
    assert (
        app_client.post(f"{endpoint}/{unit['id']}/publish", json={"reviewed": True}).json()["status"]
        == "published"
    )
    successor = app_client.post(
        f"{endpoint}/{unit['id']}/versions", json={**data, "reviewed_content": "Otra explicación revisable."}
    )
    assert successor.status_code == 201 and successor.json()["version"] == 2
    listing = app_client.get(endpoint, params={"course_id": seeded_course}).json()
    assert (
        next(row for row in listing if row["id"] == unit["id"])["reviewed_content"]
        == data["reviewed_content"]
    )
    assert app_client.post(f"/api/v1/materials/documents/{document['id']}/deactivate").status_code == 200
    assert (
        app_client.post(f"{endpoint}/{successor.json()['id']}/publish", json={"reviewed": True}).status_code
        == 409
    )
    assert app_client.post(f"{endpoint}/{unit['id']}/retire").json()["status"] == "retired"
    app_client.cookies.clear()
    assert app_client.post(endpoint, json=data).status_code == 401
    token = app_client.app.state.local_access.issue("participant", "synthetic-only")
    assert (
        app_client.post(endpoint, json=data, headers={"Authorization": f"Bearer {token}"}).status_code == 403
    )
