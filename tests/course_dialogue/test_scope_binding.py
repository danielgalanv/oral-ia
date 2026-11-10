"""A scope policy stays tied to the current SQL activity and policy bytes."""

import asyncio
import hashlib
import json
from dataclasses import replace

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from oralia.course_dialogue import rag_lab
from oralia.course_dialogue.document_evidence import build_units
from oralia.course_dialogue.rag_lab import (
    ActivityScopeBinding,
    ScopeAssessment,
    SufficiencyAssessment,
    diagnostic_rag_turn,
)
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.models import ActivityConfiguration, ActivityGovernance, Course, RetentionPolicy
from oralia.infrastructure.generation.generation_port import GenerationOutcome


@pytest.fixture(autouse=True)
def trusted_fixture_extraction(monkeypatch):
    def load(root, _profile, _source_hashes, _decisions_sha256):
        page = {
            "id": "material:1",
            "filename": "material.pdf",
            "original_sha256": hashlib.sha256((root / "material.pdf").read_bytes()).hexdigest(),
            "version": 1,
            "page": 1,
            "text": "Tema\nPruebas de software.\n",
        }
        return [page], build_units([page])

    monkeypatch.setattr(rag_lab, "_trusted_catalog", load)


def fixture(tmp_path):
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    db = Session(engine)
    db.add(Course(id="course-1", name="Curso", subject_code="IS"))
    db.add(
        RetentionPolicy(
            id="retention-1",
            content_scope="none",
            retention_days=None,
            access_scope="teacher",
            purge_rule="none",
        )
    )
    db.add(
        ActivityConfiguration(
            id="activity-1",
            course_id="course-1",
            version=3,
            name="Laboratorio",
            subject="Ingeniería del Software",
            objective="Dudas",
            mode="self_study",
            language="es",
            max_turns=5,
            max_duration_seconds=300,
            general_knowledge_allowed=False,
            retention_policy_id="retention-1",
        )
    )
    db.add(
        ActivityGovernance(
            activity_configuration_id="activity-1",
            family_id="family-1",
            version=3,
            status="active",
            model_id="deterministic",
            material_versions=[],
        )
    )
    db.commit()
    presentation = tmp_path / "presentation.pdf"
    presentation.write_bytes(b"teacher presentation fixture")
    material = tmp_path / "material.pdf"
    material.write_bytes(b"authorized material fixture")
    path = tmp_path / "scope.json"
    path.write_text(
        json.dumps(
            {
                "approval_status": "approved",
                "approval_kind": "scope_only",
                "participant_publication_allowed": False,
                "activity_id": "activity-1",
                "activity_version": 3,
                "course_id": "course-1",
                "included_blocks": ["pruebas"],
                "excluded_as_standalone_blocks_for_this_activity": ["programacion_autonoma"],
                "boundary_rules": {"exclusion_is_standalone_only": True},
                "source_scope": {
                    "presentation": {
                        "file": presentation.name,
                        "sha256": hashlib.sha256(presentation.read_bytes()).hexdigest(),
                    },
                    "authorized_lab_documents": [
                        {"file": material.name, "sha256": hashlib.sha256(material.read_bytes()).hexdigest()}
                    ],
                },
            }
        ),
        encoding="utf-8",
    )
    binding = ActivityScopeBinding(
        engine,
        "activity-1",
        3,
        "course-1",
        path,
        hashlib.sha256(path.read_bytes()).hexdigest(),
        tmp_path,
    )
    return engine, db, path, binding


def test_sql_activity_version_and_policy_bytes_are_revalidated(tmp_path):
    engine, db, path, binding = fixture(tmp_path)
    binding.revalidate(db)
    governance = db.get(ActivityGovernance, "activity-1")
    governance.status = "retired"
    db.commit()
    with pytest.raises(ValueError, match="not active"):
        binding.revalidate(db)
    governance.status = "active"
    db.commit()
    binding.revalidate(db)
    with Session(create_engine("sqlite:///:memory:")) as foreign:
        with pytest.raises(ValueError, match="another database engine"):
            binding.revalidate(foreign)
    path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
    with pytest.raises(ValueError, match="changed since binding"):
        binding.revalidate(db)
    original_policy = json.loads(path.read_text(encoding="utf-8"))
    original_policy["source_scope"]["presentation"]["sha256"] = hashlib.sha256(
        (tmp_path / "presentation.pdf").read_bytes()
    ).hexdigest()
    path.write_text(json.dumps(original_policy), encoding="utf-8")
    refreshed = ActivityScopeBinding(
        engine,
        "activity-1",
        3,
        "course-1",
        path,
        hashlib.sha256(path.read_bytes()).hexdigest(),
        tmp_path,
    )
    (tmp_path / "presentation.pdf").write_bytes(b"changed")
    with pytest.raises(ValueError, match="scope source changed"):
        refreshed.revalidate(db)
    path.write_text(json.dumps({"approval_status": "draft"}), encoding="utf-8")
    draft = ActivityScopeBinding(
        engine,
        "activity-1",
        3,
        "course-1",
        path,
        hashlib.sha256(path.read_bytes()).hexdigest(),
    )
    with pytest.raises(ValueError, match="unapproved"):
        draft.revalidate(db)
    db.close()
    engine.dispose()


