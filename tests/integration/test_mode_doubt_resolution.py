"""Integration test: flujo completo doubt_resolution — duda cubierta → respuesta
fundamentada con fuentes, concepts_addressed actualizado, agents_selected registrado
(SC-001, Escenario A, FR-003)."""

from __future__ import annotations

import pytest

from oralia.domain.policies.output_authorization_policy import (
    AllowedScope,
    DisclosureRule,
    OutputAuthorizationPolicy,
    TemplateReference,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import (
    MATERIAL_FRAGMENT_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE_2,
    MATERIAL_FRAGMENT_RESPONSE_3,
    SAFE_TECHNICAL_FALLBACK,
    SELF_STUDY_CONFLICT,
    SELF_STUDY_DEFAULT_PRACTICE_QUESTION,
    SELF_STUDY_GENERAL_KNOWLEDGE_NOTICE,
    SELF_STUDY_INCOHERENCE,
    SELF_STUDY_MISSING_INFO,
)
from oralia.infrastructure.db import models
from tests.conftest import MATERIALS_FIXTURES_DIR


def _authorize_catalogued_self_study_outputs(
    app_client,
    activity_id: str,
    participant_code: str,
    *,
    general_knowledge_allowed: bool = False,
    operational_fallback_allowed: bool = False,
) -> None:
    entries = (
        MATERIAL_FRAGMENT_RESPONSE,
        MATERIAL_FRAGMENT_RESPONSE_2,
        MATERIAL_FRAGMENT_RESPONSE_3,
        SELF_STUDY_MISSING_INFO,
        SELF_STUDY_CONFLICT,
        SELF_STUDY_INCOHERENCE,
        SELF_STUDY_GENERAL_KNOWLEDGE_NOTICE,
        SELF_STUDY_DEFAULT_PRACTICE_QUESTION,
    )
    scoped_entries = (*entries, SAFE_TECHNICAL_FALLBACK) if operational_fallback_allowed else entries
    policy = OutputAuthorizationPolicy(
        schema_version=1,
        policy_id=f"self-study-{activity_id}",
        policy_version=1,
        allowed_recipients=(participant_code,),
        allowed_disclosures=(
            DisclosureRule(
                category="texto",
                provenance="activity_material",
                recipient=participant_code,
            ),
        ),
        allowed_scopes=AllowedScope(
            topics=tuple(dict.fromkeys(entry.topic_ref for entry in scoped_entries)),
            purposes=tuple(dict.fromkeys(entry.purpose_ref for entry in scoped_entries)),
            actions=tuple(dict.fromkeys(entry.action_ref for entry in scoped_entries)),
        ),
        general_knowledge_allowed=general_knowledge_allowed,
        allowed_templates=tuple(TemplateReference(entry.template_id, entry.version) for entry in entries),
        allowed_operational_messages=(
            ((SAFE_TECHNICAL_FALLBACK.template_id, SAFE_TECHNICAL_FALLBACK.version),)
            if operational_fallback_allowed
            else ()
        ),
    )
    raw_policy = canonical_policy_json(policy)
    db = app_client.__db_sessionmaker__()
    try:
        activity = db.get(models.ActivityConfiguration, activity_id)
        activity.output_authorization_policy_json = raw_policy
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(raw_policy)
        activity.general_knowledge_allowed = general_knowledge_allowed
        db.commit()
    finally:
        db.close()


def _setup_activity_with_material(
    app_client,
    self_study_activity,
    enabled_modes,
    *,
    participant_code: str | None = None,
    general_knowledge_allowed: bool = False,
    operational_fallback_allowed: bool = False,
):
    activity_id = self_study_activity["activity_id"]
    course_id = self_study_activity["course_id"]

    with open(MATERIALS_FIXTURES_DIR / "sample.docx", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": course_id, "activity_configuration_ids": [activity_id]},
            files={
                "file": (
                    "sample.docx",
                    fh,
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": enabled_modes,
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )
    if participant_code is not None:
        _authorize_catalogued_self_study_outputs(
            app_client,
            activity_id,
            participant_code,
            general_knowledge_allowed=general_knowledge_allowed,
            operational_fallback_allowed=operational_fallback_allowed,
        )
    return activity_id


@pytest.mark.integration
def test_doubt_resolution_full_flow(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution"],
        participant_code="est-doubt-001",
    )

    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-doubt-001", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    turn_r = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert turn_r.status_code == 200
    body = turn_r.json()
    assert body["mode"] == "doubt_resolution"
    assert body.get("blocked") is not True
    assert body["output_text"]
    assert body["dialogue_action"] == "respond"
    assert body["sources"], "una respuesta fundamentada MUST incluir fuentes (FR-018)"
    for source in body["sources"]:
        for key in ("document_id", "document_version", "location_ref", "fragment_text"):
            assert key in source

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    event_types = [e["event_type"] for e in trace["trace_events"]]
    assert "agents_selected" in event_types
    agents_selected = next(e for e in trace["trace_events"] if e["event_type"] == "agents_selected")
    assert agents_selected["payload"]["mode"] == "doubt_resolution"
    activated_step_ids = {s["step_id"] for s in agents_selected["payload"]["activated_steps"]}
    assert {"retrieve", "generate", "verify-grounding", "verify-constitutional"}.issubset(activated_step_ids)


@pytest.mark.integration
def test_doubt_resolution_updates_concepts_addressed(app_client, self_study_activity):
    activity_id = _setup_activity_with_material(
        app_client,
        self_study_activity,
        ["doubt_resolution"],
        participant_code="est-doubt-002",
    )
    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-doubt-002", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    concept_patches = [
        p for p in trace["state_patches"] if p["element_type"] == "retrieved_info" and p["applied"]
    ]
    assert concept_patches, "concepts_addressed MUST have been updated via a StatePatch"
