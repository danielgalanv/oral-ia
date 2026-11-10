# Requirements Quality Checklist: Privacidad y no evaluación — Agencia de autoestudio

**Purpose**: Detectar evaluación académica encubierta y huecos de privacidad/retención
específicos de `PracticeQuestion`, `CoherenceIncident` y `StudySessionSummary` —
notas, clasificación de nivel, perfiles longitudinales indirectos o retención
indefinida no cubiertos por los checklists `no-evaluation`/`privacy` ya existentes de
las Features 001/002.
**Created**: 2026-09-01
**Feature**: [spec.md](../spec.md) · [data-model.md](../data-model.md)

## Inferencia de capacidad encubierta

- [x] CHK001 Is `difficulty_hint` (`PracticeQuestion`) required to derive only from the question bank/materials/objectives, or does `spec.md`/`data-model.md` leave open the possibility of deriving it from the *student's own prior answers in the session* — which would create a de facto ability-inference loop FR-014 otherwise prohibits? [Gap, Spec §FR-014, Data-Model §PracticeQuestion] — **Clasificación D** (Clarify 2026-09-01): FR-014 ya traza la línea correcta ("MAY usar la respuesta para elegir la siguiente pregunta" vs. "MUST NOT producir clasificación/inferencia PERMANENTE") — adaptar la siguiente pregunta dentro del turno es exactamente lo permitido; no persistir esa adaptación como perfil ya lo exige FR-011a.
- [x] CHK002 Is the boundary between "usar la respuesta del estudiante para elegir la siguiente pregunta/repregunta" (permitted, FR-014) and "clasificación... permanente de nivel" (prohibited, FR-014) precise enough that a single implementation choice (e.g., picking an easier follow-up question after a wrong answer) couldn't plausibly be read as either? [Ambiguity, Spec §FR-014] — **Clasificación D** (Clarify 2026-09-01): el calificador "permanente" en FR-014 ya es la línea divisoria; precisarla más allá empezaría a dictar implementación (p. ej. prohibir explícitamente cierta lógica de adaptación) en vez de comportamiento observable.

## Contenido del resumen de sesión

- [x] CHK003 Could an "incidencia" entry in `StudySessionSummary` (FR-021, e.g., an incident count or type per session) function as an implicit performance signal about the student even though FR-022 prohibits grades/diagnosis — is there a requirement constraining incident descriptions to system/architecture-observable facts only (mirroring the existing `technical_summary` constraint), or is this left unstated for the new participant-facing summary? [Gap, Spec §FR-021, §FR-022] — **Clasificación A — Resuelto** (Clarify 2026-09-01): FR-022a exige que las incidencias se describan como hechos observables del sistema, nunca como caracterización del estudiante — mismo estándar que `technical_summary` (Feature 001).

## Perfiles longitudinales indirectos

- [x] CHK004 Given `PracticeQuestion`/`CoherenceIncident` are scoped by `session_id` (FR-011) and *not* directly by `participant_code`, is there a requirement preventing the área técnica from reconstructing a de facto longitudinal profile by querying all sessions sharing the same `participant_code` and aggregating their `PracticeQuestion`/`CoherenceIncident` history — or does FR-011's "no persiste entre sesiones" only constrain the *agent's* input, not técnica-side aggregation? [Gap, Spec §FR-011, Constitution §Principio III] — **Resuelto** (Clarify 2026-09-01): FR-011a prohíbe explícitamente cualquier agregación/correlación entre sesiones del mismo `participant_code`, sin acotarlo a un componente concreto.

## Retención y purga

- [x] CHK005 Is `RetentionPolicy` (Feature 001, reused) explicitly extended to cover the three new tables (`SelfStudyActivityConfig` excluded — it's docente-owned config, not participant data) — `PracticeQuestion`, `CoherenceIncident`, and the `generation_call`/`study_session_summary` `TraceEvent` payloads — or is their retention/purge behavior left undefined by `data-model.md`? [Gap, Data-Model §Relaciones clave] — **Resuelto a nivel de requisito** (Clarify 2026-09-01): FR-028 exige no-persistencia por defecto y, si se autoriza, reutilizar `RetentionPolicy`/consentimiento con `retention_period` finito y configurable. Pendiente de reflejar la relación explícita en `data-model.md` antes de `/speckit-tasks`.

## Notas y lenguaje que suplanta al profesor

- [ ] CHK006 Do the Acceptance Scenarios for US4 (práctica) and US7 (cierre de sesión) each include an explicit negative check ("MUST NOT assign a grade/score") the way FR-014/FR-022 state it as a functional requirement, or does the observable/testable form of that prohibition exist only in the FR list without a corresponding scenario a reviewer could run? [Traceability, Spec §Acceptance Scenarios, §FR-014, §FR-022] — **Clasificación C** (Clarify 2026-09-01): FR-014/FR-022/FR-022a ya son individualmente testables tal como están redactadas; añadir un escenario Given/When/Then redundante es densidad de pruebas (`tasks.md`), no información nueva.

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de no evaluación
  académica" + "Checklist de privacidad y datos", combinadas y acotadas a las entidades
  nuevas de esta feature (no repite lo ya cubierto por
  `specs/001-core-cognitive-runtime/checklists/no-evaluation.md` y `privacy.md`).
