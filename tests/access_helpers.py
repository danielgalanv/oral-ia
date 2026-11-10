"""Explicit credentials for historical fixtures that construct sessions without HTTP start."""


def own_session(client, session_id):
    token = client.app.state.local_access.issue("participant", session_id)
    client.cookies.set("oralia_participant", token)
    return token
