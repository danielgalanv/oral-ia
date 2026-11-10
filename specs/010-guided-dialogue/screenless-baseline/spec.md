# Feature Specification: Conversación guiada y recuperación del diálogo

**Feature Branch**: sin Git; identificador `010-guided-dialogue`
**Created**: 2026-10-18
**Status**: Implementación parcial; G0/G1 completos todavía pendientes
**Input**: Analizar pruebas reales de autoestudio y defensa, preparar actuación completa alineada con ORALIA y anticipar complicaciones/mejoras.

## Objetivo y contexto

ORALIA debe ayudar a consultar, explicar y practicar con materiales docentes autorizados, y a ensayar explicaciones mediante preguntas relacionadas. La arquitectura multiagente es un medio de control y trazabilidad, no el resultado educativo por sí misma. La prueba real mostró continuidad insuficiente, extracción repetitiva y fallback sin salida en ambos modos. Esta feature corrige escenarios ya previstos en 003/004 y añade criterios de aceptación conversacional ausentes; no convierte el sistema en un chat general ni en un evaluador.

Fuente: [hallazgos](../../docs/HALLAZGOS-PRUEBA-USUARIO.md). No se incorporan identidades ni transcripciones completas sin consentimiento. La implementación fue autorizada expresamente por el usuario el 18-10-2026 y transmitida por el chat auditor. No se autorizan descargas de modelos ni alteración de sesiones personales activas. Los artefactos iniciales describen planificación; la evidencia ejecutada se registra por separado.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Conversar sin perder el tema (Priority: P1)

Recibir orientación y pedir repetir, reformular o un ejemplo sin reiniciar mentalmente la conversación.

**Why this priority**: bloquea el uso real observado o su validación; no es un retoque cosmético.
**Independent Test**: La secuencia de autoestudio observada, incluida «dímelo», progresa hacia una explicación o una aclaración concreta.

**Acceptance Scenarios**:

1. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Ante saludo, el sistema orienta con el tema real y una opción de consulta, sin recuperar literalmente el saludo como contenido.
2. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Tras pregunta sobre ebullición y una petición de vapor, «dímelo» se refiere al objetivo vigente si es único; después de dos referentes posibles pide selección.
3. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** «No repitas; dame otro ejemplo» elige ejemplo, conserva el tema y no reproduce la misma salida.
4. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Una petición autorizada de repetir conserva exactamente la pregunta, sin activar un bloqueo de repetición no solicitada.

---

### User Story 2 - Ensayar una defensa con apoyo y sin evaluación (Priority: P1)

Responder, reconocer que no se sabe justificar y pedir orientación o reformulación sin recibir notas ni entrar en un bucle.

**Why this priority**: bloquea el uso real observado o su validación; no es un retoque cosmético.
**Independent Test**: La secuencia 99 grados → no sé → y ahora → repetir → otra forma mantiene pregunta y opciones útiles.

**Acceptance Scenarios**:

1. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Ante 99 frente a fuente con 100, pregunta neutral sobre la discrepancia y las condiciones documentadas, sin cambiar silenciosamente la respuesta atribuida al usuario.
2. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** «No sé justificarlo» ofrece una pista o paso siguiente permitido, sin revelar la solución si está prohibida.
3. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** «Puedes repetir» repite la pregunta vigente y «otra forma» reformula sin introducir una pregunta distinta ni otro tema.
4. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Tras dos fallos de progreso, presenta opciones de orientación/otro tema/finalizar; elegir una realmente cambia la acción.

---

### User Story 3 - Estudiar con contenido suficiente y capacidades honestas (Priority: P1)

Trabajar con materiales desarrollados y estrategias explicativas verificables, sabiendo qué puede hacer el proveedor activo.

**Why this priority**: bloquea el uso real observado o su validación; no es un retoque cosmético.
**Independent Test**: Dos dominios distintos permiten explicación, ejemplo, comparación y práctica sin respuestas preparadas específicas del agua.

**Acceptance Scenarios**:

1. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Material con explicación y ejemplo autorizados permite solicitudes equivalentes y seguimiento, no solo copiar dos frases.
2. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Material breve sin ejemplos produce límite concreto y alternativas; no se anuncia una explicación generativa inexistente.
3. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Cada propuesta paraprástica o compuesta tiene autorización explícita y fuentes; si no se puede verificar, se bloquea o cambia a una estrategia autorizada.
4. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Caída del modelo muestra degradación y capacidades restantes; las pruebas con dobles no se contabilizan como inferencia real.

---

### User Story 4 - Entrar y continuar sin intervención del mantenedor (Priority: P1)

Elegir actividad y código válido, entender la modalidad y recuperarse de incidencias desde la interfaz.

**Why this priority**: bloquea el uso real observado o su validación; no es un retoque cosmético.
**Independent Test**: Usuario nuevo completa ambos modos desde PowerShell normal sin credenciales en demo, SQL ni Reset.

**Acceptance Scenarios**:

1. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Destinatario no permitido produce mensaje previo al inicio sin tomar el bloqueo de sesión; no se modifica la política para aceptarlo.
2. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Sesión ocupada permite localizar la pestaña propia o solicitar cierre autorizado con confirmación, sin cerrar a otra persona por defecto.
3. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Sin voz, se explica que la pregunta es escrita y se mantiene visible y habilitado el campo de respuesta mientras la sesión esté activa.
4. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Doble clic y reconexión no duplican turnos; cierre seguro informa causa recuperable y cómo iniciar de nuevo.

---

### User Story 5 - Comprobar utilidad conversacional y conservar límites (Priority: P1)

Revisar evidencia de diálogos variados y límites de seguridad antes de anunciar que la herramienta está lista.

**Why this priority**: bloquea el uso real observado o su validación; no es un retoque cosmético.
**Independent Test**: Corpus reservado, navegador y fallos pasan por perfil; privacidad y calidad se reportan por separado.

**Acceptance Scenarios**:

1. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Los diálogos históricos se reproducen con sus formulaciones originales y variantes sin inyectar respuestas favorables al generador.
2. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** El conjunto reservado cambia orden, dominio y referentes; se publica cada caso fallido y el criterio incumplido.
3. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Contexto nuevo se borra y exporta por scope; una sesión o reinicio no hereda preguntas de otra.
4. **Given** actividad autorizada y el contexto descrito, **When** ocurre la entrada del escenario, **Then** Informe diferencia infraestructura, calidad conversacional y evaluación humana pendiente; un perfil generativo local no se aprueba por reserva extractiva.


### Edge Cases

