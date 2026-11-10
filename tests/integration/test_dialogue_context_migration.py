"""Migrations operate exclusively on disposable databases, never prepared demo data."""

import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config


@pytest.mark.parametrize("previous", [None, "t007_demo_install"])
def test_dialogue_clean_upgrade_rollback_preserves_previous_rows(tmp_path, monkeypatch, previous):
    path = tmp_path / "dialogue.db"
    url = f"sqlite:///{path.as_posix()}"
    monkeypatch.setenv("ORALIA_DB_URL", url)
    cfg = Config()
    cfg.set_main_option(
        "script_location",
        str(Path(__file__).resolve().parents[2] / "src/oralia/infrastructure/db/migrations"),
    )
    cfg.set_main_option("sqlalchemy.url", url)
    if previous:
        command.upgrade(cfg, previous)
        with closing(sqlite3.connect(path)) as db:
            db.execute(
                "INSERT INTO participant_code(code,created_at) VALUES ('synthetic-preserved','2026-10-18')"
            )
            db.commit()
    command.upgrade(cfg, "t010_dialogue_context")
    with closing(sqlite3.connect(path)) as db:
        tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"teaching_units", "turn_request_receipts"} <= tables
        assert "dialogue_context" in {row[1] for row in db.execute("PRAGMA table_info(cognitive_state)")}
    command.downgrade(cfg, "t007_demo_install")
    with closing(sqlite3.connect(path)) as db:
        assert "dialogue_context" not in {row[1] for row in db.execute("PRAGMA table_info(cognitive_state)")}
        if previous:
            assert db.execute("SELECT code FROM participant_code").fetchall() == [("synthetic-preserved",)]
    command.upgrade(cfg, "t010_dialogue_context")


def test_old_snapshot_reads_without_fabricating_context():
    from oralia.domain.cognitive_state.cognitive_state import CognitiveStateSnapshot

    snapshot = CognitiveStateSnapshot(
        session_id="legacy",
        version=2,
        mode="oral_defense",
        objective="",
        activity_ref="activity",
        current_input="",
        participant_response="",
        summarized_history="",
        remaining_time=30,
        turn_number=1,
        confidence=1,
        next_action_proposed="",
    )
    assert snapshot.dialogue_context is None
