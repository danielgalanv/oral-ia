# Disposición individual de los418identificadores

Cada entrada contiene la decisión de necesidad, motivo, familia, fuente y requisito completo. No certifica cumplimiento ni cambia obligaciones. Los motivos compartidos corresponden a grupos cuyos textos se han leído; no proceden de una clasificación por palabras clave. `012/SC001` es alias documental de `012/SC-001`, no otro requisito formal.

## 001/FR-014 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 278. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: El sistema MUST evaluar toda propuesta de salida mediante un control constitucional capaz de bloquear mensajes que asignen notas, suplanten al profesor, emitan decisiones académicas, revelen datos no autorizados o se salgan del alcance de la actividad, antes de que la salida llegue al participante. Para detectar revelación de datos no autorizados y salidas fuera de alcance, la autoridad MUST ser una política explícita y versionada definida por la configuración docente, con permisos de divulgación y límites de alcance comprobables. El orquestador MUST entregar al control una instantánea mínima, confiable y filtrada de la política aplicable, tanto en la ruta normal como en todas las respuestas alternativas. La elección del medio de transporte, su esquema y sus tipos queda diferida a `plan.md` y los contratos internos, sin fijarse en esta especificación funcional. El control MUST NOT consultar directamente toda la base de datos ni sustituir estas decisiones contextuales por patrones literales sobre el texto propuesto; esta responsabilidad es distinta de la autorización de materiales de la Feature 002. La divulgación de datos al participante MUST requerir autorización explícita y comprobable de su categoría, procedencia y destinatario conforme a esa política; los datos sin autorización comprobable MUST bloquearse, incluidas las categorías no contempladas por la política. El alcance autorizado MUST delimitar explícitamente los temas, propósitos y acciones permitidos por la actividad, incluidos los mensajes operativos seguros. El uso de conocimiento general MUST sujetarse a la configuración de la actividad; su autorización MUST NOT interpretarse como permiso para exceder los límites de alcance definidos. La comprobación de divulgación y alcance MUST ser estructural y determinista: todo contenido sujeto a autorización MUST tener una vinculación comprobable con los datos y el alcance permitidos, contrastada con información confiable suministrada por el orquestador. La declaración del generador de que su salida está permitida MUST NOT bastar para autorizarla. El contenido sin vinculación verificable MUST bloquearse; esta comprobación MUST poder probarse mediante una matriz positiva y negativa determinista. Si falta la política, el contexto es inválido o no puede verificarse la vinculación del contenido, el sistema MUST bloquear la propuesta y registrar la causa, aplicando la recuperación segura definida en FR-015.

## 001/FR-001 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 223. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST permitir crear y versionar una configuración de actividad con nombre, asignatura, objetivo, modo, idioma, límite de turnos, duración, conocimiento general permitido o prohibido, agentes obligatorios y opcionales, y política de conservación.

## 001/FR-002 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 227. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: Una configuración de actividad utilizada por al menos una sesión MUST volverse inmutable; cualquier cambio posterior MUST crear una nueva versión.

## 001/FR-003 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Catálogo, cinco agentes, dos agencias y sustitución sin cambios prueban la hipótesis de arquitectura; conservar lo existente, pero no condicionar a nuevas demostraciones la utilidad del chat.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 229. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: El sistema MUST exponer un catálogo consultable de agentes y agencias con identificador, versión, capacidades, permisos, contrato y estado de disponibilidad.

## 001/FR-004 — sustituir mecanismo

Familia: N06. Necesidad: necesario con mecanismo prescriptivo.

Motivo: Mantener contratos y estado explícito; campos de confianza, prioridades y taxonomías solo donde un consumidor o control los necesite, evitando burocracia por cada función auxiliar. La compatibilidad constitucional se revisa antes de cambiar.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 231. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: Todo agente registrado MUST declarar un contrato versionado con identificador, versión, propósito, entradas, salidas estructuradas, precondiciones, postcondiciones, fuentes y herramientas permitidas, permisos, tiempo máximo, consumo esperado, errores posibles, confianza, criterios de éxito, terminación, cancelación y datos de trazabilidad.

## 001/FR-005 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Catálogo, cinco agentes, dos agencias y sustitución sin cambios prueban la hipótesis de arquitectura; conservar lo existente, pero no condicionar a nuevas demostraciones la utilidad del chat.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 236. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST permitir registrar al menos cinco agentes de prueba distintos bajo el mismo contrato sin requerir cambios en el orquestador.

## 001/FR-006 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Catálogo, cinco agentes, dos agencias y sustitución sin cambios prueban la hipótesis de arquitectura; conservar lo existente, pero no condicionar a nuevas demostraciones la utilidad del chat.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 238. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST permitir componer al menos dos agencias distintas que reutilicen agentes ya registrados en el catálogo, sin crear código ni agentes nuevos durante la ejecución.

## 001/FR-007 — sustituir mecanismo

Familia: N06. Necesidad: necesario con mecanismo prescriptivo.

Motivo: Mantener contratos y estado explícito; campos de confianza, prioridades y taxonomías solo donde un consumidor o control los necesite, evitando burocracia por cada función auxiliar. La compatibilidad constitucional se revisa antes de cambiar.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 241. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: Los agentes y el orquestador MUST intercambiar mensajes internos estructurados con identificador, sesión, emisor, receptor, tipo, objetivo, contenido, evidencias, fuentes, confianza, prioridad, vigencia, respuesta esperada y condición de éxito.

## 001/FR-008 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 245. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: El sistema MUST mantener una pizarra cognitiva de sesión externa al contexto privado del modelo de lenguaje, con control de versiones y un registro de cada cambio (agente responsable, versión previa, versión resultante, instante y justificación).

## 001/FR-009 — sustituir mecanismo

Familia: N06. Necesidad: necesario con mecanismo prescriptivo.

Motivo: Mantener contratos y estado explícito; campos de confianza, prioridades y taxonomías solo donde un consumidor o control los necesite, evitando burocracia por cada función auxiliar. La compatibilidad constitucional se revisa antes de cambiar.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 249. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El estado cognitivo de sesión MUST incluir como mínimo: modo activo, objetivo, actividad, materiales permitidos (aunque estén vacíos), pregunta o entrada actual, respuesta del participante, conceptos tratados y pendientes, hipótesis de intención, información recuperada, dudas, historial resumido, tiempo restante, número de turnos, incidencias, confianza y siguiente acción propuesta, distinguiendo el tipo de cada elemento (instrucción, observación, afirmación del participante, información recuperada, hipótesis, inferencia, decisión, resultado de comprobación o configuración).

## 001/FR-010 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 256. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: El sistema MUST permitir a un participante iniciar una sesión local con un código seudónimo y una actividad autorizada, y MUST mostrarle de forma explícita que interactúa con un sistema automático antes de aceptar su primer mensaje.

## 001/FR-011 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 259. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: El sistema MUST gestionar el ciclo de vida de una sesión (inicio, aplicación de configuración, turnos, duración, finalización y persistencia).

## 001/FR-011a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 261. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011a**: Cuando se alcance el límite de turnos o la duración máxima configurada de la actividad antes de que el participante finalice voluntariamente, el sistema MUST cerrar la sesión de forma segura (`status = closed_limit_reached`) y MUST generar igualmente el resumen técnico básico (FR-012b).

## 001/FR-012 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 265. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST permitir al participante intercambiar al menos mensajes de texto y finalizar la sesión voluntariamente en cualquier momento.

## 001/FR-012a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 267. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012a**: El sistema MUST admitir como máximo una sesión interactiva activa por instancia; MUST rechazar el intento de iniciar una segunda sesión interactiva mientras otra está activa, sin impedir que se conserven y consulten múltiples sesiones históricas ya cerradas.

## 001/FR-012b — sustituir mecanismo

Familia: N08. Necesidad: prescripción histórica a conciliar.

Motivo: Confirmar cierre sin juicios es necesario; la exclusión absoluta de un resumen útil al participante era una restricción técnica inicial, a conciliar con resumen descriptivo y scopes posteriores.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 271. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012b**: Al finalizar una sesión, el sistema MUST mostrar al participante únicamente una confirmación breve de cierre, sin calificaciones ni juicios académicos; el resumen técnico básico completo (agentes ejecutados, incidencias, decisiones) MUST quedar disponible solo en el área técnica o de investigador.

## 001/FR-013 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 275. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST seleccionar, para cada turno, una acción conversacional entre responder con un mensaje controlado, solicitar aclaración, reconocer falta de información, resumir o finalizar.

## 001/FR-015 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 309. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: Toda salida bloqueada por el control constitucional MUST quedar registrada con su causa; el sistema MUST NOT revelar al participante el contenido prohibido. Como recuperación, MUST intentar una única respuesta operativa mínima, segura y predefinida, cuya autorización y contenido puedan verificarse de forma independiente conforme a FR-014. MUST mostrarla únicamente si supera esa verificación y el mismo control constitucional. Si tampoco puede autorizarse, MUST finalizar de forma segura sin presentar contenido y sin encadenar nuevas respuestas alternativas para esta incidencia. El bloqueo MUST NOT implicar una obligación incondicional de mostrar un mensaje.

## 001/FR-016 — sustituir mecanismo

Familia: N12. Necesidad: necesario con evidencia proporcional.

Motivo: Conservar trazabilidad y diagnóstico suficientes; usar registros mínimos y referencias compartidas, reconstruyendo solo sesiones conservadas conforme a consentimiento, sin duplicar snapshots completos.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 317. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: El sistema MUST registrar un evento de trazabilidad por sesión, turno, agente ejecutado y cambio de estado, permitiendo reconstruir la secuencia completa de un turno a partir de los registros.

## 001/FR-017 — sustituir mecanismo

Familia: N12. Necesidad: necesario con evidencia proporcional.

Motivo: Conservar trazabilidad y diagnóstico suficientes; usar registros mínimos y referencias compartidas, reconstruyendo solo sesiones conservadas conforme a consentimiento, sin duplicar snapshots completos.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 320. Contexto: ### Functional Requirements.

Requisito leído: - **FR-017**: El sistema MUST monitorizar tiempo de ejecución, uso básico de CPU y memoria, errores y timeouts por agente y por sesión.

## 001/FR-018 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 322. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018**: Cuando un agente falle, exceda su tiempo máximo o produzca una salida que no cumpla su contrato, el sistema MUST degradar de forma controlada: registrar el fallo, evitar corromper el estado cognitivo y aplicar una alternativa configurada o finalizar el turno de forma segura.

## 001/FR-018a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 326. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018a**: La degradación controlada (FR-018) MUST NOT omitir ni saltarse el control constitucional (FR-014) sobre la salida final; toda salida presentada al participante, incluida la producida tras una degradación o un fallback, MUST pasar por el control constitucional antes de mostrarse (Constitución Principio IX: los controles constitucionales nunca pueden omitirse por ahorro de recursos).

## 001/FR-019 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 331. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019**: Cuando dos operaciones intenten actualizar la misma versión conocida del estado cognitivo, el sistema MUST detectar el conflicto, MUST NOT sobrescribir silenciosamente ninguna de las dos, y MUST conservar una secuencia reconstruible de ambas.

## 001/FR-020 — sustituir mecanismo

Familia: N12. Necesidad: necesario con evidencia proporcional.

Motivo: Conservar trazabilidad y diagnóstico suficientes; usar registros mínimos y referencias compartidas, reconstruyendo solo sesiones conservadas conforme a consentimiento, sin duplicar snapshots completos.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 335. Contexto: ### Functional Requirements.

Requisito leído: - **FR-020**: Tras cerrar o reiniciar la aplicación, el sistema MUST permitir abrir una sesión conservada y reconstruir su configuración, turnos, agentes ejecutados, decisiones y cambios de estado.

## 001/FR-021 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 338. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021**: El sistema MUST ofrecer una interfaz web local mínima con un área de participante y un área técnica o docente suficientes para ejercitar las capacidades anteriores.

## 001/FR-021a — retirar del criterio del producto actual

Familia: N05. Necesidad: restricción histórica superada.

Motivo: Dejar autenticación deshabilitada era un aplazamiento exclusivo de Feature001; no es una necesidad actual y nunca debe restaurarse frente a la autenticación posterior.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 341. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021a**: El sistema MUST proveer un punto de extensión de control de acceso (credencial administrativa) para el área técnica o docente, pero MUST dejarlo deshabilitado por defecto en esta feature; su activación completa queda fuera de alcance y se implementará en la feature de configuración docente, revisión y privacidad.

## 001/FR-022 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 346. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022**: El sistema MUST vincularse por defecto únicamente a la máquina local y MUST NOT requerir integración institucional ni identidad real para operar.

## 001/FR-023 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 348. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023**: El código de participante MUST ser un identificador seudónimo y MUST NOT contener datos personales.

## 001/FR-024 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 350. Contexto: ### Functional Requirements.

Requisito leído: - **FR-024**: El sistema MUST NOT almacenar cadenas de razonamiento privadas de los modelos en los registros de trazabilidad; MUST registrar resultados estructurados y justificaciones operativas observables.

## 001/FR-025 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 353. Contexto: ### Functional Requirements.

Requisito leído: - **FR-025**: La interfaz web mínima (FR-021) MUST ser operable íntegramente por teclado, MUST ofrecer etiquetas accesibles en todos los controles interactivos, MUST mantener contraste suficiente para texto y controles, y MUST presentar mensajes de error en lenguaje comprensible con una acción siguiente clara (Constitución Principio VII).

## 001/SC-001 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Catálogo, cinco agentes, dos agencias y sustitución sin cambios prueban la hipótesis de arquitectura; conservar lo existente, pero no condicionar a nuevas demostraciones la utilidad del chat.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 403. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: Se pueden registrar al menos cinco agentes de prueba bajo el mismo contrato sin modificar el orquestador.

## 001/SC-002 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Catálogo, cinco agentes, dos agencias y sustitución sin cambios prueban la hipótesis de arquitectura; conservar lo existente, pero no condicionar a nuevas demostraciones la utilidad del chat.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 405. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: Se pueden definir al menos dos agencias distintas que reutilizan agentes ya registrados en el catálogo.

## 001/SC-003 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 407. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: El 100% de los cambios del estado cognitivo de una sesión quedan versionados como `StatePatch` reconstruibles, aplicados exclusivamente por el motor de estado (nunca escritos directamente por un agente). Esta feature no integra ningún modelo de lenguaje real (ver Assumptions); la ausencia de estado dentro de un contexto de LLM se revalida cuando se introduzca un intérprete real en una feature posterior.

## 001/SC-004 — sustituir mecanismo

Familia: N12. Necesidad: necesario con evidencia proporcional.

Motivo: Conservar trazabilidad y diagnóstico suficientes; usar registros mínimos y referencias compartidas, reconstruyendo solo sesiones conservadas conforme a consentimiento, sin duplicar snapshots completos.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 412. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El 100% de los turnos completados de una sesión pueden reconstruirse por completo (agentes, mensajes internos, cambios de estado y decisión) a partir de los registros, incluso después de reiniciar la aplicación.

## 001/SC-005 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 415. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: El 100% de las salidas de prueba que asignan una nota, suplantan al profesor o emiten una decisión académica quedan bloqueadas antes de llegar al participante.

## 001/SC-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Límites, autoridad fuera del generador, fallback acotado, aislamiento, privacidad y estado coherente evitan daños o pérdida de control; simplificar duplicaciones no elimina estas garantías.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 417. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: El 100% de los timeouts o errores de esquema de un agente de prueba producen una degradación controlada sin dejar el estado cognitivo en una versión inconsistente o corrupta.

## 001/SC-007 — conservar para uso actual

Familia: N06. Necesidad: imprescindible.

Motivo: La actividad, el estado externo y el flujo textual accesible son necesarios para estudiar y reconstruir lo ocurrido; no implican desplegar todas las agencias históricas.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 420. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-007**: Un participante puede completar un ciclo íntegro de sesión (inicio, un turno de texto, finalización voluntaria y resumen técnico) sin intervención técnica externa.

## 001/SC-008 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Catálogo, cinco agentes, dos agencias y sustitución sin cambios prueban la hipótesis de arquitectura; conservar lo existente, pero no condicionar a nuevas demostraciones la utilidad del chat.

Fuente: [specs/001-core-cognitive-runtime/spec.md](../../../specs/001-core-cognitive-runtime/spec.md), línea 423. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-008**: Las pruebas automatizadas demuestran que un agente puede sustituirse por otro que cumpla el mismo contrato sin cambios en las agencias ni en el orquestador.

## 002/FR-001 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 319. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST permitir a un profesor incorporar documentos dentro de una asignatura ya existente (entidad `Course`, definida en la Feature 001).

## 002/FR-002 — aplazar nueva ampliación

Familia: N03. Necesidad: deseable de alto valor condicionado al corpus.

Motivo: PDF y las diapositivas autorizadas cubren la necesidad actual; mantener soporte existente de otros formatos, sin convertir su expansión o equivalencia visual completa en prerrequisito del chat.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 321. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: El sistema MUST aceptar como formatos iniciales PDF textual, DOCX, PPTX, TXT y Markdown.

## 002/FR-003 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 323. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: El sistema MUST identificar los documentos no procesables (por ejemplo, escaneados sin texto extraíble) como tales, en vez de indexarlos de forma incompleta y silenciosa.

## 002/FR-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 326. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: El sistema MUST validar formato, tamaño e integridad de cada archivo recibido antes de procesarlo, rechazando los archivos inválidos con un mensaje accionable.

## 002/FR-005 — conservar para uso actual

Familia: N03. Necesidad: imprescindible para procedencia.

Motivo: El hash permite identificar originales, evitar duplicados y revisar versiones sin exigir copia nueva de cada documento para cada ensayo.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 329. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST calcular un identificador de contenido (hash) por documento para evitar duplicados accidentales.

## 002/FR-005a — sustituir mecanismo

Familia: N08. Necesidad: necesidad real con flujo mejorable.

Motivo: Preservar la decisión docente de reutilizar o publicar otra versión; presentar duplicados de forma no intrusiva y auditable sin multiplicar cargas o alterar activación silenciosamente.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 331. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005a**: Cuando el hash de un archivo cargado coincida con el de un documento ya existente, el sistema MUST marcarlo como probable duplicado y MUST ofrecer al profesor la elección entre reutilizar/enlazar el documento existente con la actividad actual o continuar como una carga nueva y distinta; el sistema MUST NOT decidir esto de forma automática (ver Clarifications; Constitución Principio VI — toda modificación de materiales debe ser una decisión manual y auditable). Si el profesor elige reutilizar/enlazar, el sistema MUST asociar el documento existente a la actividad actual sin alterar su estado de activación vigente ni requerir un nuevo ciclo de procesamiento.

## 002/FR-006 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 340. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST extraer el texto de cada documento conservando referencias de ubicación (página, diapositiva, sección o párrafo) cuando el formato lo permita.

## 002/FR-007 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 343. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: El sistema MUST segmentar el texto extraído de forma configurable y reproducible: la misma configuración sobre el mismo documento MUST producir los mismos fragmentos.

## 002/FR-008 — sustituir mecanismo

Familia: N03. Necesidad: mecanismo técnico no fin en sí mismo.

Motivo: Conservar metadatos y recuperación local reproducible, pero justificar cada campo y elegir léxico, denso o híbrido por resultado. Igualdad exacta solo bajo condiciones compatibles; identidad de encoder e índice es esencial.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 346. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: El sistema MUST generar, para cada documento y fragmento, como mínimo los metadatos: identificador, documento de origen, versión, hash, ubicación (página/diapositiva/sección), tipo de contenido, asignatura, actividad, fecha de incorporación, estado de autorización, vigencia, prioridad, idioma y estado de indexación. El campo "prioridad" MUST utilizarse únicamente para influir en el orden de relevancia de la recuperación (FR-018); MUST NOT interpretarse ni utilizarse como una medida de dificultad atribuida a ningún participante.

## 002/FR-009 — sustituir mecanismo

Familia: N03. Necesidad: mecanismo técnico no fin en sí mismo.

Motivo: Conservar metadatos y recuperación local reproducible, pero justificar cada campo y elegir léxico, denso o híbrido por resultado. Igualdad exacta solo bajo condiciones compatibles; identidad de encoder e índice es esencial.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 353. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El sistema MUST generar embeddings y construir el índice de recuperación de forma local, sin depender de servicios externos.

## 002/FR-010 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 355. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: El sistema MUST ejecutar comprobaciones de cobertura (proporción de páginas, diapositivas, secciones o párrafos de los que se extrajo texto utilizable respecto del total del documento) y errores tras indexar un documento, y reportarlas al profesor.

## 002/FR-011 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 359. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: Un documento MUST permanecer inutilizable en sesiones hasta que su procesamiento se complete y un profesor lo active manualmente.

## 002/FR-012 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 361. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST permitir a un profesor consultar el estado de procesamiento de cada documento (pendiente, procesado, en error, activo o inactivo).

## 002/FR-013 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 363. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST permitir a un profesor activar o desactivar materiales y asignarlos a actividades específicas. Un material desactivado (a diferencia de uno retirado, FR-015) MUST poder reactivarse posteriormente por el profesor.

## 002/FR-013a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 366. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013a**: El sistema MUST rechazar la asignación de una versión retirada o inactiva de un documento a una nueva actividad; solo la versión activa vigente de un documento MUST poder asignarse.

## 002/FR-014 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 369. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: El sistema MUST permitir a un profesor sustituir un documento por una nueva versión sin eliminar la versión anterior del registro histórico. La nueva versión MAY estar en un formato admitido (FR-002) distinto al de la versión anterior.

## 002/FR-015 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 372. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: Cuando una versión de un documento se sustituye o desactiva, el sistema MUST impedir que sesiones nuevas recuperen fragmentos de esa versión, y MUST conservar la referencia histórica necesaria para auditar las sesiones que ya la utilizaron —como mínimo, el documento, la versión, el contenido de los fragmentos usados y su ubicación en el momento en que la sesión los utilizó. A diferencia de un material desactivado (FR-013), una versión retirada MUST NOT poder reactivarse; para volver a usar su contenido, el profesor MUST crear una nueva versión.

## 002/FR-016 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 379. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: El sistema MUST permitir a un profesor reconstruir el índice de materiales sin perder la relación entre documentos, fragmentos y versiones.

