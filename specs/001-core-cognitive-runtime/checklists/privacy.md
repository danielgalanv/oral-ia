# Requirements Quality Checklist: Privacidad y Datos — Núcleo cognitivo y ejecución local

**Purpose**: Validar privacidad por diseño en los requisitos de esta feature: minimización,
seudonimización, exposición de red, secretos y logs, texto no confiable, y ausencia de
perfiles. Los ítems específicos de audio/voz del prompt de referencia se excluyen aquí
porque esta feature no procesa audio (ver Notes).
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Minimization & Pseudonymization

- [ ] CHK001 Is data minimization for ParticipantCode specified with a concrete "must not contain" rule, or only a general principle? [Clarity, Spec §FR-023]
- [ ] CHK002 Are pseudonymization validation rules (rejecting name-like codes) specific enough to be implemented consistently, or left to heuristic judgment without a testable boundary? [Measurability, Spec §Edge Cases]
- [ ] CHK003 Is the separation between ParticipantCode and any real identity addressed as a requirement for this feature, given no institutional identity integration exists yet? [Consistency, Spec §FR-022, §FR-023]

## Session Lifecycle & Retention

- [ ] CHK004 Is "sesión efímera" (a session that leaves no persistent trace beyond in-memory execution) addressed for this feature, or is it explicitly deferred with a stated reason? [Gap / Assumption, Spec §Assumptions]
- [ ] CHK005 Are retention requirements for TraceEvent and StatePatch records specified (how long they persist, who can purge them), or only implied by RetentionPolicy belonging to ActivityConfiguration? [Completeness, data-model.md §RetentionPolicy]
- [ ] CHK006 Are requirements defined for participant-initiated data access or deletion requests within this feature, or is that explicitly deferred to a later feature? [Gap / Scope, Constitution §VI]

## Network Exposure & Secrets

- [ ] CHK007 Are network-exposure requirements (bind to 127.0.0.1 only) stated as a MUST with no configuration path to widen exposure in this feature? [Clarity, Spec §FR-022]
- [ ] CHK008 Are requirements defined for how secrets (if any, e.g., a future admin credential) must be excluded from logs and TraceEvent payloads? [Gap, Spec §FR-021a, §FR-024]
- [ ] CHK009 Is "no almacenar cadenas de razonamiento privadas del modelo" paired with a concrete definition of what counts as private reasoning vs. structured/observable output? [Ambiguity, Spec §FR-024]

## Untrusted Input

- [ ] CHK010 Are requirements for handling free-text participant input as untrusted data (not able to alter system policies or configuration) present for this feature's turn-processing flow? [Gap, plan.md §Seguridad y privacidad]

## Scope Boundary (Voice/Audio — deferred)

- [ ] CHK011 Is the exclusion of audio/transcript handling from this feature's privacy requirements stated explicitly, so it isn't mistaken for an oversight? [Scope, Spec §Fuera de alcance]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de privacidad y
  datos". Ítems sobre audio temporal, transcripción original/corregida y exportación se
  omiten en esta feature porque `spec.md` los excluye explícitamente del alcance
  ("Fuera de alcance de esta feature"); revisar de nuevo al planificar la Feature 004
  (voz) y la Feature 005 (privacidad/exportación).
