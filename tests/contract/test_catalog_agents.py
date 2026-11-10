"""Contract test for GET /api/v1/catalog/agents — contracts/api-tecnica.md, FR-003."""

import pytest


@pytest.mark.contract
def test_catalog_agents_empty_by_default(app_client):
    r = app_client.get("/api/v1/catalog/agents")
    assert r.status_code == 200
    assert r.json() == []


@pytest.mark.contract
def test_catalog_agents_returns_registered_agent_descriptor(app_client):
    payload = {
        "name": "test-agent",
        "version": "1.0.0",
        "capabilities": ["interpret"],
        "contract": {
            "agent_id": "test-agent-contract",
            "version": "1.0.0",
            "purpose": "test",
            "input_schema_ref": "AgentRequest",
            "output_schema_ref": "AgentResult",
            "timeout_ms": 1000,
        },
    }
    post = app_client.post("/api/v1/agents", json=payload)
    assert post.status_code == 201

    r = app_client.get("/api/v1/catalog/agents")
    assert r.status_code == 200
    descriptors = r.json()
    assert len(descriptors) == 1
    assert descriptors[0]["name"] == "test-agent"
    assert descriptors[0]["contract"]["timeout_ms"] == 1000
