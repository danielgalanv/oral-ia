"""Integration test (consumer-side, Feature 003) — H03, §7: a controlled proposal that
contradicts the retrieved evidence MUST NOT reach the participant as a grounded answer.

Uses the real `GroundingVerifierAgent` and the real `self_study_agency_composer.py`
orchestration (no production code modified) — only the material-retrieval step and the
generation adapter are replaced with doubles, exactly to control the evidence and the
proposal, per this round's authorization. The verifier's verdict is never mocked.
"""

from __future__ import annotations

import pytest

from oralia.application.orchestration import self_study_agency_composer
from oralia.domain.agents.agent_contract import AgentResult
from oralia.infrastructure.generation import deterministic_adapter
from oralia.infrastructure.generation.generation_port import GenerationOutcome
from tests.integration.test_mode_doubt_resolution import _authorize_catalogued_self_study_outputs


class _FixedEvidenceRetriever:
    """Controls only the retrieved evidence (research.md §11 H03 test scenario) — the
    real GroundingVerifierAgent then evaluates a real (contradicting) proposal against
    it, nothing about verification is replaced."""

    contract = self_study_agency_composer.MaterialRetrieverAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "fragments": [
                    {
                        "fragment_id": "f-h03-evidence",
                        "document_id": "d-h03",
                        "document_version": 1,
                        "location_ref": "p1",
                        "text": "El agua hierve a 100 grados.",
                        "relevance_score": 0.95,
                    }
                ],
                "index_version": "1",
                "warnings": [],
                "conflicts": [],
            },
            confidence=None,
            trace={"index_version": "1", "fragment_count": 1},
        )


@pytest.fixture()
def controlled_contradicting_proposal(monkeypatch):
    """Only the deterministic reserve adapter is patched (Ollama is never configured in
    tests, per research.md §1 — `ResponseGeneratorAgent` already falls back to it) so
    the generator's proposal is a fixed, controlled, evidence-contradicting sentence."""

    async def _generate(self, request):
        return GenerationOutcome(
            ok=True,
            text="El agua hierve a 20 grados.",
            internal_expected_answer=None,
            adapter="deterministic",
            model=None,
            parameters={},
            latency_ms=0,
        )

    monkeypatch.setattr(deterministic_adapter.DeterministicGenerationAdapter, "generate", _generate)
    monkeypatch.setattr(
        self_study_agency_composer, "MaterialRetrieverAgent", lambda db: _FixedEvidenceRetriever()
    )


@pytest.mark.integration
def test_contradicting_proposal_never_reaches_participant_as_grounded(
    app_client, self_study_activity, controlled_contradicting_proposal
):
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )

    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-h03-001")

    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-h03-001", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    turn_r = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿A qué temperatura hierve el agua?"},
    )
    assert turn_r.status_code == 200
    body = turn_r.json()

    # The generator's controlled, contradicting claim ("20 grados") never reaches the
    # participant as if it were grounded in the (real, evidence-checked) materials.
    assert "20 grados" not in body["output_text"]
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body["sources"] == []

    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    combined_events = [e for e in trace["trace_events"] if e["event_type"] == "verification_combined"]
    assert len(combined_events) == 1
    assert combined_events[0]["payload"]["grounding_verdict"] == "no_fundamentada"


class _FixedEvidenceRetrieverR1:
    """R1 (seguimiento H03, ronda R1-R3): evidencia controlada con una relación
    origen/destino ("de 20 a 100 grados") — el defecto que esta ronda corrige es que
    la propuesta podía intercambiar origen y destino y seguir clasificándose como
    `fundamentada`, porque ambos números existían en algún punto de la evidencia sin
    que se comprobara su papel relacional."""

    contract = self_study_agency_composer.MaterialRetrieverAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "fragments": [
                    {
                        "fragment_id": "f-h03-r1-evidence",
                        "document_id": "d-h03-r1",
                        "document_version": 1,
                        "location_ref": "p1",
                        "text": "La temperatura aumenta de 20 a 100 grados.",
                        "relevance_score": 0.95,
                    }
                ],
                "index_version": "1",
                "warnings": [],
                "conflicts": [],
            },
            confidence=None,
            trace={"index_version": "1", "fragment_count": 1},
        )


@pytest.fixture()
def controlled_swapped_endpoints_proposal_r1(monkeypatch):
    async def _generate(self, request):
        return GenerationOutcome(
            ok=True,
            text="La temperatura aumenta de 100 a 20 grados.",
            internal_expected_answer=None,
            adapter="deterministic",
            model=None,
            parameters={},
            latency_ms=0,
        )

    monkeypatch.setattr(deterministic_adapter.DeterministicGenerationAdapter, "generate", _generate)
    monkeypatch.setattr(
        self_study_agency_composer, "MaterialRetrieverAgent", lambda db: _FixedEvidenceRetrieverR1()
    )


