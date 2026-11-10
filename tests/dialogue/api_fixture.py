"""Public API preparation of synthetic guided activities; no response substitutions."""

import json
from pathlib import Path

from oralia.infrastructure.db import models


def checked(response, status=200):
    assert response.status_code == status, response.text
    return response.json()


def prepare_guided(
    client,
    domain="agua",
    mode="self_study",
    *,
    start=True,
    study_mode=None,
    material_disclosure=True,
    practice_reveals_solution=False,
    screenless=False,
    pedagogy=False,
    advanced=False,
    continuity=False,
    policy_transform=None,
):
    from oralia.domain.dialogue.catalog import guided_policy

    folder = Path(__file__).resolve().parents[2] / "materiales/docente/dialogue"
    pack = json.loads((folder / f"{domain}-v{2 if pedagogy else 1}.json").read_text(encoding="utf-8"))
    course = checked(
        client.post("/api/v1/governance/courses", json={"name": "Dominio sintético", "subject_code": domain}),
        201,
    )
    retention = checked(client.post("/api/v1/governance/retention-policies", json={"retention_days": 1}), 201)
    document = checked(
        client.post(
            "/api/v1/materials/documents",
            data={"course_id": course["id"]},
            files={
                "file": (pack["source_file"], (folder / pack["source_file"]).read_bytes(), "text/markdown")
            },
        ),
        201,
    )
    checked(client.post(f"/api/v1/materials/documents/{document['id']}/activate"))
    topics = [item["topic_ref"] for item in pack["objectives"]]
    initial = next(u["reviewed_content"] for u in pack["units"] if u["kind"] == "question")
    config = (
        {
            "initial_questions": [initial],
            "topics": topics,
            "summary_authorized": True,
            "transcript_retention_authorized": True,
        }
        if mode == "oral_defense"
        else {
            "enabled_modes": [
                "doubt_resolution",
                "guided_explanation",
                "practice_questions",
                "presentation_preparation",
                "concept_review",
            ],
            "summary_authorized": True,
            "retention_authorized": True,
        }
    )
    if mode == "self_study":
        config["practice_reveals_solution"] = practice_reveals_solution
    if mode == "self_study" and study_mode is not None:
        assert study_mode in config["enabled_modes"]
        config["enabled_modes"] = [study_mode, *[m for m in config["enabled_modes"] if m != study_mode]]
    policy = guided_policy(
        "synthetic-010", screenless=screenless, pedagogy=pedagogy, advanced=advanced, continuity=continuity
    ).model_dump(mode="json")
    if policy_transform is not None:
        policy_transform(policy)
    if not material_disclosure:
        policy["allowed_disclosures"] = [
            rule for rule in policy["allowed_disclosures"] if rule["provenance"] != "activity_material"
        ]
    activity = checked(
        client.post(
            "/api/v1/governance/activities",
            json={
                "activity": {
                    "course_id": course["id"],
                    "name": "Diálogo sintético",
                    "subject": domain,
                    "objective": "Practicar con contenido revisado",
                    "mode": mode,
                    "language": "es",
                    "max_turns": 16,
                    "max_duration_seconds": 600,
                    "retention_policy_id": retention["id"],
                    "output_authorization_policy": policy,
                },
                "model_id": "guided_controlled",
                "material_versions": [{"document_id": document["id"], "version": document["version"]}],
                "mode_config": config,
            },
        ),
        201,
    )
    with client.__db_sessionmaker__() as db:
        fragments = (
            db.query(models.MaterialFragment)
            .filter_by(document_id=document["id"])
            .order_by(models.MaterialFragment.sequence_index)
            .all()
        )
        fragment_values = [(f.id, " ".join(f.text.split())) for f in fragments]

    def source_refs(unit):
        content = " ".join(unit["reviewed_content"].split())
        matched = [ref for ref, text in fragment_values if content in text]
        if not matched:
            explanation = next(
                u["reviewed_content"]
                for u in pack["units"]
                if u["topic_ref"] == unit["topic_ref"] and u["kind"] == "explanation"
            )
            matched = [ref for ref, text in fragment_values if " ".join(explanation.split()) in text]
        assert matched, (unit["key"], "source content not found in actual ingested fragments")
        return [
            {"document_id": document["id"], "document_version": document["version"], "fragment_id": ref}
            for ref in matched[:5]
        ]

    pending = list(pack["units"])
    ids = {}
    while pending:
        ready = [
            u for u in pending if all(key in ids for refs in u["relations_by_key"].values() for key in refs)
        ]
        assert ready, "cyclic synthetic teaching relations"
        for unit in ready:
            created = checked(
                client.post(
                    "/api/v1/governance/teaching-units",
                    json={
                        "course_id": course["id"],
                        "kind": unit["kind"],
                        "topic_ref": unit["topic_ref"],
                        "subgoal_ref": unit["subgoal_ref"],
                        "reviewed_content": unit["reviewed_content"],
                        "reveal_policy": unit["reveal_policy"],
                        "source_refs": source_refs(unit),
                        "activity_refs": [activity["id"]],
                        "relations": {
                            kind: [ids[key] for key in refs]
                            for kind, refs in unit["relations_by_key"].items()
                        },
                    },
                ),
                201,
            )
            checked(
                client.post(
                    f"/api/v1/governance/teaching-units/{created['id']}/publish", json={"reviewed": True}
                )
            )
            ids[unit["key"]] = created["id"]
            pending.remove(unit)
    checked(client.post(f"/api/v1/governance/activities/{activity['id']}/activate"))
    session = (
        checked(
            client.post(
                "/api/v1/sessions",
                json={"participant_code": "synthetic-010", "activity_configuration_id": activity["id"]},
            ),
            201,
        )
        if start
        else None
    )
    return {"activity": activity, "session": session, "units": ids, "document": document, "topics": topics}