## 002/FR-016a — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 381. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016a**: La reconstrucción del índice MUST preservar los identificadores existentes de cada fragmento o, si se regeneran, MUST actualizar las referencias ya existentes en `Evidence`, `GroundingVerificationResult` y `MaterialConflictRecord`, de modo que ningún registro previamente creado quede huérfano tras una reconstrucción.

## 002/FR-017 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 385. Contexto: ### Functional Requirements.

Requisito leído: - **FR-017**: El agente de recuperación MUST aceptar una consulta junto con filtros de autorización (sesión, asignatura, actividad, materiales permitidos), un número máximo de fragmentos y un presupuesto temporal.

## 002/FR-018 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 388. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018**: El agente de recuperación MUST devolver, por cada resultado: los fragmentos, su procedencia (documento, versión, ubicación), relevancia, metadatos, la versión del índice utilizada, advertencias y los conflictos detectados.

## 002/FR-019 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 391. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019**: El agente de recuperación MUST NOT devolver fragmentos de una asignatura, actividad, versión retirada o material inactivo distintos de los autorizados para la sesión en curso.

## 002/FR-019a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 394. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019a**: El agente de recuperación MUST excluir de sus resultados los fragmentos cuyo material haya superado su vigencia configurada (FR-008), tratándolos como si estuvieran retirados.

## 002/FR-020 — sustituir mecanismo

Familia: N03. Necesidad: mecanismo técnico no fin en sí mismo.

Motivo: Conservar metadatos y recuperación local reproducible, pero justificar cada campo y elegir léxico, denso o híbrido por resultado. Igualdad exacta solo bajo condiciones compatibles; identidad de encoder e índice es esencial.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 397. Contexto: ### Functional Requirements.

Requisito leído: - **FR-020**: Una recuperación MUST ser repetible: la misma consulta, configuración y versión de índice MUST producir el mismo resultado, en el mismo orden.

## 002/FR-021 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 399. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021**: Cuando una consulta no tenga cobertura suficiente en los materiales autorizados, el sistema MUST señalarlo explícitamente en vez de generar una respuesta presentada como fundamentada.

## 002/FR-022 — decisión pendiente

Familia: N14. Necesidad: necesario con alcance empírico por decidir.

Motivo: Detectar conflictos y apoyo es necesario, pero no hay validación semántica exhaustiva demostrada. Precisar cobertura, falsos permisos y límites del juicio; un cien por cien en un banco no garantiza todos los casos.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 402. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022**: Cuando dos o más materiales activos autorizados contengan afirmaciones incompatibles relevantes para la misma consulta, la recuperación MUST devolver ambas evidencias y marcar el conflicto de forma explícita.

## 002/FR-022a — conservar para uso actual

Familia: N08. Necesidad: imprescindible para conflictos conocidos.

Motivo: Un conflicto conocido debe permanecer visible hasta revisión para no alternar decisiones; no obliga a construir detección universal automática ni una nueva base de conocimiento.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 405. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022a**: Todo conflicto detectado entre materiales MUST quedar registrado de forma persistente y visible en el área de materiales del profesor (documentos y afirmaciones implicadas), no únicamente como un campo transitorio de la respuesta de la consulta que lo detectó (ver Clarifications; Constitución Principio VI).

## 002/FR-022b — conservar para uso actual

Familia: N08. Necesidad: imprescindible para conflictos conocidos.

Motivo: Un conflicto conocido debe permanecer visible hasta revisión para no alternar decisiones; no obliga a construir detección universal automática ni una nueva base de conocimiento.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 409. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022b**: Un conflicto registrado que siga pendiente de revisión MUST seguir devolviéndose como conflictivo en cualquier consulta posterior que recupere los mismos materiales implicados, hasta que el profesor lo revise (FR-022a).

## 002/FR-023 — decisión pendiente

Familia: N14. Necesidad: necesario con alcance empírico por decidir.

Motivo: Detectar conflictos y apoyo es necesario, pero no hay validación semántica exhaustiva demostrada. Precisar cobertura, falsos permisos y límites del juicio; un cien por cien en un banco no garantiza todos los casos.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 412. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023**: Un verificador de fundamentación MUST clasificar cada propuesta de salida como fundamentada, parcialmente fundamentada, no fundamentada, conflictiva o no verificable, indicando qué afirmaciones tienen soporte y cuáles no. Este veredicto MUST evaluar exclusivamente la propuesta y su respaldo documental; MUST NOT interpretarse ni utilizarse como una medida de la capacidad o el desempeño del participante.

## 002/FR-023a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 418. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023a**: El sistema MUST NOT agregar ni acumular los veredictos de fundamentación de un participante a lo largo de una o varias sesiones como una señal de su capacidad o progreso.

## 002/FR-024 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 421. Contexto: ### Functional Requirements.

Requisito leído: - **FR-024**: Cuando el conocimiento general esté desactivado para la actividad (`ActivityConfiguration.general_knowledge_allowed = false`, Feature 001) y no exista evidencia suficiente, el sistema MUST reconocer la limitación o solicitar aclaración en vez de responder como hecho de la asignatura.

## 002/FR-025 — aplazar nueva ampliación

Familia: N05. Necesidad: futuro condicionado a autorización.

Motivo: El conocimiento general está desactivado en el objetivo actual; conservar etiquetado y permiso si una actividad futura lo habilita, sin activarlo ahora.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 425. Contexto: ### Functional Requirements.

Requisito leído: - **FR-025**: Cuando el conocimiento general esté permitido para la actividad, el sistema MUST etiquetar explícitamente el contenido no recuperado de los materiales como conocimiento general, distinguiéndolo del contenido fundamentado.

## 002/FR-026 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 428. Contexto: ### Functional Requirements.

Requisito leído: - **FR-026**: Un intento de recuperación que solicite materiales fuera del alcance autorizado de la sesión (otra asignatura o actividad) MUST ser bloqueado y MUST quedar registrado de forma trazable.

## 002/FR-027 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 431. Contexto: ### Functional Requirements.

Requisito leído: - **FR-027**: Un fallo de extracción o indexación de un documento MUST producir un error accionable para el profesor, MUST NOT activar el documento, y MUST NOT afectar la disponibilidad del índice ya existente.

## 002/FR-028 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 434. Contexto: ### Functional Requirements.

Requisito leído: - **FR-028**: El sistema MUST tratar el texto extraído de los documentos como datos, nunca como instrucciones ejecutables para los agentes, incluso si su contenido imita instrucciones del sistema.

## 002/FR-029 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 437. Contexto: ### Functional Requirements.

Requisito leído: - **FR-029**: El sistema MUST conservar la trazabilidad de cada fragmento devuelto hasta su documento, versión y ubicación de origen.

## 002/FR-030 — fusionar obligación equivalente

Familia: N05. Necesidad: redundancia de garantía transversal.

Motivo: Preservar controles y mantener separados grounding y autorización; consolidar la obligación transversal de compatibilidad sin exigir inmovilidad de todo código histórico.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 439. Contexto: ### Functional Requirements.

Requisito leído: - **FR-030**: Esta feature MUST NOT modificar el comportamiento ya validado del núcleo cognitivo de la Feature 001 (contratos de agente, ciclo de sesión/turno, control constitucional, versionado del estado cognitivo); únicamente añade materiales, recuperación y verificación de fundamentación como capacidades nuevas. El veredicto de fundamentación de esta feature y el veredicto constitucional de la Feature 001 MUST evaluarse y registrarse de forma independiente; ninguno de los dos MUST sustituir, ocultar o sobrescribir al otro.

## 002/FR-031 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 446. Contexto: ### Functional Requirements.

Requisito leído: - **FR-031**: Los endpoints de gestión de materiales de esta feature MUST heredar el mismo vínculo exclusivo a la máquina local (`127.0.0.1`) ya establecido en la Feature 001 (FR-022); esta feature MUST NOT introducir un nuevo punto de exposición de red.

## 002/FR-032 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 449. Contexto: ### Functional Requirements.

Requisito leído: - **FR-032**: Las pantallas nuevas del área técnica introducidas por esta feature (carga, activación, revisión de conflictos, resolución de duplicados) MUST cumplir el mismo estándar de accesibilidad ya exigido en la Feature 001 (FR-025): operables íntegramente por teclado, con etiquetas accesibles, contraste suficiente, y mensajes de error comprensibles que no dependan únicamente del color para transmitir su significado.

## 002/SC-001 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 509. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: El 100% de los fragmentos recuperados en las pruebas pueden atribuirse a su documento, versión y ubicación de origen.

## 002/SC-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 511. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: El 0% de los resultados de recuperación en sesiones de prueba incluye material inactivo o una versión retirada.

## 002/SC-003 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 513. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: Tras sustituir la versión de un documento, el 100% de las sesiones nuevas de prueba obtienen únicamente fragmentos de la versión activa.

## 002/SC-004 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 515. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El 100% de las consultas de prueba sin evidencia suficiente generan una señal explícita y trazable en vez de una respuesta presentada como fundamentada.

## 002/SC-005 — decisión pendiente

Familia: N14. Necesidad: necesario con alcance empírico por decidir.

Motivo: Detectar conflictos y apoyo es necesario, pero no hay validación semántica exhaustiva demostrada. Precisar cobertura, falsos permisos y límites del juicio; un cien por cien en un banco no garantiza todos los casos.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 517. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: El verificador de fundamentación detecta el 100% de las referencias que no respaldan la afirmación atribuida en el conjunto de pruebas preparado para esta feature.

## 002/SC-006 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 520. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: El índice puede reconstruirse por completo sin pérdida de la relación entre documentos, fragmentos y versiones, verificable comparando el índice reconstruido con el original.

## 002/SC-007 — conservar para uso actual

Familia: N03. Necesidad: imprescindible.

Motivo: Permitir preparar, actualizar y recuperar materiales comprensibles y trazables es necesario para el uso; los fallos de cobertura y actualización deben ser visibles, con pruebas proporcionadas.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 523. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-007**: Un profesor puede cargar, procesar y activar un documento de prueba en un único flujo sin intervención técnica externa.

## 002/SC-008 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Validar archivos, activar fuentes explícitamente y filtrar actividad, vigencia y datos no confiables es una necesidad de permiso y privacidad, no ceremonia prescindible.

Fuente: [specs/002-materials-rag/spec.md](../../../specs/002-materials-rag/spec.md), línea 525. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-008**: El 100% de los intentos de recuperación fuera del alcance autorizado (otra asignatura o actividad) de las pruebas quedan bloqueados y registrados.

## 003/FR-011 — aplazar nueva ampliación

Familia: N01. Necesidad: deseable posterior.

Motivo: Preguntas variadas de práctica aportan valor después del chat útil; conservar acotación a sesión y ausencia de clasificación académica cuando se habiliten.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 377. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: Las preguntas de práctica MUST derivarse de los objetivos, conceptos, materiales, dificultad orientativa e historial de preguntas ya realizadas **en la sesión actual**; este historial MUST NOT persistir ni ser consultable entre sesiones distintas del mismo participante (ver Clarifications).

## 003/FR-013 — conservar por seguridad

Familia: N05. Necesidad: seguridad de actividad condicional.

Motivo: Si una actividad prohíbe revelar soluciones, esa política debe respetarse con control independiente, también en pistas. No impone el modo de no revelar a toda explicación.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 391. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST NOT revelar automáticamente la solución de una pregunta de práctica cuando el modo de la actividad lo prohíba.

## 003/FR-013a — conservar por seguridad

Familia: N05. Necesidad: seguridad de actividad condicional.

Motivo: Si una actividad prohíbe revelar soluciones, esa política debe respetarse con control independiente, también en pistas. No impone el modo de no revelar a toda explicación.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 393. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013a**: La comprobación de que una salida generada no revela la solución (FR-013) MUST ejecutarse mediante un verificador independiente del agente que generó la pregunta — nunca únicamente mediante una instrucción dirigida al agente generador. Si la comprobación detecta que la salida revela la solución, la salida MUST rechazarse y MUST regenerarse o sustituirse por una alternativa determinista de reserva antes de mostrarse al estudiante. Esta comprobación MUST evaluar únicamente la salida generada por el sistema — MUST NOT evaluar ni calificar la respuesta del estudiante (ver FR-014).

## 003/FR-020 — fusionar obligación equivalente

Familia: N05. Necesidad: redundancia funcional consolidable.

Motivo: La notificación y cierre ordenado por límites ya forman parte del ciclo común; conservar comportamiento y una implementación, no varios cierres paralelos.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 420. Contexto: ### Functional Requirements.

Requisito leído: - **FR-020**: Al alcanzarse el límite de turnos o duración de la sesión, el sistema MUST avisar al estudiante y MUST permitir un cierre ordenado.

## 003/FR-001 — aplazar nueva ampliación

Familia: N01. Necesidad: deseable posterior.

Motivo: Los cinco modos son una capacidad histórica legítima, no cinco productos que deban validarse de nuevo antes del chat de dudas y explicación. Mantener interfaces y ampliar después práctica, exposición y repaso.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 317. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST ofrecer cinco modos de autoestudio, cada uno con un identificador canónico estable: resolución de dudas (`doubt_resolution`), explicación guiada (`guided_explanation`), preguntas de práctica (`practice_questions`), preparación de una exposición (`presentation_preparation`) y revisión de conceptos (`concept_review`).

## 003/FR-001a — aplazar nueva ampliación

Familia: N01. Necesidad: deseable posterior.

Motivo: Los cinco modos son una capacidad histórica legítima, no cinco productos que deban validarse de nuevo antes del chat de dudas y explicación. Mantener interfaces y ampliar después práctica, exposición y repaso.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 322. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001a**: Cada modo MUST producir un comportamiento observable y distinguible de los demás (ver Clarifications, sesión 2026-09-01), reutilizando siempre el mismo conjunto mínimo de agentes de la agencia (FR-003) — la diferencia MUST surgir de configuración, composición de agentes activados, política de diálogo y selección de acción conversacional, nunca de implementaciones independientes por modo: - `doubt_resolution`: parte de una pregunta o duda formulada por el estudiante y prioriza recuperación documental + respuesta fundamentada. - `guided_explanation`: desarrolla un concepto de forma progresiva, pudiendo dividir la explicación en pasos y solicitar confirmación del estudiante antes de continuar. - `practice_questions`: el sistema toma la iniciativa generando preguntas y gestionando las respuestas del estudiante, sin calificarlas (FR-014). - `presentation_preparation`: ayuda al estudiante a estructurar y ensayar una explicación o exposición sobre un tema, pudiendo pedir aclaraciones o ampliaciones. - `concept_review`: recorre o recupera conceptos previamente seleccionados para la actividad y permite repasarlos mediante explicaciones o preguntas.

## 003/FR-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 337. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: Cada actividad docente MUST poder habilitar solo un subconjunto de estos modos, no todos obligatoriamente.

## 003/FR-002a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 339. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002a**: Una configuración de actividad con el subconjunto de modos habilitados vacío MUST considerarse inválida y MUST rechazarse antes de permitir el inicio de cualquier sesión sobre esa actividad (ver Clarifications, sesión 2026-09-01).

## 003/FR-003 — sustituir mecanismo

Familia: N06. Necesidad: necesario con arquitectura prescriptiva.

Motivo: Conservar intención, recuperación y memoria funcional; número de agentes, confianza numérica y prohibición absoluta de reenviar todo un historial breve no son necesidades humanas. Versionar cambios y mantener límites y controles.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 342. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: Para cada turno, el orquestador MUST seleccionar únicamente los agentes necesarios entre el conjunto mínimo de la agencia (gestión de sesión, interpretación de intención, recuperación documental, respuesta fundamentada, generación de preguntas, gestión de diálogo, comprobación de fundamentación, coherencia conversacional, control constitucional y de seguridad, resumen de sesión, trazabilidad y recursos) y MUST registrar por qué activó cada uno.

## 003/FR-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 348. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: Los controles marcados como no omitibles (constitucional y de seguridad) MUST ejecutarse en todos los turnos, independientemente del modo o de la composición de agentes seleccionada.

## 003/FR-005 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 351. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST informar al estudiante del propósito y los límites de la actividad antes de aceptar su primera consulta.

## 003/FR-006 — sustituir mecanismo

Familia: N06. Necesidad: necesario con arquitectura prescriptiva.

Motivo: Conservar intención, recuperación y memoria funcional; número de agentes, confianza numérica y prohibición absoluta de reenviar todo un historial breve no son necesidades humanas. Versionar cambios y mantener límites y controles.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 353. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST interpretar cada consulta del estudiante como una hipótesis de intención con un valor de confianza asociado.

## 003/FR-007 — sustituir mecanismo

Familia: N06. Necesidad: necesario con arquitectura prescriptiva.

Motivo: Conservar intención, recuperación y memoria funcional; número de agentes, confianza numérica y prohibición absoluta de reenviar todo un historial breve no son necesidades humanas. Versionar cambios y mantener límites y controles.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 355. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: El sistema MUST recuperar materiales cuando la consulta lo requiera, utilizando el agente de recuperación ya definido en la Feature 002 sin modificar su contrato.

## 003/FR-008 — sustituir mecanismo

Familia: N06. Necesidad: necesario con arquitectura prescriptiva.

Motivo: Conservar intención, recuperación y memoria funcional; número de agentes, confianza numérica y prohibición absoluta de reenviar todo un historial breve no son necesidades humanas. Versionar cambios y mantener límites y controles.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 358. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: El sistema MUST generar una propuesta de respuesta, verificar su fundamentación y su conformidad constitucional, seleccionar la acción conversacional y actualizar el estado de la sesión, reutilizando los mecanismos de turno, estado y verificación ya establecidos en la Feature 001 sin modificarlos.

## 003/FR-008a — sustituir mecanismo

Familia: N01. Necesidad: incompatibilidad del mecanismo con el tutor actual.

Motivo: El fallo del modelo no debe perder la sesión; usar una salida operativa honesta o cierre seguro, sin convertir la alternativa determinista en respuesta académica prefabricada obligatoria.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 362. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008a**: El mecanismo que genera una respuesta fundamentada o una pregunta de práctica MUST tratarse como sujeto a degradación controlada (Principio IX): si no está disponible o no responde dentro de su límite de tiempo, el sistema MUST completar el turno igualmente mediante un mecanismo alternativo determinista, sin fallar el turno ni interrumpir la sesión.

## 003/FR-008b — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 367. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008b**: El texto de los materiales usado como evidencia para generar una respuesta o una pregunta de práctica MUST tratarse siempre como datos de entrada, nunca como instrucciones capaces de alterar el comportamiento del sistema — mismo principio ya aplicado a la recuperación documental en la Feature 002.

## 003/FR-009 — conservar para uso actual

Familia: N01. Necesidad: imprescindible.

Motivo: Adaptar explicación, reconocer bloqueo, conservar fuentes y evitar contradicción son necesidades de estudio. Los tests deben medir esos efectos, no solo acciones o etiquetas.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 371. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El estudiante MUST poder solicitar: una explicación más sencilla, un ejemplo, una comparación, una pregunta de práctica, un cambio de tema dentro del alcance autorizado, o la finalización de la sesión.

## 003/FR-010 — sustituir mecanismo

Familia: N06. Necesidad: necesario con arquitectura prescriptiva.

Motivo: Conservar intención, recuperación y memoria funcional; número de agentes, confianza numérica y prohibición absoluta de reenviar todo un historial breve no son necesidades humanas. Versionar cambios y mantener límites y controles.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 374. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: El sistema MUST recordar los conceptos ya tratados en la sesión y evitar repetición innecesaria sin reenviar el historial completo de la conversación en cada turno.

## 003/FR-011a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 381. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011a**: El sistema MUST NOT agregar, correlacionar ni construir un perfil académico, de capacidad, dificultad, rendimiento o personalidad del participante a partir de `PracticeQuestion`, `CoherenceIncident`, conceptos tratados, dudas manifestadas o resúmenes de distintas sesiones — toda esta información MUST permanecer acotada a la sesión que la generó. Cualquier memoria longitudinal entre sesiones del mismo `participant_code` queda fuera de alcance de esta feature y MUST ser objeto de una decisión y una feature futuras explícitas (ver Clarifications, sesión 2026-09-01).

## 003/FR-012 — aplazar nueva ampliación

Familia: N01. Necesidad: deseable posterior.

Motivo: Preguntas variadas de práctica aportan valor después del chat útil; conservar acotación a sesión y ausencia de clasificación académica cuando se habiliten.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 389. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST admitir preguntas de práctica de tipo explicación, aplicación, comparación, justificación o detección de errores.

## 003/FR-014 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 401. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: La respuesta del estudiante a una pregunta de práctica MAY utilizarse para seleccionar la siguiente acción o repregunta, pero MUST NOT producir una nota, clasificación o inferencia permanente de nivel del estudiante.

## 003/FR-015 — conservar para uso actual

Familia: N01. Necesidad: imprescindible.

Motivo: Adaptar explicación, reconocer bloqueo, conservar fuentes y evitar contradicción son necesidades de estudio. Los tests deben medir esos efectos, no solo acciones o etiquetas.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 404. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: El sistema MUST detectar, como mínimo: falta de información, respuesta no fundamentada, contradicción, repetición, pérdida del objetivo, exceso de turnos dedicados a un mismo concepto o duda sin resolución (una señal de coherencia, **distinta** del límite global de turnos de la sesión ya gobernado por FR-020), fallo de agente, latencia excesiva y ausencia de progreso.

## 003/FR-016 — conservar para uso actual

Familia: N01. Necesidad: imprescindible.

Motivo: Adaptar explicación, reconocer bloqueo, conservar fuentes y evitar contradicción son necesidades de estudio. Los tests deben medir esos efectos, no solo acciones o etiquetas.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 409. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: Ante cualquiera de las condiciones detectadas en FR-015, el sistema MUST poder aplicar al menos una de las siguientes acciones: volver a recuperar, reformular, pedir aclaración, reconocer desconocimiento, reducir la respuesta o finalizar de forma segura.

## 003/FR-017 — conservar para uso actual

Familia: N01. Necesidad: imprescindible.

Motivo: Adaptar explicación, reconocer bloqueo, conservar fuentes y evitar contradicción son necesidades de estudio. Los tests deben medir esos efectos, no solo acciones o etiquetas.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 413. Contexto: ### Functional Requirements.

Requisito leído: - **FR-017**: Una propuesta que contradiga una afirmación previa de la sesión o una fuente activa MUST ser bloqueada o reformulada por el verificador correspondiente, y la incidencia MUST quedar registrada de forma trazable.

