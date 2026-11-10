# Texto para `/speckit-constitution`

Establece la constitución del proyecto ORAL-IA, un sistema local multiagente de apoyo al autoestudio y al ensayo de defensas orales. Esta constitución debe gobernar todas las especificaciones, planes, tareas, implementaciones y revisiones del repositorio.

## I. Finalidad y límites institucionales

ORAL-IA es un asistente automático de apoyo docente. Debe identificarse siempre como sistema de IA, reconocer que puede cometer errores y permanecer dentro de la actividad y de los materiales autorizados. No puede presentarse como profesor, asignar notas, emitir decisiones académicas, aplicar rúbricas de forma autónoma, inferir capacidad académica o sustituir el criterio del profesorado.

La versión mínima funciona localmente en un ordenador y no incorpora robots, control de dispositivos físicos, acceso abierto a Internet durante las sesiones, Moodle, expedientes académicos, correo, calendario ni otros sistemas personales o institucionales.

## II. Arquitectura modular basada en contratos

Toda capacidad cognitiva relevante debe pertenecer a un agente con responsabilidad única y explícita. Cada agente debe declarar, mediante un contrato versionado: identificador, versión, propósito, entradas, salidas estructuradas, precondiciones, postcondiciones, fuentes y herramientas permitidas, permisos, tiempo máximo, consumo esperado, errores posibles, confianza, criterios de éxito, terminación, cancelación y datos de trazabilidad.

Los agentes pueden ejecutarse dentro de un mismo proceso. La modularidad se demuestra mediante límites de software, esquemas y pruebas, no mediante microservicios prematuros. Ningún agente puede depender de detalles internos de otro agente ni intercambiar únicamente texto libre cuando exista un esquema estructurado adecuado.

## III. Estado cognitivo explícito y memoria diferenciada

El estado relevante de una sesión debe mantenerse fuera del contexto privado del modelo de lenguaje, en una pizarra cognitiva estructurada, versionada y reconstruible. Toda modificación debe identificar al agente responsable, la versión previa, la versión resultante, el instante y la justificación.

El sistema debe distinguir como mínimo memoria de trabajo, memoria episódica de sesión, memoria semántica de materiales, memoria procedimental de agentes y agencias, y memoria metacognitiva de fallos y verificaciones. No debe crear durante el MVP perfiles psicológicos o académicos longitudinales del estudiante.

## IV. Separación entre recuperación, generación, decisión y verificación

Recuperar evidencias, generar una propuesta, decidir la siguiente acción conversacional y autorizar la presentación son responsabilidades separadas. El agente generador nunca puede aprobar por sí solo su salida.

Toda salida docente debe pasar, como mínimo, por controles de fundamentación y constitucionales. Los verificadores deben poder aprobar, reformular, pedir aclaración, marcar incertidumbre o bloquear. La reflexión verbal de un modelo no constituye por sí sola una verificación; deben preferirse comprobaciones externas y observables.

## V. Fundamentación en materiales autorizados

Las afirmaciones específicas de la asignatura deben sustentarse preferentemente en materiales autorizados, activos y vigentes. El sistema debe conservar la procedencia de los fragmentos usados y mostrarla al usuario cuando corresponda.

El conocimiento general del modelo está desactivado por defecto. Solo puede utilizarse si la configuración versionada de la actividad lo permite y debe etiquetarse claramente como conocimiento general no recuperado de los materiales. Cuando no haya evidencia suficiente, el sistema debe reconocerlo en lugar de inventar una respuesta.

## VI. Supervisión humana y gobernanza

El profesorado controla materiales, actividades, preguntas iniciales, límites, agentes obligatorios u opcionales, modelos, conservación de sesiones y eliminación de datos. Las reglas fundamentales no pueden ser modificadas por agentes durante una sesión. Toda modificación de la constitución, políticas, contratos o configuraciones debe ser manual, versionada y auditable.

Las K-lines o configuraciones cognitivas reutilizables pueden proponerse automáticamente, pero no consolidarse ni activarse permanentemente sin revisión humana durante el MVP.

