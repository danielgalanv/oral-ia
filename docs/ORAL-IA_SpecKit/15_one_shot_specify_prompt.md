# Alternativa: una sola ejecución de `/speckit-specify`

Especifica el MVP completo de ORAL-IA, un sistema local multiagente de apoyo docente para autoestudio y ensayo de defensas orales. Debe ejecutarse en un único ordenador mediante una aplicación web local, con interacción textual completa y voz opcional. No incorporará robot, Internet durante sesiones, Moodle, expedientes, calificaciones, evaluación automática, detección de fraude, correo, calendario, perfiles longitudinales ni creación autónoma de agentes o código.

El MVP debe demostrar que agentes especializados, coordinados mediante un estado cognitivo compartido y combinados dinámicamente en agencias, ofrecen control, trazabilidad, adaptación y verificación superiores o al menos medibles frente a una llamada monolítica a un modelo de lenguaje.

## Experiencias de usuario

### Autoestudio

El estudiante puede consultar materiales autorizados, resolver dudas, pedir explicaciones y ejemplos, recibir preguntas de práctica, preparar una exposición y revisar conceptos. Las respuestas específicas de la asignatura se fundamentan en fragmentos recuperados y muestran fuentes. Si falta información, el sistema lo reconoce. El conocimiento general está prohibido por defecto y, cuando una actividad lo habilite, se etiqueta.

### Defensa oral

El sistema presenta una actividad, formula una pregunta, recibe respuesta por texto o voz, transcribe localmente, permite corregir la transcripción, analiza conceptos sin evaluar, recupera materiales y genera repreguntas relacionadas. Mantiene límites de turnos y duración, permite finalizar, revisar la transcripción y generar un resumen descriptivo. El audio se descarta y cualquier fallo de voz degrada a texto.

### Profesor

El profesor crea configuraciones versionadas, carga y activa materiales, define preguntas, temas, límites, idioma, modalidades, conocimiento general, conservación, modelos y agentes. Puede revisar sesiones consentidas, fuentes, transcripciones, correcciones, bloqueos, incidencias y trazabilidad; exportar datos autorizados y eliminar sesiones.

## Arquitectura funcional

Debe incluir núcleo constitucional, interfaz y sesiones, materiales, estado cognitivo, sociedad de agentes, composición de agencias, memoria diferenciada, metacognición y verificación, persistencia, trazabilidad y recursos.

Cada agente tiene contrato versionado con responsabilidad, entradas/salidas estructuradas, permisos, fuentes, herramientas, timeout, cancelación, confianza, errores, éxito y trazabilidad. Los agentes se ejecutan inicialmente como componentes del mismo sistema. Las agencias seleccionan agentes existentes, orden, parámetros y estrategia; no crean código.

El estado cognitivo, externo al contexto del LLM, conserva modo, objetivo, actividad, materiales, pregunta, respuesta, conceptos, intención, evidencia, dudas, historial resumido, límites, incidencias, confianza y siguiente acción. Sus cambios están versionados y atribuidos.

La sociedad mínima incluye gestión de sesión, intención, recuperación, respuesta fundamentada, generación de preguntas, repreguntas, diálogo, transcripción, síntesis, verificación de fundamentación, coherencia, control constitucional, resumen, trazabilidad y recursos.

La salida generada no puede mostrarse hasta superar verificación de fundamentación y constitucional. Debe detectar falta de evidencia, contradicción, repetición, pérdida de objetivo, baja confianza de transcripción, timeout, fallo de agente, consumo excesivo y ausencia de progreso. Puede volver a buscar, reformular, pedir aclaración, reconocer desconocimiento, cambiar a texto, usar un modelo alternativo autorizado o finalizar.

## Materiales y RAG

Admitir PDF textual, DOCX, PPTX, TXT y Markdown. El proceso valida, extrae, segmenta, genera metadatos, embeddings e índice, revisa y activa. Cada fragmento conserva documento, versión y ubicación. Materiales retirados no aparecen en sesiones nuevas. Deben detectarse falta de evidencia, referencias incorrectas y conflictos entre fuentes. No hay búsqueda web.

## Privacidad y accesibilidad

Usar códigos seudónimos, ejecución local, consentimiento, retención limitada y purga. Audio temporal y no conservado. Texto como modalidad completa, teclado, contraste, etiquetas, pausa, repetición, ritmo y mensajes claros. No almacenar razonamiento privado del modelo.

## Trazabilidad y validación

Registrar configuración, modelos, agentes, mensajes, cambios de estado, fuentes, verificaciones, decisiones, latencias, errores y recursos. Permitir reconstruir sesiones. Comparar baseline monolítico, agencia completa, verificadores y estrategias de recuperación con datos sintéticos o autorizados. Medir trazabilidad, fundamentación, bloqueos, fallos, latencia, recursos y utilidad percibida, sin evaluar estudiantes.

## Criterios de éxito

- Autoestudio y defensa comparten núcleo y agentes.
- Los agentes se recombinan sin modificar su implementación.
- El estado se mantiene fuera del contexto del modelo.
- Las salidas distinguen evidencia, conocimiento general y falta de información.
- Los verificadores bloquean salidas no fundamentadas o académicamente prohibidas.
- Las sesiones se reconstruyen desde registros.
- Los fallos degradan de forma controlada.
- Se añade un agente nuevo mediante contrato sin rediseñar el orquestador.
- Existe una comparación reproducible con baseline monolítico.
- El sistema funciona localmente con recursos y límites documentados.
