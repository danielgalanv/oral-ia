# Feature 001 — Núcleo cognitivo y ejecución local

Construye el primer incremento funcional de ORAL-IA: un núcleo cognitivo local, modular y trazable capaz de iniciar sesiones, registrar agentes, componer agencias predefinidas, mantener un estado cognitivo compartido y ejecutar un flujo mínimo sin depender todavía de materiales docentes reales, voz ni evaluación académica.

## Propósito

Esta feature debe demostrar que la arquitectura puede separar responsabilidades, coordinar agentes con contratos explícitos y reconstruir lo sucedido durante una sesión. El resultado debe ser una base operativa reutilizable por las features posteriores.

## Usuarios y objetivos

### Profesor o desarrollador administrador

Debe poder crear una configuración versionada de actividad con nombre, asignatura, objetivo, modo, idioma, límite de turnos, duración, conocimiento general permitido o prohibido, agentes obligatorios y opcionales, y política de conservación.

Debe poder consultar el catálogo de agentes y agencias disponibles, sus versiones, capacidades, permisos, contratos y estado de disponibilidad.

### Participante

Debe poder iniciar una sesión local con un código seudónimo y una actividad autorizada, visualizar que está interactuando con un sistema automático, intercambiar al menos mensajes de texto y finalizar la sesión voluntariamente.

### Investigador o mantenedor

Debe poder inspeccionar el flujo de ejecución, los agentes activados, los cambios del estado cognitivo, las decisiones, los errores, las latencias y los recursos básicos consumidos.

## Capacidades requeridas

1. Catálogo versionado de agentes y agencias.
2. Contrato común de agente con entradas y salidas estructuradas, precondiciones, postcondiciones, timeout, cancelación, confianza, error y trazabilidad.
3. Mensajes internos estructurados con identificador, sesión, emisor, receptor, tipo, objetivo, contenido, evidencias, fuentes, confianza, prioridad, vigencia, respuesta esperada y condición de éxito.
4. Pizarra cognitiva de sesión externa al contexto del LLM, con control de versiones y registro de cada cambio.
5. Gestor de sesión encargado de inicio, aplicación de configuración, turnos, duración, finalización y persistencia.
6. Compositor de agencias que seleccione agentes de un catálogo validado y determine un flujo predefinido; no puede crear código ni agentes nuevos durante la ejecución.
7. Selector de acción conversacional capaz de elegir entre responder con un mensaje controlado, solicitar aclaración, reconocer falta de información, resumir o finalizar.
8. Control constitucional capaz de bloquear mensajes que asignen notas, suplanten al profesor, emitan decisiones académicas, revelen datos no autorizados o se salgan del alcance.
9. Registro de trazabilidad por sesión, turno, agente y cambio de estado.
10. Monitor básico de tiempo de ejecución, CPU, memoria, errores y timeouts.
11. Degradación controlada cuando un agente falla, excede su tiempo o produce una salida inválida.
12. Interfaz web local mínima con área de participante y área técnica o docente suficiente para probar estas capacidades.

## Estado cognitivo mínimo

Debe incluir: modo activo, objetivo, actividad, materiales permitidos aunque todavía estén vacíos, pregunta o entrada actual, respuesta del participante, conceptos tratados y pendientes, hipótesis de intención, información recuperada, dudas, historial resumido, tiempo restante, número de turnos, incidencias, confianza y siguiente acción propuesta.

Cada elemento debe distinguir entre instrucción, observación, afirmación del participante, información recuperada, hipótesis, inferencia, decisión, resultado de comprobación y configuración.

## Escenarios prioritarios

### Escenario A — Sesión válida

Un profesor crea una actividad de prueba, un participante inicia una sesión con código seudónimo, envía un mensaje, el sistema ejecuta un flujo mínimo de gestión, interpretación simulada o determinista, control constitucional y presentación, actualiza el estado y registra toda la secuencia. El participante finaliza y se genera un resumen técnico básico.

### Escenario B — Salida bloqueada

Un agente de prueba propone una salida que contiene una nota o una decisión académica. El control constitucional la bloquea, registra la causa y devuelve un mensaje seguro sin mostrar la salida prohibida.

### Escenario C — Fallo de agente

Un agente excede el timeout o devuelve un objeto inválido. El sistema registra el fallo, evita corromper el estado, selecciona una alternativa configurada o finaliza el turno de forma segura y permite continuar o cerrar la sesión.

### Escenario D — Conflicto de escritura

Dos operaciones intentan actualizar la misma versión del estado. El sistema detecta el conflicto, no sobrescribe silenciosamente y conserva una secuencia reconstruible.

### Escenario E — Reinicio y reconstrucción

Tras cerrar o reiniciar la aplicación, un mantenedor puede abrir una sesión conservada y reconstruir su configuración, turnos, agentes ejecutados, decisiones y cambios de estado.

## Requisitos de privacidad y acceso

La aplicación debe vincularse por defecto únicamente a la máquina local. No requiere integración institucional ni identidad real. El código de participante no debe contener datos personales. No debe almacenar cadenas de razonamiento privadas de modelos.

## Fuera de alcance de esta feature

- ingestión e indexación real de documentos;
- RAG y citas docentes;
- preguntas y respuestas docentes completas;
- voz, transcripción y síntesis;
- revisión de transcripciones;
- evaluación de estudiantes;
- conexión a Internet o sistemas externos;
- ejecución distribuida y microservicios;
- creación autónoma de agentes o modificación del núcleo.

## Criterios de éxito

- Se pueden registrar al menos cinco agentes de prueba con el mismo contrato sin cambiar el orquestador.
- Se pueden definir al menos dos agencias diferentes reutilizando agentes.
- El estado permanece fuera del contexto del modelo y todos sus cambios son versionados.
- El flujo de un turno se reconstruye completamente desde los registros.
- Una salida académicamente prohibida es bloqueada antes de llegar al usuario.
- Un timeout o error de esquema produce degradación controlada y no corrupción del estado.
- Las pruebas demuestran aislamiento de responsabilidades y sustitución de agentes mediante contratos.
