"""GroundingVerifierAgent (Executable/AgentContract) — contracts/material-retriever-agent.md.

FR-023: classifies a proposal against retrieved evidence into one of five verdicts.
FR-023a: verdicts are per-call output only — this agent never persists or aggregates
them across a session/participant (callers MUST NOT build such aggregation either).
FR-024/FR-025: when evidence is empty, ``general_knowledge_allowed`` only changes
``no_fundamentada`` (general knowledge explicitly disabled) into ``no_verificable``
(might be coverable by general knowledge, but this agent has nothing to check it
against) — it never yields ``fundamentada`` on empty evidence. ``no_verificable`` is
also used, since the seguimiento H03 round of 2026-09-12d, for a claim whose numeric
expression the analyzer cannot interpret and whose text does not literally match its
aligned evidence clause — the mechanism genuinely cannot determine support or
contradiction in that case, which is a more precise fit than asserting ``no_fundamentada``
(an outcome reserved for an interpreted, active mismatch — see ``_claim_outcome``).
FR-030: independent from Feature 001's constitutional ``VerificationResult`` — this
module never reads or writes that table, and its verdict never substitutes for it.
"""

from __future__ import annotations

import re

from sqlalchemy.orm import Session as SASession

from oralia.domain.agents.agent import AgentContractSchema
from oralia.domain.agents.agent_contract import AgentRequest, AgentResult, CancellationToken
from oralia.infrastructure.db import models

CONTRACT = AgentContractSchema(
    agent_id="grounding-verifier",
    version="1.0.0",
    purpose="Clasificación de fundamentación de una propuesta frente a evidencia recuperada (FR-023)",
    input_schema_ref="contracts/material-retriever-agent.md#GroundingVerifierAgent.input",
    output_schema_ref="contracts/material-retriever-agent.md#GroundingVerifierAgent.output",
    timeout_ms=3000,
    confidence_semantics="no aplica — el veredicto en sí es la salida, no una probabilidad",
    success_criteria=["nunca clasifica como fundamentada una propuesta sin evidencia de respaldo"],
    trace_fields=["verdict"],
)

_MIN_SIGNIFICANT_WORD_LEN = 4
_SUPPORT_OVERLAP_THRESHOLD = 0.4
# FR-023/H03 (research.md §11, estabilización 2026-09-12): coincidencia exacta exigida
# para la comparación numérica — decidida de forma independiente de cualquier caso
# concreto de la matriz (no un margen ajustado a un ejemplo).
_NUMERIC_TOLERANCE = 0.0

# Negación simple, por presencia de marcador léxico — no interpretación semántica
# general (no distingue alcance sintáctico de la negación dentro de una oración
# compleja; ver límite documentado en research.md §11).
_NEGATION_MARKERS = {"no", "nunca", "tampoco", "jamás", "jamas"}

# Numerales cardinales españoles simples — cero..diez, decenas hasta noventa, y "cien"
# (no "ciento", que introduciría compuestos de centena fuera de este alcance). Permite
# combinar una decena + "y" + una unidad (1-9) en un numeral compuesto ("noventa y
# nueve" = 99) — no se generaliza a compuestos de centena/millar. "un"/"una" NO son
# valores independientes aquí (ver `_extract_value_mentions`, seguimiento H03 — "una" es
# gramaticalmente un artículo la mayoría de las veces, "una sesión" no es "el número
# uno"; tratarlo como valor independiente ocultaba la magnitud real que aparecía
# después en la misma cláusula, p. ej. "Una sesión dura 20 minutos").
_SIMPLE_NUMBER_WORDS = {
    "cero": 0,
    "uno": 1,
    "dos": 2,
    "tres": 3,
    "cuatro": 4,
    "cinco": 5,
    "seis": 6,
    "siete": 7,
    "ocho": 8,
    "nueve": 9,
    "diez": 10,
    "veinte": 20,
    "treinta": 30,
    "cuarenta": 40,
    "cincuenta": 50,
    "sesenta": 60,
    "setenta": 70,
    "ochenta": 80,
    "noventa": 90,
    "cien": 100,
}
_COMPOUND_TENS = {20, 30, 40, 50, 60, 70, 80, 90}
_TENS_WORDS = {"veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"}
_UNIT_DIGIT_WORDS = {"uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"}

# Unidades reconocidas para distinguir "mismo valor, magnitud distinta" (p. ej. 20
# minutos frente a 20 kilómetros) — lista acotada y explícita, no exhaustiva; una
# unidad fuera de esta lista simplemente no se compara (ver límite documentado).
_UNIT_WORDS = {
    "grado",
    "grados",
    "minuto",
    "minutos",
    "hora",
    "horas",
    "segundo",
    "segundos",
    "kilometro",
    "kilometros",
    "kilómetro",
    "kilómetros",
    "metro",
    "metros",
    "litro",
    "litros",
    "gramo",
    "gramos",
    "kilogramo",
    "kilogramos",
}

