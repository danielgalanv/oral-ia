"""Pedagogical oracles are independent of output-publication approval."""

import json
import os
from pathlib import Path

import pytest

from tests.dialogue.api_fixture import prepare_guided


@pytest.mark.parametrize(
    "domain,prompt",
    [
        ("agua", "Explícame paso a paso la condensación"),
        ("programa", "¿Cómo valida el programa un registro?"),
    ],
)
def test_process_answers_are_spoken_steps(app_client, domain, prompt):
    prepared = prepare_guided(app_client, domain=domain, screenless=True, pedagogy=True)
    response = app_client.post(
        f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls", json={"text": prompt}
    )
    assert response.status_code == 200
    result = response.json()
    assert not result.get("blocked", False)
    # Publication can pass while the pedagogical requirement fails.
    text = result["output_text"].casefold()
    assert all(word in text for word in ["primero", "después", "por último"]), result


CASES = json.loads(
    (Path(__file__).parents[1] / "dialogue/fixtures/didactic-v1.json").read_text(encoding="utf-8")
)["cases"]


CASES += json.loads(
    (Path(__file__).parents[1] / "dialogue/fixtures/didactic-reserve2.json").read_text(encoding="utf-8")
)["cases"]
CASES += json.loads(
    (Path(__file__).parents[1] / "dialogue/fixtures/didactic-reserve3.json").read_text(encoding="utf-8")
)["cases"]
CASES += json.loads(
    (Path(__file__).parents[1] / "dialogue/fixtures/didactic-reserve4.json").read_text(encoding="utf-8")
)["cases"]
EXPECTED_TOPICS = {
    "PL01": [None, "evaporacion", "evaporacion", "evaporacion"],
    "PL02": ["condensacion"] * 3,
    "PL03": ["validacion"] * 3,
    "PL04": ["validacion"] * 3,
    "PK01": [None, "evaporacion", "evaporacion", "evaporacion"],
    "PK02": ["condensacion"] * 4,
    "PK03": ["validacion"] * 3,
    "PK04": ["validacion"] * 4,
    "PD01": [None, None, "ebullicion", "evaporacion", "evaporacion", "evaporacion", "evaporacion"],
    "PD02": ["condensacion"] * 3,
    "PD03": ["validacion"] * 3,
    "PD04": ["validacion"] * 2,
    "PH01": [None, "evaporacion", "evaporacion"],
    "PH02": ["condensacion"] * 3,
    "PH03": ["validacion"] * 3,
    "PH04": ["validacion"] * 3,
    "PJ01": [None, "evaporacion", "evaporacion", "evaporacion"],
    "PJ02": ["ebullicion", "evaporacion", "condensacion"],
    "PJ03": ["validacion"] * 3,
    "PJ04": ["validacion"] * 3,
}


