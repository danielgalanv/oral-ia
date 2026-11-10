# Follow-up Dialogue Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Validar la calidad de los requisitos sobre pregunta inicial, repreguntas,
aclaración y la política de diálogo resultante, previo a `/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md) · [contracts/defense-agents.md](../contracts/defense-agents.md)

## Diferencia pregunta inicial / repregunta / aclaración

- [X] CHK001 - ¿Define la especificación, de forma funcional, en qué se diferencia una "pregunta inicial" de una "repregunta"? [Clarity, Spec §FR-001a-equivalente/User Story 1]
- [X] CHK002 - ¿Tiene la especificación un requisito o escenario de aceptación que describa el disparador cognitivo de `clarify` (ambigüedad semántica de una respuesta ya definitiva), distinto del mecanismo de confirmación por baja confianza de transcripción (User Story 5)? [Gap, Conflict, Spec User Story 5, Research §9/§10] — tras la corrección de consistencia, `research.md` introduce un disparador de `DialogueAction.clarify` basado en ambigüedad semántica de la respuesta del estudiante (`concepts_mentioned` vacío o contradicción detectada) que **no** tiene ninguna User Story ni FR propios en `spec.md` — la única "aclaración" descrita en la especificación (US5) es la de baja confianza de transcripción, que la corrección reclasificó como *no* cognitiva. Esto deja una capacidad de diseño (`clarify` semántico) sin respaldo directo en un requisito funcional verificable de `spec.md`.
- [X] CHK003 - Si CHK002 se confirma como gap: ¿debería resolverse añadiendo un FR/escenario a `spec.md` en una futura ronda de `/speckit-clarify`, o es suficiente con que quede documentado en `research.md` como refinamiento de diseño? [Ambiguity] — marcado para decisión explícita antes de generar tareas de implementación para esta rama del diálogo.

## Relevancia y no repetición de repreguntas

- [X] CHK004 - ¿Es verificable "relevante" sin depender de comparación literal de texto, según lo exige la especificación? [Measurability, Spec §SC-005]
- [X] CHK005 - ¿Define un requisito qué ocurre cuando una repregunta candidata resulta repetida (reintento, alternativa, reconocimiento de límite)? [Completeness, Spec §FR-015]
- [X] CHK006 - ¿Se apoya la verificación de no-repetición en el mismo alcance ya validado (turno inmediatamente anterior) o en todo el historial, y está esa elección justificada frente a falsos positivos? [Consistency, Research §9]

## Profundizar vs. cambiar de tema

- [X] CHK007 - ¿Distingue la especificación, en términos funcionales (no de implementación), entre profundizar en el mismo tema y cambiar a un tema distinto? [Clarity, Spec §FR-018]
- [X] CHK008 - ¿Está acotado el cambio de tema al alcance autorizado de la actividad, con un comportamiento explícito para la petición fuera de alcance? [Completeness, Spec §FR-023/Edge Cases]
- [X] CHK009 - ¿Confirma la especificación que no se introduce una acción de diálogo nueva para representar el cambio de tema? [Consistency, Spec Clarifications Q4]

## `acknowledge_missing_info` y ausencia de evaluación

- [X] CHK010 - ¿Existe un requisito explícito (no solo una decisión de `research.md`) que cubra qué ocurre cuando no puede fundamentarse una repregunta relevante contra la evidencia disponible? [Gap, Spec, Research §9] — `research.md` §9 resuelve este caso con `acknowledge_missing_info`, pero `spec.md` no contiene un FR dedicado a "repregunta sin fundamento suficiente" (a diferencia de FR-013/FR-014, que describen el caso positivo). Confirmar si el FR de recuperación documental (FR-013) se considera suficiente cobertura implícita.
- [X] CHK011 - ¿Prohíbe explícitamente la especificación que una repregunta produzca valoración, puntuación o comentario sobre el rendimiento del estudiante? [Clarity, Spec §FR-025/FR-026]
- [X] CHK012 - ¿Está claro que la decisión final de diálogo corresponde al compositor de la agencia y no al generador de la repregunta? [Consistency, Principio IV, Contracts]

## Finalización

- [X] CHK013 - ¿Distingue la especificación entre finalización voluntaria y finalización automática por límite alcanzado, con un comportamiento observable para cada una? [Completeness, Spec §FR-019/FR-028]

## Notes

- **Hallazgo principal**: CHK002/CHK003 — el disparador semántico de `clarify`
  (introducido durante la corrección de consistencia de `research.md`) no tiene
  respaldo directo en un FR/User Story de `spec.md`. Es una brecha de **trazabilidad
  spec↔plan**, no un defecto del diseño en sí.
- CHK010 es un gap secundario de menor impacto (cobertura implícita razonable, pero no
  explícita).
## Revalidación W0 (2026-10-16)

- CHK001–CHK003: US1, FR-014 y FR-018b separan pregunta inicial, repregunta y clarify cognitivo.
- CHK004–CHK006: FR-015, SC-005, research.md §9 y T018/T023 definen relevancia estructural y regeneración acotada.
- CHK007–CHK009: FR-018/FR-018a/FR-023 definen cambio de tema mediante ask y su alcance.
- CHK010–CHK013: FR-025–FR-026, FR-037, contracts/defense-agents.md y FR-019/FR-028 cubren falta de evidencia, no evaluación, decisión del compositor y cierre.

## Revalidación de implementación (2026-10-17)

CHK001–CHK013: `tests/integration/test_defense_initial_material_question.py`, `test_defense_text_full_session.py`, `test_defense_dialogue_contract.py`, `test_defense_session_isolation.py` y `tests/unit/test_defense_relevance_structural.py` prueban inicial, referencia estructural, cambio autorizado/409, contradicción, regeneración única y cierres.

Las rutas de pruebas son relativas a la raíz del workspace. Las cifras y comandos exactos están en `../implementation-evidence.md` y sus logs; las dos pruebas reales de modelos no se cuentan como aprobadas.
