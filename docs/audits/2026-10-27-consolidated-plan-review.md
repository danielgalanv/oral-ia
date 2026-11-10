# Auditoría del plan consolidado de ORALIA

Fecha: 27 de octubre de 2026. Objeto: [plan consolidado](../plans/2026-10-27-consolidated-action-plan.md), incluida la incorporación de autoestudio y examen oral con PDF docentes, NASA, INCOSE e Ian Sommerville.

Método: lectura completa del plan, contraste con decisiones humanas, auditorías previas, constitución y especificación activa de Feature 012. No se ejecutaron tests o modelos: esta revisión evalúa el plan, no certifica la implementación. No se modificó el plan auditado, requisitos o producción ni se enviaron instrucciones a otras tareas.

## Dictamen

**Actualización posterior del usuario:** queda descartada toda evaluación, puntuación y rúbrica del alumno por ORALIA. El profesor selecciona preguntas, ayudas y sus límites, y si permite salto/vuelta. Chat ahora, voz en siguiente versión. El asistente prepara el corpus; la interpretación del aprendizaje corresponde al profesor, con datos descriptivos opcionales de ORALIA. Se hará ensayo temprano al existir recorrido funcional. Estas decisiones resuelven la decisión A01 a favor del examinador que recoge evidencias y acotan A02–A05/A09; sus controles de implementación todavía deberán verificarse. El plan consolidado ya incorpora las decisiones. Los hallazgos siguientes conservan el estado y redacción de la auditoría inicial, no se leen como órdenes de introducir rúbricas.

**La dirección es adecuada, pero el plan todavía no está listo para convertirse íntegramente en una orden de implementación.** Reutiliza correctamente la base, separa recuperación/generación/revisión, conserva evidencia y orienta el trabajo al piloto. Sin embargo, tiene una ambigüedad de autoridad relevante para el examen, una dependencia demasiado rígida del verificador y varios paquetes que aún no tienen criterios operativos suficientes.

No hace falta otra auditoría global de todo el proyecto. Hace falta una revisión focal del plan con los cambios siguientes. «P0» en las prioridades indica una decisión previa a encargar el trabajo afectado; no significa que se haya encontrado una vulnerabilidad explotable en producción.

## Hallazgos

### A01 — P0 — El alcance del examinador no está conciliado con la constitución

**Evidencia:** el plan propone rúbrica, valoración del sistema y comparación con el docente. La constitución prohíbe asignar notas y, en su alcance MVP, excluye explícitamente «evaluación automática, notas o aplicación autónoma de rúbricas». Prohibir solo las calificaciones oficiales, como hace el plan, no resuelve esa exclusión más amplia.

**Riesgo:** implementar una capacidad no autorizada pensando que basta llamarla piloto. También puede producir una nueva cadena de bloqueos si se descubre al final.

**Corrección requerida:** definir dos componentes: (a) examinador que pregunta, hace seguimientos y conserva evidencias autorizadas; (b) valoración según criterios. Para (b), precisar si la realiza exclusivamente el docente o si se propone un evaluador automático de laboratorio para investigar. Una futura valoración autónoma necesita una decisión explícita y la actualización correspondiente de los artefactos, antes de habilitarla. No asumir ni la aprobación del cambio ni que el usuario quiere renunciar a él.

**Aceptación de la corrección:** tabla de capacidades permitidas por modo, responsable de cada juicio y referencia a la autoridad vigente. Autoestudio puede avanzar sin resolver una ampliación del examinador.

### A02 — P1 — «Examen oral por chat» debe ser un hito intermedio explícito

**Evidencia:** el plan reconoce que texto no valida voz, pero denomina al conjunto piloto de examen oral y mantiene voz fuera de todo el piloto.

**Riesgo:** confundir validar la lógica de entrevista por escrito con haber probado un examen hablado. Esto altera el objeto que se podría afirmar al terminar.

**Corrección requerida:** distinguir tres resultados: autoestudio por chat; entrevista de examen por chat como validación del diálogo; examen oral hablado posterior. Mantener voz aplazada como decidió el usuario. Si se quiere que el primer piloto humano incluya habla, eso requiere una fase posterior y no se da por autorizado ni implementado.

**Aceptación:** cada informe identifica modalidad real y qué resultados no pueden transferirse de texto a voz.

### A03 — P1 — Falta un paquete de incorporación del corpus externo

**Evidencia:** hay enlaces, metadatos y cautelas, pero P0/P4 no delimitan una entrega verificable para búsqueda, selección, adquisición, revisión, traducción y activación de NASA/INCOSE/Sommerville.

