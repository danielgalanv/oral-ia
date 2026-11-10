# Requirements Quality Checklist: Accesibilidad — Núcleo cognitivo y ejecución local

**Purpose**: Validar los requisitos de accesibilidad textual/teclado de esta feature. Los
ítems de voz del prompt de referencia ("Checklist de voz y accesibilidad") se excluyen
porque la voz está fuera de alcance de esta feature (ver Notes).
**Created**: 2026-07-21
**Feature**: [spec.md](../spec.md)

## Text & Keyboard Equivalence

- [ ] CHK001 Are keyboard-navigation requirements specified for both the participant and técnica/docente areas, or only asserted generally for "la interfaz"? [Completeness, Spec §FR-021, Constitution §VII]
- [ ] CHK002 Are accessible-label and contrast requirements quantified (e.g., referencing a standard) or left as an unqualified goal? [Clarity, Constitution §VII]
- [ ] CHK003 Are pacing/control requirements (pause, repetition) addressed for the text-only interaction flow of this feature, given voice is out of scope? [Gap, Spec §Assumptions]

## Error & Disclosure Messaging

- [ ] CHK004 Are error-message comprehensibility requirements specified with concrete criteria (e.g., plain language, actionable next step), or only described qualitatively? [Clarity, Spec §Edge Cases]
- [ ] CHK005 Are requirements defined for how the "aviso de sistema automático" (FR-010) is presented accessibly (not solely via a visual-only cue)? [Gap, Spec §FR-010]

## Time & Turn Limits

- [ ] CHK006 Is there a requirement covering what happens if a participant cannot complete a turn within the configured time/turn limits due to needing more time for accessibility reasons, or is this left unaddressed? [Gap, Edge Case]

## Scope Boundary (Voice — deferred)

- [ ] CHK007 Does the spec explicitly confirm that voice-specific accessibility items (STT confidence, audio discard, TTS fallback, biometría) are out of scope for this feature rather than silently omitted? [Scope, Spec §Fuera de alcance]

## Notes

- Fuente: `docs/ORAL-IA_SpecKit/12_checklist_prompts.md` → "Checklist de voz y
  accesibilidad", recortada a los ítems de accesibilidad textual/teclado aplicables a
  esta feature. Los ítems de voz (STT/TTS, confianza, segmentos dudosos, descarte de
  audio, biometría) se revisarán al planificar la Feature 004.
