"""No model: exports must not leak unshown candidates or create server persistence."""

import json

from fastapi.testclient import TestClient

from oralia.documentary.__main__ import create_app
from oralia.documentary.study_lab import TrialBudget
from tests.integration.test_study_presentation_delivery import enter, turn
from tests.unit.test_study_lab import ProviderFixture, RetrievalFixture, identifier


def client_for_report():
    retrieval = RetrievalFixture()
    provider = ProviderFixture(text="```\n<script>inert</script>\n```")
    provider.diagnostic_label = "FIXTURE_REPORT_CPU_NO_LLM"
    provider.trial_budget = TrialBudget(maximum=None)
    return (
        TestClient(
            create_app(
                retrieval.package,
                manifest_name="manifest-v2.json",
                retrieval=retrieval,
                study_lab=True,
                study_chat=True,
                study_provider=provider,
            ),
            base_url="http://127.0.0.1",
        ),
        provider,
    )


def test_explicit_export_only_contains_shown_text_and_descriptive_observations():
    client, provider = client_for_report()
    with client:
        assert client.get("/api/v1/study-lab/export").status_code != 200
        enter(client)
        first = identifier()
        turn(client, first)
        before = client.get("/api/v1/study-lab/export").json()
        assert before["turns"][0]["answer"] is None
        assert "<script>" not in json.dumps(before) and before["counts"]["shown_answers"] == 0
        client.post(f"/api/v1/study-lab/{first}/shown", json={})
        data = client.get("/api/v1/study-lab/export")
        assert data.headers["cache-control"] == "no-store"
        report = data.json()
        assert (
            report["provider_kind"] == "FIXTURE_REPORT_CPU_NO_LLM"
            and report["semantic_support"] == "unverified"
        )
        assert report["counts"]["shown_answers"] == 1 and report["turns"][0]["answer"] == provider.text
        assert "raw_candidate" not in data.text and "web_trace" not in data.text and "grade" not in report
        md = client.get("/api/v1/study-lab/export?format=markdown")
        assert "````text" in md.text and ".md" in md.headers["content-disposition"]
        assert len(provider.requests) == 1
        client.post("/api/v1/study-lab/close", json={})
        assert client.get("/api/v1/study-lab/export").status_code != 200


def test_autoestudio_has_no_residual_thirty_two_attempt_ceiling():
    client, provider = client_for_report()
    provider.text = "Respuesta de transporte"
    with client:
        enter(client)
        for _ in range(34):
            key = identifier()
            assert turn(client, key).json()["status"] == "prepared_unverified"
            assert client.post(f"/api/v1/study-lab/{key}/shown", json={}).status_code == 200
        report = client.get("/api/v1/study-lab/export").json()
        assert report["counts"]["shown_answers"] == 34 and report["repeated_questions"][0]["count"] == 34
        assert len(provider.requests) == 34