## 003/FR-018 — conservar para uso actual

Familia: N01. Necesidad: imprescindible.

Motivo: Adaptar explicación, reconocer bloqueo, conservar fuentes y evitar contradicción son necesidades de estudio. Los tests deben medir esos efectos, no solo acciones o etiquetas.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 416. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018**: Cuando una respuesta use materiales, el estudiante MUST poder abrir una vista de fuentes con documento, versión, ubicación y el fragmento relevante.

## 003/FR-019 — aplazar nueva ampliación

Familia: N05. Necesidad: futuro condicionado.

Motivo: Etiquetado de conocimiento general solo procede si se habilita expresamente; no hace falta activar esa capacidad para el objetivo actual.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 418. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019**: Cuando se utilice conocimiento general permitido, el sistema MUST mostrar una indicación diferenciada de que no procede de los materiales.

## 003/FR-021 — decisión pendiente

Familia: N14. Necesidad: restricción ambigua entre versiones.

Motivo: Resumen útil y cierre visible son valiosos; la prohibición de consulta posterior, aun con conservación consentida, necesita conciliarse con revisión posterior y recuperación segura de Feature005.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 422. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021**: Si la actividad autoriza el resumen de sesión, el sistema MAY generar un resumen descriptivo que incluya temas tratados, preguntas realizadas, conceptos explicados, dudas manifestadas, incidencias y fuentes consultadas. El resumen MUST entregarse como una visualización única y efímera en la misma respuesta que cierra la sesión; el sistema MUST NOT ofrecer al participante una vía de consulta posterior a ese resumen (ver Clarifications).

## 003/FR-021a — decisión pendiente

Familia: N14. Necesidad: restricción ambigua entre versiones.

Motivo: Resumen útil y cierre visible son valiosos; la prohibición de consulta posterior, aun con conservación consentida, necesita conciliarse con revisión posterior y recuperación segura de Feature005.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 428. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021a** (aclaración añadida en la ronda de estabilización 2026-09-10 — no amplía la obligación MAY de FR-021 a un MUST, solo precisa cuál es "la respuesta que cierra la sesión" cuando existen dos vías de cierre distintas, FR-020): "la respuesta que cierra la sesión" MUST identificarse, en cada cierre concreto, con la respuesta HTTP del mecanismo que efectivamente cerró esa sesión — la respuesta de finalización voluntaria cuando el estudiante la solicita, o la respuesta del turno que hace que la sesión alcance su límite de turnos/duración cuando el cierre es automático (FR-020). Cuando la actividad autoriza el resumen y este se genera, su entrega y visualización MUST respetarse en cualquiera de los dos casos — un cierre automático MUST NOT descartar un resumen ya generado ni omitir comunicar el cierre en su propia respuesta.

## 003/FR-021b — decisión pendiente

Familia: N14. Necesidad: restricción ambigua entre versiones.

Motivo: Resumen útil y cierre visible son valiosos; la prohibición de consulta posterior, aun con conservación consentida, necesita conciliarse con revisión posterior y recuperación segura de Feature005.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 438. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021b** (requisito añadido en la ronda de estabilización 2026-09-10, decisión explícita sobre el cierre de autoestudio): la interfaz de participante MUST reconocer, a partir de la respuesta que cierra la sesión (voluntaria o automática), que la sesión ha finalizado, y MUST impedir el envío de nuevos turnos sobre ella — sin ofrecer una vía adicional de recuperación del resumen más allá de esa única visualización (FR-021).

## 003/FR-022 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 443. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022**: El resumen de sesión de autoestudio MUST NOT incluir notas, diagnóstico de nivel, personalidad, capacidad, ni recomendaciones académicas automatizadas basadas en inferencias no autorizadas.

## 003/FR-022a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 446. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022a**: Las incidencias incluidas en el resumen de sesión (FR-021) MUST describirse como hechos observables del sistema y su arquitectura (tipo de incidencia, acción de recuperación aplicada) — MUST NOT redactarse como una caracterización de la comprensión, el esfuerzo o la capacidad del estudiante, mismo estándar ya exigido al resumen técnico de la Feature 001 (FR-012b).

## 003/FR-023 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 451. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023**: Un cambio de tema solicitado por el estudiante que quede fuera del alcance autorizado de la actividad MUST ser rechazado o redirigido, aplicando el mismo aislamiento de autorización ya establecido en la Feature 002.

## 003/FR-024 — conservar para uso actual

Familia: N05. Necesidad: imprescindible para decisiones de revisión.

Motivo: Combinar explícitamente grounding y coherencia evita ocultar un rechazo; no exige dos modelos distintos ni duplicar el mismo juicio semántico.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 454. Contexto: ### Functional Requirements.

Requisito leído: - **FR-024**: Cuando el verificador de fundamentación y el verificador de coherencia emitan veredictos distintos sobre la misma propuesta, el sistema MUST combinarlos de forma explícita (por ejemplo, bloqueando si cualquiera de los dos lo exige) en vez de descartar uno de los dos.

## 003/FR-025 — fusionar obligación equivalente

Familia: N06. Necesidad: redundancia transversal.

Motivo: Conservar compatibilidad de contratos, no congelar toda implementación para siempre; absorber la obligación en una política común de cambios y regresión por impacto.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 458. Contexto: ### Functional Requirements.

Requisito leído: - **FR-025**: Esta feature MUST NOT modificar el comportamiento ya validado de la Feature 001 (núcleo cognitivo, contratos de agente, ciclo de sesión/turno, control constitucional, versionado del estado cognitivo) ni de la Feature 002 (materiales, recuperación, fundamentación); únicamente compone sus agentes y contratos existentes en una nueva agencia de autoestudio.

## 003/FR-026 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 463. Contexto: ### Functional Requirements.

Requisito leído: - **FR-026**: Esta feature MUST NOT inferir ni almacenar un perfil de capacidad académica o psicológica del estudiante.

## 003/FR-027 — fusionar obligación equivalente

Familia: N13. Necesidad: mezcla de límites permanentes y fase histórica.

Motivo: No web, notas ni LMS siguen siendo límites; la exclusión de voz era del incremento003, no elimina la voz histórica ni la vuelve obligación del chat actual.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 465. Contexto: ### Functional Requirements.

Requisito leído: - **FR-027**: Esta feature MUST NOT incluir voz, transcripción, un simulacro formal de defensa oral, evaluación, notas, rúbricas, acceso a Internet ni integración con sistemas LMS.

## 003/FR-028 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 468. Contexto: ### Functional Requirements.

Requisito leído: - **FR-028**: Los datos derivados de una sesión de autoestudio (`PracticeQuestion`, `CoherenceIncident`, resumen de sesión) MUST NOT conservarse de forma permanente por defecto una vez cerrada la sesión. Si una actividad autoriza su persistencia más allá del cierre, esa persistencia MUST sujetarse a la misma política de retención y consentimiento ya definida por el sistema (Principio VII; `RetentionPolicy`, Feature 001) y MUST declarar un periodo de retención finito y configurable como parte de esa configuración — esta feature MUST NOT fijar un número de días por defecto no definido ya en la constitución o en los requisitos existentes. Al expirar ese periodo, los datos MUST ser eliminables mediante el mecanismo de purga ya existente (Feature 001).

## 003/FR-028a — decisión pendiente

Familia: N04. Necesidad: migración y política histórica a resolver.

Motivo: La distinción entre autorización y plazo es necesaria; las reglas históricas de null y purga diferida deben conciliarse con eliminación al cierre posterior sin inferir consentimiento o borrar datos heredados por defecto.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 477. Contexto: ### Functional Requirements.

Requisito leído: - **FR-028a** (corregida en la segunda ronda de estabilización, 2026-09-10 — la redacción previa de esta cláusula equiparaba "existe un `RetentionPolicy` con `retention_days` finito" con "hay autorización para conservar", lo cual es incorrecto: un plazo expresa *cuánto* tiempo, nunca *si* está autorizado conservar; esa equivalencia queda retirada): esta feature no distingue hoy un permiso separado de `summary_authorized` (que únicamente autoriza *generar* el resumen efímero, FR-021) para "autorización de conservar datos derivados más allá del cierre" — FR-028 exige esa autorización, pero ningún campo la representa todavía. Se añade `SelfStudyActivityConfig.retention_authorized: bool | null` (nuevo, propio de esta feature, independiente de `summary_authorized` y de `RetentionPolicy`) como la representación explícita de esa autorización — un plazo (`RetentionPolicy. retention_days`) sigue gobernando únicamente *cuánto tiempo*, nunca si conservar. Autorización de conservación efectiva MUST requerir ambas condiciones a la vez: `retention_authorized = true` **y** una `RetentionPolicy` con `retention_days` finito (no nulo) asociada — ninguna de las dos por separado autoriza nada. - **Nueva configuración sin autorización** (`retention_authorized = false`, o sin política finita asociada aunque `retention_authorized = true`): sus datos derivados (`PracticeQuestion`, `CoherenceIncident`, resumen de sesión) MUST tratarse como sin autorización de conservación — elegibles para el mecanismo de purga ya existente desde la primera ejecución posterior al cierre de la sesión (FR-028: "MUST NOT conservarse de forma permanente por defecto"). El cierre de la sesión en sí (FR-020) no cambia — no se borra nada de forma síncrona al cerrar; lo que cambia es que esos datos ya son candidatos para la siguiente invocación manual de la purga (Principio VI: la purga sigue siendo el único mecanismo de eliminación, siempre manual). - **Configuración autorizada con plazo finito válido** (`retention_authorized = true` y `retention_days` finito): sin cambios respecto al mecanismo ya descrito — elegible para purga cuando `Session.ended_at + retention_days < now()`. - **Configuraciones y datos preexistentes** (creados antes de que `retention_authorized` existiera como campo): MUST NOT recibir un valor por defecto deducido — ni `true` (sobre-autorizaría silenciosamente) ni `false` (haría purgables, sin decisión humana, datos que un profesorado pudo asumir conservados). MUST quedar en un estado explícito "sin decidir" (`retention_authorized = null`), excluido tanto del camino de purga inmediata como del camino de purga por plazo, hasta que una persona con permiso lo fije explícitamente a `true` o `false`. Esa decisión MUST identificarse como una acción humana pendiente — **MUST NOT** deducirse de cuántas veces se invoque el mecanismo de purga (ver `research.md` §12 para el mecanismo de diagnóstico, separado de la purga, que expone qué actividades siguen sin decidir).

## 003/SC-001 — aplazar nueva ampliación

Familia: N01. Necesidad: deseable posterior.

Motivo: Los cinco modos son una capacidad histórica legítima, no cinco productos que deban validarse de nuevo antes del chat de dudas y explicación. Mantener interfaces y ampliar después práctica, exposición y repaso.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 546. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: Cada uno de los cinco modos canónicos (`doubt_resolution`, `guided_explanation`, `practice_questions`, `presentation_preparation`, `concept_review`) MUST superar, en las pruebas preparadas para esta feature, al menos un escenario de aceptación específico de su comportamiento canónico (FR-001a) que demuestre una diferencia observable frente a los demás modos en, según corresponda: quién inicia la interacción, el tipo de acción conversacional seleccionada, la política de diálogo aplicada, el uso de generación de preguntas frente a respuesta fundamentada, la progresión de turnos, o el comportamiento de cierre/continuación. La conformidad se comprueba mediante las decisiones estructuradas de la agencia y la traza registrada — nunca mediante comparación literal del texto generado ni exigiendo salidas idénticas o deterministas del mecanismo de generación. 5/5 modos MUST superar su escenario específico y MUST registrar en la traza el modo activo y las decisiones de orquestación utilizadas (qué agentes se activaron y por qué, FR-003). Todos los modos comparten los mismos agentes y el mismo estado de sesión, sin que ninguno requiera una sesión o un estado distintos del núcleo cognitivo.

## 003/SC-002 — conservar para uso actual

Familia: N01. Necesidad: imprescindible.

Motivo: Adaptar explicación, reconocer bloqueo, conservar fuentes y evitar contradicción son necesidades de estudio. Los tests deben medir esos efectos, no solo acciones o etiquetas.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 561. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: El 100% de las respuestas específicas de la asignatura en las pruebas quedan citadas o marcadas explícitamente como no fundamentadas o como conocimiento general permitido.

## 003/SC-003 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: Tres composiciones prueban selección de arquitectura, no utilidad docente; preservar evidencia y no exigir otra cifra de composiciones para declarar usable el chat.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 564. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: El orquestador selecciona al menos tres composiciones distintas de agentes en los escenarios de prueba preparados para esta feature.

## 003/SC-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 566. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El 100% de las salidas prohibidas de las pruebas quedan bloqueadas antes de mostrarse al estudiante.

## 003/SC-005 — sustituir mecanismo

Familia: N11. Necesidad: métrica prescriptiva.

Motivo: Conservar conversación contextual completa; cinco turnos y no reenviar todo el historial son criterios de ensayo iniciales que deben adaptarse al episodio de estudio y al presupuesto real.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 568. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: Un estudiante puede mantener una conversación de prueba de al menos cinco turnos con continuidad de contexto, sin que el sistema reenvíe el historial completo de la conversación en cada turno.

## 003/SC-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Modos autorizados, límites claros, no revelación de datos, no calificación y consentimiento finito son garantías necesarias incluso con capacidad reducida.

Fuente: [specs/003-self-study-agency/spec.md](../../../specs/003-self-study-agency/spec.md), línea 571. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: El 100% de las sesiones de prueba que alcanzan su límite de turnos o duración terminan de forma controlada y generan una traza completa reconstruible.

## 004/FR-001 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 335. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST ofrecer un simulador de defensa oral construido reutilizando los mismos agentes, contratos, estado cognitivo, verificadores y mecanismos de trazabilidad ya utilizados por la agencia de autoestudio (Feature 003) — MUST NOT introducir una arquitectura paralela a `SelfStudyAgency`, ni duplicar un agente cuando el ya existente pueda reutilizarse.

## 004/FR-002 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 340. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: Cada actividad de defensa oral MUST tener una configuración propia, versionada e inmutable una vez utilizada por una sesión, que defina como mínimo: banco de preguntas iniciales autorizadas y/o materiales desde los que generarlas, temas, materiales autorizados, dificultad orientativa, número máximo de turnos, duración máxima, idioma, si la entrada acepta texto y/o voz, si la salida ofrece texto y/o voz, si se permite conocimiento general, la política de conservación de la transcripción, y qué agentes son obligatorios u opcionales.

## 004/FR-002a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 347. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002a**: Una configuración de actividad de defensa oral sin ninguna pregunta inicial autorizada ni materiales desde los que generarla MUST considerarse inválida y MUST rechazarse antes de permitir el inicio de cualquier sesión sobre esa actividad.

## 004/FR-003 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 350. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: La modalidad textual (entrada y salida) MUST estar siempre disponible y MUST cubrir el 100% del flujo de la defensa oral, independientemente de si la voz está habilitada para la actividad.

## 004/FR-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 353. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: El sistema MUST informar al estudiante del propósito de la sesión, sus límites, el tratamiento del audio y la política de conservación antes de aceptar su primera respuesta.

## 004/FR-005 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 356. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST presentar cada pregunta o repregunta por texto y, si la síntesis de voz está activa para la actividad, también mediante voz.

## 004/FR-006 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 358. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST aceptar la respuesta del participante por texto o, cuando la actividad lo permita, mediante captura de voz.

## 004/FR-007 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 360. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: Cuando la respuesta se capture por voz, el sistema MUST transcribirla localmente y MUST mostrar el texto resultante al participante antes de continuar.

## 004/FR-008 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 362. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: La transcripción MUST incluir el texto reconocido, marcas temporales cuando estén disponibles, una confianza estimada, y una señalización visible de los segmentos de baja confianza.

## 004/FR-009 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 365. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El participante MUST poder corregir segmentos de la transcripción antes de que esta se utilice para generar la siguiente repregunta.

## 004/FR-010 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 367. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: Cuando la sesión se conserve, el sistema MUST conservar tanto la transcripción original como su corrección, sin que la corrección sustituya o elimine la original.

## 004/FR-011 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 370. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: El audio capturado MUST ser efímero y MUST descartarse inmediatamente después de procesarse. Esta feature MUST NOT persistirlo, conservarlo, incluirlo en trazas ni crear referencias recuperables a él bajo ninguna configuración. Cualquier recurso temporal usado por el transporte de entrada MUST cerrarse y eliminarse antes de completar la respuesta.

## 004/FR-011a — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 375. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011a**: Si la transcripción de una grabación falla por un error técnico (no por baja confianza), el audio MUST descartarse de inmediato, sin ningún reintento sobre ese mismo audio; el sistema degrada a texto en el mismo turno (ver FR-021, ver Clarifications).

## 004/FR-012 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 379. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST analizar los conceptos mencionados en cada respuesta como observaciones e hipótesis del estado cognitivo de la sesión — MUST NOT tratarlos ni registrarlos como una evaluación o un juicio de calidad de la respuesta.

## 004/FR-013 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 382. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST recuperar materiales relacionados con la respuesta del participante, reutilizando el mecanismo de recuperación documental ya definido en la Feature 002 sin modificar su contrato.

## 004/FR-014 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 385. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: El sistema MUST generar una repregunta que solicite, según corresponda, justificación, un ejemplo, una comparación, una decisión técnica, la explicación de un error, o una profundización sobre la respuesta del participante.

## 004/FR-015 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 388. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: Cada repregunta generada MUST derivarse de la respuesta del participante, el objetivo de la actividad, los conceptos ya tratados, los materiales autorizados y el historial de la sesión actual — MUST evitar preguntas irrelevantes, repetidas literalmente, sin respaldo en materiales o en la respuesta, o que impliquen una calificación encubierta.

## 004/FR-016 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 393. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: Toda repregunta o afirmación generada MUST pasar por verificación de alcance (materiales autorizados de la actividad), coherencia conversacional y conformidad constitucional antes de mostrarse al participante, reutilizando los verificadores ya existentes en las Features 002 y 003 sin modificar sus contratos.

## 004/FR-017 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 397. Contexto: ### Functional Requirements.

Requisito leído: - **FR-017**: Los controles marcados como no omitibles (constitucional y de seguridad) MUST ejecutarse en todos los turnos de una sesión de defensa oral, independientemente de la modalidad de entrada/salida o del resultado de otros agentes.

## 004/FR-018 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 400. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018**: Tras cada respuesta, el sistema MUST decidir si profundiza en el mismo tema, cambia a un tema distinto, pide aclaración o finaliza la sesión, y esa decisión MUST quedar registrada de forma trazable.

## 004/FR-018a — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 403. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018a**: Profundizar en el mismo tema y cambiar a un tema distinto MUST expresarse ambos mediante la misma acción de diálogo ya existente (presentar una nueva pregunta/repregunta) — esta feature MUST NOT introducir una acción de diálogo nueva y distinta para "cambiar de tema"; la diferencia entre ambos MUST seguir siendo observable en la traza a través de los conceptos y materiales referenciados por la repregunta (ver Clarifications).

## 004/FR-018b — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 409. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018b**: La agencia de defensa MUST seleccionar la acción de aclaración (`clarify`) cuando la respuesta textual definitiva del participante (ya confirmada, tras cualquier corrección de transcripción cuando proceda) no proporcione información suficiente o inequívoca para decidir con seguridad el siguiente paso del diálogo — por ejemplo, cuando no pueda relacionarse razonablemente con la pregunta o los conceptos autorizados relevantes, cuando admita varias interpretaciones plausibles que conducirían a continuaciones distintas, o cuando contenga una aparente incompatibilidad interna sobre la que sea necesario conocer qué interpretación pretendía expresar el participante. Esta decisión MUST tomarse exclusivamente sobre la respuesta textual ya definitiva — MUST NOT confundirse ni compartir mecanismo con la solicitud de confirmación/corrección por baja confianza de transcripción (FR-022), que es una incidencia de modalidad previa a cualquier procesamiento cognitivo. Al seleccionar `clarify`, el sistema MUST solicitar únicamente la información mínima necesaria para desambiguar, MUST NOT evaluar ni corregir académicamente al participante, MUST NOT interpretar la necesidad de aclaración como un error o una señal de bajo rendimiento, MUST registrar la decisión y su motivo estructurado de forma trazable, y tras recibir la aclaración MUST volver a decidir la acción de diálogo correspondiente con la información ya desambiguada.

## 004/FR-019 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 427. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019**: El ciclo de pregunta/repregunta MUST repetirse hasta alcanzar el límite configurado de turnos o duración, o hasta la finalización voluntaria del participante.

## 004/FR-020 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 429. Contexto: ### Functional Requirements.

Requisito leído: - **FR-020**: El participante MUST poder revisar la transcripción completa de la sesión antes de su cierre.

## 004/FR-021 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 431. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021**: Si la captura de audio o la transcripción fallan, o los recursos locales no son suficientes, el sistema MUST ofrecer continuar por texto sin perder el estado ya alcanzado en la sesión, siguiendo el mismo mecanismo de degradación controlada ya establecido en la Feature 001.

## 004/FR-022 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 435. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022**: Si la respuesta transcrita está incompleta o tiene baja confianza en un término crítico, el sistema MUST solicitar confirmación o aclaración al participante antes de generar una repregunta basada en esa interpretación. Esta solicitud de aclaración MUST ofrecer corregir el texto de los segmentos señalados y, si el participante lo prefiere, continuar respondiendo por texto desde ese punto — MUST NOT ofrecer repetir la grabación de audio (ver Clarifications). Esta solicitud es una incidencia de modalidad, previa a cualquier procesamiento cognitivo de la respuesta, y MUST distinguirse por completo de la acción de diálogo de aclaración cognitiva sobre una respuesta ya definitiva (ver FR-018b).

## 004/FR-022a — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 444. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022a**: Una respuesta capturada directamente como texto (sin transcripción de por medio) MUST NOT disparar por sí sola, solo por ser breve o poco desarrollada, la solicitud de aclaración de FR-022 — se trata como una respuesta válida sobre la que generar una repregunta normal (ver Clarifications).

## 004/FR-023 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 448. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023**: Cuando la síntesis de voz esté activa, MUST reproducir exactamente el contenido textual ya verificado — MUST NOT resumirlo, ampliarlo, suavizarlo ni modificarlo de ninguna forma.

## 004/FR-024 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 451. Contexto: ### Functional Requirements.

