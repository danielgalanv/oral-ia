# Requirements Quality Checklist: Coherencia y metacognición — Agencia de autoestudio

**Purpose**: Validar que los requisitos de detección de incoherencia (FR-015/FR-016),
combinación de veredictos con `GroundingVerifierAgent` (FR-024) y su relación con
mecanismos de degradación ya existentes de la Feature 001 sean completos, no ambiguos y
verificables.
**Created**: 2026-09-01
**Feature**: [spec.md](../spec.md) · [data-model.md](../data-model.md) · [contracts/self-study-agents.md](../contracts/self-study-agents.md)

## Cobertura de condiciones detectables

- [ ] CHK001 Is each of the nine conditions in FR-015 (falta de información, no fundamentada, contradicción, repetición, pérdida de objetivo, exceso de turnos, fallo de agente, latencia excesiva, ausencia de progreso) paired with at least one Acceptance Scenario or Edge Case, or do some exist only as a bare list item? [Coverage, Spec §FR-015] — **Clasificación C** (Clarify 2026-09-01): la FR ya es precisa y testable; la densidad de escenarios por condición es cobertura de pruebas (`tasks.md`/`tests`), no contenido faltante en la spec.
- [ ] CHK002 Is "ausencia de progreso" defined with any measurable criterion (e.g., N turns without a new concept added to `concepts_addressed`), or is it left as an unquantified judgment call? [Clarity, Spec §FR-015] — **Clasificación B** (Clarify 2026-09-01): mismo patrón ya usado en el proyecto (p. ej. el umbral de solapamiento léxico de `GroundingVerifierAgent` vive en código/`research.md`, no en la spec) — umbral de heurística, decisión de `plan.md`/`data-model.md`.
- [ ] CHK003 Is the scope of "repetición" specified — repetition against the immediately prior turn only, or against any prior statement in the session — given `CoherenceVerifierAgent.input.prior_statements` is a flat list with no explicit recency weighting? [Ambiguity, Contracts §CoherenceVerifierAgent] — **Clasificación B** (Clarify 2026-09-01): detalle del algoritmo de comparación — `plan.md`/`contracts`.

## Mapeo condición → acción de recuperación

- [ ] CHK004 Is there a requirement mapping which of the six recovery actions in FR-016 apply to which of the nine conditions in FR-015, or is the mapping left entirely to implementation discretion with no documented rule? [Gap, Spec §FR-016] — **Clasificación D** (Clarify 2026-09-01): FR-016 permite deliberadamente "al menos una de las siguientes acciones" sin mapeo rígido — forzar una tabla 1:1 reduciría flexibilidad legítima y convertiría una decisión de implementación en requisito innecesario.
- [x] CHK005 Do "exceso de turnos" (a `CoherenceIncident.incident_type`) and the session-level `max_turns` closure (FR-020, Feature 001 mechanism reused) have a documented relationship — does one imply or exclude the other, or could both fire independently for the same turn? [Consistency, Spec §FR-015, §FR-020, Data-Model §CoherenceIncident] — **Clasificación A — Resuelto** (Clarify 2026-09-01): FR-015 y la entidad `CoherenceIncident` ahora distinguen explícitamente "exceso de turnos dedicados a un mismo concepto" del límite global de sesión (FR-020).
- [ ] CHK006 Do "fallo de agente" and "latencia excesiva" (FR-015) duplicate signals already captured by the orchestrator's existing degraded/failed `Turn.status` (Feature 001), or is there a documented distinction between an agency-level degradation and a `CoherenceIncident` of these types? [Consistency, Spec §FR-015, Plan §Constitution Check Principio IX] — **Clasificación B** (Clarify 2026-09-01): cómo se traducen señales ya existentes de la agencia en filas `CoherenceIncident` es una decisión de diseño de `plan.md`, el requisito de detectarlas y registrarlas (FR-015) ya es claro.

## Combinación de veredictos (FR-024)

- [ ] CHK007 Is the combination rule between `GroundingVerifierAgent`'s five-value verdict (`fundamentada`/`parcialmente_fundamentada`/`no_fundamentada`/`conflictiva`/`no_verificable`) and `CoherenceVerifierAgent`'s three-value verdict (`approved`/`block`/`reformulate`) fully specified — which grounding verdicts count as "exigir bloqueo" for the purpose of FR-024? [Gap, Contracts §self-study-agents.md, Spec §FR-024] — **Clasificación B** (Clarify 2026-09-01): mapear cada veredicto de fundamentación a bloqueo/reformulación/aclaración exige juicio de producto no trivial (p. ej. `no_fundamentada` probablemente debe resolverse como "reconocer falta de información", US2, no como bloqueo genérico) — decisión de `plan.md`/`self_study_agency_composer.py`, no una regla que deba fijarse ahora en la spec sin ese análisis.
- [ ] CHK008 When the two verifiers disagree on `recovery_action`/next step (e.g., one implies "reformular" and the other "pedir aclaración"), is there a documented precedence rule, or only the binary "block if either requires" (FR-024) without guidance for the non-blocking disagreement case? [Ambiguity, Spec §FR-024] — **Clasificación B** (Clarify 2026-09-01): FR-016 ya permite cualquier acción aplicable; la precedencia entre sugerencias no bloqueantes es orquestación, no un requisito observable nuevo.

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → adaptado de "Checklist de
  arquitectura cognitiva" (separación generación/verificación, controles no omitibles) al
  verificador de coherencia nuevo de esta feature.