# Seguimiento H03 (ronda R1-R3, research.md §11): disparadores léxicos de "hay una
# expresión numérica aquí fuera del alcance de `_SIMPLE_NUMBER_WORDS`" —
# deliberadamente más amplios que esa tabla (centenas distintas de "cien",
# millares/millones). Encontrar cualquiera de estos en una cláusula marca TODA la
# cláusula como análisis "incompleto" (`INCOMPLETE_KIND`, ver `_analyze_numeric`):
# conservador, no se intenta rescatar el resto de valores de esa misma cláusula —
# "ciento veinte" no puede degradarse a "veinte" tomando solo la palabra reconocida.
_INCOMPLETE_NUMBER_TRIGGERS = {
    "mil",
    "millon",
    "millón",
    "millones",
    "ciento",
    "cientos",
    "doscientos",
    "trescientos",
    "cuatrocientos",
    "quinientos",
    "seiscientos",
    "setecientos",
    "ochocientos",
    "novecientos",
}
# Fracciones ("1/2") y notación científica ("3e8", "3x10^8") — reconocidas solo para
# marcar la cláusula como análisis incompleto (nunca como una lista de valores
# independientes; "1/2" MUST NOT interpretarse como "1" y "2" por separado).
_FRACTION_PATTERN = re.compile(r"\b\d+\s*/\s*\d+\b")
_SCIENTIFIC_PATTERN = re.compile(r"\b\d+(?:[.,]\d+)?\s*[eE][+-]?\d+\b|\b\d+\s*[x×]\s*10\s*\^?\s*\d+\b")

# Seguimiento H03 (ronda 2026-09-12d): puntuación considerada una diferencia
# puramente superficial para la coincidencia literal de una afirmación con
# `INCOMPLETE_KIND` (§1 de esta ronda) — deliberadamente NO incluye "-"/"+" (parte de
# un signo numérico, F7) ni "/" (parte de una fracción, distingue "1/2" de "1/3").
# Solo espacios y esta puntuación se consideran superficiales; números, signos,
# unidades, negaciones o palabras distintas MUST NOT volverse equivalentes por esta vía.
_LITERAL_PUNCTUATION_PATTERN = re.compile(r"[.,;:!¡?¿\"'()]")

# Marcadores de procedencia/atribución — acotan dónde se separa una afirmación de
# contenido de una afirmación de localización/fuente que la evidencia no respalda
# (FR-023, §5). Exige un sustantivo de referencia concreto tras el marcador (página,
# capítulo, sección...) — "según la página 12" se separa; un "según el documento"/
# "según la evidencia" genérico, sin una localización concreta que verificar, NO se
# separa (verificado: separarlo sin este requisito producía un falso positivo —
# "documento" es una palabra genérica que coincide por azar con casi cualquier
# evidencia, ver tests/integration/test_grounding_insufficient_evidence.py). Lista fija
# y explícita, no un analizador de referencias general.
_PROVENANCE_MARKERS = (
    r"(?:como se explica en|seg[uú]n|de acuerdo con)"
    r"\s+(?:la|el|los|las)?\s*(?:p[aá]gina|cap[ií]tulo|secci[oó]n|apartado|anexo|tabla|figura)\b"
)

# Conjunciones que separan cláusulas dentro de una misma oración — acotado a estas
# tres, suficiente para distinguir entidades distintas mencionadas en una misma
# oración (p. ej. "A dura 20 minutos y B dura 100 minutos"); no es un analizador
# sintáctico general. ";"/"pero" se dividen sin más comprobación; " y " NO se divide
# cuando forma parte de un numeral compuesto (decena + "y" + unidad, p. ej. "noventa y
# nueve") — dividir ciegamente ahí rompía ese numeral en dos cláusulas sin sentido
# numérico propio (seguimiento H03, caso F4).
_CLAUSE_SEPARATORS = r";|\s+pero\s+"


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p]


def _split_claims(text: str) -> list[str]:
    """Cada oración, y dentro de ella cada cláusula de procedencia/atribución
    (`_PROVENANCE_MARKERS`) como una afirmación separada — para que una localización
    sin respaldo (p. ej. "según la página 12") no arrastre a "fundamentada" el
    contenido temático que sí lo tiene, ni viceversa (FR-023, §5)."""
    out: list[str] = []
    for sentence in _split_sentences(text):
        pieces = re.split(rf",?\s*(?=\b{_PROVENANCE_MARKERS})", sentence, flags=re.I)
        out.extend(p.strip() for p in pieces if p.strip())
    return out


