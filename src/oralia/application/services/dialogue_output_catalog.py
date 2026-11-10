"""Resolve the finite catalog from the activity's hash-checked policy identity."""

from oralia.domain.dialogue.semantic_templates import SEMANTIC_POLICY_ID, SEMANTIC_TEMPLATE_CATALOG
from oralia.domain.policies.output_authorization_policy import load_output_authorization_policy
from oralia.domain.policies.output_template_catalog import DEFAULT_OUTPUT_TEMPLATE_CATALOG


def activity_output_catalog(activity):
    policy = load_output_authorization_policy(
        activity.output_authorization_policy_json, activity.output_authorization_policy_sha256
    )
    return (
        SEMANTIC_TEMPLATE_CATALOG
        if policy.policy_id == SEMANTIC_POLICY_ID
        else DEFAULT_OUTPUT_TEMPLATE_CATALOG
    )
