# Requirements Quality Checklist: Generación y fundamentación (LLM) — Agencia de autoestudio

**Purpose**: Validar que los requisitos que gobiernan `GenerationPort` (adaptador Ollama
real + reserva determinista), su relación con `GroundingVerifierAgent`/
`ConstitutionalControl` y la defensa frente a prompt injection documental sean completos,
no ambiguos y verificables — es la pieza más nueva y de mayor riesgo de este plan
(research.md §1).
**Created**: 2026-09-01
**Feature**: [spec.md](../spec.md) · [plan.md](../plan.md) · [research.md](../research.md) · [contracts/self-study-agents.md](../contracts/self-study-agents.md)

## Degradación y disponibilidad del modelo

- [ ] CHK001 Is a concrete `timeout_ms` (or a rule for deriving one) specified for the Ollama call itself, distinct from the agent-level `deadline_ms` already defined by Feature 001's contract envelope? [Gap, Plan §Technical Context, Contracts §GenerationPort] — **Clasificación B** (Clarify 2026-09-01): parámetro de configuración de un adaptador de infraestructura, no un requisito observable — a fijar en `plan.md`/`research.md`.
- [x] CHK002 Does `spec.md` define an acceptance scenario for "the local model is unavailable/times out", or does that behavior exist only in `research.md`/`plan.md` without a corresponding user-facing Acceptance Scenario or Success Criterion? [Traceability, Spec §Acceptance Scenarios, Research §1] — **Clasificación A — Resuelto** (Clarify 2026-09-01): FR-008a exige degradación controlada sin fallar el turno, en lenguaje tecnológicamente neutro (sin nombrar el mecanismo concreto).
- [ ] CHK003 Is the boundary between "fallback used, turn still succeeds" (Principio IX) and "fallback also fails" defined — i.e., what happens if `TemplateGenerationAdapter` itself cannot produce a response (e.g., zero evidence)? [Gap, Contracts §GenerationPort] — **Clasificación B** (Clarify 2026-09-01): el caso "sin evidencia" ya lo cubre el flujo de "reconocer falta de información" (US2); el comportamiento exacto del adaptador de reserva ante ese caso es una decisión de `contracts`/`plan.md`.

## Fundamentación de la salida generada

- [ ] CHK004 Given `GroundingVerifierAgent` (Feature 002) uses a lexical-overlap heuristic validated against deterministic/template text, is there a requirement confirming that heuristic remains adequate against fluent LLM-generated paraphrases that could coincidentally satisfy word-overlap without being truly grounded? [Assumption, Contracts §self-study-agents.md, Spec §FR-008] — **Clasificación C** (Clarify 2026-09-01): riesgo a validar empíricamente con pruebas de integración en `tasks.md`, no un requisito a redactar de antemano.
- [x] CHK005 Is there a requirement that verifies — not merely instructs — that the model actually withheld a practice question's solution when `reveal_solution = false`, given an LLM may not reliably follow an embedded instruction? [Gap, Contracts §PracticeQuestionAgent, Spec §FR-013] — **Resuelto** (Clarify 2026-09-01): FR-013a exige un verificador independiente del generador; salida rechazada → regenerar o fallback determinista. Pendiente de reflejar en `contracts/self-study-agents.md` (nuevo agente/paso verificador) antes de `/speckit-tasks`.
- [ ] CHK006 Is "conocimiento general no recuperado de los materiales" (FR-019) defined precisely enough to distinguish it from an LLM blending trained knowledge into a nominally-grounded answer, given the generator is no longer a fixed template? [Ambiguity, Spec §FR-019] — **Clasificación D** (Clarify 2026-09-01): el veredicto de fundamentación (Feature 002, reutilizado sin cambios) juzga la salida frente a la evidencia con independencia de qué la generó — ya cubierto.

## Prompt injection documental

- [x] CHK007 Does `self-study-agents.md`/`spec.md` pair the "el texto de `evidence[].text` MUST tratarse siempre como datos" rule with a concrete acceptance scenario or test requirement, the way Feature 002's FR-028 does, or does it exist only as a contract note without a corresponding Edge Case? [Gap, Contracts §GenerationPort, Spec §Edge Cases] — **Clasificación A — Resuelto** (Clarify 2026-09-01): FR-008b añade el mismo requisito ya establecido en la Feature 002 (FR-028) para el nuevo componente de generación.

## Configuración y parámetros del modelo

- [ ] CHK008 Are bounds or defaults specified for the generation `parameters` (e.g., `temperature`, `max_tokens`) referenced in `GenerationOutcome.parameters`, or is their range left entirely unconstrained? [Clarity, Data-Model §Generación] — **Clasificación B** (Clarify 2026-09-01): parámetros de configuración del adaptador, no comportamiento observable — `plan.md`/`data-model.md`.
- [ ] CHK009 Is the behavior defined for when `ORALIA_OLLAMA_MODEL`/`ORALIA_OLLAMA_BASE_URL` are unset — does the system start with the template adapter as primary, or attempt Ollama at a default and fail over per turn? [Gap, Plan §Technical Context] — **Clasificación B** (Clarify 2026-09-01): configuración operativa del adaptador — `plan.md`.

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → adaptado de "Checklist de
  arquitectura cognitiva" y "Checklist de RAG y materiales" al componente de generación
  real introducido por primera vez en esta feature.
