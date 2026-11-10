"""Contract test for GET /api/v1/catalog/agencies — contracts/api-tecnica.md, FR-003, FR-006."""

import pytest


def _register_agent(client, name: str) -> str:
    payload = {
        "name": name,
        "version": "1.0.0",
        "capabilities": [],
        "contract": {
            "agent_id": "shared-contract",
            "version": "1.0.0",
            "purpose": "test",
            "input_schema_ref": "AgentRequest",
            "output_schema_ref": "AgentResult",
            "timeout_ms": 1000,
        },
    }
    return client.post("/api/v1/agents", json=payload).json()["id"]


@pytest.mark.contract
def test_catalog_agencies_returns_registered_agency(app_client):
    agent_id = _register_agent(app_client, "agent-a")
    payload = {
        "name": "Agency 1",
        "version": "1.0.0",
        "steps": [{"step_id": "s1", "agent_id": agent_id, "role": "generator"}],
    }
    post = app_client.post("/api/v1/agencies", json=payload)
    assert post.status_code == 201

    r = app_client.get("/api/v1/catalog/agencies")
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert r.json()[0]["name"] == "Agency 1"
    # FR-003: availability status exposed for agencies, same as for agents.
    assert r.json()[0]["availability_status"] == "available"


@pytest.mark.contract
def test_register_agency_with_unknown_agent_returns_422(app_client):
    payload = {
        "name": "Agency bad",
        "version": "1.0.0",
        "steps": [{"step_id": "s1", "agent_id": "does-not-exist", "role": "generator"}],
    }
    r = app_client.post("/api/v1/agencies", json=payload)
    assert r.status_code == 422
