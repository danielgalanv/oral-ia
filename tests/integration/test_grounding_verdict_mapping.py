"""Integration test: hay evidencia pero no respalda la afirmación (`no_fundamentada`) →
`acknowledge_missing_info`, nunca una respuesta inventada (US2 AC1/AC2, research.md §5)."""

from __future__ import annotations

import pytest

from oralia.domain.agents.agent_contract import AgentResult
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent
from oralia.domain.policies.output_authorization_policy import (
    AllowedScope,
    OutputAuthorizationPolicy,
    TemplateReference,
    canonical_policy_json,
    canonical_policy_sha256,
)
from oralia.domain.policies.output_template_catalog import SELF_STUDY_MISSING_INFO
from oralia.infrastructure.db import models
from tests.integration.test_mode_doubt_resolution import _setup_activity_with_material


async def _always_no_fundamentada(self, request, cancellation):
    claims = request.input.get("proposal_text", "")
    return AgentResult(
        status="ok",
        output={"verdict": "no_fundamentada", "supported_claims": [], "unsupported_claims": [claims]},
        confidence=None,
        trace={"verdict": "no_fundamentada"},
    )


def _authorize_missing_info_output(app_client, activity_id: str, participant_code: str) -> None:
    entry = SELF_STUDY_MISSING_INFO
    policy = OutputAuthorizationPolicy(
        schema_version=1,
        policy_id="grounding-verdict-mapping",
        policy_version=1,
        allowed_recipients=(participant_code,),
        allowed_disclosures=(),
        allowed_scopes=AllowedScope(
            topics=(entry.topic_ref,),
            purposes=(entry.purpose_ref,),
            actions=(entry.action_ref,),
        ),
        general_knowledge_allowed=False,
        allowed_templates=(TemplateReference(entry.template_id, entry.version),),
        allowed_operational_messages=(),
    )
    raw_policy = canonical_policy_json(policy)
    db = app_client.__db_sessionmaker__()
    try:
        activity = db.get(models.ActivityConfiguration, activity_id)
        activity.output_authorization_policy_json = raw_policy
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(raw_policy)
        db.commit()
    finally:
        db.close()


@pytest.mark.integration
def test_unsupported_claim_acknowledges_missing_info_never_invents(
    app_client, self_study_activity, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.setattr(GroundingVerifierAgent, "execute", _always_no_fundamentada)

    activity_id = _setup_activity_with_material(app_client, self_study_activity, ["doubt_resolution"])
    _authorize_missing_info_output(app_client, activity_id, "est-nofund-001")
    session_id = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-nofund-001", "activity_configuration_id": activity_id},
    ).json()["session_id"]

    response = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Qué contiene el documento de prueba?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body.get("blocked") is not True
    assert body["sources"] == [], "no proposal built on unsupported claims MUST be presented as sourced"

    trace = app_client.get(f"/api/v1/sessions/{session_id}/trace").json()
    activated_step_ids = {
        s["step_id"]
        for s in next(e for e in trace["trace_events"] if e["event_type"] == "agents_selected")["payload"][
            "activated_steps"
        ]
    }
    assert {"generate", "verify-grounding"}.issubset(activated_step_ids)
