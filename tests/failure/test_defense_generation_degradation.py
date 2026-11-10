import pytest

from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.domain.agents.followup_question_agent import FollowUpQuestionAgent
from oralia.infrastructure.db import models
from oralia.infrastructure.generation.deterministic_adapter import DeterministicGenerationAdapter
from oralia.infrastructure.generation.generation_port import GenerationError
from tests.integration.test_defense_text_turn import _seed_defense


class FailedGeneration:
    async def generate(self, request):
        raise GenerationError("private failure detail")


@pytest.mark.parametrize("total_failure", [False, True])
async def test_generation_failure_uses_existing_reserve_then_safe_resolution(db_session, total_failure):
    session = _seed_defense(db_session)
    agent = FollowUpQuestionAgent(
        primary=FailedGeneration(),
        secondary=(FailedGeneration() if total_failure else DeterministicGenerationAdapter()),
    )
    result = await run_defense_turn(
        db_session, session, "La arquitectura separa generación y verificación.", followup_agent=agent
    )
    assert result.dialogue_action == ("acknowledge_missing_info" if total_failure else "ask")
    assert result.output_text
    assert session.status == "active"
    assert "private failure detail" not in str(
        [event.payload for event in db_session.query(models.TraceEvent)]
    )
    events = db_session.query(models.TraceEvent).filter_by(event_type="agent_execution").all()
    if total_failure:
        assert any(event.agent_id == "safe-fallback" for event in events)
    else:
        generation = (
            db_session.query(models.TraceEvent)
            .filter_by(agent_id="followup-question-agent", event_type="generation_call")
            .one()
        )
        assert generation.payload["fallback_used"] is True
