# Requirements Quality Checklist: General — Núcleo cognitivo y ejecución local

**Purpose**: Validar que cada requisito de la feature sea observable, no ambiguo,
verificable y coherente con la constitución (checklist general de requisitos)
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Requirement Completeness

- [ ] CHK001 Are acceptance criteria defined for every priority user story (US1–US6)? [Completeness, Spec §User Scenarios]
- [ ] CHK002 Are requirements defined for what happens when the agency composer cannot find a required agent? [Completeness, Spec §Edge Cases]
- [ ] CHK003 Is a requirement present for the maximum number of concurrent interactive sessions, not just the multi-session historical case? [Completeness, Spec §Clarifications]

## Requirement Clarity

- [ ] CHK004 Is "resumen técnico básico" defined with a concrete minimum content list rather than left as an open-ended descriptor? [Clarity, Spec §FR-012b]
- [ ] CHK005 Is "mensaje seguro" (blocked-output response) specified with concrete content bounds, or only described qualitatively? [Clarity, Spec §FR-015]
- [ ] CHK006 Is "degradación controlada" quantified (e.g., which fallback strategies are acceptable) or left as a qualitative goal? [Clarity, Spec §FR-018]

## Requirement Consistency

- [ ] CHK007 Are the single-active-session rule (FR-012a) and the concurrent state-patch conflict scenario (US5) worded consistently about what "concurrency" refers to? [Consistency, Spec §Assumptions]
- [ ] CHK008 Do FR-021 (área técnica/docente) and FR-021a (access-control extension point) agree on what is and isn't in scope for authentication in this feature? [Consistency, Spec §FR-021, §FR-021a]

## Acceptance Criteria Quality

- [ ] CHK009 Can SC-003 ("ninguno se produce dentro del contexto privado del modelo") be objectively verified without inspecting implementation internals? [Measurability, Spec §SC-003]
- [ ] CHK010 Are the pass/fail conditions for "degradación controlada sin corromper el estado" (SC-006) stated in observable terms? [Measurability, Spec §SC-006]

## Scenario Coverage

- [ ] CHK011 Are requirements defined for a participant abandoning a session without an explicit "end" action (e.g., closing the browser)? [Gap, Coverage]
- [ ] CHK012 Are timeout/cancellation requirements defined uniformly for every agent role (retriever/generator/verifier/decider/presenter), not only for the generic "agent fails" case? [Coverage, Spec §FR-018]
- [ ] CHK013 Are requirements defined for what happens if the constitutional control itself fails or times out? [Gap, Exception Flow]

## Scope Boundaries

- [ ] CHK014 Does the spec avoid introducing implementation-level technical decisions (storage engine, framework, API shape) inside functional requirements? [Scope, Spec §Requirements]
- [ ] CHK015 Are the out-of-scope exclusions (materials/RAG, voice, evaluation, distributed execution) each traceable to a specific requirement or story that could otherwise be misread as in-scope? [Scope, Spec §Fuera de alcance, Constitution §Alcance por Fases]

## Dependencies & Assumptions

- [ ] CHK016 Is the assumption that "interpretación" can be deterministic/simulated validated against every user story that depends on it (US2–US5), or only against US2? [Assumption, Spec §Assumptions]
- [ ] CHK017 Is the dependency of US1 (activity/catalog configuration) on nothing else, and of US2–US6 on US1/US2, made explicit anywhere in the spec beyond the "Why this priority" narrative? [Traceability, Spec §User Scenarios]

## Ambiguities & Conflicts (Constitution Coherence)

- [ ] CHK018 Does every functional requirement that touches agent execution reference (directly or by traceable implication) the contract fields required by Constitution Principle II? [Consistency, Constitution §II]
- [ ] CHK019 Is there a requirement tying "salida bloqueada" evidence to the non-omissible constitutional check required by Constitution Principle IX ("nunca pueden omitirse por ahorro de recursos")? [Traceability, Constitution §IX]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist general de requisitos".
- Este checklist evalúa la calidad de lo escrito en `spec.md`, no si la implementación
  funciona.