Referencia sin antecedente o con dos; tema cambiado seguido de repetir; frases negativas y mixtas; números con unidades/aproximación; material revocado entre mostrar y repetir; pregunta fuera de temario; pistas que filtran una solución; fuente que incluye instrucciones maliciosas; salida repetida de modelo; proveedor que cambia a reserva; error de carga sin confirmación; respuesta tardía tras cierre; duplicados desde dos pestañas; reinicio sin token; actividad retirada; presupuesto agotado durante ayuda; privacidad de memoria auxiliar. Matriz normativa en [acceptance-matrix.md](acceptance-matrix.md).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST preservar la finalidad de apoyo al estudio y ensayo: no asignar notas, diagnosticar capacidad, sustituir al docente ni construir perfiles longitudinales.
- **FR-002**: El sistema MUST distinguir saludo, consulta o respuesta temática, repetir, reformular, ayuda/no sé, continuar, ejemplo, comparación, cambio de tema/modo, finalizar y entrada ambigua; expresar incertidumbre y separar acto conversacional de modo de estudio.
- **FR-003**: El sistema MUST mantener tema y pregunta pendientes a través de órdenes de control y resolver referencias breves solo cuando exista un referente inequívoco, sin sustituirlo por la última palabra recibida.
- **FR-004**: El sistema MUST ante dos referentes plausibles o instrucciones incompatibles, pedir una aclaración concreta con opciones autorizadas y continuar tras la selección; una negación como «no repitas» no debe disparar repetir.
- **FR-005**: El sistema MUST orientar ante un saludo y una consulta general dentro del tema con alcance, opciones y un siguiente paso; no alegar ausencia de información si hay material pertinente disponible sin comprobarlo.
- **FR-006**: El sistema MUST repetir la pregunta o salida solicitada fielmente, identificando cuál se repite y comprobando que sigue autorizada; no generar otra pregunta ni tratar la petición como respuesta al contenido.
- **FR-007**: El sistema MUST reformular sobre el mismo objetivo y ofrecer ejemplos/comparaciones diferentes cuando haya contenido autorizado para ello; si no existe, explicar el límite y ofrecer una alternativa concreta, sin anunciar una reformulación que solo repite.
- **FR-008**: El sistema MUST responder a «no sé», ayuda o bloqueo con una pista o paso siguiente pertinente; respetar la política docente de no revelar solución, incluida la revelación indirecta por pistas, ejemplos, resumen y panel de fuentes.
- **FR-009**: El sistema MUST cambiar de tema o pregunta únicamente dentro de la actividad, conservando la pregunta actual hasta confirmar la transición y presentando un único objetivo principal por intervención.
- **FR-010**: El sistema MUST en defensa, relacionar cada repregunta con una afirmación identificable de la respuesta y su fuente u objetivo; no usar partículas, números aislados o verbos de control como conceptos temáticos sin contexto.
- **FR-011**: El sistema MUST abordar diferencias entre lo dicho y una fuente de manera neutral: mantener ambas afirmaciones distintas, explicitar condiciones/unidades si están documentadas y pedir justificación o aclaración sin calificar; no asumir que 99/100 es siempre contradicción.
- **FR-012**: El sistema MUST en autoestudio, cubrir duda, explicación guiada, práctica, exposición y revisión según modos habilitados; no convertir toda entrada en duda ni responder a tareas prohibidas por el perfil.
- **FR-013**: El sistema MUST prevenir bucles: tras una primera salida estancada cambiar estrategia; al segundo intento consecutivo sin avance ofrecer opciones distintas y ejecutables. No emitir dos avisos genéricos idénticos consecutivos por falta de progreso; avance significa cambio observable de acción, subobjetivo o evidencia, no aprendizaje inferido.
- **FR-014**: El sistema MUST resolver recuperación con la pregunta original y el contexto temático autorizado, manteniendo separados texto literal y consulta contextual; revalidar material, versión, destinatario y alcance en cada uso o repetición.
- **FR-015**: El sistema MUST reconocer materiales insuficientes, conflictos o revocaciones entre turnos; no resolverlos por invención ni reutilizar contenido revocado desde memoria; señalar qué falta y qué sí puede hacerse.
- **FR-016**: El sistema MUST presentar explicaciones y prácticas con fuentes suficientes, distinguiendo hechos del material, ejemplos docentes revisados e incertidumbre; una respuesta superficial o un aviso autorizado no prueba utilidad del diálogo.
- **FR-017**: El sistema MUST autorizar cada salida y cada transformación mediante una propuesta estructurada verificable; no convertir texto generado, un hash propio o similitud léxica en permiso de publicación.
- **FR-018**: El sistema MUST mantener independencia entre interpretación, decisión, recuperación, generación y verificación; no eliminar controles de fundamentación, coherencia, no revelación o autorización para obtener respuestas más fluidas.
- **FR-019**: El sistema MUST mostrar capacidades y proveedor efectivos antes y durante uso: guiado controlado, extractivo limitado, generativo local validado o degradado. Cambiar a reserva requiere aviso; ausencia de un modelo nunca cuenta como prueba de generación real.
- **FR-020**: El sistema MUST disponer de materiales docentes desarrollados, versionados y editables en al menos dos dominios; declarar qué explicaciones, ejemplos, contrastes y pistas están cubiertos. El material de dos frases se conserva como prueba de insuficiencia, no como demostración completa.
- **FR-021**: El sistema MUST detectar código destinatario incompatible y actividad no utilizable antes de crear una sesión o consumir su bloqueo; ofrecer corrección sin ampliar permisos ni sustituir silenciosamente la identidad elegida. La demo puede proponer demo-007 explícitamente.
- **FR-022**: El sistema MUST ante sesión ocupada o acceso perdido, ofrecer vuelta a la sesión si se conserva la autorización o cierre administrativo explícito con confirmación y política vigente; nunca cerrar sesiones ajenas automáticamente, recuperar identidad por código ni requerir edición SQL/Reset para continuar.
- **FR-023**: El sistema MUST mostrar modalidad efectiva, pregunta, entrada textual y fuentes encontrables por teclado, además de ocupado/error; ausencia de voz no puede parecer un fallo del texto. No prometer audio sin disponibilidad comprobada.
- **FR-024**: El sistema MUST manejar doble envío, cancelación, respuesta tardía, desconexión y reintento sin duplicar turnos, avanzar pregunta indebidamente ni resucitar datos cerrados; informar si el resultado es desconocido y reconciliar antes de reenviar.
- **FR-025**: El sistema MUST mantener presupuestos finitos por turno y sesión, incluidos repetir, reformular y recuperaciones; advertir de límites y aplicar cierre ganador único. Los controles de interfaz no eluden duración ni recursos.
- **FR-026**: El sistema MUST someter contexto, memoria auxiliar, corpus de pruebas e informes a minimización, consentimiento, scopes, caducidad, borrado y aislamiento; no volcar conversaciones personales ni razonamiento privado en los artefactos del plan o logs.
- **FR-027**: El sistema MUST versionar políticas, contratos, estado y actividades modificados; conservar sesiones antiguas y generar sucesoras para demo/materiales/perfiles nuevos sin Reset, migración silenciosa o relajación de autenticación normal.
- **FR-028**: El sistema MUST registrar intención, referente, decisión, estrategia de recuperación, evidencia, verificaciones, proveedor, tiempos y resultado estructural; no persistir candidatos rechazados ni presentar confianza heurística como certeza.
- **FR-029**: El sistema MUST validar secuencias completas de usuario, variantes y combinaciones no usadas para ajustar la implementación, en dos dominios y con generadores/proveedores reales del perfil anunciado; distinguir dobles de contrato de evidencia conversacional.
- **FR-030**: El sistema MUST separar aprobación técnica, aceptación de diálogo y evaluación humana. No declarar herramienta conversacional útil solo por totales de tests; publicar fallos, denominadores y capacidades pendientes por perfil.
- **FR-031**: El sistema MUST verificar instalación/arranque y recuperación desde PowerShell normal además del entorno del agente, cargas lentas y recursos ausentes sin dependencias ocultas ni cambios de PATH permanentes.
- **FR-032**: El sistema MUST entregar migraciones y retorno a versión anterior documentados, evidencia reproducible y extensión futura de modelo/voz/materiales mediante contratos, sin implementar nube, SSO, concurrencia múltiple o funciones excluidas de la constitución.

