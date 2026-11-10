"""Contract test for GroundingVerifierAgent's five verdicts — FR-023, FR-024."""

from __future__ import annotations

import uuid

import pytest

from oralia.domain.agents.agent_contract import AgentRequest, CancellationToken
from oralia.domain.agents.grounding_verifier_agent import GroundingVerifierAgent


def _request(proposal_text: str, evidence: list[dict], general_knowledge_allowed: bool = False):
    return AgentRequest(
        session_id=uuid.uuid4(),
        turn_id=uuid.uuid4(),
        input={
            "proposal_text": proposal_text,
            "evidence": evidence,
            "general_knowledge_allowed": general_knowledge_allowed,
        },
    )


@pytest.mark.contract
async def test_fundamentada_when_all_claims_supported():
    agent = GroundingVerifierAgent()
    evidence = [{"fragment_id": "f1", "text": "El sol es una estrella de tipo espectral G."}]
    result = await agent.execute(_request("El sol es una estrella.", evidence), CancellationToken())
    assert result.status == "ok"
    assert result.output["verdict"] == "fundamentada"
    assert result.output["unsupported_claims"] == []


@pytest.mark.contract
async def test_parcialmente_fundamentada_when_some_claims_unsupported():
    agent = GroundingVerifierAgent()
    evidence = [{"fragment_id": "f1", "text": "El sol es una estrella de tipo espectral G."}]
    result = await agent.execute(
        _request("El sol es una estrella. Marte tiene dos lunas pequenas.", evidence), CancellationToken()
    )
    assert result.output["verdict"] == "parcialmente_fundamentada"
    assert result.output["supported_claims"]
    assert result.output["unsupported_claims"]


@pytest.mark.contract
async def test_no_fundamentada_when_no_claims_supported():
    agent = GroundingVerifierAgent()
    evidence = [{"fragment_id": "f1", "text": "El sol es una estrella de tipo espectral G."}]
    result = await agent.execute(
        _request("Los pinguinos viven en la Antartida sin problemas.", evidence), CancellationToken()
    )
    assert result.output["verdict"] == "no_fundamentada"


@pytest.mark.contract
async def test_no_verificable_when_no_claims_and_no_evidence():
    agent = GroundingVerifierAgent()
    result = await agent.execute(_request("", []), CancellationToken())
    assert result.output["verdict"] == "no_verificable"


@pytest.mark.contract
async def test_no_fundamentada_never_when_evidence_empty_and_claims_never_fundamentada():
    """FR-024: evidence vacio + general_knowledge_allowed=False MUST NOT yield 'fundamentada'."""
    agent = GroundingVerifierAgent()
    result = await agent.execute(
        _request("Alguna afirmacion cualquiera sin respaldo.", [], general_knowledge_allowed=False),
        CancellationToken(),
    )
    assert result.output["verdict"] in ("no_fundamentada", "no_verificable")
    assert result.output["verdict"] != "fundamentada"