Requisito leído: - **FR-024**: Si la síntesis de voz falla, la respuesta en texto MUST seguir disponible y el turno MUST NOT interrumpirse por ese fallo.

## 004/FR-025 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 453. Contexto: ### Functional Requirements.

Requisito leído: - **FR-025**: El sistema MUST NOT producir ni mostrar, en ningún momento de la sesión, una nota, calificación, clasificación de desempeño, o una afirmación de que el participante ha aprobado o suspendido.

## 004/FR-026 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 456. Contexto: ### Functional Requirements.

Requisito leído: - **FR-026**: Toda propuesta generada que contenga contenido evaluativo (nota, clasificación de desempeño, afirmación de aprobado/suspenso) MUST ser bloqueada por el control constitucional antes de mostrarse y su causa MUST quedar registrada sin revelar el contenido prohibido. El sistema MAY intentar como máximo una respuesta operativa segura predefinida, que solo podrá mostrarse si supera una verificación final independiente. Si tampoco se autoriza, MUST finalizar de forma segura sin presentar contenido.

## 004/FR-027 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 463. Contexto: ### Functional Requirements.

Requisito leído: - **FR-027**: Esta feature MUST NOT inferir ni almacenar un perfil de capacidad, nivel o desempeño del participante a partir de sus respuestas, correcciones de transcripción, o historial de la sesión. Esta prohibición incluye usar como señales académicas la duración, confianza STT, número de aclaraciones/repreguntas o incidencias técnicas; esos datos solo pueden describir hechos operativos de la sesión.

## 004/FR-028 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 468. Contexto: ### Functional Requirements.

Requisito leído: - **FR-028**: Al alcanzarse el límite de turnos o duración, o ante una finalización voluntaria, el sistema MUST avisar al participante y MUST permitir un cierre ordenado.

## 004/FR-029 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 471. Contexto: ### Functional Requirements.

Requisito leído: - **FR-029**: Al cerrar la sesión, el sistema MUST generar un resumen descriptivo, limitado exclusivamente a hechos observables y datos estructurados registrados durante la propia sesión — puede incluir preguntas formuladas, repreguntas, aclaraciones solicitadas, temas/conceptos tratados, materiales o fuentes consultados, incidencias técnicas, duración, número de turnos, y causa de cierre. El resumen MUST NOT incluir notas, calificaciones, puntuaciones, diagnóstico de nivel, personalidad, capacidad, rendimiento, competencia, dominio, ni recomendaciones académicas automatizadas, y MUST NOT introducir ninguna inferencia nueva sobre el participante más allá de esos hechos ya registrados durante la sesión. El resumen MUST ser reproducible mediante construcción determinista a partir de los datos estructurados de la sesión ya disponibles y MUST NOT invocar un generador de texto libre.

## 004/FR-029a — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 482. Contexto: ### Functional Requirements.

Requisito leído: - **FR-029a**: Las incidencias, aclaraciones y repreguntas incluidas en el resumen de cierre MUST describirse como hechos observables del sistema y su desarrollo (tipo de incidencia o aclaración, acción de recuperación aplicada, tema o concepto al que se refiere la repregunta) — MUST NOT redactarse ni interpretarse como una caracterización de la comprensión, el esfuerzo, el rendimiento o la capacidad del participante, mismo estándar ya exigido en la Feature 003.

## 004/FR-030 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 488. Contexto: ### Functional Requirements.

Requisito leído: - **FR-030**: Al cierre, el participante MUST poder decidir si conserva o elimina los datos de la sesión conforme a la política de conservación configurada por la actividad; el sistema MUST ejecutar esa decisión y MUST registrar únicamente lo explícitamente permitido. La persistencia operativa durante una sesión MUST NOT interpretarse como consentimiento de conservación ni la decisión de conservación como condición para participar o completar la defensa. Cuando la actividad autoriza conservar, el participante puede elegir de forma independiente transcripción y resumen; el audio nunca forma parte de esa elección.

## 004/FR-031 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 496. Contexto: ### Functional Requirements.

Requisito leído: - **FR-031**: La conservación de transcripción, corrección o resumen más allá del cierre MUST sujetarse a la misma política de retención y consentimiento ya definida por el sistema (`RetentionPolicy`, Feature 001), con un periodo de retención finito y configurable como parte de esa configuración — esta feature MUST NOT introducir un sistema de retención paralelo ni fijar un número de días por defecto no definido ya en la constitución o en los requisitos existentes. La eliminación elegida o exigida por falta de autorización MUST aplicarse en el cierre; la purga diferida MUST limitarse a datos expirados propios de esta feature y MUST NOT afectar las Features 001–003.

## 004/FR-032 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 504. Contexto: ### Functional Requirements.

Requisito leído: - **FR-032**: El sistema MUST NOT agregar, correlacionar ni construir un perfil a partir de información de defensa oral (respuestas, transcripciones, repreguntas, incidencias, resúmenes) entre distintas sesiones del mismo `participant_code` — toda esa información MUST permanecer acotada a la sesión que la generó, mismo principio ya aplicado en la Feature 003.

## 004/FR-033 — fusionar obligación equivalente

Familia: N06. Necesidad: redundancia transversal.

Motivo: Compatibilidad y ausencia de duplicación arquitectónica son criterios transversales; conservarlos con revisión por impacto, no como prohibición absoluta de corregir componentes previos.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 509. Contexto: ### Functional Requirements.

Requisito leído: - **FR-033**: Esta feature MUST preservar el comportamiento ya validado de las Features 001 (núcleo cognitivo, contratos de agente, ciclo de sesión/turno, control constitucional, versionado del estado cognitivo), 002 (materiales, recuperación, fundamentación) ni 003 (agencia de autoestudio, generación, verificadores de coherencia y no-revelación). MUST integrar sus contratos públicos estables y MAY realizar extensiones aditivas necesarias para registrar la nueva agencia, rutas, propósitos, plantillas y clientes, siempre que las pruebas de regresión demuestren que no se debilita ningún comportamiento anterior.

## 004/FR-034 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 517. Contexto: ### Functional Requirements.

Requisito leído: - **FR-034**: Esta feature MUST NOT incluir análisis de prosodia, emociones o lenguaje corporal, evaluación automática de la calidad de la defensa, detección de fraude, robot o avatar físico, videoconferencia, ni memoria longitudinal entre sesiones.

## 004/FR-035 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 520. Contexto: ### Functional Requirements.

Requisito leído: - **FR-035**: La interfaz esencial de la sesión MUST ser operable mediante teclado, MUST permitir pausar la sesión, repetir la pregunta actual, ajustar el ritmo, y MUST mostrar mensajes de error comprensibles — sin depender del audio, del color, ni de gestos no accesibles.

## 004/FR-036 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 524. Contexto: ### Functional Requirements.

Requisito leído: - **FR-036**: Esta feature MUST NOT requerir un servicio en la nube para su funcionamiento esencial — la transcripción local y la síntesis de voz, cuando se utilicen, MUST ejecutarse localmente, consistente con la ejecución local ya exigida en la Feature 001.

## 004/FR-037 — sustituir mecanismo

Familia: N13. Necesidad: mecanismo histórico de otra experiencia.

Motivo: En defensa futura conservar recuperación ante fallo; una pregunta autorizada puede ser válida allí, pero no imponer respuestas académicas prefabricadas como fallback del tutor generativo actual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 528. Contexto: ### Functional Requirements.

Requisito leído: - **FR-037**: Si el mecanismo de generación de la pregunta inicial o de una repregunta falla o no está disponible, ese fallo MUST NOT provocar por sí solo la pérdida de la sesión. El sistema MUST intentar las alternativas de generación autorizadas por la configuración de la actividad; cuando exista una pregunta autorizada/preconfigurada o una alternativa determinista válida, MUST poder utilizarla. Si, tras agotar esas alternativas, no puede obtenerse una pregunta, repregunta o salida válida, el sistema MUST seleccionar una acción segura que no invente contenido — reconocer la imposibilidad de continuar sobre el tema actual, solicitar aclaración cuando proceda, pasar mediante la acción `ask` a otro tema autorizado, o finalizar la sesión de forma controlada — MUST NOT fabricar una repregunta sin evidencia o contexto suficiente únicamente para mantener la conversación. El fallo detectado y la acción de recuperación seleccionada MUST quedar registrados de forma trazable. Este requisito cubre tanto la pregunta inicial como las repreguntas, reutilizando el mismo mecanismo de degradación controlada ya establecido en la Feature 001 y aplicado en la Feature 003, sin introducir un mecanismo de reserva adicional.

## 004/FR-038 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 543. Contexto: ### Functional Requirements.

Requisito leído: - **FR-038**: Antes de persistir o presentar cualquier texto generado por esta feature, el sistema MUST autorizar el candidato final mediante la puerta estructurada ya establecida en la Feature 001. La autorización MUST usar una instantánea mínima, confiable y filtrada de la política aplicable, la identidad exacta de una plantilla o mensaje operativo catalogado y una vinculación verificable que cubra el contenido completo. Esta regla MUST aplicarse a la ruta normal y a todas las rutas de degradación, aclaración, falta de evidencia y cierre.

## 004/FR-039 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 550. Contexto: ### Functional Requirements.

Requisito leído: - **FR-039**: Cuando la autorización final bloquea un candidato, el sistema MUST persistir el turno como bloqueado con `output_text` ausente, MUST NOT transportar ni publicar el candidato y MUST NOT sintetizarlo. Solo se permite el intento operativo único descrito en FR-026; si ese intento se bloquea, la sesión MUST cerrarse en estado seguro y sin una tercera salida.

## 004/FR-040 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 555. Contexto: ### Functional Requirements.

Requisito leído: - **FR-040**: La síntesis de voz MUST ejecutarse únicamente sobre el texto final aprobado y ya persistido del turno. La reproducción y su repetición MUST obtener audio bajo demanda para esa misma identidad de turno y texto; el sistema MUST NOT persistir los bytes de audio ni sintetizar propuestas previas, bloqueadas o con texto ausente.

## 004/FR-041 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 559. Contexto: ### Functional Requirements.

Requisito leído: - **FR-041**: Todo cierre de defensa MUST usar la transición atómica de cierre ya establecida por la Feature 001. Solo la ejecución que gana esa transición MUST generar y entregar el resumen, registrar consentimiento, aplicar conservación o eliminación, emitir eventos de cierre y liberar recursos. Las ejecuciones concurrentes o repetidas MUST devolver el estado persistido sin repetir esos efectos.

## 004/FR-042 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 564. Contexto: ### Functional Requirements.

Requisito leído: - **FR-042**: La transcripción y la síntesis locales MUST ejecutarse con capacidad global explícitamente acotada, admisión con backpressure, plazo y cancelación. Un trabajo que termina después de cancelarse o expirar MUST descartarse y MUST NOT escribir datos, trazas ni respuestas tardías.

## 004/FR-043 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 568. Contexto: ### Functional Requirements.

Requisito leído: - **FR-043**: Cada audio de entrada MUST rechazarse antes de transcribir si supera 10 MiB y MUST rechazarse tras inspección si supera 300 segundos, si su duración no puede determinarse o si su formato no es admitido. La recepción MUST contabilizar bytes de forma acotada y garantizar el cierre y eliminación de cualquier recurso temporal del transporte multipart tanto en éxito como en error, timeout o cancelación.

## 004/FR-044 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 573. Contexto: ### Functional Requirements.

Requisito leído: - **FR-044**: La interfaz MUST distinguir de forma observable una salida textual aprobada de un turno bloqueado sin texto. Solo el primer caso MAY ofrecer reproducción de voz; un fallo de síntesis MUST dejar disponible el texto aprobado y permitir un nuevo intento explícito de reproducción sin repetir el turno cognitivo.

## 004/SC-001 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 618. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: El mismo núcleo cognitivo y el mismo conjunto mínimo de agentes básicos soportan autoestudio (Feature 003) y defensa oral en las pruebas preparadas para esta feature, sin que se detecte una arquitectura o una implementación de agentes duplicada — verificado mediante las decisiones estructuradas de la agencia y la traza registrada, nunca mediante comparación literal de texto generado.

## 004/SC-002 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 623. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: El 100% del flujo esencial (pregunta, respuesta, repregunta, revisión de transcripción, cierre y resumen) es completable únicamente por texto en el conjunto de pruebas preparado para esta feature.

## 004/SC-003 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 626. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: El 100% de las correcciones de transcripción en las pruebas quedan conservadas junto con la versión original, y la repregunta generada tras una corrección se basa verificablemente en la versión corregida.

## 004/SC-004 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 629. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El 100% de los fallos de captura o transcripción de voz simulados en las pruebas degradan la sesión a modalidad textual sin pérdida del estado ya alcanzado.

## 004/SC-005 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 631. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: El 100% de las repreguntas generadas en el conjunto de pruebas referencian de forma trazable la respuesta del participante, un concepto ya tratado o un material autorizado — ninguna repregunta de prueba resulta genérica, desconectada, o repetida literalmente dentro de la misma sesión.

## 004/SC-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 635. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: El 100% de las propuestas de prueba que contienen contenido evaluativo (nota, clasificación de desempeño, afirmación de aprobado/suspenso) quedan bloqueadas antes de mostrarse al estudiante.

## 004/SC-007 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 638. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-007**: El 100% de las sesiones de prueba que alcanzan su límite de turnos o duración, o que finalizan voluntariamente, terminan de forma controlada, generan un resumen descriptivo, y producen una traza completa reconstruible.

## 004/SC-008 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 641. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-008**: En la matriz de salidas visibles, el 100% de los candidatos aprobados conserva propuesta y verificación vinculadas, y el 100% de los bloqueados persiste `output_text` ausente sin filtrar el candidato por API, transporte, traza o TTS.

## 004/SC-009 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso condicional a ruta existente.

Motivo: La posposición de voz no suspende modalidad textual, permisos, no calificación, descarte de audio, consentimiento ni cierre único en rutas ya disponibles; conservar esas garantías sin nuevo desarrollo de voz.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 644. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-009**: Las pruebas de concurrencia de cierre demuestran un único ganador y una única ejecución de resumen, consentimiento, retención/eliminación, evento de cierre y liberación de recursos.

## 004/SC-010 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 647. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-010**: Las pruebas de audio fuerzan límites de bytes, duración, timeout, cancelación y rollover multipart, y verifican que no queda ningún archivo temporal ni escritura tardía después de responder.

## 004/SC-011 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro para el objetivo vigente.

Motivo: Defensa y voz son horizonte histórico pospuesto para el chat actual. Mantener compatibilidad y todas las salvaguardas de una ruta existente; no ampliar STT/TTS, bancos o ensayos de esa capacidad para resolver primero el tutor textual.

Fuente: [specs/004-oral-defense-agency/spec.md](../../../specs/004-oral-defense-agency/spec.md), línea 650. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-011**: Para un mismo texto definitivo y la misma configuración, las pruebas por entrada textual y por voz confirmada producen la misma estructura de acción de diálogo y conceptos referenciados, con independencia de la modalidad de origen.

## 005/FR-001 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 122. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001** (US1): El sistema MUST cumplir: El docente puede crear, duplicar y versionar configuraciones; cada sucesor recibe identidad propia y conserva familia y procedencia, incluso si la versión anterior ya fue utilizada.

## 005/FR-002 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 123. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002** (US1): El sistema MUST cumplir: Las sesiones referencian una configuración inmutable. Cambiar objetivo, límites, idioma, modos, preguntas, temas, conocimiento general, modelos, agentes o política genera una nueva versión sin alterar sesiones anteriores.

## 005/FR-003 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 124. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003** (US1): El sistema MUST cumplir: El docente puede activar y retirar versiones; solo una versión por familia está activa para nuevos usos y una retirada no inicia nuevas sesiones ni elimina evidencia histórica.

## 005/FR-004 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 125. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004** (US1): El sistema MUST cumplir: La selección de materiales identifica versiones autorizadas y valida asignatura, actividad, estado activo y vigencia. Una versión retirada no aparece en nuevas recuperaciones.

## 005/FR-005 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 126. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005** (US1): El sistema MUST cumplir: El docente selecciona únicamente modelos y composiciones de agentes disponibles y compatibles; los controles constitucionales y de privacidad son obligatorios y los contratos no pueden editarse desde una actividad.

## 005/FR-006 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 127. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006** (US1): El sistema MUST cumplir: El docente puede consultar estados técnicos de documentos, extracción e índice, sus errores y versiones sin ejecutar su contenido.

## 005/FR-007 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 128. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007** (US2): El sistema MUST cumplir: El acceso docente requiere una credencial administrativa local configurada y una sesión de duración limitada; ausencia, invalidez, caducidad y cierre de sesión deniegan acceso.

## 005/FR-008 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 129. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008** (US2): El sistema MUST cumplir: El participante solo puede acceder y modificar la sesión que ha iniciado mediante una autorización secreta de sesión. Conocer códigos seudónimos o identificadores de otra sesión no concede acceso.

## 005/FR-009 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 130. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009** (US2): El sistema MUST cumplir: La autorización abarca todas las rutas históricas y nuevas de contenido, trazas, materiales administrativos, configuración, exportación, corrección, cierre y eliminación; no quedan rutas alternativas sin protección.

## 005/FR-010 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 131. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010** (US2): El sistema MUST cumplir: Los intentos denegados se registran solo con tipo, resultado e instante, sin credenciales, contenido, parámetros sensibles ni identificadores personales.

## 005/FR-011 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 132. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011** (US2): El sistema MUST cumplir: La aplicación escucha solo en el anfitrión por defecto; habilitar una red local requiere una configuración administrativa explícita. Las peticiones de otros orígenes no pueden ejecutar acciones autenticadas.

## 005/FR-012 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 133. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012** (US3): El sistema MUST cumplir: El participante conoce finalidad, datos operativos, datos conservados, plazo y quién accede antes de participar. Rechazar conservación no impide completar la sesión efímera.

## 005/FR-013 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 134. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013** (US3): El sistema MUST cumplir: La conservación posterior exige autorización de actividad, consentimiento explícito y plazo finito no negativo. Transcripción y resumen se eligen independientemente; audio nunca se conserva.

## 005/FR-014 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 135. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014** (US3): El sistema MUST cumplir: Los cierres voluntarios, automáticos y seguros aplican la elección actual una sola vez mediante el cierre ganador. Sin consentimiento se eliminan las copias de contenido operativo y solo quedan metadatos técnicos mínimos justificados.

## 005/FR-015 — aplazar nueva ampliación

Familia: N13. Necesidad: futuro condicionado a voz.

Motivo: La corrección de transcripción es necesaria cuando se use voz; conservarla en compatibilidad y no ampliar esa modalidad ahora.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 136. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015** (US3): El sistema MUST cumplir: Las transcripciones de voz son revisables y corregibles por su participante; conservar incluye original y revisiones diferenciadas, sin reescribir la salida ya entregada.

## 005/FR-016 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 137. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016** (US3): El sistema MUST cumplir: La política de retención queda versionada e inmutable con la configuración usada; no se acepta conservación indefinida ni se introduce un plazo implícito.

## 005/FR-017 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 138. Contexto: ### Functional Requirements.

Requisito leído: - **FR-017** (US4): El sistema MUST cumplir: La revisión docente lista y abre únicamente sesiones cerradas, consentidas, no eliminadas y no expiradas. Una sesión no autorizada devuelve denegación sin contenido.

## 005/FR-018 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 139. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018** (US4): El sistema MUST cumplir: La revisión distingue entradas, originales y correcciones, respuestas aprobadas, fuentes con versión/ubicación, agentes, verificaciones, bloqueos, incidencias y resumen, filtrando cada campo según su scope consentido.

## 005/FR-019 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 140. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019** (US4): El sistema MUST cumplir: Los registros técnicos mínimos no permiten reconstruir texto eliminado ni perfiles longitudinales. No se exponen prompts internos completos, razonamiento privado, candidatos bloqueados ni secretos.

## 005/FR-020 — aplazar nueva ampliación

Familia: N08. Necesidad: deseable de alto valor posterior.

Motivo: Exportación abierta y revisión de texto libre son útiles para análisis consentido posterior. Conservar funcionalidad y filtros existentes, sin priorizar lotes y paneles sobre una conversación útil.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 141. Contexto: ### Functional Requirements.

Requisito leído: - **FR-020** (US5): El sistema MUST cumplir: El docente puede exportar una o varias sesiones autorizadas a un formato abierto estructurado y otro legible, incluyendo configuración/versiones, contenido permitido, resumen, fuentes y trazabilidad saneada.

## 005/FR-021 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 142. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021** (US5): El sistema MUST cumplir: Cada exportación revalida autorización, consentimiento, scopes, caducidad y eliminación en el momento de construirla; una selección que contenga una sesión no autorizada falla sin exportación parcial.

## 005/FR-022 — aplazar nueva ampliación

Familia: N08. Necesidad: deseable de alto valor posterior.

Motivo: Exportación abierta y revisión de texto libre son útiles para análisis consentido posterior. Conservar funcionalidad y filtros existentes, sin priorizar lotes y paneles sobre una conversación útil.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 143. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022** (US5): El sistema MUST cumplir: Las exportaciones para análisis sustituyen códigos e identidades de sesión por alias del lote y omiten identificadores directos. Texto libre requiere revisión explícita por posible información personal antes de descargarlo; no se afirma anonimización automática.

## 005/FR-023 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 144. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023** (US5): El sistema MUST cumplir: La exportación usa proyecciones de campos permitidos, excluye siempre audio, credenciales, secretos, razonamiento privado y datos fuera del consentimiento; no crea archivos persistentes en el servidor.

## 005/FR-024 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 145. Contexto: ### Functional Requirements.

Requisito leído: - **FR-024** (US6): El sistema MUST cumplir: Docente o participante propietario pueden eliminar el contenido de una sesión cerrada; una sesión activa requiere finalizar primero y no puede borrarse por accidente mientras procesa un turno.

## 005/FR-025 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 146. Contexto: ### Functional Requirements.

Requisito leído: - **FR-025** (US6): El sistema MUST cumplir: La eliminación retira contenido y copias en turnos, transcripciones, correcciones, estado, mensajes, propuestas y trazas; conserva solo un recibo técnico mínimo sin contenido y excluye la sesión de revisión y exportación posteriores.

## 005/FR-026 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 147. Contexto: ### Functional Requirements.

