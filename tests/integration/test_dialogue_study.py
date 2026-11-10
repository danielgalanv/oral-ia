"""Complete public synthetic study sequence with the effective controlled provider."""

import pytest

from tests.dialogue.api_fixture import checked, prepare_guided


def test_observed_study_sequence_has_continuity_sources_and_executable_help(app_client):
    fixture = prepare_guided(app_client)
    sid = fixture["session"]["session_id"]
    results = []
    for text in [
        "hola",
        "dime que sabes sobre el agua?",
        "¿A qué temperatura hierve el agua?",
        "el agua puede pasar a ser vapor en algun momento?",
        "dimelo",
        "puedes repetir?",
        "dame un ejemplo",
    ]:
        result = checked(app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": text}))
        assert result["output_text"] and not result.get("blocked"), result
        assert result["dialogue_status"]["effective_profile"] == "guided_controlled"
        results.append(result)
    assert "100" in results[2]["output_text"]
    assert "evapor" in results[3]["output_text"].lower()
    assert results[5]["output_text"] == results[4]["output_text"]
    assert results[2]["sources"]
    assert results[6]["output_text"] != results[5]["output_text"]
    assert checked(app_client.post(f"/api/v1/sessions/{sid}/study-end"))["status"] == "closed_voluntary"


@pytest.mark.parametrize(
    "domain,question",
    [("agua", "¿A qué temperatura hierve el agua?"), ("programa", "¿Qué comprueba la validación?")],
)
@pytest.mark.parametrize(
    "mode_request,mode",
    [
        ("explicación guiada", "guided_explanation"),
        ("pregunta de práctica", "practice_questions"),
        ("preparar una exposición", "presentation_preparation"),
        ("repasar", "concept_review"),
        ("resolver una duda", "doubt_resolution"),
    ],
)
def test_five_effective_modes_across_two_domains(app_client, domain, question, mode_request, mode):
    fixture = prepare_guided(app_client, domain=domain)
    sid = fixture["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/study-turns"
    first = checked(app_client.post(endpoint, json={"text": question}))
    assert first["dialogue_status"]["rendered_unit_ids"], first
    result = checked(app_client.post(endpoint, json={"text": mode_request}))
    assert result["mode"] == mode
    assert result["dialogue_status"]["rendered_unit_ids"], result["dialogue_status"]
    assert result["output_text"] and not result.get("blocked")
    if mode in {"practice_questions", "concept_review"}:
        assert "¿" in result["output_text"]
    if mode == "presentation_preparation":
        assert len(result["dialogue_status"]["rendered_unit_ids"]) == 3
    if mode == "practice_questions":
        assert all(not source["fragment_text"] for source in result["sources"])
    checked(app_client.post(f"/api/v1/sessions/{sid}/study-end"))
