# Traceability & State Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Validar que los requisitos permiten reconstruir la cadena completa de un
turno de defensa y que preservan `CognitiveState` como estado operativo (nunca
`TraceEvent`), previo a `/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md) · [data-model.md](../data-model.md)

## Cadena de reconstrucción completa

- [X] CHK001 - ¿Exige un criterio de éxito medible que el 100% de las sesiones (voluntarias y por límite) produzcan una traza completa reconstruible? [Measurability, Spec §SC-007]
- [X] CHK002 - ¿Está enumerada, en algún artefacto, la secuencia completa que MUST poder reconstruirse (pregunta→modalidad→STT→provisional→corrección→definitiva→estado→recuperación→agentes→generación→verificadores→decisión→salida→TTS)? [Completeness, Research §17]
- [X] CHK003 - ¿Se apoya esa reconstrucción en el mecanismo de trazabilidad genérico ya existente (`TraceEvent`/`event_type`), o requiere un mecanismo de reconstrucción nuevo y distinto? [Consistency, Spec §FR-033, Research §1/§17]

## `CognitiveState` como estado operativo

- [X] CHK004 - ¿Define algún requisito que las decisiones de la agencia de defensa se toman sobre `CognitiveState`, nunca reconstruyendo el estado a partir de la traza? [Clarity, Research §11/§17 (principio heredado de Feature 003)]
- [X] CHK005 - ¿Especifica qué conceptos operativos (pregunta actual, respuesta definitiva, conceptos tratados/pendientes, objetivo, siguiente acción) MUST ser conocidos estructuralmente por la agencia en todo momento del turno? [Completeness, Research §11]
- [X] CHK006 - ¿Excluye explícitamente algún requisito que el audio o el contenido íntegro de turnos anteriores formen parte de lo que se reenvía a un componente de generación? [Clarity, Spec §FR-010/FR-011]

## No duplicidad de fuente de verdad

- [X] CHK007 - ¿Aclara algún requisito o decisión de diseño que la traza es una copia de auditoría, no la fuente de verdad de la decisión ya tomada? [Consistency, Research §17] — heredado del mismo principio ya aplicado en la Feature 003; no requiere un FR propio en esta feature, pero conviene confirmar que ningún requisito de `spec.md` sugiere lo contrario.
- [X] CHK008 - ¿Existe algún requisito ambiguo que pudiera interpretarse como si la reconstrucción de sesión dependiera de reprocesar la traza para decidir el siguiente paso (en vez de solo para auditoría/reconstrucción posterior)? [Ambiguity] — no se detecta tal ambigüedad en `spec.md`; ítem de confirmación.

## Alineación entre eventos de traza y acciones de diálogo

- [X] CHK009 - ¿Es coherente el conjunto de eventos de traza nuevos definidos (`transcription_recorded`, `transcript_corrected`, `transcription_failed`, `followup_question_generated`, `tts_failed`, `defense_session_summary`, `consent_recorded`) con las fases del flujo descritas en la especificación, sin huecos ni duplicados evidentes? [Consistency, Data Model §Eventos de traza nuevos]
- [X] CHK010 - ¿Refleja la especificación, sin ambigüedad, que los eventos de modalidad (STT/TTS) y los eventos de decisión cognitiva son categorías distintas dentro de la traza? [Consistency, Research §5/§10 tras la corrección de consistencia]

## Notes

- Ningún hallazgo de severidad alta — el mecanismo de trazabilidad hereda íntegramente
  el ya validado en la Feature 001 y solo añade `event_type` nuevos, lo que reduce el
  riesgo de inconsistencia estructural.
## Revalidación W0 (2026-10-16)

- CHK001–CHK003: SC-007 y research.md §17 enumeran la cadena reconstruible sobre TraceEvent.
- CHK004–CHK008: research.md §§11/17 mantiene CognitiveState como fuente de verdad, limita contexto y define la traza como auditoría.
- CHK009–CHK010: data-model.md y research.md §§5/10/17 separan y cubren eventos de modalidad y decisión cognitiva.

## Revalidación de implementación (2026-10-17)

CHK001–CHK010: `tests/integration/test_defense_text_full_session.py`, `test_defense_voice_lifecycle.py`, `test_defense_correction_not_retroactive.py`, `tests/e2e/test_defense_full_session.spec.ts` y la puerta T090 prueban StatePatch, identidad de catálogo, propuesta/veredicto, fuentes, decisiones, versiones y reconstrucción por sesión. El generador recibe solo pregunta previa y respuesta actual, nunca el historial íntegro ni audio.

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
