"""Current DB policy and source controls remain independent of dialogue intent."""

from datetime import timedelta

import pytest

from oralia.application.services import teaching_unit_service as units
from oralia.application.services.dialogue_retrieval_service import authorized_fragment, authorized_unit
from oralia.domain.policies.output_authorization_contract import ScopeReference
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
    load_output_authorization_policy,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.unit.test_cognitive_state import seeded_session as _seeded_session

seeded_session = _seeded_session


@pytest.fixture
def published(db_session, seeded_session):
    session = seeded_session
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    ).model_dump(mode="json")
    policy["allowed_disclosures"] += [
        {"category": category, "provenance": provenance, "recipient": session.participant_code}
        for category, provenance in [
            ("texto", "activity_material"),
            ("reviewed_teaching_unit", "teacher_reviewed"),
        ]
    ]
    activity.output_authorization_policy_json = canonical_policy_json(
        OutputAuthorizationPolicy.model_validate(policy)
    )
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(
        activity.output_authorization_policy_json
    )
    doc = models.MaterialDocument(
        course_id=activity.course_id,
        filename="sintetico.txt",
        content_hash="a" * 64,
        mime_type="text/plain",
        size_bytes=10,
        status="active",
        activity_configuration_ids=[activity.id],
    )
    db_session.add(doc)
    db_session.flush()
    fragment = models.MaterialFragment(
        document_id=doc.id,
        document_version=1,
        text="Fuente sintética.",
        location_ref="p1",
        sequence_index=0,
        embedding_ref="test",
        course_id=activity.course_id,
        activity_configuration_ids=[activity.id],
    )
    db_session.add(fragment)
    db_session.flush()
    data = units.TeachingUnitInput(
        course_id=activity.course_id,
        kind="explanation",
        topic_ref="tema",
        subgoal_ref="objetivo",
        reviewed_content="Explicación docente.",
        source_refs=[{"document_id": doc.id, "document_version": 1, "fragment_id": fragment.id}],
        activity_refs=[activity.id],
        reveal_policy="study_only",
    )
    unit = units.create(db_session, data)
    units.publish(db_session, unit.id, reviewed=True)
    return session, activity, doc, fragment, unit


def scope():
    return ScopeReference(topic_ref="activity", purpose_ref="acknowledge_turn", action_ref="continue")


@pytest.mark.parametrize(
    "change",
    [
        "document_retired",
        "version",
        "expired",
        "assignment",
        "unit_retired",
        "recipient",
        "disclosure",
        "closed",
    ],
)
def test_reuse_rechecks_revocation_and_scope(db_session, published, change):
    session, activity, doc, fragment, unit = published
    assert authorized_unit(db_session, session, unit.id, scope(), allow_solution=True).id == unit.id
    if change == "document_retired":
        doc.status = "inactive"
    if change == "version":
        doc.version = 2
    if change == "expired":
        fragment.valid_until = utcnow() - timedelta(seconds=1)
    if change == "assignment":
        fragment.activity_configuration_ids = []
    if change == "unit_retired":
        unit.status = "retired"
    if change in {"recipient", "disclosure"}:
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        ).model_dump(mode="json")
        if change == "recipient":
            policy["allowed_recipients"] = ["other"]
        else:
            policy["allowed_disclosures"] = [
                r for r in policy["allowed_disclosures"] if r["category"] != "reviewed_teaching_unit"
            ]
        activity.output_authorization_policy_json = canonical_policy_json(
            OutputAuthorizationPolicy.model_validate(policy)
        )
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(
            activity.output_authorization_policy_json
        )
    if change == "closed":
        session.status = "closed_voluntary"
    db_session.flush()
    with pytest.raises(ValueError):
        authorized_unit(db_session, session, unit.id, scope(), allow_solution=True)


def test_non_disclosure_and_fragment_use_separate_authority(db_session, published):
    session, _, doc, fragment, unit = published
    with pytest.raises(ValueError, match="disclosure forbidden"):
        authorized_unit(db_session, session, unit.id, scope(), allow_solution=False)
    assert authorized_fragment(db_session, session, fragment.id, scope()).id == fragment.id
    doc.status = "inactive"
    db_session.flush()
    with pytest.raises(ValueError):
        authorized_fragment(db_session, session, fragment.id, scope())


def test_second_transaction_revocation_is_not_hidden_by_identity_cache(db_session, published):
    from sqlalchemy.orm import Session

    session, _, doc, _, unit = published
    db_session.commit()
    assert authorized_unit(db_session, session, unit.id, scope(), allow_solution=True)
    with Session(db_session.get_bind()) as teacher:
        teacher.get(models.MaterialDocument, doc.id).status = "inactive"
        teacher.commit()
    with pytest.raises(ValueError, match="source"):
        authorized_unit(db_session, session, unit.id, scope(), allow_solution=True)


def test_teacher_unit_routes_require_teacher_not_pseudonym(app_client):
    response = app_client.get("/api/v1/governance/teaching-units?course_id=synthetic")
    assert response.status_code == 200 and response.json() == []
    app_client.cookies.clear()
    assert app_client.get("/api/v1/governance/teaching-units?course_id=synthetic").status_code == 401
    token = app_client.app.state.local_access.issue("participant", "synthetic-session")
    assert (
        app_client.get(
            "/api/v1/governance/teaching-units?course_id=synthetic",
            headers={"Authorization": f"Bearer {token}"},
        ).status_code
        == 403
    )
