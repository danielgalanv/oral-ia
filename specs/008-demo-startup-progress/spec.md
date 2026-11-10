# Feature Specification: Progreso del arranque demo

**Feature Branch**: 008-demo-startup-progress (sin Git ni commits)
**Created**: 2026-10-18
**Status**: Implementada y validada; analyze sin críticos y converge sin brechas
**Input**: Mejorar únicamente información y duplicación innecesaria del arranque local007.

## User Scenarios & Testing

### User Story 1 — Saber qué ocurre (Priority: P1)

Presentador distingue comprobación, preparación, espera y disponibilidad sin abrir logs.
**Why this priority**: Evitar interpretar una carga normal como bloqueo.
**Independent Test**: Arranque full y textual con mensajes observables en orden real.
**Acceptance Scenarios**:
1. Given recursos locales, When arranca full, Then ve dependencias/puertos, embeddings, datos/índice, inicio API/interfaz y espera; solo tras comprobar ambos servicios ve URL e instrucciones de parada.
2. Given TextOnly, When arranca, Then no se anuncia carga de embeddings ni fuentes disponibles.
3. Given una operación larga, When sigue ejecutándose, Then recibe avisos espaciados con tiempo transcurrido, sin porcentaje ni estimación restante.

### User Story 2 — Resolver fallo o cancelar (Priority: P1)

Presentador reconoce etapa fallida y siguiente acción sin exposición de secretos.
**Why this priority**: Seguridad y diagnóstico honesto.
**Independent Test**: Puerto ocupado, error desconocido, timeout y cancelación.
**Acceptance Scenarios**:
1. Given puerto ocupado, When comprueba/arranca, Then identifica etapa y acción; no cierra procesos ni cambia puerto.
2. Given fallo desconocido, When ocurre, Then reconoce causa no determinada y deriva a diagnóstico sin inventar explicación.
3. Given espera larga, When cancela, Then cesan avisos y solo se limpian hijos propios, sin falso mensaje de etapa completada.

### User Story 3 — Mantener el recorrido existente (Priority: P1)

Preparador usa opciones y comprobaciones anteriores sin modificar datos ni políticas.
**Why this priority**: Mejora acotada compatible con007.
**Independent Test**: Check, check-demo y ensayo real con hashes/centinela.
**Acceptance Scenarios**:
1. Given Check, When ejecuta, Then no solicita credencial ni inicia servicios y conserva salida final de diagnóstico estructurado.
2. Given demo preparada, When arranca y para dos veces, Then no requiere Reset, conserva datos/índice/fixtures y procesos ajenos.

## Edge Cases

Dependencia/recurso ausente, puerto ocupado, operación concurrente, preparación fallida,
timeout, hijo terminado, Ctrl+C antes/después de pedir credencial, salida redirigida.
La espera es estado conocido de operación en curso, no afirmación de avance interno.

## Requirements

- **FR-001**: Mostrar en español las etapas reales de comprobación dependencias/puertos, embeddings cuando corresponda, preparación demo, inicio API, inicio interfaz y espera de disponibilidad. Separar proceso iniciado de servicio listo.
- **FR-002**: Durante operaciones largas mostrar tiempo transcurrido cada5s aproximadamente, advertir carga inicial lenta, sin porcentajes/ETA ni saturación. El aviso termina al finalizar/fallar/cancelar su etapa.
- **FR-003**: Anunciar DEMO LISTA con URL e instrucciones solo tras verificar ambos servicios propios; navegador después, respetando NoBrowser.
- **FR-004**: Fallos identifican etapa, causa conocida o no determinada y siguiente acción; preservar timeouts y diagnóstico detallado en logs sin secretos, tokens, entorno completo ni contenido de sesiones.
- **FR-005**: Conservar Start/Check/Stop/Reset/NoBrowser/TextOnly/puertos explícitos; Check no pide credenciales ni inicia servicios; TextOnly no anuncia carga de embeddings ni fuentes disponibles.
- **FR-006**: Credencial oculta y en memoria; mantener bloqueo concurrente, propiedad de procesos, limpieza/cancelación, localhost/offline/auth/consentimiento/T090/T150 y aislamiento.
- **FR-007**: Auditar comprobaciones repetidas y quitar solo trabajo innecesario demostrado; preservar validaciones necesarias de procesos diferentes; no atribuir mejoras de rendimiento sin medición.
- **FR-008**: Preservar entorno preparado, datos habituales y paquetes experimentales; sin Reset ni commits; regenerar/reproducir evidencia actual si cambian fuentes de manifiesto.
- **FR-009**: Probar secuencia/espera/error/cancelación/full/TextOnly/Check/puerto ocupado/secretos; ensayo real PowerShell y check-demo; regresiones relevantes y global si cambia comportamiento compartido; Black afectado/Ruff Counter con multiplicidad durable.
- **FR-010**: Documentar etapas, comandos, tiempos observados iniciales/posteriores, tareas/archivos/límites; cerrar solo analyze sin críticos y converge sin brechas.

## Key Entities

Etapa de arranque (nombre, en curso/completada/fallida/cancelada, tiempo transcurrido).
Aviso operativo sin datos de sesión ni secretos. Evidencia separada para código actual.

## Success Criteria

- **SC-001**: Todas las etapas observadas corresponden a operaciones reales; cero disponibilidad prematura en pruebas.
- **SC-002**: Espera inducida superior al intervalo produce aviso temporal, cesa al salir y no muestra porcentaje/ETA.
- **SC-003**: Casos full/TextOnly/Check/error/cancelación y script de comprobación pasan; cero credenciales ficticias en mensajes/logs inspeccionados.
- **SC-004**: Ensayo de dos arranques sin Reset deja datos preparados/habituales iguales y centinela vivo; gates y evidencia actual pasan, originales intactos.

## Assumptions / Clarifications

### Session 2026-10-18

Cero preguntas tras escanear alcance/datos/UX/fallos/seguridad/dependencias/terminología:
no bloqueos materiales. Cadencia rutinaria5s; sin terminal interactiva se usan líneas
normales y flush, sin animación ANSI. Carga inicial significa primera observada en este
ensayo con recursos preparados, no caché fría ni reinstalación. No nuevos modelos/agentes,
descargas/servicios/rediseño/políticas ni refactor general del lanzador.