def test_exclusion_must_name_a_block_in_the_bound_policy(tmp_path):
    engine, db, _path, binding = fixture(tmp_path)
    policy = binding.revalidate(db)
    valid = ScopeAssessment(
        "out_of_scope",
        authority_ref=binding.policy_sha256,
        excluded_block_id="programacion_autonoma",
        standalone_excluded_block=True,
        reason="exclusión fixture",
    )
    binding.assert_decision(valid, policy)
    with pytest.raises(ValueError, match="not a standalone block"):
        binding.assert_decision(
            ScopeAssessment(
                "out_of_scope",
                authority_ref=binding.policy_sha256,
                excluded_block_id="programacion_autonoma",
                reason="mención de apoyo",
            ),
            policy,
        )
    with pytest.raises(ValueError, match="excluded block"):
        binding.assert_decision(
            ScopeAssessment(
                "out_of_scope",
                authority_ref=binding.policy_sha256,
                excluded_block_id="tema_no_listado",
                reason="fixture",
            ),
            policy,
        )
    with pytest.raises(ValueError, match="bound policy"):
        binding.assert_decision(
            ScopeAssessment(
                "out_of_scope",
                authority_ref="otro-hash",
                excluded_block_id="programacion_autonoma",
                reason="fixture",
            ),
            policy,
        )
    db.close()
    engine.dispose()


def test_catalog_rejects_foreign_and_changed_evidence(tmp_path):
    engine, db, _path, binding = fixture(tmp_path)
    policy = binding.revalidate(db)
    source_hash = hashlib.sha256((tmp_path / "material.pdf").read_bytes()).hexdigest()
    page = {
        "id": "material:1",
        "filename": "material.pdf",
        "original_sha256": source_hash,
        "version": 1,
        "page": 1,
        "text": "Tema\nPruebas de software.\n",
    }
    binding.assert_catalog([page], build_units([page]), policy)
    with pytest.raises(ValueError, match="verified source extraction"):
        binding.assert_catalog([{**page, "filename": "foreign.pdf"}], [], policy)
    with pytest.raises(ValueError, match="verified source extraction"):
        binding.assert_catalog([{**page, "original_sha256": "changed"}], [], policy)
    with pytest.raises(ValueError, match="verified source extraction"):
        binding.assert_catalog([page], build_units([{**page, "text": "Tema\nOtro texto.\n"}]), policy)
    forged_text = "Pruebas de software\nLas pruebas garantizan la ausencia de errores.\n"
    forged = {
        **page,
        "text": forged_text,
        "text_sha256": hashlib.sha256(forged_text.encode()).hexdigest(),
    }
    with pytest.raises(ValueError, match="verified source extraction"):
        binding.assert_catalog([forged], build_units([forged]), policy)
    with pytest.raises(ValueError, match="verified source extraction"):
        binding.assert_catalog([{**page, "id": "material:99", "page": 99}], [], policy)
    db.close()
    engine.dispose()


@pytest.mark.asyncio
async def test_activity_change_during_generation_rejects_preview(tmp_path):
    engine, db, _path, binding = fixture(tmp_path)

    class ChangingProvider:
        async def generate(self, _request):
            await asyncio.sleep(0)
            activity = db.get(ActivityConfiguration, "activity-1")
            activity.version = 4
            db.commit()
            return GenerationOutcome(ok=True, text="Preview", adapter="deterministic", finish_reason="stop")

    pages = [
        {
            "id": "material:1",
            "filename": "material.pdf",
            "original_sha256": hashlib.sha256((tmp_path / "material.pdf").read_bytes()).hexdigest(),
            "version": 1,
            "page": 1,
            "text": "Tema\nPruebas de software.\n",
        }
    ]
    with pytest.raises(ValueError, match="stale or foreign activity"):
        await diagnostic_rag_turn(
            pages,
            build_units(pages),
            "pruebas",
            [],
            scope_assessor=lambda *_: ScopeAssessment(
                "in_scope", authority_ref=binding.policy_sha256, block_id="pruebas", reason="fixture"
            ),
            assessor=lambda *_: SufficiencyAssessment("sufficient", "fixture", "fixture"),
            provider=ChangingProvider(),
            binding=binding,
            db=db,
        )
    db.close()
    engine.dispose()


@pytest.mark.asyncio
async def test_catalog_change_during_generation_rejects_preview(tmp_path):
    engine, db, _path, binding = fixture(tmp_path)
    pages = [
        {
            "id": "material:1",
            "filename": "material.pdf",
            "original_sha256": hashlib.sha256((tmp_path / "material.pdf").read_bytes()).hexdigest(),
            "version": 1,
            "page": 1,
            "text": "Tema\nPruebas de software.\n",
        }
    ]
    units = build_units(pages)

    class ChangingProvider:
        async def generate(self, _request):
            await asyncio.sleep(0)
            pages[0]["text"] = "Tema\nTexto sustituido.\n"
            return GenerationOutcome(ok=True, text="Preview", adapter="deterministic", finish_reason="stop")

    with pytest.raises(ValueError, match="verified source extraction"):
        await diagnostic_rag_turn(
            pages,
            units,
            "pruebas",
            [],
            scope_assessor=lambda *_: ScopeAssessment(
                "in_scope", authority_ref=binding.policy_sha256, block_id="pruebas", reason="fixture"
            ),
            assessor=lambda *_: SufficiencyAssessment("sufficient", "fixture", "fixture"),
            provider=ChangingProvider(),
            binding=binding,
            db=db,
        )
    db.close()
    engine.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["retire", "version", "policy", "source", "catalog", "none"])
