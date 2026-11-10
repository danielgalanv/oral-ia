# Feature Specification: Agencia de autoestudio

**Feature Branch**: `003-self-study-agency`

**Created**: 2026-07-21

**Status**: Draft

**Input**: User description: "Feature 003 — Agencia de autoestudio: añadir una experiencia completa de autoestudio por texto construida sobre el núcleo cognitivo (Feature 001) y el sistema de materiales autorizados (Feature 002). La misma sociedad de agentes debe combinarse dinámicamente para resolver dudas, ofrecer explicaciones guiadas, generar preguntas de práctica, preparar una exposición y revisar conceptos, permitiendo que un estudiante consulte y practique con materiales seleccionados por el profesorado, obteniendo respuestas trazables y prudentes sin evaluación automática ni sustitución del profesor." (fuente: `docs/ORAL-IA_SpecKit/features/003_self_study_specify.md`, `.specify/memory/constitution.md`, `docs/ORAL-IA_SpecKit/14_domain_model.md`, `docs/ORAL-IA_SpecKit/13_definition_of_done.md`)

## Clarifications

### Session 2026-07-21

- Q: ¿El historial de preguntas de práctica (`PracticeQuestion`, FR-011) está acotado a
  la sesión actual o persiste entre sesiones del mismo participante? → A: Acotado a la
  sesión actual; no se conserva entre sesiones. Un almacén de historial de preguntas
  entre sesiones para el mismo código de participante bordearía la prohibición
  constitucional de perfiles longitudinales (Principio III) que esta misma feature ya
  declara fuera de alcance.
- Q: ¿El estudiante puede volver más tarde a leer su `StudySessionSummary`, o se muestra
  una única vez al finalizar la sesión? → A: Visualización única y efímera, entregada en
  la misma respuesta que cierra la sesión; no se añade una nueva capacidad de consulta
  posterior para el participante, consistente con la API de participante ya definida en
  la Feature 001 (que no ofrece acceso a sesiones pasadas) y con la minimización de datos
  del Principio VII.

### Session 2026-09-01

- Q: ¿Debe la restricción de no revelar la solución de una pregunta de práctica (FR-013)
  depender únicamente de instruir al agente generador? → A: No. La arquitectura MUST
  incluir una comprobación de no-revelación ejecutada por un verificador independiente
  del generador, antes de mostrar la salida al estudiante; si la comprobación falla, la
  salida MUST rechazarse y regenerarse o sustituirse por una alternativa determinista de
  reserva — nunca basta con instruir al generador (ver FR-013a). Esta comprobación evalúa
  la salida del sistema, no la respuesta del estudiante (ver FR-014).
- Q: ¿Puede una configuración de actividad de autoestudio tener el subconjunto de modos
  habilitados vacío? → A: No. Una configuración sin ningún modo habilitado es inválida y
  MUST rechazarse antes de permitir iniciar cualquier sesión sobre esa actividad (ver
  FR-002a).
- Q: ¿Puede el sistema agregar o correlacionar información de autoestudio (preguntas de
  práctica, incidencias de coherencia, conceptos, dudas, resúmenes) entre distintas
  sesiones del mismo `participant_code`? → A: No, bajo ninguna circunstancia dentro de
  esta feature. Toda esa información permanece acotada a la sesión que la generó;
  construir cualquier forma de memoria longitudinal (perfil académico, de capacidad,
  dificultad, rendimiento o personalidad) queda fuera de alcance y requeriría una feature
  futura explícita con su propia decisión constitucional (ver FR-011a).
- Q: ¿Cuál es la política de retención por defecto de los datos derivados de una sesión
  de autoestudio, y quién define el periodo si una actividad autoriza conservarlos? → A:
  Por defecto no se conservan de forma permanente. Si una actividad autoriza
  conservarlos, esa persistencia se sujeta a la misma política de retención y
  consentimiento ya definida por el sistema (Principio VII; `RetentionPolicy`, Feature
  001) con un periodo de retención finito y configurable como parte de esa
  configuración — esta feature no fija ningún número de días por defecto no definido ya
  en la constitución o en los requisitos existentes; al expirar, los datos MUST ser
  eliminables mediante el mecanismo de purga ya existente (ver FR-028).
- Q: ¿Cómo se garantiza que los cinco modos de autoestudio produzcan comportamientos
  distinguibles y verificables sin duplicar la implementación por modo? → A: Cada modo
  MUST tener un identificador canónico estable (`doubt_resolution`, `guided_explanation`,
  `practice_questions`, `presentation_preparation`, `concept_review`) y un comportamiento
  distintivo descrito explícitamente (ver FR-001a); todos MUST reutilizar el mismo
  conjunto mínimo de agentes de la agencia (FR-003) — la diferencia surge de
  configuración, composición de agentes activados, política de diálogo y selección de
  acción conversacional, nunca de implementaciones independientes por modo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Resolver una duda cubierta por los materiales (Priority: P1) 🎯 MVP

