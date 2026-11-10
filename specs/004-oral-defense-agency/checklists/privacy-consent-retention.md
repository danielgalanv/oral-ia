# Privacy, Consent & Retention Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Validar la calidad de los requisitos de privacidad, consentimiento y
retención, previo a `/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md) · [data-model.md](../data-model.md)

## Almacenamiento operativo vs. conservación

- [X] CHK001 - ¿Anticipa algún requisito de `spec.md` que datos como la transcripción deban existir en almacenamiento **durante** la sesión por necesidad operativa, con independencia de si su conservación posterior está autorizada? [Clarity, Spec §FR-028/FR-031, Research §4/§15] — `spec.md` no distingue explícitamente "persistencia operativa de sesión" de "conservación posterior al cierre"; la distinción es una precisión de `research.md`. No contradice la especificación, pero merece confirmarse como lectura correcta antes de generar tareas de persistencia.
- [X] CHK002 - ¿Deja claro algún requisito que esta persistencia operativa no equivale a consentimiento de conservación? [Consistency, Research §15]

## `ConsentRecord` — semántica exacta

- [X] CHK003 - ¿Especifica la especificación quién decide (el participante) y cuándo (al cierre) se toma la decisión de conservar o eliminar los datos de la sesión? [Completeness, Spec §FR-030]
- [X] CHK004 - ¿Excluye explícitamente algún requisito la interpretación de que el consentimiento de conservación sea una condición para participar en o completar la sesión? [Ambiguity, Research §15] — no existe una lectura alternativa razonable en `spec.md` (el disclosure de FR-004 ya cubre "consentir participar"), pero `spec.md` tampoco lo distingue explícitamente de "consentir conservar"; confirmar que la distinción, hecha en `research.md`, no era necesaria a nivel de especificación por ser ya inequívoca.
- [X] CHK005 - ¿Define un requisito qué subconjunto de datos puede conservarse de forma independiente (p. ej. transcripción sin resumen, o viceversa)? [Completeness, Data Model §ConsentRecord.scope]

## Comportamiento `retain`/`delete`

- [X] CHK006 - ¿Está definido el efecto inmediato de elegir "eliminar" al cierre (no depender de una purga diferida)? [Clarity, Research §15]
- [X] CHK007 - ¿Está definido qué ocurre por defecto cuando la actividad no autoriza en absoluto la conservación (sin necesidad de que el participante decida nada)? [Completeness, Spec §FR-028]

## `RetentionPolicy` y purga de datos expirados

- [X] CHK008 - ¿Reutiliza la especificación explícitamente el mecanismo de retención ya existente en vez de introducir un sistema paralelo? [Consistency, Spec §FR-031]
- [X] CHK009 - ¿Exige un requisito que los datos conservados y ya expirados sean eliminables mediante un mecanismo de purga, sin fijar un número de días no derivado de la configuración? [Completeness, Measurability, Spec §FR-031]
- [X] CHK010 - ¿Está acotado explícitamente el alcance de la purga a los datos propios de esta feature, sin tocar datos de sesión de las Features 001–003? [Consistency, Research §1/§15]

## `TranscriptCorrection` y ausencia de perfiles longitudinales

- [X] CHK011 - ¿Especifica un requisito que la corrección de transcripción coexiste con el original cuando la sesión se conserva, sin sustituirlo? [Clarity, Spec §FR-010]
- [X] CHK012 - ¿Prohíbe explícitamente algún requisito agregar o correlacionar información de defensa oral entre sesiones distintas del mismo `participant_code`? [Clarity, Spec §FR-032]

## Ausencia total de conservación de audio

- [X] CHK013 - ¿Es inequívoco que el audio queda completamente fuera de la lógica de consentimiento/retención — nunca conservable bajo ninguna configuración de esta feature? [Clarity, Spec §FR-011]

## Notes

- Ningún hallazgo de severidad alta en esta área — la corrección de consistencia previa
  ya alineó `research.md`/`data-model.md` con `spec.md`. CHK001/CHK004 quedan marcados
  como brechas menores de trazabilidad (la especificación es compatible con las
  precisiones de `research.md`, pero no las enuncia con el mismo detalle) — no bloquean
  `/speckit-tasks`.
## Revalidación W0 (2026-10-16)

- CHK001–CHK005: FR-010 y FR-030 distinguen persistencia operativa, consentimiento al cierre, participación y scopes transcript/summary.
- CHK006–CHK010: FR-030/FR-031 y research.md §15 fijan eliminación inmediata, default sin retención, purga finita y aislamiento de Features 001–003.
- CHK011–CHK013: FR-010, FR-011 y FR-032 conservan original+corrección, prohíben correlación y excluyen audio bajo toda configuración.

## Revalidación de implementación (2026-10-17)

CHK001–CHK013: `tests/contract/test_defense_end_consent.py`, `test_defense_rolled_spool_lifecycle.py`, `tests/integration/test_defense_retention_and_purge.py`, `test_defense_close_transition_outcome.py` y `test_defense_session_isolation.py` prueban scopes cerrados, eliminación inmediata, caducidad, original/corrección, aislamiento y audio efímero.

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