def _split_on_y(text: str) -> list[str]:
    """Divide por " y " salvo cuando el " y " concreto forma parte de un numeral
    compuesto (decena inmediatamente antes, unidad 1-9 inmediatamente después) —
    verificado palabra a palabra en cada punto de división candidato, no con una
    expresión regular de anchura variable (no soportada por `re`)."""
    tokens = re.split(r"(\s+y\s+)", text)
    result: list[str] = []
    buffer = tokens[0]
    i = 1
    while i < len(tokens):
        separator = tokens[i]
        following = tokens[i + 1] if i + 1 < len(tokens) else ""
        prev_words = re.findall(r"[a-záéíóúñü]+", buffer.lower())
        next_words = re.findall(r"[a-záéíóúñü]+", following.lower())
        prev_word = prev_words[-1] if prev_words else ""
        next_word = next_words[0] if next_words else ""
        is_compound_numeral = prev_word in _TENS_WORDS and next_word in _UNIT_DIGIT_WORDS
        # A single nominal object ("relaciona masa y volumen") is not a
        # second assertion. Numeric lists retain their existing comparison.
        is_nominal_object = (
            len(next_words) == 1
            and next_word in {"masa", "volumen", "formato", "rango", "cantidad", "versión", "version"}
            and next_word not in _SIMPLE_NUMBER_WORDS
            and next_word not in _INCOMPLETE_NUMBER_TRIGGERS
            and not re.search(r"\d", following)
            and next_word not in _NEGATION_MARKERS
        )
        is_coordinated_labels = bool(
            re.fullmatch(r"\s*[A-ZÁÉÍÓÚÑ]\s*", buffer) and re.match(r"[A-ZÁÉÍÓÚÑ]\b", following)
        )
        if is_compound_numeral or is_nominal_object or is_coordinated_labels:
            buffer = buffer + separator + following
        else:
            result.append(buffer)
            buffer = following
        i += 2
    result.append(buffer)
    return result


def _split_into_clauses(text: str) -> list[str]:
    """Cláusulas dentro de cada oración de la evidencia, separadas por conjunciones
    acotadas (`_CLAUSE_SEPARATORS`/`_split_on_y`) — permite alinear una afirmación de
    la propuesta con la cláusula de evidencia que realmente le corresponde, en vez de
    comparar contra todo el texto agregado (ver H03, comparación numérica
    multi-entidad), sin romper un numeral compuesto en el intento (seguimiento H03,
    caso F4)."""
    out: list[str] = []
    for sentence in _split_sentences(text):
        for rough_piece in re.split(_CLAUSE_SEPARATORS, sentence):
            out.extend(_split_on_y(rough_piece))
    return [p.strip() for p in out if p.strip()]


def _significant_words(text: str) -> set[str]:
    words = re.findall(r"[a-záéíóúñü]+", text.lower())
    return {w for w in words if len(w) >= _MIN_SIGNIFICANT_WORD_LEN}


def _entity_labels(text: str) -> set[str]:
    """Etiquetas de una sola letra mayúscula ("A", "B", ...) — el único caso en el que
    una entidad se nombra con menos de `_MIN_SIGNIFICANT_WORD_LEN` letras y por tanto
    quedaría invisible al solapamiento léxico ordinario; se usan solo para preferir la
    cláusula de evidencia que comparte la misma etiqueta al comparar valores (H03,
    caso multi-entidad) — no participan en el cálculo de solapamiento léxico general."""
    return set(re.findall(r"\b[A-ZÁÉÍÓÚÑ]\b", text))


def _is_negated(clause: str) -> bool:
    words = re.findall(r"[a-záéíóúñü]+", clause.lower())
    return any(w in _NEGATION_MARKERS for w in words)


def _normalize_literal(text: str) -> str:
    """Normaliza únicamente diferencias superficiales (mayúsculas, puntuación de
    `_LITERAL_PUNCTUATION_PATTERN`, espacios repetidos) — MUST NOT usarse para
    ninguna otra comparación que la coincidencia literal de `INCOMPLETE_KIND` (§1,
    seguimiento H03 2026-09-12d): no elimina dígitos, signos `+`/`-`, "/", ni
    ninguna letra — dos afirmaciones con números, signos, unidades, negaciones o
    palabras distintas MUST NOT normalizar al mismo valor."""
    stripped = _LITERAL_PUNCTUATION_PATTERN.sub("", text.lower())
    return re.sub(r"\s+", " ", stripped).strip()


