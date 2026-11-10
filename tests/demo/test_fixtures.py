import pytest
from sqlalchemy.orm import Session

from oralia.demo.fixtures import prepare
from oralia.demo.resources import DemoError, DemoPaths
from oralia.infrastructure.db import models
from oralia.infrastructure.db.engine import build_engine


def test_text_demo_seed_is_idempotent_and_does_not_rewrite_sessions(tmp_path):
    paths = DemoPaths(tmp_path)
    first = prepare(paths, text_only=True)
    second = prepare(paths, text_only=True)
    assert first == second
    engine = build_engine(paths.db_url)
    with Session(engine) as db:
        assert db.query(models.Course).count() == 1
        assert db.query(models.ActivityConfiguration).count() == 2
        assert db.query(models.MaterialDocument).count() == 1
        assert db.query(models.ConsentRecord).count() == 0
        assert {x.mode for x in db.query(models.ActivityConfiguration)} == {"self_study", "oral_defense"}
        assert all(x.status == "active" for x in db.query(models.ActivityGovernance))
        assert all(x.retention_days == 1 for x in db.query(models.RetentionPolicy))
    engine.dispose()
    with pytest.raises(DemoError, match="perfil"):
        prepare(paths, text_only=False)
