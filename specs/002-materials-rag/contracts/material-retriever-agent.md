# Contrato interno: MaterialRetrieverAgent / GroundingVerifierAgent

Ambos implementan el protocolo `Executable` ya definido en la Feature 001
(`src/oralia/domain/agents/agent.py`: `contract` + `async execute(request, cancellation)`
sobre `AgentRequest`/`AgentResult`, `contracts/agent-contract.md` de esa feature). Este
documento define únicamente la forma de `input`/`output` específica de estos dos agentes
nuevos — el sobre (`AgentRequest`/`AgentResult`/`AgentError`/`CancellationToken`) no
cambia.

## MaterialRetrieverAgent

```text
input (AgentRequest.input):
  query_text: string
  course_id: UUID
  activity_configuration_id: UUID
  session_id: UUID | null       # null para consultas directas de prueba/técnica
  max_fragments: int
  time_budget_ms: int

output (AgentResult.output), si status == "ok":
  fragments: [
    {
      fragment_id: UUID
      document_id: UUID
      document_version: int
      location_ref: string
      text: string
      relevance_score: float
    }
  ]
  index_version: string
  warnings: string[]            # p. ej. "presupuesto temporal agotado, resultado parcial"
  conflicts: [
    {
      conflict_record_id: UUID
      document_ids: UUID[]
      conflicting_claims: string[]
    }
  ]
```

**Reglas**:
- `fragments` MUST NOT incluir ningún fragmento cuyo `MaterialDocument` no esté
  `active`, no esté autorizado para `course_id`/`activity_configuration_id`, cuya
  versión esté retirada (FR-019), o cuya vigencia (`valid_until`) ya haya expirado
  (FR-019a).
- Si `time_budget_ms` se agota antes de completar la recuperación, el agente MUST
  devolver `status = "ok"` con los fragmentos obtenidos hasta ese momento y una entrada
  en `warnings`, no `status = "timeout"` — la degradación aquí es un resultado parcial
  válido, no un fallo (Edge Case: presupuesto temporal). "Se agota" MUST incluir
  alcanzar el límite exactamente (`elapsed_ms >= time_budget_ms`), no solo superarlo
  (T099, corregido — la implementación previa usaba `>` estricto).
- La ventana de candidatos consultada al índice vectorial MUST ampliarse
  progresivamente (geométricamente, no un multiplicador fijo como respuesta final)
  hasta que se cumpla la primera de cuatro condiciones, comprobadas en este orden:
  (1) se reúnen `max_fragments` candidatos autorizados, vigentes y suficientemente
  pertinentes; (2) se agota `time_budget_ms` (comprobado antes de cada ronda y tras
  completar cada ronda de consulta+SQL+filtrado); (3) el índice devuelve menos
  candidatos que los solicitados en esa ronda (`len(matches) < k`, corpus agotado);
  (4) un **contador de rondas consecutivas** sin ningún `fragment_id` nuevo alcanza su
  límite — no una comparación de igualdad entre dos conjuntos concretos ni de
  tamaños, para no depender del orden interno del conjunto (research.md §14.1,
  corregido en la segunda ronda de estabilización y precisado en la implementación de
  T085/T090). La selección final se reconstruye desde el orden de la ronda más
  reciente (nunca se acumula sobre rondas anteriores) — una ordenación antigua y más
  pequeña MUST NOT imponerse a la ordenación más reciente del almacén; esto garantiza
  también la deduplicación por `fragment_id`, conservando la primera aparición.
  Fundamentación (respaldo léxico de una propuesta en su evidencia, responsabilidad
  de `GroundingVerifierAgent`) y pertinencia (relación entre la evidencia recuperada y
  la pregunta, responsabilidad de este agente, que ya calcula `relevance_score`) son
  propiedades distintas — este agente MUST aplicar un umbral de relevancia mínima
  sobre `relevance_score` (comparación inclusiva en el límite: `score >= umbral`
  acepta la igualdad; valores no finitos —`NaN`/`±inf`— MUST descartarse de forma
  segura, nunca tratarse como si superaran el umbral) — valor por defecto `0.35`,
  medido empíricamente (research.md §14.2, T090: positivos 0.6212–0.8130, negativos
  0.0583–0.2162 con el modelo/almacén reales del proyecto), definido como una
  constante con nombre y configurable únicamente al construir el agente — MUST NOT
  exponerse como parámetro de `MaterialQueryInput`/la API HTTP. Cuando existan
  candidatos estructuralmente válidos (autorizados, activos, indexados, vigentes)
  pero ninguno supere el umbral, `fragments = []` con una única advertencia
  distinguible de pertinencia insuficiente (p. ej. `"sin evidencia suficientemente
  pertinente"`), con precedencia sobre la advertencia de corpus agotado cuando ambas
  condiciones coincidirían; ninguna advertencia de pertinencia MUST añadirse si al
  menos un candidato pertinente fue seleccionado (research.md §14.2, corregido —
  la versión anterior prohibía cualquier umbral, más allá de lo pedido).