Requisito leído: - **FR-026** (US6): El sistema MUST cumplir: La eliminación repetida es idempotente y la purga de expirados es manual, comprobable y limitada a las sesiones alcanzadas; sesiones vigentes y materiales docentes no se eliminan.

## 005/FR-027 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 148. Contexto: ### Functional Requirements.

Requisito leído: - **FR-027** (US6): El sistema MUST cumplir: Un fallo o rollback no comunica una eliminación o exportación exitosa; los efectos de contenido, recibo y consentimiento se confirman de forma coherente.

## 005/FR-028 — aplazar nueva ampliación

Familia: N08. Necesidad: deseable posterior.

Motivo: Las métricas agregadas ayudan a operación e investigación; ampliar el panel no desbloquea la comprensión del alumno. Conservar métricas esenciales y límites contra rankings.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 149. Contexto: ### Functional Requirements.

Requisito leído: - **FR-028** (US7): El sistema MUST cumplir: El panel muestra métricas agregadas del sistema —sesiones, turnos, cierres, bloqueos, incidencias y latencias disponibles— sin desglose individual, notas, rankings ni inferencia académica; métricas ausentes se marcan como faltantes.

## 005/FR-029 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 150. Contexto: ### Functional Requirements.

Requisito leído: - **FR-029** (US7): El sistema MUST cumplir: La interfaz docente y las funciones de privacidad del participante son operables por texto y teclado, con etiquetas, estados de carga, confirmación de acciones destructivas y errores comprensibles.

## 005/FR-030 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 151. Contexto: ### Functional Requirements.

Requisito leído: - **FR-030** (US7): El sistema MUST cumplir: Las extensiones preservan T090, T150, recuperación autorizada y contratos públicos de Features 001–004. Los cambios de autorización históricos se documentan y prueban con credenciales explícitas, sin un bypass de producción para pruebas.

## 005/FR-031 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 152. Contexto: ### Functional Requirements.

Requisito leído: - **FR-031** (US7): El sistema MUST cumplir: El sistema no almacena una relación entre identidad real y código; no incluye SSO, nube, correo, expedientes, biometría, notas ni perfiles de estudiantes.

## 005/FR-032 — fusionar obligación equivalente

Familia: N12. Necesidad: redundancia transversal consolidable.

Motivo: Migraciones, instalación y evidencia segura se mantienen como una obligación de entrega común, evitando documentos y paquetes duplicados por cada incremento.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 153. Contexto: ### Functional Requirements.

Requisito leído: - **FR-032** (US7): El sistema MUST cumplir: La entrega incluye datos ficticios, migraciones limpia y de actualización, instalación local, ejemplos ejecutados, pruebas de autorización/consentimiento/borrado/exportación y evidencia de límites.

## 005/SC-001 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 168. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: En las pruebas de versionado, el 100% de las sesiones antiguas conserva configuración y política originales tras crear y activar un sucesor.

## 005/SC-002 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 169. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: El 100% de intentos preparados de rol no autorizado o sesión ajena se deniega sin datos sensibles.

## 005/SC-003 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 170. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: Todas las combinaciones de consentimiento y scopes preparadas completan la sesión y conservan exactamente lo permitido; la negativa no impide el flujo.

## 005/SC-004 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 171. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El 100% de revisiones y lotes de exportación excluye sesiones no consentidas, expiradas o eliminadas y campos no autorizados.

## 005/SC-005 — aplazar nueva ampliación

Familia: N08. Necesidad: deseable de alto valor posterior.

Motivo: Exportación abierta y revisión de texto libre son útiles para análisis consentido posterior. Conservar funcionalidad y filtros existentes, sin priorizar lotes y paneles sobre una conversación útil.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 172. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: Las exportaciones estructurada y legible son utilizables sin servicios externos y no contienen ninguno de los secretos, audio o razonamiento privado sembrados en pruebas.

## 005/SC-006 — conservar por seguridad

Familia: N04. Necesidad: seguridad y permiso.

Motivo: Acceso, consentimiento, scopes, expiración, borrado verificable y ausencia de datos personales innecesarios son obligaciones de permiso y confianza, no candidatos a suprimir por simplificación.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 173. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: Todas las eliminaciones y purgas de prueba son verificables, idempotentes y aíslan sesiones vigentes y materiales.

## 005/SC-007 — conservar para uso actual

Familia: N08. Necesidad: imprescindible.

Motivo: Preparar y activar una actividad, conocer cobertura y actualizar versiones sin cambiar el pasado es necesario para docente y participante; mantener el recorrido por teclado.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 174. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-007**: Un docente completa por teclado el recorrido de configuración, revisión, exportación y eliminación; el participante revisa/corrige y decide privacidad por texto.

## 005/SC-008 — aplazar nueva ampliación

Familia: N08. Necesidad: deseable posterior.

Motivo: Las métricas agregadas ayudan a operación e investigación; ampliar el panel no desbloquea la comprensión del alumno. Conservar métricas esenciales y límites contra rankings.

Fuente: [specs/005-teacher-governance/spec.md](../../../specs/005-teacher-governance/spec.md), línea 175. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-008**: Las métricas agregadas describen funcionamiento, faltantes y limitaciones sin notas, rankings ni inferencias académicas.

## 006/FR-001 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: La comparación arquitectónica y los conteos de composiciones son investigación legítima separada del listo del chat; no repetir el catálogo sintético completo como evidencia de utilidad generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 161. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST ejecutar el mismo catálogo sintético con baseline directo y agencia completa, registrando condiciones comunes y diferencias.

## 006/FR-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad de experimentación.

Motivo: Conservar aislamiento de ablaciones, no exponer fallos inseguros a usuarios y no importar datos privados; esas condiciones siguen vigentes aunque el estudio se aplace.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 163. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: El sistema MUST permitir ablaciones de fundamentación y coherencia únicamente en un proceso experimental aislado con datos sintéticos y autorización de protocolo; nunca entregar sus resultados a participantes.

## 006/FR-003 — conservar por seguridad

Familia: N05. Necesidad: seguridad de experimentación.

Motivo: Conservar aislamiento de ablaciones, no exponer fallos inseguros a usuarios y no importar datos privados; esas condiciones siguen vigentes aunque el estudio se aplace.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 165. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: El sistema MUST mantener controles constitucionales y de privacidad; no añadir rutas de producción que omitan verificadores.

## 006/FR-004 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: La comparación arquitectónica y los conteos de composiciones son investigación legítima separada del listo del chat; no repetir el catálogo sintético completo como evidencia de utilidad generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 167. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: El sistema MUST comparar estrategias de recuperación y composiciones de agentes existentes con parámetros registrados y evidencia etiquetada.

## 006/FR-005 — sustituir mecanismo

Familia: N11. Necesidad: método experimental proporcionable.

Motivo: Conservar cobertura de fallos y recuperación, pero elegir escenarios y capas afectados según riesgo; voz no disponible no exige una nueva campaña STT para cada ajuste textual.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 169. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST incluir los quince escenarios del catálogo fuente: evidencia clara/ausente/conflictiva, fuera de alcance, afirmación sin respaldo, contradicción, repetición, timeout, modelo/índice/STT no disponibles, conflicto de estado, límites, eliminación y nota académica.

## 006/FR-006 — sustituir mecanismo

Familia: N11. Necesidad: método experimental proporcionable.

Motivo: Conservar cobertura de fallos y recuperación, pero elegir escenarios y capas afectados según riesgo; voz no disponible no exige una nueva campaña STT para cada ajuste textual.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 171. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST inyectar fallos en las interfaces reales de agente/modelo/índice/STT/recursos y observar recuperación o terminación segura, sin contaminar el estado interactivo.

## 006/FR-007 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: La comparación arquitectónica y los conteos de composiciones son investigación legítima separada del listo del chat; no repetir el catálogo sintético completo como evidencia de utilidad generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 173. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: El sistema MUST calcular agentes por turno/sesión, composiciones, bloqueos/reformulaciones, salidas sin fuentes, precisión/cobertura etiquetadas, conflictos y fallos de coordinación.

## 006/FR-008 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para declarar listo.

Motivo: Latencia, recursos, utilidad percibida, carga docente y límites honestos son necesarios para valorar coste y resultado; faltantes no se presentan como cero ni satisfacción como aprendizaje.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 175. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: El sistema MUST medir latencia total y por agente, CPU, memoria, GPU y contexto; informar unidades, alcance del muestreo y faltantes con motivo, sin fabricar ceros.

## 006/FR-009 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: La comparación arquitectónica y los conteos de composiciones son investigación legítima separada del listo del chat; no repetir el catálogo sintético completo como evidencia de utilidad generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 177. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El sistema MUST calcular timeouts, recuperaciones, porcentaje de turnos trazables, reconstrucción, reutilización entre agencias y efectos de corrección de transcripción.

## 006/FR-010 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para declarar listo.

Motivo: Latencia, recursos, utilidad percibida, carga docente y límites honestos son necesarios para valorar coste y resultado; faltantes no se presentan como cero ni satisfacción como aprendizaje.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 179. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: El sistema MUST registrar completadas/abandonos/duración/revisabilidad y observaciones voluntarias de utilidad/facilidad/preguntas/preparación/tiempo docente; distinguir observaciones humanas ausentes de ejecución sintética.

## 006/FR-011 — sustituir mecanismo

Familia: N12. Necesidad: necesario con mecanismo consolidable.

Motivo: Conservar identidad y reproducción del experimento; manifiestos y objetos compartidos pueden reemplazar snapshots repetidos, sin reeditar originales o exigir identidad textual generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 181. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: El sistema MUST fijar código, configuración, modelo/parámetros, índice/documentos, escenario, semilla, componentes/orden, límites y hardware para cada ejecución.

## 006/FR-012 — sustituir mecanismo

Familia: N12. Necesidad: necesario con mecanismo consolidable.

Motivo: Conservar identidad y reproducción del experimento; manifiestos y objetos compartidos pueden reemplazar snapshots repetidos, sin reeditar originales o exigir identidad textual generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 183. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST generar resultados estructurados y resumen legible por escenario/configuración y comparación baseline/agencia, con conteos y variabilidad.

## 006/FR-013 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para declarar listo.

Motivo: Latencia, recursos, utilidad percibida, carga docente y límites honestos son necesarios para valorar coste y resultado; faltantes no se presentan como cero ni satisfacción como aprendizaje.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 185. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST distinguir métricas, observaciones, inferencias y limitaciones; declarar muestras pequeñas, condiciones no comparables y resultados negativos sin afirmar superioridad injustificada.

## 006/FR-014 — sustituir mecanismo

Familia: N12. Necesidad: necesario con mecanismo consolidable.

Motivo: Conservar identidad y reproducción del experimento; manifiestos y objetos compartidos pueden reemplazar snapshots repetidos, sin reeditar originales o exigir identidad textual generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 187. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: El sistema MUST reproducir paquetes comprobando integridad de entradas/código y secuencias/decisiones estructurales; excluir tiempo/identificadores aleatorios de la igualdad.

## 006/FR-015 — conservar por seguridad

Familia: N05. Necesidad: seguridad de experimentación.

Motivo: Conservar aislamiento de ablaciones, no exponer fallos inseguros a usuarios y no importar datos privados; esas condiciones siguen vigentes aunque el estudio se aplace.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 189. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: El sistema MUST operar localmente por texto mediante herramienta de mantenedor, usando solo fixtures sintéticas incorporadas; no importar bases de participantes ni publicar datos.

## 006/FR-016 — sustituir mecanismo

Familia: N12. Necesidad: necesario con mecanismo consolidable.

Motivo: Conservar identidad y reproducción del experimento; manifiestos y objetos compartidos pueden reemplazar snapshots repetidos, sin reeditar originales o exigir identidad textual generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 191. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: El sistema MUST conservar contratos y regresiones 001–005; documentar instalación, ejemplos ejecutados, límites, pruebas negativas y propuesta de evolución sin notas ni perfiles.

## 006/SC-001 — retirar del criterio del producto actual

Familia: N07. Necesidad: experimental.

Motivo: La comparación arquitectónica y los conteos de composiciones son investigación legítima separada del listo del chat; no repetir el catálogo sintético completo como evidencia de utilidad generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 219. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: Baseline, agencia y ambas ablaciones completan el catálogo mínimo de quince escenarios con resultados o fallos explícitos para cada celda.

## 006/SC-002 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para declarar listo.

Motivo: Latencia, recursos, utilidad percibida, carga docente y límites honestos son necesarios para valorar coste y resultado; faltantes no se presentan como cero ni satisfacción como aprendizaje.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 221. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: El 100% de resultados declara procedencia de métricas y motivos de valores ausentes; nunca se presenta falta de medida como cero.

## 006/SC-003 — sustituir mecanismo

Familia: N12. Necesidad: necesario con mecanismo consolidable.

Motivo: Conservar identidad y reproducción del experimento; manifiestos y objetos compartidos pueden reemplazar snapshots repetidos, sin reeditar originales o exigir identidad textual generativa.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 223. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: Un paquete determinista repetido conserva el 100% de secuencias y decisiones estructurales comparables; manipular entradas o código se detecta.

## 006/SC-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad de experimentación.

Motivo: Conservar aislamiento de ablaciones, no exponer fallos inseguros a usuarios y no importar datos privados; esas condiciones siguen vigentes aunque el estudio se aplace.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 225. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: Las inyecciones previstas dejan resultado trazable y evidencia de recuperación o cierre; ninguna altera sesiones de la instalación normal.

## 006/SC-005 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para declarar listo.

Motivo: Latencia, recursos, utilidad percibida, carga docente y límites honestos son necesarios para valorar coste y resultado; faltantes no se presentan como cero ni satisfacción como aprendizaje.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 227. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: Los informes muestran tamaño de muestra, variabilidad, no comparabilidad y límites, incluidos resultados negativos y ausencia de valoración humana.

## 006/SC-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad de experimentación.

Motivo: Conservar aislamiento de ablaciones, no exponer fallos inseguros a usuarios y no importar datos privados; esas condiciones siguen vigentes aunque el estudio se aplace.

Fuente: [specs/006-architecture-validation/spec.md](../../../specs/006-architecture-validation/spec.md), línea 229. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: Las pruebas demuestran que las ablaciones no están disponibles para datos de usuario ni por rutas de producción y que no asignan notas.

## 007/FR-001 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para uso.

Motivo: Arranque honesto y un recorrido por teclado sin copiar identificadores son necesidades de operación; reutilizar el launcher sin crear un producto demo paralelo.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 69. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST arrancar desde PowerShell con un comando, verificar dependencias/puertos/esquema/recursos, iniciar solo localhost y abrir navegador únicamente tras readiness real.

## 007/FR-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 70. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: El sistema MUST rechazar puertos ocupados sin cambiar puertos ni detener procesos ajenos; comunicar causa y solución de fallos, incluyendo arranque parcial.

## 007/FR-003 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 71. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: El sistema MUST solicitar credencial administrativa por entrada oculta o entorno de proceso; nunca escribir secretos en argumentos, URLs, archivos, frontend o logs; mantener autenticación normal.

## 007/FR-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 72. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: El sistema MUST permitir parar solo procesos creados por el lanzador, comprobar su propiedad y limpiar arranques parciales; una parada no afecta procesos ajenos.

## 007/FR-005 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 73. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST aislar base, índice, archivos, configuración y logs de demo del entorno habitual; rechazar rutas/links que escapen del espacio de demo.

## 007/FR-006 — sustituir mecanismo

Familia: N09. Necesidad: necesario con fixture prescriptiva.

Motivo: Idempotencia y conservación de recursos son necesarias; la obligación de sembrar dos agencias y materiales ficticios pertenece a la demo y no a cada arranque de estudio real.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 74. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST preparar de forma idempotente curso/material breve/autoestudio/defensa ficticios, configuraciones activas y políticas de salida/retención válidas sin duplicar al arrancar.

## 007/FR-007 — aplazar nueva ampliación

Familia: N09. Necesidad: deseable posterior.

Motivo: Reset es una comodidad del demostrador, no necesidad del alumno; mantener su seguridad si existe y no añadir otra ruta destructiva antes del chat útil.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 75. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: El sistema MUST ofrecer reinicio explícito con ruta verificada y confirmación previa al borrado; rechazar demo activa, rutas no reconocidas y enlaces.

## 007/FR-008 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 76. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: El sistema MUST no descargar modelos silenciosamente; comprobar recursos locales y ofrecer explícitamente texto sin fuentes si faltan embeddings, sin simular fuentes, voz o modelos reales.

## 007/FR-009 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para uso.

Motivo: Arranque honesto y un recorrido por teclado sin copiar identificadores son necesidades de operación; reutilizar el launcher sin crear un producto demo paralelo.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 77. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El sistema MUST mostrar portada con accesos a participante y área docente, identificando IA, datos ficticios y funcionamiento determinista cuando corresponda; conservar rutas existentes.

## 007/FR-010 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para uso.

Motivo: Arranque honesto y un recorrido por teclado sin copiar identificadores son necesidades de operación; reutilizar el launcher sin crear un producto demo paralelo.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 78. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: El sistema MUST permitir abrir desde el área autenticada una actividad activa en su modo sin copiar identificadores; solo referencias no secretas viajan en navegación y el código seudónimo nunca autentica.

## 007/FR-011 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para uso.

Motivo: Arranque honesto y un recorrido por teclado sin copiar identificadores son necesidades de operación; reutilizar el launcher sin crear un producto demo paralelo.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 79. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: El sistema MUST ofrecer recorrido textual y de teclado con mensajes comprensibles, fuentes reales cuando disponibles, elección de scopes, cierre, revisión, exportación y eliminación verificable.

## 007/FR-012 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 80. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST permitir una alternativa efímera sin conservación; mantener T090/T150, permisos/propiedad, scopes/plazos/retención y aislamiento de sesiones.

## 007/FR-013 — sustituir mecanismo

Familia: N12. Necesidad: prescripción de demostración.

Motivo: Conservar guía de operación y límites; diez minutos es un guion de presentación, no duración ni criterio de éxito obligatorio del estudio.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 81. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST documentar guion aproximado de diez minutos, preparación/arranque/parada/reinicio/fallos y diferencia entre determinismo, modelos reales y validación humana pendiente.

## 007/FR-014 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para aceptación.

Motivo: Un recorrido real y offline de preparación a cierre es necesario para no confundir seed o tests aislados con experiencia utilizable.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 82. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: El sistema MUST probar lanzador/aislamiento, recorrido real de portada a exportación/borrado y ensayo offline tras preparación, sin alterar base habitual ni procesos ajenos.

## 007/FR-015 — sustituir mecanismo

Familia: N12. Necesidad: proceso prescriptivo y redundante.

Motivo: Preservar integridad y pruebas pertinentes; consolidar evidencia y elegir regresiones por impacto, sin nueva copia del experimento204 o suite global por cada cambio aislado.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 83. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: El sistema MUST preservar paquete006 original e integridad; registrar cambios de código del manifiesto y generar/reproducir evidencia actual con hashes medidos, nunca ajustarlos manualmente.

## 007/FR-016 — sustituir mecanismo

Familia: N12. Necesidad: proceso prescriptivo y redundante.

Motivo: Preservar integridad y pruebas pertinentes; consolidar evidencia y elegir regresiones por impacto, sin nueva copia del experimento204 o suite global por cada cambio aislado.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 84. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: El sistema MUST completar regresión global, build/lint/Playwright, Black afectado y Ruff Counter contra baseline durable; migraciones limpias/upgrade si cambia esquema; entregar tabla de tareas, archivos y límites.

## 007/SC-001 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para uso.

Motivo: Arranque honesto y un recorrido por teclado sin copiar identificadores son necesidades de operación; reutilizar el launcher sin crear un producto demo paralelo.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 97. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: Un comando inicia los dos servicios y anuncia sus URLs solo cuando están listos; los errores preparados son accionables y no provocan arranques ocultos.

## 007/SC-002 — sustituir mecanismo

Familia: N09. Necesidad: necesario con fixture prescriptiva.

Motivo: Idempotencia y conservación de recursos son necesarias; la obligación de sembrar dos agencias y materiales ficticios pertenece a la demo y no a cada arranque de estudio real.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 98. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: Arranque repetido conserva exactamente una copia de cada fixture y parada/reinicio dejan intactos recursos habituales y procesos ajenos preparados.

## 007/SC-003 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para uso.

Motivo: Arranque honesto y un recorrido por teclado sin copiar identificadores son necesidades de operación; reutilizar el launcher sin crear un producto demo paralelo.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 99. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: Un recorrido real por teclado desde portada completa login, actividad, fuentes, conservación, cierre, revisión, exportación y borrado; alternativa efímera no es revisable.

## 007/SC-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 100. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El ensayo offline completa el recorrido preparado sin descargas ni conexiones externas; ausencia de recursos no se disfraza de funcionamiento real.

## 007/SC-005 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Puertos, procesos, credenciales, aislamiento, ausencia de descargas silenciosas y modo efímero protegen recursos y personas; mantener límites aun simplificando presentación.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 101. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: Todas las denegaciones de permisos/propiedad/confirmación/rutas/puertos preparadas fallan cerradas sin exponer secretos ni borrar contenido ajeno.

## 007/SC-006 — sustituir mecanismo

Familia: N12. Necesidad: proceso prescriptivo y redundante.

Motivo: Preservar integridad y pruebas pertinentes; consolidar evidencia y elegir regresiones por impacto, sin nueva copia del experimento204 o suite global por cada cambio aislado.

Fuente: [specs/007-local-demonstration/spec.md](../../../specs/007-local-demonstration/spec.md), línea 102. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: El paquete006 original conserva hashes; el paquete actual ejecuta/reproduce204celdas y las puertas globales pasan sin nuevas infracciones Ruff.

## 008/FR-001 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para operación.

Motivo: Mostrar etapa real, readiness y siguiente acción ante error reduce incertidumbre del usuario; no anunciar disponibilidad por el mero inicio del proceso.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 47. Contexto: ## Requirements.

Requisito leído: - **FR-001**: Mostrar en español las etapas reales de comprobación dependencias/puertos, embeddings cuando corresponda, preparación demo, inicio API, inicio interfaz y espera de disponibilidad. Separar proceso iniciado de servicio listo.

## 008/FR-002 — sustituir mecanismo

Familia: N14. Necesidad: prescripción de interfaz.

