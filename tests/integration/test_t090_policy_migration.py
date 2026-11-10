"""T090 policy migration, trigger, succession, and historical reconstruction tests."""

import json
import sqlite3
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from pydantic import ValidationError
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from oralia.application.commands.create_activity import (
    ActivityAlreadyImmutable,
    ActivitySuccessionInput,
    replace_activity_output_authorization_policy,
    succeed_activity_configuration,
)
from oralia.domain.policies.output_authorization_policy import (
    canonical_policy_json,
    canonical_policy_sha256,
    load_output_authorization_policy,
)
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.ddl.t090_activity_policy_trigger import (
    ACTIVITY_POLICY_TRIGGER_NAME,
    CREATE_ACTIVITY_POLICY_TRIGGER_SQL,
)
from oralia.infrastructure.db.timeutil import utcnow
from tests.t090_policy_helpers import minimal_output_policy

ROOT = Path(__file__).parents[2]


def _alembic_config(db_path: Path) -> Config:
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path.as_posix()}")
    return config


def _columns(db_path: Path, table: str) -> set[str]:
    with sqlite3.connect(db_path) as connection:
        return {row[1] for row in connection.execute(f"PRAGMA table_info({table})")}


def _trigger_rows(db_path: Path) -> list[tuple[str, str]]:
    with sqlite3.connect(db_path) as connection:
        return list(
            connection.execute(
                "SELECT name, sql FROM sqlite_master WHERE type='trigger' AND name=?",
                (ACTIVITY_POLICY_TRIGGER_NAME,),
            )
        )


def _normalize_trigger_sql(sql: str) -> str:
    return " ".join(sql.replace("IF NOT EXISTS", "").split()).casefold()


def _insert_historical_activity(db_path: Path) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "INSERT INTO course(id,name,subject_code,created_at) VALUES(?,?,?,?)",
            ("course", "Course", "C1", "2026-10-15 00:00:00"),
        )
        connection.execute(
            """INSERT INTO retention_policy(
                id,version,content_scope,retention_days,access_scope,purge_rule
            ) VALUES(?,?,?,?,?,?)""",
            ("retention", 1, "session", None, "teacher", "manual"),
        )
        connection.execute(
            """INSERT INTO activity_configuration(
                id,family_id,version,course_id,name,subject,objective,mode,language,
                max_turns,max_duration_seconds,general_knowledge_allowed,
                required_agent_ids,optional_agent_ids,retention_policy_id,
                immutable_since,created_at
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                "historical",
                "family",
                1,
                "course",
                "Historical",
                "Subject",
                "Objective",
                "texto",
                "es",
                5,
                600,
                0,
                "[]",
                "[]",
                "retention",
                "2026-10-15 00:00:00",
                "2026-10-15 00:00:00",
            ),
        )


def _insert_trigger_fixture_rows(db_path: Path, prefix: str) -> tuple[str, str]:
    immutable_id = f"{prefix}-immutable"
    mutable_id = f"{prefix}-mutable"
    with sqlite3.connect(db_path) as connection:
        connection.execute(
            "INSERT OR IGNORE INTO course(id,name,subject_code,created_at) VALUES(?,?,?,?)",
            (f"{prefix}-course", "Course", prefix, "2026-10-15 00:00:00"),
        )
        connection.execute(
            """INSERT OR IGNORE INTO retention_policy(
                id,version,content_scope,retention_days,access_scope,purge_rule
            ) VALUES(?,?,?,?,?,?)""",
            (f"{prefix}-retention", 1, "session", None, "teacher", "manual"),
        )
        for activity_id, immutable_since in (
            (immutable_id, "2026-10-15 00:00:00"),
            (mutable_id, None),
        ):
            connection.execute(
                """INSERT INTO activity_configuration(
                    id,family_id,version,course_id,name,subject,objective,mode,language,
                    max_turns,max_duration_seconds,general_knowledge_allowed,
                    required_agent_ids,optional_agent_ids,retention_policy_id,
                    immutable_since,created_at,output_authorization_policy_json,
                    output_authorization_policy_sha256
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    activity_id,
                    f"{prefix}-family-{activity_id}",
                    1,
                    f"{prefix}-course",
                    "Trigger fixture",
                    "Subject",
                    "Objective",
                    "texto",
                    "es",
                    5,
                    600,
                    0,
                    "[]",
                    "[]",
                    f"{prefix}-retention",
                    immutable_since,
                    "2026-10-15 00:00:00",
                    None,
                    None,
                ),
            )
    return immutable_id, mutable_id


