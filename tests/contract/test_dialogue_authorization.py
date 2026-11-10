"""Rendering plans cannot turn candidate text or a self-supplied hash into authority."""

import pytest

from oralia.domain.dialogue.contracts import ProposalPlan
from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
    load_output_authorization_policy,
)
from oralia.domain.policies.output_template_catalog import MATERIAL_FRAGMENT_RESPONSE
from tests.integration.test_dialogue_authorization import published as _published
from tests.unit.test_cognitive_state import seeded_session as _seeded_session

seeded_session = _seeded_session
published = _published


def permit_reviewed_template(db, activity):
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    ).model_dump(mode="json")
    policy["allowed_templates"].append([MATERIAL_FRAGMENT_RESPONSE.template_id, 1])
    policy["allowed_scopes"]["purposes"].append("material_response")
    policy["allowed_scopes"]["actions"].append("respond")
    activity.output_authorization_policy_json = canonical_policy_json(
        OutputAuthorizationPolicy.model_validate(policy)
    )
    activity.output_authorization_policy_sha256 = canonical_policy_sha256(
        activity.output_authorization_policy_json
    )
    db.flush()


def plan(unit, **changes):
    return ProposalPlan.model_validate(
        {
            "template_id": MATERIAL_FRAGMENT_RESPONSE.template_id,
            "template_version": "1",
            "template_sha256": MATERIAL_FRAGMENT_RESPONSE.sha256,
            "action": "content_question",
            "unit_refs": [unit.id],
            **changes,
        }
    )


def test_reviewed_plan_binds_db_text_through_independent_t090(db_session, published):
    from oralia.application.orchestration.final_output_gate import decide_final_output
    from oralia.application.services.reviewed_unit_renderer import render_plan

    session, activity, _, _, unit = published
    permit_reviewed_template(db_session, activity)
    snapshot, proposal = render_plan(db_session, session, plan(unit))
    decision = decide_final_output(snapshot, proposal, allow_operational_attempt=False)
    assert decision.output_text == unit.reviewed_content and not decision.blocked
    altered = proposal.model_dump(mode="json")
    altered["text"] = "Texto inventado por el candidato."
    rejected = decide_final_output(snapshot, altered, allow_operational_attempt=False)
    assert rejected.output_text is None and rejected.blocked
    with pytest.raises(ValueError):
        render_plan(db_session, session, plan(unit, template_sha256="f" * 64))
    unit.status = "retired"
    db_session.flush()
    with pytest.raises(ValueError):
        render_plan(db_session, session, plan(unit))


def test_defense_cannot_select_explanation_as_hint_even_with_valid_template(db_session, published):
    from oralia.application.services.reviewed_unit_renderer import render_plan

    session, activity, _, _, unit = published
    permit_reviewed_template(db_session, activity)
    activity.mode = "oral_defense"
    db_session.flush()
    with pytest.raises(ValueError, match="disclosure forbidden"):
        render_plan(db_session, session, plan(unit, action="help"))


def test_greeting_template_does_not_inherit_permission_from_plain_reviewed_content(db_session, published):
    from oralia.application.orchestration.output_proposal_builder import ProposalConstructionError
    from oralia.application.services.reviewed_unit_renderer import render_plan
    from oralia.domain.policies.output_template_catalog import GREETED_REVIEWED_RESPONSE

    session, activity, _, _, unit = published
    permit_reviewed_template(db_session, activity)
    with pytest.raises(ProposalConstructionError, match="template identity is not trusted"):
        render_plan(
            db_session,
            session,
            plan(
                unit,
                template_id=GREETED_REVIEWED_RESPONSE.template_id,
                template_sha256=GREETED_REVIEWED_RESPONSE.sha256,
            ),
        )