**Riesgo:** los ensayos siguen usando un catálogo parcial mientras el plan aparenta disponer del corpus ampliado; o se toman recursos externos como autoridad que cambia el temario.

**Corrección requerida:** añadir un paquete propio, antes del banco RAG final, con inventario de recursos concretos y estado: localizado, utilizable, adquirido, extraído, revisado, activado. Registrar edición/condiciones y mapa concepto→pasajes. Revisar diferencias terminológicas y de nivel sistema/software. Conservar texto original, y tratar traducciones como representación derivada identificada. No fusionar recomendaciones contextuales en una regla universal ni considerar todos los documentos de una organización autorizados por asociación.

**Aceptación:** manifiesto de corpus de la actividad, cobertura y conflictos adjudicados; documentos no incorporables tienen alternativa o límite visible. Las diapositivas del curso fijan alcance docente, pero una discrepancia académica no se resuelve automáticamente ignorando otras fuentes.

### A04 — P1 — Los objetivos de aprendizaje y el mapa del examen siguen demasiado abstractos

**Evidencia:** el plan pide objetivos observables y rúbrica, sin descomponer todavía qué comprensión de requisitos se va a observar.

**Riesgo:** optimizar otra vez unos pocos pares terminológicos conocidos y llamarlo cobertura del tema completo.

**Corrección requerida:** proponer un mapa revisable que incluya, según material disponible: necesidades y requisitos; tipos y restricciones; obtención/negociación; especificación y calidad; validación y verificabilidad; trazabilidad/cambio. Para cada objetivo: reconocer, explicar, aplicar a un caso y justificar una decisión. No se presume que todo sea obligatorio ni que ese listado sustituya el programa docente.

**Aceptación:** matriz objetivo→fuentes→familia de pregunta→evidencia esperada→modo. Las evidencias esperadas y errores típicos son criterios de revisión; no respuestas que sustituyan la generación del tutor. El examen tiene cobertura y nivel de demanda previstos, no una secuencia arbitraria elegida por el modelo.

### A05 — P1 — Faltan controles específicos de ayudas, filtración y variabilidad del examen

**Evidencia:** se menciona no filtrar la solución y registrar ayudas, pero no se diseña la frontera entre autoestudio y examen ni el control de seguimientos adaptativos.

**Riesgo:** el historial de práctica revela una solución de evaluación; las fuentes visibles durante el examen entregan la respuesta; los seguimientos cambian dificultad o inducen al alumno sin contabilizarlo.

**Corrección requerida:** definir si el examen permite fuentes y qué ayudas son válidas; qué memoria pasa entre modos; cuándo se muestra la devolución; qué puede aclarar el examinador sin enseñar la respuesta; máximo de seguimientos y condiciones de cierre. Separar ejemplos de entrenamiento de casos de evaluación equivalentes. Mantener variedad sin exigir preguntas idénticas a todos.

**Aceptación:** casos de aclaración, silencio, respuesta parcial, rectificación, solicitud de pista y cambio de modo; revisión de cobertura y dificultad de las rutas generadas. Las fuentes y soluciones del examinador no se revelan cuando el protocolo las reserva. No penalizar longitud, estilo escrito o coincidencia literal como si fueran comprensión.

### A06 — P1 — El detector de respaldo no puede convertirse en el único cuello de botella de toda validación

**Evidencia:** P6 exige candidatas defendibles de P5 y dice que sin un revisor viable solo hay diagnóstico; a la vez, el plan afirma que no se necesita un verificador universal. La constitución exige controles externos observables, pero no prescribe LettuceDetect ni un único modelo árbitro.

**Riesgo:** repetir el bloqueo histórico: otro detector falla y se detiene todo el avance, aunque otras partes puedan medirse. O abrir el gate solo porque un detector pase una muestra.

**Corrección requerida:** describir una política de revisión compuesta, versionada: procedencia y acceso deterministas, señal de respaldo calibrada cuando exista, controles de pertinencia/cobertura y abstención. Indicar qué señal respalda cada clase de error y qué queda sin resolver. El detector especializado es una opción de P5b, no una dependencia arquitectónica obligatoria del producto. Permitir evaluar episodios completos en laboratorio con revisión humana posterior aun sin permiso de entrega a estudiantes.

**Aceptación:** diagrama de decisiones y matriz error→control→evidencia→acción. Ningún control se presenta como garantía universal; tampoco se eluden los gates vigentes. Si la política compuesta no alcanza los criterios acordados, la salida participante sigue cerrada.