Motivo: Feedback de espera y fin de aviso es necesario; cinco segundos y prohibición absoluta de toda estimación son mecanismos del ensayo, sustituibles por comunicación honesta según operación.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 48. Contexto: ## Requirements.

Requisito leído: - **FR-002**: Durante operaciones largas mostrar tiempo transcurrido cada5s aproximadamente, advertir carga inicial lenta, sin porcentajes/ETA ni saturación. El aviso termina al finalizar/fallar/cancelar su etapa.

## 008/FR-003 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para operación.

Motivo: Mostrar etapa real, readiness y siguiente acción ante error reduce incertidumbre del usuario; no anunciar disponibilidad por el mero inicio del proceso.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 49. Contexto: ## Requirements.

Requisito leído: - **FR-003**: Anunciar DEMO LISTA con URL e instrucciones solo tras verificar ambos servicios propios; navegador después, respetando NoBrowser.

## 008/FR-004 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para operación.

Motivo: Mostrar etapa real, readiness y siguiente acción ante error reduce incertidumbre del usuario; no anunciar disponibilidad por el mero inicio del proceso.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 50. Contexto: ## Requirements.

Requisito leído: - **FR-004**: Fallos identifican etapa, causa conocida o no determinada y siguiente acción; preservar timeouts y diagnóstico detallado en logs sin secretos, tokens, entorno completo ni contenido de sesiones.

## 008/FR-005 — sustituir mecanismo

Familia: N09. Necesidad: mecanismo de demo consolidable.

Motivo: Conservar comprobación sin efectos, cancelación y opciones existentes; no exigir todas las opciones de demo en el producto ni una vía sin fuentes que parezca cumplir RAG.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 51. Contexto: ## Requirements.

Requisito leído: - **FR-005**: Conservar Start/Check/Stop/Reset/NoBrowser/TextOnly/puertos explícitos; Check no pide credenciales ni inicia servicios; TextOnly no anuncia carga de embeddings ni fuentes disponibles.

## 008/FR-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Credenciales ocultas, procesos propios y preservación de permiso y privacidad son necesarios independientemente del indicador de progreso.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 52. Contexto: ## Requirements.

Requisito leído: - **FR-006**: Credencial oculta y en memoria; mantener bloqueo concurrente, propiedad de procesos, limpieza/cancelación, localhost/offline/auth/consentimiento/T090/T150 y aislamiento.

## 008/FR-007 — conservar para uso actual

Familia: N09. Necesidad: mantenibilidad de alto valor.

Motivo: Eliminar solo comprobaciones redundantes demostradas es proporcional; no eliminar validaciones de procesos o momentos diferentes por similitud de nombre.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 53. Contexto: ## Requirements.

Requisito leído: - **FR-007**: Auditar comprobaciones repetidas y quitar solo trabajo innecesario demostrado; preservar validaciones necesarias de procesos diferentes; no atribuir mejoras de rendimiento sin medición.

## 008/FR-008 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario con duplicación evitable.

Motivo: Conservar preservación, diagnóstico y verificación de rutas; consolidar ensayos y documentación por impacto, sin equiparar analyze/converge con utilidad del tutor.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 54. Contexto: ## Requirements.

Requisito leído: - **FR-008**: Preservar entorno preparado, datos habituales y paquetes experimentales; sin Reset ni commits; regenerar/reproducir evidencia actual si cambian fuentes de manifiesto.

## 008/FR-009 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario con duplicación evitable.

Motivo: Conservar preservación, diagnóstico y verificación de rutas; consolidar ensayos y documentación por impacto, sin equiparar analyze/converge con utilidad del tutor.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 55. Contexto: ## Requirements.

Requisito leído: - **FR-009**: Probar secuencia/espera/error/cancelación/full/TextOnly/Check/puerto ocupado/secretos; ensayo real PowerShell y check-demo; regresiones relevantes y global si cambia comportamiento compartido; Black afectado/Ruff Counter con multiplicidad durable.

## 008/FR-010 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario con duplicación evitable.

Motivo: Conservar preservación, diagnóstico y verificación de rutas; consolidar ensayos y documentación por impacto, sin equiparar analyze/converge con utilidad del tutor.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 56. Contexto: ## Requirements.

Requisito leído: - **FR-010**: Documentar etapas, comandos, tiempos observados iniciales/posteriores, tareas/archivos/límites; cerrar solo analyze sin críticos y converge sin brechas.

## 008/SC-001 — conservar para uso actual

Familia: N09. Necesidad: imprescindible para operación.

Motivo: Mostrar etapa real, readiness y siguiente acción ante error reduce incertidumbre del usuario; no anunciar disponibilidad por el mero inicio del proceso.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 65. Contexto: ## Success Criteria.

Requisito leído: - **SC-001**: Todas las etapas observadas corresponden a operaciones reales; cero disponibilidad prematura en pruebas.

## 008/SC-002 — sustituir mecanismo

Familia: N14. Necesidad: prescripción de interfaz.

Motivo: Feedback de espera y fin de aviso es necesario; cinco segundos y prohibición absoluta de toda estimación son mecanismos del ensayo, sustituibles por comunicación honesta según operación.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 66. Contexto: ## Success Criteria.

Requisito leído: - **SC-002**: Espera inducida superior al intervalo produce aviso temporal, cesa al salir y no muestra porcentaje/ETA.

## 008/SC-003 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario con duplicación evitable.

Motivo: Conservar preservación, diagnóstico y verificación de rutas; consolidar ensayos y documentación por impacto, sin equiparar analyze/converge con utilidad del tutor.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 67. Contexto: ## Success Criteria.

Requisito leído: - **SC-003**: Casos full/TextOnly/Check/error/cancelación y script de comprobación pasan; cero credenciales ficticias en mensajes/logs inspeccionados.

## 008/SC-004 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario con duplicación evitable.

Motivo: Conservar preservación, diagnóstico y verificación de rutas; consolidar ensayos y documentación por impacto, sin equiparar analyze/converge con utilidad del tutor.

Fuente: [specs/008-demo-startup-progress/spec.md](../../../specs/008-demo-startup-progress/spec.md), línea 68. Contexto: ## Success Criteria.

Requisito leído: - **SC-004**: Ensayo de dos arranques sin Reset deja datos preparados/habituales iguales y centinela vivo; gates y evidencia actual pasan, originales intactos.

## 009/FR-001 — retirar del criterio del producto actual

Familia: N10. Necesidad: histórico experimental.

Motivo: El archivo04 y su primer fallo son evidencia histórica específica; preservarlos como regresión, no exigir ese caso concreto como necesidad de cada episodio de estudio.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 49. Contexto: ## Requirements.

Requisito leído: - **FR-001**: Reproducir primero archivo04 original por carga/extracción/índice reales y registrar fallo previo; no acortar ni sustituirlo.

## 009/FR-002 — conservar para uso actual

Familia: N03. Necesidad: imprescindible para materiales.

Motivo: Documentos y fragmentos largos deben poder usarse sin romper procedencia ni Unicode; las fronteras numéricas del banco se conservan como controles, no como límite universal docente.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 50. Contexto: ## Requirements.

Requisito leído: - **FR-002**: Permitir extracción legítima larga mediante vínculo estructurado con fuente vigente; no invalid_context por diferencia interna de recorte; sesión utilizable.

## 009/FR-003 — conservar para uso actual

Familia: N03. Necesidad: imprescindible para materiales.

Motivo: Documentos y fragmentos largos deben poder usarse sin romper procedencia ni Unicode; las fronteras numéricas del banco se conservan como controles, no como límite universal docente.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 51. Contexto: ## Requirements.

Requisito leído: - **FR-003**: Comprobar longitudes antes/en/después400,múltiples fragmentos,Unicode,procedencia/versión/ubicación; conservar acotación y determinismo de extracción.

## 009/FR-004 — sustituir mecanismo

Familia: N05. Necesidad: mecanismo incompatible si se universaliza.

Motivo: Exactitud literal es correcta para el perfil extractivo; mantenerlo allí, pero requiere contrato sucesor para texto libre generado, no una prohibición general de paráfrasis.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 52. Contexto: ## Requirements.

Requisito leído: - **FR-004**: Solo texto exacto reconstruible de datos autorizados obtiene propuesta; mutaciones,texto libre,scope/procedencia/versión/ubicación ajenos se deniegan,con salida nula saneada y fallback acotado.

## 009/FR-005 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Mantener controles de autorización, salida nula ante permiso inválido y privacidad de rutas largas; no debilitar esas garantías por ampliar contexto.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 53. Contexto: ## Requirements.

Requisito leído: - **FR-005**: Mantener T090/T150,verificadores,plantillas/políticas existentes,consentimiento/scopes,acceso/aislamiento y cierre/exportación/borrado en ambos modos.

## 009/FR-006 — aplazar nueva ampliación

Familia: N10. Necesidad: regresión histórica condicional.

Motivo: El recorrido de archivo04 debe conservarse y repetirse si se afecta su ruta; no ampliar una demo extractiva antes de demostrar el chat generativo.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 54. Contexto: ## Requirements.

Requisito leído: - **FR-006**: Recorrido navegador docente con carga real archivo04,actividad,turno/fuentes,cierre,revisión,exportación y eliminación verificable; no solo seed breve.

## 009/FR-007 — sustituir mecanismo

Familia: N12. Necesidad: proceso redundante consolidable.

Motivo: Preservar fuentes, diagnósticos y regresiones pertinentes; unificar entrega y reproducción sin suite o paquete nuevo por ritual, y separar conformidad documental de listo.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 55. Contexto: ## Requirements.

Requisito leído: - **FR-007**: Preservar datos habituales/demo preparados sin Reset ni commits; registrar fuente/paquetes previos y regenerar/reproducir evidencia actual si manifiesto cambia.

## 009/FR-008 — sustituir mecanismo

Familia: N12. Necesidad: proceso redundante consolidable.

Motivo: Preservar fuentes, diagnósticos y regresiones pertinentes; unificar entrega y reproducción sin suite o paquete nuevo por ritual, y separar conformidad documental de listo.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 56. Contexto: ## Requirements.

Requisito leído: - **FR-008**: Suite determinista global,build/lint/Playwright,check-demo,Black afectados,Ruff Counter con multiplicidad frente baseline durable; sin nuevas infracciones.

## 009/FR-009 — sustituir mecanismo

Familia: N12. Necesidad: proceso redundante consolidable.

Motivo: Preservar fuentes, diagnósticos y regresiones pertinentes; unificar entrega y reproducción sin suite o paquete nuevo por ritual, y separar conformidad documental de listo.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 57. Contexto: ## Requirements.

Requisito leído: - **FR-009**: Actualizar materiales/docente/RESULTADO.md con causa,cambios,comandos,resultados medidos y límites una vez corregido; no afirmar soporte universal ni validación semántica/humana/voz.

## 009/FR-010 — sustituir mecanismo

Familia: N12. Necesidad: proceso redundante consolidable.

Motivo: Preservar fuentes, diagnósticos y regresiones pertinentes; unificar entrega y reproducción sin suite o paquete nuevo por ritual, y separar conformidad documental de listo.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 58. Contexto: ## Requirements.

Requisito leído: - **FR-010**: Artefactos SpecKit trazables y cierre solo analyze sin críticos y converge sin brechas obligatorias.

## 009/SC-001 — retirar del criterio del producto actual

Familia: N10. Necesidad: histórico experimental.

Motivo: El archivo04 y su primer fallo son evidencia histórica específica; preservarlos como regresión, no exigir ese caso concreto como necesidad de cada episodio de estudio.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 67. Contexto: ## Success Criteria.

Requisito leído: - **SC-001**: El caso04 falla antes y pasa después con respuesta/fuentes reales y segundo turno usable.

## 009/SC-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Mantener controles de autorización, salida nula ante permiso inválido y privacidad de rutas largas; no debilitar esas garantías por ampliar contexto.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 68. Contexto: ## Success Criteria.

Requisito leído: - **SC-002**: Matriz de frontera/procedencia pasa y todas las mutaciones preparadas se deniegan sin escape de texto ni ampliación de fallback.

## 009/SC-003 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Mantener controles de autorización, salida nula ante permiso inválido y privacidad de rutas largas; no debilitar esas garantías por ampliar contexto.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 69. Contexto: ## Success Criteria.

Requisito leído: - **SC-003**: Matriz ambos modos/scopes y recorrido largo navegador pasan con privacidad/exportación/borrado.

## 009/SC-004 — sustituir mecanismo

Familia: N12. Necesidad: proceso redundante consolidable.

Motivo: Preservar fuentes, diagnósticos y regresiones pertinentes; unificar entrega y reproducción sin suite o paquete nuevo por ritual, y separar conformidad documental de listo.

Fuente: [specs/009-long-extractive-binding/spec.md](../../../specs/009-long-extractive-binding/spec.md), línea 70. Contexto: ## Success Criteria.

Requisito leído: - **SC-004**: Gates sin regresiones,nuevos Ruff0,paquetes originales/hashes y recursos estables intactos,evidencia actual reproducible.

## 010/FR-001 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 103. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: El sistema MUST preservar la finalidad de apoyo al estudio y ensayo: no asignar notas, diagnosticar capacidad, sustituir al docente ni construir perfiles longitudinales.

## 010/FR-002 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 104. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: El sistema MUST distinguir saludo, consulta o respuesta temática, repetir, reformular, ayuda/no sé, continuar, ejemplo, comparación, cambio de tema/modo, finalizar y entrada ambigua; expresar incertidumbre y separar acto conversacional de modo de estudio.

## 010/FR-003 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 105. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: El sistema MUST mantener tema y pregunta pendientes a través de órdenes de control y resolver referencias breves solo cuando exista un referente inequívoco, sin sustituirlo por la última palabra recibida.

## 010/FR-004 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 106. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: El sistema MUST ante dos referentes plausibles o instrucciones incompatibles, pedir una aclaración concreta con opciones autorizadas y continuar tras la selección; una negación como «no repitas» no debe disparar repetir.

## 010/FR-005 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 107. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: El sistema MUST orientar ante un saludo y una consulta general dentro del tema con alcance, opciones y un siguiente paso; no alegar ausencia de información si hay material pertinente disponible sin comprobarlo.

## 010/FR-006 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 108. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: El sistema MUST repetir la pregunta o salida solicitada fielmente, identificando cuál se repite y comprobando que sigue autorizada; no generar otra pregunta ni tratar la petición como respuesta al contenido.

## 010/FR-007 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 109. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: El sistema MUST reformular sobre el mismo objetivo y ofrecer ejemplos/comparaciones diferentes cuando haya contenido autorizado para ello; si no existe, explicar el límite y ofrecer una alternativa concreta, sin anunciar una reformulación que solo repite.

## 010/FR-008 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 110. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: El sistema MUST responder a «no sé», ayuda o bloqueo con una pista o paso siguiente pertinente; respetar la política docente de no revelar solución, incluida la revelación indirecta por pistas, ejemplos, resumen y panel de fuentes.

## 010/FR-009 — sustituir mecanismo

Familia: N01. Necesidad: prescripción pedagógica de alto valor pero flexible.

Motivo: Conservar foco, prevención de bucles y opciones manejables; un objetivo por intervención, dos intentos y máximo tres temas son heurísticas revisables, no necesidades universales de toda pregunta compuesta.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 111. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: El sistema MUST cambiar de tema o pregunta únicamente dentro de la actividad, conservando la pregunta actual hasta confirmar la transición y presentando un único objetivo principal por intervención.

## 010/FR-010 — aplazar nueva ampliación

Familia: N10. Necesidad: histórico o deseable posterior según perfil.

Motivo: Preservar habilidades y controles de perfiles anteriores; dos dominios sintéticos, cinco modos o unidades docentes publicadas no deben ampliarse para sustituir generación desde documentos ni forzar defensa ahora.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 112. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: El sistema MUST en defensa, relacionar cada repregunta con una afirmación identificable de la respuesta y su fuente u objetivo; no usar partículas, números aislados o verbos de control como conceptos temáticos sin contexto.

## 010/FR-011 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 113. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: El sistema MUST abordar diferencias entre lo dicho y una fuente de manera neutral: mantener ambas afirmaciones distintas, explicitar condiciones/unidades si están documentadas y pedir justificación o aclaración sin calificar; no asumir que 99/100 es siempre contradicción.

## 010/FR-012 — aplazar nueva ampliación

Familia: N10. Necesidad: histórico o deseable posterior según perfil.

Motivo: Preservar habilidades y controles de perfiles anteriores; dos dominios sintéticos, cinco modos o unidades docentes publicadas no deben ampliarse para sustituir generación desde documentos ni forzar defensa ahora.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 114. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: El sistema MUST en autoestudio, cubrir duda, explicación guiada, práctica, exposición y revisión según modos habilitados; no convertir toda entrada en duda ni responder a tareas prohibidas por el perfil.

## 010/FR-013 — sustituir mecanismo

Familia: N01. Necesidad: prescripción pedagógica de alto valor pero flexible.

Motivo: Conservar foco, prevención de bucles y opciones manejables; un objetivo por intervención, dos intentos y máximo tres temas son heurísticas revisables, no necesidades universales de toda pregunta compuesta.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 115. Contexto: ### Functional Requirements.

Requisito leído: - **FR-013**: El sistema MUST prevenir bucles: tras una primera salida estancada cambiar estrategia; al segundo intento consecutivo sin avance ofrecer opciones distintas y ejecutables. No emitir dos avisos genéricos idénticos consecutivos por falta de progreso; avance significa cambio observable de acción, subobjetivo o evidencia, no aprendizaje inferido.

## 010/FR-014 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 116. Contexto: ### Functional Requirements.

Requisito leído: - **FR-014**: El sistema MUST resolver recuperación con la pregunta original y el contexto temático autorizado, manteniendo separados texto literal y consulta contextual; revalidar material, versión, destinatario y alcance en cada uso o repetición.

## 010/FR-015 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 117. Contexto: ### Functional Requirements.

Requisito leído: - **FR-015**: El sistema MUST reconocer materiales insuficientes, conflictos o revocaciones entre turnos; no resolverlos por invención ni reutilizar contenido revocado desde memoria; señalar qué falta y qué sí puede hacerse.

## 010/FR-016 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 118. Contexto: ### Functional Requirements.

Requisito leído: - **FR-016**: El sistema MUST presentar explicaciones y prácticas con fuentes suficientes, distinguiendo hechos del material, ejemplos docentes revisados e incertidumbre; una respuesta superficial o un aviso autorizado no prueba utilidad del diálogo.

## 010/FR-017 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 119. Contexto: ### Functional Requirements.

Requisito leído: - **FR-017**: El sistema MUST autorizar cada salida y cada transformación mediante una propuesta estructurada verificable; no convertir texto generado, un hash propio o similitud léxica en permiso de publicación.

## 010/FR-018 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 120. Contexto: ### Functional Requirements.

Requisito leído: - **FR-018**: El sistema MUST mantener independencia entre interpretación, decisión, recuperación, generación y verificación; no eliminar controles de fundamentación, coherencia, no revelación o autorización para obtener respuestas más fluidas.

## 010/FR-019 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 121. Contexto: ### Functional Requirements.

Requisito leído: - **FR-019**: El sistema MUST mostrar capacidades y proveedor efectivos antes y durante uso: guiado controlado, extractivo limitado, generativo local validado o degradado. Cambiar a reserva requiere aviso; ausencia de un modelo nunca cuenta como prueba de generación real.

## 010/FR-020 — aplazar nueva ampliación

Familia: N10. Necesidad: histórico o deseable posterior según perfil.

Motivo: Preservar habilidades y controles de perfiles anteriores; dos dominios sintéticos, cinco modos o unidades docentes publicadas no deben ampliarse para sustituir generación desde documentos ni forzar defensa ahora.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 122. Contexto: ### Functional Requirements.

Requisito leído: - **FR-020**: El sistema MUST disponer de materiales docentes desarrollados, versionados y editables en al menos dos dominios; declarar qué explicaciones, ejemplos, contrastes y pistas están cubiertos. El material de dos frases se conserva como prueba de insuficiencia, no como demostración completa.

## 010/FR-021 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 123. Contexto: ### Functional Requirements.

Requisito leído: - **FR-021**: El sistema MUST detectar código destinatario incompatible y actividad no utilizable antes de crear una sesión o consumir su bloqueo; ofrecer corrección sin ampliar permisos ni sustituir silenciosamente la identidad elegida. La demo puede proponer demo-007 explícitamente.

## 010/FR-022 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 124. Contexto: ### Functional Requirements.

Requisito leído: - **FR-022**: El sistema MUST ante sesión ocupada o acceso perdido, ofrecer vuelta a la sesión si se conserva la autorización o cierre administrativo explícito con confirmación y política vigente; nunca cerrar sesiones ajenas automáticamente, recuperar identidad por código ni requerir edición SQL/Reset para continuar.

## 010/FR-023 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 125. Contexto: ### Functional Requirements.

Requisito leído: - **FR-023**: El sistema MUST mostrar modalidad efectiva, pregunta, entrada textual y fuentes encontrables por teclado, además de ocupado/error; ausencia de voz no puede parecer un fallo del texto. No prometer audio sin disponibilidad comprobada.

## 010/FR-024 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 126. Contexto: ### Functional Requirements.

Requisito leído: - **FR-024**: El sistema MUST manejar doble envío, cancelación, respuesta tardía, desconexión y reintento sin duplicar turnos, avanzar pregunta indebidamente ni resucitar datos cerrados; informar si el resultado es desconocido y reconciliar antes de reenviar.

## 010/FR-025 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 127. Contexto: ### Functional Requirements.

Requisito leído: - **FR-025**: El sistema MUST mantener presupuestos finitos por turno y sesión, incluidos repetir, reformular y recuperaciones; advertir de límites y aplicar cierre ganador único. Los controles de interfaz no eluden duración ni recursos.

## 010/FR-026 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 128. Contexto: ### Functional Requirements.

Requisito leído: - **FR-026**: El sistema MUST someter contexto, memoria auxiliar, corpus de pruebas e informes a minimización, consentimiento, scopes, caducidad, borrado y aislamiento; no volcar conversaciones personales ni razonamiento privado en los artefactos del plan o logs.

## 010/FR-027 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 129. Contexto: ### Functional Requirements.

Requisito leído: - **FR-027**: El sistema MUST versionar políticas, contratos, estado y actividades modificados; conservar sesiones antiguas y generar sucesoras para demo/materiales/perfiles nuevos sin Reset, migración silenciosa o relajación de autenticación normal.