- El presupuesto duro de ejecución (`request.deadline_ms`, envoltura de la Feature 001)
  MUST poder interrumpir la espera del trabajo de embeddings/búsqueda incluso cuando
  este es síncrono internamente — ejecutado a través de `BoundedBlockingWorker`
  (research.md §12/§12.1, T086), un mecanismo compartido y acotado por una capacidad
  explícita (no `asyncio.to_thread` a secas: ese despacha al *executor* por defecto
  del bucle de eventos, cuya cola de trabajo pendiente no está acotada por su propio
  límite de hilos, e insuficiente por sí solo como contrapresión frente a una ráfaga
  sostenida — research.md §12, corregido en T091); al expirar, `asyncio.CancelledError`
  MUST propagarse sin capturarse dentro de `execute()` para fabricar un resultado
  `status = "ok"` — es `run_with_deadline` (Feature 001, sin cambios) quien produce
  `status = "timeout"`, igual que para cualquier otro agente (research.md §12,
  corregido en la segunda ronda de estabilización). Esto degrada el turno a tiempo, no
  garantiza detener el trabajo de CPU ya iniciado en segundo plano (research.md §12,
  límite documentado) — la capacidad admitida por ese trabajo solo se libera cuando
  termina realmente, nunca cuando el `await` exterior se cancela (research.md §12.1).
- Una consulta que solicite `activity_configuration_id` fuera del alcance autorizado de
  `session_id` MUST devolver `status = "ok"` con `fragments = []` y un
  `TraceEvent` de bloqueo (FR-026) — nunca datos de la actividad no autorizada.
- Misma `query_text` + mismos filtros + mismo `index_version` MUST producir el mismo
  `fragments` (FR-020).
- `max_fragments <= 0` MUST devolver `fragments = []` sin consultar el almacén
  vectorial en absoluto (T085 — guarda defensiva; el diseño anterior podía devolver
  hasta un fragmento por un suelo interno del almacén combinado con el punto de
  corte del bucle, ver research.md §14.1a). El esquema HTTP (`MaterialQueryInput`)
  sigue sin validar `max_fragments`/`time_budget_ms` — no se convierte este caso en
  un `422` en esta ronda.
- El aislamiento por `course_id` se aplica en dos capas: el filtro `where` enviado
  al almacén vectorial (`ChromaVectorStore`) es un prefiltrado barato, y desde T098
  el agente además revalida contra SQL, tras el `fetch` por id, que
  `MaterialFragment.course_id == course_id` **y**
  `MaterialDocument.course_id == course_id` — una discrepancia entre ambas filas
  también causa rechazo (`blocked_out_of_scope`), y un almacén vectorial que
  ignorase el filtro o cuya metadata estuviera desincronizada ya no puede filtrar
  un fragmento de otra asignatura (research.md §14.1b).
