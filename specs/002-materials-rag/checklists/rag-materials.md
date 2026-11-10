# Requirements Quality Checklist: RAG y Materiales — Materiales autorizados y RAG trazable

**Purpose**: Validar requisitos de materiales autorizados y RAG: formatos, errores de
extracción, metadatos, versiones, autorización, vigencia, duplicados, chunking
reproducible, reconstrucción del índice, filtros, citas, evidencia insuficiente,
conflicto entre fuentes, retirada de versiones, prompt injection documental, aislamiento
entre asignaturas y trazabilidad de documento a respuesta
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Formats & Extraction Errors

- [x] CHK001 Are requirements defined for every one of the five admitted formats individually, or only as a single undifferentiated group, given that extraction failure modes differ per format? [Coverage, Spec §FR-002]
- [x] CHK002 Is the distinction between "not processable" (FR-003, scanned/no text) and "error" (FR-027, extraction/indexing failure) precise enough that a single test document couldn't plausibly satisfy both classifications? [Clarity, Spec §FR-003, §FR-027]

## Metadata & Versioning

- [x] CHK003 Are all minimum metadata fields (FR-008) given a type or format constraint (e.g., what values `estado de autorización` can take), or only named without a value domain? [Clarity, Spec §FR-008]
- [x] CHK004 Is "vigencia" (validity/currency, listed in FR-008's metadata) ever used by another requirement (e.g., retrieval filtering, staleness detection), or is it collected but never acted upon? [Gap, Spec §FR-008]
- [x] CHK005 Are requirements defined for what "sustituir un documento por una nueva versión" (FR-014) requires as input — must the new version be the same format as the original, or can format change across versions? [Gap, Spec §FR-014]

## Authorization, Isolation & Retirement

- [x] CHK006 Are the authorization dimensions (asignatura, actividad, sesión — FR-017, FR-019) each independently testable, or does the spec only describe them as a bundled filter? [Measurability, Spec §FR-017, §FR-019]
- [x] CHK007 Is there a requirement distinguishing "material inactivo" from "versión retirada" in terms of whether either can ever become active again, or are both treated as permanently excluded once reached? [Ambiguity, Spec §FR-015, §User Story 5]
- [x] CHK008 Are requirements defined for what "referencia histórica necesaria para auditar" (FR-015) must minimally contain, or is the historical record's content left unspecified beyond "necessary"? [Clarity, Spec §FR-015]

## Duplicates

- [x] CHK009 Is the professor's choice between "reutilizar/enlazar" and "continuar como carga nueva" (FR-005a) followed by a requirement describing what happens to metadata (course/activity assignment) in each branch? [Gap, Spec §FR-005a]

## Reproducible Chunking & Index Reconstruction

- [x] CHK010 Is "reproducible" (FR-007) defined precisely enough to be tested — e.g., does it mean byte-identical fragment boundaries, or just stable fragment count/order? [Measurability, Spec §FR-007]
- [x] CHK011 Does FR-016 (index reconstruction preserves document/fragment/version relationships) have a corresponding requirement for what happens to `MaterialConflictRecord`s or `Evidence` referencing fragments that get regenerated with new internal ids during reconstruction? [Gap, Spec §FR-016, §Key Entities]

## Retrieval Filters, Citations & Repeatability

- [x] CHK012 Are the exact fields returned per fragment (FR-018: procedencia, relevancia, metadatos) enumerated completely, or does "metadatos" defer to FR-008's full list without confirming all of it is retrieval-relevant? [Clarity, Spec §FR-018]
- [x] CHK013 Is "el mismo resultado" for repeatable recuperación (FR-020) defined as identical fragment set + order, or could a functionally-equivalent-but-differently-ordered result still satisfy this requirement as written? [Ambiguity, Spec §FR-020]

## Insufficient Evidence & Grounding Verdicts

- [x] CHK014 Are all five `GroundingVerificationResult` verdicts (FR-023) each paired with at least one acceptance scenario demonstrating when it applies, or do some verdicts (e.g., "no_verificable") lack a concrete example? [Coverage, Spec §FR-023, §User Story 3]
- [x] CHK015 Is the boundary between "parcialmente fundamentada" and "conflictiva" testable — i.e., does the spec distinguish "some claims unsupported" from "claims that actively contradict evidence"? [Clarity, Spec §FR-023]

## Cross-Source Conflicts

- [x] CHK016 Is there a requirement for what happens if a professor reviews a `MaterialConflictRecord` and takes no corrective action (leaves both materials active) — does the conflict remain flagged on every subsequent matching query? [Gap, Spec §FR-022a, §User Story 6]

## Prompt Injection Defense

- [x] CHK017 Is FR-028 ("tratar el texto extraído... como datos, nunca como instrucciones") paired with a testable acceptance scenario, or does it exist only as a Functional Requirement with no corresponding Edge Case/scenario to verify it against? [Traceability, Spec §FR-028, §Edge Cases]

## Traceability (Document → Response)

- [x] CHK018 Is FR-029 ("trazabilidad de cada fragmento devuelto") explicit about whether this traceability must survive an index reconstruction (FR-016) — i.e., can a fragment returned before a rebuild still be traced to the same document/version/location after one? [Gap, Spec §FR-029, §FR-016]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de RAG y materiales".
  Es el checklist más directamente ligado al propósito de esta feature.