Un estudiante inicia una actividad de autoestudio autorizada, conoce su propósito y
límites, formula una duda cubierta por los materiales de la asignatura, y el sistema
recupera evidencias, genera una explicación fundamentada, la verifica, la muestra junto
con sus fuentes (documento, versión, ubicación y fragmento), y conserva el concepto
tratado en el estado de la sesión.

**Why this priority**: Es el flujo extremo a extremo que demuestra el valor central de
la agencia de autoestudio (Escenario A) y constituye su MVP mínimo demostrable, apoyado
en el núcleo cognitivo (Feature 001) y la recuperación de materiales (Feature 002).

**Independent Test**: Puede probarse de forma independiente con una actividad de
autoestudio ya configurada y materiales activos (Features 001/002), formulando una duda
cubierta y verificando que la respuesta llega fundamentada y con fuentes visibles.

**Acceptance Scenarios**:

1. **Given** una actividad de autoestudio autorizada, **When** el estudiante la inicia,
   **Then** el sistema le informa de su propósito y sus límites antes de aceptar la
   primera consulta.
2. **Given** una duda del estudiante cubierta por los materiales activos, **When** el
   sistema la procesa, **Then** interpreta la intención como una hipótesis con
   confianza, recupera evidencias, genera una propuesta, verifica su fundamentación y
   conformidad constitucional, selecciona la acción conversacional y actualiza el
   estado.
3. **Given** una respuesta que usa materiales, **When** el estudiante abre la vista de
   fuentes, **Then** puede ver documento, versión, ubicación y el fragmento relevante
   utilizado.
4. **Given** un concepto ya tratado en la sesión, **When** el estudiante vuelve a
   preguntar algo relacionado, **Then** el sistema evita repetición innecesaria sin
   reenviar todo el historial de la conversación.

---

### User Story 2 - Reconocer una duda fuera de los materiales autorizados (Priority: P1)

La actividad prohíbe el conocimiento general y el estudiante formula una duda que no
está cubierta por los materiales autorizados. El sistema reconoce explícitamente la
falta de información y puede pedir una aclaración o sugerir consultar al profesorado, en
vez de inventar una respuesta.

**Why this priority**: Protege la fiabilidad pedagógica y la confianza en el sistema
(Principio V de la constitución); es tan crítico como la User Story 1 porque una duda
"cubierta" y una "no cubierta" son las dos caras del mismo flujo de confianza.

**Independent Test**: Puede probarse de forma independiente configurando una actividad
sin conocimiento general permitido y formulando una duda deliberadamente fuera de los
materiales activos.

**Acceptance Scenarios**:

1. **Given** una actividad con conocimiento general desactivado, **When** el estudiante
   formula una duda sin cobertura en los materiales, **Then** el sistema reconoce la
   falta de información en vez de generar una respuesta específica no respaldada.
2. **Given** una duda sin evidencia suficiente, **When** el sistema responde, **Then**
   puede pedir una aclaración o sugerir consultar al profesorado, sin presentar una
   suposición como hecho de la asignatura.

---

### User Story 3 - Adaptar la explicación a petición del estudiante (Priority: P2)

El estudiante indica que no ha entendido una explicación y pide un ejemplo, una versión
más sencilla o una comparación. El sistema interpreta el cambio de intención, evita
repetir literalmente la respuesta anterior, y genera contenido fundamentado adaptado o
reconoce que no hay material suficiente para hacerlo.

**Why this priority**: Es el mecanismo que hace útil el autoestudio más allá de una
única pregunta-respuesta; depende de que exista ya un turno anterior que adaptar (User
Story 1).

**Independent Test**: Puede probarse de forma independiente completando un primer turno
de duda cubierta y luego solicitando un ejemplo o una explicación más sencilla sobre el
mismo concepto.

**Acceptance Scenarios**:

1. **Given** una respuesta previa que el estudiante no entendió, **When** pide un
   ejemplo, **Then** el sistema genera un ejemplo fundamentado distinto de la respuesta
   anterior o reconoce que no hay material suficiente.
2. **Given** una petición de explicación más sencilla o una comparación, **When** el
   sistema la procesa, **Then** interpreta el cambio de intención sin perder el
   concepto ya tratado en el estado de la sesión.

---

### User Story 4 - Practicar con preguntas sin calificación (Priority: P2)

El estudiante solicita preguntas de práctica. El sistema formula preguntas derivadas de
los objetivos, conceptos, materiales, dificultad orientativa e historial de preguntas ya
realizadas, de tipo explicación, aplicación, comparación, justificación o detección de
errores, y continúa con aclaraciones o repreguntas — sin asignar notas ni emitir juicios
académicos sobre las respuestas del estudiante.

**Why this priority**: Es uno de los cinco submodos de autoestudio y un caso de uso de
alto valor pedagógico; depende del flujo base de duda cubierta (User Story 1) para
compartir agentes y estado.

