# Feature Specification: Núcleo cognitivo y ejecución local

**Feature Branch**: `001-core-cognitive-runtime`

**Created**: 2026-07-21

**Status**: Draft

**Input**: User description: "Feature 001 — Núcleo cognitivo y ejecución local: construir el primer incremento funcional de ORAL-IA — un núcleo cognitivo local, modular y trazable capaz de iniciar sesiones, registrar agentes, componer agencias predefinidas, mantener un estado cognitivo compartido y ejecutar un flujo mínimo, sin depender todavía de materiales docentes reales, voz ni evaluación académica." (fuente: `docs/ORAL-IA_SpecKit/features/001_core_runtime_specify.md`, `docs/ORAL-IA_SpecKit/13_definition_of_done.md`, `docs/ORAL-IA_SpecKit/14_domain_model.md`)

## Clarifications

### Session 2026-07-21

- Q: (pre-resuelto en `docs/ORAL-IA_SpecKit/10_clarification_decisions.md`, sección "Alcance operativo") ¿Cuántas sesiones interactivas activas admite el sistema por instancia en esta primera versión? → A: Una única sesión interactiva activa por instancia; pueden conservarse múltiples sesiones históricas, y el diseño no debe impedir ampliar la concurrencia más adelante.
- Q: ¿Debe esta feature implementar una credencial de acceso para el área técnica/docente? → A: No se implementa por completo; se deja el mecanismo de control de acceso preparado pero deshabilitado por defecto (flag de configuración), y su activación completa se implementa en la Feature 005 (Configuración docente, revisión y privacidad).
- Q: ¿Quién ve el resumen técnico al finalizar una sesión? → A: (resuelto con la opción recomendada, al pasar el usuario directamente a `/speckit-plan` sin responder en la sesión interactiva) El participante recibe solo una confirmación breve de cierre de sesión; el resumen técnico completo (agentes, incidencias, decisiones) solo es visible en el área técnica/investigador. Revisable con `/speckit-clarify` si no es la intención deseada.

### Session 2026-10-13

- Q: Para FR-014/T090, ¿qué información debe constituir la autoridad para decidir si una salida revela datos no autorizados o excede el alcance de la actividad? → A: La configuración docente define una política explícita y versionada de permisos de divulgación y límites de alcance comprobables; el orquestador entrega al control una instantánea mínima y filtrada de esa política, aplicable a la salida normal y a todos los fallbacks.
- Q: Para FR-014/T090, ¿qué criterio debe utilizar esa política para autorizar la divulgación de datos al participante? → A: Solo pueden divulgarse datos cuya categoría, procedencia y destinatario estén explícitamente permitidos por la política; los datos sin autorización comprobable se bloquean.
- Q: Para FR-014/T090, ¿qué criterio debe definir si una salida está dentro del alcance autorizado? → A: La política delimita explícitamente temas, propósitos y acciones permitidos, incluidos mensajes operativos seguros; el conocimiento general queda sujeto a la configuración de la actividad.
- Q: Para FR-014/T090, ¿cómo debe comprobar el control que el texto presentado cumple los permisos y el alcance, evitando confiar únicamente en etiquetas declaradas por el generador? → A: Verificación estructural determinista: la propuesta aporta referencias de datos y alcance vinculadas comprobablemente al texto, contrastadas con contexto confiable del orquestador. El contenido sin vinculación verificable se bloquea.
- Q: Para FR-014/T090, si falta la política, el contexto es inválido o no puede verificarse la vinculación del contenido, ¿qué debe ocurrir después de bloquear la propuesta? → A: Registrar la causa e intentar una única respuesta operativa mínima predefinida, cuya autorización y contenido puedan verificarse de forma independiente. Esa respuesta pasa por el mismo control; si tampoco puede autorizarse, finalizar de forma segura sin mostrar contenido no autorizado.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar una actividad y consultar el catálogo (Priority: P1)

Un profesor o desarrollador administrador crea una configuración versionada de actividad
(nombre, asignatura, objetivo, modo, idioma, límite de turnos, duración, conocimiento
general permitido o prohibido, agentes obligatorios y opcionales, política de conservación)
y consulta el catálogo de agentes y agencias disponibles con sus versiones, capacidades,
permisos, contratos y estado de disponibilidad.