- **FR-033**: El sistema MUST disponer de conversaciones sintéticas reproducibles que ejerciten herramientas y operaciones públicas de ORALIA con roles, argumentos, efectos y resultados esperados, caminos normales, llamadas prohibidas, fallos y recuperación; servicios reales del perfil y datos temporales aislados, sin conceder permisos docentes al participante ni sustituir resultados por respuestas favorables. Protocolo en synthetic-tool-conversations.md.

### Key Entities

- **Acto conversacional**: lo que solicita la intervención, referente y alternativas si es ambiguo; distinto del modo.
- **Contexto de diálogo**: tema, objetivo y pregunta pendientes, última salida autorizada, referencias de material y recuperación acotada de esta sesión.
- **Acción de apoyo**: repetir, reformular, orientar, dar pista, avanzar o aclarar, con propósito observable y restricciones.
- **Unidad docente**: contenido revisado, rol pedagógico, prerrequisitos, relaciones y fuentes versionadas; no perfil del estudiante.
- **Perfil de capacidad**: proveedor configurado y efectivo, acciones soportadas, disponibilidad y límites.
- **Registro de aceptación**: caso, propiedades esperadas, resultados, evidencias y limitaciones; nunca calificación del participante.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Las dos secuencias observadas completas y sus variantes pasan todas sus aserciones obligatorias de intención, continuidad y siguiente acción en ambos modos del perfil guiado controlado; el perfil extractivo se evalúa con sus límites declarados. Los resultados se publican por caso, sin ocultar fallos con medias.
- **SC-002**: En un conjunto de 48 entradas de aceptación no usadas para ajustar reglas, al menos 44 reciben el acto/referente esperado; las 48 respetan permisos, y todos los casos ambiguos o negativos críticos deben aclarar o rechazar correctamente.
- **SC-003**: En 24 diálogos de 6–12 intervenciones (12 de desarrollo y 12 reservados, repartidos entre dos dominios y ambos modos), no hay avisos genéricos idénticos consecutivos y todo bloqueo recuperable ofrece y ejecuta una opción válida en las dos intervenciones siguientes.
- **SC-004**: El 100% de las respuestas de contenido entregadas en el corpus enlazan evidencia vigente y los controles obligatorios; cero publicaciones no autorizadas, notas, revelaciones de solución prohibidas o fugas de sesión en las matrices negativas.
- **SC-005**: Los cinco modos habilitables de autoestudio y las acciones repetir/reformular/ayuda/siguiente de defensa tienen al menos un diálogo completo de aceptación por modo/acción y controles negativos para modos deshabilitados.
- **SC-006**: El 100% de escenarios operativos prioritarios (destinatario incorrecto, sesión ocupada, acceso perdido, sin audio, carga lenta y envío duplicado) permite recuperarse o terminar explícitamente sin Reset, intervención SQL ni cierre de una sesión ajena.
- **SC-007**: Cada ejecución publica perfil/modelo, material, versión, semilla si aplica, entorno y tiempos medidos; decisiones de los casos deterministas se reproducen y una generación local no determinista se evalúa por propiedades en tres ejecuciones por caso, sin afirmar identidad textual.
- **SC-008**: La entrega distingue de manera visible puertas técnicas y conversacionales aprobadas y la utilidad humana aún no medida; explica limitaciones, costes y recuperación en una guía ejecutable por alguien distinto del implementador.

