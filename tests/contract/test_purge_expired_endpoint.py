"""Contract test for POST /tecnica/self-study/purge-expired (forma de PurgeResult)."""

from __future__ import annotations

import pytest


@pytest.mark.contract
def test_purge_expired_response_shape(app_client):
    response = app_client.post("/api/v1/tecnica/self-study/purge-expired")
    assert response.status_code == 200
    body = response.json()
    for key in (
        "sessions_matching_criteria",
        "sessions_with_rows_deleted",
        "practice_questions_deleted",
        "coherence_incidents_deleted",
        "trace_events_deleted",
    ):
        assert key in body
        assert isinstance(body[key], int)
