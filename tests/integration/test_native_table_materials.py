"""Real ingestion/index/query of native tables with existing authorization lifecycle."""

import pytest

from oralia.infrastructure.db import models
from tests.table_fixtures import NOTE, make_docx, make_pptx

MIMES = {
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}


@pytest.mark.parametrize("kind", ["docx", "pptx"])
def test_native_table_keeps_provenance_activation_scope_and_retirement(
    app_client, seeded_course, tmp_path, kind
):
    path = (make_docx if kind == "docx" else make_pptx)(tmp_path / f"table.{kind}")
    response = app_client.post(
        "/api/v1/materials/documents",
        data={"course_id": seeded_course, "activity_configuration_ids": ["table-authorized"]},
        files={"file": (path.name, path.read_bytes(), MIMES[kind])},
    )
    assert response.status_code == 201, response.text
    first = response.json()
    assert first["status"] == "processed"

    def query(activity="table-authorized", course=None):
        r = app_client.post(
            "/api/v1/materials/query",
            json={
                "query_text": "cantidad 007 formato siete válido",
                "course_id": course or seeded_course,
                "activity_configuration_id": activity,
                "max_fragments": 50,
                "time_budget_ms": 5000,
            },
        )
        assert r.status_code == 200, r.text
        return r.json()["fragments"]

    assert not query(), "Processing must not authorize activation"
    assert app_client.post(f"/api/v1/materials/documents/{first['id']}/activate").status_code == 200
    fragments = query()
    assert fragments
    cells = [f for f in fragments if "tabla 1" in f["location_ref"]]
    assert any("007" in f["text"] and "fila 2" in f["location_ref"] for f in cells)
    assert all(f["document_id"] == first["id"] and f["document_version"] == 1 for f in fragments)
    assert NOTE not in "\n".join(f["text"] for f in fragments)
    assert not query("another-activity")
    other = app_client.post(
        "/api/v1/governance/courses", json={"name": "Curso ficticio externo", "subject_code": "tables-other"}
    )
    assert other.status_code == 201, other.text
    assert not query(course=other.json()["id"])
    with app_client.__db_sessionmaker__() as db:
        stored = db.query(models.MaterialFragment).filter_by(document_id=first["id"]).all()
        old = [(f.id, f.text, f.location_ref) for f in stored]
        assert any("3,5" in f.text for f in stored)
    replacement = app_client.post(
        f"/api/v1/materials/documents/{first['id']}/versions",
        files={"file": (path.name, path.read_bytes(), MIMES[kind])},
    )
    assert replacement.status_code == 201, replacement.text
    second = replacement.json()
    assert second["version"] == 2 and second["family_id"] == first["family_id"]
    assert not query()
    assert app_client.post(f"/api/v1/materials/documents/{second['id']}/activate").status_code == 200
    assert all(f["document_id"] == second["id"] and f["document_version"] == 2 for f in query())
    with app_client.__db_sessionmaker__() as db:
        assert old == [
            (f.id, f.text, f.location_ref)
            for f in db.query(models.MaterialFragment).filter_by(document_id=first["id"]).all()
        ]
    assert app_client.post(f"/api/v1/materials/documents/{second['id']}/deactivate").status_code == 200
    assert not query()


def test_only_notes_and_excessive_structure_do_not_get_indexed(app_client, seeded_course, tmp_path):
    for path, status in [
        (make_pptx(tmp_path / "notes.pptx", notes_only=True), "not_processable"),
        (make_docx(tmp_path / "deep.docx", depth=4), "error"),
    ]:
        response = app_client.post(
            "/api/v1/materials/documents",
            data={"course_id": seeded_course},
            files={"file": (path.name, path.read_bytes(), MIMES[path.suffix[1:]])},
        )
        assert response.status_code == 201, response.text
        document = response.json()
        assert document["status"] == status
        with app_client.__db_sessionmaker__() as db:
            assert db.query(models.MaterialFragment).filter_by(document_id=document["id"]).count() == 0
