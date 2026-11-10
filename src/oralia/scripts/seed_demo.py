"""Demo seed data for quickstart.md: 1 Course, 1 RetentionPolicy, 1 ActivityConfiguration,
>=5 test Agents sharing one AgentContract, and >=2 Agencies reusing those agents
(SC-001, SC-002). Run with: uv run python -m oralia.scripts.seed_demo
"""

from __future__ import annotations

from oralia.application.commands.create_activity import (
    ActivityConfigurationInput,
    create_activity,
)
from oralia.application.commands.register_agency import AgencyCompositionInput, register_agency
from oralia.domain.agencies.agency import ExecutionStep
from oralia.domain.policies.output_authorization_policy import OutputAuthorizationPolicy
from oralia.domain.policies.output_template_catalog import SC007_ACKNOWLEDGEMENT
from oralia.infrastructure.db import models
from oralia.infrastructure.db.base import Base
from oralia.infrastructure.db.engine import get_engine, get_sessionmaker


def run() -> dict:
    Base.metadata.create_all(get_engine())
    db = get_sessionmaker()()
    try:
        course = models.Course(name="Demo — ORAL-IA", subject_code="DEMO101")
        db.add(course)
        db.flush()

        policy = models.RetentionPolicy(
            content_scope="session",
            access_scope="profesor",
            purge_rule="manual, sin plazo fijo en la demo",
        )
        db.add(policy)
        db.flush()

        output_policy = OutputAuthorizationPolicy.model_validate(
            {
                "schema_version": 1,
                "policy_id": "demo-sc007-policy",
                "policy_version": 1,
                "allowed_recipients": ["demo-participant"],
                "allowed_disclosures": [
                    {
                        "category": "public_activity",
                        "provenance": "trusted_template",
                        "recipient": "demo-participant",
                    }
                ],
                "allowed_scopes": {
                    "topics": [SC007_ACKNOWLEDGEMENT.topic_ref],
                    "purposes": [SC007_ACKNOWLEDGEMENT.purpose_ref],
                    "actions": [SC007_ACKNOWLEDGEMENT.action_ref],
                },
                "general_knowledge_allowed": False,
                "allowed_templates": [
                    [SC007_ACKNOWLEDGEMENT.template_id, SC007_ACKNOWLEDGEMENT.version]
                ],
                "allowed_operational_messages": [],
            }
        )

        activity = create_activity(
            db,
            ActivityConfigurationInput(
                course_id=course.id,
                name="Actividad de demostración",
                subject="Demo",
                objective="Probar el nucleo cognitivo de extremo a extremo",
                mode="texto",
                language="es",
                max_turns=20,
                max_duration_seconds=1800,
                retention_policy_id=policy.id,
                output_authorization_policy=output_policy,
            ),
        )

        # A single shared AgentContract — every test agent below implements this exact
        # shape, so the catalog can register N agents "under the same contract" (SC-001)
        # without changing the orchestrator (data-model.md: AgentContract 1-N Agent).
        contract = models.AgentContract(
            agent_id="test-agent-contract",
            version="1.0.0",
            purpose="Contrato de prueba compartido por los agentes de demostracion",
            input_schema_ref="AgentRequest",
            output_schema_ref="AgentResult",
            timeout_ms=3000,
            trace_fields=["status", "confidence"],
        )
        db.add(contract)
        db.flush()

        agent_specs = [
            ("interpreter-1", ["interpret"], "retriever"),
            ("interpreter-2", ["interpret"], "retriever"),
            ("generator-1", ["generate"], "generator"),
            ("verifier-constitutional", ["verify"], "verifier"),
            ("presenter-1", ["present"], "presenter"),
        ]
        agents = []
        for name, capabilities, _role in agent_specs:
            agent = models.Agent(
                name=name,
                version="1.0.0",
                contract_id=contract.id,
                capabilities=capabilities,
                availability_status="available",
            )
            db.add(agent)
            db.flush()
            agents.append(agent)

        by_name = {a.name: a for a in agents}

        agency_1 = register_agency(
            db,
            AgencyCompositionInput(
                name="Agencia demo — turno estandar",
                version="1.0.0",
                steps=[
                    ExecutionStep(step_id="s1", agent_id=by_name["interpreter-1"].id, role="retriever"),
                    ExecutionStep(
                        step_id="s2",
                        agent_id=by_name["generator-1"].id,
                        role="generator",
                        depends_on=["s1"],
                    ),
                    ExecutionStep(
                        step_id="s3",
                        agent_id=by_name["verifier-constitutional"].id,
                        role="verifier",
                        depends_on=["s2"],
                    ),
                    ExecutionStep(
                        step_id="s4",
                        agent_id=by_name["presenter-1"].id,
                        role="presenter",
                        depends_on=["s3"],
                    ),
                ],
                verifiers_required=["s3"],
                termination_rule="finish after presenter step",
            ),
        )

        agency_2 = register_agency(
            db,
            AgencyCompositionInput(
                name="Agencia demo — interpretacion alternativa",
                version="1.0.0",
                steps=[
                    ExecutionStep(step_id="s1", agent_id=by_name["interpreter-2"].id, role="retriever"),
                    ExecutionStep(
                        step_id="s2",
                        agent_id=by_name["generator-1"].id,
                        role="generator",
                        depends_on=["s1"],
                    ),
                    ExecutionStep(
                        step_id="s3",
                        agent_id=by_name["verifier-constitutional"].id,
                        role="verifier",
                        depends_on=["s2"],
                    ),
                ],
                verifiers_required=["s3"],
                termination_rule="finish after verifier step",
            ),
        )

        db.commit()
        return {
            "course_id": course.id,
            "activity_id": activity.id,
            "agent_ids": [a.id for a in agents],
            "agency_ids": [agency_1.id, agency_2.id],
        }
    finally:
        db.close()


if __name__ == "__main__":
    result = run()
    print(result)
