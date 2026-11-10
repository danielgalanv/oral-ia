# Contrato de diálogo v2 — diseño 010

## Entrada de interpretación

session_id, turn_id, raw_text, mode, enabled_modes y ContextView validado. Las fuentes,
la pregunta previa y la respuesta del participante son datos, nunca instrucciones.
El agente no consulta sesiones por código ni decide políticas.

## Salida

schema_version=2; primary_act enum:
greeting/content_question/content_answer/repeat/rephrase/help/continue/example/
comparison/topic_switch/mode_switch/finish/ambiguous.
confidence_kind=heuristic|calibrated|not_applicable; reason_code cerrado;
referent_candidate_refs hasta4; requested_topic/mode opcionales; negated_acts;
needs_clarification bool. El agente no puede conceder autorización.

Identidad del agente existente con versión de contrato v2; el adaptador v1 conserva
sus campos y errores. Precondición: sesión activa, configuración versionada y contexto
validado. Postcondición: exactamente un acto principal o ambiguous, sin mutación ni
publicación. Herramientas permitidas: ninguna adicional; solo las del contrato vigente.
Deadline, memoria, llamadas y cancelación heredan el máximo existente congelado en T004;
cualquier cambio exige política manual versionada y aceptación de recursos. Errores
tipados: invalid_input, stale_context, deadline_exceeded, cancelled y unavailable.
Éxito: estructura válida y acto/referente conforme al oráculo; no éxito por texto plausible.
Traza: versión, entrada referenciada según scope, razón cerrada, duración y resultado.
Cancelación no aplica patches. Ningún agente accede a detalles privados de otro.

## Tabla de decisión de la política

| Acto/contexto | Recuperación | Acción |
|---|---|---|
| greeting | temario publicado, sin buscar «hola» | orientación con opciones válidas |
| content_question amplia | tema/objetivo + texto, restricciones del curso | explicar o falta concreta |
| repeat con ancla única | revalidar referencia y permiso actual | repetir fielmente objetivo actual |
| rephrase con ancla | evidencia/unidad del mismo subobjetivo | alternativa revisada; no respuesta a pregunta distinta |
| help/no sé | pregunta pendiente y support_step | pista permitida o opción segura |
| continue | siguiente paso del plan actual | avanzar o preguntar qué continuar si ambiguo |
| example/comparison | unidades revisadas relacionadas | ejemplo/contraste o explicar qué falta |
| topic_switch | temario elegido, invalidar ancla previa | nueva pregunta única |
| ambiguous | no búsqueda arbitraria | aclaración con hasta4 opciones |
| finish | cierre existente | T150, resumen si autorizado y privacidad |

El servicio decide si requiere nueva evidencia; aun al reutilizar se revalida vigencia.
Contrato HTTP: adición optativa dialogue_control al request y dialogue_status al response;
texto y botones comparten acción, no dos políticas independientes. Campos desconocidos
se rechazan. La ruta legacy conserva su semántica; la actividad versionada elige perfil.

## Presupuestos e idempotencia

Una orden enviada al backend que genera respuesta se registra y consume turno según el
contrato actual; repetición local del texto ya visible es presentación sin avance y sin
llamada de modelo. Ambas respetan duración, cierre y material retirado: el botón local
no debe prometer volver a divulgar material cuya autorización de visualización expiró.
Sin streaming de texto no aprobado. Máximo una recuperación alternativa por turno y
una generación alternativa dentro del presupuesto restante; al agotarse, opciones
autorizadas, nunca while indefinido. Suma de pasos <= deadline global del turno.

client_request_id optativo para legacy y obligatorio en UI v2; mismo ID/payload = mismo
turno proyectado, otro payload =409. Cierre gana una sola vez; timeout se reconcilia con
recibo. Si el cliente no conserva owner token tras reinicio, no se le devuelve contenido.

## Recuperación de sesión y acceso

Preflight 409 con code cerrado recipient_not_allowed/activity_unavailable sin adquirir
lock. Si hay otra sesión: interactive_session_active, enlaces de recuperación solo si
propietario ya autenticado; no revelar su contenido. Cierre docente explícito usa rol
normal o grant demo local dentro de su aislamiento, confirmación y comandos existentes.
Sin recuperación por participant_code ni edición SQL. Ninguna ruta permite cambiar
consentimiento por mera recuperación.

## Verificadores v2 integrados — 19-10-2026

