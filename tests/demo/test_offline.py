import socket
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from oralia.application.commands.end_study_session import end_study_session
from oralia.application.commands.start_session import StartSessionInput, start_session
from oralia.application.commands.submit_study_turn import submit_study_turn
from oralia.demo.fixtures import prepare
from oralia.demo.resources import DemoPaths, child_environment
from oralia.infrastructure.db import models
from oralia.infrastructure.db.engine import build_engine


@pytest.mark.asyncio
async def test_prepared_full_demo_runs_real_retrieval_offline_without_external_sockets(tmp_path, monkeypatch):
    attempted = []
    original = socket.socket.connect

    def local_only(sock, address):
        if isinstance(address, tuple) and address[0] not in {"127.0.0.1", "localhost", "::1"}:
            attempted.append(address[0])
            raise AssertionError("external network forbidden during offline rehearsal")
        return original(sock, address)

    monkeypatch.setattr(socket.socket, "connect", local_only)
    paths = DemoPaths(tmp_path)
    with patch.dict("os.environ", child_environment(paths, 5180), clear=True):
        manifest = prepare(paths)
        assert prepare(paths) == manifest
        engine = build_engine(paths.db_url)
        try:
            with Session(engine, expire_on_commit=False) as db:
                activity = next(a for a in manifest["activities"] if a["mode"] == "self_study")
                session = start_session(
                    db,
                    StartSessionInput(participant_code="demo-007", activity_configuration_id=activity["id"]),
                )
                result = await submit_study_turn(db, session, "¿A qué temperatura hierve el agua?")
                assert result.sources
                assert "100" in (result.output_text or "")
                config = (
                    db.query(models.SelfStudyActivityConfig)
                    .filter_by(activity_configuration_id=activity["id"])
                    .one()
                )
                end_study_session(db, session, config, status="closed_by_participant")
                assert not db.query(models.ConsentRecord).filter_by(session_id=session.id).count()
                assert all(t.input_text == "" for t in db.query(models.Turn).filter_by(session_id=session.id))
                db.commit()
        finally:
            engine.dispose()
    assert not attempted


@pytest.mark.asyncio
async def test_text_only_missing_embeddings_keeps_textual_flow_without_claiming_sources(
    tmp_path, monkeypatch
):
    from oralia.infrastructure.embeddings.sentence_transformer_adapter import (
        SentenceTransformerEmbeddingAdapter,
    )

    def missing(_self, _texts):
        raise OSError("injected missing local embeddings")

    monkeypatch.setattr(SentenceTransformerEmbeddingAdapter, "embed", missing)
    paths = DemoPaths(tmp_path)
    manifest = prepare(paths, text_only=True)
    with patch.dict("os.environ", child_environment(paths, 5180), clear=True):
        engine = build_engine(paths.db_url)
        try:
            with Session(engine, expire_on_commit=False) as db:
                activity = next(a for a in manifest["activities"] if a["mode"] == "self_study")
                session = start_session(
                    db,
                    StartSessionInput(participant_code="demo-007", activity_configuration_id=activity["id"]),
                )
                result = await submit_study_turn(db, session, "¿A qué temperatura hierve el agua?")
                assert result.sources == []
                assert result.output_text is not None
                assert "100" not in result.output_text
        finally:
            engine.dispose()
