"""Explicit technical publication with real DB UUIDs and strict textual witnesses."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.package_fixture import (
    ensure_owned_temporary,
    prepare_package,
    resolve_source,
    start_package_session,
)


def test_missing_witness_never_uses_first_fragment():
    with pytest.raises(ValueError, match="literal"):
        resolve_source("Contenido que no existe", [("otro texto", [{"id": "not-a-real-id"}])])


def test_technical_publication_requires_explicit_owned_client():
    with pytest.raises(ValueError, match="Explicit"):
        ensure_owned_temporary(object(), False)


@pytest.mark.skipif(not os.environ.get("ORALIA_PACKAGE_BINDING"), reason="explicit proposed-package binding")
@pytest.mark.parametrize("stream", ["agua-docx", "programa-docx", "programa-pptx", "datos-pdf"])
def test_real_package_bindings(app_client, stream):
    prepared = prepare_package(app_client, stream, technical_publish=True, policy_version=3)
    assert len(prepared["units"]) == (86 if prepared["domain"] == "programa" else 85)
    assert all(
        w["source_role"] in {"practice", "practice_support"}
        for key, w in prepared["witnesses"].items()
        if "-question" in key or "-hint-" in key
    )
    out = Path(os.environ["ORALIA_PACKAGE_BINDING"])
    out.mkdir(parents=True, exist_ok=True)
    target = out / (stream + ".json")
    assert not target.exists()
    target.write_text(
        json.dumps({k: v for k, v in prepared.items() if k != "published"}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    primary = prepared["documents"]["primary"]
    course = prepared["course"]["id"]
    activity = prepared["activities"]["self_study"]["id"]

    def query(course_id):
        response = app_client.post(
            "/api/v1/materials/query",
            json={
                "query_text": "contenido de la actividad",
                "course_id": course_id,
                "activity_configuration_id": activity,
                "max_fragments": 50,
                "time_budget_ms": 5000,
            },
        )
        assert response.status_code == 200, response.text
        return response.json()["fragments"]

    assert query(course)
    other = app_client.post(
        "/api/v1/governance/courses",
        json={
            "name": "Otro curso temporal",
            "subject_code": "package-negative",
        },
    )
    assert other.status_code == 201
    assert not query(other.json()["id"])
    session = start_package_session(app_client, prepared, "self_study")
    sid = session["session_id"]
    topic = {"agua": "evaporacion", "programa": "validacion", "datos": "media"}[prepared["domain"]]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    first = app_client.post(endpoint, json={"text": f"¿Qué significa {topic}?"}).json()
    assert first["dialogue_status"]["rendered_unit_ids"]
    config = json.loads(
        (Path("materiales/docente/integracion-controlada-20261020-v3") / "revision.json").read_text(
            encoding="utf-8"
        )
    )
    original_file = Path(config["streams"][stream]["primary"])
    try:
        successor = app_client.post(
            f"/api/v1/materials/documents/{primary['id']}/versions",
            files={"file": (original_file.name, original_file.read_bytes())},
        )
        assert successor.status_code == 201, successor.text
        second = successor.json()
        assert second["version"] == 2 and second["family_id"] == primary["family_id"]
        assert all(f["document_id"] != primary["id"] for f in query(course))
        assert app_client.post(f"/api/v1/materials/documents/{second['id']}/activate").status_code == 200
        response = app_client.post(endpoint, json={"text": "Repítelo exactamente"})
        assert response.status_code == 200
        assert not response.json()["dialogue_status"]["rendered_unit_ids"]
        assert not response.json()["sources"]
        cycle = {
            "first": primary,
            "successor": second,
            "cross_course_fragments": 0,
            "stale_repeat": response.json(),
            "original_retired_and_not_emitted": True,
        }
        (out / (stream + "-lifecycle.json")).write_text(
            json.dumps(cycle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    finally:
        app_client.post(
            f"/api/v1/governance/sessions/{sid}/close", json={"confirm": True, "reason": "abandoned"}
        )
