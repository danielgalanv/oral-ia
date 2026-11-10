"""Screen-hidden transcript checks; never evidence of real STT/TTS or human utility."""

import json
import os
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import pytest

from oralia.domain.dialogue.contracts import DialogueContext
from oralia.infrastructure.db import models
from oralia.infrastructure.db.timeutil import utcnow
from tests.dialogue.api_fixture import checked, prepare_guided


def test_orientation_says_current_options_without_a_screen(app_client):
    prepared = prepare_guided(app_client, screenless=True)
    sid = prepared["session"]["session_id"]
    result = checked(app_client.post(f"/api/v1/sessions/{sid}/study-turns", json={"text": "hola"}))
    assert "condensacion" in result["output_text"]
    assert "congelacion" in result["output_text"]
    assert "elijo" in result["output_text"]
    assert "repetir la pregunta" not in result["output_text"]


def test_v1_context_and_activity_do_not_silently_gain_navigation(app_client):
    assert "navigation_page" not in DialogueContext().model_dump()
    assert "navigation_page" in DialogueContext(schema_version=2).model_dump()
    prepared = prepare_guided(app_client)
    sid = prepared["session"]["session_id"]
    assert (
        app_client.post(f"/api/v1/sessions/{sid}/conversation-controls", json={"text": "hola"}).status_code
        == 409
    )
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).turn_count == 0


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_unknown_selection_and_ambiguous_confirmation_do_not_change_the_topic(app_client, mode):
    prepared = prepare_guided(app_client, screenless=True, mode=mode)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    for text in ["elijo condensacion", "elijo un tema inexistente", "confirmo"]:
        result = checked(app_client.post(endpoint, json={"text": text}))
        assert not result["dialogue_status"]["rendered_unit_ids"]
    checked(app_client.post(endpoint, json={"text": "elijo condensacion"}))
    result = checked(app_client.post(endpoint, json={"text": "confirmo algo distinto"}))
    assert "Se propone el tema condensacion" in result["output_text"]
    assert not result["dialogue_status"]["rendered_unit_ids"]
    result = checked(app_client.post(endpoint, json={"text": "confirmo"}))
    assert result["dialogue_status"]["rendered_unit_ids"]
    if mode == "oral_defense":
        result = checked(app_client.post(endpoint, json={"text": "quiero repasar conceptos"}))
        assert "Ese modo no está habilitado" in result["output_text"]
        result = checked(app_client.post(endpoint, json={"text": "qué modos hay"}))
        assert "no ofrece modos de autoestudio" in result["output_text"]