def _tokenize_for_numbers(clause: str) -> list[str]:
    return re.findall(r"[a-záéíóúñü]+|[+-]?\d+(?:[.,]\d+)?", clause.lower())


def _extract_value_mentions(clause: str, tokens: list[str]) -> list[tuple[float, str | None, int]]:
    """Todos los valores numéricos de la cláusula, en orden, junto con la posición del
    token que ocupan — no solo el primero (una cláusula con más de un valor, p. ej.
    "de 20 a 100 grados", exige comparar cada uno; quedarse solo con el primero
    aprobaría cambios en los valores siguientes — seguimiento H03, caso F3). Cada
    valor es un dígito/decimal (el signo `-`/`+` inmediatamente adyacente forma parte
    del valor — F7), o un numeral cardinal simple o compuesto (`_SIMPLE_NUMBER_WORDS`,
    decena + "y" + unidad), junto con su unidad adyacente si pertenece a
    `_UNIT_WORDS`.

    "un"/"una" MUST NOT contar como valor por sí solos (son, la mayoría de las veces,
    el artículo indefinido — "una sesión" no afirma "el número uno"; seguimiento H03,
    caso F1) — solo cuentan cuando preceden inmediatamente a una unidad reconocida
    ("una hora" = 1 hora). La posición devuelta permite después (`_tag_roles`)
    reconocer el patrón relacional "de X a Y" sin perder cuál valor es cuál."""
    values: list[tuple[float, str | None, int]] = []
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        value: float | None = None
        consumed = 1
        if re.fullmatch(r"[+-]?\d+(?:[.,]\d+)?", tok):
            value = float(tok.replace(",", "."))
        elif tok in _SIMPLE_NUMBER_WORDS:
            value = float(_SIMPLE_NUMBER_WORDS[tok])
            if value in _COMPOUND_TENS and i + 2 < len(tokens) and tokens[i + 1] == "y":
                unit_word = tokens[i + 2]
                if unit_word in _SIMPLE_NUMBER_WORDS and _SIMPLE_NUMBER_WORDS[unit_word] < 10:
                    value += _SIMPLE_NUMBER_WORDS[unit_word]
                    consumed = 3
        elif tok in ("un", "una"):
            if i + 1 < len(tokens) and tokens[i + 1] in _UNIT_WORDS:
                value = 1.0
            else:
                i += 1
                continue
        if value is not None:
            unit = None
            next_idx = i + consumed
            if next_idx < len(tokens) and tokens[next_idx] in _UNIT_WORDS:
                unit = tokens[next_idx]
            values.append((value, unit, i))
            i += consumed
        else:
            i += 1
    return values


def _tag_roles(
    mentions: list[tuple[float, str | None, int]], tokens: list[str]
) -> list[tuple[float, str | None, str | None]]:
    """Etiqueta con `role` ("origin"/"destination") únicamente la pareja de valores que
    encaja en el patrón relacional "de VALOR ... a VALOR" — el resto queda con
    `role=None` (mención suelta, sin papel relacional declarado). Esto es lo que
    permite exigir después (`_values_are_consistent`) que el origen de la propuesta
    coincida con el origen de la evidencia y no con cualquier valor suelto —
    seguimiento H03, R1: "de 100 a 20" no puede confundirse con "de 20 a 100" solo
    porque ambos números existen en alguna parte de la evidencia."""
    tagged: list[tuple[float, str | None, str | None]] = [(v, u, None) for v, u, _pos in mentions]
    for idx_a, (v_a, u_a, pos_a) in enumerate(mentions):
        if pos_a == 0 or tokens[pos_a - 1] != "de":
            continue
        for idx_b in range(idx_a + 1, len(mentions)):
            v_b, u_b, pos_b = mentions[idx_b]
            if pos_b > 0 and tokens[pos_b - 1] == "a":
                tagged[idx_a] = (v_a, u_a, "origin")
                tagged[idx_b] = (v_b, u_b, "destination")
                break
        break
    return tagged


# Resultado del análisis numérico de una cláusula (§3, seguimiento H03 R1-R3) — una
# lista vacía por sí sola no distinguía "sin afirmación numérica" (no hay nada que
# contrastar, el resto de la cláusula puede aprobarse por solapamiento léxico) de
# "expresión numérica detectada pero fuera del alcance reconocido" (NO debe aprobarse
# recurriendo al solapamiento léxico restante — "mil"/"ciento veinte"/"1/2"/notación
# científica caían antes en esta segunda situación pero se trataban como la primera).
NONE_KIND = "none"
PARSED_KIND = "parsed"
INCOMPLETE_KIND = "incomplete"