def _assert_trigger_enforcement(db_path: Path, prefix: str) -> None:
    immutable_id, mutable_id = _insert_trigger_fixture_rows(db_path, prefix)
    with sqlite3.connect(db_path) as connection:
        forbidden_updates = (
            (
                "output_authorization_policy_json='{}'",
                immutable_id,
            ),
            ("immutable_since=NULL", immutable_id),
            ("immutable_since='2026-10-16 00:00:00'", immutable_id),
            (
                "immutable_since=NULL, output_authorization_policy_json='{}', "
                "output_authorization_policy_sha256='changed'",
                immutable_id,
            ),
        )
        for assignment, activity_id in forbidden_updates:
            with pytest.raises(sqlite3.IntegrityError):
                connection.execute(
                    f"UPDATE activity_configuration SET {assignment} WHERE id=?",
                    (activity_id,),
                )
            connection.rollback()

        # The first step of the historical two-step bypass must now fail, so the
        # second step remains protected by the original immutable marker.
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                "UPDATE activity_configuration SET immutable_since=NULL WHERE id=?",
                (immutable_id,),
            )
        connection.rollback()
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """UPDATE activity_configuration
                   SET output_authorization_policy_json='{}' WHERE id=?""",
                (immutable_id,),
            )
        connection.rollback()

        connection.execute(
            """UPDATE activity_configuration
               SET immutable_since='2026-10-15 00:00:00' WHERE id=?""",
            (mutable_id,),
        )
        connection.commit()
        marker = connection.execute(
            "SELECT immutable_since FROM activity_configuration WHERE id=?",
            (mutable_id,),
        ).fetchone()
        assert marker == ("2026-10-15 00:00:00",)
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """UPDATE activity_configuration
                   SET immutable_since='2026-10-16 00:00:00' WHERE id=?""",
                (mutable_id,),
            )


@pytest.mark.integration
def test_alembic_round_trip_matches_create_all_trigger_and_is_idempotent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ORALIA_DB_URL", raising=False)
    migrated_path = tmp_path / "migrated.db"
    config = _alembic_config(migrated_path)
    command.upgrade(config, "8df2dd196803")
    _insert_historical_activity(migrated_path)

    command.upgrade(config, "head")
    assert {
        "output_authorization_policy_json",
        "output_authorization_policy_sha256",
    } <= _columns(migrated_path, "activity_configuration")
    assert "authorization_context" in _columns(migrated_path, "verification_result")
    with sqlite3.connect(migrated_path) as connection:
        historical = connection.execute(
            """SELECT output_authorization_policy_json,
                      output_authorization_policy_sha256
               FROM activity_configuration WHERE id='historical'"""
        ).fetchone()
    assert historical == (None, None)
    first_trigger = _trigger_rows(migrated_path)
    assert len(first_trigger) == 1

    command.downgrade(config, "8df2dd196803")
    assert _trigger_rows(migrated_path) == []
    assert "output_authorization_policy_json" not in _columns(
        migrated_path, "activity_configuration"
    )
    assert "authorization_context" not in _columns(migrated_path, "verification_result")

    command.upgrade(config, "head")
    with sqlite3.connect(migrated_path) as connection:
        connection.execute(CREATE_ACTIVITY_POLICY_TRIGGER_SQL)
    migrated_trigger = _trigger_rows(migrated_path)
    assert len(migrated_trigger) == 1

    metadata_path = tmp_path / "metadata.db"
    metadata_engine = create_engine(f"sqlite:///{metadata_path.as_posix()}")
    try:
        Base.metadata.create_all(metadata_engine)
        Base.metadata.create_all(metadata_engine)
    finally:
        metadata_engine.dispose()
    metadata_trigger = _trigger_rows(metadata_path)
    assert len(metadata_trigger) == 1
    assert migrated_trigger[0][0] == metadata_trigger[0][0] == ACTIVITY_POLICY_TRIGGER_NAME
    assert _normalize_trigger_sql(migrated_trigger[0][1]) == _normalize_trigger_sql(
        metadata_trigger[0][1]
    )
    assert _normalize_trigger_sql(migrated_trigger[0][1]) == _normalize_trigger_sql(
        CREATE_ACTIVITY_POLICY_TRIGGER_SQL
    )
    _assert_trigger_enforcement(migrated_path, "alembic")
    _assert_trigger_enforcement(metadata_path, "metadata")