## 010/FR-028 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 130. Contexto: ### Functional Requirements.

Requisito leído: - **FR-028**: El sistema MUST registrar intención, referente, decisión, estrategia de recuperación, evidencia, verificaciones, proveedor, tiempos y resultado estructural; no persistir candidatos rechazados ni presentar confianza heurística como certeza.

## 010/FR-029 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 131. Contexto: ### Functional Requirements.

Requisito leído: - **FR-029**: El sistema MUST validar secuencias completas de usuario, variantes y combinaciones no usadas para ajustar la implementación, en dos dominios y con generadores/proveedores reales del perfil anunciado; distinguir dobles de contrato de evidencia conversacional.

## 010/FR-030 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 132. Contexto: ### Functional Requirements.

Requisito leído: - **FR-030**: El sistema MUST separar aprobación técnica, aceptación de diálogo y evaluación humana. No declarar herramienta conversacional útil solo por totales de tests; publicar fallos, denominadores y capacidades pendientes por perfil.

## 010/FR-031 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 133. Contexto: ### Functional Requirements.

Requisito leído: - **FR-031**: El sistema MUST verificar instalación/arranque y recuperación desde PowerShell normal además del entorno del agente, cargas lentas y recursos ausentes sin dependencias ocultas ni cambios de PATH permanentes.

## 010/FR-032 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 134. Contexto: ### Functional Requirements.

Requisito leído: - **FR-032**: El sistema MUST entregar migraciones y retorno a versión anterior documentados, evidencia reproducible y extensión futura de modelo/voz/materiales mediante contratos, sin implementar nube, SSO, concurrencia múltiple o funciones excluidas de la constitución.

## 010/FR-033 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 136. Contexto: ### Functional Requirements.

Requisito leído: - **FR-033**: El sistema MUST disponer de conversaciones sintéticas reproducibles que ejerciten herramientas y operaciones públicas de ORALIA con roles, argumentos, efectos y resultados esperados, caminos normales, llamadas prohibidas, fallos y recuperación; servicios reales del perfil y datos temporales aislados, sin conceder permisos docentes al participante ni sustituir resultados por respuestas favorables. Protocolo en synthetic-tool-conversations.md.

## 010/SC-001 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 151. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-001**: Las dos secuencias observadas completas y sus variantes pasan todas sus aserciones obligatorias de intención, continuidad y siguiente acción en ambos modos del perfil guiado controlado; el perfil extractivo se evalúa con sus límites declarados. Los resultados se publican por caso, sin ocultar fallos con medias.

## 010/SC-002 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 152. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-002**: En un conjunto de 48 entradas de aceptación no usadas para ajustar reglas, al menos 44 reciben el acto/referente esperado; las 48 respetan permisos, y todos los casos ambiguos o negativos críticos deben aclarar o rechazar correctamente.

## 010/SC-003 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 153. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-003**: En 24 diálogos de 6–12 intervenciones (12 de desarrollo y 12 reservados, repartidos entre dos dominios y ambos modos), no hay avisos genéricos idénticos consecutivos y todo bloqueo recuperable ofrece y ejecuta una opción válida en las dos intervenciones siguientes.

## 010/SC-004 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 154. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-004**: El 100% de las respuestas de contenido entregadas en el corpus enlazan evidencia vigente y los controles obligatorios; cero publicaciones no autorizadas, notas, revelaciones de solución prohibidas o fugas de sesión en las matrices negativas.

## 010/SC-005 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 155. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-005**: Los cinco modos habilitables de autoestudio y las acciones repetir/reformular/ayuda/siguiente de defensa tienen al menos un diálogo completo de aceptación por modo/acción y controles negativos para modos deshabilitados.

## 010/SC-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 156. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-006**: El 100% de escenarios operativos prioritarios (destinatario incorrecto, sesión ocupada, acceso perdido, sin audio, carga lenta y envío duplicado) permite recuperarse o terminar explícitamente sin Reset, intervención SQL ni cierre de una sesión ajena.

## 010/SC-007 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 157. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-007**: Cada ejecución publica perfil/modelo, material, versión, semilla si aplica, entorno y tiempos medidos; decisiones de los casos deterministas se reproducen y una generación local no determinista se evalúa por propiedades en tres ejecuciones por caso, sin afirmar identidad textual.

## 010/SC-008 — conservar para uso actual

Familia: N11. Necesidad: imprescindible para aceptación honesta.

Motivo: Separar puertas técnicas, diálogo y utilidad humana evita anunciar listo por conteos de tests; la guía debe poder usarla otra persona.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 158. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-008**: La entrega distingue de manera visible puertas técnicas y conversacionales aprobadas y la utilidad humana aún no medida; explica limitaciones, costes y recuperación en una guía ejecutable por alguien distinto del implementador.

## 010/SC-009 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 160. Contexto: ### Measurable Outcomes.

Requisito leído: - **SC-009**: Los 16 escenarios sintéticos adicionales de herramientas (8 de desarrollo y 8 reservados) pasan todas sus propiedades obligatorias de llamada, argumentos, estado y respuesta; cero operaciones no autorizadas, duplicados, fugas o resurrección de datos. Resultados por familia distinguen fallos inyectados de recorridos normales.

## 010/FR-034 — sustituir mecanismo

Familia: N01. Necesidad: prescripción pedagógica de alto valor pero flexible.

Motivo: Conservar foco, prevención de bucles y opciones manejables; un objetivo por intervención, dos intentos y máximo tres temas son heurísticas revisables, no necesidades universales de toda pregunta compuesta.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 186. Contexto: ## Aclaración humana 19-10-2026 — autonomía sin pantalla.

Requisito leído: - **FR-034**: El diálogo MUST enunciar opciones autorizadas manejables (máximo tres temas por intervención, más opciones/repetir opciones) y selección/confirmación verbal sin posiciones visuales. No ofrecer repetir una pregunta inexistente. Revalidar permisos y referencias en cada selección y confirmación.

## 010/FR-035 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 187. Contexto: ## Aclaración humana 19-10-2026 — autonomía sin pantalla.

Requisito leído: - **FR-035**: Fuentes, modos, ayudas, recuperación y límites MUST tener instrucciones conversacionales ejecutables; la procedencia debe ser comprensible al oído y ampliable a petición, sin identificadores técnicos como única referencia ni citas prohibidas. No se autoriza contenido generado por convertirlo en metadatos.

## 010/FR-036 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 188. Contexto: ## Aclaración humana 19-10-2026 — autonomía sin pantalla.

Requisito leído: - **FR-036**: Elección de conservación y cierre MUST tener recorrido conversacional con alcance/plazo explícitos, confirmación inequívoca de la elección pendiente, posibilidad de cancelar y sin asumir que sí equivale a consentimiento; sin conservación por defecto. Revisión/eliminación posteriores MUST respetar propietario, scopes, caducidad y confirmación, sin resucitar estado borrado. T090/T150 y límites siguen vigentes.

## 010/FR-037 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 189. Contexto: ## Aclaración humana 19-10-2026 — autonomía sin pantalla.

Requisito leído: - **FR-037**: La entrega MUST auditar los24 diálogos ocultando interfaz, conservar fallos anteriores, publicar matriz de equivalencia y casos/pasos a corregir, y separar pruebas de texto/transcripción de STT/TTS real, interrupciones, silencios y disponibilidad de modelos. Ninguna prueba textual aprueba voz real, G3 o revisión humana.

## 010/SC-010 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 190. Contexto: ## Aclaración humana 19-10-2026 — autonomía sin pantalla.

Requisito leído: - **SC-010**: En recorridos sin pantalla de ambos dominios y modos, cada acción necesaria está enunciada y ejecutable solo por transcripciones: orientación, elección/confirmación, repetir/reformular/ayuda, fuente, conservación, cierre, revisión y eliminación; cero permisos, contenido prohibido o consentimiento inferidos. Las respuestas v1 anteriores se conservan como compatibilidad limitada, sin atribuirles autonomía nueva.

## 010/FR-038 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 207. Contexto: ## Correcciones humanas D01 — 20-10-2026.

Requisito leído: - **FR-038**: Corresponder al saludo y reconocer preguntas generales sin tratarlas automáticamente como referencias inseguras; orientar con opciones autorizadas y alcance sustentado.

## 010/FR-039 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 208. Contexto: ## Correcciones humanas D01 — 20-10-2026.

Requisito leído: - **FR-039**: Seleccionar respuesta según propósito completo de la petición y contexto: definición, causa, proceso, posibilidad y condiciones. No decidir por palabra aislada (cómo se llama no pide proceso), no ignorar negación ni mezclar preguntas incompatibles. Contestar directamente y con alcance sustentado antes del ejemplo.

## 010/FR-040 — aplazar nueva ampliación

Familia: N10. Necesidad: histórico o deseable posterior según perfil.

Motivo: Preservar habilidades y controles de perfiles anteriores; dos dominios sintéticos, cinco modos o unidades docentes publicadas no deben ampliarse para sustituir generación desde documentos ni forzar defensa ahora.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 209. Contexto: ## Correcciones humanas D01 — 20-10-2026.

Requisito leído: - **FR-040**: Ante duda reiterada conservar el objetivo y cambiar estrategia explicativa con contenido docente publicado: pasos breves, explicación causal, contraste o ejemplo conectado. Repetir literalmente sigue fiel; dímelo se resuelve por contexto, no como regla universal de reformulación. Sin mecanismo publicado, reconocer el límite; no contar material breve como explicación completa.

## 010/FR-041 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 210. Contexto: ## Correcciones humanas D01 — 20-10-2026.

Requisito leído: - **FR-041**: Evaluar pertinencia/didáctica con oráculos independientes de publicación, corpus nuevo congelado y segundo dominio. Preservar versiones y fallos previos. Entregar D01 completo corregido; no atribuir aprobación humana global, utilidad G3, audio o excepción de preservación.

## 010/SC-011 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 211. Contexto: ## Correcciones humanas D01 — 20-10-2026.

Requisito leído: - **SC-011**: D01/D02 corregidos responden al propósito en cada paso observado, distinguen posibilidad general de ejemplo y proceso de definición, con saludo y orientación autosuficiente; secuencias nuevas en dos dominios conservan literalidad, negaciones, permisos, no revelación y límites. Clarificaciones resueltas: la evaluación humana anterior es parcial y negativa, no No evaluado. Los nuevos materiales son propuestas docentes ficticias publicadas explícitamente para pruebas; no equivalen a revisión didáctica humana. La corrección se habilita en política sucesora optativa y actividades nuevas, sin reescribir sesiones en uso.

## 010/FR-042 — conservar para uso actual

Familia: N03. Necesidad: imprescindible cuando la fuente lo usa.

Motivo: Tablas nativas, cabeceras y valores literales son contenido docente útil; conservar soporte y QA sin prometer interpretación visual total ni convertir todo a imágenes.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 228. Contexto: ## Corrección de lectura de tablas nativas —20-10-2026.

Requisito leído: - **FR-042**: Extraer texto de tablas nativas DOCX/PPTX en orden documental y de fila/columna, con tabla/fila/columna/celda identificables; conservar literalmente ceros iniciales, coma decimal y texto. Celdas combinadas se emiten desde su origen sin duplicar contenido; Word anidado mantiene orden con límite explícito ante estructura excesiva. Proporcionar contexto acotado de columna/fila sin truncar el contenido principal ni confundir referencia con cabecera semántica. Mantener ubicaciones antiguas de párrafos/diapositivas sin tablas.

## 010/FR-043 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 229. Contexto: ## Corrección de lectura de tablas nativas —20-10-2026.

Requisito leído: - **FR-043**: Las notas de presentador/docentes, comentarios y soluciones en notas no se incorporan automáticamente; notas sin contenido de cuerpo no hacen procesable un archivo. Documentar alcance/exclusiones: processed no garantiza cobertura visual total, OCR o suficiencia. La extracción no activa material ni concede permisos; conservar atribución/versiones/retirada/aislamiento y fuentes vigentes. No reescribir materiales previos, convertir tablas a imágenes ni reprocesar la base habitual; versiones existentes requieren sucesora explícita.

## 010/SC-012 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 230. Contexto: ## Corrección de lectura de tablas nativas —20-10-2026.

Requisito leído: - **SC-012**: Tablas sintéticas DOCX/PPTX y archivo docente real ficticio de13diapositivas conservan007/1000/3,5 con ubicaciones verificables; pruebas de orden/combinadas/anidado/grupos/notas y carga→activación→consulta→retiro/aislamiento pasan por servicios reales. Fuentes previas, historial y datos habituales no cambian. Clarificación rutinaria: notas excluidas sin opción de inclusión implícita; el docente traslada contenido esencial autorizado al cuerpo visible y lo revisa antes de activar. No se añaden OCR, nuevos formatos o reconstrucción del diseño visual.

## 010/FR-044 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 244. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-044**: Preservar manifiesto/bytes del paquete original y comprobar su recepción. Cada revisión necesaria vive en sucesora/overlay separado, con diff y SHA; materiales y actividades habituales no cambian. Mantener propuesta/revisión docente pendiente incluso en publicación técnica explícita de pruebas.

## 010/FR-045 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 245. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-045**: Cargar por API los cuatro formatos en cursos/actividades temporales separados; Word/PPTX programa no se publican juntos. Verificar extracción/tabla/orden/literalidad/citas/versiones/ámbitos/retiro. Notas excluidas; verificar PowerPoint nativo cuando sea posible o registrar límite real.

## 010/FR-046 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 246. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-046**: Resolver cada unidad contra documentos/versiones/fragmentos reales con testigo de presencia textual y relaciones válidas; preguntas/pistas en fuente separada. Cero UUID ficticios, atribución al primer fragmento por defecto o guías/oráculos cargados. Si el formato no contiene una unidad completa, fallar cerrado o declarar/publicar suplemento visible explícito, sin atribuírsela al archivo insuficiente.

## 010/FR-047 — aplazar nueva ampliación

Familia: N10. Necesidad: histórico o deseable posterior según perfil.

Motivo: Preservar habilidades y controles de perfiles anteriores; dos dominios sintéticos, cinco modos o unidades docentes publicadas no deben ampliarse para sustituir generación desde documentos ni forzar defensa ahora.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 247. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-047**: Ejecutar diálogos completos de agua/programa/datos con componentes reales: saludo, definición/causa/proceso/posibilidad/condiciones, respuesta general antes de ejemplos, tres dudas con estrategias distintas, referentes/objetivo/cambio/pregunta pendiente y fuera de fuente. Comparaciones condicionadas no se tratan como contradicción sin atender condiciones. Defensa guía sin revelar solución.

## 010/FR-048 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 248. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-048**: Recorrido conversacional sin controles visuales para orientación/fuentes/conservación/cierre/revisión/borrado verifica estado real y T090/T150; no convierte transcripciones en audio real validado.

## 010/FR-049 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 249. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-049**: Los60 estímulos son desarrollo expuesto; añadir secuencias y reserva independiente congelada antes de ejecutar/ajustar. Conservar primeras ejecuciones/fallos/versiones y transcriptos íntegros con citas y criterios por bloques. La aprobación técnica no aprueba revisión humana, utilidad o pérdida histórica.

## 010/FR-050 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 250. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **FR-050**: Toda corrección de planificación/verificación necesaria se versiona optativamente y conserva independencia/fuentes/no revelación/presupuestos y compatibilidad anterior. Entregar métricas/comandos/tareas/archivos, regresiones, frontend, Ruff estructural y preservación/replay sin reescribir paquetes.

## 010/SC-013 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 251. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **SC-013**: Cuatro escenarios de formato producen vínculos verificables y diálogos de autoestudio/defensa con fuentes reales en los tres dominios; toda cita corresponde al documento/versión activo y cada negativa/confirmación tiene efecto comprobado o límite honesto.

## 010/SC-014 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 252. Contexto: ## Integración controlada del paquete docente —20-10-2026.

Requisito leído: - **SC-014**:60casos únicos de desarrollo y secuencias completas publican resultados por formato/rol; reserva nueva pasa todas sus propiedades obligatorias o queda registrada como fallo sin cierre. Se entrega paquete completo de revisión humana, sin recortes ni aprobación inferida. Clarificaciones rutinarias: PPTX contiene35/50unidades de contenido literalmente yPDF37/50; se registrará suplemento textual explícito solo para lo no vinculable, no una procedencia ficticia. Se excluyen guías/oráculos y notas. La publicación con reviewed=True en test es un acto técnico del actor ficticio, no certificación de revisión docente. No se publica en demo habitual.

## 010/FR-051 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 259. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **FR-051**: Conservar ambas intenciones de saludo con petición académica; derivar objetivo de material/pregunta vigente y responder por propósito de cláusula completa, sin usar un término subordinado como cambio de objetivo. Identidad molecular, precondición de validación y cálculo con ausentes se sustentan en fuente, sin calificar al alumno.

## 010/FR-052 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para uso actual.

Motivo: Actos naturales, referente, explicación pertinente, feedback neutral, capacidades honestas y fuentes accesibles responden a problemas reales del alumno; no requieren un catálogo de frases exactas ni voz activa.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 260. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **FR-052**: Resolver referentes solo desde anclas autorizadas actuales y contexto inequívoco; ante ambigüedad pedir aclaración. Continuar tras duda/rectificación sin menú genérico si existe contenido pertinente. No cambiar tema por vocabulario incidental o negar fuente únicamente por redacción no canónica.

## 010/FR-053 — aplazar nueva ampliación

Familia: N10. Necesidad: histórico o deseable posterior según perfil.

Motivo: Preservar habilidades y controles de perfiles anteriores; dos dominios sintéticos, cinco modos o unidades docentes publicadas no deben ampliarse para sustituir generación desde documentos ni forzar defensa ahora.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 261. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **FR-053**: En defensa, la veracidad incierta de lo dicho por el alumno no invalida una repregunta autorizada independiente. Conservar pregunta/objetivo, variar seguimiento con unidades docentes vigentes y contexto; no calificar, repetir indefinidamente una pregunta genérica, revelar solución o relajar verificadores.

## 010/FR-054 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: No calificación, no revelación condicionada a actividad, fuentes vigentes, recuperación autorizada, idempotencia y consentimiento son garantías de uso; conservar resultados sin imponer el mecanismo literal de un perfil al generativo.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 262. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **FR-054**: Interpretar confirmaciones naturales inequívocas únicamente para la operación pendiente vigente. Cierre y preferencia de conservación siguen siendo decisiones separadas; una confirmación de cierre nunca aumenta conservación, no aplica sin propuesta ni ante negación/cita/ambigüedad. Cancelación, expiración, T090/T150 y atomicidad se conservan.

## 010/FR-055 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 263. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **FR-055**: Evaluar seguimiento con respuestas sintéticas a preguntas efectivamente emitidas, detener/registrar divergencia antes de asumir una pregunta no emitida y separar captura/aceptación. Preservar las100peticiones auditadas, sus primeros fallos y reservas previas; congelar casos nuevos antes de ajustes y publicar transcriptos completos con criterios por paso.

## 010/FR-056 — sustituir mecanismo

Familia: N12. Necesidad: proceso consolidable.

Motivo: Conservar identidad, rollback, primeros fallos y seguimiento de salida real; consolidar paquetes, snapshots y pasos de entrega por versión, sin cambiar exposición de casos ni reescribir evidencia.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 264. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **FR-056**: Versionar política/materiales sucesores explícitos conservando v1–v3, fuentes, manifiestos originales y datos/procesos habituales. Regresiones/global/frontend/Black/Ruff y experimento/replay nuevo con fuente estable; no aprobación humana/audio ni excepción de pérdida inferidas.

## 010/SC-015 — sustituir mecanismo

Familia: N11. Necesidad: método experimental prescriptivo.

Motivo: Conservar evaluación completa de capacidades, roles y casos críticos; cifras48/44,24diálogos,16escenarios,60casos,dominios fijos y3repeticiones describen bancos históricos, no el tamaño necesario de cada evaluación nueva. Probar impacto y diversidad sin aprobar voz desde texto.

Fuente: [specs/010-guided-dialogue/spec.md](../../../specs/010-guided-dialogue/spec.md), línea 265. Contexto: ## Continuidad contextual tras auditoría natural20-10-2026.

Requisito leído: - **SC-015**: Seis secuencias de desarrollo y seis reservadas nuevas en tres dominios/dos modos mantienen intención/contexto/pregunta y cierran por operación pendiente confirmada; el oráculo verifica contenido/fuentes/estado, no HTTP200. Los primeros desvíos naturales auditados tienen regresiones observables y fallos conservados. Clarificación rutinaria: permanece010; se introduce política sucesora optativa v4, no cambios retrospectivos de actividades v3. Reconocimiento finito por cláusulas/relaciones/contexto, no comprensión general. Si se pide terminar sin conservar desde conservación activa, primero se propone revocación, se confirma esa preferencia y después el cierre; no se funden consentimientos.

## 011/FR-001 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Conservar procedencia docente, permisos y aislamiento del perfil existente; no cargar datos personales ni declarar publicación normal desde un ensayo de laboratorio.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 44. Contexto: ### Functional Requirements.

Requisito leído: - **FR-001**: Usar solo documentos docentes proporcionados, PDF único por documento, con hashes y originales intactos.

## 011/FR-002 — retirar del criterio del producto actual

Familia: N10. Necesidad: selección experimental histórica.

Motivo: Las páginas10–12 y dos temas eran un foco extractivo experimental, no el alcance humano completo; preservar el caso sin restringir por él el temario autorizado.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 45. Contexto: ### Functional Requirements.

Requisito leído: - **FR-002**: Iniciar aprendizaje en páginas10–12 del procedimiento; distinguir material disponible de foco activo y citar versión/página real sin atribuir una derivación al original.

## 011/FR-003 — retirar del criterio del producto actual

Familia: N10. Necesidad: selección experimental histórica.

Motivo: Las páginas10–12 y dos temas eran un foco extractivo experimental, no el alcance humano completo; preservar el caso sin restringir por él el temario autorizado.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 46. Contexto: ### Functional Requirements.

Requisito leído: - **FR-003**: Permitir conversación de autoestudio sobre validacion_requisitos y calidad_requisitos con significado propio, sin atajos de cantidades/agua/datos.

## 011/FR-004 — sustituir mecanismo

Familia: N01. Necesidad: restricción histórica superada para el tutor actual.

