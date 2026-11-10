# Reuse & Architecture Requirements Checklist: Agencia de defensa oral y voz opcional

**Purpose**: Buscar requisitos que puedan provocar duplicación accidental de
componentes ya implementados en las Features 001–003, previo a `/speckit-tasks`
**Created**: 2026-09-02
**Feature**: [spec.md](../spec.md) · [research.md](../research.md) · [plan.md](../plan.md)

## Núcleo cognitivo y sesión (Feature 001)

- [X] CHK001 - ¿Exige explícitamente algún requisito reutilizar `Session`/`Turn` y el ciclo de sesión ya existente, en vez de un modelo de sesión propio de defensa? [Consistency, Spec §FR-033]
- [X] CHK002 - ¿Prohíbe un requisito ampliar el esquema de `CognitiveState` salvo necesidad demostrada? [Clarity, Spec §FR-033, Research §11] — `research.md` concluye que no hace falta ningún campo nuevo; confirmar que ningún FR de `spec.md` requiere implícitamente un dato que no quepa en los campos ya existentes.
- [X] CHK003 - ¿Reutiliza la especificación, sin plantear una alternativa, el mismo mecanismo de versionado de `StatePatch` ya validado? [Consistency, Spec §FR-033]

## Materiales y recuperación (Feature 002)

- [X] CHK004 - ¿Exige un requisito reutilizar `MaterialRetrieverAgent` y su aislamiento de autorización sin modificar su contrato? [Clarity, Spec §FR-013/FR-023]
- [X] CHK005 - ¿Podría algún requisito de recuperación de materiales para la repregunta interpretarse como necesitando un filtro de autorización propio y distinto del ya existente? [Ambiguity] — no se detecta tal necesidad; ítem de confirmación negativa.

## Generación y verificadores (Feature 003)

- [X] CHK006 - ¿Reutiliza la especificación, explícitamente, `GenerationPort` con sus dos adaptadores ya existentes en vez de plantear un mecanismo de generación propio de esta feature? [Consistency, Spec §FR-033, Research §1]
- [X] CHK007 - ¿Es la extensión aditiva de `GenerationPurpose` (nuevos valores de propósito, sin tocar los existentes) una interpretación inequívoca de "no modificar el comportamiento ya validado" (FR-033), o es una zona gris que convendría confirmar antes de tocar ese fichero? [Assumption, Research §1] — decisión de plan razonada y documentada (research.md §1), pero al tratarse de editar un fichero de la Feature 003 ya validada, se marca explícitamente como supuesto a confirmar antes de implementar, no como un hecho ya verificado.
- [X] CHK008 - ¿Exige un requisito reutilizar `GroundingVerifierAgent`/`CoherenceVerifierAgent`/`ConstitutionalControl` sin duplicar su técnica de verificación? [Clarity, Spec §FR-016/FR-033]
- [X] CHK009 - ¿Confirma algún requisito, de forma verificable antes de implementar, que `ConstitutionalControl` ya bloquea el contenido evaluativo prohibido por esta feature sin necesitar ninguna regla nueva? [Completeness, Research §1] — hallazgo favorable de `research.md` (patrones `assigns_grade`/`academic_decision` ya existen); recomendable verificarlo con una prueba de contrato temprana en `/speckit-tasks` antes de asumir que ninguna regla adicional será necesaria.
- [X] CHK010 - ¿Reutiliza la especificación `PracticeQuestionAgent` para la pregunta inicial en vez de requerir un generador de preguntas propio? [Consistency, Research §8]

## `DialogueAction`, trazabilidad y retención

- [X] CHK011 - ¿Prohíbe un requisito ampliar el conjunto de `DialogueAction` salvo imposibilidad demostrada? [Clarity, Spec Clarifications Q4]
- [X] CHK012 - ¿Reutiliza la especificación el mecanismo de trazabilidad genérico (`TraceEvent`/`event_type`) en vez de un sistema de registro propio? [Consistency, Spec §FR-033]
- [X] CHK013 - ¿Reutiliza la especificación `RetentionPolicy` sin introducir un sistema de retención paralelo? [Consistency, Spec §FR-031]

## STT/TTS como adaptadores, no agentes

- [X] CHK014 - ¿Deja claro algún requisito que la transcripción y la síntesis de voz son adaptadores de interfaz, no agentes cognitivos con responsabilidad de decisión? [Clarity, Research §2]
- [X] CHK015 - ¿Está limitada explícitamente a `FollowUpQuestionAgent` la única capacidad cognitiva genuinamente nueva de esta feature, con una justificación explícita de por qué no basta con reutilizar un agente existente? [Completeness, Research §8]

## Notes

- **Único hallazgo con seguimiento recomendado**: CHK007 — la extensión aditiva de
  `generation_port.py` (Feature 003) es la única modificación de un fichero ya validado
  que este plan contempla; aunque está bien justificada, se marca como supuesto
  (`[Assumption]`) a confirmar explícitamente (p. ej. re-ejecutando la suite completa de
  la Feature 003 tras la extensión) antes de darla por válida sin más verificación.
- CHK009 es una oportunidad, no un defecto: aprovechar que `ConstitutionalControl` ya
  cubre el caso de uso de esta feature para priorizar una prueba de contrato temprana
  en vez de trabajo de implementación.
## Revalidación W0 (2026-10-16)

- CHK001–CHK003: FR-001/FR-033, research.md §11 y plan.md reutilizan Session/Turn, CognitiveState y StatePatch.
- CHK004–CHK010: FR-013/FR-016/FR-033, research.md §§1/8 y la integración T090 reutilizan recuperación, generación, verificadores, catálogo y PracticeQuestionAgent mediante extensiones aditivas probadas.
- CHK011–CHK015: Clarifications Q4, FR-018a, FR-031, FR-033, research.md §§2/8/17 fijan DialogueAction, trazabilidad, retención, puertos de voz y el único agente nuevo.

## Revalidación de implementación (2026-10-17)

CHK001–CHK015: compositor y puertos reutilizan los contratos existentes; `tests/contract/test_defense_speech_ports.py`, `test_followup_question_agent.py`, `tests/integration/test_defense_initial_material_question.py` y la regresión completa constituyen evidencia. CHK009: el supuesto de suficiencia del patrón antiguo se refutó y se resolvió con la extensión aditiva `academic_decision` documentada en research.md §27; no hay un verificador paralelo.

Las rutas de pruebas son relativas a la raíz del workspace. Las cifras y comandos exactos están en `../implementation-evidence.md` y sus logs; las dos pruebas reales de modelos no se cuentan como aprobadas.