- **SC-009**: Los 16 escenarios sintéticos adicionales de herramientas (8 de desarrollo y 8 reservados) pasan todas sus propiedades obligatorias de llamada, argumentos, estado y respuesta; cero operaciones no autorizadas, duplicados, fugas o resurrección de datos. Resultados por familia distinguen fallos inyectados de recorridos normales.

## Assumptions

- Se conserva ejecución local, una sesión interactiva y texto completo; no se cambia la constitución ni se vuelve obligatoria la voz.
- Perfil objetivo inicial: diálogo guiado con contenido docente estructurado y revisado. El extractivo breve sigue disponible como perfil limitado; no acredita explicación abierta.
- Evaluar generación local real y su autorización es obligatorio como estudio de viabilidad; habilitar paráfrasis abierta en producción es un gate separado y condicionado a verificación suficiente. Si no pasa, informar límite y no marcar esa capacidad como disponible.
- El docente publica nuevas versiones de contenido/perfiles; las actividades demo existentes no cambian de contrato en silencio.
- Los números de aceptación son objetivos de prueba de este diseño, no resultados obtenidos, promesas universales o medidas de aprendizaje.

## Clarifications

### Sesión 2026-10-18

Se resolvió desde decisiones existentes y evidencia: finalidad de apoyo, no evaluación; local/texto; conservación vigente; una sesión; sin nube/SSO; modelos solo explícitos. No se requiere preguntar al usuario por elecciones rutinarias. No se elige todavía una marca/tamaño de modelo sin pruebas de calidad y recursos. La decisión arquitectónica controlado primero y evaluación generativa aislada está documentada en research.md; no se pide aprobar ni se declara segura una autorización de texto libre.

## Fuera de alcance

Voz real nueva, redes institucionales, nube, SSO, notas/rúbricas autónomas, memoria longitudinal, múltiples sesiones simultáneas, optimización autónoma y demostración de aprendizaje humano. Su posible evolución se recoge como seguimiento separado, no trabajo obligatorio encubierto.

