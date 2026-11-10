# Feature 003 — Agencia de autoestudio

Añade una experiencia completa de autoestudio por texto construida sobre el núcleo cognitivo y el sistema de materiales autorizados. La misma sociedad de agentes debe combinarse dinámicamente para resolver dudas, ofrecer explicaciones guiadas, generar preguntas de práctica, preparar una exposición y revisar conceptos.

## Propósito

Permitir que un estudiante consulte y practique con materiales seleccionados por el profesorado, obteniendo respuestas trazables y prudentes sin evaluación automática ni sustitución del profesor.

## Modos de autoestudio

1. Resolución de dudas.
2. Explicación guiada.
3. Preguntas de práctica.
4. Preparación de una exposición.
5. Revisión de conceptos.

Cada actividad docente debe poder habilitar solo algunos modos.

## Agentes mínimos de la agencia

- gestión de sesión;
- interpretación de intención;
- recuperación documental;
- respuesta fundamentada;
- generación de preguntas;
- gestión de diálogo;
- comprobación de fundamentación;
- coherencia conversacional;
- control constitucional y de seguridad;
- resumen de sesión;
- trazabilidad y recursos.

El orquestador debe seleccionar los agentes necesarios para cada turno y registrar por qué los activó. No es obligatorio ejecutar todos los agentes en todos los turnos, salvo los controles definidos como no omitibles.

## Comportamiento esperado

El estudiante inicia una actividad autorizada, conoce el propósito y los límites, formula una consulta y recibe una respuesta o una acción alternativa. El sistema interpreta la intención como hipótesis con confianza, recupera material cuando corresponde, genera una propuesta, verifica su fundamentación y conformidad, selecciona la acción conversacional y actualiza el estado.

El estudiante puede pedir una explicación más sencilla, un ejemplo, una comparación, una pregunta de práctica, un cambio de tema dentro del alcance o la finalización. El sistema debe recordar los conceptos tratados y evitar repetición innecesaria sin depender de reenviar todo el historial al modelo.

## Preguntas de práctica

Las preguntas deben derivarse de objetivos, conceptos, materiales, dificultad orientativa e historial de preguntas. Deben poder solicitar explicación, aplicación, comparación, justificación o detección de errores. No deben revelar automáticamente la solución cuando el modo de actividad lo prohíba.

La respuesta del estudiante puede utilizarse para seleccionar la siguiente acción o repregunta, pero no para producir una nota, clasificación o inferencia permanente de nivel.

## Coherencia y metacognición

El sistema debe detectar falta de información, respuesta no fundamentada, contradicción, repetición, pérdida del objetivo, exceso de turnos, fallo de agente, latencia excesiva y ausencia de progreso. Debe poder volver a recuperar, reformular, pedir aclaración, reconocer desconocimiento, reducir la respuesta o finalizar de forma segura.

## Fuentes visibles

Cuando una respuesta use materiales, el estudiante debe poder abrir una vista de fuentes con documento, versión, ubicación y fragmento relevante. Si se utiliza conocimiento general permitido, debe mostrarse una indicación diferenciada.

## Escenarios prioritarios

### Escenario A — Duda cubierta

El estudiante plantea una duda contenida en los materiales. El sistema recupera evidencias, genera una explicación, la verifica, muestra las fuentes y conserva el concepto tratado en el estado.

### Escenario B — Duda fuera de materiales

La actividad prohíbe conocimiento general y la duda no está cubierta. El sistema reconoce la falta de información y puede pedir una aclaración o sugerir consultar al profesor, sin inventar una respuesta.

### Escenario C — Explicación adaptada al turno

El estudiante indica que no ha entendido y pide un ejemplo. El sistema interpreta el cambio de intención, evita repetir literalmente la respuesta anterior y genera un ejemplo fundamentado o reconoce que no hay material suficiente.

### Escenario D — Práctica sin calificación

El estudiante solicita preguntas de práctica. El sistema formula preguntas pertinentes, recibe respuestas y continúa con aclaraciones o repreguntas, pero no asigna notas ni emite juicios académicos.

### Escenario E — Contradicción

Una propuesta contradice una afirmación previa o una fuente activa. El verificador de coherencia o fundamentación la bloquea o reformula y registra la incidencia.

### Escenario F — Límite de sesión

Se alcanza el número máximo de turnos o la duración. El sistema avisa, permite cerrar ordenadamente y genera, si está autorizado, un resumen descriptivo sin evaluación.

## Resumen de sesión

Puede incluir temas tratados, preguntas realizadas, conceptos explicados, dudas manifestadas, incidencias y fuentes consultadas. No puede incluir notas, diagnóstico de nivel, personalidad, capacidad ni recomendaciones académicas automatizadas basadas en inferencias no autorizadas.

## Fuera de alcance

- voz y transcripción;
- simulacro formal de defensa oral;
- evaluación, notas o rúbricas;
- perfil longitudinal del estudiante;
- acceso a Internet;
- integración con LMS;
- recomendaciones que impliquen decisiones académicas.

## Criterios de éxito

- Los cinco submodos comparten agentes y estado sin duplicar el núcleo.
- Toda respuesta específica de la asignatura está citada o marcada como no fundamentada/conocimiento general permitido.
- El sistema selecciona al menos tres composiciones distintas de agentes en escenarios de prueba.
- Las salidas prohibidas son bloqueadas antes de mostrarse.
- El historial resumido y el estado permiten mantener continuidad sin reenviar toda la conversación.
- Las sesiones terminan de manera controlada y producen una traza completa.
