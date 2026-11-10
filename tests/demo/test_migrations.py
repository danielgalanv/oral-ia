from unittest.mock import patch

import pytest
from alembic import command
from sqlalchemy import inspect
from sqlalchemy.orm import Session

from oralia.application.services.index_rebuild_lock_service import acquire, release
from oralia.demo.fixtures import migration_config
from oralia.demo.resources import DemoPaths, child_environment
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import build_engine


@pytest.mark.parametrize("previous", [None, "t005_governance"])
def test_migrated_demo_matches_all_model_columns_and_real_index_lock(tmp_path, previous):
    paths = DemoPaths(tmp_path)
    paths.initialize()
    config = migration_config(paths)
    with patch.dict("os.environ", child_environment(paths, 5180), clear=True):
        if previous:
            command.upgrade(config, previous)
        command.upgrade(config, "head")
    engine = build_engine(paths.db_url)
    try:
        inspector = inspect(engine)
        assert set(Base.metadata.tables) <= set(inspector.get_table_names())
        for name, table in Base.metadata.tables.items():
            assert set(table.columns.keys()) == {c["name"] for c in inspector.get_columns(name)}
        with Session(engine) as db:
            lock = acquire(db)
            release(db, lock)
            db.commit()
    finally:
        engine.dispose()
