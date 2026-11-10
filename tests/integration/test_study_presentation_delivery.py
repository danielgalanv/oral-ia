"""HTTP delivery over real package bytes; generation is an explicit CPU fixture."""

import json

from fastapi.testclient import TestClient

from oralia.documentary.__main__ import create_app
from tests.unit.test_study_lab import ProviderFixture, RetrievalFixture, identifier


def client_for(provider):
    retrieval = RetrievalFixture()
    return TestClient(
        create_app(
            retrieval.package,
            manifest_name="manifest-v2.json",
            retrieval=retrieval,
            study_lab=True,
            study_provider=provider,
        ),
        base_url="http://127.0.0.1",
    )


def enter(client):
    assert client.post("/documentary/enter").status_code == 200
    assert (
        client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).status_code == 200
    )


def turn(client, key):
    return client.post("/api/v1/study-lab/turn", json={"id": key, "question": "Pregunta fixture CPU"})


def test_http_visible_text_raw_receipt_duplicate_confirmation_and_reentry():
    body = "FIXTURE CPU: explicación con tildes.\nSegunda línea <script>inerte</script>."
    raw = json.dumps({"mensaje_mostrado": body}, ensure_ascii=False)
    provider = ProviderFixture(text=raw)
    with client_for(provider) as client:
        enter(client)
        first = identifier()
        assert turn(client, first).json()["status"] == "prepared_unverified"
        display = client.get(f"/api/v1/study-lab/{first}/display").json()
        assert display["diagnostic_preview"] == body and display["raw_candidate"] == raw
        assert turn(client, first).status_code == 409
        assert len(provider.requests) == 1
        assert client.post(f"/api/v1/study-lab/{first}/shown", json={}).status_code == 200
        assert client.post(f"/api/v1/study-lab/{first}/shown", json={}).status_code == 200
        provider.text = "FIXTURE CPU: continuación"
        second = identifier()
        assert turn(client, second).json()["status"] == "prepared_unverified"
        assert len(provider.requests[1].conversation_history) == 2
        assert provider.requests[1].conversation_history[-1].content == body
        assert client.post(f"/api/v1/study-lab/{second}/shown", json={}).status_code == 200
        assert client.get("/api/v1/study-lab/state").json()["quota"]["used"] == 2
        assert client.post("/api/v1/study-lab/close", json={}).status_code == 200
        assert client.get(f"/api/v1/study-lab/{first}/display").status_code == 409
        assert (
            client.post("/api/v1/study-lab/open", json={"ephemeral_inspection_consent": True}).status_code
            == 200
        )
        assert client.get("/api/v1/study-lab/state").json()["quota"]["used"] == 2
        assert turn(client, identifier()).json()["status"] == "prepared_unverified"
        assert not provider.requests[2].conversation_history


def test_http_ambiguous_wrapper_preserves_receipt_and_allows_clean_continuation():
    raw = '{"mensaje_mostrado":"texto", "extra":"no descartar"}'
    provider = ProviderFixture(text=raw)
    with client_for(provider) as client:
        enter(client)
        first = identifier()
        assert turn(client, first).json()["status"] == "invalid_candidate_format"
        receipt = client.get(f"/api/v1/study-lab/{first}/receipt").json()
        assert receipt["raw_candidate"] == raw and receipt["diagnostic_preview"] is None
        assert client.get(f"/api/v1/study-lab/{first}/display").status_code == 409
        assert client.post(f"/api/v1/study-lab/{first}/shown", json={}).status_code == 409
        provider.text = "FIXTURE CPU: respuesta posterior"
        assert turn(client, identifier()).json()["status"] == "prepared_unverified"
        assert not provider.requests[1].conversation_history


def test_http_truncated_wrapper_never_becomes_a_complete_answer():
    provider = ProviderFixture(reason="length", text='{"mensaje_mostrado":"texto parcial')
    with client_for(provider) as client:
        enter(client)
        key = identifier()
        assert turn(client, key).json()["status"] == "incomplete_candidate"
        receipt = client.get(f"/api/v1/study-lab/{key}/receipt").json()
        assert receipt["diagnostic_preview"] is None and receipt["raw_candidate"] == provider.text
        assert client.get(f"/api/v1/study-lab/{key}/display").status_code == 409