- Un consumidor que reutilice un `fragment_id` obtenido en una llamada anterior (p.
  ej. la cola `concepts_pending` de Feature 003 para continuaciones anafóricas)
  MUST NOT presumir que la autorización/vigencia de ese momento sigue vigente ahora
  — MUST revalidar contra SQL en cada reutilización (T099, research.md §14.2b).
  `get_currently_valid_fragment` (módulo de este agente) expone esa misma política
  (course_id, actividad, indexación, estado/retirada del documento, vigencia) como
  una función compartida, aditiva, para quien necesite este chequeo fuera del propio
  bucle de `execute()` — no forma parte del contrato input/output de este agente.
  Desde T098, `get_currently_valid_fragment` y el propio bucle de `execute()`
  delegan en las MISMAS dos funciones puras (`_fragment_authorized_for_scope`/
  `_fragment_currently_retrievable`), de modo que ambos sitios de uso ya no pueden
  divergir en la política aplicada — resuelto por T098, research.md §14.1b.

## GroundingVerifierAgent

```text
input (AgentRequest.input):
  proposal_text: string
  evidence: [ { fragment_id: UUID, text: string } ]
  general_knowledge_allowed: bool

output (AgentResult.output), si status == "ok":
  verdict: "fundamentada" | "parcialmente_fundamentada" | "no_fundamentada" | "conflictiva" | "no_verificable"
  supported_claims: string[]
  unsupported_claims: string[]
```

**Reglas**:
- Si `evidence` está vacío y `general_knowledge_allowed = false`, `verdict` MUST ser
  `"no_fundamentada"` o `"no_verificable"` — nunca `"fundamentada"` (FR-021, FR-024).
- Este agente es independiente del `ConstitutionalControl` de la Feature 001; un
  `verdict` de este agente MUST NOT sustituir ni alterar el veredicto constitucional ya
  existente (FR-030) — ambos controles se ejecutan y se registran por separado.
- Semántica de los cinco veredictos, aclarada mediante `/speckit-clarify` (research.md
  §11, ronda 2026-09-12f — resuelve la ambigüedad registrada por T096; `spec.md` §
  Clarifications, Session 2026-09-12): `"conflictiva"` MUST reservarse
  exclusivamente al caso en que la evidencia utilizada toca un `MaterialConflictRecord`
  con `review_status = "pending_review"` (conflicto pendiente entre dos o más fuentes
  autorizadas, User Story 6) — MUST tener **precedencia** sobre los otros cuatro
  veredictos cuando ese conflicto existe, incluso si alguna afirmación aislada de la
  propuesta parecería tener soporte. Un conflicto ya revisado (`review_status`
  distinto de `"pending_review"`) MUST NOT seguir forzando `"conflictiva"` (FR-022b).
  Una contradicción entre la propuesta y un **único** fragmento de evidencia (sin que
  exista ese conflicto entre fuentes) MUST NOT clasificarse como `"conflictiva"` ni
  generar un `MaterialConflictRecord` sintético — se clasifica `"no_fundamentada"`
  (ninguna afirmación soportada) o `"parcialmente_fundamentada"` (coexiste con al
  menos una afirmación soportada), según corresponda. `"no_verificable"` se reserva
  para cuando ninguna afirmación está soportada y el mecanismo no puede determinar de
  forma fiable respaldo o contradicción (evidencia vacía con conocimiento general
  permitido, o toda afirmación no soportada corresponde a una expresión no
  interpretada sin coincidencia literal — nunca a una contradicción efectivamente
  interpretada, que es `"no_fundamentada"`).
- Una afirmación con solapamiento léxico suficiente pero que contradice **cualquiera**
  de los valores numéricos presentes en su cláusula de evidencia alineada (no solo el
  primero — una cláusula puede tener más de un valor, p. ej. "de 20 a 100 grados"; no
  en cualquier punto de la evidencia agregada — ver el caso multi-entidad de
  research.md §11), o cuya unidad reconocida difiere, o cuya polaridad (negación
  explícita) difiere, MUST clasificarse como `no_fundamentada`, no `fundamentada`.