# H03 acceptance matrix (research.md §11, estabilización 2026-09-10/11/12). Every case
# asserts the CORRECT required behavior per FR-023 — invoked against the real
# GroundingVerifierAgent.execute() (its actual AgentRequest/AgentResult contract), never
# a copy of its internal logic. A case marked "no_fundamentada" MUST assert exactly
# that; this is simultaneously the reproduction for 002/T089 (fails against the
# unreinforced agent) and the acceptance check for 002/T084 once corrected — same file,
# same assertions before and after.
_H03_SINGLE_VERDICT_MATRIX = [
    ("S1", "El agua hierve a 100 grados.", "El agua hierve a 100 grados.", "fundamentada"),
    ("C1", "El agua hierve a 20 grados.", "El agua hierve a 100 grados.", "no_fundamentada"),
    ("C2", "La sesión dura 45 minutos.", "La sesión dura 90 minutos.", "no_fundamentada"),
    ("C3", "El agua no hierve a 100 grados.", "El agua hierve a 100 grados.", "no_fundamentada"),
    (
        "I1",
        "El proceso es reversible en condiciones estándar.",
        "El proceso es reversible en condiciones estándar de laboratorio.",
        "fundamentada",
    ),
    ("V1", "El agua hierve a 99 grados.", "El agua hierve a 100 grados.", "no_fundamentada"),
    ("V2", "El agua hierve a noventa y nueve grados.", "El agua hierve a 100 grados.", "no_fundamentada"),
    ("CIEN", "El agua hierve a cien grados.", "El agua hierve a 100 grados.", "fundamentada"),
    ("NEG1", "El proceso es reversible.", "El proceso no es reversible.", "no_fundamentada"),
    ("NEG2", "El proceso no es reversible.", "El proceso no es reversible.", "fundamentada"),
    (
        "MULTI",
        "A dura 100 minutos.",
        "A dura 20 minutos y B dura 100 minutos.",
        "no_fundamentada",
    ),
    ("UNIT", "El objeto dura 20 minutos.", "El objeto dura 20 kilómetros.", "no_fundamentada"),
    # Seguimiento H03 (ronda 2026-09-12b) — falsos positivos/negativos F1-F4/F7
    # confirmados por revisión independiente sobre el código de la ronda anterior.
    ("F1", "Una sesión dura 20 minutos.", "Una sesión dura 100 minutos.", "no_fundamentada"),
    ("F2", "El proceso dura 20 minutos.", "El proceso dura varios minutos.", "no_fundamentada"),
    (
        "F3",
        "La temperatura aumenta de 20 a 100 grados.",
        "La temperatura aumenta de 20 a 30 grados.",
        "no_fundamentada",
    ),
    (
        "F4",
        "La sesión dura noventa y nueve minutos.",
        "La sesión dura noventa y nueve minutos.",
        "fundamentada",
    ),
    ("F7", "La temperatura es 20 grados.", "La temperatura es -20 grados.", "no_fundamentada"),
    # Propiedades/contrastes adicionales (§3 de esta ronda)
    (
        "PROP-SECOND-VALUE-OK",
        "La temperatura aumenta de 20 a 100 grados.",
        "La temperatura aumenta de 20 a 100 grados.",
        "fundamentada",
    ),
    (
        "PROP-SAME-NEG-MAGNITUDE",
        "La temperatura es -20 grados.",
        "La temperatura es -20 grados.",
        "fundamentada",
    ),
    # Seguimiento H03 (ronda 2026-09-12c) — R1-R3, defectos estructurales
    # reproducidos por revisión independiente sobre el código de T093.
    (
        "R1",
        "La temperatura aumenta de 100 a 20 grados.",
        "La temperatura aumenta de 20 a 100 grados.",
        "no_fundamentada",
    ),
    # R2/R3: corregidos en la ronda 2026-09-12d (§1) — la propuesta usa una expresión
    # numérica fuera del alcance del analizador ("mil"/"ciento") y su texto NO
    # coincide literalmente con la evidencia ("cien"/"veinte" son palabras distintas):
    # el mecanismo no puede interpretar el valor propio ni confirmar que la evidencia
    # lo respalda, pero tampoco tiene una diferencia interpretada que declarar como
    # contradicción activa — `no_verificable` es más preciso que `no_fundamentada`
    # aquí (nunca `fundamentada`, ver INCOMPLETE-MIL-IDENTICAL/INCOMPLETE-FRACTION/
    # INCOMPLETE-SCIENTIFIC más abajo para el caso de coincidencia literal).
    ("R2", "La sesión dura mil minutos.", "La sesión dura cien minutos.", "no_verificable"),
    (
        "R3",
        "La sesión dura ciento veinte minutos.",
        "La sesión dura veinte minutos.",
        "no_verificable",
    ),
    # Contrastes de relación origen/destino (§2 de esta ronda)
    (
        "REL-IDENTICAL",
        "La temperatura aumenta de 20 a 100 grados.",
        "La temperatura aumenta de 20 a 100 grados.",
        "fundamentada",
    ),
    (
        "REL-ONE-END-CHANGES",
        "La temperatura aumenta de 20 a 100 grados.",
        "La temperatura aumenta de 20 a 30 grados.",
        "no_fundamentada",
    ),
    (
        "REL-SIMPLE-PARTIAL",
        "La temperatura alcanza 100 grados.",
        "La temperatura aumenta de 20 a 100 grados.",
        "fundamentada",
    ),
    # Corrección semántica (ronda 2026-09-12d, §1 y §2): una coincidencia literal
    # normalizada de la afirmación completa con su cláusula de evidencia SÍ
    # constituye respaldo documental, aunque el formato numérico quede fuera del
    # analizador — la incapacidad de interpretar el valor no permite afirmar que la
    # evidencia no lo respalda cuando el texto es, salvo espacios/puntuación, el
    # mismo. Decisión anterior (T094, ronda 2026-09-12c) de exigir siempre
    # `no_fundamentada` para estos tres casos era incorrecta y se corrige aquí.
    (
        "INCOMPLETE-MIL-IDENTICAL",
        "La sesión dura mil minutos.",
        "La sesión dura mil minutos.",
        "fundamentada",
    ),
    (
        "INCOMPLETE-FRACTION",
        "La dosis es 1/2 miligramo.",
        "La dosis es 1/2 miligramo.",
        "fundamentada",
    ),
    (
        "INCOMPLETE-SCIENTIFIC",
        "La velocidad es 3e8 metros.",
        "La velocidad es 3e8 metros.",
        "fundamentada",
    ),
    # Contraste: un prefijo no reconocido antes de un numeral reconocido no deja
    # pasar el sufijo como si fuera toda la cantidad (§4, ronda 2026-09-12c). Verdicto
    # corregido a `no_verificable` en la ronda 2026-09-12d (§1, mismo razonamiento que
    # R2/R3: "doscientos veinte" no interpretado, texto distinto de "veinte").
    (
        "PREFIX-DOES-NOT-LEAK-SUFFIX",
        "La sesión dura doscientos veinte minutos.",
        "La sesión dura veinte minutos.",
        "no_verificable",
    ),
    # Nuevos contrastes (ronda 2026-09-12d, §2): la excepción de coincidencia literal
    # exige textos iguales salvo espacios/puntuación — nunca equivale números, signos,
    # unidades, negaciones o entidades distintas.
    (
        "INCOMPLETE-FRACTION-DIFFERENT-VALUE",
        "La dosis es 1/2 miligramo.",
        "La dosis es 1/3 miligramo.",
        "no_verificable",
    ),
    (
        "INCOMPLETE-SCIENTIFIC-DIFFERENT-VALUE",
        "La velocidad es 3e8 metros.",
        "La velocidad es 4e8 metros.",
        "no_verificable",
    ),
    (
        "INCOMPLETE-SIGN-DIFFERENT",
        "La velocidad es -3e8 metros.",
        "La velocidad es 3e8 metros.",
        "no_verificable",
    ),
    (
        "INCOMPLETE-UNIT-DIFFERENT",
        "La sesión dura mil minutos.",
        "La sesión dura mil kilómetros.",
        "no_verificable",
    ),
    (
        "INCOMPLETE-NEGATION-DIFFERENT",
        "La sesión dura mil minutos.",
        "La sesión no dura mil minutos.",
        "no_fundamentada",
    ),
    (
        "INCOMPLETE-WHITESPACE-PUNCTUATION-ONLY",
        "La sesión dura mil minutos.",
        "La sesión  dura mil minutos",
        "fundamentada",
    ),
    (
        "INCOMPLETE-SAME-FIGURE-DIFFERENT-ENTITY",
        "A dura mil minutos.",
        "A dura cien minutos. B dura mil minutos.",
        "no_verificable",
    ),
    # Seguimiento H03 (ronda 2026-09-12e, T096) — asimetría reproducida: T095 solo
    # analizaba el resultado numérico de la PROPUESTA; una propuesta PARSED_KIND
    # frente a una cláusula de evidencia INCOMPLETE_KIND caía en el caso F2
    # (`_CONTRADICTED_OUTCOME`) sin que la evidencia hubiera sido interpretada,
    # violando la regla ya declarada de que una contradicción activa exige AMBOS
    # valores interpretados. Cada par se prueba en los dos sentidos — el veredicto
    # (`no_verificable`) MUST ser el mismo independientemente de qué lado (propuesta o
    # evidencia) contenga el formato numérico no interpretado.
    (
        "T096-1000-VS-MIL",
        "La sesión dura 1000 minutos.",
        "La sesión dura mil minutos.",
        "no_verificable",
    ),
    (
        "T096-MIL-VS-1000",
        "La sesión dura mil minutos.",
        "La sesión dura 1000 minutos.",
        "no_verificable",
    ),
    (
        "T096-20-VS-MIL",
        "La sesión dura 20 minutos.",
        "La sesión dura mil minutos.",
        "no_verificable",
    ),
    (
        "T096-MIL-VS-20",
        "La sesión dura mil minutos.",
        "La sesión dura 20 minutos.",
        "no_verificable",
    ),
    (
        "T096-05-VS-FRACTION",
        "La dosis es 0.5 miligramos.",
        "La dosis es 1/2 miligramos.",
        "no_verificable",
    ),
    (
        "T096-FRACTION-VS-05",
        "La dosis es 1/2 miligramos.",
        "La dosis es 0.5 miligramos.",
        "no_verificable",
    ),
    (
        "T096-SCIENTIFIC-VS-FULL",
        "La velocidad es 3e8 metros.",
        "La velocidad es 300000000 metros.",
        "no_verificable",
    ),
    (
        "T096-FULL-VS-SCIENTIFIC",
        "La velocidad es 300000000 metros.",
        "La velocidad es 3e8 metros.",
        "no_verificable",
    ),
]