@pytest.mark.skipif(
    not os.environ.get("ORALIA_DIDACTIC_RUN"), reason="explicit frozen pedagogical evaluation"
)
@pytest.mark.parametrize("case", CASES, ids=lambda c: c["case_id"])
def test_frozen_didactic_conversation(app_client, case):
    partition = os.environ.get("ORALIA_DIDACTIC_PARTITION", "development")
    exposed = partition == "exposed" and case["partition"] in {
        "development",
        "reserved",
        "reserved_cycle_2",
        "reserved_cycle_3",
    }
    if case["partition"] != partition and not exposed:
        pytest.skip("other partition; no silent reserve")
    folder = Path(os.environ["ORALIA_DIDACTIC_RUN"])
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (case["case_id"] + ".json")
    assert not target.exists()
    report = {
        "case": case,
        "observations": [],
        "human_review": "D01 prior version requires correction; new version unevaluated",
        "audio_real": False,
    }

    def save():
        target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    save()
    prepared = prepare_guided(app_client, domain=case["domain"], screenless=True, pedagogy=True)
    endpoint = f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls"
    previous = ""
    try:
        for text, criterion in zip(case["steps"], case["expected"], strict=True):
            response = app_client.post(endpoint, json={"text": text})
            result = response.json()
            report["observations"].append(
                {
                    "input": text,
                    "expected_criterion": criterion,
                    "http_status": response.status_code,
                    "response": result,
                }
            )
            save()
            assert response.status_code == 200
            output = result["output_text"]
            lower = output.casefold()
            assert not result.get("blocked", False)
            if criterion == "greeting":
                assert lower.startswith("hola.")
            elif criterion == "overview":
                assert "referencia" not in lower and "temas publicados" in lower
            elif criterion == "repeat":
                assert output == previous
            elif criterion.startswith("process"):
                assert all(word in lower for word in ["primero", "después", "por último"]), result
            elif criterion.startswith("possibility"):
                if case["domain"] == "agua":
                    assert lower.startswith("sí") and "evaporación" in lower and "ebullición" in lower
                else:
                    assert "no" in lower and "valid" in lower and "aceptado" in lower
            elif criterion == "conditions":
                assert "100" in lower and "presión" in lower
            elif criterion.startswith("cause"):
                assert any(word in lower for word in ["porque", "para evitar", "causa", "explica"]), result
            elif criterion == "definition":
                assert any(word in lower for word in ["se llama", "es el paso", "validación"])
            if criterion.endswith("alternative"):
                assert output != previous
            if criterion not in {"greeting", "overview", "repeat"}:
                # Actual publication verification is required in addition to the
                # independent request-specific assertions above.
                status = result["dialogue_status"]
                assert status["rendered_unit_ids"] and status["grounding_verdict"] == "fundamentada"
                assert status["coherence_verdict"] == "approved"
            expected_topic = EXPECTED_TOPICS[case["case_id"]][len(report["observations"]) - 1]
            if expected_topic and criterion != "repeat":
                from oralia.infrastructure.db import models

                refs = result["dialogue_status"]["rendered_unit_ids"]
                with app_client.__db_sessionmaker__() as db:
                    assert refs and {db.get(models.TeachingUnit, ref).topic_ref for ref in refs} == {
                        expected_topic
                    }
            previous = output
        report["outcome"] = "passed"
        save()
    except Exception as exc:
        report.update(outcome="failed", failure_type=type(exc).__name__)
        save()
        raise
    finally:
        app_client.post(endpoint, json={"text": "terminar la sesión"})
        app_client.post(endpoint, json={"text": "confirmo cerrar"})


@pytest.mark.parametrize(
    "text,purpose",
    [
        ("¿Cómo se llama ese cambio?", "definition"),
        ("No expliques cómo funciona; solo dime qué es la validación", "definition"),
        ("¿Por qué ocurre y cómo pasa?", "ambiguous"),
        ("¿Cómo funciona y por qué ocurre?", "ambiguous"),
    ],
)
def test_clause_request_does_not_use_isolated_como(text, purpose):
    from oralia.domain.dialogue.pedagogy import request_purpose

    assert request_purpose(text, {"validacion"}, "validacion").purpose == purpose


def test_missing_mechanism_is_a_limit_not_an_example(app_client):
    from oralia.infrastructure.db import models

    prepared = prepare_guided(app_client, screenless=True, pedagogy=True)
    with app_client.__db_sessionmaker__() as db:
        unit = db.get(models.TeachingUnit, prepared["units"]["agua-evaporacion-didactic-process"])
        unit.status = "retired"
        db.commit()
    response = app_client.post(
        f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls",
        json={"text": "¿Cómo pasa el agua líquida a vapor?"},
    )
    result = response.json()
    assert response.status_code == 200
    assert not result["dialogue_status"]["rendered_unit_ids"]
    assert "no está disponible" in result["output_text"]


def test_protected_defense_does_not_publish_study_mechanism(app_client):
    prepared = prepare_guided(app_client, mode="oral_defense", screenless=True, pedagogy=True)
    result = app_client.post(
        f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls",
        json={"text": "¿Cómo pasa el agua líquida a vapor?"},
    ).json()
    assert "moléculas" not in result["output_text"]
    assert result["dialogue_status"]["non_disclosure_verdict"] in {"approved", "not_applicable"}


