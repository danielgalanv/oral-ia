"""Every composed unit is cited; source quotes require their own disclosure rule."""

from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


def test_reviewed_content_does_not_grant_raw_material_disclosure(app_client):
    prepared = prepare_guided(app_client, material_disclosure=False)
    sid = prepared["session"]["session_id"]
    response = checked(
        app_client.post(
            f"/api/v1/sessions/{sid}/study-turns", json={"text": "¿A qué temperatura hierve el agua?"}
        )
    )
    assert response["output_text"] and response["dialogue_status"]["rendered_unit_ids"]
    assert response["sources"]
    assert all(not source["fragment_text"] and source["content_withheld"] for source in response["sources"])


def test_composition_sources_cover_every_selected_reviewed_unit(app_client):
    prepared = prepare_guided(app_client, domain="programa", study_mode="presentation_preparation")
    sid = prepared["session"]["session_id"]
    response = checked(
        app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": "¿Qué hace la entrada?"})
    )
    assert len(response["dialogue_status"]["rendered_unit_ids"]) == 3
    with app_client.__db_sessionmaker__() as db:
        refs = {
            ref["fragment_id"]
            for uid in response["dialogue_status"]["rendered_unit_ids"]
            for ref in db.get(models.TeachingUnit, uid).source_refs
        }
        expected = {
            (fragment.document_id, fragment.document_version, fragment.location_ref)
            for ref in refs
            if (fragment := db.get(models.MaterialFragment, ref)) is not None
        }
    actual = {
        (source["document_id"], source["document_version"], source["location_ref"])
        for source in response["sources"]
    }
    assert actual == expected
