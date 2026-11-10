"""US3 integration test (Escenario C): a query with no coverage in authorized materials
yields no_fundamentada/no_verificable, never a confident answer."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from tests.conftest import MATERIALS_FIXTURES_DIR


@pytest.mark.integration
async def test_query_outside_coverage_never_yields_fundamentada(app_client, seeded_course):
    with open(MATERIALS_FIXTURES_DIR / "sample.pdf", "rb") as fh:
        r = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course, "activity_configuration_ids": ["act-1"]},
            files={"file": ("sample.pdf", fh, "application/pdf")},
        )
    doc_id = r.json()["id"]
    app_client.post(f"/api/v1/materials/documents/{doc_id}/activate")

    r2 = app_client.post(
        "/api/v1/materials/query",
        json={
            "query_text": "recetas de cocina italiana avanzada",
            "course_id": seeded_course,
            "activity_configuration_id": "act-1",
            "max_fragments": 5,
            "time_budget_ms": 5000,
        },
    )
    fragments = r2.json()["fragments"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    verifier = GroundingVerifierAgent(db)
    request = AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "proposal_text": "La receta perfecta de pasta carbonara lleva nata segun el documento.",
            "evidence": [{"fragment_id": f["fragment_id"], "text": f["text"]} for f in fragments],
            "general_knowledge_allowed": False,
        },
    )
    result = await verifier.execute(request, CancellationToken())
    db.close()

    assert result.output["verdict"] in ("no_fundamentada", "no_verificable")