La selección de `guided_controlled` es explícita por versión de actividad. El puerto
`GuidedGenerationPort.render(DialogueGenerationRequest)` recibe únicamente referencias
y devuelve snapshot/propuesta; nunca una aprobación. El adaptador rechaza sesión ajena,
turno fuera de `in_progress` y `base_version` obsoleto. El presupuesto controlado es
10 000 ms por turno; cada agente recibe el mínimo de su timeout, tiempo restante del
turno y duración restante de sesión. No se invoca otro agente cuando no queda tiempo.

Coherencia v2 exceptúa únicamente una repetición exacta solicitada; siguen vigentes los
controles de contradicción. Fundamentación v2 verifica todas las cláusulas, separando
conjunciones con distinta polaridad; una contradicción bloquea y una cláusula sin apoyo
impide aprobar. Los contratos y resultados de los verificadores v1 permanecen vigentes.

## Transporte de identidad implementado

`client_request_id: UUID` es optativo en los POST de texto legacy y se envía siempre
desde la UI actual de autoestudio/defensa. Misma sesión/ID/payload produce el mismo
`turn_id`; payload distinto devuelve 409 antes de modificar consentimiento. El recibo
y el turno se confirman en una sola transacción. Fallo/cancelación revierte ambos.
El cierre que elimina transcript elimina también el recibo, incluso si ese mismo turno
lo creó; completar una operación no puede recrearlo después de la purga.

GET `/sessions/{session_id}/requests/{request_id}` requiere el grant propietario de esa
sesión y devuelve solo ID/estado/turno. Un 404 no autoriza ejecutar de nuevo. Ante pérdida
de transporte o 5xx, la UI bloquea nuevos envíos y permite consultar el resultado; solo
tras recibo `completed` vuelve a proyectar el mismo envío. No persiste texto ni secretos
en URL, localStorage o recibos. La proyección no es una copia histórica: revalida el
plan docente actual y T090; puede devolver `replay_content_withheld=true` si no existe
contenido reconstruible autorizado. No reproduce fuentes, resumen ni audio cacheados.

Las operaciones de texto/cierre adquieren una exclusión asíncrona antes de abrir la
transacción y la liberan después del commit/rollback de alcance función. La fila de
sesión y unicidad del recibo siguen protegiendo los efectos persistidos. La espera de
la exclusión es finita (10 s); no bloquea el event loop mientras otro turno espera un
agente. El estado aditivo `closed_teacher_confirmed` no altera los estados históricos.

La pregunta pendiente visible se proyecta por referencia desde su turno originalmente
aprobado y vuelve a pasar por renderer/T090 con fuentes vigentes; no procede de una
caché de texto del navegador. Al recuperar sesión no se emite otro turno ni token.

## Non-disclosure v2

La rama guiada envía `internal_expected_answers` como lista acotada de unidades
publicadas del mismo objetivo. El verificador independiente compara cada cláusula
individual, sin diluir una solución breve concatenándola con otros ejemplos. Bloquea
también anclas numéricas compartidas con la solución en el perfil protegido. Lista
ausente, vacía o inválida produce error y no aprobación. Solo devuelve veredicto y
score técnico; las soluciones no se persisten como trazas ni se devuelven al cliente.

El negativo público con una pista deliberadamente mal etiquetada descubrió y probó
la dilución inicial; su primer fallo se conserva en el registro de validación. Los
dos modos bloquean ahora esa publicación, incluyendo fuentes y propuestas persistidas.
Es un control léxico acotado de contenido revisado, no una prueba de comprensión
semántica general ni habilitación de G2. El contrato v1 conserva su score original.


## Foco solicitado en coherencia v2

Una petición explícita de ejemplo, comparación, ayuda o reformulación puede aislar una unidad revisada de una composición anterior más larga. La excepción de repetición exige coincidencia exacta entre propuesta, unidad seleccionada y fuente activa, y que sea subcadena estricta del turno previo. No permite repetir el turno entero ni evita comprobar contradicciones, grounding, no revelación o T090. Los campos los construye el compositor a partir de las unidades vigentes, nunca el cliente. Es continuidad estructural, no una afirmación de progreso educativo.


El resumen devuelto por la respuesta de cierre conserva su presentación efímera única del contrato previo, incluso sin scope de retención. No se guarda ni se reconstruye al recargar/recuperar; eliminación explícita limpia también esa vista. La transcripción/pregunta/contexto local se limpian al cierre efímero. Una lectura de privacidad no elimina retrospectivamente la presentación única que autoriza la respuesta de cierre.