# Pares sin direccionalidad semántica (ronda 2026-09-12e, T096, §comprobación de
# simetría): intercambiar cuál de los dos textos se envía como propuesta y cuál como
# evidencia MUST NOT cambiar el veredicto agregado solo porque cambie qué lado
# contiene el formato numérico no interpretado (T096-*), un valor idéntico (S1-like),
# o una contradicción numérica simple (C1-like) — la relación de soporte/contradicción
# no depende de la dirección en la que se comparan dos afirmaciones equivalentes.
_H03_SYMMETRY_PAIRS = [
    ("T096-1000-MIL", "La sesión dura 1000 minutos.", "La sesión dura mil minutos."),
    ("T096-20-MIL", "La sesión dura 20 minutos.", "La sesión dura mil minutos."),
    ("T096-05-FRACTION", "La dosis es 0.5 miligramos.", "La dosis es 1/2 miligramos."),
    ("T096-SCIENTIFIC-FULL", "La velocidad es 3e8 metros.", "La velocidad es 300000000 metros."),
    ("IDENTICAL-DIGIT", "El agua hierve a 100 grados.", "El agua hierve a 100 grados."),
    ("SIMPLE-CONTRADICTION", "El agua hierve a 20 grados.", "El agua hierve a 100 grados."),
    ("IDENTICAL-INCOMPLETE", "La sesión dura mil minutos.", "La sesión dura mil minutos."),
]