**Why this priority**: Sin una actividad configurada y sin un catálogo consultable no existe
nada que un participante pueda ejecutar ni nada que un investigador pueda inspeccionar; es
el prerrequisito de valor para todas las demás historias.

**Independent Test**: Puede probarse por completo creando una configuración de actividad de
prueba y consultando el catálogo, sin que exista todavía ninguna sesión de participante.

**Acceptance Scenarios**:

1. **Given** un catálogo con al menos cinco agentes de prueba registrados bajo el mismo
   contrato, **When** el administrador lo consulta, **Then** el sistema devuelve
   identificador, versión, capacidades, permisos, contrato y disponibilidad de cada agente
   sin requerir cambios en el orquestador.
2. **Given** el catálogo de agentes validado, **When** el administrador define dos agencias
   distintas que reutilizan los mismos agentes en distinto orden o combinación, **Then**
   ambas agencias quedan registradas como configuraciones versionadas independientes.
3. **Given** una configuración de actividad nueva, **When** el administrador la guarda con
   todos los campos requeridos, **Then** la configuración queda versionada e inmutable una
   vez que una sesión la utilice por primera vez.

---

### User Story 2 - Completar una sesión con un turno trazable (Priority: P1) 🎯 MVP

Un participante inicia una sesión local con un código seudónimo sobre una actividad
autorizada, ve indicado que interactúa con un sistema automático, envía al menos un mensaje
de texto, el sistema ejecuta un flujo mínimo (gestión de turno, interpretación simulada o
determinista, control constitucional y presentación), actualiza el estado cognitivo y
registra la secuencia completa. El participante finaliza voluntariamente y se genera un
resumen técnico básico.

**Why this priority**: Es el flujo extremo a extremo que demuestra la arquitectura completa
(Escenario A de la feature) y constituye el MVP mínimo demostrable de esta feature.

**Independent Test**: Puede probarse de forma independiente iniciando una sesión sobre una
actividad ya configurada (User Story 1), enviando un turno y verificando que la sesión
finaliza con un resumen técnico y un registro reconstruible.

**Acceptance Scenarios**:

1. **Given** una actividad autorizada y un código de participante seudónimo, **When** el
   participante inicia sesión, **Then** el sistema muestra de forma explícita que se trata
   de un sistema automático antes de aceptar el primer mensaje.
2. **Given** una sesión iniciada, **When** el participante envía un mensaje de texto,
   **Then** el sistema ejecuta gestión de turno, interpretación, control constitucional y
   presentación, y actualiza el estado cognitivo con una nueva versión trazable.
3. **Given** un turno completado, **When** se consulta el registro de esa sesión, **Then**
   se puede reconstruir la secuencia completa de agentes ejecutados, mensajes internos,
   cambios de estado y decisión de acción conversacional.
4. **Given** una sesión activa, **When** el participante decide finalizarla
   voluntariamente, **Then** el sistema cierra la sesión, muestra al participante una
   confirmación breve de cierre y genera un resumen técnico básico (visible en el área
   técnica/investigador) sin emitir calificaciones ni juicios académicos.

---

### User Story 3 - Bloquear una salida académicamente prohibida (Priority: P2)

Un agente de prueba propone una salida que asigna una nota, suplanta al profesor o emite
una decisión académica. El control constitucional la bloquea antes de que llegue al
participante, registra la causa del bloqueo y devuelve un mensaje seguro.

**Why this priority**: Protege el límite institucional no negociable de la Constitución
(Principio I y IV); es de prioridad alta pero depende de que exista un flujo de turno
(User Story 2) sobre el que interceptar la salida.

**Independent Test**: Puede probarse de forma independiente inyectando un agente de prueba
que genere una propuesta prohibida y verificando que nunca llega al participante.

**Acceptance Scenarios**:

1. **Given** una propuesta de salida generada que asigna una nota o emite una decisión
   académica, **When** el control constitucional la evalúa, **Then** la salida se bloquea y
   no se muestra al participante.
2. **Given** una salida bloqueada, **When** se consulta el registro de la sesión, **Then**
   la causa del bloqueo queda registrada de forma trazable.
3. **Given** una salida bloqueada, **When** el sistema responde al participante, **Then**
   recibe un mensaje seguro que no revela el contenido prohibido.

---