**Independent Test**: Puede probarse de forma independiente en una actividad con el modo
de preguntas de práctica habilitado, solicitando preguntas y respondiéndolas.

**Acceptance Scenarios**:

1. **Given** una actividad con el modo de preguntas de práctica habilitado, **When** el
   estudiante las solicita, **Then** el sistema formula preguntas pertinentes derivadas
   de objetivos, conceptos, materiales e historial de preguntas.
2. **Given** una pregunta de práctica cuyo modo prohíbe revelar la solución, **When** el
   estudiante la responde, **Then** el sistema no revela automáticamente la solución.
3. **Given** la respuesta del estudiante a una pregunta de práctica, **When** el sistema
   decide la siguiente acción, **Then** puede usarla para elegir la siguiente pregunta o
   repregunta, pero MUST NOT producir una nota, clasificación o inferencia permanente de
   nivel.

---

### User Story 5 - Componer dinámicamente los agentes según el modo habilitado (Priority: P2)

Para cada turno, el orquestador selecciona únicamente los agentes necesarios entre el
conjunto mínimo de la agencia (gestión de sesión, interpretación de intención,
recuperación documental, respuesta fundamentada, generación de preguntas, gestión de
diálogo, comprobación de fundamentación, coherencia conversacional, control
constitucional y de seguridad, resumen de sesión, trazabilidad y recursos), y registra
por qué activó cada uno. Los controles no omitibles se ejecutan siempre,
independientemente del modo.

**Why this priority**: Demuestra que los cinco submodos comparten una única sociedad de
agentes sin duplicar el núcleo cognitivo — el criterio de éxito arquitectónico central
de esta feature; depende de que existan al menos dos modos habilitados para poder
demostrar composiciones distintas (User Stories 1 y 4).

**Independent Test**: Puede probarse de forma independiente configurando dos actividades
con distintos modos habilitados y verificando que el orquestador activa subconjuntos de
agentes distintos y trazables para cada una.

**Acceptance Scenarios**:

1. **Given** una actividad que solo habilita resolución de dudas, **When** se ejecuta un
   turno, **Then** el orquestador no activa agentes exclusivos de otros modos (por
   ejemplo, generación de preguntas).
2. **Given** una actividad que habilita varios modos, **When** se ejecutan turnos de
   distinto tipo, **Then** el sistema registra, para cada turno, qué agentes se
   activaron y por qué.
3. **Given** cualquier modo habilitado, **When** se ejecuta un turno, **Then** los
   controles marcados como no omitibles (constitucional y de seguridad) se ejecutan
   siempre.

---

### User Story 6 - Detectar y gestionar fallos de coherencia (Priority: P2)

Una propuesta contradice una afirmación previa de la sesión o una fuente activa, o el
sistema detecta falta de información, repetición, pérdida del objetivo, exceso de
turnos, fallo de agente, latencia excesiva o ausencia de progreso. El verificador de
coherencia y fundamentación bloquea o reformula la propuesta y registra la incidencia,
pudiendo volver a recuperar, reformular, pedir aclaración, reconocer desconocimiento,
reducir la respuesta o finalizar de forma segura.

**Why this priority**: Protege la fiabilidad conversacional a lo largo de una sesión
completa, no solo en un turno aislado; depende de que exista una conversación de varios
turnos sobre la que detectar incoherencias (User Stories 1 y 3).

**Independent Test**: Puede probarse de forma independiente forzando una propuesta de
prueba que contradiga una afirmación previa de la sesión y verificando que se bloquea o
reformula con la incidencia registrada.

**Acceptance Scenarios**:

1. **Given** una propuesta que contradice una afirmación previa o una fuente activa,
   **When** el verificador la evalúa, **Then** la bloquea o reformula y registra la
   incidencia de forma trazable.
2. **Given** cualquiera de las condiciones detectables (falta de información,
   repetición, pérdida de objetivo, exceso de turnos, fallo de agente, latencia
   excesiva, ausencia de progreso), **When** se detecta, **Then** el sistema aplica una
   de las acciones de recuperación previstas (recuperar de nuevo, reformular, pedir
   aclaración, reconocer desconocimiento, reducir la respuesta o finalizar de forma
   segura).

---

### User Story 7 - Cerrar la sesión al alcanzar su límite con un resumen descriptivo (Priority: P3)

Se alcanza el número máximo de turnos o la duración configurada de la sesión de
autoestudio. El sistema avisa al estudiante, permite un cierre ordenado y, si la
actividad lo autoriza, genera un resumen descriptivo (temas tratados, preguntas
realizadas, conceptos explicados, dudas manifestadas, incidencias y fuentes
consultadas) sin evaluación, diagnóstico de nivel ni recomendaciones académicas.

**Why this priority**: Es una condición de cierre de baja frecuencia esperada frente a
una sesión ya en curso; refuerza la degradación controlada y el límite de sesión ya
establecidos en la Feature 001, aplicados aquí al contexto pedagógico del autoestudio.

