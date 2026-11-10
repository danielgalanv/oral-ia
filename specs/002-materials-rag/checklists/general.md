# Requirements Quality Checklist: General — Materiales autorizados y RAG trazable

**Purpose**: Validar que cada requisito de la feature sea observable, no ambiguo,
verificable y coherente con la constitución (checklist general de requisitos)
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [x] CHK001 Are acceptance criteria defined for every priority user story (US1–US7)? [Completeness, Spec §User Scenarios]
- [x] CHK002 Is a requirement present for what happens when a professor tries to assign an inactive/retired document version to a new activity? [Gap, Coverage]
- [x] CHK003 Are requirements defined for the maximum file size accepted per upload, or is this left entirely to planning without even a qualitative bound? [Completeness, Spec §FR-004]

## Requirement Clarity

- [x] CHK004 Is "presupuesto temporal" (FR-017) defined with units and a minimum/maximum reasonable range, or left as an open numeric parameter with no bound? [Clarity, Spec §FR-017]
- [x] CHK005 Is "cobertura" (FR-010, "comprobaciones de cobertura y errores") quantified with a measurable threshold, or left as a qualitative check? [Clarity, Spec §FR-010]
- [x] CHK006 Is "afirmaciones incompatibles" (FR-022) given any concrete criterion for what counts as incompatible, or left fully to implementation judgment? [Ambiguity, Spec §FR-022]

## Requirement Consistency

- [x] CHK007 Do FR-005a (duplicate resolution, professor choice required) and FR-011 (document unusable until manually activated) agree on whether a "linked" duplicate document requires its own separate activation step? [Consistency, Spec §FR-005a, §FR-011]
- [x] CHK008 Is the professor-facing `MaterialConflictRecord` review flow (FR-022a) reconciled with the query-time conflict signal (FR-022) — same terminology and same conflict identifier reused across both? [Consistency, Spec §FR-022, §FR-022a]

## Acceptance Criteria Quality

- [x] CHK009 Can SC-005 ("el verificador de fundamentación detecta el 100% de las referencias que no respaldan...") be objectively measured without already knowing the composition of the "conjunto de pruebas preparado"? [Measurability, Spec §SC-005]
- [x] CHK010 Is SC-006 ("el índice puede reconstruirse... verificable comparando el índice reconstruido con el original") specific about what "comparing" means at a requirements level (byte-identical vectors vs. equivalent retrieval results)? [Measurability, Spec §SC-006]

## Scenario Coverage

- [x] CHK011 Are requirements defined for a professor deleting (not just deactivating) a document entirely, or is deletion intentionally out of scope for this feature? [Gap, Coverage]
- [x] CHK012 Are requirements defined for what happens to in-flight retrieval queries when an index reconstruction completes mid-query? [Gap, Exception Flow]
- [x] CHK013 Is there a requirement covering a professor uploading a file in a rejected/unsupported format, distinct from a supported-but-corrupt file (FR-004 vs. User Story 7)? [Coverage, Spec §FR-004, §User Story 7]

## Scope Boundaries

- [x] CHK014 Does the spec avoid introducing implementation-level technical decisions (vector store choice, embeddings model, chunking library) inside functional requirements? [Scope, Spec §Requirements]
- [x] CHK015 Is the boundary between this feature's `MaterialRetrieverAgent` (structured retrieval only) and Feature 003's dialogue/response generation kept explicit enough that a reader wouldn't assume this feature also produces conversational answers? [Scope, Spec §Assumptions]

## Dependencies & Assumptions

- [x] CHK016 Is the dependency of every user story on Feature 001 entities (`Course`, `ActivityConfiguration`, `Session`) made explicit per story, or only asserted once generally in Key Entities? [Traceability, Spec §Key Entities]
- [x] CHK017 Is the assumption that segmentation parameters (chunk size, overlap) are plan-level decisions validated against FR-007's reproducibility requirement — i.e., does the spec guarantee reproducibility survives whatever those parameters turn out to be? [Assumption, Spec §Assumptions, §FR-007]

## Ambiguities & Conflicts (Constitution Coherence)

- [x] CHK018 Does every functional requirement touching agent execution reference (directly or by traceable implication) the same `AgentContract` fields already required by Constitution Principio II, without redefining them? [Consistency, Constitution §II]
- [x] CHK019 Is there a requirement tying `MaterialConflictRecord` persistence and duplicate-resolution confirmation to Constitution Principio VI ("toda modificación... debe ser manual, versionada y auditable")? [Traceability, Constitution §VI]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist general de requisitos".
