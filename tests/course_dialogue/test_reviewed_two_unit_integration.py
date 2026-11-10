"""Normal T090 execution with fictional published content; no real model evidence."""

import pytest

from oralia.application.services import guided_dialogue_service
from oralia.domain.dialogue.policy import GuidedChoice
from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import prepare_guided


@pytest.mark.parametrize("deny_template", [False, True])
def test_two_reviewed_units_use_the_existing_two_slot_template(app_client, monkeypatch, deny_template):
    def policy_transform(policy):
        if deny_template:
            policy["allowed_templates"] = [
                row for row in policy["allowed_templates"] if row[0] != "material-fragment-response-2"
            ]

    prepared = prepare_guided(app_client, domain="programa", policy_transform=policy_transform)
    sid = prepared["session"]["session_id"]
    root = prepared["units"]["programa-entrada-explanation"]
    example = prepared["units"]["programa-entrada-example"]
    monkeypatch.setattr(
        guided_dialogue_service,
        "choose",
        lambda *args, **kwargs: GuidedChoice(
            unit_id=root, topic_ref="entrada", additional_unit_ids=(example,)
        ),
    )
    response = app_client.post(
        f"/api/v1/sessions/{sid}/study-turns", json={"text": "Consulta sintética de entrada."}
    )
    if deny_template:
        assert response.status_code == 409, response.text
        with app_client.__db_sessionmaker__() as db:
            assert db.get(models.Session, sid).turn_count == 0
            assert db.query(models.Turn).filter_by(session_id=sid).count() == 0
        return
    assert response.status_code == 200, response.text
    payload = response.json()
    assert payload["dialogue_status"]["rendered_unit_ids"] == [root, example]
    assert payload["dialogue_status"]["grounding_verdict"] == "fundamentada"
    with app_client.__db_sessionmaker__() as db:
        turn = db.get(models.Turn, payload["turn_id"])
        proposal = db.get(models.GeneratedProposal, turn.generated_proposal_id)
        assert proposal.content["template_id"] == "material-fragment-response-2"
        assert db.get(models.VerificationResult, turn.verification_result_id).verdict == "approved"