Motivo: Pertinencia y límite son necesarios; la prohibición de ejemplos no literales corresponde al perfil extractivo y no prevalece sobre la ficción coherente expresamente permitida después.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 47. Contexto: ### Functional Requirements.

Requisito leído: - **FR-004**: Emitir contenido autorizado pertinente o límite explícito; no afirmar ejemplos, hechos de proyecto o pruebas que no consten en la fuente.

## 011/FR-005 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar primer fallo, autoría de derivaciones, privacidad e integridad; compartir evidencia y ejecutar regresiones pertinentes sin perpetuar el protocolo de una entrega pasada como necesidad nueva.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 48. Contexto: ### Functional Requirements.

Requisito leído: - **FR-005**: Conservar y diagnosticar el primer intento fallido antes de modificar producción; demostrar causas con candidatos, referencias y decisiones efectivas.

## 011/FR-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Conservar procedencia docente, permisos y aislamiento del perfil existente; no cargar datos personales ni declarar publicación normal desde un ensayo de laboratorio.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 49. Contexto: ### Functional Requirements.

Requisito leído: - **FR-006**: Mantener T090/T150 y verificadores independientes; toda transformación de contenido conserva testigo de fuente exacto y autorización completa. Nunca eximir controles para publicar.

## 011/FR-007 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para honestidad de capacidad.

Motivo: Mostrar perfil efectivo y no fabricar objetivos para habilitarlo evita prometer capacidades inexistentes; el generativo debe validarse por su propio comportamiento.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 50. Contexto: ### Functional Requirements.

Requisito leído: - **FR-007**: Preservar gates del perfil guiado; no fabricar cinco objetivos/repertorio para activarlo. Elegir perfil adecuado y describir sus límites.

## 011/FR-008 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar primer fallo, autoría de derivaciones, privacidad e integridad; compartir evidencia y ejecutar regresiones pertinentes sin perpetuar el protocolo de una entrega pasada como necesidad nueva.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 51. Contexto: ### Functional Requirements.

Requisito leído: - **FR-008**: Si se preparan unidades o documentos derivados, explicitar autoría, transformación y fuentes; publicación técnica no implica aprobación docente.

## 011/FR-009 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Conservar procedencia docente, permisos y aislamiento del perfil existente; no cargar datos personales ni declarar publicación normal desde un ensayo de laboratorio.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 52. Contexto: ### Functional Requirements.

Requisito leído: - **FR-009**: Separar BD/índice/archivos/credenciales/actividad del entorno habitual y preservar procesos/entornos originales; sin Reset, commits, modelos o descargas nuevos.

## 011/FR-010 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar primer fallo, autoría de derivaciones, privacidad e integridad; compartir evidencia y ejecutar regresiones pertinentes sin perpetuar el protocolo de una entrega pasada como necesidad nueva.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 53. Contexto: ### Functional Requirements.

Requisito leído: - **FR-010**: Entregar transcriptos completos reales con entradas, salidas, fuentes, estado, perfil y verificación; separar propuesta de respuesta ejecutada y captura de aceptación.

## 011/FR-011 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Conservar procedencia docente, permisos y aislamiento del perfil existente; no cargar datos personales ni declarar publicación normal desde un ensayo de laboratorio.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 54. Contexto: ### Functional Requirements.

Requisito leído: - **FR-011**: Preparación repetible y forma de probar el perfil/actividad aislada, sin activación habitual inferida, secretos en URL/logs o bypass de acceso/consentimiento.

## 011/FR-012 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar primer fallo, autoría de derivaciones, privacidad e integridad; compartir evidencia y ejecutar regresiones pertinentes sin perpetuar el protocolo de una entrega pasada como necesidad nueva.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 55. Contexto: ### Functional Requirements.

Requisito leído: - **FR-012**: Validar contratos, fallos, privacidad, regresiones y evidencia histórica; mantener T061/T067 y demás puertas humanas previas abiertas.

## 011/SC-001 — sustituir mecanismo

Familia: N11. Necesidad: métrica experimental prescriptiva.

Motivo: La necesidad es una experiencia útil completa, no exactamente seis turnos ni solo dos temas; conservar el banco antiguo y evaluar objetivos actuales con medidas de utilidad.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 63. Contexto: ## Success Criteria.

Requisito leído: - **SC-001**: Una experiencia académica completa de al menos seis turnos útiles sobre significado, comparación, aclaración y límites produce salidas efectivas con citas o aviso honesto; ninguna sesión se cierra por error ocultado.

## 011/SC-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Conservar procedencia docente, permisos y aislamiento del perfil existente; no cargar datos personales ni declarar publicación normal desde un ensayo de laboratorio.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 64. Contexto: ## Success Criteria.

Requisito leído: - **SC-002**: Cada afirmación publicada se vincula a una fuente vigente; cero atribuciones al antiguo caso numérico y cero contenidos personales/administrativos incorporados.

## 011/SC-003 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar primer fallo, autoría de derivaciones, privacidad e integridad; compartir evidencia y ejecutar regresiones pertinentes sin perpetuar el protocolo de una entrega pasada como necesidad nueva.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 65. Contexto: ## Success Criteria.

Requisito leído: - **SC-003**: Una variante de conversación distinta de desarrollo se congela antes de ajustar; se conserva su primera ejecución y se registra toda divergencia sin simular continuación.

## 011/SC-004 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar primer fallo, autoría de derivaciones, privacidad e integridad; compartir evidencia y ejecutar regresiones pertinentes sin perpetuar el protocolo de una entrega pasada como necesidad nueva.

Fuente: [specs/011-real-course-self-study/spec.md](../../../specs/011-real-course-self-study/spec.md), línea 66. Contexto: ## Success Criteria.

Requisito leído: - **SC-004**: El ensayo aislado finaliza y puede repetirse con recursos propios, con datos/procesos habituales y evidencias anteriores intactos; pruebas pertinentes y global si cambia código compartido.

## 012/FR-001 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 29. Contexto: ## Requirements.

Requisito leído: - **FR-001**: Explicar qué/porqué/cómo según duda concreta, con ejemplo pertinente después de explicación y pregunta de comprensión no calificadora cuando corresponda.

## 012/FR-002 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 30. Contexto: ## Requirements.

Requisito leído: - **FR-002**: Mantener referente, objetivo/pregunta pendiente/transición; variar estrategia ante incomprensión y responder a errores/rectificaciones sin evaluar capacidad.

## 012/FR-003 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 31. Contexto: ## Requirements.

Requisito leído: - **FR-003**: Atender saludo compuesto y aclarar ambigüedad concreta; orientación/fuentes/controles comprensibles sin pantalla. Texto solo acredita lógica; voz requiere prueba separada.

## 012/FR-004 — sustituir mecanismo

Familia: N03. Necesidad: cobertura necesaria con selección experimental limitada.

Motivo: Mantener selección docente y un formato por documento; tresPDF son selección experimental de cobertura, no restricción de autorización a solo esos temas. Activar otras diapositivas ya autorizadas con versión y política sin reautorizar la asignatura.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 32. Contexto: ## Requirements.

Requisito leído: - **FR-004**: Fundamentar en PDF docente autorizado, un formato por documento; permitir Requisitos/Procedimiento/Testing según objetivos, con páginas originales, incidentes y versiones; excluir datos personales/evaluación histórica y alumnos.

## 012/FR-005 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Procedencia, autoridad independiente, privacidad y recursos propios son garantías necesarias; no se obtiene permiso declarando confiable el texto del modelo.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 33. Contexto: ## Requirements.

Requisito leído: - **FR-005**: Distinguir citas/paráfrasis/ejemplos didácticos derivados y sus testigos de fuente. No confiar en la salida del generador como evidencia ni atribuir revisión docente a validación técnica.

## 012/FR-006 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Procedencia, autoridad independiente, privacidad y recursos propios son garantías necesarias; no se obtiene permiso declarando confiable el texto del modelo.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 34. Contexto: ## Requirements.

Requisito leído: - **FR-006**: Conservar T090/T150, consentimiento/retención/privacidad, acceso y sesiones. No publicar texto libre mediante ranura confiable inventada ni debilitar verificador para pasar caso.

## 012/FR-007 — sustituir mecanismo

Familia: N15. Necesidad: mecanismo experimental sustituible.

Motivo: Conservar generación local y presupuesto; investigar representación finita no es un fin permanente ni autoriza otra escalera de modelos sin hipótesis.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 35. Contexto: ## Requirements.

Requisito leído: - **FR-007**: Investigar capacidad finita/determinista frente a transferencia; implementar capacidad generativa local y puertas si se necesita, usando recursos realmente instalados sin descargas ni nube. Generador propone, no autoriza.

## 012/FR-008 — decisión pendiente

Familia: N14. Necesidad: decisión material de publicación y aceptación.

Motivo: Mantener gate y revisión; definir contrato generativo y suficiencia empírica sin promesa universal. Revisar las tres ejecuciones según variabilidad y cobertura sin rebajar condiciones vigentes automáticamente.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 36. Contexto: ## Requirements.

Requisito leído: - **FR-008**: Publicación generativa requiere G2 explícito: contrato/verificación de afirmaciones, proveedor real, tres ejecuciones por caso y revisión independiente. G3/G4 y gates históricos no se infieren. Fallo de gate conserva perfil no disponible y evidencia de candidata separada.

## 012/FR-009 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar exposición de bancos, primer fallo, informe honesto y calidad; reducir snapshots y corridas repetidas, y permitir diagnóstico independiente sin inventar continuidad conversacional.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 37. Contexto: ## Requirements.

Requisito leído: - **FR-009**: Congelar nuevas conversaciones/oráculos antes de ajustar; preservar primeras divergencias, marcar reserva expuesta, continuar según salidas reales y no simular éxitos.

## 012/FR-010 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Procedencia, autoridad independiente, privacidad y recursos propios son garantías necesarias; no se obtiene permiso declarando confiable el texto del modelo.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 38. Contexto: ## Requirements.

Requisito leído: - **FR-010**: Entorno propio utilizable, aislamiento de recursos/procesos/credenciales, operación única, cierre/cancelación y comando claro; no Reset/commits ni activación de material habitual.

## 012/FR-011 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar exposición de bancos, primer fallo, informe honesto y calidad; reducir snapshots y corridas repetidas, y permitir diagnóstico independiente sin inventar continuidad conversacional.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 39. Contexto: ## Requirements.

Requisito leído: - **FR-011**: Entregar transcriptos completos manejables, tabla tarea→evidencia, archivos, comandos/resultados exactos y límites. Preservar011 y paquetes anteriores, T061/T067 abiertos.

## 012/FR-012 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar exposición de bancos, primer fallo, informe honesto y calidad; reducir snapshots y corridas repetidas, y permitir diagnóstico independiente sin inventar continuidad conversacional.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 40. Contexto: ## Requirements.

Requisito leído: - **FR-012**: Regresiones proporcionadas/global si compartido, Black/Ruff estructural con multiplicidad contra baseline durable, paquetes experimentales nuevos cuando cambia manifiesto, sin hashes falsificados.

## 012/FR-013 — sustituir mecanismo

Familia: N03. Necesidad: prescripción documental revisable.

Motivo: Conservar significado, estructura y procedencia de unidades; no exigir bloques de tamaño ilimitado ni prohibir segmentación semántica trazable cuando mejora recuperación o presupuesto.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 41. Contexto: ## Requirements.

Requisito leído: - **FR-013**: En el laboratorio, recuperar evidencia desde todas las páginas docentes autorizadas **ya ingeridas**, no solo una página o línea preseleccionada. Conservar unidades completas de párrafo, lista y tabla, posiciones y procedencia original; enlazar continuidad entre páginas solo cuando esté justificada. Permitir varios pasajes complementarios y supuestos explícitos dentro de presupuesto, sin equiparar citas repetidas con verificación semántica ni afirmar cobertura de la asignatura completa.

## 012/FR-014 — decisión pendiente

Familia: N14. Necesidad: decisión material de publicación y aceptación.

Motivo: Mantener gate y revisión; definir contrato generativo y suficiencia empírica sin promesa universal. Revisar las tres ejecuciones según variabilidad y cobertura sin rebajar condiciones vigentes automáticamente.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 43. Contexto: ## Requirements.

Requisito leído: - **FR-014**: En el perfil conversacional, publicar afirmaciones académicas solo si una comprobación semántica independiente acredita apoyo en fuente docente activa y autorizada, pertinencia y cobertura; rechazo o incertidumbre bloquean la afirmación y producen límite o aclaración. Internet permanece desactivado en el MVP; una fase web requiere enmienda constitucional y permiso docente explícito, con política de fuentes y procedencia.

## 012/FR-015 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 44. Contexto: ## Requirements.

Requisito leído: - **FR-015**: La respuesta conversacional se genera a partir de pregunta, historial realmente mostrado y evidencia recuperada vigente mediante RAG. El modelo puede explicar y parafrasear, pero no aportar hechos académicos de memoria como si fueran recuperados. No sustituir el objetivo por respuestas de contenido predefinidas.

## 012/FR-016 — conservar para uso actual

Familia: N03. Necesidad: imprescindible para recuperación útil.

Motivo: Ampliar búsqueda local cuando pueda resolver insuficiencia, registrar lo entregado y expresar límites honestos es necesario; no obliga a una llamada inútil si la cobertura falta de forma conocida.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 45. Contexto: ## Requirements.

Requisito leído: - **FR-016**: Ante evidencia insuficiente o conflictiva, ampliar de forma acotada la búsqueda local en documentos autorizados y comprobar procedencia; si continúa insuficiente, pedir aclaración concreta o indicar el límite. La futura ruta web, solo con política y permiso válidos tras enmienda constitucional, entrará en el mismo flujo de recuperación, no eludirá grounding ni obedecerá instrucciones halladas en fuentes.

## 012/FR-017 — sustituir mecanismo

Familia: N02. Necesidad: resultado necesario con mecanismo flexible.

Motivo: Conservar alcance, preguntas mixtas y ruta operativa; un clasificador previo a toda búsqueda no es obligatorio para decidir antes de generar. La política docente decide y el vacío nunca excluye.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 46. Contexto: ## Requirements.

Requisito leído: - **FR-017**: Clasificar el alcance académico frente a temario o delimitación docente vigente antes de generar: distinguir dentro de alcance con evidencia, dentro de alcance con evidencia insuficiente, fuera de alcance confirmado e incierto. Solo un fuera de alcance confirmado permite decir cortésmente que el tema no forma parte de la asignatura y no necesita estudiarse para ella; no responderlo académicamente ni buscarlo en internet. La falta de pasajes, una cuarentena o un score bajo nunca prueban exclusión. En caso incierto pedir precisión sin afirmar que no necesita estudiarlo.

## 012/FR-018 — sustituir mecanismo

Familia: N02. Necesidad: resultado necesario con mecanismo flexible.

Motivo: Conservar alcance, preguntas mixtas y ruta operativa; un clasificador previo a toda búsqueda no es obligatorio para decidir antes de generar. La política docente decide y el vacío nunca excluye.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 47. Contexto: ## Requirements.

Requisito leído: - **FR-018**: En preguntas mixtas, tratar únicamente la parte dentro de alcance con evidencia y señalar la parte excluida; no confundir prerrequisitos o analogías para explicar un tema con exigencias adicionales de estudio. Saludos, fuentes, controles, aclaraciones y gestión de sesión conservan su ruta operativa.

## 012/FR-019 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 48. Contexto: ## Requirements.

Requisito leído: - **FR-019**: Presentar referencias legibles al documento o título, con página cuando sea útil; no exigir al modelo identificadores técnicos ni citas por frase como formato de conversación. El host puede construir la presentación desde la procedencia exacta. Si solo conoce los documentos entregados al generador, debe llamarlos «Fuentes consultadas», sin afirmar que verifican todo el texto. Conservar internamente unidades, versiones, hashes y trazas para revisar apoyo, pertinencia y cobertura; la atribución general no rebaja FR-014 ni valida ejemplos injustificados. La futura atribución web mediante título/enlace no habilita Internet durante sesiones.

## 012/FR-020 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 49. Contexto: ## Requirements.

Requisito leído: - **FR-020**: Atender al acto pedagógico actual; ante incomprensión cambiar la estrategia explicativa sin añadir hechos académicos ajenos a fuentes. Permitir ejemplos o propuestas coherentes con valores, requisitos y escenarios inventados cuando se presentan inequívocamente como hipotéticos; no exigir respaldo literal para sus datos ficticios ni enumerar cada detalle de modo burocrático. Fundamentar el principio académico y su interpretación; hacer claros los supuestos decisivos, la condición observable y el resultado esperado. Distinguir requisito propuesto, criterio de aceptación y viabilidad demostrada. No concluir coste, tiempo, exhaustividad, impacto o garantías sin premisas suficientes; pedir o proponer el contexto que falte sin invalidar una primera formulación del alumno.

## 012/SC-001 — conservar para uso actual

Familia: N01. Necesidad: imprescindible para el objetivo actual.

Motivo: Son el núcleo humano vigente: explicación y adaptación contextual, ficción coherente, referencias legibles y conversación completa. Mantener flexibilidad en ejemplo o pregunta cuando corresponda.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 57. Contexto: ## Success Criteria.

Requisito leído: - **SC-001**: Conversaciones reales nuevas (desarrollo y variante congelada) cubren saludo/pregunta, explicación, incomprensión repetida, ejemplo, error/rectificación y cambio de foco con oráculos independientes satisfactorios; no basta HTTP200 ni grounding aprobado.

## 012/SC-002 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Procedencia, autoridad independiente, privacidad y recursos propios son garantías necesarias; no se obtiene permiso declarando confiable el texto del modelo.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 58. Contexto: ## Success Criteria.

Requisito leído: - **SC-002**: Cero afirmaciones publicadas sin procedencia permitida, cero ejemplos atribuidos literalmente a fuente y cero publicación con gate fallido. Mantener evidencia separada de candidatas rechazadas.

## 012/SC-003 — conservar por seguridad

Familia: N05. Necesidad: seguridad y permiso.

Motivo: Procedencia, autoridad independiente, privacidad y recursos propios son garantías necesarias; no se obtiene permiso declarando confiable el texto del modelo.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 59. Contexto: ## Success Criteria.

Requisito leído: - **SC-003**: Repetición/cierre/cancelación propios, sin cambios en originales/entornos históricos ni procesos ajenos; recursos preparados y parada propia.

## 012/SC-004 — sustituir mecanismo

Familia: N12. Necesidad: proceso necesario consolidable.

Motivo: Conservar exposición de bancos, primer fallo, informe honesto y calidad; reducir snapshots y corridas repetidas, y permitir diagnóstico independiente sin inventar continuidad conversacional.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 60. Contexto: ## Success Criteria.

Requisito leído: - **SC-004**: Informe separa cumplimiento técnico, capacidad efectiva y aceptación/voz humana pendientes; gates fallidos son trabajo pendiente y no éxito didáctico.

## 012/SC-005 — sustituir mecanismo

Familia: N03. Necesidad: prescripción documental revisable.

Motivo: Conservar significado, estructura y procedencia de unidades; no exigir bloques de tamaño ilimitado ni prohibir segmentación semántica trazable cuando mejora recuperación o presupuesto.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 61. Contexto: ## Success Criteria.

Requisito leído: - **SC-005**: Pruebas deterministas demuestran unidades sin cortes físicos, procedencia exacta, continuidad justificada, recuperación multi-fuente con vecinos, presupuesto y discrepancias conservadas; una revisión por conjuntos puede registrar varios pasajes/premisas sin otorgar aprobación semántica ni publicación. La utilidad conversacional sigue sometida a SC-001/G2 y revisión humana.

## 012/SC-006 — decisión pendiente

Familia: N14. Necesidad: decisión material de publicación y aceptación.

Motivo: Mantener gate y revisión; definir contrato generativo y suficiencia empírica sin promesa universal. Revisar las tres ejecuciones según variabilidad y cobertura sin rebajar condiciones vigentes automáticamente.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 63. Contexto: ## Success Criteria.

Requisito leído: - **SC-006**: Ningún caso negativo congelado de contradicción compatible, premisa ausente, fuente retirada, respuesta parcial o inyección obtiene permiso falso; sin evaluador calibrado no se abre G2.

## 012/SC-007 — conservar para uso actual

Familia: N03. Necesidad: imprescindible para recuperación útil.

Motivo: Ampliar búsqueda local cuando pueda resolver insuficiencia, registrar lo entregado y expresar límites honestos es necesario; no obliga a una llamada inútil si la cobertura falta de forma conocida.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 64. Contexto: ## Success Criteria.

Requisito leído: - **SC-007**: El laboratorio conserva trazas de recuperación inicial y ampliación local acotada, evidencia entregada al generador, respuesta completa y revisión separada de procedencia, apoyo, cobertura y continuidad. Insuficiencia persistente o conflicto no termina en afirmación académica inventada; los controles positivos también miden cobertura y rechazos falsos.

## 012/SC-008 — sustituir mecanismo

Familia: N02. Necesidad: resultado necesario con mecanismo flexible.

Motivo: Conservar alcance, preguntas mixtas y ruta operativa; un clasificador previo a toda búsqueda no es obligatorio para decidir antes de generar. La política docente decide y el vacío nunca excluye.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 65. Contexto: ## Success Criteria.

Requisito leído: - **SC-008**: Casos positivos y negativos de frontera, recuperación vacía, fuente retirada/cuarentena, pregunta mixta, referente elíptico y controles operativos demuestran que solo una autoridad de alcance explícita habilita el aviso «no necesitas estudiarlo»; los demás casos no amplían temario ni inventan respuesta.

## 012/SC001 — fusionar obligación equivalente

Familia: N12. Necesidad: alias redundante del registro.

Motivo: Es una referencia no normalizada al SC-001 dentro de una decisión de estado, no otra obligación formal. Mantener su procedencia y unificar el identificador sin sumar un requisito o un éxito adicional.

Fuente: [specs/012-conversational-course-study/spec.md](../../../specs/012-conversational-course-study/spec.md), línea 78. Contexto: NO FORMAL BULLET; previous register excerpt.

Requisito leído: - La política de alcance v1 de esta actividad referencia cuatro PDF docentes; alcance aprobado no significa respuestas aprobadas. Los ensayos Qwen/Mistral son diagnósticos incompatibles para ranking y no abren G2/SC001. Reserva intacta, perfil participante cerrado.