### A07 — P1 — Falta decidir el comportamiento después de un rechazo

**Evidencia:** hay abstención, insuficiencia y conservación del primer fallo, pero no una política conversacional completa ante candidato rechazado.

**Riesgo:** el alumno recibe un cierre seguro o un bloqueo genérico tras una pregunta legítima, repitiendo un problema ya observado en la demo. También existe el riesgo contrario de reintentos ilimitados y reparación opaca.

**Corrección requerida:** separar fallo de generación, error semántico detectado, evidencia insuficiente, conflicto y retirada. Proponer qué admite ampliación de búsqueda, una reformulación acotada, aclaración o devolución del límite. Cualquier reparación es un intento nuevo registrado y revisado; nunca modifica la salida histórica ni se incorpora al historial sin mostrarse. Congelar su presupuesto antes de probar.

**Aceptación:** el usuario conserva control de la sesión, sabe qué puede hacer y puede continuar/cerrar. Se mide frecuencia y coste de abstenciones y recuperaciones; no basta con cero salidas erróneas a costa de no responder.

### A08 — P1 — Los criterios son razonables, pero no bastan para tomar decisiones reproducibles

**Evidencia:** faltan tamaño/diversidad del banco, responsables de revisión, umbrales de positivos y reglas de adjudicación. «Cualquier error crítico bloquea» aparece sin distinguir una corrección de seguridad de una comparación diagnóstica.

**Riesgo:** decidir después de ver resultados, o detener todo un banco al primer fallo sin conocer la distribución de errores. El plan conserva esa ambigüedad aunque permita casos independientes.

**Corrección requerida:** fijar antes del ensayo el diseño del banco, unidades de análisis (afirmación, turno, episodio), particiones por escenario/familia para evitar contaminación, métricas y reglas de selección. Distinguir parada de entrega, parada por recursos y finalización del diagnóstico independiente. Clasificar omisión, error central, incumplimiento de formato y salida no ejecutada por separado.

**Aceptación:** ficha de evaluación con criterios prospectivos y autoridad para adjudicar. Reportar numeradores/denominadores y límites de muestra; cero fallos observados no prueba riesgo cero. No hacen falta cifras universales inventadas, pero sí propuestas concretas antes de encargar inferencias.

### A09 — P1 — El diseño de eficacia y la validez del examinador deben separarse

**Evidencia:** se menciona evaluación previa/posterior y revisión docente, sin detallar cómo evitar que el examinador sea a la vez intervención y única medida de resultado.

**Riesgo:** concluir aprendizaje porque el mismo sistema que enseñó juzga mejor una respuesta familiar; o confundir diferencias de dificultad con cambios de comprensión.

**Corrección requerida:** dos preguntas de investigación: (1) si el autoestudio ayuda a comprender/aplicar, observado con una tarea sin ayuda y revisión docente; (2) si el examinador obtiene evidencias pertinentes y comparables, y, solo si está autorizado, si su valoración concuerda con la docente. Registrar conocimiento previo, exposición, ayudas y problemas técnicos. Considerar orden de actividades y reutilización de preguntas para evitar práctica/carryover. Plantear comparación o contrabalanceo proporcionados al tamaño real, sin prometer potencia estadística inexistente.

**Aceptación:** protocolo que identifica resultado principal, medidas secundarias y límites de inferencia. La revisión de muestras no usa al juez automático como oráculo de su propia validez.

### A10 — P1 — Falta un presupuesto de investigación y una regla global de abandono

**Evidencia:** existen límites por ensayo y una propuesta de 7B/14B, pero no techo de candidatos, de revisiones o de esfuerzo total de la fase de viabilidad.

**Riesgo:** continuar la sucesión de bancos, prompts y contratos que ha retrasado la conversación usable. La propuesta histórica puede no seguir siendo la comparación de mayor valor al cambiar corpus/objetivos.

**Corrección requerida:** en P0 proponer una hoja de inversión: preguntas que se quiere resolver, candidatos máximos, recursos locales/nuevos, horas de revisión y puntos de decisión. Revisar la validez de la propuesta 7B/14B sin reescribirla; un sucesor justificado tiene presupuesto distinto. Cada candidato adicional necesita una hipótesis que no esté ya refutada, no solo mayor tamaño o un prompt distinto.

**Aceptación:** límite acordado antes de pruebas; al agotarlo se entrega decisión de continuar investigación, cambiar configuración o mantener capacidad no disponible. Sin fecha o coste inventados como compromiso.