def test_successor_policy_requires_complete_templates(app_client):
    def remove_greeting(policy):
        policy["allowed_templates"] = [
            entry for entry in policy["allowed_templates"] if entry[0] != "didactic-greeting"
        ]

    with pytest.raises(AssertionError, match="didáctica"):
        prepare_guided(app_client, screenless=True, pedagogy=True, policy_transform=remove_greeting)


def test_literal_repetition_preserves_multisentence_mechanism(app_client):
    prepared = prepare_guided(app_client, screenless=True, pedagogy=True)
    endpoint = f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls"
    first = app_client.post(endpoint, json={"text": "¿Cómo pasa el agua líquida a vapor?"}).json()
    second = app_client.post(endpoint, json={"text": "repite exactamente la última respuesta"}).json()
    assert "moléculas" in first["output_text"]
    assert second["output_text"] == first["output_text"]


def test_v1_material_stays_limited_and_does_not_claim_new_process(app_client):
    prepared = prepare_guided(app_client, screenless=True)
    response = app_client.post(
        f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls",
        json={"text": "Explícame paso a paso la condensación"},
    )
    text = response.json()["output_text"]
    assert "La condensación transforma" in text
    assert "Primero" not in text


@pytest.mark.parametrize(
    "domain,prompt",
    [
        ("agua", "Explícame paso a paso la condensación"),
        ("programa", "¿Cómo valida el programa un registro?"),
    ],
)
def test_repeated_doubt_changes_process_strategy_in_both_domains(app_client, domain, prompt):
    prepared = prepare_guided(app_client, domain=domain, screenless=True, pedagogy=True)
    endpoint = f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls"
    first = app_client.post(endpoint, json={"text": prompt}).json()
    second = app_client.post(endpoint, json={"text": "no lo entiendo"}).json()
    assert first["output_text"] != second["output_text"]
    assert all(
        word in second["output_text"].casefold() for word in ["primero", "después", "por último"]
    ), second


@pytest.mark.parametrize(
    "text,topic",
    [
        ("¿Cómo se llama la comprobación anterior al almacenamiento?", "validacion"),
        ("¿Por qué se condensa el vapor sobre un vaso frío?", "condensacion"),
        ("¿Cómo comprueba el programa un registro antes del almacenamiento?", "validacion"),
    ],
)
def test_request_object_precedes_its_relational_complement(text, topic):
    from oralia.domain.dialogue.pedagogy import request_purpose

    assert (
        request_purpose(
            text, {"validacion", "almacenamiento", "condensacion", "evaporacion"}, "evaporacion"
        ).topic
        == topic
    )


@pytest.mark.parametrize("domain", ["agua", "programa"])
def test_published_didactic_variants_do_not_conflict_with_each_other(domain):
    from oralia.domain.agents.coherence_verifier_agent import _detect_contradiction

    folder = Path(__file__).parents[2] / "materiales/docente/dialogue"
    units = json.loads((folder / f"{domain}-v2.json").read_text(encoding="utf-8"))["units"]
    variants = [u for u in units if "-didactic-" in u["key"]]
    failures = []
    for proposed in variants:
        for prior in variants:
            if proposed["topic_ref"] == prior["topic_ref"]:
                if _detect_contradiction(
                    proposed["reviewed_content"], [prior["reviewed_content"]], clause_polarity=True
                ):
                    failures.append((proposed["key"], prior["key"]))
    assert not failures, failures


def test_generic_topic_confirmation_uses_base_lesson_not_purpose_uuid_order(app_client):
    prepared = prepare_guided(app_client, screenless=True, pedagogy=True)
    endpoint = f"/api/v1/sessions/{prepared['session']['session_id']}/conversation-controls"
    app_client.post(endpoint, json={"text": "elijo evaporacion"})
    result = app_client.post(endpoint, json={"text": "confirmo"}).json()
    assert result["dialogue_status"]["rendered_unit_ids"] == [
        prepared["units"]["agua-evaporacion-explanation"]
    ]
