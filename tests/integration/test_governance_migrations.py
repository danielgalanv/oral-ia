import sqlite3
from contextlib import closing
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config


@pytest.mark.parametrize("start", [None, "t004_oral_defense"])
def test_governance_migration_clean_and_upgrade_preserve_historical_ddl(tmp_path, monkeypatch, start):
    path = tmp_path / "governance-migration.db"
    url = f"sqlite:///{path.as_posix()}"
    monkeypatch.setenv("ORALIA_DB_URL", url)
    config = Config()
    config.set_main_option(
        "script_location",
        str(Path(__file__).resolve().parents[2] / "src/oralia/infrastructure/db/migrations"),
    )
    config.set_main_option("sqlalchemy.url", url)
    before = {}
    if start:
        command.upgrade(config, start)
        with closing(sqlite3.connect(path)) as db:
            before = dict(
                db.execute(
                    "SELECT name,sql FROM sqlite_master WHERE type='table' AND name!='alembic_version'"
                )
            )
    command.upgrade(config, "t005_governance")
    with closing(sqlite3.connect(path)) as db:
        assert db.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "t005_governance"
        after = dict(
            db.execute("SELECT name,sql FROM sqlite_master WHERE type='table' AND name!='alembic_version'")
        )
        assert len(after) == 31
        assert all(after[key] == value for key, value in before.items())
        assert "source_activity_configuration_id" in after["activity_governance"]
        assert db.execute("SELECT sql FROM sqlite_master WHERE name='uq_governance_active_family'").fetchone()
        if start:
            assert set(after) - set(before) == {
                "activity_governance",
                "session_privacy_preference",
                "session_deletion_receipt",
            }