### User Story 4 - Degradar de forma controlada ante el fallo de un agente (Priority: P2)

Un agente excede su tiempo máximo de ejecución o devuelve una salida que no cumple su
contrato. El sistema registra el fallo, evita corromper el estado cognitivo, aplica una
alternativa configurada o finaliza el turno de forma segura, y permite continuar o cerrar
la sesión.

**Why this priority**: Sin degradación controlada, un fallo de agente comprometería la
integridad del estado y la continuidad de la sesión; depende del flujo de turno (User
Story 2) para tener un punto de fallo que interceptar.

**Independent Test**: Puede probarse de forma independiente forzando a un agente de prueba
a superar su timeout o a devolver un objeto inválido, y verificando que el estado permanece
consistente y la sesión sigue siendo utilizable o se cierra de forma segura.

**Acceptance Scenarios**:

1. **Given** un agente que supera su tiempo máximo configurado, **When** se detecta el
   timeout, **Then** el sistema registra el fallo, no aplica ningún cambio parcial al
   estado y activa una alternativa configurada o finaliza el turno de forma segura.
2. **Given** un agente que devuelve una salida que no cumple su contrato, **When** el
   sistema valida la salida, **Then** el fallo se registra como incidencia trazable y el
   estado cognitivo conserva su última versión válida.
3. **Given** un fallo gestionado, **When** el participante continúa interactuando, **Then**
   puede seguir usando la sesión con normalidad o recibir una finalización segura explícita.

---

### User Story 5 - Evitar conflictos de escritura sobre el estado cognitivo (Priority: P3)

Dos operaciones intentan actualizar la misma versión del estado cognitivo de una sesión de
forma simultánea. El sistema detecta el conflicto, no sobrescribe silenciosamente ninguna de
las dos y conserva una secuencia reconstruible de lo ocurrido.

**Why this priority**: Es una condición de borde importante para la integridad del estado,
pero de menor frecuencia esperada que los flujos anteriores; refuerza la trazabilidad ya
cubierta por las historias P1/P2.

**Independent Test**: Puede probarse de forma independiente disparando dos parches de
estado concurrentes contra la misma versión conocida y verificando que el sistema resuelve
el conflicto sin pérdida silenciosa de información.

**Acceptance Scenarios**:

1. **Given** dos parches de estado que referencian la misma versión base, **When** ambos
   se aplican de forma simultánea, **Then** el sistema acepta solo uno como válido contra
   esa versión y rechaza o reencola el otro de forma explícita.
2. **Given** un conflicto de escritura detectado, **When** se consulta el historial de
   versiones del estado, **Then** ambas operaciones quedan registradas de forma
   reconstruible, incluida la rechazada.

---

### User Story 6 - Reconstruir una sesión cerrada tras un reinicio (Priority: P3)

Tras cerrar o reiniciar la aplicación, un investigador o mantenedor abre una sesión
conservada y reconstruye su configuración, turnos, agentes ejecutados, decisiones y
cambios de estado.

**Why this priority**: Es un requisito de auditoría y reproducibilidad (Principio VIII)
que valida de forma acumulativa todo lo registrado por las historias anteriores; no aporta
valor nuevo por sí sola sin sesiones previas ya ejecutadas.

**Independent Test**: Puede probarse de forma independiente reiniciando la aplicación
después de haber cerrado al menos una sesión y verificando que toda su secuencia se puede
reconstruir desde los registros persistidos.

**Acceptance Scenarios**:

1. **Given** una sesión cerrada antes de un reinicio de la aplicación, **When** un
   mantenedor la abre después del reinicio, **Then** puede consultar su configuración
   completa, sus turnos, los agentes ejecutados y las decisiones tomadas.
2. **Given** una sesión reconstruida, **When** se comparan sus cambios de estado con los
   registrados originalmente, **Then** la secuencia de versiones coincide sin huecos ni
   pérdida de eventos.

---

### Edge Cases

- ¿Qué ocurre si un participante intenta iniciar una sesión sobre una actividad que no
  existe o no está autorizada? El sistema MUST rechazar el inicio con un mensaje
  comprensible sin crear una sesión.
- ¿Qué ocurre si el código de participante proporcionado contiene datos que parecen
  identificar a una persona real (por ejemplo, un nombre)? El sistema MUST rechazar o
  neutralizar el dato antes de aceptarlo como identificador de sesión.