## VII. Privacidad, minimización y accesibilidad

La ejecución, recuperación, inferencia y transcripción deben realizarse localmente. Los participantes se representan mediante códigos seudónimos. El audio se procesa y descarta; no se conserva por defecto. Las transcripciones solo se almacenan con consentimiento explícito, son revisables y corregibles, tienen retención limitada y pueden eliminarse.

La modalidad textual debe permitir realizar todas las funciones esenciales. La interfaz debe ser utilizable mediante teclado, ofrecer etiquetas accesibles, contraste adecuado, control del ritmo, pausa, repetición, corrección de transcripción y mensajes de error comprensibles. La voz es opcional y nunca un requisito de acceso.

## VIII. Trazabilidad y reproducibilidad

Toda respuesta o acción relevante debe poder relacionarse con la sesión, configuración, versión del sistema, modelo y parámetros, agentes ejecutados, mensajes internos, cambios de estado, fragmentos recuperados, verificaciones, decisiones, latencias, errores y consumo de recursos.

La reproducción significa reconstruir el flujo, los datos y las decisiones a partir de registros. No se debe prometer identidad byte a byte de salidas generativas salvo que se hayan fijado modelo, versión, semilla y condiciones deterministas.

Los registros no deben almacenar datos personales que no sean necesarios ni cadenas de razonamiento privadas del modelo. Deben registrar resultados estructurados y justificaciones operativas observables.

## IX. Degradación controlada y límites de recursos

Cada agente y sesión debe disponer de límites explícitos de tiempo, memoria, contexto, iteraciones, recuperaciones, almacenamiento y llamadas al modelo. Los fallos deben transformarse en estados conocidos y trazables, no en bloqueos silenciosos.

Cuando un componente no esté disponible, el sistema debe degradarse de forma explícita: pasar de voz a texto, reducir contexto o recuperación, desactivar análisis secundarios, usar un modelo alternativo autorizado, aplazar resúmenes o finalizar de forma segura. Los controles constitucionales y de privacidad nunca pueden omitirse por ahorro de recursos.

## X. Calidad, pruebas y evidencia

Cada requisito funcional debe poseer criterios de aceptación observables. Cada agente debe disponer de pruebas unitarias de contrato; cada agencia, pruebas de integración; cada flujo prioritario, una prueba extremo a extremo. Deben existir pruebas de fallo, cancelación, timeout, datos insuficientes, conflicto entre fuentes, degradación y bloqueo constitucional.

La arquitectura debe compararse con un baseline monolítico cuando proceda. Las métricas evaluarán el sistema y su arquitectura, no la capacidad o personalidad del estudiante.

No se considera terminada una feature si no incluye código, pruebas, trazabilidad, documentación mínima, migraciones o datos de ejemplo necesarios, manejo de errores, comprobación de privacidad y evidencia de que satisface sus escenarios de aceptación.

## XI. Simplicidad evolutiva

Debe implementarse la solución más sencilla que preserve los contratos y permita medir la hipótesis arquitectónica. Se evitarán frameworks de agentes, colas, bases de datos o servicios distribuidos que oculten el comportamiento o compliquen la reproducibilidad sin aportar una necesidad demostrable.

Toda dependencia nueva debe justificar qué requisito satisface, qué alternativa más simple se descartó y cómo se sustituiría mediante un adaptador. Los componentes de inferencia, embeddings, vectorización, transcripción y síntesis deben quedar detrás de interfaces reemplazables.

## XII. Gobierno de la constitución

La constitución prevalece sobre decisiones locales de una feature. Las excepciones requieren una enmienda explícita con motivación, impacto, alternativa considerada y plan de migración. Los cambios incompatibles en contratos, estado cognitivo, políticas o esquemas persistidos requieren versionado y pruebas de compatibilidad o migración.

En cada revisión se debe comprobar: conformidad con la constitución, cobertura de requisitos, límites de alcance, privacidad, trazabilidad, pruebas, recursos, degradación y documentación. La constitución se versionará con numeración semántica y fecha de ratificación o última enmienda.