**Independent Test**: Puede probarse de forma independiente configurando un límite bajo
de turnos o duración y verificando que la sesión se cierra de forma ordenada con el
resumen correspondiente.

**Acceptance Scenarios**:

1. **Given** una sesión que alcanza su límite de turnos o duración, **When** ocurre,
   **Then** el sistema avisa al estudiante y permite cerrar la sesión de forma
   ordenada.
2. **Given** una actividad que autoriza el resumen de sesión, **When** la sesión
   termina, **Then** el resumen generado puede incluir temas, preguntas, conceptos,
   dudas, incidencias y fuentes, pero MUST NOT incluir notas, diagnóstico de nivel,
   personalidad, capacidad ni recomendaciones académicas automatizadas.

---

### Edge Cases

- ¿Qué ocurre si el estudiante solicita un modo no habilitado por la actividad (por
  ejemplo, preguntas de práctica cuando solo está habilitada la resolución de dudas)? El
  sistema MUST rechazar o redirigir la solicitud explicando que ese modo no está
  disponible para la actividad.
- ¿Qué ocurre si el estudiante pide la solución directa a una pregunta de práctica
  cuando el modo de la actividad lo prohíbe? El sistema MUST NOT revelarla
  automáticamente.
- ¿Qué ocurre si un agente no esencial (por ejemplo, generación de preguntas) falla a
  mitad de turno mientras el resto de la agencia funciona con normalidad? El sistema
  MUST degradar ese componente sin interrumpir el resto de la sesión, siguiendo el
  mecanismo de degradación controlada ya establecido en la Feature 001.
- ¿Qué ocurre si el estudiante pide cambiar a un tema fuera del alcance autorizado de la
  actividad? El sistema MUST rechazar o redirigir la petición, siguiendo el mismo
  aislamiento de autorización ya establecido en la Feature 002.
- ¿Qué ocurre si el verificador de fundamentación y el de coherencia emiten veredictos
  distintos sobre la misma propuesta? El sistema MUST combinarlos de forma explícita
  (por ejemplo, bloquear si cualquiera de los dos lo exige) en vez de ignorar uno de los
  dos veredictos.
- ¿Qué ocurre si se intenta configurar o iniciar una sesión sobre una actividad de
  autoestudio sin ningún modo habilitado? El sistema MUST rechazar esa configuración
  antes de permitir iniciar cualquier sesión sobre ella (ver FR-002a).
- ¿Qué ocurre si la comprobación de no-revelación de solución (FR-013a) falla tanto para
  la salida del generador como para la alternativa determinista de reserva? El sistema
  MUST optar por no mostrar la pregunta de práctica y reconocer la limitación en vez de
  arriesgar una revelación (degradación segura, Principio IX).
- ¿Qué ocurre si el cierre de una sesión (voluntario o automático por límite, FR-020) se
  solicita más de una vez, o si la respuesta que comunica el cierre se pierde en tránsito
  antes de llegar al participante? El sistema MUST tratar una solicitud de cierre sobre
  una sesión ya cerrada como una confirmación de estado, no como un error, y MUST NOT
  intentar regenerar ni reentregar el resumen ya producido (ver FR-021a) — el resumen es
  una visualización única por diseño (FR-021), no una entrega garantizada exactamente una
  vez frente a un fallo de transporte; si la respuesta de cierre no llega al participante,
  el resumen queda irrecuperable para él aunque persista como `TraceEvent` de auditoría
  (estabilización 2026-09-10, research.md §11).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST ofrecer cinco modos de autoestudio, cada uno con un
  identificador canónico estable: resolución de dudas (`doubt_resolution`), explicación
  guiada (`guided_explanation`), preguntas de práctica (`practice_questions`),
  preparación de una exposición (`presentation_preparation`) y revisión de conceptos
  (`concept_review`).
- **FR-001a**: Cada modo MUST producir un comportamiento observable y distinguible de
  los demás (ver Clarifications, sesión 2026-09-01), reutilizando siempre el mismo
  conjunto mínimo de agentes de la agencia (FR-003) — la diferencia MUST surgir de
  configuración, composición de agentes activados, política de diálogo y selección de
  acción conversacional, nunca de implementaciones independientes por modo:
  - `doubt_resolution`: parte de una pregunta o duda formulada por el estudiante y
    prioriza recuperación documental + respuesta fundamentada.
  - `guided_explanation`: desarrolla un concepto de forma progresiva, pudiendo dividir
    la explicación en pasos y solicitar confirmación del estudiante antes de continuar.
  - `practice_questions`: el sistema toma la iniciativa generando preguntas y
    gestionando las respuestas del estudiante, sin calificarlas (FR-014).
  - `presentation_preparation`: ayuda al estudiante a estructurar y ensayar una
    explicación o exposición sobre un tema, pudiendo pedir aclaraciones o ampliaciones.
  - `concept_review`: recorre o recupera conceptos previamente seleccionados para la
    actividad y permite repasarlos mediante explicaciones o preguntas.
