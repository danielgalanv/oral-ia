# Requirements Quality Checklist: Privacidad y Datos — Materiales autorizados y RAG trazable

**Purpose**: Validar privacidad por diseño en los requisitos de esta feature: contenido
de documentos, exposición de red, minimización y control docente. Los ítems de
audio/transcripción del prompt de referencia se excluyen (fuera de alcance de esta
feature — ver Notes).
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Document Content Risk

- [x] CHK001 Does the spec address the possibility that a professor-uploaded document contains third-party personal data (e.g., a slide with a real student's name from a prior cohort), or is document content implicitly trusted as free of personal data? [Gap, Spec §Assumptions]
- [x] CHK002 Is `MaterialFragment.text` (which stores extracted document content verbatim) covered by any minimization or redaction requirement, or does the spec only address minimization for participant-generated data (inherited from Feature 001)? [Gap]

## Network Exposure

- [x] CHK003 Are the new materials-management endpoints (`/materials/*`) required to inherit the same `127.0.0.1`-only binding already established for Feature 001, or does the spec leave this to be re-derived rather than stating it explicitly for this feature's own endpoints? [Consistency, Spec §Constraints]

## Human Control Over Materials

- [x] CHK004 Is every state-changing action on a `MaterialDocument` (activate, deactivate, version, resolve duplicate, review conflict) traceable to an explicit professor action with no automatic/background equivalent? [Traceability, Spec §FR-005a, §FR-013, §FR-022a, Constitution §VI]

## Scope Boundary (Voice/Transcripts — deferred)

- [x] CHK005 Does the spec avoid conflating document "vigencia"/retention with participant transcript retention rules (Feature 004+), keeping the two retention concepts clearly separate? [Scope]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de privacidad y
  datos", recortada a lo aplicable a materiales docentes en esta feature. Los ítems
  sobre audio temporal, transcripción original/corregida y exportación de datos de
  participante siguen siendo territorio de la Feature 004/005, no de esta.
