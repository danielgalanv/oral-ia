# Requirements Quality Checklist: Accesibilidad — Materiales autorizados y RAG trazable

**Purpose**: Validar que las nuevas pantallas del área técnica (gestión de materiales,
conflictos, duplicados) hereden el mismo estándar de accesibilidad ya exigido para la
interfaz de la Feature 001. Los ítems de voz del prompt de referencia se excluyen (fuera
de alcance de esta feature).
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Inherited Standard

- [x] CHK001 Does the spec state explicitly that the new materials-management screens (upload, activation, conflict review, duplicate resolution) must meet the same accessibility requirement already established for the área técnica (Feature 001 FR-025), or does it leave this unstated and assumed? [Gap, Spec §Assumptions]

## New Interaction Patterns

- [x] CHK002 Is the professor's duplicate-resolution choice (FR-005a) required to be operable by keyboard alone, given it introduces a new decision-point UI not present in Feature 001? [Gap]
- [x] CHK003 Are error messages for rejected/corrupt/unsupported file uploads (FR-004, FR-027) required to be understandable without relying on color alone to distinguish error states? [Gap]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de voz y
  accesibilidad", recortada a accesibilidad textual/teclado — la voz sigue sin aplicar a
  esta feature (Feature 004).