- **FR-002**: Cada actividad docente MUST poder habilitar solo un subconjunto de estos
  modos, no todos obligatoriamente.
- **FR-002a**: Una configuración de actividad con el subconjunto de modos habilitados
  vacío MUST considerarse inválida y MUST rechazarse antes de permitir el inicio de
  cualquier sesión sobre esa actividad (ver Clarifications, sesión 2026-09-01).
- **FR-003**: Para cada turno, el orquestador MUST seleccionar únicamente los agentes
  necesarios entre el conjunto mínimo de la agencia (gestión de sesión, interpretación
  de intención, recuperación documental, respuesta fundamentada, generación de
  preguntas, gestión de diálogo, comprobación de fundamentación, coherencia
  conversacional, control constitucional y de seguridad, resumen de sesión, trazabilidad
  y recursos) y MUST registrar por qué activó cada uno.
- **FR-004**: Los controles marcados como no omitibles (constitucional y de seguridad)
  MUST ejecutarse en todos los turnos, independientemente del modo o de la composición
  de agentes seleccionada.
- **FR-005**: El sistema MUST informar al estudiante del propósito y los límites de la
  actividad antes de aceptar su primera consulta.
- **FR-006**: El sistema MUST interpretar cada consulta del estudiante como una
  hipótesis de intención con un valor de confianza asociado.
- **FR-007**: El sistema MUST recuperar materiales cuando la consulta lo requiera,
  utilizando el agente de recuperación ya definido en la Feature 002 sin modificar su
  contrato.
- **FR-008**: El sistema MUST generar una propuesta de respuesta, verificar su
  fundamentación y su conformidad constitucional, seleccionar la acción conversacional y
  actualizar el estado de la sesión, reutilizando los mecanismos de turno, estado y
  verificación ya establecidos en la Feature 001 sin modificarlos.
- **FR-008a**: El mecanismo que genera una respuesta fundamentada o una pregunta de
  práctica MUST tratarse como sujeto a degradación controlada (Principio IX): si no está
  disponible o no responde dentro de su límite de tiempo, el sistema MUST completar el
  turno igualmente mediante un mecanismo alternativo determinista, sin fallar el turno
  ni interrumpir la sesión.
- **FR-008b**: El texto de los materiales usado como evidencia para generar una
  respuesta o una pregunta de práctica MUST tratarse siempre como datos de entrada,
  nunca como instrucciones capaces de alterar el comportamiento del sistema — mismo
  principio ya aplicado a la recuperación documental en la Feature 002.
- **FR-009**: El estudiante MUST poder solicitar: una explicación más sencilla, un
  ejemplo, una comparación, una pregunta de práctica, un cambio de tema dentro del
  alcance autorizado, o la finalización de la sesión.
- **FR-010**: El sistema MUST recordar los conceptos ya tratados en la sesión y evitar
  repetición innecesaria sin reenviar el historial completo de la conversación en cada
  turno.
- **FR-011**: Las preguntas de práctica MUST derivarse de los objetivos, conceptos,
  materiales, dificultad orientativa e historial de preguntas ya realizadas **en la
  sesión actual**; este historial MUST NOT persistir ni ser consultable entre sesiones
  distintas del mismo participante (ver Clarifications).
- **FR-011a**: El sistema MUST NOT agregar, correlacionar ni construir un perfil
  académico, de capacidad, dificultad, rendimiento o personalidad del participante a
  partir de `PracticeQuestion`, `CoherenceIncident`, conceptos tratados, dudas
  manifestadas o resúmenes de distintas sesiones — toda esta información MUST
  permanecer acotada a la sesión que la generó. Cualquier memoria longitudinal entre
  sesiones del mismo `participant_code` queda fuera de alcance de esta feature y MUST
  ser objeto de una decisión y una feature futuras explícitas (ver Clarifications,
  sesión 2026-09-01).
- **FR-012**: El sistema MUST admitir preguntas de práctica de tipo explicación,
  aplicación, comparación, justificación o detección de errores.
- **FR-013**: El sistema MUST NOT revelar automáticamente la solución de una pregunta de
  práctica cuando el modo de la actividad lo prohíba.
- **FR-013a**: La comprobación de que una salida generada no revela la solución (FR-013)
  MUST ejecutarse mediante un verificador independiente del agente que generó la
  pregunta — nunca únicamente mediante una instrucción dirigida al agente generador. Si
  la comprobación detecta que la salida revela la solución, la salida MUST rechazarse y
  MUST regenerarse o sustituirse por una alternativa determinista de reserva antes de
  mostrarse al estudiante. Esta comprobación MUST evaluar únicamente la salida generada
  por el sistema — MUST NOT evaluar ni calificar la respuesta del estudiante (ver
  FR-014).