- Una afirmación que declara un valor numérico propio MUST NOT clasificarse como
  `fundamentada` únicamente por solapamiento léxico cuando su cláusula de evidencia
  alineada no contiene ningún valor numérico reconocido — la cifra concreta no tiene
  con qué contrastarse (research.md §11, distinción de los casos a/b/c).
- Para una relación numérica admitida entre dos valores (p. ej. origen/destino en "de
  X a Y"), la comparación MUST conservar el papel de cada valor, no solo su
  pertenencia al conjunto de valores presentes en la evidencia — un origen y un
  destino intercambiados MUST NOT clasificarse como `fundamentada` aunque ambos
  números existan en algún punto de la evidencia (research.md §11, ronda R1-R3). Una
  afirmación simple que no declara ningún papel relacional (menciona un único valor,
  sin reproducir la relación completa) sigue comparándose de forma permisiva contra
  cualquier valor de la evidencia — esto no exige que una afirmación mencione todos
  los valores presentes en la evidencia para ser `fundamentada`.
- El análisis numérico de una cláusula MUST distinguir explícitamente tres resultados
  (research.md §11, ronda R1-R3): ninguna expresión numérica relevante; una o más
  expresiones interpretadas completamente dentro del alcance admitido (dígitos y
  decimales con signo, numerales cardinales simples/compuestos de decena+unidad hasta
  "cien", papel relacional origen/destino); o una expresión numérica detectada pero
  fuera de ese alcance (numerales de centena distinta de "cien", "mil"/millón,
  fracciones con barra, notación científica) — este último caso MUST NOT tratarse
  como si la cláusula no afirmara ningún número. Los formatos numéricos admitidos no
  son exhaustivos — una expresión fuera de ambas categorías (p. ej. un ordinal) se
  trata como ausencia de afirmación numérica, no como analizada.
- Corrección semántica (research.md §11, ronda 2026-09-12d): cuando la propuesta usa
  una expresión numérica fuera del alcance admitido, una coincidencia literal
  normalizada (únicamente mayúsculas/minúsculas, puntuación superficial y espacios —
  MUST NOT volver equivalentes números, signos, unidades, negaciones o palabras
  distintas) de la afirmación completa con su cláusula de evidencia alineada MUST
  clasificarse como soportada — el formato numérico fuera de alcance NO impide que una
  coincidencia literal cuente como respaldo documental. Sin esa coincidencia, la
  afirmación MUST NOT aprobarse por el resto de su solapamiento léxico, pero tampoco
  MUST forzarse a `no_fundamentada`: el veredicto agregado MUST distinguir
  `no_fundamentada` (al menos una afirmación con una diferencia activamente
  interpretada — polaridad, o valores ambos comparables que no coinciden) de
  `no_verificable` (ninguna afirmación soportada, y ninguna con una diferencia
  interpretada — solo expresiones numéricas fuera de alcance sin coincidencia
  literal): el mecanismo no puede confirmar el respaldo, pero tampoco tiene base para
  declarar una contradicción. Esta distinción es un cambio interno de agregación del
  campo `verdict` — no requiere ni introduce un tercer valor en
  `supported_claims`/`unsupported_claims`, que siguen siendo `string[]` sin cambios.
- Corrección de simetría (research.md §11, ronda 2026-09-12e, T096): la regla anterior
  MUST aplicarse analizando el formato numérico de **ambos** lados — la propuesta y la
  cláusula de evidencia alineada — antes de decidir, no solo el de la propuesta. Si
  **cualquiera** de los dos lados usa una expresión numérica fuera del alcance
  admitido, el resultado MUST depender únicamente de la coincidencia literal
  normalizada entre ambos textos (soportada si coinciden, `no_verificable` en caso
  contrario) — MUST NOT clasificarse como una contradicción activamente interpretada
  solo porque uno de los dos lados (cualquiera) no pudo interpretarse. La dirección en
  la que se comparan dos afirmaciones equivalentes (cuál se llama "propuesta" y cuál
  "evidencia") MUST NOT decidir por sí sola si el resultado es `no_fundamentada` o
  `no_verificable`. El caso ya existente de una propuesta con valor interpretado
  frente a una cláusula de evidencia sin ninguna expresión numérica en absoluto
  (ausencia real, no una expresión fuera de alcance) se conserva sin cambio como una
  contradicción activa (research.md §11, caso F2).
- Un empate entre varias cláusulas de evidencia igualmente alineadas (p. ej. evidencia
  duplicada) MUST evaluarse cláusula por cláusula (polaridad y valor) — MUST NOT
  resolverse aprobando ni rechazando por defecto solo por existir el empate.
  Implementado en `_claim_is_supported`/`_claim_is_supported_by_clause`, con matriz de
  aceptación y límites documentados en research.md §11 (no es una garantía semántica
  universal de fundamentación; sinónimos, paráfrasis y ofuscación del valor siguen sin
  detectarse).
- Una afirmación que combine contenido temático con una localización/atribución
  concreta ("como se explica en la página N", "según el capítulo N") MUST evaluarse
  como dos afirmaciones separadas en `supported_claims`/`unsupported_claims` — el
  contenido temático y la localización no comparten automáticamente el mismo veredicto
  (research.md §11, FR-023/§5).

## Endpoints HTTP (área técnica — pruebas/demostración de esta feature)

Prefijo `/api/v1/materials`, mismo patrón de autenticación no-op de la Feature 001
(`tecnica_access_control`).

### `POST /materials/documents`

Sube un documento (FR-001..FR-005a). `multipart/form-data`: `file`, `course_id`,
`activity_configuration_ids[]` (opcional).

**Response `201`**: `MaterialDocument` creado, `status = "pending"`.

**Response `409`** (posible duplicado — FR-005a):
```json
{ "detail": "possible duplicate", "existing_document_id": "uuid", "conflict_token": "uuid" }
```

### `POST /materials/documents/{id}/duplicate-resolution`

**Request**: `{ "resolution": "link_existing" | "proceed_new" }`

**Response `200`**: `MaterialDocument` resultante según la elección.

### `POST /materials/documents/{id}/activate` / `.../deactivate`

**Response `200`**: documento actualizado. `activate` responde `409` si
`status != "processed"` (FR-011).

### `POST /materials/documents/{id}/versions`

Sustituye por una nueva versión (`multipart/form-data`, mismos campos que la carga
inicial). **Response `201`**: nueva versión; la anterior queda `retired_at` fijado
(FR-014, FR-015).

### `GET /materials/documents` / `GET /materials/documents/{id}`

Lista/consulta estado de procesamiento (FR-012).

### `POST /materials/index/rebuild`

Reconstruye el índice (FR-016). **Response `409`** si ya hay una reconstrucción en curso
(incluida una ingestión que mantiene el mismo lock de escritura). Tras completar el
swap se conservan únicamente la generación publicada y la inmediatamente anterior; la
retirada de N-2 no puede provocar una colección vacía recreada por un lector. Si una
consulta pierde su generación entre resolución y lectura, re-resuelve una vez el
puntero y `index_version` refleja la generación realmente utilizada (Edge Case,
research.md §§9 y 13).

### `GET /materials/conflicts`

Lista `MaterialConflictRecord` pendientes de revisión del profesor (FR-022a).

### `POST /materials/conflicts/{id}/review`

Marca un conflicto como revisado (`review_status = "reviewed"`).

### `POST /materials/query`

Invoca `MaterialRetrieverAgent` directamente (demostración/prueba de esta feature — ver
research.md §1). **Request**/**Response**: igual que el `input`/`output` del agente
arriba.
