"""US6 integration test: GroundingVerifierAgent classifies a proposal touching a
detected conflict as conflictiva."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
async def test_proposal_touching_conflict_is_classified_conflictiva(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "conflict_a.md", "rb") as fh:
        ra = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_a.md", fh, "text/markdown")},
        )
    with open(MATERIALS_FIXTURES_DIR / "conflict_b.md", "rb") as fh:
        rb = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_b.md", fh, "text/markdown")},
        )
    app_client.post(f"/api/v1/materials/documents/{ra.json()['id']}/activate")
    app_client.post(f"/api/v1/materials/documents/{rb.json()['id']}/activate")

    query_result = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "la capital de Testlandia",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    ).json()
    assert query_result["conflicts"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    verifier = GroundingVerifierAgent(db)
    request = AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "proposal_text": "La capital de Testlandia es Villanorte.",
            "evidence": [
                {"fragment_id": f["fragment_id"], "text": f["text"]} for f in query_result["fragments"]
            ],
            "general_knowledge_allowed": False,
        },
    )
    result = await verifier.execute(request, CancellationToken())
    db.close()

    assert result.output["verdict"] == "conflictiva"


@pytest.mark.integration
async def test_reviewed_conflict_no_longer_forces_conflictiva(app_client, seeded_course):
    """T097 (seguimiento H03, resolución de la ambigüedad parcialmente_fundamentada/
    no_fundamentada/conflictiva, ronda 2026-09-12f): FR-022b acota la persistencia de
    `conflictiva` a un conflicto "pendiente de revisión" — una vez que el profesor lo
    revisa (`review_status = "reviewed"`), una consulta posterior sobre los mismos
    materiales implicados MUST NOT seguir clasificándose como `conflictiva` por ese
    conflicto ya revisado. Ya implementado en
    `GroundingVerifierAgent._touches_unreviewed_conflict` (filtra por
    `review_status == "pending_review"`); esta prueba lo confirma explícitamente contra
    el verificador real, cerrando el hallazgo #6 de la ronda T097."""
    with open(MATERIALS_FIXTURES_DIR / "conflict_a.md", "rb") as fh:
        ra = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_a.md", fh, "text/markdown")},
        )
    with open(MATERIALS_FIXTURES_DIR / "conflict_b.md", "rb") as fh:
        rb = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("conflict_b.md", fh, "text/markdown")},
        )
    app_client.post(f"/api/v1/materials/documents/{ra.json()['id']}/activate")
    app_client.post(f"/api/v1/materials/documents/{rb.json()['id']}/activate")

    query_result = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "la capital de Testlandia",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    ).json()
    assert query_result["conflicts"]

    conflicts = app_client.get("/api/v1/materials/conflicts").json()
    assert len(conflicts) == 1
    assert conflicts[0]["review_status"] == "pending_review"
    review_r = app_client.post(f"/api/v1/materials/conflicts/{conflicts[0]['id']}/review")
    assert review_r.json()["review_status"] == "reviewed"

    Session = app_client.__db_sessionmaker__
    db = Session()
    verifier = GroundingVerifierAgent(db)
    request = AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "proposal_text": "La capital de Testlandia es Villanorte.",
            "evidence": [
                {"fragment_id": f["fragment_id"], "text": f["text"]} for f in query_result["fragments"]
            ],
            "general_knowledge_allowed": False,
        },
    )
    result = await verifier.execute(request, CancellationToken())
    db.close()

    assert result.output["verdict"] != "conflictiva"
