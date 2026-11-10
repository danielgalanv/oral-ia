from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.domain.agents.agent_contract import AgentResult
from oralia.infrastructure.db import models
from tests.contract.test_defense_output_authorization_matrix import _permit_template
from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense


class InitialQuestion:
    contract = type("Contract", (), {"agent_id": "practice-question-agent", "timeout_ms": 1000})()

    def __init__(self):
        self.calls = []

    async def execute(self, request, cancellation):
        self.calls.append(request.input)
        return AgentResult(
            status="ok",
            output={
                "question_text": "¿Cómo separa la arquitectura generación y verificación?",
                "generation_trace": {"adapter": "deterministic"},
            },
        )


async def test_empty_bank_reuses_practice_agent_with_authorized_retrieval(db_session):
    session = _seed_defense(db_session)
    config = db_session.query(models.DefenseActivityConfig).one()
    config.initial_questions = []
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    activity.objective = "La arquitectura separa generación y verificación."
    _permit_template(activity, "defense-initial-question", "oral_defense", "ask")
    agent = InitialQuestion()
    result = await run_defense_turn(
        db_session,
        session,
        "",
        practice_question_agent=agent,
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert result.output_text == "¿Cómo separa la arquitectura generación y verificación?"
    assert len(agent.calls) == 1
    assert agent.calls[0]["evidence"]
    assert agent.calls[0]["previous_questions"] == []
    assert result.sources
    events = {event.event_type for event in db_session.query(models.TraceEvent)}
    assert {"agent_execution", "generation_call", "verification_combined", "turn_completed"} <= events