@pytest.mark.parametrize("domain,topic", [("agua", "evaporacion"), ("programa", "salida")])
def test_explicit_named_confirmation_keeps_existing_spoken_meaning(app_client, domain, topic):
    prepared = prepare_guided(app_client, domain=domain, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    checked(app_client.post(endpoint, json={"text": "cambiar de tema"}))
    result = checked(app_client.post(endpoint, json={"text": f"confirmo: {topic}"}))
    refs = result["dialogue_status"]["rendered_unit_ids"]
    assert refs
    with app_client.__db_sessionmaker__() as db:
        assert {db.get(models.TeachingUnit, ref).topic_ref for ref in refs} == {topic}


def test_unconfirmed_conservation_and_topic_choices_cannot_confirm_each_other(app_client):
    prepared = prepare_guided(app_client, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    for text in ["elijo condensacion", "conservar solo resumen", "confirmo"]:
        result = checked(app_client.post(endpoint, json={"text": text}))
        assert not result["dialogue_status"]["rendered_unit_ids"]
    assert "confirmo conservar solo resumen" in result["output_text"]
    assert not checked(app_client.get(f"/api/v1/sessions/{sid}/privacy"))["retain"]


def test_partial_navigation_permission_cannot_be_published(app_client):
    def revoke(policy):
        policy["allowed_disclosures"] = [
            r for r in policy["allowed_disclosures"] if r["category"] != "session_navigation"
        ]

    with pytest.raises(AssertionError, match="plantillas y permisos"):
        prepare_guided(app_client, screenless=True, policy_transform=revoke)


def test_options_repeat_selection_and_source_revocation_are_current(app_client):
    prepared = prepare_guided(app_client, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"

    def command(text):
        return checked(app_client.post(endpoint, json={"text": text}))

    first = command("qué temas hay")["output_text"]
    assert command("repite opciones")["output_text"] == first
    assert "evaporacion" in command("más opciones")["output_text"]
    proposed = command("elijo condensacion")
    assert "Se propone el tema condensacion" in proposed["output_text"]
    assert not proposed["dialogue_status"]["rendered_unit_ids"]
    chosen = command("confirmo")
    refs = chosen["dialogue_status"]["rendered_unit_ids"]
    assert refs
    assert "sección" in command("de dónde sale eso")["output_text"]
    assert "versión" in command("más sobre la fuente")["output_text"]
    for ref in refs:
        checked(app_client.post(f"/api/v1/governance/teaching-units/{ref}/retire"))
    assert "No hay una fuente vigente" in command("de dónde sale eso")["output_text"]


def test_navigation_metadata_passes_independent_disclosure_gate(app_client):
    prepared = prepare_guided(app_client, screenless=True, mode="oral_defense")
    sid = prepared["session"]["session_id"]
    # Fault injection into synthetic teacher metadata, not a production bypass.
    with app_client.__db_sessionmaker__() as db:
        for unit in db.query(models.TeachingUnit).filter_by(
            course_id=prepared["document"]["course_id"], topic_ref="ebullicion"
        ):
            unit.topic_ref = "100"
        db.commit()
    result = checked(app_client.post(f"/api/v1/sessions/{sid}/conversation-controls", json={"text": "hola"}))
    assert "100" not in result["output_text"]
    assert result["dialogue_status"]["non_disclosure_verdict"] == "block"
    second = checked(
        app_client.post(f"/api/v1/sessions/{sid}/conversation-controls", json={"text": "qué temas hay"})
    )
    assert second["output_text"] != result["output_text"]
    assert "100" not in second["output_text"]
    assert "terminar la sesión" in second["output_text"]


def test_failed_confirmation_rolls_back_preference_and_turn(app_client, monkeypatch):
    prepared = prepare_guided(app_client, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    checked(app_client.post(endpoint, json={"text": "conservar solo resumen"}))

    def reject(*args, **kwargs):
        raise ValueError("synthetic context conflict")

    monkeypatch.setattr("oralia.application.services.guided_dialogue_service.update_context", reject)
    assert app_client.post(endpoint, json={"text": "confirmo conservar solo resumen"}).status_code == 409
    assert not checked(app_client.get(f"/api/v1/sessions/{sid}/privacy"))["retain"]
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).turn_count == 1


def test_resource_close_does_not_confirm_a_pending_retention_choice(app_client):
    prepared = prepare_guided(app_client, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    checked(app_client.post(endpoint, json={"text": "conservar resumen y transcripción"}))
    with app_client.__db_sessionmaker__() as db:
        db.get(models.ActivityConfiguration, prepared["activity"]["id"]).max_turns = 2
        db.commit()
    result = checked(app_client.post(endpoint, json={"text": "sí"}))
    assert result["session_status"] == "closed_limit_reached"
    with app_client.__db_sessionmaker__() as db:
        assert db.query(models.ConsentRecord).filter_by(session_id=sid).count() == 0


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_all_material_revoked_still_allows_spoken_voluntary_close(app_client, mode):
    prepared = prepare_guided(app_client, screenless=True, mode=mode)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    checked(app_client.post(endpoint, json={"text": "elijo condensacion"}))
    checked(app_client.post(endpoint, json={"text": "confirmo"}))
    checked(app_client.post(f"/api/v1/materials/documents/{prepared['document']['id']}/deactivate"))
    reply = checked(app_client.post(endpoint, json={"text": "terminar"}))
    assert "confirmo cerrar" in reply["output_text"]
    reply = checked(app_client.post(endpoint, json={"text": "confirmo cerrar"}))
    assert reply["session_status"] == "closed_voluntary"


def test_expired_record_and_teacher_role_do_not_grant_owner_review(app_client):
    prepared = prepare_guided(app_client, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    for text in [
        "hola",
        "conservar resumen y transcripción",
        "confirmo conservar resumen y transcripción",
        "terminar",
        "confirmo cerrar",
    ]:
        checked(app_client.post(endpoint, json={"text": text}))
    assert (
        "Registro histórico propio"
        in checked(app_client.post(endpoint, json={"text": "revisar intervención uno"}))["output_text"]
    )
    with app_client.__db_sessionmaker__() as db:
        db.get(models.Session, sid).ended_at = utcnow() - timedelta(days=2)
        db.commit()
    assert (
        "No hay una transcripción"
        in checked(app_client.post(endpoint, json={"text": "revisar intervención uno"}))["output_text"]
    )
    app_client.cookies.clear()
    checked(app_client.post("/api/v1/auth/login", json={"secret": "fictional-installation-secret-005"}))
    assert app_client.post(endpoint, json={"text": "revisar intervención uno"}).status_code == 403


@pytest.mark.parametrize("mode", ["self_study", "oral_defense"])
def test_conservation_requires_exact_pending_choice_and_close_confirmation(app_client, mode):
    prepared = prepare_guided(app_client, mode=mode, screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"

    def command(text):
        return checked(app_client.post(endpoint, json={"text": text}))

    proposed = command("conservar solo resumen")
    assert "confirmo conservar solo resumen" in proposed["output_text"]
    command("sí")
    assert not checked(app_client.get(f"/api/v1/sessions/{sid}/privacy"))["retain"]
    command("confirmo conservar resumen y transcripción")
    assert not checked(app_client.get(f"/api/v1/sessions/{sid}/privacy"))["retain"]
    request_id = str(uuid4())
    payload = {"text": "confirmo conservar solo resumen", "client_request_id": request_id}
    one = checked(app_client.post(endpoint, json=payload))
    two = checked(app_client.post(endpoint, json=payload))
    assert one["turn_id"] == two["turn_id"]
    assert checked(app_client.get(f"/api/v1/sessions/{sid}/privacy"))["scope"] == ["summary"]
    closing = command("terminar la sesión")
    assert "confirmo cerrar" in closing["output_text"]
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "active"
    command("continuar sesión")
    command("confirmo cerrar")
    with app_client.__db_sessionmaker__() as db:
        assert db.get(models.Session, sid).status == "active"
    final = command("confirmo cerrar")
    assert final.get("session_status") == "closed_voluntary"
    assert "transcripción propia conservada" in command("revisar intervención uno")["output_text"]
    assert "no se puede deshacer" in command("eliminar mi contenido")["output_text"]
    assert not command("sí")["deleted"]
    assert command("confirmo eliminar el contenido de esta sesión")["deleted"]
    assert command("confirmo eliminar el contenido de esta sesión")["deleted"]
    with app_client.__db_sessionmaker__() as db:
        state = db.get(models.CognitiveState, sid)
        assert state is None or not state.dialogue_context
        assert db.query(models.ConsentRecord).filter_by(session_id=sid).count() == 0
    app_client.cookies.clear()
    assert app_client.post(endpoint, json={"text": "revisar intervención uno"}).status_code == 401


def run_screenless_case(client, case, on_step=None):
    prepared = prepare_guided(client, domain=case["domain"], mode=case["mode"], screenless=True)
    sid = prepared["session"]["session_id"]
    endpoint = f"/api/v1/sessions/{sid}/conversation-controls"
    records = []
    for step, text in enumerate(case["steps"]):
        result = checked(client.post(endpoint, json={"text": text}))
        assert result["output_text"], (case["case_id"], step, result)
        records.append({"step": step, "input": text, "response": result})
        if on_step:
            on_step(
                {
                    "case": case,
                    "observations": records,
                    "audio_real": False,
                    "human_review": "No evaluado",
                    "outcome": "in_progress",
                }
            )
        if step == 0:
            assert "elijo" in result["output_text"] and "repetir la pregunta" not in result["output_text"]
        if step == 4:
            assert result["dialogue_status"]["rendered_unit_ids"]
        if step == 5:
            assert (
                "sección" in result["output_text"] and prepared["document"]["id"] not in result["output_text"]
            )
        if step == 8:
            view = checked(client.get(f"/api/v1/sessions/{sid}/privacy"))
            assert view["retain"] == case["retain"]
        if step == 10:
            assert result.get("session_status") == "closed_voluntary"
        if step == 11:
            assert ("Registro histórico propio" in result["output_text"]) == case["retain"]
        if step == 13:
            assert "No hay una transcripción" in result["output_text"]
    return {"case": case, "observations": records, "audio_real": False, "human_review": "No evaluado"}


CORPUS = json.loads(
    (Path(__file__).parents[1] / "dialogue/fixtures/screenless-v1.json").read_text(encoding="utf-8")
)


@pytest.mark.skipif(
    not os.environ.get("ORALIA_SCREENLESS_RUN"), reason="explicit frozen navigation evaluation"
)
@pytest.mark.parametrize("case", CORPUS, ids=lambda case: case["case_id"])
def test_screenless_frozen_conversation(app_client, case):
    partition = os.environ.get("ORALIA_SCREENLESS_PARTITION", "development")
    if case["partition"] != partition:
        pytest.skip("other partition; never silently execute a reserve")
    folder = Path(os.environ["ORALIA_SCREENLESS_RUN"])
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (case["case_id"] + ".json")
    assert not target.exists(), "preserve each first run; use another result directory"

    def save(result):
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save({"case": case, "observations": [], "outcome": "setup_pending"})
    try:
        result = run_screenless_case(app_client, case, save)
        result["outcome"] = "passed"
        save(result)
    except Exception as exc:
        partial = json.loads(target.read_text(encoding="utf-8"))
        partial.update(outcome="failed", failure_type=type(exc).__name__)
        save(partial)
        raise
