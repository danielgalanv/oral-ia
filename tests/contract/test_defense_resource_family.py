from oralia.infrastructure.db import models
from tests.access_helpers import own_session


def test_defense_routes_cannot_close_or_process_a_session_of_another_activity_mode(
    app_client, seeded_activity
):
    with app_client.__db_sessionmaker__() as db:
        participant = models.ParticipantCode(code="other-mode-participant")
        db.add(participant)
        db.flush()
        session = models.Session(
            activity_configuration_id=seeded_activity, participant_code=participant.code, status="active"
        )
        db.add(session)
        db.commit()
        session_id = session.id
    own_session(app_client, session_id)
    prefix = f"/api/v1/defense-sessions/{session_id}"
    closed = app_client.post(f"{prefix}/defense-end")
    assert closed.status_code == 404
    assert app_client.post(f"{prefix}/defense-turns", json={"text": "respuesta"}).status_code == 404
    assert app_client.get(f"{prefix}/settings").status_code == 404
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, session_id).status == "active"
        assert db.query(models.Turn).count() == 0