def _stored_policy_state(policy_json: str | None, policy_sha256: str | None) -> str:
    if policy_json is None and policy_sha256 is None:
        return "missing_policy"
    if policy_json is None or policy_sha256 is None:
        return "invalid_context"
    try:
        load_output_authorization_policy(policy_json, policy_sha256)
    except (ValueError, ValidationError):
        return "invalid_context"
    return "valid"


@pytest.mark.integration
def test_historical_partial_corrupt_and_decoded_mutation_states(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{(tmp_path / 'states.db').as_posix()}")
    try:
        Base.metadata.create_all(engine)
        policy = minimal_output_policy()
        canonical = canonical_policy_json(policy)
        digest = canonical_policy_sha256(canonical)

        assert _stored_policy_state(None, None) == "missing_policy"
        assert _stored_policy_state(canonical, None) == "invalid_context"
        assert _stored_policy_state(None, digest) == "invalid_context"
        assert _stored_policy_state(canonical, "0" * 64) == "invalid_context"
        assert _stored_policy_state(canonical + " ", digest) == "invalid_context"
        assert _stored_policy_state(canonical, digest) == "valid"

        decoded = json.loads(canonical)
        decoded["allowed_recipients"].append("intruder")
        assert "intruder" not in load_output_authorization_policy(
            canonical,
            digest,
        ).allowed_recipients
        assert canonical_policy_sha256(canonical) == digest
    finally:
        engine.dispose()


@pytest.mark.integration
def test_succession_and_reconstruction_preserve_historical_rows(tmp_path: Path) -> None:
    engine = create_engine(f"sqlite:///{(tmp_path / 'succession.db').as_posix()}")
    try:
        Base.metadata.create_all(engine)
        with Session(engine, expire_on_commit=False) as db:
            course = models.Course(name="Course", subject_code="C1")
            retention = models.RetentionPolicy(
                content_scope="session",
                access_scope="teacher",
                purge_rule="manual",
            )
            participant = models.ParticipantCode(code="participant")
            db.add_all([course, retention, participant])
            db.flush()
            historical = models.ActivityConfiguration(
                course_id=course.id,
                name="Historical",
                subject="Subject",
                objective="Objective",
                mode="texto",
                language="es",
                max_turns=5,
                max_duration_seconds=600,
                general_knowledge_allowed=False,
                required_agent_ids=["required"],
                optional_agent_ids=["optional"],
                retention_policy_id=retention.id,
                output_authorization_policy_json=None,
                output_authorization_policy_sha256=None,
                immutable_since=utcnow(),
            )
            db.add(historical)
            db.flush()
            session = models.Session(
                activity_configuration_id=historical.id,
                participant_code=participant.code,
                status="closed_voluntary",
            )
            db.add(session)
            db.flush()
            historical_id = historical.id
            session_id = session.id

            successor = succeed_activity_configuration(
                db,
                historical.id,
                ActivitySuccessionInput(output_authorization_policy=minimal_output_policy()),
            )
            successor_id = successor.id
            with pytest.raises(ActivityAlreadyImmutable):
                replace_activity_output_authorization_policy(
                    db,
                    historical,
                    minimal_output_policy(policy_id="replacement"),
                )
            db.commit()

        with Session(engine) as reconstructed:
            old = reconstructed.get(models.ActivityConfiguration, historical_id)
            new = reconstructed.get(models.ActivityConfiguration, successor_id)
            old_session = reconstructed.get(models.Session, session_id)
            assert old is not None and new is not None and old_session is not None
            assert old.output_authorization_policy_json is None
            assert old.output_authorization_policy_sha256 is None
            assert old_session.activity_configuration_id == old.id
            assert new.id != old.id
            assert new.family_id == old.family_id
            assert new.version == old.version + 1
            assert new.immutable_since is None
            assert new.required_agent_ids == ["required"]
            assert new.optional_agent_ids == ["optional"]
            loaded = load_output_authorization_policy(
                new.output_authorization_policy_json,
                new.output_authorization_policy_sha256,
            )
            assert loaded.policy_id == "test-minimal-output-policy"

        with engine.begin() as connection:
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        """UPDATE activity_configuration
                           SET output_authorization_policy_json='{}'
                           WHERE id=:activity_id"""
                    ),
                    {"activity_id": historical_id},
                )
    finally:
        engine.dispose()