@pytest.mark.integration
def test_r1_swapped_origin_destination_never_reaches_participant_as_grounded(
    app_client, self_study_activity, controlled_swapped_endpoints_proposal_r1
):
    """§4 de esta ronda: al menos uno de los contraejemplos nuevos (R1) verificado
    también en integración, no solo en el contrato, usando el `GroundingVerifierAgent`
    real dentro de la orquestación real de autoestudio."""
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )

    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-h03-r1-001")

    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-h03-r1-001", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    turn_r = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Cómo cambia la temperatura?"},
    )
    assert turn_r.status_code == 200
    body = turn_r.json()

    assert "de 100 a 20 grados" not in body["output_text"]
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body["sources"] == []

    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    combined_events = [e for e in trace["trace_events"] if e["event_type"] == "verification_combined"]
    assert len(combined_events) == 1
    assert combined_events[0]["payload"]["grounding_verdict"] == "no_fundamentada"


class _FixedEvidenceRetrieverR2:
    """R2 (seguimiento H03, ronda 2026-09-12d): evidencia controlada con "cien" —
    distinto en texto de la propuesta ("mil"), ambos fuera del alcance del analizador
    salvo por coincidencia literal. Verifica que el veredicto agregado distinga
    `no_verificable` (el mecanismo no puede interpretar "mil" ni confirmar que "cien"
    lo contradice) de `no_fundamentada` (reservado para una diferencia activamente
    interpretada) — la corrección semántica de esta ronda, no solo en el contrato."""

    contract = self_study_agency_composer.MaterialRetrieverAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "fragments": [
                    {
                        "fragment_id": "f-h03-r2-evidence",
                        "document_id": "d-h03-r2",
                        "document_version": 1,
                        "location_ref": "p1",
                        "text": "La sesión dura cien minutos.",
                        "relevance_score": 0.95,
                    }
                ],
                "index_version": "1",
                "warnings": [],
                "conflicts": [],
            },
            confidence=None,
            trace={"index_version": "1", "fragment_count": 1},
        )


@pytest.fixture()
def controlled_unverifiable_numeral_proposal_r2(monkeypatch):
    async def _generate(self, request):
        return GenerationOutcome(
            ok=True,
            text="La sesión dura mil minutos.",
            internal_expected_answer=None,
            adapter="deterministic",
            model=None,
            parameters={},
            latency_ms=0,
        )

    monkeypatch.setattr(deterministic_adapter.DeterministicGenerationAdapter, "generate", _generate)
    monkeypatch.setattr(
        self_study_agency_composer, "MaterialRetrieverAgent", lambda db: _FixedEvidenceRetrieverR2()
    )


@pytest.mark.integration
def test_r2_unrecognized_numeral_never_reaches_participant_as_grounded(
    app_client, self_study_activity, controlled_unverifiable_numeral_proposal_r2
):
    """§5 de esta ronda: al menos una integración con autoestudio para R1 o R2 usando
    el verificador real — cubre R2, distinta de la ya existente para R1, y verifica
    explícitamente que el veredicto trazado es `no_verificable` (no `no_fundamentada`
    ni `fundamentada`), reflejando la corrección semántica de esta ronda de principio
    a fin, no solo en el contrato."""
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )

    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-h03-r2-001")

    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-h03-r2-001", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    turn_r = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Cuánto dura la sesión?"},
    )
    assert turn_r.status_code == 200
    body = turn_r.json()

    assert "mil minutos" not in body["output_text"]
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body["sources"] == []

    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    combined_events = [e for e in trace["trace_events"] if e["event_type"] == "verification_combined"]
    assert len(combined_events) == 1
    assert combined_events[0]["payload"]["grounding_verdict"] == "no_verificable"


class _FixedEvidenceRetrieverT096:
    """T096 (seguimiento H03, ronda 2026-09-12e): evidencia controlada con "mil"
    (INCOMPLETE_KIND) frente a una propuesta con el dígito "1000" (PARSED_KIND) — la
    dirección exacta que quedaba rota tras T095 (`_CONTRADICTED_OUTCOME` por defecto,
    sin haber interpretado el lado de la evidencia). Verifica que la corrección
    simétrica de T096 produce `no_verificable` también en esta dirección concreta,
    dentro de la orquestación real de autoestudio, no solo en el contrato."""

    contract = self_study_agency_composer.MaterialRetrieverAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "fragments": [
                    {
                        "fragment_id": "f-h03-t096-evidence",
                        "document_id": "d-h03-t096",
                        "document_version": 1,
                        "location_ref": "p1",
                        "text": "La sesión dura mil minutos.",
                        "relevance_score": 0.95,
                    }
                ],
                "index_version": "1",
                "warnings": [],
                "conflicts": [],
            },
            confidence=None,
            trace={"index_version": "1", "fragment_count": 1},
        )


