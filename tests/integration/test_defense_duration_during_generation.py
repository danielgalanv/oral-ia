import asyncio
from datetime import timedelta

from oralia.application.orchestration.defense_agency_composer import run_defense_turn
from oralia.domain.agents.agent_contract import AgentResult
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.contract.test_defense_output_authorization_matrix import _permit_template
from tests.integration.test_defense_text_turn import _ApprovedGrounding, _seed_defense


async def test_duration_expiring_during_generation_closes_without_waiting_for_next_turn(db_session):
    session = _seed_defense(db_session)
    activity = db_session.get(models.ActivityConfiguration, session.activity_configuration_id)
    _permit_template(activity, "defense-limit-close", "oral_defense_close", "finish")
    fragment = db_session.query(models.MaterialFragment).one()

    class Retriever:
        contract = type("Contract", (), {"agent_id": "material-retriever", "timeout_ms": 1000})()

        async def execute(self, request, cancellation):
            return AgentResult(
                status="ok",
                output={
                    "fragments": [
                        {
                            "fragment_id": fragment.id,
                            "document_id": fragment.document_id,
                            "document_version": 1,
                            "location_ref": "p1",
                            "text": fragment.text,
                        }
                    ]
                },
            )

    class SlowQuestion:
        contract = type("Contract", (), {"agent_id": "followup-question-agent", "timeout_ms": 1000})()

        async def execute(self, request, cancellation):
            await asyncio.sleep(0.08)
            return AgentResult(
                status="ok",
                output={
                    "question_text": "¿Cómo separa la arquitectura generación?",
                    "referenced_concept": "arquitectura",
                    "generation_trace": {},
                },
            )

    session.started_at = utcnow() - timedelta(seconds=activity.max_duration_seconds - 0.04)
    result = await run_defense_turn(
        db_session,
        session,
        "arquitectura generación",
        material_retriever_agent=Retriever(),
        followup_agent=SlowQuestion(),
        grounding_verifier_agent=_ApprovedGrounding(),
    )
    assert result.dialogue_action == "finish"
    assert session.status == "closed_limit_reached"
    assert result.output_text != "¿Cómo separa la arquitectura generación?"
