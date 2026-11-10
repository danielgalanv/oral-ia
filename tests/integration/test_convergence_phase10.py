"""Regression coverage for /speckit-converge Phase 10 findings: F1/T080 (Constitution
III, memory_category always "episodic"), F2/T081 (FR-007, InternalMessage never
persisted), F3/T082 (FR-009, StatePatch.element_type always "decision"), and F4/T083
(FR-017, CPU/memory monitor never wired into real execution)."""

import pytest

from oralia.infrastructure.db import models
from tests.t090_policy_helpers import configure_minimal_output_policy


@pytest.mark.integration
def test_turn_persists_internal_messages_per_agent_step(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-conv001",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-conv001", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    turn = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})
    turn_id = turn.json()["turn_id"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    messages = db.query(models.InternalMessage).filter(models.InternalMessage.turn_id == turn_id).all()
    db.close()

    assert len(messages) >= 2  # interpret + verify, at minimum
    agent_ids = {m.receiver_agent_id for m in messages}
    assert {"interpreter", "constitutional-control"}.issubset(agent_ids)
    for m in messages:
        assert m.sender_agent_id == "turn-orchestrator"
        assert m.objective
        assert m.success_condition


@pytest.mark.integration
def test_trace_events_use_more_than_one_memory_category(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-conv002",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-conv002", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})

    Session = app_client.__db_sessionmaker__
    db = Session()
    categories = {
        e.memory_category
        for e in db.query(models.TraceEvent).filter(models.TraceEvent.session_id == sid).all()
    }
    db.close()

    assert categories.issubset({"working", "episodic", "semantic", "procedural", "metacognitive"})
    assert "episodic" in categories
    assert "procedural" in categories
    assert len(categories) > 1  # not hardcoded to a single value anymore


@pytest.mark.integration
def test_state_patches_use_more_than_one_element_type(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-conv003",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-conv003", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})

    Session = app_client.__db_sessionmaker__
    db = Session()
    element_types = [
        p.element_type
        for p in db.query(models.StatePatch)
        .filter(models.StatePatch.session_id == sid)
        .order_by(models.StatePatch.created_at.asc())
        .all()
    ]
    db.close()

    valid_types = {
        "instruction",
        "observation",
        "participant_statement",
        "retrieved_info",
        "hypothesis",
        "inference",
        "decision",
        "check_result",
        "configuration",
    }
    assert set(element_types).issubset(valid_types)
    assert "participant_statement" in element_types  # not hardcoded to "decision" anymore
    assert len(set(element_types)) > 1


@pytest.mark.integration
def test_resource_usage_is_captured_for_turn_and_agent_events(app_client, seeded_activity):
    configure_minimal_output_policy(app_client, seeded_activity, recipients=("part-conv004",))
    start = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "part-conv004", "activity_configuration_id": seeded_activity},
    )
    sid = start.json()["session_id"]
    turn = app_client.post(f"/api/v1/sessions/{sid}/turns", json={"text": "hola"})
    turn_id = turn.json()["turn_id"]

    Session = app_client.__db_sessionmaker__
    db = Session()
    turn_row = db.get(models.Turn, turn_id)
    agent_events = (
        db.query(models.TraceEvent)
        .filter(models.TraceEvent.turn_id == turn_id, models.TraceEvent.event_type == "agent_execution")
        .all()
    )
    db.close()

    assert turn_row.resource_usage is not None
    assert set(turn_row.resource_usage.keys()) == {"cpu_percent", "memory_rss_mb"}
    assert turn_row.resource_usage["memory_rss_mb"] > 0

    assert len(agent_events) > 0
    for e in agent_events:
        assert e.resource_usage is not None
        assert e.resource_usage["memory_rss_mb"] > 0