- **FR-014**: La respuesta del estudiante a una pregunta de práctica MAY utilizarse para
  seleccionar la siguiente acción o repregunta, pero MUST NOT producir una nota,
  clasificación o inferencia permanente de nivel del estudiante.
- **FR-015**: El sistema MUST detectar, como mínimo: falta de información, respuesta no
  fundamentada, contradicción, repetición, pérdida del objetivo, exceso de turnos
  dedicados a un mismo concepto o duda sin resolución (una señal de coherencia, **distinta**
  del límite global de turnos de la sesión ya gobernado por FR-020), fallo de agente,
  latencia excesiva y ausencia de progreso.
- **FR-016**: Ante cualquiera de las condiciones detectadas en FR-015, el sistema MUST
  poder aplicar al menos una de las siguientes acciones: volver a recuperar, reformular,
  pedir aclaración, reconocer desconocimiento, reducir la respuesta o finalizar de forma
  segura.
- **FR-017**: Una propuesta que contradiga una afirmación previa de la sesión o una
  fuente activa MUST ser bloqueada o reformulada por el verificador correspondiente, y
  la incidencia MUST quedar registrada de forma trazable.
- **FR-018**: Cuando una respuesta use materiales, el estudiante MUST poder abrir una
  vista de fuentes con documento, versión, ubicación y el fragmento relevante.
- **FR-019**: Cuando se utilice conocimiento general permitido, el sistema MUST mostrar
  una indicación diferenciada de que no procede de los materiales.
- **FR-020**: Al alcanzarse el límite de turnos o duración de la sesión, el sistema MUST
  avisar al estudiante y MUST permitir un cierre ordenado.
- **FR-021**: Si la actividad autoriza el resumen de sesión, el sistema MAY generar un
  resumen descriptivo que incluya temas tratados, preguntas realizadas, conceptos
  explicados, dudas manifestadas, incidencias y fuentes consultadas. El resumen MUST
  entregarse como una visualización única y efímera en la misma respuesta que cierra la
  sesión; el sistema MUST NOT ofrecer al participante una vía de consulta posterior a
  ese resumen (ver Clarifications).
