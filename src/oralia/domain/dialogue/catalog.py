"""Manually authored, versioned operational dialogue templates and explicit policy."""

from oralia.domain.policies.output_authorization_policy import OutputAuthorizationPolicy
from oralia.domain.policies.output_template_catalog import (
    CONTINUITY_NAVIGATION_TEMPLATES,
    DEFAULT_OUTPUT_TEMPLATE_CATALOG,
    DEFENSE_SUMMARY,
    GREETED_REVIEWED_RESPONSE,
    GUIDED_NOTICES,
    MATERIAL_FRAGMENT_RESPONSE,
    MATERIAL_FRAGMENT_RESPONSE_2,
    MATERIAL_FRAGMENT_RESPONSE_3,
    NAVIGATION_TEMPLATES,
    PACKAGE_NAVIGATION_TEMPLATES,
    PEDAGOGIC_NAVIGATION_TEMPLATES,
)

GUIDED_CATALOG = DEFAULT_OUTPUT_TEMPLATE_CATALOG


def guided_policy(
    recipient: str,
    *,
    screenless: bool = False,
    pedagogy: bool = False,
    advanced: bool = False,
    continuity: bool = False,
) -> OutputAuthorizationPolicy:
    """Authoring helper; publishing this policy still requires the teacher API."""
    if advanced and not pedagogy:
        raise ValueError("advanced pedagogy requires explicit pedagogy")
    if continuity and not advanced:
        raise ValueError("continuity requires explicit advanced pedagogy")
    if pedagogy and not screenless:
        raise ValueError("pedagogy requires screenless policy")
    entries = [
        MATERIAL_FRAGMENT_RESPONSE,
        MATERIAL_FRAGMENT_RESPONSE_2,
        MATERIAL_FRAGMENT_RESPONSE_3,
        DEFENSE_SUMMARY,
        *GUIDED_NOTICES.values(),
    ]
    if screenless:
        entries.extend(NAVIGATION_TEMPLATES.values())
    if pedagogy:
        entries.extend(PEDAGOGIC_NAVIGATION_TEMPLATES.values())
    if advanced:
        entries.extend(PACKAGE_NAVIGATION_TEMPLATES.values())
    if continuity:
        entries.append(GREETED_REVIEWED_RESPONSE)
        entries.extend(CONTINUITY_NAVIGATION_TEMPLATES.values())
    return OutputAuthorizationPolicy.model_validate(
        {
            "schema_version": 1,
            "policy_id": (
                "guided-screenless/v4"
                if continuity
                else (
                    "guided-screenless/v3"
                    if advanced
                    else (
                        "guided-screenless/v2"
                        if pedagogy
                        else "guided-screenless/v1" if screenless else "guided-controlled/v1"
                    )
                )
            ),
            "policy_version": 2 if continuity else 1,
            "allowed_recipients": [recipient],
            "allowed_disclosures": (
                [
                    {
                        "category": "session_navigation",
                        "provenance": "current_session_configuration",
                        "recipient": recipient,
                    },
                    {
                        "category": "retained_session_record",
                        "provenance": "consented_owner_record",
                        "recipient": recipient,
                    },
                ]
                if screenless
                else []
            )
            + [
                {
                    "category": "reviewed_teaching_unit",
                    "provenance": "teacher_reviewed",
                    "recipient": recipient,
                },
                {"category": "texto", "provenance": "activity_material", "recipient": recipient},
                {
                    "category": "defense_summary",
                    "provenance": "persisted_session_facts",
                    "recipient": recipient,
                },
            ],
            "allowed_scopes": {
                "topics": ["activity"],
                "purposes": ["material_response", "guided_control", "oral_defense_summary"],
                "actions": ["respond"],
            },
            "general_knowledge_allowed": False,
            "allowed_templates": [[e.template_id, e.version] for e in entries],
            "allowed_operational_messages": [],
        }
    )
