"""Application dependency scoping; fictional objects, no teacher or model claim."""

from types import SimpleNamespace

import pytest

from oralia.application.services.reviewed_semantic_runtime import ReviewedSemanticRuntime
from oralia.domain.dialogue.contracts import DialogueContext


@pytest.mark.asyncio
async def test_runtime_rejects_foreign_engine_before_reading_course_or_generating():
    owned_engine = object()
    foreign_engine = object()
    runtime = ReviewedSemanticRuntime(engine=owned_engine, activity_id="owned", generation_port=object())
    db = SimpleNamespace(get_bind=lambda: SimpleNamespace(engine=foreign_engine))
    session = SimpleNamespace(activity_configuration_id="owned")
    with pytest.raises(ValueError, match="another database"):
        await runtime.propose(db, session, "synthetic", DialogueContext(), deadline_ms=32000)


@pytest.mark.asyncio
async def test_runtime_rejects_foreign_activity_without_any_course_lookup():
    engine = object()
    runtime = ReviewedSemanticRuntime(engine=engine, activity_id="owned", generation_port=object())
    db = SimpleNamespace(get_bind=lambda: SimpleNamespace(engine=engine))
    session = SimpleNamespace(activity_configuration_id="foreign")
    assert runtime.applies(session) is False
    with pytest.raises(ValueError, match="another activity"):
        await runtime.propose(db, session, "synthetic", DialogueContext(), deadline_ms=32000)