async def test_revalidate_after_assessment_before_provider(tmp_path, change):
    engine, db, path, binding = fixture(tmp_path)
    pages, units = rag_lab._trusted_catalog(tmp_path, "selected", (), None)
    calls = []

    def assess(*_):
        if change == "retire":
            db.get(ActivityGovernance, "activity-1").status = "retired"
            db.commit()
        elif change == "version":
            db.get(ActivityConfiguration, "activity-1").version = 4
            db.commit()
        elif change == "policy":
            path.write_bytes(path.read_bytes() + b" ")
        elif change == "source":
            (tmp_path / "material.pdf").write_bytes(b"replaced")
        elif change == "catalog":
            pages[0]["text"] = "Texto sustituido"
        return SufficiencyAssessment("sufficient", "fixture", "fixture")

    class Provider:
        async def generate(self, request):
            calls.append(request)
            return GenerationOutcome(ok=True, text="Preview", adapter="deterministic", finish_reason="stop")

    async def run():
        return await diagnostic_rag_turn(
            pages,
            units,
            "pruebas",
            [],
            scope_assessor=lambda *_: ScopeAssessment(
                "in_scope", authority_ref=binding.policy_sha256, block_id="pruebas", reason="fixture"
            ),
            assessor=assess,
            provider=Provider(),
            binding=binding,
            db=db,
        )

    try:
        if change == "none":
            row = await run()
            assert len(calls) == 1
            assert row["participant_display"] is None
        else:
            with pytest.raises(ValueError):
                await run()
            assert calls == []
    finally:
        db.close()
        engine.dispose()


@pytest.mark.asyncio
@pytest.mark.parametrize("stage", ["scope", "first_assessment", "expanded_assessment", "post_review"])
@pytest.mark.parametrize("change", ["retire", "source", "quarantine"])
async def test_waits_revalidate_actual_binding_before_next_stage(tmp_path, monkeypatch, stage, change):
    from oralia.course_dialogue import full_corpus
    from oralia.course_dialogue.conversation_lab import LaboratoryConversation, PostReview

    engine, db, _, binding = fixture(tmp_path)
    decisions = tmp_path / "decisions.json"
    decisions.write_text('{"decision":"include_lab"}', encoding="utf-8")
    monkeypatch.setattr(full_corpus, "DECISIONS", decisions)
    binding = replace(
        binding, catalog_profile="full", decisions_sha256=hashlib.sha256(decisions.read_bytes()).hexdigest()
    )
    pages, units = rag_lab._trusted_catalog(tmp_path, "full", (), binding.decisions_sha256)
    assessment_calls = 0
    provider_calls = []

    async def mutate():
        await asyncio.sleep(0)
        if change == "retire":
            db.get(ActivityGovernance, "activity-1").status = "retired"
            db.commit()
        elif change == "source":
            (tmp_path / "material.pdf").write_bytes(b"changed during wait")
        else:
            decisions.write_text('{"decision":"quarantine"}', encoding="utf-8")

    async def scope(*_):
        if stage == "scope":
            await mutate()
        return ScopeAssessment(
            "in_scope", authority_ref=binding.policy_sha256, block_id="pruebas", reason="fixture"
        )

    async def assess(*_):
        nonlocal assessment_calls
        assessment_calls += 1
        if stage == "first_assessment" or (stage == "expanded_assessment" and assessment_calls == 2):
            await mutate()
        return SufficiencyAssessment(
            "insufficient" if stage == "expanded_assessment" and assessment_calls == 1 else "sufficient",
            "fixture",
            "simulated",
        )

    class Provider:
        async def generate(self, request):
            provider_calls.append(request)
            return GenerationOutcome(
                ok=True, text=f"Fixture [{units[0].id}]", adapter="deterministic", finish_reason="stop"
            )

    async def post_review(*_):
        await mutate()
        return PostReview("supported", "fixture-post-review", "simulated", simulated=True)

    try:
        lab = LaboratoryConversation(
            pages,
            units,
            binding=binding,
            db=db,
            scope_assessor=scope,
            assessor=assess,
            provider=Provider(),
            post_reviewer=post_review,
            interfaces_are_simulated=True,
        )
        row = await lab.turn("pruebas")
        assert row["reason"] == "source_or_policy_invalid"
        assert row["laboratory_preview"] is None
        assert lab.history == []
        assert len(provider_calls) == (1 if stage == "post_review" else 0)
        if stage == "scope":
            assert assessment_calls == 0
    finally:
        db.close()
        engine.dispose()
