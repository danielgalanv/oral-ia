# ORALIA: plan de acción consolidado para un piloto de autoestudio y examen oral

**Adenda del 30-10-2026:** la orden humana posterior y la constitución 2.0.0 autorizan
ampliación documental web restringida en autoestudio cuando falte evidencia local, con
atribución externa, contraste de validez y compatibilidad con material docente.
[Contrato y tareas vigentes](../../specs/012-conversational-course-study/contracts/web-evidence-fallback.md).
Esta adenda sustituye solo las referencias del texto del 27-10 a una enmienda web aún no
autorizada. No activa red ni modifica el alcance del examen, la voz o los ensayos preservados.

Fecha: 27 de octubre de 2026. Estado: **propuesta para revisar con el usuario; implementación detenida**.

Este documento integra las auditorías, la revisión de necesidades, los ensayos conservados y la nueva búsqueda de soluciones existentes. No se ha enviado a otras tareas. No autoriza reanudar implementación, ejecutar modelos, instalar dependencias, descargar pesos, cambiar requisitos ni publicar el tutor. Para la planificación futura sustituye las instrucciones de ejecución inmediata de los planes anteriores, que se conservan como antecedentes. Reanudar requiere una instrucción posterior del usuario.

## 1. Objetivo y límites

Preparar una herramienta autónoma de ayuda al estudio por chat, basada en documentos docentes autorizados, y comprobar su utilidad y viabilidad con algunos estudiantes en una actividad real acotada. Un piloto pequeño puede detectar problemas y aportar señales de aprendizaje; no demuestra por sí solo eficacia causal general.

**Actividad confirmada por el usuario:** autoestudio y examen oral sobre requisitos de Ingeniería del Software. El corpus combina los PDF docentes existentes y documentación pertinente localizada en fuentes oficiales de NASA, INCOSE e Ian Sommerville. No queda pendiente elegir otra actividad. La voz sigue aplazada: primero se valida el diálogo de ambos modos mediante chat; eso no acredita todavía la experiencia acústica de un examen oral.

Los modos tienen objetivos distintos. En autoestudio se explican conceptos, se reformula y se ofrecen ejemplos y práctica con retroalimentación didáctica. En examen ORALIA únicamente presenta las preguntas seleccionadas por el profesor y recoge las respuestas y eventos permitidos. Nunca evalúa, puntúa, aplica rúbricas, decide si la respuesta es correcta ni infiere el aprendizaje o capacidad del alumno. La interpretación de las evidencias corresponde al profesor. La revisión técnica de las preguntas y ayudas de ORALIA evalúa la herramienta, no al estudiante.

### Decisiones humanas que resuelven la auditoría del plan

- **Modalidad:** ambos modos por chat en esta versión. Voz en la siguiente versión, con validación propia y sin ser condición del primer ensayo por chat.
- **Corpus:** su preparación corresponde al asistente coordinador, usando los PDF docentes y fuentes oficiales autorizadas. No se exige al profesor generar el corpus ni redactar respuestas académicas. Prepararlo es trabajo documental autorizado; activarlo en el producto no reanuda la implementación por sí solo.
- **Examen:** el profesor selecciona las preguntas y configura por pregunta si permite ayudas y cuántas. También decide si se permite saltar preguntas y volver a ellas. El sistema ejecuta esa configuración, no altera preguntas o permisos por su juicio sobre el alumno.
- **Evidencia de aprendizaje:** la interpreta el profesor. ORALIA puede proporcionar datos descriptivos, como número de preguntas y conceptos consultados con mayor frecuencia, respetando consentimiento y conservación. Frecuencia no significa dificultad, dominio ni aprendizaje.
- **Ensayo:** en cuanto exista un recorrido funcional se hará un ensayo real temprano con el usuario/docente, para comprobar funcionamiento y uso. No se espera a terminar toda la investigación. Un ensayo temprano no habilita automáticamente participación de estudiantes ni prueba eficacia; el piloto posterior mantiene sus controles proporcionados.

**Aclaración posterior del usuario:** desarrollar primero autoestudio, por ser el núcleo más complejo; después adaptar esa base al examen. El examen conserva pruebas propias de configuración, navegación, ayudas y evidencias, pero no se antepone al autoestudio por ser más sencillo.

**Saltar significa aplazar, no omitir definitivamente.** Cuando el profesor permite saltar, el alumno puede pedir otra pregunta antes de responder la actual. ORALIA continúa el orden establecido de la ronda y, al terminarla, vuelve a las preguntas aplazadas en su orden original. No es navegación arbitraria ni abandono de la pregunta. Si saltar no está permitido, explica esa limitación. No se ofrece como variante del salto la omisión irreversible. Si el alumno vuelve a aplazar una pendiente, no se marca respondida ni se inventa una respuesta; se conserva pendiente y se permite el cierre explícito sin bucle automático.

**Una ayuda se consume cuando, ante una pregunta de examen, el alumno pide ayuda o aclaración y ORALIA genera una respuesta de ayuda para comprender correctamente esa pregunta.** No es evaluación del alumno ni una respuesta al ejercicio. El profesor fija si se permite y cuántas por pregunta. La ayuda generada debe respetar fuentes y límites de contenido; se cuenta una vez por solicitud válida con ayuda producida, no por clic o retransmisión. Una generación fallida o un candidato rechazado que no constituye ayuda no consume unidad. Si la ayuda ya se produjo, un reintento de transporte recupera la misma y no genera ni consume otra. Registrar generación y entrega separadamente; no cambiar silenciosamente el contador según la conexión. Pedir «aclaración» del contenido de la pregunta sigue esta misma política de ayudas; una instrucción puramente operativa de la interfaz no da pistas. Volver a una pregunta no reinicia el cupo.

### Detalles confirmados para envío, pistas y conservación

El alumno confirma su respuesta pulsando el botón de envío. En la versión oral posterior también pulsará un botón para indicar que ha terminado; el silencio o una inferencia del modelo no equivalen a confirmar la respuesta. La versión por chat no implementa todavía captura de voz. La futura voz necesitará procesamiento transitorio para transcribir, pero **no se guardan audios** en archivos, base de datos, logs, exportaciones o evidencias de prueba. También deben comprobarse temporales y comportamientos por defecto de las bibliotecas cuando se aborde esa versión.

