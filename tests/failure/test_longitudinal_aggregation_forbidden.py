"""Failure test: ningún endpoint/consulta de esta feature acepta participant_code como
filtro entre sesiones — session_id es la única clave (FR-011a)."""

from __future__ import annotations

import inspect

import pytest

from oralia.application.commands import purge_expired_self_study_data as purge_module
from oralia.application.services import study_session_summary_service
from oralia.interfaces.api.routers import self_study


def _source_mentions_participant_code_as_filter(module) -> bool:
    source = inspect.getsource(module)
    # A literal query/filter keyed by participant_code across sessions — not merely the
    # string appearing in an unrelated comment.
    return "participant_code ==" in source or ".filter_by(participant_code" in source


@pytest.mark.failure
def test_no_module_filters_by_participant_code():
    for module in (self_study, purge_module, study_session_summary_service):
        assert not _source_mentions_participant_code_as_filter(module), (
            f"{module.__name__} MUST NOT aggregate/filter by participant_code across sessions"
        )


@pytest.mark.failure
def test_study_trace_and_purge_endpoints_never_accept_participant_code(app_client, self_study_activity):
    from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material

    activity_id = _setup_activity_with_material(
        app_client, self_study_activity, ["doubt_resolution"], participant_code="est-noagg-001"
    )
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-noagg-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    # Passing participant_code as a query param MUST have no effect — the trace
    # endpoint only ever keys on session_id (path parameter).
    response = app_client.get(
        f"/api/v1/tecnica/sessions/{session_id}/study-trace", params={"participant_code": "est-noagg-001"}
    )
    assert response.status_code == 200

    purge_response = app_client.post(
        "/api/v1/tecnica/self-study/purge-expired", params={"participant_code": "est-noagg-001"}
    )
    assert purge_response.status_code == 200
