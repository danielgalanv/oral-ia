# Requirements Quality Checklist: No Evaluación Académica — Materiales autorizados y RAG trazable

**Purpose**: Confirmar que los veredictos de fundamentación de esta feature evalúan el
contenido de una propuesta, nunca al estudiante, y que ningún metadato de material se
reutiliza como señal de evaluación
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Content-Only Verdicts

- [x] CHK001 Is `GroundingVerificationResult.verdict` explicitly scoped to the proposal/content being evaluated, with language precise enough that it couldn't be misread as judging the student who asked the question? [Clarity, Spec §FR-023, §Key Entities]
- [x] CHK002 Is there a requirement stating that repeated "no_fundamentada"/"no_verificable" verdicts across a session MUST NOT be aggregated into any participant-level signal? [Gap]

## Metadata Reuse Risk

- [x] CHK003 Is `MaterialDocument`/`MaterialFragment` "prioridad" (FR-008) defined narrowly enough (e.g., retrieval ranking weight) that it couldn't be repurposed as a difficulty-to-student-ability mapping? [Ambiguity, Spec §FR-008]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de no evaluación
  académica". Esta feature no introduce evaluación de estudiantes directamente (no
  gestiona preguntas de práctica ni respuestas de estudiante — eso es Feature 003), por
  lo que el riesgo aquí es indirecto: que los veredictos de fundamentación sobre el
  *contenido* se confundan o reutilicen como señal sobre el *participante*.
