"""Explicit candidate policy/templates; the ordinary default catalog is unchanged."""

from oralia.domain.dialogue.catalog import guided_policy
from oralia.domain.policies.output_authorization_policy import OutputAuthorizationPolicy
from oralia.domain.policies.output_template_catalog import (
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    GREETED_REVIEWED_RESPONSE,
    OutputTemplateEntry,
)

SEMANTIC_POLICY_ID = "guided-semantic-candidate/v1"


def _entry(identity, text):
    return OutputTemplateEntry.from_text(
        template_id=identity,
        version=1,
        message_type="normal",
        text=text,
        topic_ref="activity",
        purpose_ref="material_response",
        action_ref="respond",
    )


SEMANTIC_GREETED_2 = _entry("semantic-greeted-reviewed-2", "Hola. {content_0} {content_1}")
SEMANTIC_GREETED_3 = _entry("semantic-greeted-reviewed-3", "Hola. {content_0} {content_1} {content_2}")
SEMANTIC_RECEIPT = _entry(
    "semantic-reviewed-message-receipt", "Mensaje recibido. Para contrastar la idea: {content}"
)
SEMANTIC_GREETING_TEMPLATES = {1: GREETED_REVIEWED_RESPONSE, 2: SEMANTIC_GREETED_2, 3: SEMANTIC_GREETED_3}
SEMANTIC_TEMPLATE_CATALOG = DEFAULT_OUTPUT_TEMPLATE_CATALOG.extended(
    [SEMANTIC_GREETED_2, SEMANTIC_GREETED_3, SEMANTIC_RECEIPT]
)


def semantic_guided_policy(recipient):
    """Authoring only: this helper cannot publish a policy, unit or activity."""
    data = guided_policy(
        recipient, screenless=True, pedagogy=True, advanced=True, continuity=True
    ).model_dump(mode="json")
    data["policy_id"] = SEMANTIC_POLICY_ID
    data["allowed_templates"] += [
        [entry.template_id, entry.version]
        for entry in [SEMANTIC_GREETED_2, SEMANTIC_GREETED_3, SEMANTIC_RECEIPT]
    ]
    return OutputAuthorizationPolicy.model_validate(data)
