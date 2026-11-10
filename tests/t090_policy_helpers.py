"""Explicit minimal output policies for tests that create new activity configurations."""

from collections.abc import Iterable

from oralia.domain.policies.output_authorization_policy import (
    OutputAuthorizationPolicy,
    canonical_policy_json,
    canonical_policy_sha256,
)


def minimal_output_policy(
    *,
    recipients: Iterable[str] = ("participant",),
    general_knowledge_allowed: bool = False,
    policy_id: str = "test-minimal-output-policy",
) -> OutputAuthorizationPolicy:
    recipient_values = tuple(recipients)
    return OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": policy_id,
            "policy_version": 1,
            "allowed_recipients": recipient_values,
            "allowed_disclosures": [
                {
                    "category": "public_activity",
                    "provenance": "trusted_template",
                    "recipient": recipient,
                }
                for recipient in recipient_values
            ],
            "allowed_scopes": {
                "topics": ["activity"],
                "purposes": ["acknowledge_turn"],
                "actions": ["continue"],
            },
            "general_knowledge_allowed": general_knowledge_allowed,
            "allowed_templates": [["sc007-acknowledgement", 1]],
            "allowed_operational_messages": [],
        }
    )


def minimal_output_policy_storage(**kwargs: object) -> tuple[str, str]:
    policy = minimal_output_policy(**kwargs)
    policy_json = canonical_policy_json(policy)
    return policy_json, canonical_policy_sha256(policy_json)


def minimal_output_policy_columns(**kwargs: object) -> dict[str, str]:
    policy_json, policy_sha256 = minimal_output_policy_storage(**kwargs)
    return {
        "output_authorization_policy_json": policy_json,
        "output_authorization_policy_sha256": policy_sha256,
    }


def configure_minimal_output_policy(
    app_client,
    activity_id: str,
    *,
    recipients: Iterable[str],
) -> None:
    """Replace a fixture policy with the exact recipients used by one test."""

    from oralia.infrastructure.db import models

    policy_json, policy_sha256 = minimal_output_policy_storage(recipients=recipients)
    db = app_client.__db_sessionmaker__()
    try:
        activity = db.get(models.ActivityConfiguration, activity_id)
        activity.output_authorization_policy_json = policy_json
        activity.output_authorization_policy_sha256 = policy_sha256
        db.commit()
    finally:
        db.close()


def configure_test_recipients(app_client, activity_id: str, *, recipients: Iterable[str]) -> None:
    """Declare synthetic entry recipients before first use, preserving other rules.

    Feature 010 checks recipient eligibility at entry. Historical lifecycle fixtures
    must therefore declare the codes their test uses; this helper never runs in
    production and cannot change an activity after it has been used.
    """
    from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
    from oralia.infrastructure.db import models

    with app_client.__db_sessionmaker__() as db:
        activity = db.get(models.ActivityConfiguration, activity_id)
        assert activity.immutable_since is None
        policy = load_output_authorization_policy(
            activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
        ).model_dump(mode="json")
        declared = tuple(recipients)
        rules = {(rule["category"], rule["provenance"]) for rule in policy["allowed_disclosures"]}
        policy["allowed_recipients"] = list(declared)
        policy["allowed_disclosures"] = [
            {"category": category, "provenance": provenance, "recipient": recipient}
            for category, provenance in sorted(rules)
            for recipient in declared
        ]
        validated = OutputAuthorizationPolicy.model_validate(policy)
        activity.output_authorization_policy_json = canonical_policy_json(validated)
        activity.output_authorization_policy_sha256 = canonical_policy_sha256(
            activity.output_authorization_policy_json
        )
        db.commit()