def _analyze_numeric(clause: str) -> tuple[str, list[tuple[float, str | None, str | None]]]:
    """Clasifica la cláusula en una de tres categorías:

    - `NONE_KIND`: ninguna expresión numérica reconocible ni fuera de alcance — la
      cláusula simplemente no afirma ninguna cantidad propia.
    - `PARSED_KIND`: una o más expresiones numéricas dentro del alcance admitido
      (dígitos/decimales con signo, numerales simples y compuestos decena+unidad de
      `_SIMPLE_NUMBER_WORDS`), con su papel relacional ya etiquetado
      (`_tag_roles`) cuando corresponde.
    - `INCOMPLETE_KIND`: se detectó una expresión numérica fuera de este alcance
      (disparadores de `_INCOMPLETE_NUMBER_TRIGGERS`, fracciones `_FRACTION_PATTERN`,
      notación científica `_SCIENTIFIC_PATTERN`) — la cláusula entera se trata como no
      interpretada con seguridad, sin intentar rescatar valores parciales de ella
      (evita que "ciento veinte" se reduzca a "veinte", o que "1/2" se lea como dos
      números independientes)."""
    if _FRACTION_PATTERN.search(clause) or _SCIENTIFIC_PATTERN.search(clause):
        return (INCOMPLETE_KIND, [])
    words = re.findall(r"[a-záéíóúñü]+", clause.lower())
    if any(w in _INCOMPLETE_NUMBER_TRIGGERS for w in words):
        return (INCOMPLETE_KIND, [])
    tokens = _tokenize_for_numbers(clause)
    mentions = _extract_value_mentions(clause, tokens)
    if not mentions:
        return (NONE_KIND, [])
    return (PARSED_KIND, _tag_roles(mentions, tokens))


def _values_are_consistent(
    claim_values: list[tuple[float, str | None, str | None]],
    evidence_values: list[tuple[float, str | None, str | None]],
) -> bool:
    """Cada valor de `claim_values` MUST encontrar un valor equivalente (mismo número
    dentro de `_NUMERIC_TOLERANCE`, y unidad compatible cuando ambas declaran una) en
    `evidence_values` — no basta con que aparezca *alguno* de los valores de la
    propuesta; todos deben tener contrapartida (seguimiento H03, caso F3: "de 20 a
    100" frente a "de 20 a 30" — el 20 coincide, pero eso no basta si el 100 no
    coincide con nada).

    Cuando el valor de la propuesta tiene un papel relacional (`role` = "origin" o
    "destination", §2 de esta ronda), solo se compara contra valores de evidencia con
    ese MISMO papel — no contra cualquier valor de la lista. Esto es lo que impide
    certificar como fundamentada una propuesta con origen/destino intercambiados
    (R1): "100" como origen no encuentra contrapartida en un "100" que en la
    evidencia es destino, aunque el número exista en la evidencia. Un valor sin papel
    relacional (`role=None`, p. ej. una afirmación simple que menciona un único valor)
    sigue comparándose de forma permisiva contra cualquier valor de la evidencia, para
    no rechazar una afirmación parcial válida que no repite toda la relación
    (REL-SIMPLE-PARTIAL)."""
    for claim_num, claim_unit, claim_role in claim_values:
        if claim_role is not None:
            candidates = [(v, u) for v, u, r in evidence_values if r == claim_role]
            if not candidates:
                return False
        else:
            candidates = [(v, u) for v, u, _r in evidence_values]
        match = any(
            abs(claim_num - evidence_num) <= _NUMERIC_TOLERANCE
            and (not claim_unit or not evidence_unit or claim_unit == evidence_unit)
            for evidence_num, evidence_unit in candidates
        )
        if not match:
            return False
    return True


def _is_supported(claim: str, evidence_words: set[str]) -> bool:
    claim_words = _significant_words(claim)
    if not claim_words:
        return False
    overlap = claim_words & evidence_words
    return len(overlap) / len(claim_words) >= _SUPPORT_OVERLAP_THRESHOLD


def _best_aligned_clauses(claim: str, evidence_clauses: list[str]) -> list[str]:
    """La(s) cláusula(s) de evidencia con mayor solapamiento léxico con `claim` — si la
    propia `claim` referencia una etiqueta de entidad (`_entity_labels`), se restringe
    primero a las cláusulas que comparten esa etiqueta (H03, caso multi-entidad: sin
    esto, "A dura 100 minutos" empataría por igual con la cláusula de "A" y la de "B",
    ya que ambas comparten las mismas palabras significativas "dura"/"minutos")."""
    claim_words = _significant_words(claim)
    claim_labels = _entity_labels(claim)
    candidates = evidence_clauses
    if claim_labels:
        label_matches = [c for c in evidence_clauses if _entity_labels(c) & claim_labels]
        if label_matches:
            candidates = label_matches
    best_score = -1
    best: list[str] = []
    for clause in candidates:
        overlap = len(claim_words & _significant_words(clause))
        if overlap > best_score:
            best_score, best = overlap, [clause]
        elif overlap == best_score:
            best.append(clause)
    return best