Las pistas permitidas, según la configuración docente por pregunta y su cupo, son: reformular la pregunta para comprenderla; situarla en el tema y apartado de la documentación; nombrar conceptos similares sin explicarlos; o proporcionar un ejemplo. No se presupone una secuencia obligatoria, ni que todos los tipos estén habilitados para toda pregunta. El ejemplo puede ser hipotético y coherente; no debe resolver la pregunta concreta ni convertirse en evaluación de la respuesta del alumno. La reformulación conserva lo que la pregunta pide, sin añadir o retirar exigencias. La localización documental debe corresponder a una sección real; el sistema no inventa apartados. Nombrar conceptos relacionados no autoriza desarrollar su explicación ni revelar la solución.

El usuario confirma que el piloto contará con permiso para conservar los datos necesarios para informes, **excepto audio**. Se pueden planificar conservación de textos/transcripciones, preguntas/respuestas, pistas, conceptos, estados, eventos y tiempos. Antes de incorporar participantes se materializa ese permiso en el consentimiento y configuración de la actividad; esta decisión no cambia retroactivamente elecciones de conservación de sesiones anteriores. Registrar por actividad los datos recogidos, quién accede y el ciclo de retención/purga, sin exigir otra aprobación humana para cada campo técnico. Las estadísticas siguen siendo descriptivas y no habilitan notas, perfiles de capacidad o valoración académica automática.

### Corpus y fuentes externas confirmadas

Los PDF de la asignatura fijan el contexto docente. NASA, INCOSE y Sommerville aportan perspectivas complementarias sobre necesidades, requisitos, calidad, especificación, verificación y validación, siempre dentro de la actividad. No se fusionan términos o recomendaciones de ingeniería de sistemas con los del curso sin explicar su contexto. Ante diferencias sustantivas se muestran procedencia y discrepancia para su aclaración docente; no se inventa una verdad única por mayoría de fuentes.

Fuentes iniciales comprobadas para preparar el inventario:

