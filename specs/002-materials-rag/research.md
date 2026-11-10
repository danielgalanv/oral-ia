# Research: Materiales autorizados y RAG trazable

**Input**: `spec.md`, `docs/ORAL-IA_SpecKit/11_plan_prompt.md` (sección RAG), `.specify/memory/constitution.md`, estado real del código de la Feature 001 (`src/oralia/`).

Este documento resuelve las incógnitas técnicas reales de esta feature, acotadas a su
alcance. No investiga decisiones ya resueltas en la Feature 001 (motor de estado, sesión
única activa, etc.) ni adelanta trabajo de features posteriores.

## 1. Cómo se integra la recuperación con el núcleo cognitivo de la Feature 001

**Decision**: esta feature añade un `MaterialRetrieverAgent` y un
`GroundingVerifierAgent` que implementan el mismo protocolo `Executable`
(`contract`/`execute(request, cancellation)`) ya definido en la Feature 001
(`oralia.domain.agents.agent.Executable`), y los expone mediante un endpoint de consulta
directo (`POST /api/v1/materials/query`, área técnica) para demostrar y probar esta
feature de forma independiente. **No se modifica** `DEFAULT_AGENCY` ni
`turn_orchestrator.py` de la Feature 001. La composición de estos agentes dentro de un
turno conversacional real de estudiante es responsabilidad explícita de la Feature 003
(agencia de autoestudio), que ya declara en su propia especificación que reutilizará "el
agente de recuperación ya definido en la Feature 002" dentro de su propia
`AgencyDefinition`.

**Rationale**: cumple FR-025/FR-030 (no modificar el comportamiento ya validado de la
Feature 001) de la forma más literal posible — cero cambios en `turn_orchestrator.py` — y
mantiene esta feature independientemente probable (su propio "Independent Test" de cada
historia de usuario no menciona una sesión de diálogo completa). El endpoint de consulta
directa es suficiente para demostrar la User Story 2 (incluida su Acceptance Scenario 4,
que se valida devolviendo fragmentos/fuentes ya filtrados como si fueran a mostrarse a un
participante, sin necesitar todavía un agente de diálogo real — ese agente pertenece al
roster de la Feature 003).

**Alternatives considered**:
- Añadir ya un paso "retrieve" a `DEFAULT_AGENCY`: rechazado; violaría FR-030 al tocar un
  archivo cuyo comportamiento ya está validado y probado, y anticiparía la composición de
  agentes que la Feature 003 debe decidir explícitamente.

## 2. Motor de índice vectorial local

**Decision**: ChromaDB en modo persistente local, detrás de una interfaz `VectorStore`
propia (`add(fragment_id, embedding, metadata)`, `query(embedding, filters, k)`,
`delete(fragment_id)`, `rebuild()`), tal como recomienda
`docs/ORAL-IA_SpecKit/11_plan_prompt.md`.

**Rationale**: ChromaDB ya soporta filtrado por metadatos (necesario para FR-019:
aislamiento por asignatura/actividad/versión) y borrado/reconstrucción sin escribir un
índice a mano; correr en modo persistente local no introduce ninguna dependencia de red
(Constitución Principio I/VII). La interfaz `VectorStore` mantiene el motor sustituible
(Principio XI) si más adelante se justifica otro backend.

**Alternatives considered**:
- Implementar similitud coseno a mano sobre filas SQLite: rechazado; reinventa
  indexación y filtrado que ChromaDB ya resuelve, sin beneficio de simplicidad real dado
  que la interfaz `VectorStore` ya aísla la elección.
- FAISS: rechazado para el MVP; más bajo nivel, requeriría implementar aparte el
  filtrado por metadatos y la persistencia que ChromaDB ya incluye.

## 3. Embeddings locales

**Decision**: `sentence-transformers` con un modelo multilingüe pequeño ejecutado
localmente (candidato: `paraphrase-multilingual-MiniLM-L12-v2`), detrás de una interfaz
`EmbeddingAdapter` propia (`embed(texts: list[str]) -> list[list[float]]`).

**Rationale**: corre en CPU sin GPU dedicada, soporta español (idioma esperado de los
materiales) y no depende de ningún servicio remoto. La interfaz `EmbeddingAdapter` deja
el modelo concreto sustituible sin tocar el resto del sistema (Principio XI).

**Alternatives considered**:
- Embeddings remotos (OpenAI, etc.): rechazado; viola la ejecución local exigida por la
  Constitución (Principio I/VII).

## 4. Extracción de texto por formato

**Decision**: un `DocumentExtractor` por formato, seleccionado por tipo MIME/extensión,
detrás de una interfaz común `extract(file) -> list[ExtractedBlock]` donde cada bloque
lleva su referencia de ubicación:

| Formato | Librería | Referencia de ubicación |
|---|---|---|
| PDF textual | `pdfplumber` | página |
| DOCX | `python-docx` | párrafo/sección (encabezados) |
| PPTX | `python-pptx` | diapositiva |
| TXT | lectura directa | offset de línea |
| Markdown | lectura directa + parseo de encabezados | sección (encabezado) |

Un PDF cuyo texto extraído esté vacío o por debajo de un umbral mínimo de caracteres por
página se marca como no procesable (FR-003) en vez de indexarse de forma incompleta.

**Rationale**: cada librería es específica de formato y ligera (sin motor de OCR ni
dependencias pesadas), coherente con "OCR avanzado... fuera de alcance". La interfaz
común permite añadir formatos nuevos sin tocar el resto del pipeline.

**Alternatives considered**:
- Un único extractor "universal" (p. ej. `unstructured`): rechazado por ahora; añade una
  dependencia pesada y menos control sobre la referencia de ubicación exacta por
  formato, sin necesidad demostrada para los 5 formatos ya acotados (Principio XI).

## 5. Segmentación reproducible

**Decision**: un divisor de texto determinista propio (sin aleatoriedad ni dependencia de
modelo), configurable por tamaño de fragmento y solapamiento, que respeta límites de
párrafo/oración cuando es posible. Misma entrada + misma configuración → mismos
fragmentos, byte a byte (FR-007).