@pytest.mark.contract
@pytest.mark.parametrize(
    "case_id,claim,evidence_text,expected_verdict",
    _H03_SINGLE_VERDICT_MATRIX,
    ids=[c[0] for c in _H03_SINGLE_VERDICT_MATRIX],
)
async def test_h03_matrix_single_claim_cases(case_id, claim, evidence_text, expected_verdict):
    agent = GroundingVerifierAgent()
    evidence = [{"fragment_id": "f1", "text": evidence_text}]
    result = await agent.execute(_request(claim, evidence), CancellationToken())
    got = result.output["verdict"]
    msg = f"{case_id}: expected {expected_verdict!r}, got {got!r} (claim={claim!r})"
    assert got == expected_verdict, msg


@pytest.mark.contract
@pytest.mark.parametrize(
    "case_id,text_a,text_b",
    _H03_SYMMETRY_PAIRS,
    ids=[c[0] for c in _H03_SYMMETRY_PAIRS],
)
async def test_h03_t096_symmetry_swapping_proposal_and_evidence_keeps_same_verdict(
    case_id, text_a, text_b
):
    """T096, seguimiento H03 (ronda 2026-09-12e): para un par de textos sin
    direccionalidad semántica, evaluar (A como propuesta, B como evidencia) y (B como
    propuesta, A como evidencia) MUST producir el mismo veredicto agregado — la
    dirección de la comparación no puede decidir si existe una contradicción
    (asimetría reproducida y corregida en T096)."""
    agent = GroundingVerifierAgent()
    result_ab = await agent.execute(
        _request(text_a, [{"fragment_id": "f1", "text": text_b}]), CancellationToken()
    )
    result_ba = await agent.execute(
        _request(text_b, [{"fragment_id": "f1", "text": text_a}]), CancellationToken()
    )
    verdict_ab = result_ab.output["verdict"]
    verdict_ba = result_ba.output["verdict"]
    msg = (
        f"{case_id}: swapping proposal/evidence changed the verdict "
        f"({text_a!r} as proposal -> {verdict_ab!r}; {text_b!r} as proposal -> {verdict_ba!r})"
    )
    assert verdict_ab == verdict_ba, msg