## Repregunta y afirmación del participante

`claim_followup` es una referencia acotada al turno de entrada propietario, a la
pregunta original y a la reformulación docente vinculada por `relations.rephrases`,
con subobjetivo común y fragmentos vigentes. No copia el texto ni atribuye al
participante lo que afirma la fuente. `assessment` solo admite `not_assessed`.
La actualización transaccional comprueba sesión, turno aprobado, relación docente,
objetivo y fuentes; una referencia falsa se rechaza. Cambio de objetivo/pregunta o
retiro elimina el ancla activa y borrado de contenido limpia el contexto completo.

La pregunta revisada pide justificación/condiciones documentadas. 99 frente a 100,
aproximación o Fahrenheit frente a Celsius no se califican ni se declaran una
contradicción automática. Las soluciones siguen ocultas en defensa y la referencia
no concede permiso para mostrarlas. No hay comparador semántico libre ni calificación.


## Precisión semántica 19-10-2026

StudyIntentInterpreter dialogue_contract 2.1.2 añade repeat_target opcional cerrado (question, last_output, explanation, example, comparison, hint), solo para acto repeat. Distingue objeto nominal de orden coordinada; la cortesía no crea referentes y cero/varios referentes siguen requiriendo aclaración. Comparar no cambia por sí solo el objetivo. Coherencia v2 2.1.0 distingue sujetos/predicados conocidos con alcance de negación, mantiene contradicciones reales y conserva comprobaciones ante casos desconocidos; no constituye prueba semántica general. El componente repetido debe pertenecer a una unidad previamente autorizada y pasa los verificadores independientes y T090. practice_reveals_solution respeta configuración docente explícita; permiso de unidad revisada y permiso de revelar fragmentos originales son independientes. Sin cambio de contrato v1, migración adicional o habilitación G2.

## Contrato conversacional optativo

Publicar una actividad nueva con `guided_policy(recipient, screenless=True)`; el valor por defecto conserva la política anterior. La publicación exige todas las plantillas y reglas de metadatos de navegación. `screenless_text_ready` declara capacidad textual de la política, nunca validación humana o audio.

`POST /api/v1/sessions/{id}/conversation-controls` requiere el grant del propietario, incluso después del cierre. Texto acotado a 4000 caracteres; UUID de petición opcional solo durante sesión activa. Reutiliza las operaciones y recibos existentes. Tras cerrar, se rechaza ese UUID y se admiten revisión propia por número, estado y eliminación explícita; no crea turnos/contexto y respeta scope/caducidad. Un docente no obtiene privilegios de propietario por su rol.

Órdenes canónicas: «qué temas hay», «más opciones», «repetir opciones», «elijo condensación», «confirmo», «de dónde sale eso», «más fuentes», «ayuda», «qué modos hay». Se ofrecen como máximo tres temas actuales. «confirmo: salida» confirma únicamente un tema publicado inequívoco; nunca equivale a consentimiento. Las fuentes son título/sección/versión del turno propio aprobado, revalidadas ante retirada, sin recitar fragmentos prohibidos.

«conservar resumen y transcripción» propone una elección; «confirmo conservar resumen y transcripción» solo aplica esa elección pendiente permitida. «no conservar nada» requiere su confirmación correspondiente. «sí» no confirma. «cancelar conservación» cancela. «terminar la sesión» lee la elección vigente y pide «confirmo cerrar»; «continuar sesión» cancela. La conservación y el cierre no se confirman mutuamente. Después: «revisar intervención 1», «eliminar contenido» y «confirmo eliminar el contenido de esta sesión». El borrado no recrea respuestas.

Los metadatos se obtienen del estado autorizado, no del candidato, y pasan verificación independiente y T090. La revalidación y el presupuesto temporal pueden denegar la salida sin aplicar cambios pendientes. Véase G4-audio-gate.md para audio, silencio e interrupción todavía pendientes.

## Propósito didáctico optativo

`guided_policy(recipient, screenless=True, pedagogy=True)` prepara una política sucesora para actividades nuevas. No se amplía el esquema público DialogueAct ni se alteran sus reservas anteriores. La selección acotada examina cláusulas, propósito y contexto y devuelve solo referencias de unidades; no autoriza texto. Saludo/consulta general usan plantillas aditivas con opciones autorizadas. Definición/causa/proceso/posibilidad/condiciones seleccionan relaciones docentes explícitas. Dudas reiteradas usan una alternativa del mismo propósito; repetir literal conserva la salida autorizada íntegra. Ausencia de variante autorizada produce un límite explícito, sin sustituir el mecanismo por un ejemplo. Práctica protegida y defensa conservan sus preguntas y no revelación. No se afirma comprensión general del lenguaje natural; el reconocimiento es finito y se evalúan errores conservados y generalización por caso.