**Rationale**: evita añadir un framework de chunking de terceros (p. ej. LangChain
completo) solo para esta función, cuando una función pura y auditable de ~50 líneas
resuelve el requisito sin opacar el comportamiento (Principio XI, "evitar frameworks que
oculten el comportamiento").

**Alternatives considered**:
- LangChain `RecursiveCharacterTextSplitter`: rechazado; añadiría una dependencia grande
  para una sola función, cuando el requisito (reproducibilidad configurable) no exige su
  sofisticación adicional.

## 6. Flujo de resolución de duplicados (FR-005a)

**Decision**: `POST /api/v1/materials/documents` calcula el hash antes de procesar; si
coincide con un documento existente, responde `409` con el id/metadatos del documento
existente y un token de conflicto. El profesor confirma explícitamente mediante
`POST /api/v1/materials/documents/{id}/duplicate-resolution` con
`resolution: "link_existing" | "proceed_new"` antes de que el sistema continúe.

**Rationale**: implementa literalmente la decisión de Clarifications ("el sistema MUST
NOT decidir esto de forma automática") como un flujo de dos pasos con confirmación
explícita, en vez de una heurística implícita.

## 7. Detección de conflicto entre fuentes (Escenario D, FR-022)

**Decision**: el `MaterialRetrieverAgent` aplica una heurística determinista (sin modelo)
sobre el conjunto de fragmentos recuperados para una consulta: fragmentos de documentos
distintos que comparten términos clave relevantes pero difieren en marcadores de
polaridad/negación (p. ej. "es"/"no es", cifras distintas para el mismo concepto) se
marcan como conflictivos y generan un `MaterialConflictRecord`.

**Rationale**: coherente con el patrón ya establecido en la Feature 001 de no introducir
un LLM real todavía (research.md §2 de la Feature 001); una heurística determinista y
con pruebas dirigidas es suficiente para el conjunto de pruebas preparado que pide
SC-005/Escenario D, sin añadir un modelo de inferencia de lenguaje natural (NLI) que esta
feature no justifica.

**Alternatives considered**:
- Un modelo NLI (Natural Language Inference) dedicado: rechazado para el MVP; añade una
  dependencia de ML significativa sin necesidad demostrada frente a una heurística
  dirigida y probada.

## 8. Defensa frente a prompt injection documental

**Decision**: el texto extraído de un documento MUST NOT concatenarse nunca en una
región de instrucciones/sistema; se transporta exclusivamente como datos estructurados
(`MaterialFragment.text`, campo `content`/`input` de `AgentRequest`), igual que
cualquier otro dato de entrada de un agente en la Feature 001. Como esta feature (como la
Feature 001) no integra todavía un LLM real, la regla se documenta como una restricción
de contrato explícita para cuando la Feature 003 conecte agentes de generación reales,
no como un filtro de contenido añadido ahora.

**Rationale**: consistente con el patrón "AgentRequest.context = subconjunto mínimo
filtrado, nunca el estado completo" ya establecido en `contracts/agent-contract.md` de la
Feature 001; declarar la regla en el contrato ahora evita que se tenga que reconstruir
más tarde.

## 9. Reconstrucción del índice y concurrencia (Edge Case)

**Decision**: reutilizar el mismo patrón de bloqueo de un solo escritor que
`session_lock_service.py` de la Feature 001 (columna con restricción de unicidad,
comparar-y-escribir atómico), aplicado a un nuevo `index_rebuild_lock` en vez de a
sesiones. Una segunda solicitud de reconstrucción mientras la primera está en curso se
rechaza explícitamente (`409`) en vez de encolarse, por simplicidad (Principio XI) y
porque el propio Edge Case solo exige "tratar la otra de forma explícita".

**Rationale**: reutiliza un mecanismo ya validado y probado en la Feature 001 en vez de
inventar uno nuevo para el mismo problema estructural (evitar dos escritores
concurrentes sobre un recurso único).

## 10. Componentes de la pila propuesta que esta feature sí adopta (a diferencia de la Feature 001)

**Decision**: se adoptan ahora ChromaDB, `sentence-transformers`, `pdfplumber`,
`python-docx` y `python-pptx` — deliberadamente diferidos en la Feature 001
(research.md §6 de esa feature) porque no eran necesarios todavía. Esta feature es
precisamente la que los necesita.

**Rationale**: cumple la propia justificación que la Feature 001 dejó escrita: estos
componentes "pertenecen a las Features 002 (materiales/RAG)". Adoptarlos aquí, con una
interfaz sustituible para cada uno, respeta el Principio XI (dependencia justificada por
necesidad real, no anticipada).

## 11. Refuerzo del verificador de fundamentación (FR-023) — corregido en el seguimiento de H03, 2026-09-12b; ampliado en la ronda R1-R3, 2026-09-12c; corregido semánticamente en la ronda 2026-09-12d (encabezado corregido en 2026-09-12f — la regla es: INCOMPLETE_KIND con coincidencia literal → fundamentada; INCOMPLETE_KIND sin coincidencia literal y sin contradicción interpretable → no_verificable, nunca no_fundamentada por defecto); corregida la simetría en la ronda 2026-09-12e (T096); resuelta la ambigüedad parcialmente_fundamentada/no_fundamentada/conflictiva en la ronda 2026-09-12f (T097, /speckit-clarify)

**Hallazgo de partida (auditoría previa, H03)**: `grounding_verifier_agent.py` clasifica
como `fundamentada` una propuesta cuyo solapamiento léxico de palabras ≥4 letras con la
evidencia supera el 40%, sin comparar valores. *"El agua hierve a 20 grados."* frente a
la evidencia *"El agua hierve a 100 grados."* obtiene solapamiento 3/3 = 1.0 → clasifica
como `fundamentada` pese a contradecir el valor numérico de la evidencia.

**Corrección de esta ronda (F1–F7, revisión independiente sobre la implementación de la
ronda anterior)**: siete causas concretas, todas corregidas juntas en
`_extract_values`/`_split_on_y`/`_claim_is_supported` (`src/oralia/domain/agents/
grounding_verifier_agent.py`) — **sin excepciones literales para las siete frases**,
verificado con contrastes propios distintos de los siete casos (ver matriz):

| Causa | Ejemplo que la revela | Corrección |
|---|---|---|
| "un"/"una" se trataban como numerales independientes | F1: "Una sesión dura 20 minutos." → el "una" inicial se leía como valor 1, ocultando el "20" real | `un`/`una` MUST NOT contar como valor por sí solos — solo cuando preceden inmediatamente a una unidad reconocida ("una hora" = 1 hora); en cualquier otro caso se saltan y la extracción continúa buscando el valor real de la cláusula |
| Solo se extraía el primer valor de la cláusula | F3: "de 20 a 100" frente a "de 20 a 30" — el primer valor (20) coincidía y el segundo (100 vs. 30) nunca se comprobaba | `_extract_values` devuelve **todos** los valores de la cláusula, en orden; `_values_are_consistent` exige que **cada** valor de la propuesta tenga un valor equivalente en la evidencia — no basta con que uno coincida |
| La división de cláusulas por " y " rompía numerales compuestos | F4: "noventa y nueve" se partía en "noventa" + "nueve minutos", perdiendo el valor real (99) | `_split_on_y` comprueba, en cada punto de división candidato, si la palabra anterior es una decena (`_TENS_WORDS`) y la siguiente una unidad 1-9 (`_UNIT_DIGIT_WORDS`) — si ambas se cumplen, no se divide ahí |
| Un valor sin contrapartida comparable se aprobaba por solapamiento léxico | F2: "El proceso dura 20 minutos." frente a "El proceso dura varios minutos." — "varios" no es un valor, pero el solapamiento léxico ya bastaba para "fundamentada" | Cuando la propuesta tiene un valor y la cláusula de evidencia alineada NO tiene ningún valor reconocido, la afirmación se trata como no soportada — nunca se aprueba recurriendo solo al solapamiento de palabras (ver la distinción a/b/c más abajo) |
| El signo no formaba parte del valor extraído | F7: "20 grados" frente a "-20 grados" — el signo se perdía y ambos se comparaban como "20" | El tokenizador captura un signo `+`/`-` inmediatamente adyacente al dígito como parte del valor |
| Fragmentos de evidencia duplicados se trataban como ambigüedad | F5: evidencia idéntica duplicada (dos fragmentos, mismo texto) producía un empate que se resolvía como no soportada sin comprobar nada más | Un empate entre cláusulas ya NO devuelve un resultado fijo — cada cláusula empatada se evalúa por separado (polaridad + valor); si todas coinciden con la propuesta, está soportada |
| Un empate entre cláusulas devolvía `True` sin comprobar polaridad | F6: evidencia duplicada, pero además de polaridad opuesta a la propuesta, "aprobaba" solo por el empate | La misma corrección anterior resuelve esto: cada cláusula empatada se evalúa, incluida la polaridad — si **ninguna** coincide (como en F6), es una contradicción, no una aprobación por defecto |

**Distinción explícita de tres casos (§2 de esta ronda), implementada en
`_claim_is_supported_by_clause`**:

- **(a) No existe afirmación numérica en la propuesta** (`_extract_values(claim)` está
  vacío) — el paso de comparación numérica no se aplica; el veredicto depende solo del
  solapamiento léxico y la polaridad, igual que antes.
- **(b) Existe y puede compararse** — la propuesta tiene valores y la cláusula de
  evidencia alineada también → se comparan con `_values_are_consistent` (cada valor de
  la propuesta MUST tener un valor equivalente en la evidencia).
- **(c) Existe, pero no puede interpretarse o alinearse con seguridad** — la propuesta
  tiene un valor, pero la cláusula de evidencia alineada no tiene ninguno reconocido
  (F2), o el alineamiento entre cláusulas está genuinamente en desacuerdo (algunas
  cláusulas empatadas respaldan la afirmación, otras no) → **no soportada**, nunca
  convertida en "fundamentada" por el solapamiento léxico que ya se había superado en
  el paso 1.

**Alineamiento por cláusula (`_best_aligned_clauses`, sin cambios de diseño respecto a
la ronda anterior, solo corregido en su interacción con los empates — ver arriba)**: la
evidencia se divide en cláusulas (por oración y por conjunciones acotadas — "y" con la
protección de numerales compuestos, ";", "pero") y se busca la o las cláusulas con
mayor solapamiento léxico con la propuesta; si la propuesta menciona una etiqueta de
entidad de una sola letra mayúscula ("A", "B" — invisible al solapamiento léxico
ordinario), el alineamiento se restringe primero a las cláusulas que comparten esa
misma etiqueta (caso MULTI, sin cambios: sigue funcionando tras esta corrección).

**Separación de afirmaciones de procedencia (`_split_claims`, sin cambios respecto a la
ronda anterior)**: un marcador de procedencia/atribución ("como se explica en",
"según", "de acuerdo con") seguido de un sustantivo de referencia concreto ("página",
"capítulo", "sección"...) separa la localización de su contenido temático — no se
modifica en esta ronda.

**Alcance explícito y honesto de la extracción numérica (corregido: ya no se afirma
"no verificado" donde el código sí verifica; actualizado en la ronda R1-R3, ver más
abajo — esta redacción ya no es exacta desde esa ronda para fracciones/notación
científica/compuestos de centena, ver la corrección explícita)**: numerales
cardinales simples (cero–diez, decenas hasta noventa) y compuestos de decena+unidad
("noventa y nueve"), más "cien" — comparando **todos** los valores de una cláusula, no
solo el primero, y con el signo como parte del valor. Unidades reconocidas: lista
acotada (grados, minutos, horas, segundos, kilómetros, metros, litros, gramos,
kilogramos).

**Corrección de esta ronda (R1-R3, revisión independiente sobre la implementación
F1-F7)**: dos defectos estructurales, ambos con causa en que `_values_are_consistent`
(comparación por pertenencia vía `any()`) y la distinción a/b/c anterior (basada en
"¿la lista de valores extraídos está vacía?") no eran suficientes:

| Causa | Ejemplo que la revela | Corrección |
|---|---|---|
| `_values_are_consistent` comparaba por pertenencia en el conjunto de valores de la evidencia, sin conservar el papel relacional de cada valor | R1: "de 100 a 20 grados" frente a evidencia "de 20 a 100 grados" — ambos números (20 y 100) existen en la evidencia, así que la comparación por pertenencia los daba por buenos aunque origen y destino estuvieran intercambiados | Se introduce `_tag_roles`: cuando una cláusula encaja en el patrón "de VALOR ... a VALOR", el primer valor se etiqueta `role="origin"` y el segundo `role="destination"`. `_values_are_consistent` exige, para un valor de la propuesta con `role` definido, que el candidato de evidencia comparado tenga el **mismo** `role` — no cualquier valor de la lista. Un valor sin papel relacional declarado (`role=None`, afirmación simple que no reproduce la relación completa) se sigue comparando de forma permisiva contra cualquier valor de la evidencia, para no rechazar una afirmación parcial válida (REL-SIMPLE-PARTIAL) |
| Una lista de valores vacía no distinguía "la cláusula no afirma ningún número" de "la cláusula tiene una expresión numérica que el analizador no interpreta con seguridad" — el segundo caso caía en el primero y el veredicto quedaba solo al solapamiento léxico, que "mil"/"ciento veinte" ya habían superado por las palabras restantes | R2: "mil minutos" frente a "cien minutos" — "mil" no está en `_SIMPLE_NUMBER_WORDS`, así que no se extraía ningún valor de la propuesta; el resto de palabras ("sesión", "dura", "minutos") ya bastaban para el solapamiento léxico, y el caso (a) ("sin afirmación numérica") aprobaba por defecto. R3: "ciento veinte minutos" — "ciento" tampoco se reconoce, pero "veinte" sí, y se extraía como si fuera el valor completo de la cláusula (120 se leía como 20) | Se sustituye la lista (vacía/no vacía) por una clasificación explícita de tres vías (`_analyze_numeric` → `NONE_KIND`/`PARSED_KIND`/`INCOMPLETE_KIND`, §3 de esta ronda, detallada más abajo). Encontrar un disparador de `_INCOMPLETE_NUMBER_TRIGGERS` (mil, millón, cualquier centena distinta de "cien"), una fracción (`_FRACTION_PATTERN`) o notación científica (`_SCIENTIFIC_PATTERN`) en la cláusula marca **toda la cláusula** como `INCOMPLETE_KIND` — no se intenta rescatar valores parciales de ella (evita que "ciento veinte" se lea como "veinte") |

**Representación explícita de tres vías del análisis numérico (§3 de esta ronda,
`_analyze_numeric`), que sustituye la distinción a/b/c basada solo en "lista vacía o
no" de la ronda anterior**:

- **`NONE_KIND`** — ninguna expresión numérica reconocible ni fuera de alcance en la
  cláusula; el paso de comparación numérica no se aplica (equivalente al caso (a)
  anterior).
- **`PARSED_KIND`** — una o más expresiones numéricas dentro del alcance admitido,
  con su papel relacional ya etiquetado cuando corresponde (`_tag_roles`); se comparan
  con `_values_are_consistent` (equivalente al caso (b) anterior, ahora role-aware).
- **`INCOMPLETE_KIND`** — se detectó una expresión numérica fuera del alcance
  reconocido (disparadores de centena/millar, fracción, notación científica); la
  cláusula se trata como no interpretada con seguridad. Si es la propia **propuesta**
  la que analiza como `INCOMPLETE_KIND`, se aplica la regla corregida en la ronda
  2026-09-12d (ver más abajo: coincidencia literal → soportada; texto distinto → no
  soportada, con el veredicto agregado distinguiendo `no_verificable` de
  `no_fundamentada`). Si es la cláusula de **evidencia** alineada la que analiza como
  `INCOMPLETE_KIND` (o como `NONE_KIND`) mientras la propuesta sí tiene valores
  `PARSED_KIND`, sigue aplicando el caso (c) ya existente: no soportada (contribuye a
  `no_fundamentada`), nunca aprobada por el solapamiento léxico ya superado — este
  caso no puede coincidir literalmente por construcción (si el texto fuera idéntico,
  ambas cláusulas analizarían con el mismo `_analyze_numeric`, luego no podrían tener
  `PARSED_KIND` en una y no en la otra).

**Corrección semántica de esta ronda (2026-09-12d) — la decisión anterior era
incorrecta**: la ronda R1-R3 (T094) exigía `no_fundamentada` para **toda** propuesta
con análisis `INCOMPLETE_KIND`, incluso cuando el texto era idéntico al de la
evidencia (`INCOMPLETE-MIL-IDENTICAL`, `INCOMPLETE-FRACTION`, `INCOMPLETE-SCIENTIFIC`:
"La sesión dura mil minutos." frente a sí misma clasificaba `no_fundamentada`). Esa
regla era demasiado fuerte: una coincidencia literal normalizada de la afirmación
completa con una cláusula de evidencia SÍ constituye respaldo documental, aunque el
formato numérico quede fuera del analizador — la incapacidad de interpretar el valor
no permite afirmar que la evidencia no lo respalda cuando el texto es, salvo
espacios/puntuación, el mismo. Se retira esa exigencia y se sustituye por:

- **Coincidencia literal normalizada** (`_normalize_literal` — únicamente minúsculas,
  puntuación superficial de una lista fija `.,;:!¡?¿"'()`, y colapso de espacios; MUST
  NOT eliminar dígitos, signos `+`/`-`, "/", ni ninguna letra) de la afirmación
  completa con la cláusula de evidencia alineada → `_SUPPORTED_OUTCOME` (soportada),
  aunque el análisis numérico sea `INCOMPLETE_KIND`.
- **Sin coincidencia literal** (texto distinto en número, signo, unidad, negación o
  cualquier palabra) → `_UNVERIFIABLE_OUTCOME` — nunca `_SUPPORTED_OUTCOME` por
  solapamiento léxico parcial, y nunca `_CONTRADICTED_OUTCOME` (que exige una
  diferencia realmente interpretada, no solo una incapacidad de interpretación).

**Veredicto agregado — `no_fundamentada` frente a `no_verificable` (§1 de esta
ronda)**: `GroundingVerifierAgent.execute` distingue, internamente, tres resultados
por afirmación (`_SUPPORTED_OUTCOME`/`_CONTRADICTED_OUTCOME`/`_UNVERIFIABLE_OUTCOME`,
ver `_claim_outcome`) sin cambiar el contrato ya publicado de
`supported_claims`/`unsupported_claims` (ambas listas siguen siendo `string[]`; una
afirmación `_UNVERIFIABLE_OUTCOME` se sigue reportando en `unsupported_claims`, igual
que antes). Cuando ninguna afirmación está soportada: si al menos una es
`_CONTRADICTED_OUTCOME` (una diferencia activamente interpretada — polaridad, o dos
valores ambos comparables que no coinciden), el veredicto es `no_fundamentada`; si
**todas** las no soportadas son `_UNVERIFIABLE_OUTCOME` (el mecanismo no pudo
interpretar la expresión numérica y el texto no coincide literalmente), el veredicto
es `no_verificable` — más preciso que `no_fundamentada`, que se reserva para una
contradicción efectivamente interpretada. Esto no requirió cambiar el esquema de
`supported_claims`/`unsupported_claims`: la distinción de tres vías es una decisión
interna de agregación para el campo `verdict`, compatible con los consumidores
actuales sin modificarlos (Feature 003 ya trata `no_verificable` como un veredicto
válido — ver la nota de límite más abajo sobre `self_study_agency_composer.py`).

**Corrección de simetría de esta ronda (2026-09-12e, T096) — la regla de T095 se
aplicaba de forma asimétrica**: T095 declaró que `_CONTRADICTED_OUTCOME` exige "una
diferencia activamente interpretada — polaridad, o dos valores ambos comparables que
no coinciden" (párrafo anterior), pero `_claim_is_supported_by_clause` solo analizaba
`_analyze_numeric` sobre la **propuesta**; la cláusula de evidencia alineada se
analizaba únicamente dentro de la rama `PARSED_KIND` (caso b/c), nunca antes de
decidir la rama `INCOMPLETE_KIND` de la propuesta. Esto producía una asimetría
verificable: "La sesión dura 1000 minutos." (propuesta, `PARSED_KIND`) frente a "La
sesión dura mil minutos." (evidencia, `INCOMPLETE_KIND`) clasificaba `no_fundamentada`
(caía en el caso c, "evidencia sin `PARSED_KIND`" — pensado para `NONE_KIND`, F2, no
para `INCOMPLETE_KIND`); la misma relación invertida (propuesta "mil minutos",
evidencia "1000 minutos") clasificaba `no_verificable` — la dirección de la
comparación decidía el veredicto sin que existiera asimetría semántica en la relación
expresada, y sin que ambos valores hubieran sido interpretados en el caso que daba
`no_fundamentada`.

**Corrección**: `_claim_is_supported_by_clause` ahora analiza `_analyze_numeric` de
**ambos** lados (propuesta y cláusula de evidencia alineada) antes de decidir. Si
**cualquiera** de los dos lados es `INCOMPLETE_KIND`, se aplica la misma regla de
coincidencia literal normalizada que T095 ya aplicaba solo a la propuesta —
`_SUPPORTED_OUTCOME` si coincide, `_UNVERIFIABLE_OUTCOME` si no — nunca
`_CONTRADICTED_OUTCOME` sin que ambos valores hayan podido interpretarse. La
comparación literal (`_normalize_literal(a) == _normalize_literal(b)`) es en sí misma
simétrica, luego el resultado deja de depender de qué lado se llame "propuesta". El
caso F2 (`PARSED_KIND` frente a `NONE_KIND`) se conserva exactamente igual — se
comprueba después de descartar `INCOMPLETE_KIND` en ambos lados, así que
`NONE_KIND` (ausencia real de expresión numérica) y `INCOMPLETE_KIND` (expresión
detectada pero no interpretada) siguen siendo casos distintos con tratamiento
distinto, tal como exigía la instrucción de esta ronda.

**Verificado explícitamente en ambos sentidos** (`tests/contract/
test_grounding_verifier.py`, matriz `T096-*`): "1000 minutos"↔"mil minutos",
"20 minutos"↔"mil minutos", "0.5 miligramos"↔"1/2 miligramos", y "3e8 metros"↔
"300000000 metros" — los ocho casos (cuatro pares × dos direcciones) clasifican
`no_verificable`. Una propiedad adicional (`test_h03_t096_symmetry_swapping_proposal_and_evidence_keeps_same_verdict`,
parametrizada sobre `_H03_SYMMETRY_PAIRS`) confirma, para pares sin direccionalidad
semántica (incluidos los cuatro anteriores, más una coincidencia exacta de dígitos,
una contradicción numérica simple, y una coincidencia incompleta idéntica), que
intercambiar cuál texto se envía como propuesta y cuál como evidencia produce
siempre el mismo veredicto agregado.

**Formatos numéricos admitidos y tratamiento explícito de los no interpretados
(corregido — no se promete reconocimiento universal de cualquier expresión del
lenguaje, y no se afirma "no se presenta como verificado" donde el código sí lo
distingue)**:

- **Admitidos (`PARSED_KIND`)**: dígitos y decimales con signo opcional adyacente
  (`-20`, `+3.5`); numerales cardinales simples cero–diez, decenas hasta noventa, y
  "cien" (`_SIMPLE_NUMBER_WORDS`); compuestos decena+"y"+unidad 1-9 ("noventa y
  nueve" = 99); "un"/"una" únicamente cuando preceden a una unidad reconocida ("una
  hora" = 1 hora); el papel relacional origen/destino del patrón "de VALOR ... a
  VALOR".
- **Detectados pero no interpretados como un valor concreto (`INCOMPLETE_KIND`,
  `_INCOMPLETE_NUMBER_TRIGGERS`/`_FRACTION_PATTERN`/`_SCIENTIFIC_PATTERN`)**:
  "mil"/"millón"/"millones"; cualquier centena distinta de "cien" ("ciento",
  "doscientos", ..., "novecientos") — incluida como prefijo de un compuesto de
  centena+decena ("ciento veinte"); fracciones con barra ("1/2", "3/4"); notación
  científica ("3e8", "3×10^8"). Una cláusula que contiene cualquiera de estos MUST
  NOT clasificarse como `fundamentada` recurriendo al resto de su contenido léxico
  cuando el texto difiere del de la evidencia — pero SÍ cuando coincide literalmente
  con ella salvo espacios/puntuación (corrección de esta ronda, ver arriba).
- **Fuera de ambas categorías (ni admitidos ni detectados como incompletos; en la
  práctica caen en `NONE_KIND` si no hay ningún otro valor en la cláusula)**:
  numerales ordinales, fracciones en palabras ("un tercio"), cualquier otra
  construcción numérica no cubierta arriba. No se promete su reconocimiento — este
  refuerzo no es un analizador numérico general del español.
- **No se resuelve mediante excepciones a las frases R1/R2/R3 concretas**: la
  clasificación opera sobre patrones léxicos acotados
  (`_INCOMPLETE_NUMBER_TRIGGERS`, `_FRACTION_PATTERN`, `_SCIENTIFIC_PATTERN`,
  `_tag_roles`, `_normalize_literal`), verificado con contrastes construidos
  independientemente de esas tres frases (ver matriz: REL-IDENTICAL,
  REL-ONE-END-CHANGES, REL-SIMPLE-PARTIAL, INCOMPLETE-FRACTION-DIFFERENT-VALUE,
  INCOMPLETE-SCIENTIFIC-DIFFERENT-VALUE, INCOMPLETE-SIGN-DIFFERENT,
  INCOMPLETE-UNIT-DIFFERENT, INCOMPLETE-NEGATION-DIFFERENT,
  INCOMPLETE-WHITESPACE-PUNCTUATION-ONLY, INCOMPLETE-SAME-FIGURE-DIFFERENT-ENTITY,
  PREFIX-DOES-NOT-LEAK-SUFFIX).

**Límite documentado — interacción con Feature 003, no modificada esta ronda**:
`self_study_agency_composer.py` (Feature 003) contiene un comentario ("única
situación en la que GroundingVerifierAgent produce `no_verificable`") que ya no es
exacto tras esta corrección — `no_verificable` ahora también surge con evidencia no
vacía, para una afirmación con una expresión numérica no interpretada sin coincidencia
literal. El comportamiento observable no cambia cuando
`general_knowledge_allowed = false` (el caso por defecto): el compositor cae en la
misma rama que usa `supported_claims` y produce `acknowledge_missing_info`, verificado
con la nueva integración `test_r2_unrecognized_numeral_never_reaches_participant_as_grounded`.
Cuando `general_knowledge_allowed = true`, el compositor etiquetaría esta respuesta
como conocimiento general en vez de reconocer la falta de evidencia interpretable —
un caso no cubierto por las pruebas de esta ronda ni corregido aquí (Feature 003 está
fuera del alcance autorizado). Se documenta como riesgo conocido para una ronda
posterior de 003, no se declara resuelto.

**Por qué no se generaliza más allá de esto**: sinónimos, paráfrasis, negación con
alcance sintáctico ambiguo dentro de una oración compleja, u ofuscación deliberada del
valor siguen sin detectarse — límite aceptado y fuera del alcance de este refuerzo. No
se presenta la superación de la matriz siguiente como garantía semántica universal de
fundamentación.

**Matriz de aceptación (casos de control — implementada; verificada con
`GroundingVerifierAgent.execute()` real, `tests/contract/test_grounding_verifier.py`)**:

| # | Claim | Evidencia | Esperado | Motivo |
|---|---|---|---|---|
| S1 | "El agua hierve a 100 grados." | "El agua hierve a 100 grados." | `fundamentada` | coincidencia exacta |
| C1 | "El agua hierve a 20 grados." | "El agua hierve a 100 grados." | `no_fundamentada` | caso original H03 — contradicción numérica |
| C2 | "La sesión dura 45 minutos." | "La sesión dura 90 minutos." | `no_fundamentada` | contradicción numérica en dominio distinto |
| C3 | "El agua no hierve a 100 grados." | "El agua hierve a 100 grados." | `no_fundamentada` | contradicción de polaridad |
| NEG1 | "El proceso es reversible." | "El proceso no es reversible." | `no_fundamentada` | mismo contraste que C3, dominio distinto |
| NEG2 | "El proceso no es reversible." | "El proceso no es reversible." | `fundamentada` | misma negación en ambos |
| NEG-UNRELACIONADA | "El proceso es reversible. El experimento no funcionó ayer." | "El proceso es reversible en laboratorio. Otro tema no relacionado no aplica aquí." | `parcialmente_fundamentada` | una negación en una cláusula no alineada no invalida la afirmación soportada |
| I1 | "El proceso es reversible en condiciones estándar." | "El proceso es reversible en condiciones estándar de laboratorio." | `fundamentada` | sin números ni negación |
| I2 | "El calentamiento global aumenta la temperatura media, como se explica en la página 12." | "El calentamiento global aumenta la temperatura media del planeta." | `parcialmente_fundamentada` | procedencia sin respaldo separada del contenido temático |
| V1 | "El agua hierve a 99 grados." | "El agua hierve a 100 grados." | `no_fundamentada` | 99≠100, tolerancia 0 |
| V2 | "El agua hierve a noventa y nueve grados." | "El agua hierve a 100 grados." | `no_fundamentada` | numeral compuesto (90+9) comparado con dígito |
| CIEN | "El agua hierve a cien grados." | "El agua hierve a 100 grados." | `fundamentada` | numeral simple equivalente a 100 |
| MULTI | "A dura 100 minutos." | "A dura 20 minutos y B dura 100 minutos." | `no_fundamentada` | alineamiento por etiqueta de entidad — 100 pertenece a B, no a A |
| UNIT | "El objeto dura 20 minutos." | "El objeto dura 20 kilómetros." | `no_fundamentada` | mismo valor numérico, unidades incompatibles |
| **F1** (nuevo, causa: "un"/"una" como valor independiente) | "Una sesión dura 20 minutos." | "Una sesión dura 100 minutos." | `no_fundamentada` | "una" ya no oculta el valor real (20 vs. 100) |
| **F2** (nuevo, caso (c)) | "El proceso dura 20 minutos." | "El proceso dura varios minutos." | `no_fundamentada` | la cifra concreta (20) no tiene contrapartida numérica en la evidencia — "varios" no es un valor |
| **F3** (nuevo, causa: solo el primer valor) | "La temperatura aumenta de 20 a 100 grados." | "La temperatura aumenta de 20 a 30 grados." | `no_fundamentada` | el segundo valor (100 vs. 30) también se compara y no coincide |
| **F4** (nuevo, causa: división rompía numerales compuestos) | "La sesión dura noventa y nueve minutos." | "La sesión dura noventa y nueve minutos." (idéntica) | `fundamentada` | "noventa y nueve" ya no se divide en dos cláusulas sin sentido numérico |
| **F5** (nuevo, causa: empate → no soportada sin más) | "El agua hierve a 100 grados." | dos fragmentos, cada uno "El agua hierve a 100 grados." | `fundamentada` | evidencia duplicada idéntica — ambas cláusulas empatadas coinciden con la propuesta |
| **F6** (nuevo, causa: empate → `True` sin comprobar polaridad) | "El proceso no es reversible." | dos fragmentos, cada uno "El proceso es reversible." | `no_fundamentada` | evidencia duplicada, pero de polaridad opuesta — ninguna cláusula empatada coincide |
| **F7** (nuevo, causa: signo no formaba parte del valor) | "La temperatura es 20 grados." | "La temperatura es -20 grados." | `no_fundamentada` | 20≠-20 |
| PROP-SEGUNDO-VALOR (contraste de F3) | "La temperatura aumenta de 20 a 100 grados." | idéntica | `fundamentada` | cambiar solo el segundo valor se detecta (F3); mantenerlo igual sigue fundamentado |
| PROP-MAGNITUD-NEGATIVA (contraste de F7) | "La temperatura es -20 grados." | idéntica | `fundamentada` | igual magnitud negativa en ambos se admite; el signo opuesto (F7) se distingue |
| **R1** (nuevo, causa: comparación por pertenencia sin papel relacional) | "La temperatura aumenta de 100 a 20 grados." | "La temperatura aumenta de 20 a 100 grados." | `no_fundamentada` | origen/destino intercambiados — 100 como origen no encuentra un 100-origen en la evidencia (es destino allí); diferencia activamente interpretada (`_CONTRADICTED_OUTCOME`) |
| **R2** (causa: "mil" no reconocido; verdict corregido en 2026-09-12d) | "La sesión dura mil minutos." | "La sesión dura cien minutos." | `no_verificable` | la propuesta analiza `INCOMPLETE_KIND` y su texto no coincide literalmente con la evidencia — el mecanismo no puede interpretar "mil" ni afirmar que "cien" lo contradice (`_UNVERIFIABLE_OUTCOME`); no `no_fundamentada` (esa ronda anterior era demasiado fuerte, ver corrección arriba) |
| **R3** (causa: "ciento veinte" degradado a "veinte"; verdict corregido en 2026-09-12d) | "La sesión dura ciento veinte minutos." | "La sesión dura veinte minutos." | `no_verificable` | "ciento" marca toda la cláusula como `INCOMPLETE_KIND`; texto distinto de la evidencia → `_UNVERIFIABLE_OUTCOME`, no una contradicción interpretada |
| REL-IDENTICAL (contraste de R1) | "La temperatura aumenta de 20 a 100 grados." | idéntica | `fundamentada` | misma relación origen/destino, sin intercambiar |
| REL-ONE-END-CHANGES (contraste de R1) | "La temperatura aumenta de 20 a 100 grados." | "La temperatura aumenta de 20 a 30 grados." | `no_fundamentada` | mismo origen (20), destino distinto (100 vs. 30) — ya cubierto también por F3, reafirmado con roles |
| REL-SIMPLE-PARTIAL (contraste de R1) | "La temperatura alcanza 100 grados." | "La temperatura aumenta de 20 a 100 grados." | `fundamentada` | afirmación simple sin papel relacional declarado (`role=None`) — se compara de forma permisiva, no se rechaza por no mencionar el origen |
| INCOMPLETE-MIL-IDENTICAL (corregido en 2026-09-12d) | "La sesión dura mil minutos." | idéntica | `fundamentada` | coincidencia literal normalizada — SÍ constituye respaldo aunque "mil" quede fuera del analizador (decisión anterior de exigir `no_fundamentada` aquí era incorrecta, ver corrección arriba) |
| INCOMPLETE-FRACTION (corregido en 2026-09-12d) | "La dosis es 1/2 miligramo." | idéntica | `fundamentada` | coincidencia literal — "1/2" no se trata como dos números independientes, pero el texto idéntico sí se reconoce como respaldo |
| INCOMPLETE-SCIENTIFIC (corregido en 2026-09-12d) | "La velocidad es 3e8 metros." | idéntica | `fundamentada` | coincidencia literal — notación científica no se convierte en una lista de valores verificados, pero el texto idéntico sí se reconoce como respaldo |
| INCOMPLETE-FRACTION-DIFFERENT-VALUE (nuevo, 2026-09-12d) | "La dosis es 1/2 miligramo." | "La dosis es 1/3 miligramo." | `no_verificable` | texto distinto — sin coincidencia literal, no se puede confirmar ni descartar el respaldo |
| INCOMPLETE-SCIENTIFIC-DIFFERENT-VALUE (nuevo, 2026-09-12d) | "La velocidad es 3e8 metros." | "La velocidad es 4e8 metros." | `no_verificable` | mismo razonamiento, notación científica con valor distinto |
| INCOMPLETE-SIGN-DIFFERENT (nuevo, 2026-09-12d) | "La velocidad es -3e8 metros." | "La velocidad es 3e8 metros." | `no_verificable` | `_normalize_literal` MUST NOT eliminar el signo — un signo distinto no coincide literalmente |
| INCOMPLETE-UNIT-DIFFERENT (nuevo, 2026-09-12d) | "La sesión dura mil minutos." | "La sesión dura mil kilómetros." | `no_verificable` | unidad distinta — no coincide literalmente, no se normaliza como equivalente |
| INCOMPLETE-NEGATION-DIFFERENT (nuevo, 2026-09-12d) | "La sesión dura mil minutos." | "La sesión no dura mil minutos." | `no_fundamentada` | polaridad distinta se detecta ANTES del análisis numérico — diferencia activamente interpretada (`_CONTRADICTED_OUTCOME`), no `no_verificable` |
| INCOMPLETE-WHITESPACE-PUNCTUATION-ONLY (nuevo, 2026-09-12d) | "La sesión dura mil minutos." | "La sesión  dura mil minutos" (doble espacio, sin punto) | `fundamentada` | única diferencia es espacios/puntuación — `_normalize_literal` los colapsa/elimina, coincidencia literal |
| INCOMPLETE-SAME-FIGURE-DIFFERENT-ENTITY (nuevo, 2026-09-12d) | "A dura mil minutos." | "A dura cien minutos. B dura mil minutos." | `no_verificable` | el alineamiento por etiqueta de entidad restringe la comparación a la cláusula de "A" ("cien", no "mil") — la misma cifra "mil" en la cláusula de "B" no puede usarse para inflar el respaldo de "A" |
| PREFIX-DOES-NOT-LEAK-SUFFIX (corregido en 2026-09-12d) | "La sesión dura doscientos veinte minutos." | "La sesión dura veinte minutos." | `no_verificable` | un prefijo de centena no reconocido no deja pasar el sufijo ("veinte") como si fuera la cantidad completa; texto distinto → `_UNVERIFIABLE_OUTCOME`, no `no_fundamentada` |

**Propiedades verificadas además de la matriz** (`tests/contract/
test_grounding_verifier.py`): duplicar evidencia idéntica y reordenar esos fragmentos
no cambia el veredicto (`test_h03_property_duplicate_and_reorder_evidence_same_verdict`);
una afirmación parcialmente respaldada conserva `supported_claims`/`unsupported_claims`
disjuntas y completas (`test_h03_property_partial_claim_lists_stay_coherent`).

**Las variantes ya publicadas (V1/V2/CIEN/MULTI/UNIT y ahora F1–F7) son casos de
regresión conocidos, no una validación independiente oculta**: todas con resultado
esperado definido y derivado del diseño — no se usan para *construir* esas decisiones,
solo para comprobar que la implementación las satisface.

**Consumidores**: `GroundingVerifierAgent` es reutilizado sin cambios de contrato por la
Feature 003 (verificado con cuatro pruebas de integración de autoestudio reales — la
original, `test_grounding_blocks_contradicting_proposal_in_self_study.py`, una para
F1, `test_f1_contradicting_duration_never_reaches_participant_as_grounded`, una para
R1, `test_r1_swapped_origin_destination_never_reaches_participant_as_grounded`, y una
nueva para R2, `test_r2_unrecognized_numeral_never_reaches_participant_as_grounded`
— esta última confirma explícitamente el veredicto trazado `no_verificable` (no
`no_fundamentada`), verificando la corrección semántica de esta ronda de principio a
fin — verificador real sin mock, la afirmación incorrecta no llega al participante
como respuesta respaldada) y está previsto que lo reutilice la Feature 004
(`specs/004-oral-defense-agency/plan.md:67`). Ver el límite documentado arriba sobre
`self_study_agency_composer.py` cuando `general_knowledge_allowed = true`. Añadida en
esta ronda: `test_t096_digit_proposal_vs_word_evidence_never_reaches_participant_as_grounded`
— confirma que "1000 minutos" (dígito, propuesta) frente a "mil minutos" (palabra,
evidencia) clasifica `no_verificable` también dentro de la orquestación real de
autoestudio, la dirección exacta que quedaba rota tras T095.

**Decisión contractual resuelta (T097, ronda 2026-09-12f, vía `/speckit-clarify`) —
sustituye la "decisión pendiente" registrada por T096**: `spec.md` (Key Entities,
`GroundingVerificationResult`, línea ~444 antes de esta ronda) decía, cita exacta del
texto **anterior** (ya sustituido en `spec.md`, conservado aquí como registro
histórico): *""Parcialmente fundamentada" significa que al menos una afirmación
carece de soporte en la evidencia recuperada, sin que ninguna la contradiga
activamente; "conflictiva" significa que al menos una afirmación es contradicha por
la evidencia recuperada o por otra fuente autorizada (Escenario D)."*

La anotación `(Escenario D)` era sintácticamente ambigua: podía acotar solo el segundo
disyunto ("por otra fuente autorizada") o la cláusula completa ("contradicha por la
evidencia recuperada **o** por otra fuente autorizada"). Resuelto en `spec.md` §
Clarifications, Session 2026-09-12: **acota todo el disyunto** — `conflictiva` se
reserva exclusivamente al conflicto pendiente y registrado entre fuentes de la User
Story 6 (`Escenario D`, `quickstart-validation-evidence.md:20`,
`quickstart.md:60` — dos materiales **activos y distintos** con afirmaciones
incompatibles), coherente con `research.md §7` (arriba: *"fragmentos de documentos
**distintos**... se marcan como conflictivos y generan un `MaterialConflictRecord`"*)
y con el código ya implementado y probado
(`GroundingVerifierAgent._touches_unreviewed_conflict`, exige un
`MaterialConflictRecord` con `review_status = "pending_review"`, nunca se dispara por
un único fragmento). Una contradicción entre una propuesta y un único fragmento de
evidencia NO constituye un conflicto entre fuentes y NO debe generar un
`MaterialConflictRecord` sintético.

**Los cinco veredictos, condiciones y precedencia (definición final, `spec.md` Key
Entities)**:

| Veredicto | Condición | Precedencia |
|---|---|---|
| `conflictiva` | La evidencia utilizada toca un `MaterialConflictRecord` con `review_status = "pending_review"` (conflicto entre dos o más fuentes autorizadas, User Story 6) | **Máxima** — se evalúa primero (`_touches_unreviewed_conflict`, antes de clasificar ninguna afirmación); anula cualquier otro resultado, incluso si alguna afirmación aislada parecería soportada |
| `fundamentada` | Sin conflicto pendiente; todas las afirmaciones están soportadas | Se evalúa solo si no hay conflicto pendiente |
| `parcialmente_fundamentada` | Sin conflicto pendiente; al menos una afirmación soportada y al menos una no soportada (sin respaldo o contradicha por una fuente individual) | ídem |
| `no_fundamentada` | Sin conflicto pendiente; ninguna afirmación soportada, y al menos una carece de respaldo o contradice una fuente individual (`_CONTRADICTED_OUTCOME` en al menos una, research.md §11) | ídem |
| `no_verificable` | Sin conflicto pendiente; ninguna afirmación soportada, evidencia vacía con conocimiento general permitido, o ninguna afirmación no soportada tiene una diferencia activamente interpretada (todas `_UNVERIFIABLE_OUTCOME`, research.md §11) | ídem |

Un conflicto **ya revisado** (`review_status` distinto de `"pending_review"`) MUST NOT
seguir forzando `conflictiva` — `_touches_unreviewed_conflict` ya filtra por
`review_status == "pending_review"` (FR-022b: "pendiente de revisión", no "revisado
alguna vez"); comportamiento ya implementado y confirmado por
`test_reviewed_conflict_no_longer_forces_conflictiva` (ver más abajo, reutilizada, no
nueva).

**Código de producción**: no requirió ningún cambio — `GroundingVerifierAgent`
(T093-T096) ya implementaba exactamente esta semántica; la clarificación formaliza en
`spec.md`/`contracts/material-retriever-agent.md` lo que el código ya hacía y las
pruebas ya confirmaban, cerrando la ambigüedad de redacción sin alterar
comportamiento.

## 12. Presupuesto temporal enforzable frente a trabajo bloqueante (FR-017/FR-018, Principio IX) — estabilización 2026-09-10

**Hallazgo de partida (H10) — distinción necesaria entre dos mecanismos de tiempo
distintos que la auditoría previa no separaba con claridad**:

1. **`time_budget_ms`** (parámetro propio de `MaterialRetrieverAgent.execute`, definido en
   `contracts/material-retriever-agent.md`): un presupuesto **blando**, autocomprobado
   *después* de completar el trabajo — el propio contrato ya documenta que agotarlo
   produce `status = "ok"` con resultado parcial y una entrada en `warnings`, nunca un
   fallo (Edge Case, sección "Reglas" de ese contrato). **Este mecanismo funciona tal
   como está documentado — no es el hallazgo.**
2. **`request.deadline_ms`** (envoltura genérica de la Feature 001,
   `run_with_deadline`/`asyncio.wait_for`, `cancellation.py`): un límite **duro**,
   pensado para convertir cualquier agente que exceda su `timeout_ms` de contrato en
   `status = "timeout"` y activar la degradación de agencia (`fallback_step`). **Este es
   el mecanismo que no funciona como se pretende** para `MaterialRetrieverAgent`: los
   embeddings (`sentence-transformers`) y la consulta al índice (ChromaDB) dentro de
   `execute()` son llamadas síncronas y bloqueantes, sin ningún `await` intermedio;
   `asyncio.wait_for` solo puede cancelar en un punto de suspensión, así que un
   `deadline_ms` menor que la duración real de esas llamadas no las interrumpe — la
   ejecución corre hasta el final igualmente y solo entonces se comprueba
   `time_budget_ms` (mecanismo 1), demasiado tarde para el propósito del mecanismo 2.

**Decision — mover el trabajo bloqueante fuera del hilo del bucle de eventos, con
contrapresión explícita, sin introducir un servicio ni una cola nueva (Principio
XI)** — **implementada en T086, 2026-09-13**: ejecutar la llamada a
`self._embedder.embed(...)` y a `self._store.query(...)` a través de
`BoundedBlockingWorker.run(...)`
(`src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py`) en vez de
invocarlas directamente o mediante `asyncio.to_thread(...)` puro. La corrección de
T091 más abajo en esta misma sección ya documentaba por qué `asyncio.to_thread` por sí
solo (que despacha al *executor* por defecto del proceso) no basta: su bounded worker
count no acota su cola de trabajo pendiente. `BoundedBlockingWorker` introduce el
mismo punto de suspensión que faltaba (`asyncio.wait_for` ya puede entregar la
cancelación mientras el hilo auxiliar sigue corriendo) MÁS un control de admisión
explícito — ver §12.1 para el diseño completo, ahora implementado.

**Corrección respecto a la primera ronda — no ocultar la cancelación**: el diseño
anterior proponía que `execute()` capturase `asyncio.CancelledError` para devolver el
resultado parcial ya calculado "en vez de perderlo". Esto es exactamente lo que MUST
NOT hacerse: convertiría un `deadline_ms` agotado en una respuesta `status = "ok"`,
evitando la degradación de agencia (`fallback_step`) que `run_with_deadline` ya
implementa correctamente hoy para cualquier otro agente. Se retira ese punto del
diseño. En su lugar: si `asyncio.wait_for` cancela la espera al agotarse
`deadline_ms`, `MaterialRetrieverAgent.execute` MUST dejar que `asyncio.CancelledError`
se propague sin capturarla para fabricar un resultado — `run_with_deadline`
(`cancellation.py`, Feature 001, sin cambios) es quien ya traduce ese caso en
`status = "timeout"`, tal como hace para cualquier otro agente. El único rol de
`BoundedBlockingWorker.run(...)` aquí es **habilitar** que esa cancelación exterior
pueda efectivamente interrumpir la espera — no absorberla dentro del agente. La
cancelación de este `await` en concreto es inmediata (`asyncio.wrap_future` cancela su
`Future` envoltorio de forma síncrona y solo intenta, de mejor esfuerzo, cancelar el
`concurrent.futures.Future` subyacente después — un no-op una vez que el hilo worker
ya empezó a ejecutarlo) — nunca espera a que el hilo bloqueado termine para que
`run_with_deadline` pueda producir el timeout.

**Qué operaciones salen del bucle de eventos**: únicamente
`self._embedder.embed([query_text])` y `self._store.query(vector, filters, k)` —
ambas de solo lectura, sin escritura a base de datos ni al índice. El resto de
`execute()` (consulta de `MaterialFragment` por `id`, filtrado de autorización/
vigencia, detección de conflictos, registro del intento bloqueado) sigue ejecutándose
en el hilo principal del bucle de eventos, sin cambios.

**La sesión SQLAlchemy no se comparte entre hilos**: `self._db` (la sesión SQLAlchemy
de la petición) MUST NOT usarse dentro del hilo worker de `BoundedBlockingWorker` — ni
`self._embedder.embed(...)` ni `self._store.query(...)` la referencian (verificado por
inspección, y comprobado en pruebas mediante instrumentación de identidad de hilo —
`tests/integration/test_material_retrieval_h10_admission_integration.py::
test_sql_access_stays_on_the_event_loop_thread_never_the_worker`, T086), y la
implementación preserva esa separación: cualquier acceso a `self._db` (la consulta de
`MaterialFragment`, el registro de conflictos) sigue ocurriendo en el hilo principal,
antes o después del `await self._worker.run(...)`, nunca dentro de él — SQLAlchemy
`Session` no es segura para compartir entre hilos concurrentes.

**Una ejecución cancelada no publica resultados ni escribe tarde**: dado que las dos
llamadas movidas a un hilo son de solo lectura (no escriben en `self._db` ni en el
índice), una cancelación no deja ninguna escritura a medias que revertir — el valor de
retorno del hilo, si la tarea exterior ya fue cancelada, simplemente se descarta (nadie
vuelve a leerlo ni lo persiste; verificado en
`test_late_embed_completion_does_not_trigger_a_later_query`/`test_late_query_
completion_triggers_no_sql_conflicts_traces_or_late_results`, T086). Esta propiedad es
específica de que el trabajo movido al worker en este agente concreto es puramente de
lectura; MUST documentarse como una condición explícita para reutilizar este mismo
patrón en un agente que sí escriba (no es una garantía general de
`BoundedBlockingWorker`/`asyncio.to_thread`).

**Límite documentado sobre el trabajo ya iniciado**: `BoundedBlockingWorker` permite
que `wait_for` deje de **esperar** al hilo bloqueado y devuelva el control (y por tanto
que el turno se degrade a tiempo), pero **no mata** el hilo del sistema operativo
subyacente — el trabajo de embeddings/búsqueda sigue consumiendo CPU en segundo plano
hasta que termina por sí solo. Esto es degradación controlada del turno (Principio IX:
el turno no se bloquea más allá de su límite), no cancelación real de trabajo de CPU ya
iniciado.

**Corrección (T091, 2026-09-13) — el `ThreadPoolExecutor` por defecto NO aporta
contrapresión frente a una ráfaga sostenida**: la afirmación de esta sección en la
ronda anterior era incorrecta y queda retractada aquí. Lo único que
`min(32, os.cpu_count() + 4)` acota es el número de **hilos worker** simultáneos del
*executor* por defecto del proceso — no acota su **cola de trabajo pendiente**
(`ThreadPoolExecutor._work_queue`, un `queue.SimpleQueue` sin límite de tamaño en la
librería estándar). Bajo una ráfaga sostenida de turnos que agotan su `deadline_ms`
mientras el trabajo de `embed`/`query` sigue en marcha, `asyncio.to_thread` seguirá
aceptando y encolando **cada** nueva llamada sin bloquear a quien la emite ni
rechazarla — no "esperará un hilo libre antes de aceptar el trabajo" como decía la
versión anterior de esta sección, sino que la aceptará inmediatamente y la apilará en
una cola que crece sin límite mientras la tasa de llegada supere a la de finalización.
`asyncio.to_thread` por sí solo, por tanto, **no** es un mecanismo de contrapresión
suficiente frente a esa ráfaga — es exactamente lo que permite que el `deadline_ms`
de un turno concreto deje de esperar (research.md, más arriba en esta misma sección),
pero no impide que el número de trabajos pendientes/en curso crezca sin límite
explícito alguno, lo cual contradice el requisito de límites explícitos de recursos
del Principio IX si se deja así. Además, cancelar la espera (`await`) de un turno no
libera ninguna capacidad del pool: el trabajo ya encolado o ya en ejecución en un hilo
sigue consumiendo un slot del pool hasta que termina por sí solo, cancelado o no desde
el punto de vista del `await` — visible también más arriba ("no mata el hilo del
sistema operativo subyacente"). T086 (implementada, 2026-09-13) introduce por tanto un
límite explícito de admisión propio, no dependiente únicamente del límite de hilos de
ningún *executor* por defecto — ver §12.1 para el diseño implementado.

**Qué operaciones de inicialización siguen bloqueando antes del primer `await`**:
`ChromaVectorStore.__init__` (lectura síncrona de `index_version.json`) y la carga
perezosa del modelo de `sentence-transformers` (si `SentenceTransformerEmbeddingAdapter`
la difiere a la primera llamada a `.embed(...)`, esa primera carga ocurre **dentro**
del turno que la dispare, no antes) siguen siendo síncronas y bloqueantes en el hilo
principal en el momento de construir `MaterialRetrieverAgent(db)` — antes de que exista
ningún `await` que permita cancelarlas. Esto queda fuera del alcance del cambio de esta
ronda (mover solo `embed`/`query`, ya suficientemente costosas por turno, no la
construcción del agente) — se documenta como límite conocido, no se extiende
`asyncio.to_thread` a la inicialización sin evidencia de que sea necesario.

**Pruebas requeridas** (no solo un timeout aislado): (a) trabajo lento controlado (un
doble de `EmbeddingAdapter`/`VectorStore` con una demora determinista, no un modelo
real) con `deadline_ms` menor que esa demora — confirmar `status = "timeout"`
propagado por `run_with_deadline`, no `status = "ok"`; (b) la misma configuración pero
con un `deadline_ms` mayor (presupuesto positivo) — confirmar que el turno completa con
normalidad; (c) mientras la primera petición está en curso y a punto de expirar, una
**segunda** petición independiente (turno o consulta directa) MUST seguir progresando
con normalidad — el bucle de eventos no debe quedar bloqueado por la primera; (d) tras
cancelar la primera por timeout, dejar que el trabajo abandonado termine en segundo
plano y confirmar que no publica ningún resultado tardío, no escribe nada, y no afecta
a la segunda petición ya completada.

**Evidencia T091 (reproducción previa a T086, 2026-09-13)** —
`tests/failure/test_material_retrieval_h10_reproduction.py` (dos reproducciones
obligatorias, contra el `MaterialRetrieverAgent`/`run_with_deadline` reales, dobles
`EmbeddingAdapter`/`VectorStore` bloqueantes coordinados por `threading.Event`, nunca
un `sleep` frágil) confirma exactamente el defecto de esta sección: con
`time_budget_ms=60000` (nunca alcanzado) y `request.deadline_ms` corto, tanto un
`embed()` bloqueante (H10.A) como un `query()` bloqueante (H10.B) hacen que
`run_with_deadline` devuelva `status = "ok"` en vez de `status = "timeout"` — 2/2
fallan tal como exige (a) más arriba; el contraste positivo (mismos dobles, liberados
muy por debajo de un `deadline_ms` de 5000ms) devuelve `status = "ok"` sin
`AGENT_TIMEOUT`, conservando el fragmento autorizado y rechazando uno fuera de
`course_id` (T098) — cubre (b). (c) se documenta por separado, como experimento no
obligatorio (no estable de forma garantizada en el estado posterior a T086, ver el
archivo para el razonamiento completo), en
`tests/failure/test_material_retrieval_h10_event_loop_responsiveness_experiment.py`:
contra el código actual, una segunda corutina independiente y breve, programada
mientras `embed()` bloquea, queda demostrablemente retrasada hasta que el bloqueo
termina — no por una carrera de tiempos, sino porque el bucle de eventos de asyncio es
cooperativo y de un solo hilo: una tarea sin ningún punto de suspensión interno lo
monopoliza durante toda su duración. (d) queda fuera del alcance de T091 (no hay
trabajo real que cancelar hasta que T086 mueva las llamadas a un hilo) — pendiente
para la evidencia de T086. Las tres reproducciones eran deliberadamente rojas en T091;
T086 las deja en verde sin modificar ninguna de sus aserciones (ver evidencia
siguiente) — incluida, como bonus no exigido, la del experimento (c): con el trabajo
ya genuinamente suspendido en un hilo worker, la segunda corutina progresa primero de
forma estable en las ejecuciones observadas, aunque esta última sigue documentada como
no-obligatoria (research.md no la trata como garantía dura, a diferencia de (a)/(b)).

**Evidencia T086 (implementación, 2026-09-13)** — `MaterialRetrieverAgent.execute`/
`_run_widening_search` ahora son `await`-conscientes en las dos llamadas bloqueantes,
a través de `BoundedBlockingWorker` (§12.1). Ejecutando, sin modificar ninguna
aserción, los mismos dos archivos de T091: las 4 pruebas (H10.A, H10.B, el contraste
positivo, y el experimento de capacidad de respuesta) quedan en verde, estable en 5
ejecuciones consecutivas de cada archivo. Pruebas nuevas añadidas por T086 (todas
coordinadas por `threading.Event`, nunca `sleep` como mecanismo principal, con
timeouts de seguridad y liberación en `finally`):
`tests/unit/test_blocking_retrieval_worker.py` (6 pruebas: ráfaga nunca excede la
capacidad inyectada, una espera de admisión expirada nunca se envía después al
executor, cancelar trabajo en curso no libera el cupo antes de tiempo, el cupo se
recupera tras una finalización normal, el worker es reutilizable entre dos bucles de
eventos sucesivos —`asyncio.run()` × 2— y la capacidad sigue exigiéndose correctamente
tras ese cambio de bucle) y
`tests/integration/test_material_retrieval_h10_admission_integration.py` (4 pruebas:
un `embed()` tardío no dispara un `query()` posterior al timeout, un `query()` tardío
no produce SQL/conflictos/trazas ni resultados tardíos, el acceso SQL permanece en el
hilo del bucle de eventos mientras `embed`/`query` corren en un hilo distinto
—identidades de hilo registradas explícitamente, nunca inferidas—, y el bucle de
ampliación de T085 sigue emitiendo varias consultas `await`-eadas al store dentro de
una misma petición válida). Las 10 pruebas nuevas están en verde; las 4 de T091, en
verde sin cambios. Regresión: `tests/integration/test_material_retrieval_h08_
reproduction.py`, `test_material_retrieval_widening_structural.py`,
`test_material_retrieval_course_isolation.py`,
`test_self_study_pending_fragment_revalidation.py`,
`tests/unit/test_material_fragment_revalidation.py` (evidencia T085/T090/T098/T099):
46/46 en verde, sin regresión. Suite completa: `PYTHONPATH=src uv run pytest tests/ -q
-m "not ollama and not speech"` → 385 passed, 1 deselected, 0 failed (antes de T086:
372 passed, 3 failed —las reproducciones de T091—, 1 deselected; +10 pruebas nuevas,
+3 que pasan de rojo a verde, 0 regresiones). Ruff: 0 errores nuevos en los archivos
modificados/creados; `uv run ruff check src/ tests/ --statistics` → 49 errores,
idéntico al recuento de referencia heredado (45 E501, 2 F401, 1 F541, 1 F841).

### 12.1 Diseño de contrapresión para T086 — implementado, 2026-09-13

**Nota de cierre (T100, 2026-09-13)**: una revisión posterior a esta ronda encontró
tres fisuras estructurales en el mecanismo de admisión aquí descrito
(`_LoopScopedSemaphore` multiplicaba la capacidad al cambiar de bucle de eventos en
vez de compartirla realmente; `run()` podía perder un permiso si `executor.submit()`
fallaba; `default_blocking_retrieval_worker()` no tenía exclusión mutua). **T086 NO
se declara efectivamente cerrada hasta T100** (§12.2 más abajo), que sustituye
`_LoopScopedSemaphore` por `_ProcessWideAdmission` y corrige las otras dos fisuras.
Esta subsección (§12.1) se conserva sin reescribir como evidencia histórica de lo que
T086 implementó y validó en su momento — las pruebas que siguen citándose aquí
siguen existiendo y en verde, pero ya no describen el mecanismo de admisión
actualmente en uso; ver §12.2 para el diseño vigente.

Corregida la premisa de más arriba (el *executor* por defecto no aporta contrapresión
real), T086 implementa un control de admisión explícito, propio del agente, además de
mover `embed`/`query` a un hilo:
`BoundedBlockingWorker`/`_LoopScopedSemaphore`
(`src/oralia/infrastructure/concurrency/blocking_retrieval_worker.py`),
inyectado en `MaterialRetrieverAgent.__init__` (`blocking_retrieval_worker`, parámetro
interno — nunca expuesto en `MaterialQueryInput`/la API HTTP) y compartido por
defecto vía un singleton de proceso (`default_blocking_retrieval_worker()`), porque
producción construye una instancia nueva de `MaterialRetrieverAgent` por petición
(`materials.py`, `self_study_agency_composer.py`) — un semáforo privado por instancia
de agente no limitaría nada entre peticiones concurrentes.

- **Límite de capacidad elegido — conservador, no medido**: `DEFAULT_BLOCKING_
  RETRIEVAL_CAPACITY = 4`, una constante con nombre en el mismo módulo. **Corrección
  respecto a la ronda anterior de esta sección**: aquí se afirmaba que el valor MUST
  derivarse en parte de un "coste por embedding/consulta medido en T090" — esto es
  incorrecto y queda retractado. T090 (research.md §14.2) midió únicamente la
  distribución de `relevance_score` (positivos 0.6212–0.8130, negativos 0.0583–0.2162)
  para calibrar el umbral de pertinencia — nunca latencia, CPU ni memoria de
  `embed`/`query`; no existe ninguna medición de coste temporal/de recursos de esas
  llamadas en este proyecto. `4` es, honestamente, un techo de seguridad elegido para
  que exista un límite explícito en absoluto (Principio IX), no un valor calibrado —
  MUST recalibrarse con métricas reales de despliegue (volumen de peticiones
  concurrentes, latencia real de `embed`/`query` bajo el modelo/almacén del proyecto
  en producción) antes de tratarse como definitivo. Queda registrada aquí la necesidad
  de esa calibración futura, no resuelta en esta ronda.
- **Ejecutor dedicado Y control de admisión, ambos**: `BoundedBlockingWorker` posee su
  propio `ThreadPoolExecutor` (`max_workers=capacity`), dedicado — nunca el *executor*
  por defecto del bucle de eventos (`asyncio.to_thread` no se usa; esto también
  cumple "no cambiar el *executor* predeterminado global ni interferir con otros usos
  de `asyncio.to_thread`") — combinado con un semáforo de admisión de ESE MISMO
  tamaño, adquirido ANTES de enviar el trabajo al *executor*. Esto es lo que cierra la
  fisura documentada más arriba: como nunca se envían más de `capacity` llamadas a la
  vez, la cola interna (no acotada) del *executor* dedicado nunca llega a usarse en la
  práctica — el semáforo es la contrapresión real, el *executor* dedicado es el
  aislamiento (esta ruta no compite por hilos con ningún otro uso de `asyncio.to_thread`
  en el proceso).
- **Momento exacto de adquisición y liberación**: el semáforo se adquiere en
  `BoundedBlockingWorker.run()`, ANTES de `self._executor.submit(func, *args)` — una
  petición cuyo `deadline_ms` expira mientras espera esta adquisición nunca llega a
  `submit()` (verificado en
  `test_expired_admission_wait_never_submits_to_executor`). La liberación está atada a
  la finalización REAL del `concurrent.futures.Future` devuelto por `submit()`
  (`cf_future.add_done_callback(_release)`), nunca al `finally` de la corutina que
  hace `await` — un `await` cancelado no libera nada por sí mismo (verificado en
  `test_cancelling_in_flight_work_does_not_release_capacity_early`); solo cuando el
  hilo worker realmente termina (normal, con excepción, o genuinamente cancelado antes
  de arrancar) se libera el cupo, marshalled de vuelta al bucle de eventos correcto
  vía `loop.call_soon_threadsafe(semaphore.release)` (la liberación puede dispararse
  desde el hilo worker, nunca asumir que es el hilo del bucle de eventos).
- **Cancelar esperando admisión, frente a cancelar trabajo ya iniciado**: cancelar
  mientras se espera el semáforo (`await self._admission.acquire()` aún no ha
  retornado) simplemente interrumpe esa espera — `asyncio.Semaphore.acquire()` retira
  su propio waiter de la cola al cancelarse, sin dejar ninguna adquisición fantasma;
  el trabajo nunca se envía al *executor* (ver arriba). Cancelar mientras el trabajo
  YA se está ejecutando en el hilo worker (`await asyncio.wrap_future(cf_future,
  loop=loop)`) propaga la cancelación al llamador de inmediato — `wrap_future` cancela
  su `Future` envoltorio de forma síncrona y solo intenta, de mejor esfuerzo, cancelar
  el `concurrent.futures.Future` subyacente (`cf_future.cancel()`, un no-op una vez
  que el hilo ya empezó a ejecutarlo) — sin esperar a que el hilo termine; el cupo
  sigue retenido hasta que ese hilo realmente termina por sí solo.
- **Ninguna hebra nueva por petición; ningún resultado tardío se publica**: el
  *executor* dedicado se reutiliza entre todas las llamadas (nunca un
  `threading.Thread` por petición/operación); `embed`/`query` son de solo lectura
  (documentado más arriba), así que un resultado que termina después de que su turno
  ya expiró simplemente se descarta — no hay escritura tardía que evitar (verificado
  en `test_late_embed_completion_does_not_trigger_a_later_query`/`test_late_query_
  completion_triggers_no_sql_conflicts_traces_or_late_results`); esta propiedad sigue
  siendo específica del carácter de solo lectura de este agente, no una garantía
  general de `BoundedBlockingWorker` reutilizable sin revisar en un agente que sí
  escriba. `self._db` sigue sin usarse dentro de ningún hilo worker (verificado por
  identidad de hilo en `test_sql_access_stays_on_the_event_loop_thread_never_the_worker`).
- **Compatibilidad entre distintos bucles de eventos**: `_LoopScopedSemaphore` NO
  construye un `asyncio.Semaphore` a nivel de módulo/import — lo crea perezosamente la
  primera vez que se usa desde el bucle de eventos EN CURSO, y lo reconstruye si el
  bucle en curso ha cambiado desde la última vez (un proceso real nunca cambia de
  bucle con trabajo admitido pendiente; solo ocurre entre ejecuciones de prueba
  independientes, cada una responsable de liberar sus propios dobles antes de acabar).
  Verificado con dos llamadas `asyncio.run()` sucesivas sobre la MISMA instancia de
  `BoundedBlockingWorker` — sin error de "bound to a different event loop" — en
  `test_worker_reusable_across_successive_event_loops` y, además, confirmando que la
  capacidad se sigue exigiendo correctamente tras el cambio de bucle, en
  `test_capacity_still_enforced_after_rebinding_to_a_new_event_loop`.
- **Cómo se observa en pruebas que una ráfaga no crea una cola ilimitada**: lanzar N
  llamadas concurrentes (`asyncio.create_task`) muy por encima de una capacidad
  inyectada pequeña, con dobles bloqueantes coordinados por `threading.Event`
  (contador instrumentado, incrementado al entrar al doble, decrementado al salir),
  esperando —siempre vía `loop.run_in_executor`, nunca una espera bloqueante directa
  sobre el hilo del bucle de eventos, que estancaría a las propias tareas que se
  quiere observar— a que se alcance la capacidad, y confirmando entonces (de forma
  estructural, no probabilística: el resto de solicitudes solo puede seguir esperando
  el mismo semáforo) que el máximo observado nunca la supera —
  `test_admission_never_exceeds_injected_capacity_under_burst`.
- **Esperar a que el trabajo auxiliar termine, para no dejar hilos vivos entre
  pruebas**: `BoundedBlockingWorker.shutdown(wait=True)` envuelve
  `ThreadPoolExecutor.shutdown(wait=True)` — cada prueba libera sus dobles bloqueantes
  en un bloque `finally` (incluso si una aserción falla antes) y después llama a
  `shutdown(wait=True)` sobre su propia instancia de worker inyectada (nunca sobre el
  singleton de proceso), de modo que la suite nunca termina con hilos del *executor*
  dedicado de una prueba concreta todavía en ejecución.

**Consumidores**: mismo agente que en H03 (003 y, previsiblemente, 004).

### 12.2 Corrección de convergencia T100 — admisión process-wide real, 2026-09-13

**Contexto**: una revisión posterior a T086 encontró que `_LoopScopedSemaphore`
(§12.1) no era realmente process-wide pese a describirse como tal — pasaba las
pruebas de T086 (que solo ejercitaban bucles de eventos *sucesivos*, nunca dos
bucles *simultáneos* en hilos distintos) pero fallaba exactamente ese caso, además
de dos fisuras adicionales (fuga de permiso, singleton sin exclusión mutua). T100
sustituye el mecanismo de admisión — `MaterialRetrieverAgent` no se modifica, T085/
T098/T099 no se tocan, `run_with_deadline` no se modifica.

**R1 — causa confirmada**: `_LoopScopedSemaphore.acquire()` comparaba
`self._loop is not loop` y, si eran distintos, reconstruía un `asyncio.Semaphore`
COMPLETAMENTE NUEVO y lleno (`asyncio.Semaphore(self._capacity)`), sin comprobar si
el semáforo anterior tenía permisos pendientes de liberar. Reproducido: con
`capacity=1`, un bucle A (hilo propio) ocupa el único permiso con un doble
bloqueante; un bucle B (hilo propio, distinto) llama a `worker.run(...)` — con un
espía sobre `worker._executor.submit`, se confirma que `submit()` SÍ se invoca para
B mientras A sigue bloqueado, en vez de esperar. La ejecución real de B queda además
enmascarada por el propio `ThreadPoolExecutor` (`max_workers == capacity` siempre),
que jamás ejecuta más de `capacity` operaciones a la vez con independencia de cuántas
fueron admitidas — el daño real y observable de R1 no es "más ejecuciones
concurrentes de las debidas" sino "más envíos (`submit()`) de los debidos,
alimentando la cola interna del *executor* que el diseño de §12.1 afirmaba no usar
nunca" — de ahí que las pruebas de reproducción (A/C, más abajo) instrumenten
`submit()` directamente en vez de inferir el defecto a partir de la ejecución.

**R2 — causa confirmada**: `run()` llamaba `self._executor.submit(func, *args)`
inmediatamente después de adquirir el semáforo, sin ningún `try`/`except` — si
`submit()` lanzaba (p. ej. `RuntimeError: cannot schedule new futures after
shutdown`), no existía ningún `concurrent.futures.Future` sobre el que enganchar el
callback de liberación, así que el permiso quedaba perdido para siempre. Reproducido
literalmente con los pasos dados: `capacity=1` → `worker.shutdown()` → primera
`run()` lanza `RuntimeError` desde `submit()` → segunda `run()` queda bloqueada
esperando un permiso que nadie liberará jamás (confirmado con un
`asyncio.wait_for(..., timeout=3)` que expira).

**R3 — causa confirmada**: `default_blocking_retrieval_worker()` hacía
`if _default_worker is None: _default_worker = BoundedBlockingWorker()` sin ningún
`threading.Lock` — dos hilos que evalúen la condición como verdadera antes de que
cualquiera de los dos asigne la variable global pueden, cada uno, construir y quedarse
con una referencia a una instancia distinta, partiendo la capacidad compartida en dos
mitades independientes. (No se logró forzar de manera fiable esta carrera concreta en
una prueba de duración razonable — el intervalo entre comprobar y asignar es
demasiado estrecho bajo el GIL de CPython para un test determinista corto — pero la
ausencia de exclusión mutua es una fisura real y verificable por inspección del
código; la corrección aplica el patrón estándar de *double-checked locking*
independientemente de si la carrera se manifestó en la sesión de pruebas.)

**Diseño de la admisión process-wide** —
`_ProcessWideAdmission`/`_Waiter`/`_resolve_waiter`/`_reject_waiter`
(`blocking_retrieval_worker.py`), sustituye por completo a `_LoopScopedSemaphore`
(retirada, no conservada "por minimizar el diff" — ver instrucción de esta ronda):
un único pool de `capacity` permisos (`_available: int`, `_waiters: deque[_Waiter]`,
`_closed: bool`), protegido por un único `threading.Lock`, compartido de verdad —
nunca reconstruido ni reasignado al cambiar de bucle de eventos. El `Lock` solo se
mantiene durante operaciones de contabilidad breves y no bloqueantes (append/pop de
deque, incrementar/decrementar un entero) — jamás durante un `await` ni una espera
bloqueante: la espera real de un permiso es siempre `await fut` sobre un
`asyncio.Future` propio del bucle que llama, nunca `threading.Semaphore.acquire()`
(cumple la propiedad 12 de esta ronda).

**Invariante**: en todo instante, cada uno de los `capacity` permisos está en
exactamente uno de tres estados — libre (contado en `_available`), en manos de un
trabajo admitido (responsabilidad de quien llamó `acquire()`, hasta que llame
`release()`), o en tránsito hacia un waiter concreto (`waiter.consumed = True`, entre
que `_grant_next_locked` se lo entrega y ese waiter o bien retorna con normalidad o
bien descubre, bajo el mismo lock, que debe reenviarlo). Ningún camino de código fuera
de `_grant_next_locked`/el manejador de cancelación de `acquire()` crea o destruye un
permiso, así que el total se conserva por construcción — nunca hay más ni menos de
`capacity` permisos en el sistema.

**Tratamiento de las tres carreras exigidas** en la entrega de un permiso liberado a
un waiter (todas resueltas bajo el mismo `_lock`, así que como mucho un lado "gana"):
- *Cancelación del waiter*: `acquire()` captura `asyncio.CancelledError` y, bajo el
  lock, comprueba `waiter.consumed` — si un `release()` ya se lo había entregado (o
  estaba en ello) antes de que la cancelación llegara, ese permiso nunca llegó a
  usarse y se reenvía (`_grant_next_locked()` de nuevo) en vez de perderse; si aún no
  se le había entregado nada, simplemente se retira de `_waiters` (con `deque.remove`
  protegido por `ValueError` para el caso en que un `release()` concurrente ya lo
  hubiera sacado de la cola en el instante anterior).
- *Cierre del bucle del waiter*: `_grant_next_locked()` intenta
  `waiter.loop.call_soon_threadsafe(_resolve_waiter, waiter)`; si el bucle ya está
  cerrado, esa llamada lanza `RuntimeError` — se deshace la marca `consumed` y se
  prueba con el siguiente waiter de la cola, sin perder el permiso. Si el cierre
  ocurre en la ventana exacta entre que `_resolve_waiter` se programa y se ejecuta,
  `_resolve_waiter` comprueba `waiter.fut.done()` antes de fijar el resultado — un
  `Future` ya cancelado no se toca, y es el propio manejador de cancelación de
  `acquire()` (arriba) quien recupera el permiso en ese caso.
- *Liberación desde el hilo worker*: `release()` es código plano, seguro para
  cualquier hilo (solo toma `self._lock`) — no necesita `call_soon_threadsafe` a este
  nivel; solo la entrega final a un waiter concreto se marshalla, vía
  `call_soon_threadsafe`, al bucle específico de ESE waiter.

**Fallo de `executor.submit()` (R2, corregido)**: `run()` ahora envuelve
`self._executor.submit(...)` en `try/except Exception: self._admission.release();
raise` — el permiso se devuelve inmediatamente, antes de propagar la excepción,
nunca después.

**`shutdown()` (propiedad 10)**: `_ProcessWideAdmission.close()` es idempotente
(una segunda llamada no hace nada y devuelve `[]`), marca `_closed = True` bajo el
lock, y devuelve los waiters que quedaran pendientes en ESE instante para que
`BoundedBlockingWorker.shutdown()` los rechace (`_reject_waiter`, mejor esfuerzo,
vía `call_soon_threadsafe`, ignorando un bucle ya cerrado). `acquire()` comprueba
`self._closed` como lo primero que hace, bajo el lock, antes de tocar
`_available`/`_waiters` — una llamada a `run()` posterior a `shutdown()` falla de
inmediato, sin adquirir ni filtrar ningún permiso.

**Singleton (R3, corregido)**: `default_blocking_retrieval_worker()` aplica
*double-checked locking* estándar con un `threading.Lock` a nivel de módulo — el
caso común (ya construido) nunca paga el coste del lock.

**Corrección adicional de esta ronda — la capacidad NO se deriva de ningún coste
medido**: la instrucción de esta ronda señaló, correctamente, que §12.1 ya contenía
esta misma corrección (T090 solo midió `relevance_score`, nunca coste); T100 no
cambia el valor (`DEFAULT_BLOCKING_RETRIEVAL_CAPACITY = 4`, sigue sin calibrar) ni
introduce una nueva afirmación de coste — se deja constancia aquí de que la
verificación de esta ronda confirmó que §12.1 ya lo documentaba correctamente, sin
necesidad de una segunda corrección sobre el mismo punto.

**No se crean hilos, executores ni tareas permanentes por petición**: sigue
existiendo un único `ThreadPoolExecutor` dedicado por instancia de
`BoundedBlockingWorker` (sin cambios respecto a T086); `_ProcessWideAdmission` no
crea ningún hilo — solo usa el hilo que ya está ejecutando la corutina que llama
(`acquire`) o el hilo worker que completa el trabajo real (`release`).

**Pruebas — reproducción antes/después de cada defecto**
(`tests/unit/test_blocking_retrieval_worker_multiloop.py`, coordinación por
`threading.Event`/`_LoopThread` —bucles de eventos reales en hilos propios, no solo
`Task`s concurrentes en un único bucle—, nunca `sleep` como mecanismo principal —
salvo una ventana de equidad breve y acotada, documentada explícitamente donde
aparece, allí donde el propio `ThreadPoolExecutor` de tamaño fijo enmascararía el
síntoma observable de otro modo):
- **A + D** (`test_A_and_D_second_loop_blocked_until_first_loop_releases_then_completes`):
  contra el código previo a T100, **FALLA** — `submit()` para el bucle B se invoca
  mientras el bucle A sigue reteniendo el único permiso (`capacity=1`). En verde tras
  T100, y confirma además que B es admitido y completa correctamente al liberar A.
- **B** (`test_B_cancelling_other_loops_waiter_before_release_never_submits_later`):
  contra el código previo, **FALLA** — el `submit()` de B ya había ocurrido en el
  instante de cancelar su espera (la admisión previa nunca llegaba a esperar de
  verdad entre bucles distintos). En verde tras T100.
- **C** (`test_C_several_loops_never_exceed_capacity_structurally`): contra el código
  previo, **FALLA** — con `capacity=2` y 3 bucles, se observan 3 envíos admitidos
  simultáneamente (uno por bucle) en vez de 2. En verde tras T100.
- **E** (`test_E_permit_skips_a_waiter_whose_loop_already_closed`): contra el código
  previo, la suite entera falla en la recolección (`ImportError`: `_ProcessWideAdmission`
  no existe) — evidencia igualmente válida de que el mecanismo no existía. Probada
  directamente contra `_ProcessWideAdmission` (no a través de `BoundedBlockingWorker`,
  ya que el comportamiento bajo prueba es puramente de contabilidad de admisión): un
  waiter del bucle B, con su bucle cerrado mientras sigue en cola, es saltado sin
  perder el permiso, que llega correctamente al waiter del bucle C. En verde tras
  T100.
- **F1/F2** (`test_F1_submit_failure_returns_the_permit_immediately`/
  `test_F2_shutdown_makes_every_subsequent_call_fail_immediately`): contra el código
  previo, **FALLAN** ambas — reproducción literal de R2 (pasos dados en esta ronda):
  la segunda llamada a `run()` cuelga indefinidamente esperando el permiso perdido
  (detectado con `asyncio.wait_for(..., timeout)`, nunca una espera sin límite). En
  verde tras T100 — F1 además prueba, de forma estructural (adquiriendo el permiso
  directamente tras el fallo, sin colgarse), que no hubo fuga incluso cuando el fallo
  de `submit()` no viene de `shutdown()` propio del worker.
- **G** (`test_G_shutdown_is_idempotent`) y **H**
  (`test_H_default_worker_singleton_is_thread_safe`): en verde tanto antes como
  después de T100 — documentado honestamente, sin forzar una discrepancia artificial:
  `ThreadPoolExecutor.shutdown()` ya era idempotente por sí solo (G no es un
  diferenciador de la corrección, sino evidencia de que la propiedad se preserva); la
  carrera de R3 (H) es real y confirmada por inspección del código (ausencia de
  `Lock`), pero la ventana entre comprobar y asignar es demasiado estrecha bajo el
  GIL de CPython para forzarla de manera determinista en una prueba corta — la
  corrección (*double-checked locking*) se aplica igualmente, con independencia de
  que la carrera se haya podido observar empíricamente en esta sesión.

**Regresión**: 22/22 en verde
(`tests/unit/test_blocking_retrieval_worker.py` —6, sin modificar—,
`tests/unit/test_blocking_retrieval_worker_multiloop.py` —8, nuevas—,
`tests/integration/test_material_retrieval_h10_admission_integration.py` —4, sin
modificar—, los dos archivos de T091 —4, sin modificar—). T085/T098/T099: sin
regresión (ver tasks.md para el recuento exacto). Suite completa y Ruff: ver
tasks.md.

## 13. Lector con versión de índice obsoleta durante una reconstrucción concurrente (FR-016/FR-016a, Edge Case) — corregido en la segunda ronda de estabilización, 2026-09-10

**Hallazgo de partida (H09)**: `ChromaVectorStore` cachea `self._version` en su
constructor y no la refresca; `rebuild()` borra la colección de la versión anterior tras
mover el puntero. Una instancia construida antes del `rebuild()` y que consulta después
de que este haya terminado (incluido el borrado de la colección antigua) intentaría leer
una colección que ya no existe.

**Corrección respecto a la primera ronda**: la solución propuesta entonces (releer
`index_version.json` al empezar `query()`, en vez de en `__init__`) **reduce** la
ventana de la carrera pero no la elimina — sigue existiendo un intervalo, por pequeño
que sea, entre "resolver qué versión está vigente" y "obtener/leer la colección de esa
versión", durante el cual un `rebuild()` completo (incluido el borrado de la colección
antigua) podría intercalarse. Declarar esa solución "resuelta" porque el intervalo es
breve es exactamente el error que se pide corregir aquí — se retira esa afirmación.

**Decision — dos mecanismos combinados, ninguno de los dos nuevo en el sentido de
infraestructura (Principio XI), que juntos sí cierran la carrera**:

1. **Política acotada de retirada de colecciones antiguas**: `rebuild()` deja de
   borrar la colección de la versión inmediatamente anterior de forma síncrona —
   conserva **la versión actual y la inmediatamente anterior** (dos generaciones
   como máximo simultáneamente en disco) y solo borra la generación `N-2` cuando se
   completa el rebuild que produce `N`. Esto acota el crecimiento en disco (nunca más
   de dos colecciones vivas a la vez — límite explícito, Principio IX) y, en el caso
   normal (una sola reconstrucción concurrente con una consulta), garantiza que la
   colección que un lector resolvió sigue existiendo durante toda su lectura, incluso
   si el puntero ya avanzó.
2. **Reintento acotado con re-resolución en `query()`**: si, pese a lo anterior, la
   colección resuelta ya no existe (caso extremo: dos reconstrucciones completas
   suceden dentro de la vida de una única consulta — no impedido por el punto 1, solo
   hecho muy improbable), `query()` MUST capturar el error específico de "colección
   inexistente" de ChromaDB, releer `index_version.json` **de nuevo** (obteniendo la
   versión realmente vigente en ese instante) y reintentar contra ella — acotado a un
   número fijo de intentos (p. ej. 2). La lectura **MUST NOT** recrear silenciosamente
   una colección vacía con `get_or_create_collection` tras un fallo — recrear una
   colección borrada como si estuviera vacía serviría un resultado vacío
   indistinguible de "no hay materiales", violando FR-020 (repetibilidad) y
   ocultando el problema en vez de resolverlo mediante la versión realmente vigente.
   La versión que finalmente se usó (no la resuelta originalmente) es la que se
   reporta en `output.index_version` — satisface "la versión reportada corresponde a
   los resultados realmente leídos".
3. **Escritura atómica del puntero de versión**: `_version_file().write_text(...)`
   (escritura directa, no atómica en todos los sistemas de archivos) se sustituye por
   escribir a un archivo temporal en el mismo directorio y renombrarlo sobre
   `index_version.json` (`os.replace`, atómico en el mismo volumen tanto en POSIX
   como en Windows) — ningún lector puede observar un contenido a medio escribir del
   propio archivo de versión (distinto del contenido a medio escribir de una
   *colección*, ya cubierto por el patrón blue-green existente).

**Por qué no una infraestructura nueva**: no se introduce un servicio de coordinación,
un conteo de referencias distribuido, ni un locking de lectura — la combinación
"conservar una generación adicional" + "reintentar con la versión realmente vigente
tras un fallo puntual" resuelve el caso real con los mecanismos que el propio
`ChromaVectorStore` ya expone (`create_collection`/`delete_collection`/lectura de un
archivo JSON), coherente con Principio XI.

**Límite que sigue dependiendo de verificación empírica, no asumible**: si el cliente
persistente de ChromaDB, al ejecutar `.query()` sobre un objeto `Collection` cuya
colección subyacente fue borrada *durante* la propia llamada (no antes de obtenerla,
sino mientras lee), lanza un error reconocible o devuelve un resultado corrupto sin
error, es un comportamiento de la librería que esta feature no controla y que MUST
verificarse durante la implementación (no se puede confirmar por lectura de código —
requiere una prueba real contra ChromaDB). Si la librería no distingue ese caso de
forma limpia, el mecanismo de reintento del punto 2 no podría dispararse de forma
fiable para esa sub-variante — se documenta como riesgo a confirmar, no se declara
cerrado de antemano.

**Corrección de una afirmación no verificada (pedida explícitamente esta ronda)**:
*no* es cierto que `add()`/`delete()`/`rebuild()` estén "todos protegidos por
`IndexRebuildLock`". Verificado por inspección: únicamente
`rebuild_material_index.py` adquiere `index_rebuild_lock_service.acquire(db)` antes de
llamar a `store.rebuild(...)`. `ingest_material.py:203` llama a
`store.add(fragment.id, vector, {...})` **sin adquirir ningún lock** — un `ingest`
concurrente con un `rebuild` no está serializado por ningún mecanismo hoy: el
`rebuild` consulta `MaterialFragment` (SQL) en un instante dado y construye la nueva
colección a partir de esa foto; si un `ingest` concurrente inserta una fila nueva y
llama a `store.add(...)` después de que el `rebuild` ya tomó su foto pero antes de que
termine, el nuevo fragmento queda en la colección **antigua** (que el `rebuild` va a
sustituir/retirar) y ausente de la nueva — se perdería del índice hasta la siguiente
reconstrucción, sin ningún aviso. `ChromaVectorStore.delete()` está definida pero **no
tiene ningún invocador en el código actual** (confirmado por búsqueda) — riesgo
únicamente en abstracto, no en el comportamiento actual del sistema.

**Prueba pendiente explícita — intercalación coordinada (no simulación de estado)**:
a diferencia del test existente (que fija el estado del store directamente, sin
interleaving real), esta prueba MUST forzar la secuencia real: (1) un lector resuelve
la versión N; (2) se produce, de forma controlada (p. ej. mediante un doble de prueba
del cliente de Chroma, o coordinación explícita con un evento/barrera entre dos
hilos/tareas — no temporización basada en `sleep`), el cambio de puntero a N+1 y el
retiro de la generación N-1 según la política acotada del punto 1; (3) el lector
continúa y complete su lectura. Confirmar que sigue sirviendo los resultados de N (si
N aún no fue retirada, por la política acotada) o de la versión realmente vigente tras
el reintento (si N ya no existe), nunca un error no controlado ni una colección vacía
recreada en silencio.

**Prueba pendiente adicional (hallazgo nuevo de esta ronda)**: reproducir un `ingest`
concurrente con un `rebuild` (sin ningún lock compartido hoy) y confirmar si el
fragmento insertado durante el `rebuild` sobrevive, se pierde silenciosamente, o
produce un estado inconsistente — antes de decidir si `ingest_material.py` debe
adquirir el mismo `IndexRebuildLock` (opción más simple, serializa ambas operaciones)
o si el propio `rebuild` debe volver a consultar `MaterialFragment` justo antes del
swap final.

### 13.1 Evidencia T092 — reproducción con intercalación real, previa a T087, 2026-09-14

`chroma_store.py` NO se modifica en esta ronda. Nuevo archivo:
`tests/integration/test_material_index_rebuild_race_reproduction.py`.

**Punto exacto de intercalación**: una sola instancia lectora (`reader`) recibe una
sustitución de método a nivel de INSTANCIA (nunca de clase) sobre `_collection()` —
la sustitución señala "versión ya resuelta" (`self._version`, fijada desde la
construcción, sin tocarse) y bloquea hasta ser liberada; al liberarse, delega
exactamente en la `ChromaVectorStore._collection` original y sin modificar, capturada
una sola vez antes de instalar ninguna sustitución. Esto pausa la consulta real
EXACTAMENTE entre "qué colección se usará ya está decidido" y "obtener esa colección"
(`self._client.get_or_create_collection(...)`) — nunca antes (la versión ya estaría
resuelta igualmente) ni después (ya se habría leído). Coordinación:
`threading.Event` (`resolved`/`proceed`), nunca `sleep`; timeout de seguridad de 5s en
toda espera; hilos siempre unidos (`thread.join`) y eventos siempre liberados en un
bloque `finally`, incluso si una aserción falla antes.

**Estado de N/N+1/N+2 antes y después**:
- **Reproducción A**: antes — `writer` crea N=1 con `frag-v1`; `reader` se construye
  mientras N=1 vigente y cachea `self._version=1`. Durante la pausa, un `rebuilder`
  real ejecuta `rebuild([("frag-v2", ...)])`: crea N+1=2, mueve el puntero, y (código
  actual, sin corregir) borra N=1 de forma síncrona. Después — solo existe
  `material_fragments_v2` en disco; `material_fragments_v1` no existe hasta que el
  lector, al reanudarse, la recrea vacía vía `get_or_create_collection` (el defecto
  bajo prueba).
- **Reproducción B**: antes — igual que A. Durante la pausa, DOS reconstrucciones
  reales consecutivas: `rebuilder_1.rebuild(...)` → N+1=2 (borra N=1); una SEGUNDA
  instancia (`rebuilder_2`), que re-lee el puntero (confirmado `get_index_version()
  == "2"`), ejecuta `rebuild(...)` → N+2=3 (borra N+1=2). Después — solo existe
  `material_fragments_v3`; ni `material_fragments_v1` ni `_v2` existen hasta que el
  lector, al reanudarse, recrea `_v1` vacía (sigue apuntando a la versión 1 original,
  nunca re-resuelve).

**Resultado antes de T087, cada reproducción** (ejecutado 5 veces consecutivas, sin
flakiness en ninguna dirección):
- **Reproducción A**: **FALLA**, discriminante — `query()` devuelve `[]`
  (`reported_version` sigue siendo `"1"`), en vez de servir `frag-v1` (si N se
  hubiera conservado) o re-resolver y servir `frag-v2`. Causa confirmada por
  inspección y por el propio resultado: `_collection()` original, tras reanudarse,
  invoca `get_or_create_collection("material_fragments_v1", ...)` sobre una colección
  ya borrada por el `rebuild()` real — Chroma la recrea vacía en vez de señalar un
  error, `collection.count() == 0` y `query()` devuelve `[]`.
- **Reproducción B**: **FALLA**, discriminante — mismo síntoma (`query()` devuelve
  `[]`, `reported_version == "1"`) en vez de re-resolver y servir `frag-v3`
  (`reported_version == "3"`), pese a que N está genuinamente retirada incluso bajo
  la futura política de dos generaciones (dos reconstrucciones completas ocurrieron
  durante la pausa).
- Ninguna de las dos reproducciones deja escapar una excepción no controlada
  (`run.exception is None` se cumple en ambas incluso hoy) — el defecto observable es
  exclusivamente la recreación silenciosa, no un fallo ruidoso.

**Comportamiento empírico exacto de Chroma con un objeto de colección eliminado**
(prueba separada, no bloqueante — `test_empirical_chroma_behavior_on_a_deleted_
collection_object`, `chromadb==1.5.9` instalado en este entorno): tanto `.count()`
como `.query(...)` sobre un objeto `Collection` real cuya colección subyacente fue
borrada por OTRA instancia de cliente lanzan `chromadb.errors.NotFoundError` —
`count()`: `"Collection [<uuid>] does not exist."`; `query()`: `"Error getting
collection: Collection [<uuid>] does not exist."` — nunca un resultado corrupto o
silencioso en ninguno de los dos métodos. Esto resuelve el riesgo documentado más
arriba ("límite que sigue dependiendo de verificación empírica, no asumible"): T087
MUST capturar específicamente `chromadb.errors.NotFoundError` (no un `except
Exception` indiscriminado) alrededor del acceso a una colección ya resuelta —
suficientemente específico y estable en la versión instalada, aunque el mensaje
exacto incluye un UUID variable (no debe compararse por texto completo, solo por
tipo, o por un substring estable como `"does not exist"` si se necesita
diferenciarlo de otros `NotFoundError`).

### 13.2 Implementación T087 — cierre de H09 (2026-10-16)

`ChromaVectorStore.rebuild()` conserva después de cada swap las generaciones N y N-1
y retira exclusivamente N-2. La consulta obtiene una colección existente mediante
`get_collection`; nunca usa `get_or_create_collection` para una versión ya resuelta.
Si `get_collection`, `count` o `query` detectan que la generación desapareció, captura
exclusivamente `chromadb.errors.NotFoundError`, relee el puntero y realiza un segundo y
último intento. `self._version` queda en la generación realmente leída y por tanto es
la que se informa a los consumidores.

El puntero se escribe en un temporal del mismo directorio, se vacía y sincroniza, y se
publica con `os.replace`. La ingestión adquiere el mismo
`index_rebuild_lock_service` alrededor de todas sus llamadas `store.add`, de modo que
ningún fragmento puede añadirse a la generación que un rebuild está sustituyendo.

Evidencia posterior, sin alterar las reproducciones T092:

```text
PYTHONPATH=src uv run --no-sync pytest \
  tests/integration/test_material_query_during_rebuild.py \
  tests/integration/test_material_index_rebuild_race_reproduction.py -q
9 passed, 1 warning in 1.74s

uv run --no-sync ruff check \
  src/oralia/infrastructure/vector_store/chroma_store.py \
  src/oralia/application/commands/ingest_material.py \
  tests/integration/test_material_query_during_rebuild.py --no-cache
All checks passed!
```

La reproducción A sirve N=1, que permanece retenida; B detecta N retirada tras dos
rebuilds, re-resuelve y sirve N+2=3, informando versión `"3"`; el experimento empírico
continúa verde. Las pruebas adicionales usan `threading.Event`, nunca `sleep`, para el
límite de dos intentos y para demostrar que `store.add` espera al mismo lock que
`rebuild_material_index`.

### 13.3 Regresión T088 y cierre de Feature 002 (2026-10-16)

La suite focal enumerada en T088 pasó con **78 passed, 1 warning in 8.74s**. La suite
amplia, sin excluir las reproducciones A/B, pasó con **588 passed, 1 deselected,
1 warning in 47.34s** usando `-m "not ollama and not speech"`. El único `deselected`
corresponde al caso Ollama externo y el warning es el `StarletteDeprecationWarning`
heredado; no hubo regresiones de T085/T086/T098/T099/T100 ni de T090 de Feature 001.

Ruff 0.15.22 conserva 17 hallazgos heredados (`E501`: 16, `F541`: 1) frente a los 49
del manifiesto T090: 12 en la misma ubicación, 5 desplazados, 32 eliminados y **0
nuevos** por identidad estable `(ruta, código, mensaje)` con multiplicidad. SHA-256 del
manifiesto: `3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

**Evidencia de recreación silenciosa**: confirmada directamente — tras cada
reproducción, `material_fragments_v1` SÍ existe en el listado de colecciones
(`store._client.list_collections()`) con `count() == 0`, pese a haber tenido
originalmente un fragmento — la firma exacta de "recreación silenciosa vacía" que
`research.md` y el contrato prohíben.

**Suite previa, excluyendo los nuevos casos rojos**: `PYTHONPATH=src uv run pytest
tests/ -q -m "not ollama and not speech" --deselect
tests/integration/test_material_index_rebuild_race_reproduction.py::
test_A_reader_paused_mid_resolution_survives_one_concurrent_rebuild --deselect
tests/integration/test_material_index_rebuild_race_reproduction.py::
test_B_reader_paused_survives_two_concurrent_rebuilds_needs_retry` — ver `tasks.md`
para el recuento exacto; sin regresiones. `tests/integration/test_material_query_
during_rebuild.py` (test existente, no modificado) sigue en verde de forma aislada.

**Ruff**: `uv run ruff check tests/integration/test_material_index_rebuild_race_
reproduction.py --statistics` → 0 errores; recuento global sin nuevos errores
respecto a la referencia heredada — ver `tasks.md`.

## 14. Recuperación acotada: terminación, exhaustividad y relevancia (FR-017/FR-018/FR-019/FR-019a) — corregido en la segunda ronda de estabilización, 2026-09-10; implementado en T085/T090, 2026-09-12g; corregida la reutilización de cola del compositor en T099, 2026-09-12h

**Hallazgo de partida (H08)**: `MaterialRetrieverAgent.execute` limita los candidatos
recuperados del índice a `over_fetch = max(max_fragments * 4, max_fragments)` **antes**
de aplicar `_authorized`/`_is_retrievable`. Si más del 75% de esos candidatos no está
autorizado o vigente, evidencia autorizada y relevante más allá de esa ventana queda
descartada sin considerarse.

### 14.1 Exhaustividad de autorización/vigencia — terminación corregida

**Corrección respecto a la primera ronda**: el diseño anterior ("ampliar
progresivamente hasta `max_fragments` autorizados o agotar `time_budget_ms`") no
especificaba qué ocurre cuando el corpus tiene *menos* fragmentos autorizados y
vigentes que `max_fragments` — sin una condición de parada adicional, la ampliación
progresiva seguiría duplicando el tamaño de lote y volviendo a consultar,
potencialmente el mismo conjunto agotado de candidatos, hasta consumir todo
`time_budget_ms` de forma inútil en vez de detectar pronto que no hay más que ofrecer.

**Decision — dos condiciones de parada adicionales, además de las dos ya definidas**:
la ampliación progresiva MUST detenerse cuando ocurra la primera de estas cuatro
condiciones: (a) se han acumulado `max_fragments` candidatos autorizados y vigentes;
(b) se agota `time_budget_ms`; (c) el propio índice devuelve **menos** candidatos que
los solicitados en la última ampliación (`len(matches) < k` pedido a
`self._store.query(...)`) — señal de que el corpus ya no tiene más candidatos que
ofrecer para esa consulta, sin necesidad de seguir ampliando; (d) dos ampliaciones
sucesivas devuelven el **mismo conjunto** de identificadores de fragmento que la
anterior (sin candidatos nuevos) — señal equivalente cuando (c) no se cumple
literalmente pero el índice ya no aporta nada distinto. En los casos (c)/(d) el
resultado se devuelve con los candidatos autorizados ya acumulados (posiblemente menos
de `max_fragments`) y una entrada en `warnings` distinta de la de presupuesto agotado
(p. ej. `"corpus agotado para esta consulta"`) — no es un fallo ni un resultado
parcial por tiempo, es un resultado completo dado lo que existe.

### 14.1a Implementación (T085/T090, ronda 2026-09-12g)

**Algoritmo final** (`MaterialRetrieverAgent._run_widening_search`): ventana inicial
`k = max(max_fragments * 4, max_fragments)` (mismo multiplicador que el diseño
retractado, ahora solo el tamaño de la **primera** ronda, no la respuesta final);
cada ronda duplica `k` (`_WIDENING_FACTOR = 2`) y vuelve a consultar
`self._store.query(vector, {"course_id": course_id}, k)` **desde cero** — el
resultado de una ronda es el top-`k` completo y reordenado del almacén, no un
incremento sobre la ronda anterior. La selección (`selected`) se **reconstruye por
completo** a partir del orden de la ronda más reciente en cada iteración (nunca
`selected.extend(...)`), de modo que una ordenación de una ronda más antigua y
pequeña nunca pueda imponerse a la más reciente del almacén — esto también garantiza
deduplicación por `fragment_id` (una única consulta nunca repite un id) conservando
la primera aparición dentro de esa ronda. Un conjunto `seen_ids` acumulado (a través
de rondas) evita volver a consultar SQL por identificadores ya cacheados
(`fragment_rows_cache`, local a cada llamada a `execute()`) y alimenta el contador de
rondas consecutivas sin novedad.

**Corrección de redacción de la condición (d)**: el texto original de este documento
decía "dos ampliaciones sucesivas devuelven el mismo conjunto de identificadores" —
la implementación usa, tal como exigió esta ronda, un **contador de rondas
consecutivas sin ningún id nuevo** (`stale_rounds`, reiniciado a 0 en cuanto una
ronda aporta al menos un id nuevo), no una comparación de igualdad de conjuntos entre
dos rondas concretas ni una comparación de tamaños — evita depender del orden interno
del conjunto y cubre el caso en que el almacén recicla ids sin que dos rondas
consecutivas sean literalmente idénticas en otros aspectos.

**Las cuatro condiciones de parada, en el orden en que se comprueban** (tras
completar la consulta+SQL+filtrado de la ronda; `time_budget_ms` se comprueba
además **antes** de cada ronda): (1) `len(selected) >= max_fragments`; (2)
`_elapsed_ms(started) > time_budget_ms` (presupuesto agotado, cooperativo — T086,
no esta tarea, lo haría preemptivo); (3) `len(matches) < k`; (4) `stale_rounds >=
_STALE_ROUNDS_LIMIT` (2). Pruebas dedicadas por condición
(`tests/integration/test_material_retrieval_widening_structural.py`):
`test_multiple_widenings_recover_the_two_valid_fragments_beyond_them` (1, con
múltiples rondas reales), `test_budget_exhausted_between_rounds_keeps_partial_results_single_warning`
(2), `test_fewer_matches_than_k_terminates_without_further_queries` (3),
`test_two_consecutive_stale_rounds_terminate_the_search` (4, con un doble que
recicla ids manteniendo `len(matches) == k` para excluir la condición 3).

**Efectos laterales, una sola vez, solo sobre la selección final**: `blocked_out_of_scope`
se acumula (OR) a través de todas las rondas pero `_log_blocked_attempt` se invoca
como máximo una vez, después de terminar el bucle completo — confirmado por
`test_blocked_out_of_scope_attempt_is_logged_once_across_several_widenings` (un
candidato no autorizado presente en múltiples rondas, un único
`trace_service.record_event`). `_detect_and_record_conflicts` recibe exclusivamente
`selected` (la lista final, ya filtrada) — confirmado por
`test_discarded_candidates_never_reach_conflict_detection` (candidatos no
autorizados/de baja relevancia nunca llegan a `detect_conflicts`). Todo acceso a
`self._db` permanece en el hilo principal — cierto tanto en esta ronda (T085, sin
mover ninguna llamada a un hilo todavía) como después de T086 (§12/§12.1): solo
`embed`/`query` se mueven a `BoundedBlockingWorker`, nunca el acceso a `self._db`.

**`max_fragments <= 0`**: guarda defensiva nueva en `execute()` — devuelve
`fragments = []` inmediatamente, sin invocar `self._store.query(...)` en absoluto
(confirmado por `test_max_fragments_zero_or_negative_returns_empty_without_querying_store`,
que usa un `VectorStore` espía). Corrige la fisura documentada en T090: con la
ventana fija anterior, `ChromaVectorStore.query` fuerza `n_results = min(max(k, 1),
count())` — un suelo de 1 incluso pidiendo `k=0` — y el bucle del agente comprobaba
el límite **después** de añadir un candidato, así que `max_fragments <= 0` podía
devolver hasta 1 fragmento en vez de ninguno. El esquema HTTP
(`MaterialQueryInput`) sigue sin validar este caso — la tarea de seguimiento
registrada entonces (`course_id`, ver §14.1b más abajo) ya se implementó en T098; la
validación de `max_fragments`/`time_budget_ms` en el esquema HTTP sigue sin
abordarse (guarda defensiva a nivel de agente únicamente, sin convertir el caso en
un `422`).

### 14.1b Aislamiento SQL de `course_id` — corregido en T098 (2026-09-12i)

**Hallazgo de partida**: `MaterialRetrieverAgent` envía `filters={"course_id":
course_id}` a `self._store.query(...)` (`ChromaVectorStore`) como un prefiltrado
barato, pero nunca revalidaba `MaterialFragment.course_id`/`MaterialDocument.course_id`
contra SQL después de recuperar los `fragment_id` — `_authorized` solo comprobaba
`activity_configuration_id`. Un `VectorStore` que ignorase el filtro, o cuya
metadata estuviera desincronizada respecto a SQL, podía devolver un fragmento de
**otra asignatura** siempre que compartiera `activity_configuration_id` con la
consulta — el único filtro que sí se revalidaba. `ChromaVectorStore`'s propio
docstring inducía a este error: describía el prefiltrado por `course_id` como algo
ya resuelto, dejando "las comprobaciones restantes" (sin incluir `course_id` mismo)
a cargo de SQL — corregido, ver el propio archivo.

**Corrección**: `course_id`, cuando está presente, ahora exige simultáneamente
`fragment.course_id == course_id` **y** `document.course_id == course_id` — una
discrepancia entre ambas copias denormalizadas (que en teoría nunca deberían
divergir, pero SQL es la única fuente de verdad, nunca la metadata del índice)
también causa rechazo. Un candidato de otra asignatura cuenta como
`blocked_out_of_scope` (mismo cubo que un `activity_configuration_id` incorrecto):
el ensanchamiento progresivo continúa buscando candidatos válidos posteriores
(H08.A, sin cambios de diseño), y el intento bloqueado se registra como máximo una
vez por `execute()` aunque aparezca en varias rondas (mismo mecanismo ya validado
para `activity_configuration_id`). `VectorMatch.metadata` NUNCA se consulta para
autorizar — solo las filas SQL ya obtenidas deciden.

**Sin políticas divergentes (compartido con T099)**: dos funciones puras nuevas,
`_fragment_authorized_for_scope`/`_fragment_currently_retrievable`
(`material_retriever_agent.py`, module-level, sin efectos secundarios), son ahora la
**única** implementación de la política de asignatura/actividad/ciclo de vida —
`MaterialRetrieverAgent._authorized`/`_is_retrievable` (bucle propio del agente,
efectos secundarios `blocked_out_of_scope`/traza FR-026 conservados fuera de las
funciones puras) y `get_currently_valid_fragment` (T099, reutilización de
`concepts_pending` en Feature 003) delegan ambas en las mismas dos funciones — ya no
existen dos copias de las mismas reglas que pudieran divergir con el tiempo.

**Consultas/cachés SQL por ronda**: se añadió `document_rows_cache` (paralelo al ya
existente `fragment_rows_cache`), poblado en un único `db.query(MaterialDocument)
.filter(id.in_(...))` por ronda para los `document_id` distintos de fragmentos
recién vistos — antes, `_is_retrievable` invocaba `self._db.get(MaterialDocument,
...)` una vez por candidato por ronda (mitigado en la práctica por el mapa de
identidad de SQLAlchemy, pero no explícito ni por lotes); ahora es un único `IN`
por lote de ids nuevos, igual que ya se hacía para `MaterialFragment`. Ningún
`db.get(fragment)` adicional por candidato — la caché de T085 se conserva sin
cambios.

**Reproducción antes/después**
(`tests/integration/test_material_retrieval_course_isolation.py`, 8 pruebas): contra
el código previo a T098, 7/8 fallan — un `VectorStore` que ignora el filtro
`course_id` y devuelve primero un fragmento de otra asignatura con relevancia 0.90
(sobre el umbral 0.35) se filtraba hasta `fragments`; un `fragment.course_id`
incorrecto con `document.course_id` correcto (o viceversa) también se aceptaba; una
metadata de `VectorMatch` que afirmaba el curso correcto no cambiaba el resultado
(el defecto real estaba en no consultar SQL en absoluto, no en confiar en la
metadata, pero la prueba confirma que tampoco se cuela por esa vía). El contraste
positivo (fragmento y documento del curso correcto) ya pasaba. Tras T098, mismas
aserciones, 8/8 en verde — incluidas dos pruebas dedicadas a que el ensanchamiento
progresivo sigue encontrando el candidato correcto tras varios de otra asignatura, y
a que el bloqueo por asignatura incorrecta se registra una sola vez pese a aparecer
en múltiples rondas.

**Alcance explícitamente NO ampliado**: no se modifica el esquema HTTP
(`MaterialQueryInput.course_id` sigue siendo obligatorio, tal como estaba); no se
introduce un `422` nuevo; no se toca T086/T087/T091/T092 ni Feature 003 más allá de
la función compartida ya usada por T099. Cuando `course_id` no se proporciona en la
llamada interna (`course_id=None`), el comportamiento se conserva sin cambios:
ninguna de las dos comprobaciones nuevas se aplica (mismo criterio ya usado por
`activity_configuration_id=None`) — esto no es una relajación nueva, es el
comportamiento ya vigente para un filtro ausente, documentado aquí por completitud.

### 14.2 Relevancia respecto a la pregunta — se retira la prohibición absoluta

**Corrección respecto a la primera ronda**: la instrucción original era no introducir
un umbral *arbitrario* — no prohibir cualquier umbral. La primera ronda lo convirtió,
incorrectamente, en "este agente MUST NOT aplicar ningún umbral de similitud/relevancia
mínima" (así quedó incluso escrito en `contracts/material-retriever-agent.md`). Esa
prohibición absoluta se retira.

**Fundamentación y pertinencia son propiedades distintas**: `GroundingVerifierAgent`
comprueba que una propuesta esté respaldada por la evidencia **que se le entregó** —
si esa evidencia es, en sí misma, ajena a la pregunta del estudiante (recuperada por
coincidencia léxica/semántica débil, pero perteneciente a un fragmento que no responde
lo que se preguntó), una respuesta que parafrasee fielmente esa evidencia puede pasar
`fundamentada` sin ser pertinente — el verificador de fundamentación no tiene forma de
saber si la evidencia que recibió era la correcta para la pregunta, solo si la
propuesta la refleja fielmente. Son dos comprobaciones distintas y ninguna sustituye a
la otra.

**Responsabilidad (sin imponer un algoritmo concreto)**: `MaterialRetrieverAgent` es el
componente adecuado para reconocer "ningún candidato recuperado es suficientemente
pertinente para esta consulta" — ya calcula `relevance_score` (similitud coseno vía
ChromaDB) por cada candidato, la señal ya existe, no hace falta un segundo modelo. Qué
umbral concreto, si un valor fijo o configurable, y cómo se combina con la ampliación
progresiva de §14.1, es una decisión de la tarea de implementación — no se fija aquí
para evitar un umbral no justificado por un escenario real (ver escenario nuevo más
abajo, que SÍ lo justifica). Cuando ningún candidato autorizado supera ese umbral, el
resultado esperado es `fragments = []` con una advertencia distinguible (p. ej.
`"sin evidencia suficientemente pertinente"`) — el compositor de agencia (Feature 003,
ya implementado, Nivel 0 de la cadena de degradación, research.md §2 de esa feature)
ya sabe tratar `fragments = []` como señal para omitir la generación
(`acknowledge_missing_info`), sin necesitar un nuevo mecanismo en 003.

**Escenario que justifica el umbral (nuevo, no arbitrario)**: una consulta ajena al
contenido de un corpus **no vacío** (p. ej. "¿cómo se hace una tortilla de patatas?"
sobre un corpus de materiales de programación) MUST producir una respuesta de
abstención o aclaración — no una respuesta generada a partir del fragmento
"menos lejano" del corpus, por irrelevante que sea, solo porque el índice siempre
devuelve *algo* cuando `k ≥ 1` y hay al menos un documento indexado. Sin un umbral de
relevancia en algún punto del recorrido (aquí, o en el compositor), este escenario no
tiene forma de detectarse — `GroundingVerifierAgent` solo vería una propuesta
"fundamentada" en un fragmento real, aunque ese fragmento no tenga nada que ver con la
pregunta.

**Rationale**: la ampliación progresiva con terminación completa (§14.1) resuelve el
riesgo de descartar evidencia autorizada sin inventar un parámetro nuevo; asignar la
responsabilidad de relevancia a `MaterialRetrieverAgent` (que ya calcula la señal) y
justificarla con un escenario real, en vez de prohibirla por decreto, resuelve la
distinción real entre fundamentación y pertinencia sin construir un segundo modelo de
verificación (instrucción explícita).

**Consumidores**: mismo agente que en H03/H10 (003 y, previsiblemente, 004).

### 14.2a Implementación (T085/T090, ronda 2026-09-12g)

**Umbral adoptado y justificación cuantitativa (medición de T090)**: `0.35`, sobre
`relevance_score = 1 - distancia_coseno` (Chroma, `hnsw:space=cosine`) — medido con
el modelo y almacén reales del proyecto
(`paraphrase-multilingual-MiniLM-L12-v2` + `ChromaVectorStore`), no elegido a priori.
Positivos observados: 0.6212–0.8130 (incluidas paráfrasis, no solo coincidencias
literales); negativos observados: 0.0583–0.2162 (4 consultas claramente ajenas,
incluida la del propio Escenario C.1, "receta de tortilla de patatas" → 0.2162);
hueco limpio de 0.4050 entre ambos rangos. `0.35` queda deliberadamente más cerca del
extremo negativo (margen 0.134 sobre el peor negativo, 0.271 bajo el positivo más
débil) — sesgado contra rechazar evidencia genuinamente relevante, ya que ese falso
positivo de "sin pertinencia" es pedagógicamente más costoso (el sistema negaría
tener información que sí tiene) que aceptar un fragmento marginalmente relacionado.

**Valor único con nombre, configurable solo al construir el agente**:
`_DEFAULT_RELEVANCE_THRESHOLD = 0.35` en `material_retriever_agent.py`, parámetro
`relevance_threshold` del constructor de `MaterialRetrieverAgent` — no expuesto en
`MaterialQueryInput` ni en ningún endpoint HTTP (research.md §14.2 ya decidía dejar
esto a la tarea de implementación; T085 la resuelve como un ajuste interno de
calidad de recuperación, no una opción del usuario).

**Comparación en el límite** (`_meets_relevance_threshold`): `math.isfinite(score)
and score >= threshold` — `score == 0.35` se acepta (confirmado por
`test_relevance_score_exactly_at_threshold_is_accepted`); un valor infinitesimalmente
inferior (`0.349999`) se descarta (`test_relevance_score_immediately_below_threshold_is_rejected`).
`math.isfinite` descarta explícitamente `NaN`/`+inf`/`-inf` — necesario porque
`float("inf") >= 0.35` sería `True` con una comparación ingenua, aunque `NaN` ya
falla cualquier comparación por sí solo (`test_non_finite_relevance_scores_are_never_returned`).

**Política de advertencias, sin duplicar y con prioridad explícita**: `_run_widening_search`
devuelve también `relevance_rejected` (`True` si alguna ronda tuvo al menos un
candidato estructuralmente válido —autorizado, activo, indexado, vigente— rechazado
únicamente por relevancia). En `execute()`: si `not selected and relevance_rejected`
→ `"sin evidencia suficientemente pertinente"` (única advertencia, tiene precedencia
sobre la de corpus agotado); si no, y el corpus se agotó con `len(selected) <
max_fragments` → `"corpus agotado para esta consulta"`; el aviso de presupuesto
(`"presupuesto temporal agotado, resultado parcial"`) es independiente y se añade
siempre que `budget_exhausted` sea cierto, sin describir como parcial por tiempo un
corpus que en realidad se examinó por completo (nunca se añade si el bucle terminó
por las condiciones 1/3/4). Si al menos un fragmento pertinente fue seleccionado, no
se añade ninguna advertencia de pertinencia — los candidatos de baja relevancia
simplemente se descartan en silencio (`test_h08b_mixed_contrast_keeps_relevant_and_excludes_both_irrelevant`,
extiende el contraste mixto ya reproducido en T090 con exclusión explícita de ambos
irrelevantes).

**Descubrimiento no anticipado — acoplamiento con Feature 003 (autorizado a corregir
en esta misma ronda, tras confirmar la causa exacta)**: al ejecutar la regresión
completa con el umbral activo, 4 pruebas de Feature 003 fallaron
(`test_exceso_turnos_mismo_concepto_detected`,
`test_perdida_objetivo_detected_near_session_limit`, y las 2 variantes de
`test_adaptation_request_changes_generation_purpose`). Causa diagnosticada
(revirtiendo temporalmente el umbral a `0.0` para confirmar antes de tocar nada):
`self_study_agency_composer.py` asumía implícitamente que la recuperación de
`MaterialRetrieverAgent` siempre devolvía el conjunto completo de fragmentos
autorizados/vigentes de un documento pequeño — una suposición nunca antes puesta a
prueba porque, antes de T085, no existía ningún mecanismo capaz de devolver un
subconjunto. Con el umbral activo, una consulta de continuación con poco contenido
propio ("continúa", "Dame un ejemplo de esto") puede legítimamente recuperar menos
fragmentos que una consulta inicial más rica, y esto rompía tres mecanismos
distintos del compositor: (1) la rotación de `concepts_pending` en los modos
progresivos (`guided_explanation`/`presentation_preparation`/`concept_review`)
invalidaba la cola pendiente contra el conjunto (ahora más pequeño) de esta ronda en
vez de confiar en ella; (2) al no encontrar el fragmento en cola en el conjunto de
esta ronda, sustituía silenciosamente por un fragmento distinto, produciendo
contenido casi idéntico turno tras turno y disparando una `repeticion` espuria en
`CoherenceVerifierAgent`; (3) `nivel_0_skip` (research.md §2, Nivel 0) se decidía
sobre el `fragments` en crudo de la ronda, tratando una recuperación reducida como
"sin evidencia en absoluto" incluso con una cola ya vetada pendiente; (4) para
`doubt_resolution`, una petición de adaptación reconocida por `primary_intent`
(`_INTENT_PURPOSE`: "dame un ejemplo", "explícamelo más sencillo") usaba el texto
literal de la petición como consulta de recuperación, perdiendo el tema real al que
se refería anafóricamente ("esto").

**Corrección aplicada en `self_study_agency_composer.py`** (autorizada explícitamente
para esta ronda, acotada a estos tres puntos, sin más cambios de diseño de Feature
003): (1) la cola `concepts_pending` ya no se invalida contra el `fragments` de la
ronda actual — se confía en ella mientras tenga elementos, y solo se resiembra desde
la recuperación cuando está genuinamente vacía; (2) si el fragmento en cabeza de cola
no aparece en el `fragments` de esta ronda, se recupera su fila autoritativa
directamente por SQL (`db.get(models.MaterialFragment, current_fragment_id)`) en vez
de sustituirlo por otro fragmento no relacionado — **corregido en T099, ver más
abajo: esta fila MUST revalidarse, nunca darse por buena solo porque existe**; (3)
`nivel_0_skip` se decide sobre `active_fragments` (ya resuelto, incluida la cola) en
vez de sobre `fragments` en crudo; (4) para intenciones de adaptación reconocidas
(`primary_intent in _INTENT_PURPOSE`), la consulta de recuperación reutiliza
`previous_turn.input_text` (el tema real que se está adaptando) en vez del texto
literal de la adaptación — generaliza el mismo principio que `concept_review` ya
aplicaba con `concepts_addressed`. Verificado: las 4 pruebas antes fallidas pasan
tras esta corrección, y la regresión completa (345 passed, 1 deselected) no
introduce ninguna regresión nueva.

### 14.2b Corrección de T099 — revalidar en el momento de uso, no en el de encolar (2026-09-12h)

**Afirmación incorrecta de la ronda anterior, retirada**: el punto (2) de más arriba
presentaba "recuperar la fila autoritativa directamente por SQL" como suficiente,
apoyándose implícitamente en que el fragmento "ya fue vetado al encolarse". Esa
premisa es falsa en general: entre el turno que encola un `fragment_id` en
`concepts_pending` y el turno que lo reutiliza, cualquiera de estos cambios puede
ocurrir sin que el compositor lo detectara: `MaterialDocument.status` pasa a
`"inactive"`; `MaterialDocument.retired_at` se establece; `MaterialFragment.valid_until`
expira; `MaterialFragment.indexing_status` deja de ser `"indexed"`; el fragmento deja
de estar asignado a la actividad actual; el fragmento o su documento pasan a otro
`course_id`; o la propia fila se elimina (en cuyo caso el código anterior caía a
`fragments[:1]` — una sustitución arbitraria, no relacionada con lo que se pidió).

**Distinción explícita que debe mantenerse (y que la corrección respeta)**: la
**relevancia** inicial de un fragmento respecto a la pregunta que lo trajo a la cola
SÍ se hereda deliberadamente para una continuación anafórica ("continúa", "dame un
ejemplo de esto") — no tendría sentido volver a exigir que ese fragmento supere el
umbral de 0.35 frente a una frase que, por diseño, no lleva contenido temático propio
(§14.2a). Pero la **autorización y el ciclo de vida** (curso, actividad, indexación,
estado del documento, retirada, vigencia) NUNCA se heredan de cuándo se encoló el
fragmento — se revalidan contra SQL en cada reutilización, sin excepción.

**Corrección**: nueva función compartida, aditiva, `get_currently_valid_fragment`
(`material_retriever_agent.py`) — revalida `fragment.course_id`/`document.course_id`
contra el `course_id` de la actividad, `activity.id in
fragment.activity_configuration_ids`, `fragment.indexing_status == "indexed"`,
`document.status == "active"`, `document.retired_at is None`, y
`fragment.valid_until` nulo o futuro; devuelve la fila solo si pasa todo, o `None`
(incluida la fila inexistente) en caso contrario. Deliberadamente NO integrada en
`_authorized`/`_is_retrievable` ni en el bucle de `_run_widening_search` — esos
efectos secundarios (`blocked_out_of_scope`, traza FR-026) pertenecen al propio
bucle del agente, y añadir `course_id` allí sigue siendo el alcance, todavía sin
implementar, de T098. En el compositor: la cola se recorre desde la cabeza,
descartando cada entrada que no revalide y probando la siguiente (acotado, nunca
sustituyendo por una fila arbitraria); si ninguna entrada pendiente revalida pero la
recuperación de este turno sí tiene contenido, la cola se resiembra desde ahí; si
tampoco hay nada, se activa Nivel 0.

**Corrección adicional en el mismo archivo de agente**: `_run_widening_search`
comprobaba el presupuesto temporal con `elapsed_ms > time_budget_ms` — la igualdad
exacta (`elapsed_ms == time_budget_ms`) no se trataba como agotado, permitiendo una
ronda adicional exactamente en el límite. Corregido a `>=` en los dos puntos donde
aparece (antes de cada ronda y tras completar cada ronda) — el presupuesto "se
agota" incluye alcanzarlo exactamente, no solo superarlo.

**Reproducción antes/después**: 7 escenarios de invalidación entre turnos
(documento inactivo, documento retirado, fragmento expirado, no indexado,
desasignado de la actividad, curso distinto, fila eliminada), usando el flujo real
de autoestudio (`tests/integration/test_self_study_pending_fragment_revalidation.py`)
— contra el código previo a T099, 6/7 fallan de forma discriminante (el texto/id
inválido aparecía en `output_text`/`sources`/la traza `generation_call`/`concepts_pending`);
el séptimo (fila eliminada) no se distingue de forma fiable con este fixture concreto
porque la sustitución arbitraria anterior (`fragments[:1]`) podía coincidir por azar
con un fragmento distinto pero igualmente válido del mismo documento pequeño — cubierto
de forma precisa y determinista, en su lugar, por una prueba unitaria dedicada sobre
`get_currently_valid_fragment` (`tests/unit/test_material_fragment_revalidation.py`,
10 casos: 1 válido + los 7 estados inválidos + 2 casos de filtro `None` permisivo).
Tras T099, mismas aserciones, 7/7 en verde en el archivo de integración y 10/10 en el
de unidad. Prueba de límite exacto del presupuesto
(`test_budget_exactly_at_the_limit_does_not_trigger_an_extra_round`): reproducido
contra `>` (ronda adicional, `queried_k=[4, 8]`) y corregido contra `>=`
(`queried_k=[4]`).

**Las cuatro correcciones de continuidad de T085 se conservan intactas**: verificado
ejecutando `tests/integration/test_mode_guided_explanation.py` (3/3) y
`tests/integration/test_coherence_conditions_fr015.py` (5/5) completos tras el
cambio de T099 — ninguna de las 4 regresiones de Feature 003 que motivaron ese fix
reaparece.