- ¿Qué ocurre si se alcanza el límite de turnos o la duración máxima configurada antes de
  que el participante finalice voluntariamente? El sistema MUST finalizar la sesión de
  forma segura y generar igualmente el resumen técnico básico (FR-011a).
- ¿Qué ocurre si el compositor de agencias no encuentra en el catálogo un agente requerido
  por una agencia predefinida? El sistema MUST rechazar la composición de forma explícita y
  trazable en lugar de ejecutar un flujo incompleto.
- ¿Qué ocurre si un investigador consulta una sesión que aún está activa? El sistema MUST
  permitir la inspección de lo ejecutado hasta ese momento sin interrumpir la sesión.
- ¿Qué ocurre si un segundo participante intenta iniciar una sesión interactiva mientras ya
  hay una sesión activa en la misma instancia? El sistema MUST rechazar el inicio de la
  segunda sesión con un mensaje comprensible, sin afectar a la sesión ya activa.
- ¿Qué ocurre si el sistema pierde la conexión con el proceso local que ejecuta un agente
  a mitad de un turno? El sistema MUST tratarlo como un fallo de agente (User Story 4) y
  degradar de forma controlada.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir crear y versionar una configuración de actividad con
  nombre, asignatura, objetivo, modo, idioma, límite de turnos, duración, conocimiento
  general permitido o prohibido, agentes obligatorios y opcionales, y política de
  conservación.
- **FR-002**: Una configuración de actividad utilizada por al menos una sesión MUST
  volverse inmutable; cualquier cambio posterior MUST crear una nueva versión.
- **FR-003**: El sistema MUST exponer un catálogo consultable de agentes y agencias con
  identificador, versión, capacidades, permisos, contrato y estado de disponibilidad.
- **FR-004**: Todo agente registrado MUST declarar un contrato versionado con
  identificador, versión, propósito, entradas, salidas estructuradas, precondiciones,
  postcondiciones, fuentes y herramientas permitidas, permisos, tiempo máximo, consumo
  esperado, errores posibles, confianza, criterios de éxito, terminación, cancelación y
  datos de trazabilidad.
- **FR-005**: El sistema MUST permitir registrar al menos cinco agentes de prueba
  distintos bajo el mismo contrato sin requerir cambios en el orquestador.
- **FR-006**: El sistema MUST permitir componer al menos dos agencias distintas que
  reutilicen agentes ya registrados en el catálogo, sin crear código ni agentes nuevos
  durante la ejecución.
- **FR-007**: Los agentes y el orquestador MUST intercambiar mensajes internos
  estructurados con identificador, sesión, emisor, receptor, tipo, objetivo, contenido,
  evidencias, fuentes, confianza, prioridad, vigencia, respuesta esperada y condición de
  éxito.
- **FR-008**: El sistema MUST mantener una pizarra cognitiva de sesión externa al
  contexto privado del modelo de lenguaje, con control de versiones y un registro de cada
  cambio (agente responsable, versión previa, versión resultante, instante y
  justificación).
- **FR-009**: El estado cognitivo de sesión MUST incluir como mínimo: modo activo,
  objetivo, actividad, materiales permitidos (aunque estén vacíos), pregunta o entrada
  actual, respuesta del participante, conceptos tratados y pendientes, hipótesis de
  intención, información recuperada, dudas, historial resumido, tiempo restante, número de
  turnos, incidencias, confianza y siguiente acción propuesta, distinguiendo el tipo de
  cada elemento (instrucción, observación, afirmación del participante, información
  recuperada, hipótesis, inferencia, decisión, resultado de comprobación o configuración).
- **FR-010**: El sistema MUST permitir a un participante iniciar una sesión local con un
  código seudónimo y una actividad autorizada, y MUST mostrarle de forma explícita que
  interactúa con un sistema automático antes de aceptar su primer mensaje.
- **FR-011**: El sistema MUST gestionar el ciclo de vida de una sesión (inicio, aplicación
  de configuración, turnos, duración, finalización y persistencia).
- **FR-011a**: Cuando se alcance el límite de turnos o la duración máxima configurada de
  la actividad antes de que el participante finalice voluntariamente, el sistema MUST
  cerrar la sesión de forma segura (`status = closed_limit_reached`) y MUST generar
  igualmente el resumen técnico básico (FR-012b).
