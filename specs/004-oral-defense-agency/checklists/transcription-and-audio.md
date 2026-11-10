# Transcription & Audio Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Validar la calidad y completitud de los requisitos que gobiernan el ciclo
audio→transcripción provisional→revisión/corrección→transcripción definitiva, previo a
`/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md) · [data-model.md](../data-model.md)

## Distinción provisional/definitiva

- [X] CHK001 - ¿Definen los requisitos, sin ambigüedad, qué texto se considera "definitivo" cuando existe una corrección frente a cuando no existe ninguna? [Clarity, Spec §FR-009/FR-010, Research §4]
- [X] CHK002 - ¿Especifica algún requisito qué componentes (estado cognitivo, recuperación, generación, decisión de diálogo) MUST usar exclusivamente la transcripción definitiva, nunca la provisional? [Completeness, Research §4]
- [X] CHK003 - ¿Está definido el comportamiento cuando el estudiante corrige la transcripción después de que ya se generó contenido sobre la versión original (no retroactividad)? [Edge Case, Spec Edge Cases]

## Confirmación antes de cognición

- [X] CHK004 - ¿Establece `spec.md` con suficiente precisión que **ningún** componente cognitivo (recuperación, generación, verificadores, decisión de diálogo) se ejecuta antes de la confirmación/corrección de una transcripción de voz, o esa exhaustividad solo aparece en `research.md` §5? [Gap, Ambiguity, Spec §FR-022] — `spec.md` FR-022 solo exige "no generar una repregunta"; la prohibición explícita sobre recuperación/verificadores/decisión de diálogo es una precisión introducida en `research.md` que no está reflejada literalmente en el texto de la especificación. Confirmar si esta brecha de redacción es aceptable o si conviene una futura ronda de `/speckit-clarify` sobre `spec.md`.
- [X] CHK005 - ¿Define algún requisito el estado observable de un turno mientras espera confirmación (p. ej. sin `dialogue_action` asociado)? [Completeness, Research §5, Contracts]

## Baja confianza STT y segmentos dudosos

- [X] CHK006 - ¿Especifica la especificación qué mecanismos concretos se ofrecen ante baja confianza (corrección textual, cambio a texto) y cuáles se excluyen explícitamente (repetir grabación)? [Clarity, Spec §FR-022/FR-022a, Clarifications Q1]
- [X] CHK007 - ¿Están definidos los atributos mínimos que debe exponer una transcripción (texto, marcas temporales, confianza, segmentos dudosos)? [Completeness, Spec §FR-008]
- [X] CHK008 - ¿Es medible/verificable el umbral que determina "baja confianza", o queda como parámetro de configuración explícitamente delegado a implementación? [Measurability, Research §5] — aceptable como decisión de configuración (no requiere cifra en spec.md), confirmar que así se entiende.

## Fallo técnico STT y descarte de audio

- [X] CHK009 - ¿Define un requisito el comportamiento exacto ante un fallo técnico de transcripción (distinto de baja confianza), incluyendo qué ocurre con el audio ya capturado? [Completeness, Spec §FR-011a/FR-021]
- [X] CHK010 - ¿Prohíbe explícitamente algún requisito reintentar la transcripción sobre el mismo audio tras un fallo técnico? [Clarity, Spec §FR-011a, Clarifications]
- [X] CHK011 - ¿Establece la especificación, sin dejar lugar a una implementación alternativa razonable, que el audio nunca se persiste ni se referencia desde ningún registro (incluida la traza)? [Clarity, Spec §FR-011]

## Cambio a texto y equivalencia cognitiva texto/voz

- [X] CHK012 - ¿Requiere explícitamente la especificación que la modalidad textual cubra el 100% del flujo, con independencia de si la voz está habilitada? [Completeness, Spec §FR-003]
- [X] CHK013 - ¿Existe un criterio de éxito medible que verifique que el comportamiento cognitivo (repregunta, decisión de diálogo) es equivalente para una misma entrada textual definitiva, independientemente de si llegó por texto o por voz confirmada — más allá de la ausencia de arquitectura duplicada (SC-001)? [Gap, Measurability, Spec §SC-001] — SC-001 verifica que no hay una arquitectura paralela, pero no fija un criterio observable de que el *resultado* del pipeline sea indistinguible por modalidad de entrada; considerar si merece un criterio de éxito propio.

## Notes

- CHK004 y CHK013 son los únicos hallazgos con impacto real detectados en esta área —
  ambos son brechas de trazabilidad plan↔spec, no defectos de diseño (la decisión de
  `research.md` es correcta; el texto de `spec.md` simplemente no la enuncia con el
  mismo nivel de detalle).
- El resto de ítems confirma cobertura ya adecuada.
## Revalidación W0 (2026-10-16)

- CHK001–CHK005: FR-009/FR-010/FR-022, research.md §§4/5 y el contrato HTTP definen texto definitivo, gating cognitivo y awaiting_confirmation.
- CHK006–CHK010: Clarifications Q1/Q3, FR-008/FR-011a/FR-021/FR-022 y configuración del umbral cubren baja confianza y fallo técnico sin reintento.
- CHK011–CHK013: FR-003, FR-011, FR-043 y SC-011 prohíben toda persistencia/referencia de audio y prueban equivalencia texto/voz.

## Revalidación de implementación (2026-10-17)

CHK001–CHK013: `tests/integration/test_defense_voice_lifecycle.py`, `test_defense_correction_not_retroactive.py`, `test_defense_remaining_boundaries.py`, `tests/contract/test_defense_rolled_spool_lifecycle.py` y `tests/e2e/test_defense_route.spec.ts` prueban provisional/definitiva, revisión, no retroactividad, umbral configurable, fallback textual y equivalencia cognitiva.

Las rutas de pruebas son relativas a la raíz del workspace. Las cifras y comandos exactos están en `../implementation-evidence.md` y sus logs; las dos pruebas reales de modelos no se cuentan como aprobadas.

Verificación adicional: `test_defense_retention_copies.py` demuestra borrado de copias
operativas limitado a la sesión terminal propia; quedan IDs/versiones/veredictos sin
contenido. `test_defense_retention_requires_finite_policy.py` impide conservación
indefinida. `test_defense_stt_after_close.py` y `test_defense_speech_endpoint.py`
descartan resultados de voz posteriores a un cierre que eliminó contenido.

Revalidación tras auditoría independiente: la selección explícita se aplica también en
cierre automático textual y por voz confirmada; se consulta el registro completo de
turnos/originales/correcciones antes del cierre voluntario. Evidencia:
`test_defense_automatic_close_consent.py` y `test_defense_full_session.spec.ts`.
