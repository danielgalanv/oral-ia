# Degradation Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Validar que los requisitos cubren de forma completa y consistente cada vía
de fallo/degradación del turno de defensa, previo a `/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md)

## STT/TTS no disponibles

- [X] CHK001 - ¿Define un requisito el comportamiento cuando STT no está configurado en absoluto (a diferencia de fallar en tiempo de ejecución)? [Completeness, Research §2] — cubierto como decisión de plan ("la actividad no puede habilitar voz"); confirmar si `spec.md` debería anticiparlo explícitamente o si es correcto dejarlo como decisión de configuración no normativa a nivel de especificación.
- [X] CHK002 - ¿Distingue la especificación el fallo de captura/transcripción (FR-021) del fallo de síntesis de voz (FR-024), con un comportamiento propio para cada uno? [Consistency, Spec §FR-021/FR-024]
- [X] CHK003 - ¿Especifica un requisito que un fallo de síntesis de voz nunca degrada el contenido del turno, solo su modalidad de presentación? [Clarity, Spec §FR-024]

## Generación de texto (`GenerationPort`) no disponible

- [X] CHK004 - ¿Contiene la especificación un requisito explícito de que la generación de la pregunta inicial o de una repregunta está sujeta a degradación controlada (sin fallar el turno), análogo al ya exigido para STT/TTS? [Gap, Spec §FR-021/FR-024 vs. ausencia de equivalente para generación] — `spec.md` especifica degradación explícita para fallos de voz (FR-021/FR-024), pero no contiene un FR equivalente y explícito para un fallo del mecanismo de generación de texto en sí (más allá de heredar implícitamente el Principio IX). Dado que esta feature reutiliza `GenerationPort`/`execute_agency` sin cambios, el comportamiento ya está garantizado a nivel de plataforma — pero conviene confirmar si merece su propia línea de requisito en `spec.md`, como ya lo tuvo la Feature 003 (FR-008a), para que la garantía sea verificable directamente desde la especificación y no solo por herencia.
- [X] CHK005 - ¿Es reutilizado explícitamente, según los requisitos, el mismo mecanismo de reserva determinista ya validado, en vez de introducir uno nuevo específico de esta feature? [Consistency, Spec §FR-033, Research §1/§2]

## Evidencia insuficiente y conflicto entre verificadores

- [X] CHK006 - ¿Define un requisito el comportamiento cuando no puede fundamentarse una repregunta relevante contra la evidencia disponible? [Completeness, Spec §FR-013, Research §9] — ver también follow-up-dialogue.md CHK010 (mismo hallazgo, distinta perspectiva).
- [X] CHK007 - ¿Contiene la especificación un requisito (no solo un Edge Case) que exija combinar explícitamente los veredictos de fundamentación y coherencia cuando difieren? [Gap, Consistency, Spec Edge Cases] — el comportamiento aparece como Edge Case ("¿Qué ocurre si el verificador de fundamentación y el de coherencia emiten veredictos distintos...?") pero no como un FR numerado, a diferencia del resto de comportamientos equivalentes de esta misma especificación (p. ej. FR-023 para cambio de tema fuera de alcance). Confirmar si el Edge Case por sí solo se considera suficientemente normativo para `/speckit-tasks`.

## Fallo de `FollowUpQuestionAgent` y agentes no esenciales

- [X] CHK008 - ¿Cubre algún requisito el fallo técnico (no solo la insuficiencia de evidencia) del propio generador de repreguntas? [Ambiguity] — el Edge Case sobre "agente no esencial... por ejemplo, síntesis de voz" no aclara si `FollowUpQuestionAgent` (la única pieza cognitiva genuinamente nueva) se considera "esencial" o "no esencial" a estos efectos, dado que sin repregunta no hay continuación de la defensa. Relacionado con CHK004.
- [X] CHK009 - ¿Especifica un requisito que la degradación de un agente no esencial no interrumpe el resto de la sesión? [Clarity, Spec Edge Cases]

## Límites de sesión

- [X] CHK010 - ¿Define la especificación, sin fijar cifras concretas, el comportamiento al alcanzar el límite de turnos o duración? [Completeness, Spec §FR-019/FR-028]
- [X] CHK011 - ¿Distingue un requisito la finalización automática de la voluntaria, con la misma garantía de cierre válido + resumen + traza reconstruible para ambas? [Consistency, Spec §SC-007]

## Integridad de la sesión durante la degradación

- [X] CHK012 - ¿Prohíbe explícitamente algún requisito que el sistema genere contenido a partir de una transcripción no confirmada o de datos inválidos? [Clarity, Spec §FR-022]
- [X] CHK013 - ¿Garantiza un requisito que ninguna vía de degradación provoca pérdida del estado ya alcanzado en la sesión? [Clarity, Spec §FR-021]

## Notes

- **Hallazgo principal**: CHK004/CHK007/CHK008 — la especificación cubre con detalle la
  degradación de las capacidades *nuevas* de esta feature (voz), pero delega en
  herencia implícita (Principio IX, FR-033) la degradación del *núcleo* generativo
  reutilizado (repregunta/pregunta inicial), sin un FR propio equivalente al FR-008a de
  la Feature 003. No es un defecto de diseño (el mecanismo subyacente sí está
  garantizado por la reutilización), pero reduce la trazabilidad directa
  spec→comportamiento para esta rama concreta.
## Revalidación W0 (2026-10-16)

- CHK001–CHK003: FR-003, FR-021, FR-024 y contracts/defense-agents.md distinguen ausencia, fallo STT y fallo TTS.
- CHK004–CHK009: FR-037 y T019–T021 fijan alternativas autorizadas, fallo total, conflicto de verificadores y continuidad.
- CHK010–CHK013: FR-019, FR-021, FR-022, FR-028 y SC-007 fijan límites, cierre, veto cognitivo previo y conservación del estado.

## Revalidación de implementación (2026-10-17)

CHK001–CHK013: `tests/failure/test_defense_generation_degradation.py`, `test_defense_speech_exceptions.py`, `test_defense_worker_request_lifetime.py`, `test_defense_speech_timeout_late_results.py` y `tests/integration/test_defense_text_full_session.py` cubren reserva, agotamiento, STT/TTS, continuidad, límites y descarte tardío.

Las rutas de pruebas son relativas a la raíz del workspace. Las cifras y comandos exactos están en `../implementation-evidence.md` y sus logs; las dos pruebas reales de modelos no se cuentan como aprobadas.
