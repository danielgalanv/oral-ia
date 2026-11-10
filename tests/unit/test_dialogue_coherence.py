from uuid import uuid4

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.coherence_verifier_agent import CoherenceVerifierAgent


async def test_requested_exact_repeat_preserves_contradiction_check():
    agent = CoherenceVerifierAgent()
    payload = {
        "proposal_text": "El líquido cambia de estado.",
        "prior_statements": ["El líquido cambia de estado."],
        "active_sources": ["El líquido cambia de estado."],
        "concepts_addressed": ["cambio"],
        "turn_number": 5,
        "max_turns": 8,
        "dialogue_schema_version": 2,
        "intentional_repeat": True,
        "structural_progress": True,
    }
    result = await agent.execute(
        AgentRequest(session_id=uuid4(), turn_id=uuid4(), input=payload), CancellationToken()
    )
    assert result.output["verdict"] == "approved"
    payload["active_sources"] = ["El líquido no cambia de estado."]
    result = await agent.execute(
        AgentRequest(session_id=uuid4(), turn_id=uuid4(), input=payload), CancellationToken()
    )
    assert result.output["verdict"] == "block"


async def test_v2_conjunct_negation_does_not_negate_another_operation():
    result = await CoherenceVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "proposal_text": "La validación explica el campo requerido que falta.",
                "prior_statements": [
                    "La validación explica el campo requerido que falta y no guarda registros."
                ],
                "dialogue_schema_version": 2,
                "structural_progress": True,
            },
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "reformulate"
    assert result.output["incident_types"] == ["repeticion"]


async def test_requested_focus_can_extract_reviewed_unit_but_not_repeat_or_contradict():
    payload = {
        "dialogue_schema_version": 2,
        "proposal_text": "La entrada recibe registros.",
        "prior_statements": ["La entrada recibe registros. La validación comprueba sus campos."],
        "active_sources": ["La entrada recibe registros."],
        "structural_progress": True,
        "requested_focus": "example",
        "focused_reviewed_unit": "La entrada recibe registros.",
    }

    async def check():
        return await CoherenceVerifierAgent().execute(
            AgentRequest(session_id=uuid4(), turn_id=uuid4(), input=payload), CancellationToken()
        )

    assert (await check()).output["verdict"] == "approved"
    payload["prior_statements"] = ["La entrada recibe registros."]
    assert (await check()).output["verdict"] == "reformulate"
    payload["prior_statements"] = ["La entrada recibe registros. La validación comprueba sus campos."]
    payload["active_sources"] = ["La entrada no recibe registros."]
    assert (await check()).output["verdict"] == "block"


async def test_v2_different_predicates_are_not_opposite_assertions():
    proposal = (
        "La salida presenta un resultado comprensible: "
        "confirmación de registro aceptado o aviso de validación. "
        "Presentar ese resultado no añade por sí mismo otra operación de almacenamiento."
    )
    payload = {
        "dialogue_schema_version": 2,
        "proposal_text": proposal,
        "prior_statements": [
            "Conservar un registro y presentar su resultado son responsabilidades diferentes."
        ],
        "active_sources": [proposal],
        "structural_progress": True,
    }

    async def check():
        return await CoherenceVerifierAgent().execute(
            AgentRequest(session_id=uuid4(), turn_id=uuid4(), input=payload), CancellationToken()
        )

    assert (await check()).output["verdict"] == "approved"
    payload["prior_statements"] = ["La salida no presenta un resultado comprensible."]
    assert (await check()).output["verdict"] == "block"


async def test_v2_synonymous_predicate_contradiction_still_blocks():
    result = await CoherenceVerifierAgent().execute(
        AgentRequest(
            session_id=uuid4(),
            turn_id=uuid4(),
            input={
                "dialogue_schema_version": 2,
                "proposal_text": "La salida conserva registros.",
                "prior_statements": ["La salida no guarda registros."],
                "structural_progress": True,
            },
        ),
        CancellationToken(),
    )
    assert result.output["verdict"] == "block"


async def test_v2_polarity_tracks_explicit_subject_and_its_omitted_continuation():
    payload = {
        "dialogue_schema_version": 2,
        "proposal_text": "La entrada recibe registros.",
        "prior_statements": ["El almacenamiento conserva registros. No recibe registros."],
        "active_sources": ["La entrada recibe registros."],
        "structural_progress": True,
    }

    async def check():
        return await CoherenceVerifierAgent().execute(
            AgentRequest(session_id=uuid4(), turn_id=uuid4(), input=payload), CancellationToken()
        )

    assert (await check()).output["verdict"] == "approved"
    payload["prior_statements"] = ["La entrada comprueba registros. No recibe registros."]
    assert (await check()).output["verdict"] == "block"