- **FR-012**: El sistema MUST permitir al participante intercambiar al menos mensajes de
  texto y finalizar la sesión voluntariamente en cualquier momento.
- **FR-012a**: El sistema MUST admitir como máximo una sesión interactiva activa por
  instancia; MUST rechazar el intento de iniciar una segunda sesión interactiva mientras
  otra está activa, sin impedir que se conserven y consulten múltiples sesiones históricas
  ya cerradas.
- **FR-012b**: Al finalizar una sesión, el sistema MUST mostrar al participante únicamente
  una confirmación breve de cierre, sin calificaciones ni juicios académicos; el resumen
  técnico básico completo (agentes ejecutados, incidencias, decisiones) MUST quedar
  disponible solo en el área técnica o de investigador.
- **FR-013**: El sistema MUST seleccionar, para cada turno, una acción conversacional entre
  responder con un mensaje controlado, solicitar aclaración, reconocer falta de
  información, resumir o finalizar.
- **FR-014**: El sistema MUST evaluar toda propuesta de salida mediante un control
  constitucional capaz de bloquear mensajes que asignen notas, suplanten al profesor,
  emitan decisiones académicas, revelen datos no autorizados o se salgan del alcance de la
  actividad, antes de que la salida llegue al participante.
  Para detectar revelación de datos no autorizados y salidas fuera de alcance, la
  autoridad MUST ser una política explícita y versionada definida por la configuración
  docente, con permisos de divulgación y límites de alcance comprobables. El orquestador
  MUST entregar al control una instantánea mínima, confiable y filtrada de la política
  aplicable, tanto en la ruta normal como en todas las respuestas alternativas. La elección
  del medio de transporte, su esquema y sus tipos queda diferida a `plan.md` y los contratos
  internos, sin fijarse en esta especificación funcional. El control
  MUST NOT consultar directamente toda la base de datos ni sustituir estas decisiones
  contextuales por patrones literales sobre el texto propuesto; esta responsabilidad es
  distinta de la autorización de materiales de la Feature 002.
  La divulgación de datos al participante MUST requerir autorización explícita y
  comprobable de su categoría, procedencia y destinatario conforme a esa política;
  los datos sin autorización comprobable MUST bloquearse, incluidas las categorías
  no contempladas por la política.
  El alcance autorizado MUST delimitar explícitamente los temas, propósitos y acciones
  permitidos por la actividad, incluidos los mensajes operativos seguros. El uso de
  conocimiento general MUST sujetarse a la configuración de la actividad; su autorización
  MUST NOT interpretarse como permiso para exceder los límites de alcance definidos.
  La comprobación de divulgación y alcance MUST ser estructural y determinista: todo
  contenido sujeto a autorización MUST tener una vinculación comprobable con los datos
  y el alcance permitidos, contrastada con información confiable suministrada por el
  orquestador. La declaración del generador de que su salida está permitida MUST NOT
  bastar para autorizarla. El contenido sin vinculación verificable MUST bloquearse; esta comprobación
  MUST poder probarse mediante una matriz positiva y negativa determinista.
  Si falta la política, el contexto es inválido o no puede verificarse la vinculación del
  contenido, el sistema MUST bloquear la propuesta y registrar la causa, aplicando la
  recuperación segura definida en FR-015.
- **FR-015**: Toda salida bloqueada por el control constitucional MUST quedar registrada
  con su causa; el sistema MUST NOT revelar al participante el contenido prohibido.
  Como recuperación, MUST intentar una única respuesta operativa mínima, segura y
  predefinida, cuya autorización y contenido puedan verificarse de forma independiente
  conforme a FR-014. MUST mostrarla únicamente si supera esa verificación y el mismo
  control constitucional. Si tampoco puede autorizarse, MUST finalizar de forma segura
  sin presentar contenido y sin encadenar nuevas respuestas alternativas para esta
  incidencia. El bloqueo MUST NOT implicar una obligación incondicional de mostrar un mensaje.
- **FR-016**: El sistema MUST registrar un evento de trazabilidad por sesión, turno,
  agente ejecutado y cambio de estado, permitiendo reconstruir la secuencia completa de un
  turno a partir de los registros.