- **FR-021a** (aclaración añadida en la ronda de estabilización 2026-09-10 — no amplía la
  obligación MAY de FR-021 a un MUST, solo precisa cuál es "la respuesta que cierra la
  sesión" cuando existen dos vías de cierre distintas, FR-020): "la respuesta que cierra
  la sesión" MUST identificarse, en cada cierre concreto, con la respuesta HTTP del
  mecanismo que efectivamente cerró esa sesión — la respuesta de finalización voluntaria
  cuando el estudiante la solicita, o la respuesta del turno que hace que la sesión
  alcance su límite de turnos/duración cuando el cierre es automático (FR-020). Cuando la
  actividad autoriza el resumen y este se genera, su entrega y visualización MUST
  respetarse en cualquiera de los dos casos — un cierre automático MUST NOT descartar un
  resumen ya generado ni omitir comunicar el cierre en su propia respuesta.
- **FR-021b** (requisito añadido en la ronda de estabilización 2026-09-10, decisión
  explícita sobre el cierre de autoestudio): la interfaz de participante MUST reconocer,
  a partir de la respuesta que cierra la sesión (voluntaria o automática), que la sesión
  ha finalizado, y MUST impedir el envío de nuevos turnos sobre ella — sin ofrecer una
  vía adicional de recuperación del resumen más allá de esa única visualización (FR-021).
- **FR-022**: El resumen de sesión de autoestudio MUST NOT incluir notas, diagnóstico de
  nivel, personalidad, capacidad, ni recomendaciones académicas automatizadas basadas en
  inferencias no autorizadas.
- **FR-022a**: Las incidencias incluidas en el resumen de sesión (FR-021) MUST
  describirse como hechos observables del sistema y su arquitectura (tipo de incidencia,
  acción de recuperación aplicada) — MUST NOT redactarse como una caracterización de la
  comprensión, el esfuerzo o la capacidad del estudiante, mismo estándar ya exigido al
  resumen técnico de la Feature 001 (FR-012b).
- **FR-023**: Un cambio de tema solicitado por el estudiante que quede fuera del alcance
  autorizado de la actividad MUST ser rechazado o redirigido, aplicando el mismo
  aislamiento de autorización ya establecido en la Feature 002.
- **FR-024**: Cuando el verificador de fundamentación y el verificador de coherencia
  emitan veredictos distintos sobre la misma propuesta, el sistema MUST combinarlos de
  forma explícita (por ejemplo, bloqueando si cualquiera de los dos lo exige) en vez de
  descartar uno de los dos.
- **FR-025**: Esta feature MUST NOT modificar el comportamiento ya validado de la
  Feature 001 (núcleo cognitivo, contratos de agente, ciclo de sesión/turno, control
  constitucional, versionado del estado cognitivo) ni de la Feature 002 (materiales,
  recuperación, fundamentación); únicamente compone sus agentes y contratos existentes
  en una nueva agencia de autoestudio.
- **FR-026**: Esta feature MUST NOT inferir ni almacenar un perfil de capacidad
  académica o psicológica del estudiante.
- **FR-027**: Esta feature MUST NOT incluir voz, transcripción, un simulacro formal de
  defensa oral, evaluación, notas, rúbricas, acceso a Internet ni integración con
  sistemas LMS.
- **FR-028**: Los datos derivados de una sesión de autoestudio (`PracticeQuestion`,
  `CoherenceIncident`, resumen de sesión) MUST NOT conservarse de forma permanente por
  defecto una vez cerrada la sesión. Si una actividad autoriza su persistencia más allá
  del cierre, esa persistencia MUST sujetarse a la misma política de retención y
  consentimiento ya definida por el sistema (Principio VII; `RetentionPolicy`, Feature
  001) y MUST declarar un periodo de retención finito y configurable como parte de esa
  configuración — esta feature MUST NOT fijar un número de días por defecto no definido
  ya en la constitución o en los requisitos existentes. Al expirar ese periodo, los
  datos MUST ser eliminables mediante el mecanismo de purga ya existente (Feature 001).
- **FR-028a** (corregida en la segunda ronda de estabilización, 2026-09-10 — la
  redacción previa de esta cláusula equiparaba "existe un `RetentionPolicy` con
  `retention_days` finito" con "hay autorización para conservar", lo cual es incorrecto:
  un plazo expresa *cuánto* tiempo, nunca *si* está autorizado conservar; esa
  equivalencia queda retirada): esta feature no distingue hoy un permiso separado de
  `summary_authorized` (que únicamente autoriza *generar* el resumen efímero, FR-021)
  para "autorización de conservar datos derivados más allá del cierre" — FR-028 exige
  esa autorización, pero ningún campo la representa todavía. Se añade
  `SelfStudyActivityConfig.retention_authorized: bool | null` (nuevo, propio de esta
  feature, independiente de `summary_authorized` y de `RetentionPolicy`) como la
  representación explícita de esa autorización — un plazo (`RetentionPolicy.
  retention_days`) sigue gobernando únicamente *cuánto tiempo*, nunca si conservar.
  Autorización de conservación efectiva MUST requerir ambas condiciones a la vez:
  `retention_authorized = true` **y** una `RetentionPolicy` con `retention_days` finito
  (no nulo) asociada — ninguna de las dos por separado autoriza nada.
  - **Nueva configuración sin autorización** (`retention_authorized = false`, o sin
    política finita asociada aunque `retention_authorized = true`): sus datos derivados
    (`PracticeQuestion`, `CoherenceIncident`, resumen de sesión) MUST tratarse como sin
    autorización de conservación — elegibles para el mecanismo de purga ya existente
    desde la primera ejecución posterior al cierre de la sesión (FR-028: "MUST NOT
    conservarse de forma permanente por defecto"). El cierre de la sesión en sí (FR-020)
    no cambia — no se borra nada de forma síncrona al cerrar; lo que cambia es que esos
    datos ya son candidatos para la siguiente invocación manual de la purga (Principio
    VI: la purga sigue siendo el único mecanismo de eliminación, siempre manual).
  - **Configuración autorizada con plazo finito válido** (`retention_authorized = true`
    y `retention_days` finito): sin cambios respecto al mecanismo ya descrito — elegible
    para purga cuando `Session.ended_at + retention_days < now()`.
  - **Configuraciones y datos preexistentes** (creados antes de que
    `retention_authorized` existiera como campo): MUST NOT recibir un valor por defecto
    deducido — ni `true` (sobre-autorizaría silenciosamente) ni `false` (haría
    purgables, sin decisión humana, datos que un profesorado pudo asumir conservados).
    MUST quedar en un estado explícito "sin decidir" (`retention_authorized = null`),
    excluido tanto del camino de purga inmediata como del camino de purga por plazo,
    hasta que una persona con permiso lo fije explícitamente a `true` o `false`. Esa
    decisión MUST identificarse como una acción humana pendiente — **MUST NOT**
    deducirse de cuántas veces se invoque el mecanismo de purga (ver `research.md` §12
    para el mecanismo de diagnóstico, separado de la purga, que expone qué actividades
    siguen sin decidir).

### Key Entities

- **PracticeQuestion**: pregunta de práctica generada, con tipo (explicación,
  aplicación, comparación, justificación, detección de errores), objetivo y conceptos de
  origen, materiales de referencia, dificultad orientativa, indicador de si revela
  solución automáticamente, e historial de preguntas ya formuladas **en la sesión
  actual** (acotado por sesión, no persistente entre sesiones — ver Clarifications).
- **CoherenceIncident**: incidencia detectada por el verificador de coherencia, con
  tipo (falta de información, respuesta no fundamentada, contradicción, repetición,
  pérdida de objetivo, exceso de turnos dedicados a un mismo concepto o duda sin
  resolución — distinto del límite global de turnos de la sesión, FR-020 —, fallo de
  agente, latencia excesiva, ausencia de progreso), la propuesta afectada, y la acción
  de recuperación aplicada.
- **StudySessionSummary**: resumen descriptivo de una sesión de autoestudio (temas,
  preguntas, conceptos, dudas, incidencias, fuentes), visible para el propio estudiante
  cuando la actividad lo autoriza, entregado como visualización única y efímera al
  cerrar la sesión (sin consulta posterior — ver Clarifications) — a diferencia del
  resumen técnico de la Feature 001 (FR-012b), que es interno, persistente y solo
  visible en el área técnica; ver Assumptions.

*(Session, Turn, CognitiveState (incluido su campo `intent_hypotheses`), Agent, Agency,
AgentContract, InternalMessage, StatePatch y TraceEvent se reutilizan tal como quedaron
definidos en la Feature 001. MaterialDocument, MaterialFragment, Evidence,
GroundingVerificationResult y el agente de recuperación se reutilizan tal como quedaron
definidos en la Feature 002. Ninguno se modifica.)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Cada uno de los cinco modos canónicos (`doubt_resolution`,
  `guided_explanation`, `practice_questions`, `presentation_preparation`,
  `concept_review`) MUST superar, en las pruebas preparadas para esta feature, al menos
  un escenario de aceptación específico de su comportamiento canónico (FR-001a) que
  demuestre una diferencia observable frente a los demás modos en, según corresponda:
  quién inicia la interacción, el tipo de acción conversacional seleccionada, la
  política de diálogo aplicada, el uso de generación de preguntas frente a respuesta
  fundamentada, la progresión de turnos, o el comportamiento de cierre/continuación. La
  conformidad se comprueba mediante las decisiones estructuradas de la agencia y la
  traza registrada — nunca mediante comparación literal del texto generado ni exigiendo
  salidas idénticas o deterministas del mecanismo de generación. 5/5 modos MUST superar
  su escenario específico y MUST registrar en la traza el modo activo y las decisiones
  de orquestación utilizadas (qué agentes se activaron y por qué, FR-003). Todos los
  modos comparten los mismos agentes y el mismo estado de sesión, sin que ninguno
  requiera una sesión o un estado distintos del núcleo cognitivo.
- **SC-002**: El 100% de las respuestas específicas de la asignatura en las pruebas
  quedan citadas o marcadas explícitamente como no fundamentadas o como conocimiento
  general permitido.
- **SC-003**: El orquestador selecciona al menos tres composiciones distintas de
  agentes en los escenarios de prueba preparados para esta feature.
- **SC-004**: El 100% de las salidas prohibidas de las pruebas quedan bloqueadas antes
  de mostrarse al estudiante.
- **SC-005**: Un estudiante puede mantener una conversación de prueba de al menos cinco
  turnos con continuidad de contexto, sin que el sistema reenvíe el historial completo
  de la conversación en cada turno.
- **SC-006**: El 100% de las sesiones de prueba que alcanzan su límite de turnos o
  duración terminan de forma controlada y generan una traza completa reconstruible.

## Assumptions

- El comportamiento ya validado de la Feature 001 (núcleo cognitivo) y de la Feature 002
  (materiales y RAG) permanece sin cambios; esta feature es puramente aditiva y compone
  agentes y contratos ya existentes en una nueva agencia de autoestudio. Cómo se
  implementa exactamente esa composición (por ejemplo, cuántas `AgencyDefinition`
  distintas se registran) es una decisión de `/speckit-plan`.
- El "resumen de sesión" de esta feature (`StudySessionSummary`) es distinto y visible
  para el estudiante, a diferencia del resumen técnico de la Feature 001 (FR-012b), que
  permanece interno y visible solo en el área técnica. Ambos pueden coexistir: el
  técnico para el investigador/mantenedor, el descriptivo de autoestudio para el propio
  estudiante cuando la actividad lo autorice.
- El campo `CognitiveState.intent_hypotheses` (Feature 001) es la estructura que ya
  soporta el registro de hipótesis de intención con confianza que pide esta feature; no
  se introduce un campo paralelo.
- La "dificultad orientativa" de una pregunta de práctica sirve únicamente para
  seleccionar la siguiente pregunta, nunca para clasificar al estudiante (Constitución,
  sección "Evaluación" del gobierno de la constitución).
- Los detalles exactos de qué agente concreto implementa cada rol mínimo de la agencia
  (por ejemplo, si "comprobación de fundamentación" reutiliza literalmente el verificador
  de la Feature 002 o añade un adaptador) son decisiones de planificación técnica, no de
  esta especificación.
- Preparación de una exposición y revisión de conceptos, aunque nombrados como modos en
  el ámbito de esta feature, no incluyen el simulacro formal de defensa oral ni la voz;
  esos aspectos están reservados a la Feature 004, conforme a "Fuera de alcance".