@pytest.mark.contract
async def test_h03_neg_unrelated_negation_does_not_invalidate_supported_claim():
    """§3: una negación en otra oración/concepto no debe invalidar automáticamente una
    afirmación respaldada distinta."""
    agent = GroundingVerifierAgent()
    evidence = [
        {
            "fragment_id": "f1",
            "text": "El proceso es reversible en laboratorio. Otro tema no relacionado no aplica aquí.",
        }
    ]
    claim = "El proceso es reversible. El experimento no funcionó ayer."
    result = await agent.execute(_request(claim, evidence), CancellationToken())
    assert result.output["verdict"] == "parcialmente_fundamentada"
    assert any("reversible" in c for c in result.output["supported_claims"])
    assert any("experimento" in c for c in result.output["unsupported_claims"])


@pytest.mark.contract
async def test_h03_f5_duplicate_identical_evidence_still_fundamentada():
    """F5: duplicar evidencia equivalente no debe cambiar el veredicto — un empate
    entre cláusulas idénticas MUST resolverse comprobando polaridad/valor en cada una,
    no devolviendo `False` solo por existir un empate."""
    agent = GroundingVerifierAgent()
    evidence = [
        {"fragment_id": "f1", "text": "El agua hierve a 100 grados."},
        {"fragment_id": "f2", "text": "El agua hierve a 100 grados."},
    ]
    result = await agent.execute(
        _request("El agua hierve a 100 grados.", evidence), CancellationToken()
    )
    assert result.output["verdict"] == "fundamentada"


@pytest.mark.contract
async def test_h03_f6_duplicate_evidence_does_not_skip_polarity_check():
    """F6: duplicar evidencia no debe saltarse la comprobación de polaridad — ambas
    cláusulas empatadas están, además, en polaridad opuesta a la propuesta."""
    agent = GroundingVerifierAgent()
    evidence = [
        {"fragment_id": "f1", "text": "El proceso es reversible."},
        {"fragment_id": "f2", "text": "El proceso es reversible."},
    ]
    result = await agent.execute(
        _request("El proceso no es reversible.", evidence), CancellationToken()
    )
    assert result.output["verdict"] == "no_fundamentada"


@pytest.mark.contract
async def test_h03_property_duplicate_and_reorder_evidence_same_verdict():
    """§3: duplicar evidencia idéntica, y reordenar esos fragmentos, no cambia el
    veredicto."""
    agent = GroundingVerifierAgent()
    frag_a = {"fragment_id": "f1", "text": "El agua hierve a 100 grados."}
    frag_b = {"fragment_id": "f2", "text": "El agua hierve a 100 grados."}
    claim = "El agua hierve a 100 grados."

    result_in_order = await agent.execute(_request(claim, [frag_a, frag_b]), CancellationToken())
    result_reordered = await agent.execute(_request(claim, [frag_b, frag_a]), CancellationToken())

    assert result_in_order.output["verdict"] == "fundamentada"
    assert result_reordered.output["verdict"] == result_in_order.output["verdict"]


@pytest.mark.contract
async def test_h03_property_partial_claim_lists_stay_coherent():
    """§3: una afirmación parcialmente respaldada conserva listas
    supported_claims/unsupported_claims coherentes (sin solapamiento entre ambas, cada
    afirmación del texto original aparece exactamente en una de las dos)."""
    agent = GroundingVerifierAgent()
    evidence = [{"fragment_id": "f1", "text": "El agua hierve a 100 grados."}]
    claim = "El agua hierve a 100 grados. El agua hierve a 20 grados."
    result = await agent.execute(_request(claim, evidence), CancellationToken())
    assert result.output["verdict"] == "parcialmente_fundamentada"
    supported = result.output["supported_claims"]
    unsupported = result.output["unsupported_claims"]
    assert set(supported).isdisjoint(unsupported)
    assert len(supported) + len(unsupported) == 2


@pytest.mark.contract
async def test_h03_i2_partial_separates_topic_from_unsupported_provenance():
    """§5 (I2 corregido): el contenido temático respaldado y la afirmación de
    procedencia sin respaldo deben separarse en supported_claims/unsupported_claims,
    con veredicto parcial — no 'fundamentada' completa."""
    agent = GroundingVerifierAgent()
    evidence = [
        {"fragment_id": "f1", "text": "El calentamiento global aumenta la temperatura media del planeta."}
    ]
    claim = "El calentamiento global aumenta la temperatura media, como se explica en la página 12."
    result = await agent.execute(_request(claim, evidence), CancellationToken())
    assert result.output["verdict"] == "parcialmente_fundamentada"
    assert any("calentamiento" in c and "temperatura" in c for c in result.output["supported_claims"])
    assert any("página" in c for c in result.output["unsupported_claims"])
