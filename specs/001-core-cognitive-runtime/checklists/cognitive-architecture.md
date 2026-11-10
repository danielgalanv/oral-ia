# Requirements Quality Checklist: Arquitectura Cognitiva — Núcleo cognitivo y ejecución local

**Purpose**: Validar que los requisitos preserven la arquitectura cognitiva (responsabilidad
única de agentes, contratos explícitos, mensajes estructurados, estado externo al LLM,
composición de agencias, separación recuperación/generación/decisión/verificación,
controles constitucionales no omitibles, memoria diferenciada, trazabilidad, cancelación,
degradación y sustitución de agentes)
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Agent Responsibility & Contracts

- [ ] CHK001 Is "responsabilidad única" for an agent defined with a boundary test (what one agent may vs. may not do), or only asserted generally? [Clarity, Spec §FR-004, Constitution §II]
- [ ] CHK002 Are all fields required in AgentContract (Constitution §II list) reflected in the functional requirements/data model, or only partially enumerated? [Completeness, Spec §FR-004, data-model.md §AgentContract]
- [ ] CHK003 Are the criteria for "mismo contrato" (what must match for agent substitutability) enumerated, or left to interpretation? [Clarity, Spec §FR-005, §SC-001]
- [ ] CHK004 Does the spec state a requirement that an agent can be replaced by another agent honoring the same contract without changing any Agency or orchestrator code — not just imply it via a success criterion? [Traceability, Spec §SC-008]

## Structured Messaging & State

- [ ] CHK005 Is the structured shape of InternalMessage fully specified (all fields from Constitution §II), leaving no field to be inferred at implementation time? [Completeness, Spec §FR-007]
- [ ] CHK006 Is "estado externo al LLM" paired with a verifiable non-negotiable rule (e.g., no state field may only exist inside a prompt), or just stated as intent? [Measurability, Spec §FR-008, Constitution §III]
- [ ] CHK007 Are read/write access rules to the cognitive state specified per agent role (who may propose a patch vs. who may read it), or left implicit? [Gap, data-model.md §StatePatch]
- [ ] CHK008 Is the conflict-detection rule for concurrent state writes (US5) specified independently of any particular storage mechanism? [Scope, Spec §FR-019]

## Agency Composition

- [ ] CHK009 Is the process for composing an agency (selecting existing agents, no new code) bounded by an explicit requirement, distinguishing it from ad hoc orchestration logic? [Clarity, Spec §FR-006]
- [ ] CHK010 Are the roles retriever/generator/verifier/decider/presenter each required to be a distinct step, or could a single step legally combine generator+verifier under the current wording? [Ambiguity, contracts/agent-contract.md §ExecutionStep]

## Separation of Retrieval / Generation / Decision / Verification

- [ ] CHK011 Is the rule "el agente generador nunca puede aprobar su propia salida" (Constitution §IV) restated as a checkable requirement in this feature's spec, or only assumed via the contract document? [Traceability, Spec §FR-014, Constitution §IV]
- [ ] CHK012 Are requirements defined for what a verifier does with an "incertidumbre"/uncertainty verdict distinct from "bloquear", matching all verdict types implied by Constitution §IV? [Coverage, contracts/agent-contract.md §VerificationResult]

## Non-Omissible Constitutional Controls

- [ ] CHK013 Are the conditions under which a constitutional control may be skipped explicitly stated as "never", with no configuration escape hatch? [Consistency, Spec §FR-014, Constitution §IX]

## Memory Differentiation

- [ ] CHK014 Are the five memory categories (trabajo/episódica/semántica/procedimental/metacognitiva) each mapped to at least one concrete field or entity in the spec, or are some only named without a home? [Completeness, Spec §FR-009, Spec §Key Entities → Memory]

## Traceability, Cancellation & Degradation

- [ ] CHK015 Is "trazabilidad completa de un turno" defined by an explicit minimum field list, or only by example? [Clarity, Spec §FR-016]
- [ ] CHK016 Are cancellation requirements specified per agent (what must happen to in-flight work when cancelled), beyond "timeout produces degradation"? [Gap, Spec §FR-018]
- [ ] CHK017 Is the boundary between "degradación controlada" and "fallo de sesión" (when a degraded turn becomes a closed_error_safe session) defined with a concrete rule? [Ambiguity, Spec §User Story 4]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de arquitectura
  cognitiva".
- Este checklist es el más directamente ligado al propósito de la Feature 001; una
  respuesta "no" en varios ítems aquí es un riesgo de severidad alta para la hipótesis
  arquitectónica del proyecto (Constitution §X).
