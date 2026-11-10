"""Guarded public-API preparation of proposed teacher packages in owned temporary DBs."""

from __future__ import annotations

import json
import tempfile
import unicodedata
from pathlib import Path

from fastapi.testclient import TestClient

from oralia.domain.dialogue.catalog import guided_policy
from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked

REVISION = Path(__file__).resolve().parents[2] / "materiales/docente/integracion-controlada-20261020-v3"


def normalized_quote(text):
    return " ".join(unicodedata.normalize("NFC", text).split())


def ensure_owned_temporary(client, technical_publish):
    if technical_publish is not True or not isinstance(client, TestClient):
        raise ValueError("Explicit technical publication with an owned TestClient is required")
    with client.__db_sessionmaker__() as db:
        path = Path(db.get_bind().url.database).resolve()
        if not path.is_relative_to(Path(tempfile.gettempdir()).resolve()) or not path.name.startswith(
            "test_"
        ):
            raise ValueError("Refusing publication outside the owned temporary test DB")


def binding_windows(fragments):
    ordered = sorted(fragments, key=lambda f: f["sequence_index"])
    result = [(normalized_quote(f["text"]), [f]) for f in ordered]
    for size in range(2, 6):
        for start in range(len(ordered) - size + 1):
            window = ordered[start : start + size]
            combined = normalized_quote(window[0]["text"])
            for fragment in window[1:]:
                value = normalized_quote(fragment["text"])
                overlap = 0
                for n in range(min(len(combined), len(value)), 29, -1):
                    if combined.endswith(value[:n]):
                        overlap = n
                        break
                combined = combined + value[overlap:] if overlap else combined + " " + value
            result.append((combined, window))
    return result


def resolve_source(content, windows):
    target = normalized_quote(content)
    for text, fragments in windows:
        if target in text:
            return [
                {
                    "document_id": f["document_id"],
                    "document_version": f["document_version"],
                    "fragment_id": f["id"],
                }
                for f in fragments
            ], {
                "normalized_quote": target,
                "fragment_ids": [f["id"] for f in fragments],
                "locations": [f["location_ref"] for f in fragments],
                "normalization": "NFC and whitespace only; no numeric/text inference",
            }
    raise ValueError("No complete literal source witness; publication denied")


