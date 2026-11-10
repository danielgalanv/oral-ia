# No-Evaluation Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Buscar cualquier requisito que pueda permitir, directa o indirectamente,
evaluación académica, scoring o inferencia de capacidad, previo a `/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md)

## Prohibiciones directas

- [X] CHK001 - ¿Prohíbe explícitamente algún requisito que el sistema produzca o muestre una nota, calificación o puntuación en cualquier momento de la sesión? [Clarity, Spec §FR-025]
- [X] CHK002 - ¿Prohíbe explícitamente algún requisito una afirmación de que el participante ha aprobado o suspendido? [Clarity, Spec §FR-025]
- [X] CHK003 - ¿Exige un requisito que el control constitucional bloquee y sustituya cualquier propuesta con contenido evaluativo, en vez de simplemente omitirlo? [Completeness, Spec §FR-026]

## Inferencia indirecta de capacidad

- [X] CHK004 - ¿Prohíbe un requisito inferir o almacenar un perfil de capacidad, nivel o desempeño a partir de las respuestas, correcciones de transcripción o historial de la sesión? [Clarity, Spec §FR-027]
- [X] CHK005 - ¿Enumera la especificación, o deja ambiguo, si métricas operativas concretas (confianza de transcripción, número de aclaraciones/repreguntas, duración de la sesión, incidencias técnicas) están explícitamente incluidas dentro de la prohibición de FR-027, o si esta queda implícita bajo "historial de la sesión"? [Ambiguity, Spec §FR-027] — FR-027 prohíbe inferir capacidad "a partir de sus respuestas, correcciones de transcripción, o historial de la sesión"; no menciona por nombre duración, número de repreguntas/aclaraciones, ni confianza STT como señales específicamente vedadas. Es una lectura razonable que "historial de la sesión" ya las cubre, pero al ser un área de riesgo señalada explícitamente, conviene confirmar que esa lectura amplia es la intencionada antes de implementar el resumen y cualquier métrica derivada.
- [X] CHK006 - ¿Existe algún requisito o Key Entity que use el término "confianza" (de transcripción o de recuperación) de forma que pudiera confundirse con confianza en la capacidad del estudiante? [Consistency, Spec Assumptions/`14_domain_model.md`] — el propio glosario del proyecto ya distingue ambos sentidos explícitamente; confirmar que ningún FR de esta feature reintroduce la ambigüedad.

## Resumen descriptivo

- [X] CHK007 - ¿Enumera la especificación de forma cerrada qué puede y qué no puede contener el resumen de sesión? [Completeness, Spec §FR-029]
- [X] CHK008 - ¿Exige un requisito que las incidencias del resumen se describan como hechos observables del sistema (tipo, acción de recuperación), nunca como caracterización del estudiante? [Clarity, Spec §FR-029a]
- [X] CHK009 - ¿Es el resumen, según los requisitos, generado por un mecanismo determinista a partir de hechos ya persistidos, o queda abierta la posibilidad de que un componente generativo redacte texto libre sobre la sesión (con el riesgo de fuga evaluativa que eso implicaría)? [Gap, Ambiguity, Spec §FR-029, Research §14] — `research.md` §14 decide explícitamente que el resumen se construye por código determinista, nunca por LLM; `spec.md` no descarta expresamente la alternativa (no dice "el resumen MUST generarse sin invocar un modelo de lenguaje"). Es una garantía importante para la ausencia de evaluación encubierta que actualmente solo vive en `research.md`, no en un MUST de `spec.md`.

## Repreguntas y preguntas

- [X] CHK010 - ¿Prohíbe un requisito que la generación de preguntas/repreguntas produzca comentario sobre el rendimiento del estudiante? [Clarity, Spec §FR-025/FR-026 aplicado a User Story 4/6]
- [X] CHK011 - ¿Distingue la especificación entre "usar la respuesta para decidir el siguiente paso" (permitido) y "calificar la respuesta" (prohibido)? [Clarity, Spec User Story 4 (heredado del principio ya aplicado en autoestudio)]

## Notes

- **Hallazgo de mayor impacto**: CHK009 — la garantía de que el resumen es
  puramente determinista (sin LLM) es una decisión de `research.md` que convendría
  reforzar como requisito explícito de `spec.md`, dado que es la salvaguarda estructural
  clave contra un "resumen evaluativo encubierto" (la propia área de riesgo señalada).
- CHK005 es un hallazgo de ambigüedad menor-medio, con lectura amplia razonable pero no
  garantizada por el texto literal.
## Revalidación W0 (2026-10-16)

- CHK001–CHK003: FR-025, FR-026, FR-038 y FR-039 prohíben, bloquean y definen el único fallback autorizado.
- CHK004–CHK006: FR-027 enumera también confianza STT, duración, aclaraciones, repreguntas e incidencias como señales no académicas.
- CHK007–CHK009: FR-029/FR-029a cierran contenido del resumen y exigen construcción determinista sin generación libre.
- CHK010–CHK011: FR-012, FR-014, FR-025 y FR-026 permiten decidir continuidad sin calificar al participante.

## Revalidación de implementación (2026-10-17)

CHK001–CHK011: `tests/failure/test_defense_no_evaluation.py`, `tests/contract/test_defense_output_authorization_matrix.py`, `tests/integration/test_defense_summary_authorization.py` y `test_defense_voice_lifecycle.py` verifican no evaluación, fallback único, resumen determinista, bloqueo de caracterización y separación de confianza STT.

Las rutas de pruebas son relativas a la raíz del workspace. Las cifras y comandos exactos están en `../implementation-evidence.md` y sus logs; las dos pruebas reales de modelos no se cuentan como aprobadas.
