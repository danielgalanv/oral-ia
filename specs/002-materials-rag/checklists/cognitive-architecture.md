# Requirements Quality Checklist: Arquitectura Cognitiva — Materiales autorizados y RAG trazable

**Purpose**: Validar que los nuevos agentes de esta feature (recuperación,
fundamentación) preserven la arquitectura cognitiva ya establecida: responsabilidad
única, contratos explícitos, separación recuperación/generación/decisión/verificación,
trazabilidad, degradación y sustitución de agentes sin modificar el orquestador
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Agent Responsibility & Contracts

- [x] CHK001 Is it explicit that `MaterialRetrieverAgent` and `GroundingVerifierAgent` MUST implement the same `AgentContract` shape already required by Constitution Principio II, or does the spec leave room for a divergent contract shape for these two new agents? [Consistency, Spec §Key Entities, Constitution §II]
- [x] CHK002 Are the two agents' responsibilities kept single and non-overlapping — i.e., does any requirement imply `MaterialRetrieverAgent` also judges fundamentación, or `GroundingVerifierAgent` also filters by authorization? [Clarity, Spec §FR-017..FR-019 vs §FR-021..FR-023]

## Separation of Retrieval / Generation / Decision / Verification

- [x] CHK003 Is it explicit that `GroundingVerificationResult` (this feature) and the constitutional `VerificationResult` (Feature 001) are evaluated independently, with neither verdict silently overriding the other? [Traceability, Spec §Key Entities, §FR-030]
- [x] CHK004 Does the spec avoid implying that this feature's retriever also decides the final conversational action (a decision-role responsibility reserved for Feature 003's dialogue agent)? [Scope, Spec §Assumptions]

## Non-Omissible Constitutional Controls

- [x] CHK005 Is there a requirement confirming that grounding verification (this feature) never substitutes for or bypasses the constitutional control already established in Feature 001? [Consistency, Spec §FR-030, Constitution §IX]

## Traceability, Cancellation & Degradation

- [x] CHK006 Is per-agent timeout/cancellation behavior for `MaterialRetrieverAgent`/`GroundingVerifierAgent` specified with the same rigor as Feature 001's agents (deadline honored, degrade instead of crash), or only implied by reusing "the same contract"? [Gap, Spec §FR-017]
- [x] CHK007 Is the "presupuesto temporal agotado → resultado parcial" behavior (Edge Case) distinguished clearly from a true agent timeout/failure (which would produce `status != "ok"` per Feature 001's contract), to avoid conflating a partial-but-successful result with a degraded one? [Ambiguity, Spec §Edge Cases]

## Non-Regression (This Feature's Own Explicit Requirement)

- [x] CHK008 Is FR-025/FR-030 ("MUST NOT modificar el comportamiento ya validado de la Feature 001") paired with any concrete, checkable boundary (e.g., a named list of files/contracts that must not change), or is it only a general intent statement? [Measurability, Spec §FR-030]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de arquitectura
  cognitiva", recortada a los aspectos que esta feature realmente introduce (dos agentes
  nuevos y su separación de responsabilidades), sin repetir ítems ya cubiertos por la
  auditoría de la Feature 001.
