from tests.access_helpers import own_session
from tests.integration.test_defense_text_turn import _seed_defense


def test_defense_text_endpoint_returns_nullable_contract(app_client) -> None:
    Session = app_client.__db_sessionmaker__
    with Session() as db:
        session = _seed_defense(db)
        session_id = session.id
        db.commit()
    own_session(app_client, session_id)
    response = app_client.post(
        f"/api/v1/defense-sessions/{session_id}/defense-turns",
        json={"text": "Separé generación y verificación."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["dialogue_action"] == "ask"
    assert isinstance(body["output_text"], str)
    assert body["speech"] is None
    assert body["blocked"] is False


def test_missing_session_is_404(app_client) -> None:
    own_session(app_client, "missing")
    response = app_client.post("/api/v1/defense-sessions/missing/defense-turns", json={"text": "respuesta"})
    assert response.status_code == 404