- [NASA Systems Engineering Handbook, apéndices C–E](https://www.nasa.gov/reference/system-engineering-handbook-appendix/): escritura, revisión y matrices de verificación/validación de requisitos.
- [NASA Software Engineering Handbook, SWE-055](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695440/SWE-055%2B-%2BRequirements%2BValidation): validación de requisitos de software.
- [INCOSE Publications & Resources](https://www.incose.org/resources-publications/) y [presentación oficial de la guía de escritura v4](https://www.incose.org/resource/webinar-168-guide-to-writing-requirements-version-4/): localizar edición y materiales utilizables. Revisar los derechos del recurso concreto antes de reproducir o distribuir el texto íntegro; una URL accesible no acredita esos derechos.
- [Ian Sommerville, presentaciones oficiales de Software Engineering](https://software-engineering-book.com/slides/): seleccionar material sobre requisitos y registrar edición; evitar duplicar las mismas diapositivas ya presentes en los PDF docentes.

Esta autorización permite planificar búsquedas e incorporación de esas fuentes; no activa navegación durante cada sesión. Se propone preparar primero un corpus local revisado, con URL, autor/organización, edición, fecha de acceso, licencia/condiciones, hash y posiciones. La búsqueda web dinámica ante insuficiencia es una capacidad separada, pendiente de diseño y conciliación constitucional. No se emplean copias no autorizadas de libros o guías ni se da por incorporado un documento por haber localizado su enlace.

El LLM genera explicaciones desde evidencia recuperada. No se sustituye por respuestas docentes predefinidas, un perfil extractivo presentado como tutor natural o aprobación humana de cada respuesta. La supervisión del investigador y la revisión de muestras sí forman parte de preparar y observar el piloto.

Se mantienen las decisiones ya tomadas:

- Contenido de la asignatura y bloques principales confirmados, sin bloques extra autónomos. Cobertura de la actividad piloto declarada; una fuente ausente no excluye un tema del temario.
- Diapositivas docentes autorizadas, sin material de alumnado. Una representación útil por documento, evitando duplicar PDF y PPTX equivalentes.
- Explicaciones sensibles a qué, por qué y cómo; saludo, continuidad, reformulación material ante dificultad, ejemplos y práctica cuando sean pertinentes.
- Ficción coherente permitida en ejemplos. El principio académico, la interpretación y las conclusiones necesitan respaldo o premisas suficientes; no se exige encontrar cada dato ficticio en el PDF.
- Fuentes visibles legibles por documento/página y procedencia interna exacta. «Consultadas» no significa «todas las afirmaciones verificadas».
- Voz aplazada. Internet de producto desactivado; las búsquedas de investigación no modifican esa política.
- Consentimiento, conservación, cierre, aislamiento de datos y parada siguen siendo necesarios aunque el destino sea un piloto.

No se exige antes del piloto cobertura de toda la asignatura, todos los modos históricos, escalabilidad, disponibilidad continua, voz ni superioridad de una arquitectura multiagente. Tampoco se eliminan esas aspiraciones ni sus pendientes históricos por este plan.

## 2. Base documental y autoridad

| Fuente | Uso en este plan |
|---|---|
| [Auditoría global de ensayos](../audits/2026-10-27-global-viability/informe.md) y [limitaciones](../audits/2026-10-27-global-viability/limitaciones-y-decisiones.md) | Distinguir defectos corregibles, límites observados y capacidades sin validar. |
| [Hallazgos F01–F21](../audits/2026-10-27-foundations-review/hallazgos-final.md), [backlog B01–B18](../audits/2026-10-27-foundations-review/backlog.md) y [arquitectura recomendada](../audits/2026-10-27-foundations-review/arquitectura-recomendada.md) | Fundamentos, seguridad, recuperación y transición compatible. |
| [Revisión final de necesidades](../audits/2026-10-27-needs-proportionality/informe-final.md) y [decisiones materiales](../audits/2026-10-27-needs-proportionality/decisiones-para-el-usuario.md) | Revisión de 418 identificadores; separar necesidad humana de mecanismo prescrito. Sus disposiciones son propuestas, no derogaciones. |
| [Nueva revisión de reutilización y estado del arte](../audits/2026-10-27-reuse-state-of-art/decision.md) | Sentence Transformers, Docling, detectores especializados, gramáticas y límites de integración. Contiene las fuentes primarias externas. |
| [Plan anterior](2026-10-27-oralia-audit-action-plan.md) y [anexo de proporcionalidad](2026-10-27-requirements-proportionality-addendum.md) | Antecedentes preservados; sus órdenes de continuar no prevalecen sobre la pausa actual. |
| [Propuesta de comparación de generadores](../../specs/012-conversational-course-study/evidence/generator-capacity-decision-v1/decision.md) | Protocolo existente que revisar antes de crear otro experimento redundante. |

La inspección más reciente ya muestra corregida la identidad de caché de embeddings y la carga local explícita. Otras correcciones estaban en curso al detener implementación. Por eso este plan no da por pendientes todos los defectos históricos ni por aceptadas las entregas recientes: primero debe verificarse el estado efectivo del árbol detenido.

## 3. Decisión de arquitectura y reutilización

La selección concreta de algoritmos, fuentes primarias, flujo y decisiones todavía pendientes está en [técnicas y flujos seleccionados](2026-10-27-technology-and-workflow-decisions.md). Se reutilizan soluciones contrastadas antes de crear alternativas propias, y se conservan si funcionan en las pruebas de ORALIA. No se exige investigar desde cero su principio ni se presupone que un benchmark externo acredita nuestro uso.

**Conservar:** monolito modular, aplicación y almacenamiento local, puertos/adaptadores, permisos del host, versiones de fuentes, trazas, extractores nativos correctos, estado basado en lo mostrado y evidencia histórica.

**Refactorizar:** recuperación de laboratorio para compartir capacidades existentes; segmentación/representación según tokens; contratos redundantes y recibos mutables; fronteras de entrega y configuración donde la auditoría reproduce defectos.

**Integrar solo después de comparar:** recuperación semántica y posible reranking con Sentence Transformers ya presente; Docling/OCR para huecos concretos; detector especializado de respaldo; motor de schema mantenido si aparece una necesidad que el decoder pequeño no resuelve.

**Desarrollo propio necesario:** enlace curso/actividad/fuentes y alcance docente; política de ejemplos y límites; entrega idempotente; adaptación de interfaces; banco de evaluación de la asignatura; criterios y protocolo del piloto. No desarrollar desde cero modelos, motores de OCR, embeddings, compiladores de gramáticas ni otro framework de agentes.

**No priorizar:** GraphRAG, más agentes, migración completa de framework, fine-tuning, voz, memoria longitudinal, web, LAN y paneles adicionales. Una necesidad futura demostrada puede cambiar esta decisión.

## 4. Fases y criterios de salida

Las fases son paquetes de trabajo propuestos, no tareas en ejecución. Las dependencias son lógicas; no autorizan delegación o procesos simultáneos.

### P0. Conciliar el estado y fijar la primera actividad

**Trabajo:** inventariar cambios al momento de la pausa y comprobar las entregas ya realizadas con sus pruebas y evidencias. Clasificar cada hallazgo como pendiente, corregido con evidencia, riesgo no reproducido o decisión de producto. Mantener un único registro, sin otra colección masiva de snapshots.

Preparar dos fichas de piloto dentro de la actividad ya confirmada: autoestudio y examen oral sobre requisitos. Concretar objetivos observables, fuentes docentes y externas, cobertura, tipos de pregunta y configuración candidata. Inventariar contenidos disponibles antes de fijar subtemas; no reducir automáticamente el piloto a calidad y validación. Usar preguntas nuevas, sin fijar respuestas generadas ni convertir los ejemplos expuestos en reserva. Si falta cobertura, completar las fuentes pertinentes o declarar el límite del subtema; no cambiar la actividad confirmada sin decisión humana.

**Salida:** matriz de estado y dos fichas revisables, con mapa de conceptos a fuentes y configuración docente del examen: preguntas elegidas, ayudas permitidas y límites por pregunta, salto/vuelta y cierre. Sin rúbrica ni valoración automática. Recursos protegidos identificados, incluidos originales, evidencias, presupuestos y reserva. No se pierde ningún pendiente al simplificar tareas. El profesor cumplimenta la configuración concreta; ya no queda pendiente decidir quién formula las preguntas o quién evalúa.

### P1. Terminar y verificar los fundamentos técnicos

**Trabajo:** identidad modelo/revisión, offline explícito, fingerprint del índice, configuración solicitada/efectiva, límites y causas de terminación. Verificar A→B→A, concurrencia y recursos ausentes con dobles CPU. Igual dimensión no implica mismo espacio vectorial. Un índice antiguo sin identidad se declara no acreditado para comparaciones nuevas, no corrupto.

Medir tokenización frente al segmentador de 800 caracteres y al límite declarado de 128 tokens del MiniLM actual. Diseñar unidades de búsqueda acotadas que puedan expandirse a contexto completo con procedencia. No asumir que todos los fragmentos actuales exceden el límite ni reindexar datos habituales por defecto.

**Salida:** pruebas negativas reproducen los defectos antes de corregirlos o justifican qué ya estaba corregido; no hay recortes de presupuesto silenciosos ni mezclas de identidad. Índices de prueba aislados y ruta de reversión documentada. `length` nunca cuenta como respuesta completa.

**Dependencia:** P0. **Recursos:** CPU, datos propios; sin pesos nuevos.

### P2. Asegurar privacidad, estado y entrega para el piloto

**Trabajo:** cerrar valores de eventos técnicos, no solo nombres de claves; probar conservación y exportación; probar caída/reinicio, reintento, dos conexiones, cancelación, cierre ganador, retirada y resultado tardío. Revisar mutabilidad de recibos y confirmaciones repetidas. Ensayar documentos ficticios con instrucciones maliciosas sin conceder autoridad al modelo.

Describir honestamente borrado lógico, temporales, logs, WAL y copias. No prometer eliminación forense ni aplicar VACUUM o migraciones a datos habituales. Una política de abandono de sesión nueva se presenta por separado antes de aplicarla.

**Salida:** ningún texto no autorizado llega a la entrega; no se duplica historial o cierre; los eventos conservan solo valores permitidos; existe recuperación operativa controlada. Riesgos no reproducidos siguen etiquetados como tales, sin fabricar vulnerabilidades.

**Dependencia:** P0; comparte información con P1 pero no requiere inferencia. **Recursos:** CPU y bases temporales.

### P3. Acordar criterios y contrato de publicación generativa

**Trabajo:** preparar un contrato sucesor optativo, compatible con T090/T150. El host vincula permiso a texto final, sesión, actividad, fuentes y revisión; cambios relevantes lo invalidan. El generador no se autoriza a sí mismo. Un hash identifica contenido, no certifica verdad.

Separar controles deterministas de acceso de señales semánticas empíricas. Proponer criterios de fidelidad, pertinencia, cobertura, utilidad, falsos rechazos y abstención. Fijar banco, revisores y adjudicación antes de evaluar, sin exigir demostración universal de toda paráfrasis.

**Salida:** diseño concreto y negativos de sustitución/reutilización/retirada; criterios revisados con el usuario. Puede probarse en laboratorio con autoridad simulada etiquetada, pero no activar participantes mediante un cambio de nombre a «piloto» o «preview».

**Dependencia:** P0 y límites conocidos de P2. La aprobación de diseño no acredita que exista un evaluador viable.

### P4. Mejorar recuperación y cobertura de forma comparativa

**Trabajo:** puerto común sobre fuentes autorizadas; baseline léxico conservado; adaptador denso existente; posible unión de rankings y después reranker si los candidatos pertinentes sobreviven. No sumar escalas incompatibles. Controlar aporte total del historial y resolver referente sin arrastrar instrucciones antiguas.

Comparar en preguntas nuevas: paráfrasis, español/inglés técnico, elipsis, cambio de tema, distractores, tablas y evidencia en varios pasajes. Registrar candidatos antes/después de filtros, recall, pertinencia, volumen de contexto y latencia. La mejora no consiste solo en recuperar más páginas.

Probar alcance informado por búsqueda autorizada como variante optativa. La política docente autoriza; ni vacío ni score alto prueban exclusión/inclusión. Preguntas mixtas y operativas tienen tratamiento explícito. No volver a promover el clasificador anterior que excluyó una introducción de Ingeniería del Software.

Para las 26 páginas visuales en cuarentena, resolver primero las necesarias para la actividad. Usar PPTX autorizado si resulta más fiel; Docling/OCR solo ante un hueco concreto, con QA contra el original. No ampliar todo el curso como condición previa.

**Salida:** decisión medida de conservar/rechazar cada estrategia, representación versionada y cobertura declarada. Datos anteriores intactos. Ningún resultado sobre recuperación acredita calidad de generación.

**Dependencia:** P1 y ficha de P0. **Recursos:** primero CPU/local existente; pesos adicionales requieren propuesta concreta.

### P5. Resolver por separado capacidad del generador y viabilidad del revisor

**P5a — Generador.** Revisar la propuesta congelada 7B/14B existente: evidencia fija pertinente frente a RAG, mismas condiciones y preguntas nuevas. El protocolo previo plantea hasta 16 respuestas y dos calentamientos, 768 tokens y 20 minutos globales; son límites de esa propuesta, no requisitos universales del producto ni ejecución autorizada ahora. Cualquier revisión de presupuesto se congela prospectivamente.

Si falla con fuentes adecuadas, no atribuirlo al ranking. Si funciona con evidencia fija y falla en RAG, estudiar recuperación/contexto. Si hay truncamiento, registrar esa limitación sin inventar los turnos posteriores. No añadir automáticamente otro prompt, familia o modelo mayor. Entregar decisión de capacidad y alternativas con coste.

**P5b — Revisor.** Examinar un candidato especializado antes de crear otro juez propio. Primera opción de estudio: familia LettuceDetect; elegir un checkpoint concreto tras comprobar idioma, licencia, preprocesamiento y compatibilidad. EuroBERT español advierte Transformers <5 y código remoto; requiere revisión y entorno separado. mmBERT v2 tampoco se presupone compatible o eficaz: verificar entrada real, incluida la pregunta. RefChecker aporta un planteamiento modular, con límites publicados de cobertura y contexto.

Preparar calibración y transferencia separadas: afirmaciones respaldadas, paráfrasis, errores centrales, negación/modalidad, evidencia distribuida, conclusión falsa con cita correcta, ejemplos ficticios válidos y preguntas parcialmente respondidas. Medir falsos permisos, falsos rechazos, omisiones y coste. Un detector de respaldo no sustituye la evaluación de pertinencia, cobertura o pedagogía.

**Salida:** candidato defendible o limitación explícita de cada vía. Rechazar todo falla; pasar controles breves no acredita transferencia. No se entrena sobre el oráculo ni se consume reserva para ajustar. Si ninguna vía resulta suficiente, detener esa inversión y presentar una decisión de viabilidad; no construir otra capa estructural vacía.

**Dependencia:** P1; P5a con evidencia fija puede preceder a P4 completo. La evaluación RAG usa una versión identificada de P4. P5b comienza con compatibilidad CPU y solo después plantea inferencia.

### P6. Demostrar episodios completos de estudio

**Trabajo:** integrar candidatas defendibles en laboratorio y observar duda → incomprensión → explicación distinta → ejemplo → aplicación o matiz/cambio. Solo lo efectivamente mostrado alimenta el historial. Añadir saludos, preguntas qué/por qué/cómo, correcciones del alumno, alcance, insuficiencia y conflicto como controles explícitos.

Para examen, ejecutar además un episodio separado: pregunta elegida por el profesor → respuesta o petición de ayuda → ayuda autorizada dentro de su límite → siguiente pregunta o salto/vuelta permitido → cierre y recogida de evidencias. No generar preguntas evaluadoras nuevas ni seguimientos por inferencia de corrección; cualquier subpregunta debe pertenecer a la configuración docente. Comprobar que no se filtra la solución, que las ayudas se contabilizan y que no se emiten juicios sobre la respuesta. Probar salto permitido/prohibido, vuelta a pendientes, límites de ayudas, reconexión y ausencia de duplicados. El cierre informa del recorrido y pendientes, no devuelve una nota ni un veredicto académico.

La política pedagógica es flexible: explicación directa si se pide, práctica opcional, sin examen obligatorio en cada turno. No se guardan diagnósticos de capacidad del alumno. Revisores identificados evalúan fidelidad y utilidad; las diferencias se adjudican contra fuentes, no mediante voto automático sin calibración.

Separar diagnóstico de casos independientes de continuidad conversacional. Un fallo bloquea la entrega de esa conversación; otros casos independientes pueden ejecutarse si así se presupuestó. No simular que el alumno vio un texto rechazado.

**Salida:** episodios nuevos completos con revisión y costes, sin reparar salidas durante el ensayo; límites y fallos preservados. Repeticiones greedy idénticas no equivalen a diversidad de evidencia. Requisitos históricos de repeticiones se mantienen hasta acordar su evolución.

**Dependencia:** P3, P4 y candidatas defendibles de P5. Si falta un revisor viable, P6 solo puede producir evidencia diagnóstica; no permiso de publicación.

### P7. Preparar la experiencia y el protocolo humano

**Trabajo:** ruta docente para activar fuentes y ver cobertura; alumno pregunta, ve espera/cancelación y fuentes, continúa y cierra con conservación comprensible. Reutilizar interfaz; no crear otro panel técnico. Probar recorrido, errores y recuperación en recursos propios.

Proponer un piloto pequeño: objetivos y criterios de inclusión, tareas equivalentes, medida previa y posterior sin ayuda cuando corresponda, valoración de claridad, errores, bloqueos, tiempos y carga docente. Medir satisfacción por separado del aprendizaje. Si se compara una condición alternativa, controlar tarea y exposición; un grupo de conveniencia no autoriza afirmar causalidad general.

La evidencia del aprendizaje y su interpretación corresponden al profesor, que puede usar tareas o preguntas distintas de las practicadas si desea observar transferencia. ORALIA no mide ni califica ese aprendizaje. Entrega, cuando el consentimiento lo permite, transcripción y datos descriptivos: preguntas presentadas/contestadas/omitidas/pendientes, ayudas solicitadas y entregadas por pregunta, y duración como dato operativo, nunca como indicador de capacidad. En autoestudio puede resumir frecuencias de preguntas o conceptos consultados. Los conceptos se identifican mediante un vocabulario docente trazable o categorías con origen e incertidumbre registrados; no se convierten en perfiles longitudinales ni en diagnósticos de dificultad. Separar eventos operativos mínimos de contenido y estadísticas que requieren conservación consentida. La fase por chat valida el diálogo del examen, no escucha, reconocimiento del habla o latencia de voz.

Precisar consentimiento, datos mínimos, retención, acceso del investigador, derecho a parar y plan de incidentes. No reclutar, contactar o iniciar sesiones reales automáticamente; requisitos institucionales se concretan con el docente.

**Salida:** paquete listo para decisión humana: configuración, cobertura, muestras, errores residuales, criterios de parada, protocolo, carga docente y plan de retorno al modo cerrado. Voz sigue fuera del piloto.

**Dependencia:** partes documentales desde P0; activación exige P2, P3 y P6 aceptados.

### Hito transversal: ensayo real temprano con el usuario/docente

Al disponer de un recorrido funcional, realizar el ensayo desde su entorno habitual con documentos y preguntas reales: preparar actividad, autoestudio, configurar preguntas/ayudas/salto, responder, volver a pendientes cuando proceda y cerrar. No requiere esperar la finalización de todos los experimentos comparativos. Debe existir seguridad operativa básica; cualquier salida generativa aún no autorizada se mantiene como preview de laboratorio identificado para el docente. Recoger fallos de funcionamiento y experiencia, corregirlos en su fase y repetir solo lo afectado. No contar este ensayo como piloto con estudiantes ni como aceptación semántica general. El usuario ya ha pedido hacerlo cuando sea funcional; coordinar su realización sin reclutar a otras personas.

### P8. Piloto y decisión posterior

Solo tras autorización específica: ejecutar el protocolo acordado, sin ajustes silenciosos durante la recogida. Ante incidente, parar o suspender la condición afectada y conservar únicamente los datos autorizados. Cualquier cambio de modelo/fuentes/política crea una versión de ensayo distinta.

**Salida:** informe de factibilidad, señales de aprendizaje/transferencia, errores y esfuerzo docente. Decidir continuar, corregir o no ampliar. Comparación arquitectónica y voz son fases posteriores independientes, no condiciones añadidas retrospectivamente al piloto.

## 5. Dependencias y decisiones de inversión

| Punto de decisión | Evidencia necesaria | Si no se alcanza |
|---|---|---|
| Base interpretable | P1 y configuración real acreditadas | Corregir fundamentos; no interpretar otro ensayo de capacidad. |
| Seguridad operativa | P2 y contrato P3 revisados | Mantener participante cerrado; continuar solo diagnósticos independientes. |
| Recuperación suficiente | Referencias relevantes alcanzables y contexto útil en banco nuevo | Corregir fuente/representación/ranking según causa; no compensar con más agentes. |
| Generación suficiente | Explicación y ejemplos fieles con evidencia fija y después RAG | Declarar límite de la configuración; comparar alternativa solo con hipótesis nueva. |
| Revisión suficiente | Discrimina positivos y negativos y transfiere | No promocionarla por su benchmark; decidir investigación adicional o mantener no disponible. |
| Episodio útil | Conversación completa fiel, pertinente y pedagógicamente revisada | Corregir la capa responsable; no anunciar tutor listo por cantidad de tests. |
| Piloto preparado | Fuentes, contrato, experiencia, protocolo y aprobación docente | No reclutar ni abrir acceso. |

La falta de un verificador universal no bloquea por definición cualquier piloto; sí exige un mecanismo empírico suficiente para el riesgo y dominio acordados. El contrato vigente no se elude, y un nivel de riesgo residual nuevo se presenta al usuario para decisión explícita. La revisión humana del diseño y muestras no se convierte en aprobación manual de cada turno.

## 6. Criterios de aceptación que faltan por concretar

Propuesta para acordar en P0/P3, antes de ejecutar bancos nuevos:

1. **Actividad y aprendizaje:** qué debe poder explicar o aplicar el alumno tras usar el tutor, fuentes y límites de cobertura.
2. **Errores críticos:** error conceptual central, conclusión incompatible con premisas, falsa exclusión del curso, entrega no autorizada o conservación indebida. Propuesta: cualquiera de ellos en el banco crítico bloquea promoción hasta resolver y revalidar con controles nuevos. No equivale a riesgo cero fuera del banco.
3. **Positivos y utilidad:** definir diversidad de casos y cobertura mínima antes de probar. Un sistema que se abstiene siempre no cumple. No inventar porcentajes aprobados ni reducir criterios después de ver resultados.
4. **Servicio:** medir finalización, mediana y cola de espera, carga inicial y cancelación. El objetivo tolerable de uso se acuerda con datos; 30/50 segundos históricos son deadlines de perfiles, no aceptación humana automática.
5. **Esfuerzo docente:** presupuesto de preparación, QA y revisión de muestras. El docente no redacta todas las respuestas ni revisa cada salida de uso.
6. **Revisión y autoridad:** revisores, discrepancias, contrato sucesor y cambios necesarios de requisitos. Nadie marca revisión humana por haber ejecutado un script.

Estas decisiones se agrupan; no son una nueva ronda de preguntas sobre voz, temario, ficción, referencias o permisos ya fijados.

## 7. Trazabilidad completa del trabajo auditado

| Backlog previo | Fase principal | Conservación de su intención |
|---|---|---|
| B01 caché/offline; B02 identidad de índice; B03 budgets | P1 | Verificar estado actual antes de repetir correcciones. |
| B04 recibos y exposición de bancos | P0, P1, P5 | Evidencia mínima suficiente y separación de reserva/regresión. |
| B05 eventos; B06 caída/concurrencia; B07 borrado | P2 | Garantías proporcionadas al piloto, sin promesas forenses inventadas. |
| B08 autorización; B09 inyección/entrega | P2, P3 | Host con autoridad; generador sin autopermiso; no bypass de T090/T150. |
| B10 puerto; B11 historial/híbrido/reranking; B12 alcance | P4 | Reutilización real y comparación de causas. |
| B13 representación | P4 | Reparación focal, formatos y QA antes de ampliar corpus. |
| B14 pedagogía | P5, P6 | Hipótesis flexible evaluada, no respuestas prefabricadas. |
| B15 generación/revisión | P5 | Candidatos externos y experimentos aislados, sin escalera de prompts. |
| B16 episodio | P6 | Continuidad desde lo mostrado y transferencia nueva. |
| B17 ruta de producto | P7 | Experiencia reutilizada y capacidades honestas. |
| B18 utilidad/arquitectura | P7, P8 | Piloto separado de superioridad arquitectónica. |

Las disposiciones de los 418 IDs no se ejecutan como eliminaciones en bloque. Cuando se reanude, cada modificación de requisito tendrá motivo, autoridad y efecto en SpecKit. Se distinguen necesidad mantenida, mecanismo sustituido, aspiración aplazada y ambigüedad pendiente.

Las seis evidencias históricas perdidas y la revisión humana de Feature 010 conservan su estado. Las nuevas pruebas no restauran originales. Una disposición explícita y documentada puede resolver su tratamiento administrativo, pero no se inventa restauración ni aprobación. El cierre histórico global y la preparación de una actividad nueva son decisiones distintas, con bloqueos trazados.

## 8. Ejecución futura con SpecKit y preservación

Al recibir una orden posterior de reanudación, el primer bloque será P0: conciliar lo implementado, presentar ficha y traducir el bloque aprobado a tareas dependientes. Reutilizar spec/plan/tasks actuales; no regenerarlos o compactarlos perdiendo estados. Aplicar specify/clarify/plan/tasks solo donde corresponda y analizar coherencia antes de implementar. Analizar y converger al entregar un bloque no convierte una prueba de código en aceptación docente.

Un único escritor futuro, sin encargar trabajo ahora. Cada entrega indica problema, cambio, prueba, resultado y límite. Tests proporcionados: reproducción negativa, contrato/integración afectada y regresión amplia al consolidar cambios comunes. No repetir las 204 celdas o toda la suite por cambios ajenos a ellas. Ruff por identidad y multiplicidad; estilo y build cuando corresponda.

Sin commits, Reset, alteración de originales/evidencia/reserva/presupuestos, reindexación habitual automática ni intervención en procesos ajenos. Todo experimento nuevo usa raíz y presupuesto propios; se conserva el primer fallo. No editar retrospectivamente oráculos o salidas para aprobar.

Para GPU, cuando se autorice reanudar: anunciar propósito, modelo, presupuesto y duración, verificar disponibilidad vigente y muestrear antes/durante/después. La autorización anterior de disponibilidad no inicia pruebas durante esta pausa. Competencia de recursos vuelve inconcluyente el rendimiento; no explica por sí sola un error textual. Detener únicamente procesos propios.

## 9. Primer resultado que debe producir el plan

No otra implementación general ni una batería de modelos. Primero, una ficha breve con la actividad piloto ya confirmada, estado real de las correcciones, criterios pendientes y bloque inicial delimitado. La sección 10 concreta ese bloque para evitar otra fase de planificación indefinida. Con esa base el usuario puede aprobar un paso concreto y revisable. Hasta entonces, este documento permanece como planificación y las demás tareas no reciben órdenes.

## 10. Entregas incrementales y pruebas del usuario

Esta sección concreta el orden de entrega y prevalece sobre una lectura secuencial de P0–P8. Esas fases conservan la trazabilidad técnica, pero no obligan a terminar toda la investigación antes de probar funciones independientes. La implementación sigue detenida hasta una orden posterior. Las decisiones funcionales siguientes son propuestas de comportamiento para las entregas, no cambios ya ejecutados.

### Reglas de cada incremento

Cada incremento tiene un recorrido completo en la aplicación existente, una forma de iniciarlo, datos reales de prueba, alcance visible y posibilidad de volver al estado anterior sin borrar datos habituales. Antes de ofrecerlo al usuario, el implementador realiza su propia comprobación técnica y un recorrido de extremo a extremo. No se entrega una funcionalidad conocida como rota para que el usuario encuentre el fallo.

La entrega incluye: qué cambió, cómo probarlo, qué debería observarse, qué falta y dónde queda su evidencia. La prueba humana se solicita solo para funciones con entidad visible; caché, fingerprint o refactor interno se verifican técnicamente y se agrupan con el siguiente recorrido útil. No se exige al usuario revisar cada script, test o microcambio.

Registrar por separado «implementado», «verificado técnicamente», «disponible para prueba», «probado por el usuario» y «aceptado para el piloto». La prueba del usuario no equivale a aceptación de seguridad, eficacia o cobertura no observadas. Su respuesta sobre un incremento orienta el siguiente; no se acumulan cambios que oculten o invaliden lo que está probando. Las partes técnicas independientes pueden prepararse, pero no se cambian silenciosamente las condiciones de su sesión.

| Incremento | Resultado visible para el usuario | Prueba propuesta | Dependencia y límite |
|---|---|---|---|
| I0. Arranque fiable y acceso | Abrir desde su terminal habitual, entrar en una actividad de prueba, cerrar y volver a entrar sin errores de dependencias o sesión ocupada. | Arrancar, entrar, cerrar y repetir. | Verificar lo ya implementado y corregir solo brechas reproducidas. Sin Reset ni detener procesos ajenos. No valida generación. |
| I1. Fuentes y cobertura | Consultar qué PDF y recursos externos están incorporados, su versión y qué contenido puede estudiarse; abrir una fuente y localizar un pasaje. | Elegir un concepto y contrastar su procedencia con el original. | Corpus local inicial con contenido real revisado. La incorporación completa de las tres familias externas puede progresar por versiones; no anunciar las aún no disponibles. Reutilizar la vista existente, sin panel nuevo por defecto. |
| I4. Autoestudio RAG inicial | Preguntar por requisitos y recibir explicación generada con fuentes consultadas; pedir una aclaración y continuar desde lo mostrado. | Una duda real, un «por qué» y una petición de ejemplo; contrastar contenido y fuentes. | I1, configuración acreditada y controles aplicables. Si los gates siguen cerrados, solo prueba docente del preview de laboratorio identificado, sin simular publicación al participante. Corpus y capacidades limitadas visibles. |
| I5. Continuidad didáctica y límites | Reformulación útil, ejemplos coherentes, cambio de tema, orientación y recuperación ante insuficiencia o rechazo sin perder la sesión. | Indicar que no se entiende, rectificar la pregunta, cambiar de tema y probar una duda sin fuentes suficientes. | I4; revisar cada comportamiento contra fuentes y contrato. No convertir un límite legítimo en cierre automático de toda la sesión. |
| I2. Examen básico completo | El profesor configura preguntas; el alumno las recibe en orden, redacta y confirma respuestas, cierra; el profesor consulta evidencia cuando se permite conservarla. | Tres preguntas propias con respuestas distintas; comprobar orden, texto confirmado y cierre sin comentarios evaluadores. | Después de la base de autoestudio I4/I5 por prioridad humana; reutiliza sus servicios, pero esta ruta sin ayudas generadas no necesita una inferencia por pregunta. P1/P2 y permisos aplicables. |
| I3. Salto, vuelta y recuperación | Si se permite saltar, ORALIA continúa la ronda y al terminar vuelve a las aplazadas; estados y recuperación coherentes. | Aplazar la primera y tercera preguntas, responder las restantes y comprobar la vuelta en orden; probar también salto deshabilitado. | I2. Ningún salto equivale a omisión irreversible; cierre explícito con pendientes y persistencia según consentimiento. |
| I6. Ayudas del examen | El profesor habilita ayudas y límites por pregunta; ante petición del alumno ORALIA genera una aclaración para comprenderla, sin resolverla ni evaluar. | Preguntas con cero, una y dos ayudas; doble clic, fallo y vuelta a una pregunta para comprobar el contador. | I2/I3 y generación acreditada de I4/I5 con sus controles. El profesor no tiene que redactar respuestas completas ni un banco de ayudas prefabricadas. |
| I7. Evidencias y datos descriptivos | Revisar/exportar respuestas y eventos consentidos; ver recuentos operativos y consultas por concepto sin juicios académicos. | Comparar un recorrido conocido con su informe; probar conservación y no conservación y acceso solo del propietario. | I2/I3 para examen; I4 para conceptos de autoestudio; eventos de I6 cuando estén presentes. No requiere terminar ayudas generadas para entregar los recuentos ya disponibles. |
| I8. Ensayo integrado | Recorrido real del profesor con ambos modos y configuración identificada; después decisión de preparación del piloto con estudiantes. | Preparar, estudiar, realizar examen, revisar evidencia y cerrar desde el entorno habitual. | Incrementos que se incluyan en el alcance declarado y controles P7. No exige voz, web dinámica o cobertura total. |

El orden de entrega confirmado es **I0 → I1 → I4 → I5 → I2 → I3 → I6 → I7 → I8**. Se conservan los identificadores para mantener referencias anteriores; sus números ya no indican orden cronológico. Las evidencias básicas acompañan cada entrega; I7 añade su presentación e informes, no inicia por primera vez la trazabilidad. El primer ensayo del autoestudio ocurre en I4 y se repite al añadir funciones con entidad, sin esperar el examen ni I8. No reconstruir una función que ya existe: comprobar si satisface el incremento y reutilizarla.

### Contratos funcionales mínimos para los incrementos

**Examen y configuración.** La sesión usa una instantánea de preguntas, orden y política docente. Cambiar la actividad no cambia retroactivamente una sesión empezada. El profesor puede configurar una nueva versión para sesiones posteriores; retirada de permisos o fuentes conserva su efecto inmediato. ORALIA no reescribe preguntas, añade seguimientos académicos ni decide pasar de pregunta según corrección. Preguntas secundarias, si se quieren, se configuran por el docente. No hay selección adaptativa basada en capacidad inferida.

**Respuesta y navegación.** Distinguir texto en edición de respuesta confirmada. El alumno pulsa el botón de envío para confirmar; la futura versión oral mantiene también un botón explícito de fin de respuesta. No hay confirmación por silencio o juicio del modelo. Contenido exacto y sin corrección/reformulación automática. Saltar conserva la pregunta pendiente, continúa la ronda establecida y provoca vuelta al terminarla si el salto está habilitado. No implica permiso para editar respuestas ya confirmadas; esa es una capacidad distinta, no solicitada por esta aclaración. El cierre conserva las pendientes sin respuesta si el alumno decide terminar; no inventa respuestas ni emite juicios sobre vacíos. Probar retorno, aplazamientos repetidos y reconexión sin duplicar la cola ni alterar orden.

**Ayudas.** Aplicar la definición humana anterior: solicitud de ayuda o aclaración sobre la pregunta y respuesta de ayuda generada para comprenderla. Contabilizar una vez la ayuda válida producida, conservando identidad, pregunta, versión y entrega. Error previo a producir ayuda o candidato rechazado no consume. Un reenvío de la misma ayuda no consume otra unidad. Reentrada y vuelta no reinician límites. El profesor fija permiso y cantidad; la ayuda usa fuentes y política sin juzgar la respuesta del alumno ni resolver el ejercicio. Las instrucciones operativas de interfaz no cuentan como ayuda académica y no deben incluir pistas. El usuario no puede ampliar su cupo mediante instrucciones al modelo.

**Memoria entre modos.** Propuesta inicial: sesiones de autoestudio y examen separadas. No arrastrar historial de estudio, soluciones o estadísticas al contexto del examinador. No crear un perfil del estudiante al vincular las actividades. Cualquier relación entre sesiones para investigación necesita propósito y conservación explícitos. Preguntas, fuentes y ayudas del examen se muestran solo como lo permita su configuración.

**Datos descriptivos.** Diferenciar mensajes del alumno de preguntas académicas: un saludo no cuenta como pregunta sobre requisitos. Propuesta inicial: recuentos exactos de eventos y preguntas configuradas; para conceptos, vocabulario y reglas trazables con categoría «sin clasificar» y varios conceptos por consulta si procede. Documentar que una consulta puede contribuir a varias categorías; no sumar categorías como si fueran personas o consultas distintas. Separar repetición de un mismo request de una nueva pregunta real. No inferir dificultad, dominio ni aprendizaje de frecuencia, duración o ayudas. No añadir una encuesta o un clasificador LLM solo para obtener recuentos sencillos.

**Conservación.** Recopilar únicamente eventos mínimos y contenido permitidos. No usar analíticas como una segunda copia oculta de una transcripción no conservada. No publicar agregados o supuestos anónimos de un grupo pequeño por defecto. Exportaciones, acceso docente y purga deben mantener el alcance del consentimiento; el profesor no accede por ser profesor a toda sesión ajena.

**Rechazo y continuidad.** Distinguir insuficiencia, conflicto, fuente retirada, generación fallida y contenido rechazado. Un límite operativo explica opciones disponibles sin inventar hechos académicos. Proponer antes del ensayo el número máximo de ampliaciones/reintentos; conservar todos los intentos y revisar cada candidato nuevo. No reparar retrospectivamente salidas. La sesión no termina por una duda válida que no se pudo responder salvo condición de cierre prevista.

### Trabajo técnico y criterios que no deben bloquear incrementos independientes

El examen básico sin generación no depende de la comparación de modelos ni del detector especializado. Las estadísticas descriptivas no dependen de un evaluador del alumno. Los documentos pueden revisarse antes de indexarlos. Los episodios de autoestudio pueden evaluarse en laboratorio por el docente aunque aún no esté habilitado el participante. Ninguna de estas separaciones elimina controles de acceso, privacidad o vigencia.

LettuceDetect u otro detector sigue siendo candidato, no dependencia por nombre. Antes de cada ensayo real de generación se define una política de revisión compuesta, los errores que cada control detecta, su coste y lo que queda incierto. El diseño de publicación generativa puede avanzar en paralelo lógico a su medición; no se activa hasta la revisión de su resultado concreto. No es necesario resolver una garantía universal para iniciar I0–I3.

Antes de ejecutar investigación adicional, fijar una ficha breve: hipótesis, versiones, preguntas nuevas, particiones de desarrollo/transferencia, criterios de éxito/fallo, recursos y máximo de candidatos/llamadas/revisión. Si el presupuesto no permite decidir, registrar «inconcluyente» y presentar la inversión siguiente, no seguir automáticamente. Seguridad de entrega, parada de recursos y diagnóstico independiente tienen reglas distintas. Cero errores observados en un banco no se extrapola como garantía total.

### Lista para autorizar el primer bloque de implementación

El alcance funcional ya permite preparar un primer bloque orientado al **autoestudio**: conciliar el árbol detenido, verificar I0, preparar el corpus inicial I1 y obtener el recorrido RAG I4 para prueba docente. Son entregas separables y no una orden de ejecutarlas todas sin revisión. Después se mejora continuidad en I5 y se adapta la base al examen I2/I3/I6. No hace falta decidir ahora todas las métricas del piloto o elegir el detector para iniciar la preparación del corpus y verificar arranque; la salida generativa mantiene sus controles y límites explícitos.

Antes de encargarlo se registran el responsable único futuro, rutas que se modificarán, criterios del incremento y las comprobaciones existentes que los cubren. Las decisiones humanas de ayuda y aplazamiento se traducen a SpecKit sin reinterpretarlas como omisión irreversible o navegación libre. No se modifica ahora Feature 012 ni se declara aceptado el piloto. La orden actual es auditar y planificar; sigue sin autorizar reanudación o mensajes a otras tareas.