# Resultado de comparar una afirmación con una cláusula de evidencia — sustituye el
# booleano anterior (seguimiento H03, ronda 2026-09-12d, §1). Distinguir
# `CONTRADICTED_OUTCOME` de `UNVERIFIABLE_OUTCOME` es lo que permite que el veredicto
# agregado (`GroundingVerifierAgent.execute`) elija entre `no_fundamentada` (una
# diferencia activamente interpretada: polaridad, o dos valores ambos comparables que
# no coinciden) y `no_verificable` (el mecanismo no puede interpretar la expresión de
# la propuesta con seguridad y su texto no coincide literalmente con la evidencia —
# no hay base para afirmar que la evidencia NO la respalda, solo que este mecanismo no
# puede confirmarlo). Ningún consumidor externo observa estos tres valores
# directamente — `supported_claims`/`unsupported_claims` (el contrato ya publicado)
# siguen siendo listas de texto sin cambios; ver `GroundingVerifierAgent.execute`.
_SUPPORTED_OUTCOME = "supported"
_CONTRADICTED_OUTCOME = "contradicted"
_UNVERIFIABLE_OUTCOME = "unverifiable"


def _claim_is_supported_by_clause(
    claim: str,
    clause: str,
    claim_kind: str,
    claim_values: list[tuple[float, str | None, str | None]],
) -> str:
    """Evalúa la afirmación contra una única cláusula de evidencia ya alineada —
    polaridad primero, después valor numérico. Devuelve uno de
    `_SUPPORTED_OUTCOME`/`_CONTRADICTED_OUTCOME`/`_UNVERIFIABLE_OUTCOME` (§1,
    seguimiento H03 2026-09-12d). Distingue, según el resultado de `_analyze_numeric`
    sobre la propia propuesta:

    (a) `NONE_KIND` → la afirmación no hace ninguna afirmación numérica propia, este
    paso no se aplica → `_SUPPORTED_OUTCOME`.

    (b) `PARSED_KIND` y la cláusula de evidencia alineada también analiza como
    `PARSED_KIND` → se comparan con `_values_are_consistent` (role-aware, §2 de la
    ronda anterior) → `_SUPPORTED_OUTCOME` si coinciden, `_CONTRADICTED_OUTCOME` si no
    (ambos valores fueron interpretados y difieren — una diferencia activa, no una
    incapacidad de interpretación).

    (c) `PARSED_KIND` en ambos lados pero los valores/roles/unidades no coinciden
    (`_values_are_consistent`) → `_CONTRADICTED_OUTCOME` — ambos valores fueron
    interpretados y difieren, una diferencia activa.

    (d) `PARSED_KIND` en la propuesta pero la cláusula de evidencia analiza
    `NONE_KIND` (sin valor reconocido en absoluto) → la cifra concreta de la
    propuesta no tiene con qué contrastarse con seguridad → `_CONTRADICTED_OUTCOME`
    (seguimiento H03, caso F2 — conservado sin cambio en la ronda 2026-09-12e/T096:
    `NONE_KIND` no es una expresión numérica no interpretada, es la ausencia de una;
    si el texto fuera idéntico, ambas cláusulas analizarían igual y esta rama no se
    alcanzaría, ver `_analyze_numeric`).

    (e) `INCOMPLETE_KIND` en **cualquiera** de los dos lados (propuesta o cláusula de
    evidencia alineada) — corregido en la ronda 2026-09-12e (T096, simetría): antes
    (T095) solo se miraba el resultado de la propuesta, así que "1000 minutos"
    (propuesta, `PARSED_KIND`) frente a "mil minutos" (evidencia, `INCOMPLETE_KIND`)
    caía en el caso (d) anterior y devolvía `_CONTRADICTED_OUTCOME` — violando la
    propia regla de que una contradicción activa exige **ambos** valores
    interpretados. Ahora, si cualquiera de los dos lados es `INCOMPLETE_KIND`: una
    coincidencia literal normalizada de la afirmación completa con la cláusula de
    evidencia (`_normalize_literal`, solo espacios y puntuación superficial) SÍ
    constituye respaldo documental → `_SUPPORTED_OUTCOME`; si los textos no
    coinciden, la incapacidad de interpretar al menos un lado no permite afirmar que
    hay contradicción → `_UNVERIFIABLE_OUTCOME` (nunca `_SUPPORTED_OUTCOME` por
    solapamiento léxico parcial, y nunca `_CONTRADICTED_OUTCOME` sin que ambos
    valores hayan podido interpretarse). Esta comprobación se hace ANTES de la
    distinción (c)/(d) — por eso `NONE_KIND` (ausencia real de expresión, sin nada
    que interpretar) y `INCOMPLETE_KIND` (expresión detectada pero no interpretada)
    siguen tratándose de forma distinta: solo el segundo activa esta rama."""
    if _is_negated(claim) != _is_negated(clause):
        return _CONTRADICTED_OUTCOME
    if claim_kind == NONE_KIND:
        return _SUPPORTED_OUTCOME
    evidence_kind, evidence_values = _analyze_numeric(clause)
    if claim_kind == INCOMPLETE_KIND or evidence_kind == INCOMPLETE_KIND:
        if _normalize_literal(claim) == _normalize_literal(clause):
            return _SUPPORTED_OUTCOME
        return _UNVERIFIABLE_OUTCOME
    # claim_kind == PARSED_KIND en este punto (NONE_KIND e INCOMPLETE_KIND ya
    # devueltos arriba); evidence_kind es PARSED_KIND o NONE_KIND.
    if evidence_kind != PARSED_KIND:
        return _CONTRADICTED_OUTCOME
    if _values_are_consistent(claim_values, evidence_values):
        return _SUPPORTED_OUTCOME
    return _CONTRADICTED_OUTCOME


