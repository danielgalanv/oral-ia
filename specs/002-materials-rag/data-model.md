# Data Model: Materiales autorizados y RAG trazable

Entidades nuevas de esta feature (ver `spec.md` → Key Entities). `Course`,
`ActivityConfiguration`, `Session`, `Turn`, `AgentContract`, `InternalMessage`,
`VerificationResult` se reutilizan tal como quedaron definidos en la Feature 001
(`src/oralia/infrastructure/db/models.py`) — ninguno se modifica.

## MaterialDocument

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| family_id | UUID | agrupa versiones del "mismo" documento (mismo patrón que `ActivityConfiguration.family_id`, Feature 001) |
| version | int | monotónico dentro de `family_id` |
| course_id | UUID (FK Course) | FR-001 |
| activity_configuration_ids | list[UUID] | actividades a las que está asignado (FR-013); puede estar vacío hasta activarse |
| filename | string | |
| content_hash | string | SHA-256 del archivo (FR-005) |
| mime_type | string | |
| size_bytes | int | |
| language | string | |
| status | enum(`pending`,`processing`,`processed`,`error`,`active`,`inactive`,`not_processable`,`pending_duplicate_review`) | FR-012; `pending_duplicate_review` is the transient state between a `409` possible-duplicate response and the professor's explicit resolution (FR-005a) |
| error_detail | string \| null | obligatorio si `status = error` o `not_processable` (FR-027) |
| retired_at | datetime \| null | se fija **únicamente** cuando esta versión es sustituida por una nueva (FR-014/FR-015) — nunca al desactivar (FR-013), que solo alterna `status` entre `active`/`inactive` y es reversible |
| duplicate_of_document_id | UUID \| null | se fija solo si el profesor eligió `link_existing` ante un duplicado (FR-005a) |
| created_at | datetime | |

**Validación**:
- `status` solo puede pasar a `active` si `status` previo era `processed` (FR-011: MUST
  rechazar activación de un documento no procesado o en error).
- Una asignación a actividad (`activity_configuration_ids`) MUST rechazarse si
  `retired_at` no es nulo o si `status = inactive` (FR-013a): solo la versión activa
  vigente de un `family_id` puede asignarse a una actividad.

**Transición de estado**: `pending` → `processing` → (`processed` | `error` |
`not_processable`) → `active` ⇄ `inactive` (manual, **reversible** — FR-013). Sustituir
por una nueva versión (FR-014) fija `retired_at` en la versión anterior; una vez
`retired_at` no es nulo, esa versión concreta **no puede** volver a `active`
(**irreversible** — FR-015): reutilizar su contenido exige crear otra versión nueva.

## MaterialFragment

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| document_id | UUID (FK MaterialDocument) | |
| document_version | int | copiado del documento en el momento de indexar, para citar la versión exacta aunque el documento avance |
| text | string | contenido recuperable — MUST tratarse como datos, nunca como instrucción (FR-028) |
| location_ref | string | página/diapositiva/sección/párrafo/offset según formato (FR-006) |
| sequence_index | int | orden dentro del documento, para reproducibilidad (FR-007) |
| embedding_ref | string | referencia al vector en el `VectorStore` (no se duplica el vector en SQL) |
| content_type | string | p. ej. "texto", "tabla" |
| course_id, activity_configuration_ids | igual que en `MaterialDocument` | autorización heredada (FR-019) |
| priority | int | FR-008 — solo afecta el orden de relevancia de la recuperación (FR-018), nunca una medida de dificultad del participante |
| valid_until | datetime \| null | vigencia heredada del documento (FR-008); null = sin caducidad |
| indexing_status | enum(`indexed`,`stale`,`retired`) | `stale` tras reconstrucción parcial pendiente; `retired` cuando el documento se retira |
| created_at | datetime | |

**Validación**: un `MaterialFragment` MUST NOT devolverse en ninguna recuperación
(FR-019) si se cumple cualquiera de:
- `indexing_status = retired`, o
- `MaterialDocument.status != active`, o
- `valid_until` no es nulo y ya pasó (FR-019a — tratado igual que `retired`).

**Reconstrucción del índice (FR-016a)**: `id` MUST preservarse entre reconstrucciones
para el mismo `(document_id, document_version, sequence_index)`. Si el motor de índice
subyacente exige regenerar `id`, la reconstrucción MUST actualizar en la misma
transacción cualquier `Evidence.fragment_id`, `GroundingVerificationResult.evidence_ids`
o `MaterialConflictRecord.fragment_ids` que referenciara el `id` anterior, para que
ningún registro quede huérfano.

## Evidence

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| fragment_id | UUID (FK MaterialFragment) | |
| relevance_score | float | |
| supports_claim | bool \| null | asignado por el verificador de fundamentación, null antes de evaluar |
| retrieved_at | datetime | |

## GroundingVerificationResult

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| turn_id | UUID \| null (FK Turn, Feature 001) | null si se generó fuera de un turno (p. ej. consulta directa de prueba) |
| proposal_ref | string | referencia a la propuesta evaluada (p. ej. `GeneratedProposal.id` cuando exista) |
| verdict | enum(`fundamentada`,`parcialmente_fundamentada`,`no_fundamentada`,`conflictiva`,`no_verificable`) | FR-023 — **distinto** del `VerificationResult.verdict` constitucional de la Feature 001 |
| supported_claims | list[string] | |
| unsupported_claims | list[string] | |
| evidence_ids | list[UUID] (FK Evidence) | |
| created_at | datetime | |

**Regla**: esta entidad y su tabla son independientes de `verification_result` (Feature
001); ningún código existente lee o escribe `GroundingVerificationResult` y viceversa
(FR-030).

## MaterialConflictRecord

| Campo | Tipo | Notas |
|---|---|---|
| id | UUID | PK |
| document_ids | list[UUID] (FK MaterialDocument) | documentos implicados |
| fragment_ids | list[UUID] (FK MaterialFragment) | fragmentos implicados |
| conflicting_claims | list[string] | afirmaciones incompatibles detectadas |
| detected_by_query | string | consulta que lo detectó (FR-022a) |
| review_status | enum(`pending_review`,`reviewed`) | visible en el área de materiales del profesor hasta que se revise |
| created_at | datetime | |
| reviewed_at | datetime \| null | |

## Relaciones clave (resumen)

```text
Course 1─N MaterialDocument(family_id) N─N ActivityConfiguration
MaterialDocument 1─N MaterialFragment
MaterialFragment 1─N Evidence
Evidence N─N GroundingVerificationResult (a través de evidence_ids)
MaterialDocument N─N MaterialConflictRecord (a través de document_ids)
MaterialFragment N─N MaterialConflictRecord (a través de fragment_ids)
GroundingVerificationResult N─0..1 Turn (Feature 001, opcional)
```
