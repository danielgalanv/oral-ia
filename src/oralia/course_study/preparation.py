"""Authenticated API preparation, shared by terminal and isolated integration test."""

from oralia.course_study.materials import DEFAULT_SOURCE, selected_material
from oralia.domain.materials.query_excerpt import PROFILE_ID
from oralia.domain.policies import output_template_catalog as catalog

RECIPIENT = "autoestudio-is-local"


def checked(response, status=200):
    if response.status_code != status:
        raise RuntimeError(f"API preparation rejected ({response.status_code}): {response.text[:500]}")
    return response.json()


def prepare(client, source=DEFAULT_SOURCE):
    data, provenance = selected_material(source)
    course = checked(
        client.post(
            "/api/v1/governance/courses",
            json={
                "name": "Ingeniería del Software — autoestudio real aislado",
                "subject_code": "IS-REAL-011",
            },
        ),
        201,
    )
    retention = checked(client.post("/api/v1/governance/retention-policies", json={"retention_days": 1}), 201)
    document = checked(
        client.post(
            "/api/v1/materials/documents",
            data={"course_id": course["id"]},
            files={"file": (provenance["derived_name"], data, "application/pdf")},
        ),
        201,
    )
    checked(client.post(f"/api/v1/materials/documents/{document['id']}/activate"))
    names = [
        "MATERIAL_FRAGMENT_RESPONSE",
        "MATERIAL_FRAGMENT_RESPONSE_2",
        "MATERIAL_FRAGMENT_RESPONSE_3",
        "SELF_STUDY_MISSING_INFO",
        "SELF_STUDY_CONFLICT",
        "SELF_STUDY_INCOHERENCE",
        "SELF_STUDY_GENERAL_KNOWLEDGE_NOTICE",
        "SELF_STUDY_DEFAULT_PRACTICE_QUESTION",
    ]
    entries = [getattr(catalog, name) for name in names]
    operational = catalog.SAFE_TECHNICAL_FALLBACK
    policy = {
        "schema_version": 1,
        "policy_id": PROFILE_ID,
        "policy_version": 1,
        "allowed_recipients": [RECIPIENT],
        "allowed_disclosures": [
            {"category": "texto", "provenance": "activity_material", "recipient": RECIPIENT},
            {"category": "public_activity", "provenance": "trusted_template", "recipient": RECIPIENT},
        ],
        "allowed_scopes": {
            "topics": list(dict.fromkeys(e.topic_ref for e in entries + [operational])),
            "purposes": list(dict.fromkeys(e.purpose_ref for e in entries + [operational])),
            "actions": list(dict.fromkeys(e.action_ref for e in entries + [operational])),
        },
        "general_knowledge_allowed": False,
        "allowed_templates": [{"template_id": e.template_id, "version": e.version} for e in entries],
        "allowed_operational_messages": [
            {"operational_message_id": operational.template_id, "version": operational.version}
        ],
    }
    activity = checked(
        client.post(
            "/api/v1/governance/activities",
            json={
                "activity": {
                    "course_id": course["id"],
                    "name": "Validación y calidad de requisitos — citas de diapositivas",
                    "subject": "Ingeniería del Software",
                    "objective": (
                        "validacion_requisitos/calidad_requisitos; necesidades, calidad, riesgos, tareas "
                        "y comprobabilidad; extractivo limitado, no tutor generativo"
                    ),
                    "mode": "self_study",
                    "language": "es",
                    "max_turns": 30,
                    "max_duration_seconds": 900,
                    "retention_policy_id": retention["id"],
                    "output_authorization_policy": policy,
                },
                "model_id": "deterministic",
                "material_versions": [{"document_id": document["id"], "version": document["version"]}],
                "mode_config": {
                    "enabled_modes": ["doubt_resolution"],
                    "summary_authorized": False,
                    "retention_authorized": False,
                    "practice_reveals_solution": False,
                },
            },
        ),
        201,
    )
    checked(client.post(f"/api/v1/governance/activities/{activity['id']}/activate"))
    return {
        "course_id": course["id"],
        "activity_id": activity["id"],
        "document": document,
        "provenance": provenance,
        "profile": "extractive_limited",
        "policy": PROFILE_ID,
        "human_review": "pending",
        "retention": False,
    }