def _combine_clause_outcomes(outcomes: list[str]) -> str:
    """Combina los resultados de todas las cláusulas de evidencia empatadas en
    alineamiento para una misma afirmación (seguimiento H03, casos F5/F6, conservado
    sin cambio de comportamiento — solo generalizado a tres valores): si **todas**
    coinciden (`_SUPPORTED_OUTCOME`), la afirmación está soportada; si **todas**
    son una contradicción activa (`_CONTRADICTED_OUTCOME`), es una contradicción; en
    cualquier otro caso (desacuerdo entre cláusulas, o alguna es
    `_UNVERIFIABLE_OUTCOME`) el resultado es genuinamente incierto → conservador,
    `_UNVERIFIABLE_OUTCOME` — nunca se aprueba ni se declara contradicha una
    afirmación cuyo alineamiento está en desacuerdo consigo mismo."""
    if all(o == _SUPPORTED_OUTCOME for o in outcomes):
        return _SUPPORTED_OUTCOME
    if all(o == _CONTRADICTED_OUTCOME for o in outcomes):
        return _CONTRADICTED_OUTCOME
    return _UNVERIFIABLE_OUTCOME


def _claim_outcome(claim: str, evidence_words: set[str], evidence_clauses: list[str]) -> str:
    """Sustituye la comprobación de solapamiento léxico puro por pasos adicionales,
    aplicados solo cuando el paso anterior ya considera la afirmación soportada
    (research.md §11). Devuelve uno de
    `_SUPPORTED_OUTCOME`/`_CONTRADICTED_OUTCOME`/`_UNVERIFIABLE_OUTCOME` — antes un
    booleano; generalizado en esta ronda (2026-09-12d, §1) para que
    `GroundingVerifierAgent.execute` pueda distinguir `no_fundamentada` de
    `no_verificable` en el veredicto agregado sin cambiar el contrato publicado de
    `supported_claims`/`unsupported_claims`.

    1. Solapamiento léxico (sin cambios, `_is_supported`) — condición necesaria; si
       falla, `_CONTRADICTED_OUTCOME` (conserva el comportamiento previo: un tema sin
       relación alguna con la evidencia se trata como no soportado, no como incierto).
    2. Alineamiento con la(s) cláusula(s) de evidencia correspondiente(s)
       (`_best_aligned_clauses`) — puede haber más de una cláusula empatada en
       solapamiento léxico (evidencia duplicada/repetida, casos F5/F6), combinadas vía
       `_combine_clause_outcomes`.
    3. Por cada cláusula alineada: polaridad y análisis numérico, vía
       `_claim_is_supported_by_clause` — ver ahí la distinción de casos (a)-(d).
    """
    if not _is_supported(claim, evidence_words):
        return _CONTRADICTED_OUTCOME

    aligned = _best_aligned_clauses(claim, evidence_clauses)
    if not aligned:
        return _SUPPORTED_OUTCOME

    claim_kind, claim_values = _analyze_numeric(claim)
    outcomes = [_claim_is_supported_by_clause(claim, clause, claim_kind, claim_values) for clause in aligned]
    return _combine_clause_outcomes(outcomes)