- **FR-017**: El sistema MUST monitorizar tiempo de ejecución, uso básico de CPU y
  memoria, errores y timeouts por agente y por sesión.
- **FR-018**: Cuando un agente falle, exceda su tiempo máximo o produzca una salida que no
  cumpla su contrato, el sistema MUST degradar de forma controlada: registrar el fallo,
  evitar corromper el estado cognitivo y aplicar una alternativa configurada o finalizar el
  turno de forma segura.
- **FR-018a**: La degradación controlada (FR-018) MUST NOT omitir ni saltarse el control
  constitucional (FR-014) sobre la salida final; toda salida presentada al participante,
  incluida la producida tras una degradación o un fallback, MUST pasar por el control
  constitucional antes de mostrarse (Constitución Principio IX: los controles
  constitucionales nunca pueden omitirse por ahorro de recursos).
- **FR-019**: Cuando dos operaciones intenten actualizar la misma versión conocida del
  estado cognitivo, el sistema MUST detectar el conflicto, MUST NOT sobrescribir
  silenciosamente ninguna de las dos, y MUST conservar una secuencia reconstruible de
  ambas.
- **FR-020**: Tras cerrar o reiniciar la aplicación, el sistema MUST permitir abrir una
  sesión conservada y reconstruir su configuración, turnos, agentes ejecutados, decisiones
  y cambios de estado.
- **FR-021**: El sistema MUST ofrecer una interfaz web local mínima con un área de
  participante y un área técnica o docente suficientes para ejercitar las capacidades
  anteriores.
- **FR-021a**: El sistema MUST proveer un punto de extensión de control de acceso
  (credencial administrativa) para el área técnica o docente, pero MUST dejarlo
  deshabilitado por defecto en esta feature; su activación completa queda fuera de
  alcance y se implementará en la feature de configuración docente, revisión y
  privacidad.
- **FR-022**: El sistema MUST vincularse por defecto únicamente a la máquina local y MUST
  NOT requerir integración institucional ni identidad real para operar.
- **FR-023**: El código de participante MUST ser un identificador seudónimo y MUST NOT
  contener datos personales.
- **FR-024**: El sistema MUST NOT almacenar cadenas de razonamiento privadas de los
  modelos en los registros de trazabilidad; MUST registrar resultados estructurados y
  justificaciones operativas observables.
- **FR-025**: La interfaz web mínima (FR-021) MUST ser operable íntegramente por teclado,
  MUST ofrecer etiquetas accesibles en todos los controles interactivos, MUST mantener
  contraste suficiente para texto y controles, y MUST presentar mensajes de error en
  lenguaje comprensible con una acción siguiente clara (Constitución Principio VII).

### Key Entities

- **Course**: contenedor lógico de actividades y materiales de una asignatura; no
  representa matrícula ni expediente institucional.
- **ActivityConfiguration**: definición versionada e inmutable, una vez utilizada, de una
  actividad (objetivo, modo, idioma, límites, conocimiento general permitido, agentes
  obligatorios/opcionales y política de conservación).
- **ParticipantCode**: identificador seudónimo de un participante sin identidad real
  incorporada.
- **Session**: ejecución de una actividad bajo una versión concreta de su configuración;
  incluye estado, turnos, recursos consumidos e incidencias.
- **Turn**: unidad de interacción de una sesión, con entrada, interpretación, agentes
  ejecutados, verificación constitucional, acción conversacional elegida, salida y
  métricas.
- **Agent**: componente con responsabilidad cognitiva única, registrado en el catálogo
  mediante un contrato versionado.
- **Agency**: composición versionada de agentes, pasos, condiciones y terminación para un
  escenario predefinido.
- **AgentContract**: esquema de responsabilidad, entrada, salida, permisos, límites,
  criterios de éxito, error y trazabilidad declarado por cada agente.
- **InternalMessage**: objeto estructurado intercambiado entre agentes y el orquestador.
- **CognitiveState**: representación estructurada y versionada de lo relevante durante una
  sesión (la "pizarra cognitiva").
- **StatePatch**: cambio propuesto por un agente sobre el estado cognitivo, validado y
  aplicado contra una versión conocida.
- **Memory**: las cinco categorías mínimas que el estado cognitivo debe distinguir —
  trabajo, episódica de sesión, semántica de materiales, procedimental de agentes/agencias
  y metacognitiva de fallos y verificaciones.
