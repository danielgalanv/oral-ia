# Requirements Quality Checklist: Modos y supervisión docente — Agencia de autoestudio

**Purpose**: Validar que los requisitos de habilitación de modos por actividad
(`SelfStudyActivityConfig`, FR-002/FR-006), su inmutabilidad y la diferenciación real
entre los cinco submodos sean completos, no ambiguos y verificables.
**Created**: 2026-09-01
**Feature**: [spec.md](../spec.md) · [data-model.md](../data-model.md) · [contracts/api-self-study.md](../contracts/api-self-study.md)

## Configuración de modos habilitados

- [x] CHK001 Does FR-002 itself require at least one mode to be enabled per activity, or is the "no vacío" constraint only introduced later in `data-model.md` without a corresponding functional requirement in `spec.md`? [Gap, Spec §FR-002, Data-Model §SelfStudyActivityConfig] — **Resuelto** (Clarify 2026-09-01): FR-002a, en `spec.md`, ya coincide con la validación que `data-model.md` tenía.
- [ ] CHK002 Is it specified whether `SelfStudyActivityConfig` becomes immutable once the activity's first session starts (mirroring `ActivityConfiguration.immutable_since`), or could a teacher change `enabled_modes`/`practice_reveals_solution` mid-course while sessions are already using the previous configuration? [Ambiguity, Contracts §api-self-study.md, Spec §FR-002] — **Clasificación B** (Clarify 2026-09-01): la spec ya trata la habilitación de modos como parte de "la configuración de la actividad docente" (FR-002), y la Feature 001 ya hace esa configuración inmutable tras el primer uso (FR-025: reutilizada sin cambios). Cómo vincula `plan.md` la nueva tabla a ese mismo ciclo de vida es una decisión de diseño, no un requisito nuevo.
- [ ] CHK003 If a mode is disabled while a session already has an in-progress `PracticeQuestion` generated under it, is the expected behavior for that session's remaining turns defined? [Gap, Spec §Edge Cases] — **Clasificación B** (Clarify 2026-09-01): consecuencia directa de CHK002 — si `plan.md` vincula correctamente la inmutabilidad, este escenario queda estructuralmente excluido; no requiere un requisito propio.

## Alcance autorizado y cambio de tema

- [ ] CHK004 Is "el alcance autorizado de la actividad" (FR-023, Edge Cases) defined at the granularity of course, activity, or per-enabled-mode — i.e., could a change of topic be within the activity's authorized materials but outside the currently active self-study mode, and if so which requirement governs the rejection? [Ambiguity, Spec §FR-023, §Edge Cases] — **Clasificación D** (Clarify 2026-09-01): la Feature 002 (reutilizada sin cambios) no tiene ninguna noción de alcance "por modo" — los materiales se autorizan a nivel de actividad, sin partición más fina. FR-023 ya remite sin ambigüedad a ese único mecanismo existente.

## Diferenciación entre submodos

- [x] CHK005 Do "preparación de una exposición" and "revisión de conceptos" have any functional requirement that distinguishes their expected output from "resolución de dudas" / "explicación guiada", beyond a differing label — i.e., is there an observable, testable difference a reviewer could check, or could all four collapse into indistinguishable behavior as currently specified? [Measurability, Spec §FR-001, §Assumptions] — **Resuelto** (Clarify 2026-09-01): FR-001a define un comportamiento distintivo explícito para cada uno de los cinco modos.
- [x] CHK006 Is SC-001 ("los cinco submodos comparten los mismos agentes y el mismo estado de sesión") paired with a success criterion that also requires their *outputs* to be observably different per mode, or does SC-001 only test agent/state sharing without ruling out functionally identical behavior across modes? [Gap, Spec §SC-001] — **Resuelto** (Clarify 2026-09-01, ronda 2): SC-001 se reescribió íntegramente — exige 5/5 modos superando un escenario específico con diferencias observables en iniciativa, acción conversacional, política de diálogo, generación vs respuesta, progresión de turnos y cierre/continuación, verificable vía decisiones estructuradas de la agencia y traza, nunca por comparación literal de texto.

## Supervisión y auditabilidad

- [ ] CHK007 Is there a requirement for how a professor discovers or reviews which `enabled_modes`/flags are currently active for a given activity (a read path), or does `spec.md`/`contracts/api-self-study.md` only define the write/configure path? [Gap, Contracts §api-self-study.md] — **Clasificación D** (Clarify 2026-09-01): ni la Feature 001 ni la 002 tienen un requisito explícito equivalente para leer configuración ya creada — es coherente con el nivel de detalle ya establecido en el proyecto; la visibilidad de lectura queda implícita en "administración vía API" (FR-002/FR-006).

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → adaptado de "Checklist general
  de requisitos" (coherencia con la constitución, límites de alcance) al mecanismo de
  configuración docente nuevo de esta feature.