class GroundingVerifierAgent:
    contract = CONTRACT
    dialogue_contract = CONTRACT.model_copy(
        update={
            "version": "2.0.0",
            "input_schema_ref": "specs/010-guided-dialogue/contracts/dialogue.md#verification-v2",
        }
    )

    def __init__(self, db: SASession | None = None) -> None:
        self._db = db

    async def execute(self, request: AgentRequest, cancellation: CancellationToken) -> AgentResult:
        data = request.input
        proposal_text = str(data.get("proposal_text", ""))
        evidence = data.get("evidence", [])
        general_knowledge_allowed = bool(data.get("general_knowledge_allowed", False))

        if self._db is not None and self._touches_unreviewed_conflict(evidence):
            output = {
                "verdict": "conflictiva",
                "supported_claims": [],
                "unsupported_claims": _split_claims(proposal_text),
            }
            return AgentResult(status="ok", output=output, confidence=None, trace={"verdict": "conflictiva"})

        claims = _split_claims(proposal_text)
        if not claims:
            output = {"verdict": "no_verificable", "supported_claims": [], "unsupported_claims": []}
            return AgentResult(
                status="ok", output=output, confidence=None, trace={"verdict": "no_verificable"}
            )

        if not evidence:
            verdict = "no_verificable" if general_knowledge_allowed else "no_fundamentada"
            output = {"verdict": verdict, "supported_claims": [], "unsupported_claims": claims}
            return AgentResult(status="ok", output=output, confidence=None, trace={"verdict": verdict})

        evidence_words: set[str] = set()
        evidence_clauses: list[str] = []
        for item in evidence:
            text = str(item.get("text", ""))
            evidence_words |= _significant_words(text)
            evidence_clauses.extend(_split_into_clauses(text))

        def outcome(claim):
            # V2 aligns the candidate and evidence at the same conjunct granularity.
            # V1 remains unchanged. No literal-match exemption or candidate hash is
            # used: every clause still passes polarity and numeric consistency.
            parts = _split_into_clauses(claim) if data.get("dialogue_schema_version") == 2 else [claim]
            if not parts or len(parts) > 16:
                return _UNVERIFIABLE_OUTCOME
            values = [_claim_outcome(part, evidence_words, evidence_clauses) for part in parts]
            if _CONTRADICTED_OUTCOME in values:
                return _CONTRADICTED_OUTCOME
            return (
                _SUPPORTED_OUTCOME
                if all(value == _SUPPORTED_OUTCOME for value in values)
                else _UNVERIFIABLE_OUTCOME
            )

        outcomes = {c: outcome(c) for c in claims}
        supported = [c for c in claims if outcomes[c] == _SUPPORTED_OUTCOME]
        unsupported = [c for c in claims if outcomes[c] != _SUPPORTED_OUTCOME]

        if supported and not unsupported:
            verdict = "fundamentada"
        elif supported and unsupported:
            verdict = "parcialmente_fundamentada"
        elif any(outcomes[c] == _CONTRADICTED_OUTCOME for c in unsupported):
            # Al menos una afirmación tiene una diferencia activamente interpretada
            # (polaridad, o dos valores comparables que no coinciden) — seguimiento
            # H03 2026-09-12d, §1: `no_fundamentada` se reserva para este caso.
            verdict = "no_fundamentada"
        else:
            # Ninguna afirmación soportada, y ninguna contradicha de forma
            # interpretada — todas son `_UNVERIFIABLE_OUTCOME` (expresión numérica
            # fuera de alcance sin coincidencia literal): el mecanismo no puede
            # confirmar ni descartar el respaldo, `no_verificable` es más preciso que
            # `no_fundamentada` (seguimiento H03 2026-09-12d, §1).
            verdict = "no_verificable"

        output = {"verdict": verdict, "supported_claims": supported, "unsupported_claims": unsupported}
        return AgentResult(status="ok", output=output, confidence=None, trace={"verdict": verdict})

    def _touches_unreviewed_conflict(self, evidence: list[dict]) -> bool:
        fragment_ids = {str(item.get("fragment_id")) for item in evidence if item.get("fragment_id")}
        if not fragment_ids:
            return False
        records = (
            self._db.query(models.MaterialConflictRecord)
            .filter(models.MaterialConflictRecord.review_status == "pending_review")
            .all()
        )
        for record in records:
            if fragment_ids & set(record.fragment_ids or []):
                return True
        return False
