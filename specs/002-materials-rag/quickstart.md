# Quickstart: validar Materiales autorizados y RAG trazable

Continúa `specs/001-core-cognitive-runtime/quickstart.md` — requiere esa instalación ya
funcionando. No repite código de implementación, solo pasos y resultados esperados.

## Prerrequisitos adicionales sobre la Feature 001

```bash
uv add chromadb sentence-transformers pdfplumber python-docx python-pptx
PYTHONPATH=src uv run alembic upgrade head   # nueva migración de esta feature
```

Ningún servicio externo ni conexión a Internet requerida — ChromaDB corre en modo
persistente local y el modelo de embeddings se descarga una vez y se ejecuta en CPU.

## Escenario A — Documento autorizado (User Stories 1 y 2)

1. `POST /api/v1/materials/documents` con un PDF de prueba con texto real.
   - **Esperado**: `201`, `status = "pending"`.
2. Consultar `GET /api/v1/materials/documents/{id}` hasta `status = "processed"`.
   - **Esperado**: sin error; metadatos completos (FR-008).
3. `POST /api/v1/materials/documents/{id}/activate`.
   - **Esperado**: `200`, `status = "active"`.
4. `POST /api/v1/materials/query` con una consulta cubierta por el documento.
   - **Esperado**: `fragments` no vacío, cada uno con `document_id`, `document_version`,
     `location_ref` — valida SC-001.

## Escenario B — Material retirado (User Story 5)

1. `POST /api/v1/materials/documents/{id}/versions` con una versión nueva del mismo
   documento.
   - **Esperado**: `201`; la versión anterior queda con `retired_at` no nulo.
2. Repetir la consulta del Escenario A.
   - **Esperado**: los fragmentos devueltos son de la nueva versión únicamente — valida
     SC-002/SC-003.

## Escenario C — Sin evidencia suficiente (User Story 3)

1. `POST /api/v1/materials/query` con una consulta fuera de cobertura de los materiales
   activos (corpus vacío o sin ningún documento indexado para la actividad).
   - **Esperado**: `fragments = []`; al evaluar con `GroundingVerifierAgent`,
     `verdict = "no_fundamentada"` o `"no_verificable"` — valida SC-004.

**Limitación conocida (estabilización 2026-09-10, research.md §11)**: este escenario
cubre ausencia total de evidencia, no contradicción de valor con evidencia parcialmente
solapada léxicamente — ver la matriz de aceptación de research.md §11 para los casos de
control de esa distinción, pendientes de la tarea de refuerzo de convergencia.

## Escenario C.1 — Consulta ajena a un corpus no vacío (research.md §14.2, nuevo en la segunda ronda de estabilización)

1. Activar un documento de prueba (p. ej. de programación) y `POST /api/v1/materials/query`
   con una consulta sin relación temática con ese documento (p. ej. una receta de
   cocina).
   - **Esperado (corregido — retira la prohibición absoluta de umbral de la primera
     ronda)**: `fragments = []` con una advertencia de pertinencia insuficiente —
     **no** el fragmento léxicamente "menos lejano" del único documento indexado
     presentado como si respondiera la consulta. Distinto de C: aquí el corpus no está
     vacío, la pregunta es simplemente ajena a él.

## Escenario D — Conflicto entre fuentes (User Story 6)

1. Activar dos documentos de prueba con afirmaciones contradictorias preparadas para el
   conjunto de pruebas de esta feature.
2. `POST /api/v1/materials/query` con una consulta relacionada.
   - **Esperado**: `conflicts` no vacío en la respuesta.
3. `GET /api/v1/materials/conflicts`.
   - **Esperado**: el conflicto aparece con `review_status = "pending_review"` — valida
     el registro persistente de Clarifications/FR-022a.

## Escenario E — Aislamiento de autorización (User Story 4)

1. Crear dos `ActivityConfiguration` con materiales activos distintos.
2. `POST /api/v1/materials/query` para la actividad A solicitando (mediante un filtro
   manipulado en la prueba) materiales de la actividad B.
   - **Esperado**: `fragments = []`; un `TraceEvent` de bloqueo queda registrado — valida
     SC-008.

## Escenario F — Fallo de indexación (User Story 7)

1. `POST /api/v1/materials/documents` con un archivo corrupto o un PDF sin texto
   extraíble.
   - **Esperado**: `status` termina en `"error"` o `"not_processable"` con
     `error_detail` comprensible; el documento nunca llega a `"active"`.
2. Repetir el Escenario A con el documento ya activo de antes.
   - **Esperado**: sigue respondiendo con normalidad — el índice existente no se vio
     afectado.

**Nota de cobertura pendiente (estabilización 2026-09-10, research.md §13)**: este
escenario no cubre una instancia de `MaterialRetrieverAgent`/`ChromaVectorStore` creada
antes de un `POST /materials/index/rebuild` completo y consultada después — ese caso de
concurrencia queda como prueba pendiente explícita (research.md §13, tarea de
convergencia).

## Escenario G — Duplicado (Clarifications, FR-005a)

1. Repetir la carga del archivo del Escenario A.
   - **Esperado**: `409` con `existing_document_id` y `conflict_token`.
2. `POST /api/v1/materials/documents/{id}/duplicate-resolution` con
   `resolution: "proceed_new"`.
   - **Esperado**: se crea un documento nuevo y distinto, no enlazado automáticamente.

## Validación de criterios de éxito adicionales

- **SC-006**: ejecutar `POST /materials/index/rebuild` y repetir el Escenario A —
  confirmar que la relación documento/fragmento/versión no cambia.
- **SC-007**: cronometrar el flujo carga→activación del Escenario A sin intervención
  manual fuera de las llamadas API/UI.
