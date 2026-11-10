# Requirements Quality Checklist: No Evaluación Académica — Núcleo cognitivo y ejecución local

**Purpose**: Detectar si los requisitos permiten, por omisión o ambigüedad, evaluación
académica explícita o encubierta (notas, juicios de capacidad, clasificación del
participante)
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Explicit Grading & Academic Decisions

- [ ] CHK001 Is there an explicit requirement prohibiting any agent output from assigning a grade or score, beyond the general constitutional principle? [Traceability, Spec §FR-014, Constitution §I]
- [ ] CHK002 Are the specific phrases/patterns considered "decisión académica" enumerated or exemplified, or left fully open to interpretation by whoever implements the constitutional control? [Clarity, Spec §FR-014]
- [ ] CHK003 Is the blocked-output requirement (FR-015) explicit that the block applies regardless of which agent or agency produced the prohibited content, not just the "agente generador" example given in User Story 3? [Coverage, Spec §FR-014, §User Story 3]
- [ ] CHK004 Are requirements present for logging *why* an output was judged as an academic decision (a traceable reason), so the block isn't a silent/unexplained rejection? [Traceability, Spec §FR-015]

## Descriptive-Only Summaries

- [ ] CHK005 Is the technical summary (FR-012b) required to be strictly descriptive (topics, incidents, duration) with an explicit prohibition on any judgment of participant ability? [Clarity, Spec §FR-012b, §Assumptions]

## Hidden Classification Signals

- [ ] CHK006 Are requirements defined preventing an internal signal (e.g., a future "dificultad orientativa") from being surfaced as a participant classification in this feature? [Gap, Constitution §Governance "Evaluación"]
- [ ] CHK007 Is there a requirement that confidence values (Turn/VerificationResult/InternalMessage confidence fields) are documented as *not* representing confidence in the participant's ability? [Ambiguity, data-model.md §Turn, §VerificationResult]

## Success Criteria Framing

- [ ] CHK008 Are success criteria (SC-001…SC-008) worded so that none of them could be read as measuring participant performance rather than system/architecture behavior? [Consistency, Spec §Success Criteria, Constitution §X]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de no evaluación
  académica".
- Este checklist es de severidad alta por defecto: cualquier "no" aquí toca un límite
  institucional no negociable (Constitution Principio I).