def prepare_package(client, stream, *, technical_publish=False, policy_version=2, revision=None):
    ensure_owned_temporary(client, technical_publish)
    revision = revision or (
        REVISION.parent / "integracion-controlada-20261021-v10" if policy_version == 4 else REVISION
    )
    metadata = json.loads((revision / "revision.json").read_text(encoding="utf-8"))
    config = metadata["streams"][stream]
    domain = config["domain"]
    pack = json.loads((revision / f"{domain}-units.json").read_text(encoding="utf-8"))
    course = checked(
        client.post(
            "/api/v1/governance/courses",
            json={"name": f"Propuesta aislada {stream}, revisión humana pendiente", "subject_code": stream},
        ),
        201,
    )
    retention = checked(client.post("/api/v1/governance/retention-policies", json={"retention_days": 1}), 201)
    files = {
        "primary": Path(config["primary"]),
        "practice": Path(config["practice"]),
        "support": revision / config["support"],
    }
    if config.get("practice_support"):
        files["practice_support"] = revision / config["practice_support"]
    if config["supplement"]:
        files["supplement"] = revision / config["supplement"]
    documents = {}
    windows = {}
    for role, path in files.items():
        if path.name.startswith(("GUIA", "casos-")) or "docente" in path.parts[-2:]:
            raise ValueError("Teacher guide/oracle is not participant source")
        doc = checked(
            client.post(
                "/api/v1/materials/documents",
                data={"course_id": course["id"]},
                files={"file": (path.name, path.read_bytes())},
            ),
            201,
        )
        checked(client.post(f"/api/v1/materials/documents/{doc['id']}/activate"))
        documents[role] = doc
        with client.__db_sessionmaker__() as db:
            fragments = [
                {
                    "id": f.id,
                    "text": f.text,
                    "document_id": f.document_id,
                    "document_version": f.document_version,
                    "location_ref": f.location_ref,
                    "sequence_index": f.sequence_index,
                }
                for f in db.query(models.MaterialFragment).filter_by(document_id=doc["id"]).all()
            ]
        windows[role] = binding_windows(fragments)
    recipient = "synthetic-package-010"
    activities = {}
    topics = [o["topic_ref"] for o in pack["objectives"]]
    initial_topic = {"agua": "evaporacion", "programa": "validacion", "datos": "media"}[domain]
    initial = next(
        u["reviewed_content"]
        for u in pack["units"]
        if u["kind"] == "question" and u["topic_ref"] == initial_topic
    )
    for mode in ["self_study", "oral_defense"]:
        policy = guided_policy(
            recipient,
            screenless=True,
            pedagogy=True,
            **({"advanced": True, "continuity": policy_version == 4} if policy_version in {3, 4} else {}),
        ).model_dump(mode="json")
        mode_config = (
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
                "practice_reveals_solution": False,
            }
        )
        activity = checked(
            client.post(
                "/api/v1/governance/activities",
                json={
                    "activity": {
                        "course_id": course["id"],
                        "name": f"Propuesta {stream} {mode}, pendiente de revisión humana",
                        "subject": domain,
                        "objective": "Validación técnica aislada de propuesta; no aprobación docente",
                        "mode": mode,
                        "language": "es",
                        "max_turns": 40,
                        "max_duration_seconds": 600,
                        "retention_policy_id": retention["id"],
                        "output_authorization_policy": policy,
                    },
                    "model_id": "guided_controlled",
                    "material_versions": [
                        {"document_id": d["id"], "version": d["version"]} for d in documents.values()
                    ],
                    "mode_config": mode_config,
                },
            ),
            201,
        )
        activities[mode] = activity
    pending = list(pack["units"])
    ids = {}
    witnesses = {}
    published = {}
    while pending:
        ready = [u for u in pending if all(k in ids for refs in u["relations_by_key"].values() for k in refs)]
        if not ready:
            raise ValueError("Cyclic/unresolved teacher relations")
        for unit in ready:
            role = (
                "practice_support"
                if unit.get("integration_source") == "practice_support"
                else (
                    "practice"
                    if unit["kind"] in {"question", "hint"}
                    else (
                        "support"
                        if unit.get("integration_source") == "support"
                        else "supplement" if unit["key"] in config["primary_missing_unit_keys"] else "primary"
                    )
                )
            )
            refs, witness = resolve_source(unit["reviewed_content"], windows[role])
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
                        "source_refs": refs,
                        "activity_refs": [a["id"] for a in activities.values()],
                        "relations": {
                            k: [ids[x] for x in values] for k, values in unit["relations_by_key"].items()
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
            published[created["id"]] = unit
            witnesses[unit["key"]] = {
                **witness,
                "source_role": role,
                "filename": documents[role]["filename"],
                "unit_id": created["id"],
                "source_refs": refs,
                "human_review": "pending; technical test publication only",
            }
            pending.remove(unit)
    for activity in activities.values():
        checked(client.post(f"/api/v1/governance/activities/{activity['id']}/activate"))
    return {
        "course": course,
        "activities": activities,
        "documents": documents,
        "units": ids,
        "published": published,
        "witnesses": witnesses,
        "topics": topics,
        "recipient": recipient,
        "stream": stream,
        "domain": domain,
        "original_units": 70,
        "technical_units": len(pack["units"]),
        "human_review": "pending",
    }


def start_package_session(client, prepared, mode):
    return checked(
        client.post(
            "/api/v1/sessions",
            json={
                "participant_code": prepared["recipient"],
                "activity_configuration_id": prepared["activities"][mode]["id"],
            },
        ),
        201,
    )