Pruebas pedagógicas comparan la respuesta real con expectativas de alcance, orden y contenido separadas del veredicto de publicación. Un grounding aprobado no demuestra pertinencia o suficiencia didáctica. Validación textual no aprueba audio ni utilidad con personas.

## Materiales tabulares y notas

Las referencias de tabla DOCX/PPTX son de celda de origen con fila/columna y número de tabla; Word puede incluir ruta de anidado y parte local. El texto principal se conserva y el contexto estructural acotado no infiere cabeceras ni da permiso. Los extractores no leen notas docentes. La API mantiene estados/versiones/aislamiento y T090 no cambia; corrección de extractor no reingiere documentos previos. Véase docs/LECTURA-DE-MATERIALES.md. No se publican automáticamente propuestas/unidades del paquete externo ni UUID de sus validadores.


## Verification v3

`guided_policy(..., screenless=True, pedagogy=True, advanced=True)` es optativa para nuevas actividades técnicas. Mantiene contrato v1/v2 y permisos previos. El planificador solo selecciona referencias publicadas: saludo general, propósito de cláusula, objetivo explícito, confirmación de cambio y hasta tres apoyos ordenados por relaciones. Desconocido fuera de fuente devuelve límite; no sustituye un tema ausente por el actual.

Solo coherencia recibe `dialogue_schema_version=3`, contrato2.2.0. Compara proposiciones de sujeto/predicado conocidos, negación local y propiedad numérica escalar con condiciones explícitas de presión/serie. Condiciones incompletas piden aclaración; distintas condiciones no prueban contradicción. Complementos modales, listas de observaciones y sujetos diferentes se distinguen. Repetición contrasta cláusulas completas; repetir literal nunca exime contradicciones. Es un analizador finito, sin garantía de inferencia semántica general. Grounding y no revelación conservan verificaciones independientes v2, fuentes vigentes y T090/T150. Grounding reconoce objetos nominales coordinados acotados y sujetos A y B; mantiene división de afirmaciones numéricas por entidad.

El paquete material propuesto conserva originales: overlays numerados aportan soportes/preguntas y ampliaciones explícitas. Solo TestClient con SQLite temporal propia admite publicación técnica; `reviewed=True` en estas pruebas no es aprobación humana. Tres dominios/cuatro formatos y recorridos de transcripción no validan STT/TTS o utilidad humana.


## Continuidad optativa v4

`guided_policy(..., screenless=True, pedagogy=True, advanced=True, continuity=True)` añade la plantilla normal `greeted-reviewed-response/v1`, texto fijo `Hola. {content}`. No hereda permiso de la plantilla de contenido anterior: actividad sin ese permiso explícito se rechaza. El renderer solo vincula el contenido docente vigente. Grounding/coherencia/SDV examinan íntegramente la parte académica reconstruida de la unidad; el prefijo fijo de saludo se comprueba por T090 en la propuesta completa. No hay contenido candidato eximido, hash propio de autorización o relajación de umbrales. El visor de pregunta conserva la fuente/pregunta original tras saludo autorizado.

La planificación de cláusulas usa propósito, precondición, conceptos de unidades publicadas y referentes actuales, con coincidencia léxica acotada y aclaración/límite si falta ancla. La respuesta del alumno conserva acto content_answer y no se introduce como verdad del asistente. Repreguntas recorren relaciones docentes vigentes distintas; la pregunta original permanece y la evaluación es not_assessed. Agotar apoyos da límite, no repetición eximida de coherencia.

«Lo confirmo» o «confirmo terminar sin conservarlos» solo confirma cierre si la última salida propone ese cierre y no hay otra operación pendiente. Sin contexto/tras intervención distinta/negación/cita no ejecuta. Si se pide terminar sin conservar desde conservación activa, se propone primero revocación; su confirmación no cierra. Después se solicita y confirma cierre separado. El comando exacto previo y las elecciones canónicas permanecen compatibles. No nueva estructura persistida, agente, migración, credencial o modo de red. No audio ni utilidad humana aprobados.