- **GeneratedProposal**: salida candidata producida por un agente generador que todavía no
  está autorizada para mostrarse al participante.
- **VerificationResult**: clasificación observable del control constitucional sobre una
  propuesta, con un veredicto cerrado de cuatro valores (aprobado, reformular, aclarar o
  bloquear); las razones concretas de cada veredicto se registran como texto observable
  adicional (`reasons`), no como veredictos nuevos.
- **DialogueAction**: la acción conversacional elegida para un turno (responder, preguntar,
  aclarar, reconocer falta de información, resumir o finalizar).
- **TraceEvent**: registro estructurado de ejecución, decisión, cambio de estado, error o
  recurso consumido, asociado a una sesión y un turno.
- **RetentionPolicy**: reglas versionadas de conservación de los datos de una actividad
  (contenido, plazo, acceso y purga).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Se pueden registrar al menos cinco agentes de prueba bajo el mismo contrato
  sin modificar el orquestador.
- **SC-002**: Se pueden definir al menos dos agencias distintas que reutilizan agentes ya
  registrados en el catálogo.
- **SC-003**: El 100% de los cambios del estado cognitivo de una sesión quedan versionados
  como `StatePatch` reconstruibles, aplicados exclusivamente por el motor de estado (nunca
  escritos directamente por un agente). Esta feature no integra ningún modelo de lenguaje
  real (ver Assumptions); la ausencia de estado dentro de un contexto de LLM se revalida
  cuando se introduzca un intérprete real en una feature posterior.
- **SC-004**: El 100% de los turnos completados de una sesión pueden reconstruirse por
  completo (agentes, mensajes internos, cambios de estado y decisión) a partir de los
  registros, incluso después de reiniciar la aplicación.
- **SC-005**: El 100% de las salidas de prueba que asignan una nota, suplantan al profesor
  o emiten una decisión académica quedan bloqueadas antes de llegar al participante.
- **SC-006**: El 100% de los timeouts o errores de esquema de un agente de prueba
  producen una degradación controlada sin dejar el estado cognitivo en una versión
  inconsistente o corrupta.
- **SC-007**: Un participante puede completar un ciclo íntegro de sesión (inicio, un
  turno de texto, finalización voluntaria y resumen técnico) sin intervención técnica
  externa.
- **SC-008**: Las pruebas automatizadas demuestran que un agente puede sustituirse por
  otro que cumpla el mismo contrato sin cambios en las agencias ni en el orquestador.

## Assumptions

- El flujo de "interpretación" de un turno en esta feature puede resolverse mediante
  lógica simulada o determinista; la comprensión de lenguaje natural real, la recuperación
  documental (RAG) y la verificación de fundamentación llegan en features posteriores
  (002 en adelante) y quedan fuera de esta especificación.
- El sistema opera para un único operador local por instancia (perfil profesor/
  investigador/administrador) sin sistema de autenticación institucional; el acceso se
  limita por estar vinculado únicamente a la máquina local (Principio VII de la
  constitución). El punto de extensión de credencial administrativa (FR-021a) queda
  deshabilitado por defecto en esta feature (ver Clarifications).
- El sistema admite una única sesión interactiva activa por instancia en esta primera
  versión (ver Clarifications); pueden conservarse múltiples sesiones históricas cerradas.
  El escenario de conflicto de escritura (User Story 5) se refiere a operaciones
  concurrentes dentro de esa única sesión activa (por ejemplo, dos agentes que intentan
  parchear el estado a la vez), no entre sesiones distintas. El diseño no debe impedir
  ampliar la concurrencia de sesiones en el futuro.
- La modalidad de voz, la transcripción y su revisión no forman parte de esta feature; la
  interacción se realiza íntegramente por texto, conforme al alcance declarado en
  `docs/ORAL-IA_SpecKit/features/001_core_runtime_specify.md`.
- El "resumen técnico básico" generado al finalizar una sesión es un resumen operativo del
  desarrollo de la sesión (agentes ejecutados, incidencias, duración), no una evaluación ni
  una calificación del participante.
- No existe todavía ingestión real de materiales docentes; el campo "materiales permitidos"
  del estado cognitivo puede permanecer vacío durante esta feature.
