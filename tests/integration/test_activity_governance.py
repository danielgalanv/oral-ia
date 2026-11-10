import pytest

from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.integration.test_defense_close_transition_outcome import _seed_active_defense


def test_used_activity_can_be_duplicated_without_rewriting_its_session(db_session):
    from oralia.application.services.activity_governance_service import duplicate_activity, publish_activity

    sid, _ = _seed_active_defense(db_session)
    session = db_session.get(models.Session, sid)
    original = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    original.immutable_since = utcnow()
    successor = duplicate_activity(db_session, original.id, {"max_turns": 12})
    assert successor.id != original.id
    assert successor.family_id == original.family_id and successor.version == original.version + 1
    assert original.max_turns == 5 and successor.max_turns == 12
    assert session.activity_configuration_id == original.id
    assert successor.retention_policy_id != original.retention_policy_id
    assert db_session.query(models.DefenseActivityConfig).filter_by(
        activity_configuration_id=successor.id
    ).one().initial_questions == ["Explica la decisión."]
    publish_activity(db_session, successor.id)
    assert db_session.get(models.ActivityGovernance, successor.id).status == "active"


def test_unavailable_model_or_material_never_publishes_a_version(db_session):
    from oralia.application.services.activity_governance_service import duplicate_activity, publish_activity

    sid, _ = _seed_active_defense(db_session)
    source = db_session.get(models.Session, sid).activity_configuration_id
    with pytest.raises(ValueError, match="model"):
        duplicate_activity(db_session, source, {"model_id": "remote-cloud-model"})
    successor = duplicate_activity(db_session, source, {})
    db_session.get(models.ActivityGovernance, successor.id).material_versions = [
        {"document_id": "missing", "version": 1}
    ]
    with pytest.raises(ValueError, match="material"):
        publish_activity(db_session, successor.id)
    assert db_session.get(models.ActivityGovernance, successor.id).status == "draft"


def test_retired_configuration_rejects_new_session_without_changing_history(db_session):
    from oralia.application.commands.start_session import StartSessionInput, start_session
    from oralia.application.services.activity_governance_service import (
        duplicate_activity,
        publish_activity,
        retire_activity,
    )

    sid, _ = _seed_active_defense(db_session)
    source = db_session.get(models.Session, sid).activity_configuration_id
    successor = duplicate_activity(db_session, source, {})
    publish_activity(db_session, successor.id)
    retire_activity(db_session, successor.id)
    with pytest.raises(ValueError, match="published"):
        start_session(
            db_session,
            StartSessionInput(participant_code="new-participant", activity_configuration_id=successor.id),
        )


def test_frozen_material_versions_reject_a_later_association(db_session):
    from oralia.domain.agents.material_retriever_agent import get_currently_valid_fragment
    from tests.integration.test_defense_text_turn import _seed_defense

    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    original_fragment = db_session.query(models.MaterialFragment).first()
    original_document = db_session.get(models.MaterialDocument, original_fragment.document_id)
    document = models.MaterialDocument(
        **{
            c.name: getattr(original_document, c.name)
            for c in models.MaterialDocument.__table__.columns
            if c.name not in {"id", "family_id", "created_at"}
        }
    )
    db_session.add(document)
    db_session.flush()
    late = models.MaterialFragment(
        **{
            c.name: getattr(original_fragment, c.name)
            for c in models.MaterialFragment.__table__.columns
            if c.name not in {"id", "created_at", "document_id"}
        },
        document_id=document.id,
    )
    db_session.add_all(
        [
            late,
            models.ActivityGovernance(
                activity_configuration_id=activity.id,
                family_id=activity.family_id,
                version=activity.version,
                status="active",
                material_versions=[
                    {"document_id": original_document.id, "version": original_document.version}
                ],
            ),
        ]
    )
    db_session.flush()
    assert (
        get_currently_valid_fragment(
            db_session,
            original_fragment.id,
            course_id=activity.course_id,
            activity_configuration_id=activity.id,
        )
        is not None
    )
    assert (
        get_currently_valid_fragment(
            db_session, late.id, course_id=activity.course_id, activity_configuration_id=activity.id
        )
        is None
    )


async def test_generation_uses_frozen_model_and_resets_between_invocations(db_session, monkeypatch):
    from oralia.application.orchestration.defense_agency_composer import run_defense_turn
    from oralia.infrastructure.generation.config import get_ollama_model
    from tests.contract.test_defense_output_authorization_matrix import _CandidateAgent
    from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense

    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    db_session.add(
        models.ActivityGovernance(
            activity_configuration_id=activity.id,
            family_id=activity.family_id,
            version=activity.version,
            status="active",
            model_id="ollama:frozen-A",
            material_versions=[
                {"document_id": document.id, "version": document.version}
                for document in db_session.query(models.MaterialDocument)
            ],
        )
    )
    db_session.flush()
    monkeypatch.setenv("ORALIA_OLLAMA_MODEL", "new-installation-B")
    seen = []

    class ObserveModel(_CandidateAgent):
        async def execute(self, request, cancellation):
            seen.append(get_ollama_model())
            return await super().execute(request, cancellation)

    await run_defense_turn(
        db_session,
        session,
        "arquitectura",
        followup_agent=ObserveModel("¿Cómo separa la arquitectura generación y verificación?"),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert seen == ["frozen-A"]
    assert get_ollama_model() == "new-installation-B"


def test_concurrent_publications_leave_exactly_one_active_version(db_session):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    from sqlalchemy.exc import IntegrityError, OperationalError
    from sqlalchemy.orm import Session

    from oralia.application.services.activity_governance_service import duplicate_activity, publish_activity

    sid, _ = _seed_active_defense(db_session)
    source_id = db_session.get(models.Session, sid).activity_configuration_id
    first = duplicate_activity(db_session, source_id, {})
    second = duplicate_activity(db_session, source_id, {})
    ids = [first.id, second.id]
    family = first.family_id
    db_session.commit()
    barrier = Barrier(2)

    def publish(aid):
        with Session(db_session.get_bind()) as writer:
            barrier.wait(timeout=5)
            try:
                publish_activity(writer, aid)
                writer.commit()
                return True
            except (IntegrityError, OperationalError):
                writer.rollback()
                return False

    with ThreadPoolExecutor(max_workers=2) as workers:
        outcomes = list(workers.map(publish, ids))
    db_session.expire_all()
    assert any(outcomes)
    assert (
        db_session.query(models.ActivityGovernance).filter_by(family_id=family, status="active").count() == 1
    )


def test_duplicate_into_new_family_retains_explicit_provenance(db_session):
    from oralia.application.services.activity_governance_service import duplicate_activity

    sid, _ = _seed_active_defense(db_session)
    source = db_session.get(
        models.ActivityConfiguration, db_session.get(models.Session, sid).activity_configuration_id
    )
    copied = duplicate_activity(db_session, source.id, {"name": "Copia autorizada"}, new_family=True)
    assert copied.family_id != source.family_id and copied.version == 1
    metadata = db_session.get(models.ActivityGovernance, copied.id)
    assert metadata.source_activity_configuration_id == source.id and metadata.status == "draft"