### A11 — P2 — Se necesita un checklist de preparación operativa ligado al entorno real

**Evidencia:** hay recuperación y recorrido, pero no una entrega compacta que cubra arranque desde la cuenta habitual, dependencias fuera del PATH de Codex, acceso, participantes simultáneos o secuenciales y ayuda al usuario.

**Riesgo:** repetir «Node ausente», credenciales inesperadas o sesión interactiva ocupada en el día del piloto pese a tests verdes. Son incidentes históricos concretos, no trabajo de explotación a gran escala.

**Corrección requerida:** ensayo de instalación/arranque desde el terminal del usuario, documentos de prueba reales, sesión nueva, reconexión y cierre; definir si los estudiantes usan el equipo local secuencialmente o un acceso distinto. LAN no se añade por defecto. Incluir ruta accesible por teclado, espera/cancelación y contacto con el responsable del piloto.

**Aceptación:** ensayo general en la topología real, con instrucciones legibles y recuperación sin Reset ni eliminación de sesiones ajenas. Configuración congelada para la prueba humana.

### A12 — P2 — Falta un registro explícito de cambios a requisitos y responsabilidades

**Evidencia:** la tabla B01–B18 asegura cobertura temática, pero no asigna a cada entregable un responsable, revisor, artefacto y evidencia de cierre. Se remite a SpecKit sin precisar qué modificaciones requieren decisión humana.

**Riesgo:** otro índice voluminoso de tareas sin distinguir implementación de aceptación, o cambios silenciosos de alcance al conciliar los 418 IDs.

**Corrección requerida:** por paquete: requisito humano, IDs afectados, entregable, criterio, responsable y revisor futuro, dependencia y decisión pendiente. Preparar una lista focal de cambios materiales (examen/valoración, corpus externo, autorización generativa, repeticiones y alcance del piloto). No modificar los 418 requisitos como condición previa ni exigir otro cierre global.

**Aceptación:** cada paquete puede cerrarse con evidencia finita; la aprobación técnica no marca revisión docente o humana. Los responsables pueden quedar por designar mientras no se reanude; no se crean tareas ahora.

## Reordenación propuesta

1. **Definir lo que se evaluará:** dos fichas, capacidades del examinador, mapa de objetivos, modalidad y topología. Preparar decisiones de alcance sin implementar.
2. **Congelar base real y criterios:** qué ya está corregido, defectos pendientes, bancos y presupuesto de investigación. No volver a descubrir lo ya demostrado.
3. **Preparar corpus y controles:** fuentes concretas, QA, terminología y referencias. En paralelo lógico, terminar fundamentos/privacidad que no dependen de contenido.
4. **Diagnosticar generación y recuperación por separado:** evidencia fija para capacidad y banco de recuperación para ranking. Reutilizar las piezas existentes.
5. **Evaluar política compuesta de revisión y recuperación tras rechazo:** candidato especializado solo si encaja; episodios de laboratorio revisados aunque todavía no haya permiso participante.
6. **Evaluar ambos modos completos:** autoestudio y entrevista de examen, con ayudas/memoria separadas y condiciones comparables.
7. **Acordar contrato y aceptación del resultado concreto:** el diseño empieza antes; la activación espera evidencia. No diseñar un gate para una señal que aún no existe ni presentar un detector como imprescindible por su nombre.
8. **Ensayo general y piloto humano autorizado:** medidas de aprendizaje separadas de validez del examinador, configuración estable y criterios de parada.

No son ocho nuevas features ni órdenes de trabajo. Es el orden de decisiones recomendado para corregir el plan actual.

## Qué ya está bien y debe mantenerse

- Objetivo acotado de piloto; ausencia de obligación de explotación, voz o cobertura total previa.
- Fuentes autorizadas, ficción coherente y referencias visibles comprensibles.
- Reutilización del monolito y adaptadores; no apostar por más agentes o GraphRAG sin necesidad.
- Separación de generación, recuperación, autoridad y revisión.
- Preservación de originales, primeros fallos, presupuestos y reserva; sin Reset, commits o procesos ajenos.
- Compatibilidad, regresión por impacto y distinción entre fixture, prueba real, revisión docente y utilidad humana.

## Resultado de la auditoría

Se identifican doce mejoras del plan: una decisión P0, nueve P1 y dos P2. Son deficiencias de planificación, no doce defectos nuevos del código. El plan se puede corregir sin reescribir el proyecto ni repetir la auditoría completa. La implementación permanece detenida y no se ha comunicado trabajo a otras tareas.