@pytest.fixture()
def controlled_unverifiable_digit_vs_word_proposal_t096(monkeypatch):
    async def _generate(self, request):
        return GenerationOutcome(
            ok=True,
            text="La sesión dura 1000 minutos.",
            internal_expected_answer=None,
            adapter="deterministic",
            model=None,
            parameters={},
            latency_ms=0,
        )

    monkeypatch.setattr(deterministic_adapter.DeterministicGenerationAdapter, "generate", _generate)
    monkeypatch.setattr(
        self_study_agency_composer, "MaterialRetrieverAgent", lambda db: _FixedEvidenceRetrieverT096()
    )


@pytest.mark.integration
def test_t096_digit_proposal_vs_word_evidence_never_reaches_participant_as_grounded(
    app_client, self_study_activity, controlled_unverifiable_digit_vs_word_proposal_t096
):
    """Prueba de integración exigida por T096: la propuesta ("1000 minutos",
    PARSED_KIND) frente a la evidencia ("mil minutos", INCOMPLETE_KIND) — antes de
    T096 esta dirección concreta clasificaba `no_fundamentada` por defecto (caso F2
    aplicado incorrectamente a una evidencia INCOMPLETE_KIND); tras T096 clasifica
    `no_verificable`, con el mismo verificador real dentro de la orquestación real de
    autoestudio."""
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )

    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-h03-t096-001")

    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-h03-t096-001", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    turn_r = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Cuánto dura la sesión?"},
    )
    assert turn_r.status_code == 200
    body = turn_r.json()

    assert "1000 minutos" not in body["output_text"]
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body["sources"] == []

    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    combined_events = [e for e in trace["trace_events"] if e["event_type"] == "verification_combined"]
    assert len(combined_events) == 1
    assert combined_events[0]["payload"]["grounding_verdict"] == "no_verificable"


class _FixedEvidenceRetrieverF1:
    """F1 (seguimiento H03, ronda 2026-09-12b): evidencia controlada donde "una" es un
    artículo, no un valor — un caso que la primera ronda de H03 aprobaba
    incorrectamente (`fundamentada`) por confundir "una" con el número 1."""

    contract = self_study_agency_composer.MaterialRetrieverAgent.contract

    async def execute(self, request, cancellation):
        return AgentResult(
            status="ok",
            output={
                "fragments": [
                    {
                        "fragment_id": "f-h03-f1-evidence",
                        "document_id": "d-h03-f1",
                        "document_version": 1,
                        "location_ref": "p1",
                        "text": "Una sesión dura 100 minutos.",
                        "relevance_score": 0.95,
                    }
                ],
                "index_version": "1",
                "warnings": [],
                "conflicts": [],
            },
            confidence=None,
            trace={"index_version": "1", "fragment_count": 1},
        )


@pytest.fixture()
def controlled_contradicting_proposal_f1(monkeypatch):
    async def _generate(self, request):
        return GenerationOutcome(
            ok=True,
            text="Una sesión dura 20 minutos.",
            internal_expected_answer=None,
            adapter="deterministic",
            model=None,
            parameters={},
            latency_ms=0,
        )

    monkeypatch.setattr(deterministic_adapter.DeterministicGenerationAdapter, "generate", _generate)
    monkeypatch.setattr(
        self_study_agency_composer, "MaterialRetrieverAgent", lambda db: _FixedEvidenceRetrieverF1()
    )


@pytest.mark.integration
def test_f1_contradicting_duration_never_reaches_participant_as_grounded(
    app_client, self_study_activity, controlled_contradicting_proposal_f1
):
    """§4 de esta ronda: al menos uno de los contraejemplos nuevos que antes se
    aprobaba (F1) verificado también en integración, no solo en el contrato."""
    activity_id = self_study_activity["activity_id"]
    app_client.post(
        f"/api/v1/tecnica/activities/{activity_id}/self-study-config",
        json={
            "enabled_modes": ["doubt_resolution"],
            "summary_authorized": False,
            "practice_reveals_solution": False,
        },
    )

    _authorize_catalogued_self_study_outputs(app_client, activity_id, "est-h03-f1-001")

    session_r = app_client.post(
        "/api/v1/sessions",
        json={"participant_code": "est-h03-f1-001", "activity_configuration_id": activity_id},
    )
    session_id = session_r.json()["session_id"]

    turn_r = app_client.post(
        f"/api/v1/sessions/{session_id}/study-turns",
        json={"text": "¿Cuánto dura una sesión?"},
    )
    assert turn_r.status_code == 200
    body = turn_r.json()

    assert "20 minutos" not in body["output_text"]
    assert body["dialogue_action"] == "acknowledge_missing_info"
    assert body["sources"] == []

    trace = app_client.get(f"/api/v1/tecnica/sessions/{session_id}/study-trace").json()
    combined_events = [e for e in trace["trace_events"] if e["event_type"] == "verification_combined"]
    assert len(combined_events) == 1
    assert combined_events[0]["payload"]["grounding_verdict"] == "no_fundamentada"
