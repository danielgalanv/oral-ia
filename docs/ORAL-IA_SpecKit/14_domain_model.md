# Modelo de dominio y vocabulario estable

## Entidades principales

### Course / Asignatura

Contenedor lógico de actividades y materiales. No representa matrícula ni expediente institucional.

### ActivityConfiguration / Configuración de actividad

Definición versionada e inmutable una vez utilizada: objetivo, modos, materiales, preguntas, límites, idioma, modalidades, conocimiento general, retención, modelos y agentes.

### ParticipantCode / Código de participante

Identificador seudónimo sin identidad real incorporada.

### Session / Sesión

Ejecución de una actividad bajo una versión concreta de configuración. Incluye estado, turnos, consentimiento, recursos e incidencias.

### Turn / Turno

Unidad de interacción con entrada, interpretación, evidencias, agentes, verificaciones, acción, salida y métricas.

### Agent / Agente

Componente con responsabilidad cognitiva única y contrato versionado.

### Agency / Agencia

Composición versionada de agentes, pasos, condiciones, verificadores, fallback y terminación para un escenario.

### AgentContract / Contrato de agente

Esquema de responsabilidad, entrada, salida, permisos, límites, éxito, error y trazabilidad.

### InternalMessage / Mensaje interno

Objeto estructurado intercambiado entre agentes u orquestador.

### CognitiveState / Estado cognitivo

Representación estructurada y versionada de lo relevante durante la sesión.

### StatePatch / Parche de estado

Cambio propuesto por un agente, validado y aplicado contra una versión conocida.

### Memory

- trabajo: estado activo;
- episódica: acontecimientos de sesión;
- semántica: materiales y conceptos;
- procedimental: agentes, agencias, flujos y reglas;
- metacognitiva: fallos, bloqueos, contradicciones y recuperaciones.

### KLine

Configuración cognitiva reutilizable que referencia situación, agentes, orden, materiales, estrategia, resultado e incidencias. No es código autogenerado.

### MaterialDocument / Documento

Archivo docente versionado, procesado y autorizado.

### MaterialFragment / Fragmento

Unidad recuperable con texto, ubicación, metadatos, embedding y autorización heredada.

### Evidence / Evidencia

Fragmento o resultado verificable que respalda una afirmación o decisión.

### GeneratedProposal / Propuesta generada

Salida candidata que todavía no está autorizada para mostrarse.

### VerificationResult / Resultado de verificación

Clasificación y razones observables: aprobado, reformular, aclarar, bloquear, fundamentación parcial, conflicto o no verificable.

### DialogueAction / Acción de diálogo

Responder, preguntar, repreguntar, aclarar, reconocer falta de información, resumir o finalizar.

### Transcript / Transcripción

Texto producido por STT con segmentos, confianza y marcas temporales opcionales.

### TranscriptCorrection / Corrección

Versión aportada por el participante que no elimina la transcripción original cuando la sesión se conserva.

### TraceEvent / Evento de trazabilidad

Registro estructurado de ejecución, decisión, cambio de estado, error, fuente, verificación o recurso.

### ConsentRecord / Consentimiento

Decisión versionada sobre conservación y uso de datos.

### RetentionPolicy / Política de retención

Reglas versionadas de contenido, plazo, acceso y purga.

### ExperimentRun / Ejecución experimental

Ejecución reproducible de escenario, configuración, variante arquitectónica y entorno.

## Términos que no deben confundirse

- **Agente** no significa proceso independiente.
- **Agencia** no significa entidad externa ni organización humana.
- **Evaluación arquitectónica** no significa evaluación académica.
- **Resumen descriptivo** no significa calificación.
- **Confianza de transcripción o recuperación** no significa confianza en la capacidad del estudiante.
- **Reproducción** no implica identidad textual de una generación no determinista.
- **Conocimiento general permitido** no se considera material autorizado y debe etiquetarse.
