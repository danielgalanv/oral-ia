# Feature Specification: Demostración local de ORALIA

**Feature Branch**: `007-local-demonstration` (sin Git, sin commits)
**Created**: 2026-10-18
**Status**: Implementada y validada; analyze sin críticos y converge sin brechas obligatorias
**Input**: Petición explícita Feature007, posterior al MVP001–006 auditado. Extensión de empaquetado/demo, sin cambiar constitución ni arquitectura.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Arrancar y detener con confianza (Priority: P1)

Preparador inicia la demo, recibe URL lista y la detiene sin afectar otro proceso.

**Why this priority**: Demostración repetible con seguridad y gobierno existentes.
**Independent Test**: Preparador inicia la demo, recibe URL lista y la detiene sin afectar otro proceso.

**Acceptance Scenarios**:

1. **Given** dependencias y recursos preparados, **When** se ejecuta demo.ps1, **Then** API y frontend escuchan solo en localhost y se abre la portada tras readiness de ambos.
2. **Given** puerto ocupado o readiness fallida, **When** se intenta arrancar, **Then** se informa causa/solución y solo se limpian hijos propios; el centinela ajeno sigue vivo.

### User Story 2 - Repetir datos ficticios aislados (Priority: P1)

Preparador arranca dos veces y reinicia solo la demo tras confirmar su ruta.

**Why this priority**: Demostración repetible con seguridad y gobierno existentes.
**Independent Test**: Preparador arranca dos veces y reinicia solo la demo tras confirmar su ruta.

**Acceptance Scenarios**:

1. **Given** fixtures preparados, **When** se arranca, para y vuelve a arrancar, **Then** existen exactamente un curso, un material y dos actividades, con mismos identificadores y recursos habituales sin cambios.
2. **Given** demo parada, **When** se solicita Reset, **Then** solo BORRAR DEMO permite eliminar la raíz marcada; cancelar, enlaces o demo activa se rechazan sin borrar recursos ajenos.

### User Story 3 - Presentar un recorrido completo (Priority: P1)

Presentador abre desde portada y área docente la actividad, conserva, revisa, exporta y elimina por teclado.

**Why this priority**: Demostración repetible con seguridad y gobierno existentes.
**Independent Test**: Presentador abre desde portada y área docente la actividad, conserva, revisa, exporta y elimina por teclado.

**Acceptance Scenarios**:

1. **Given** portada y credencial válida, **When** se usa teclado para entrar y abrir autoestudio, **Then** se pregunta por agua, se muestran fuentes, se elige conservación y se completa cierre/revisión/exportaciones JSON y Markdown.
2. **Given** sesión conservada, **When** se confirma su eliminación, **Then** la revisión devuelve404 y la exportación409; sin credencial no se accede al área protegida.

### User Story 4 - Mostrar alternativa efímera y límites (Priority: P1)

Participante rechaza conservación y completa por texto; presentador explica fuentes/modelos/voz y utilidad no validados.

**Why this priority**: Demostración repetible con seguridad y gobierno existentes.
**Independent Test**: Participante rechaza conservación y completa por texto; presentador explica fuentes/modelos/voz y utilidad no validados.

**Acceptance Scenarios**:

1. **Given** defensa textual sin marcar conservación, **When** se responde y finaliza, **Then** el contenido no es revisable; la presentación distingue determinismo, embeddings reales y voz/utilidad humana pendientes.
2. **Given** red externa bloqueada y recursos preparados, **When** se recorre la sesión, **Then** funciona sin conexiones externas; sin embeddings se ofrece TextOnly explícito y nunca fuentes inventadas.

### Edge Cases

- Dependencia/modelo ausente, sin conexión, puerto ocupado, timeout/readiness fallida, salida inesperada de hijo y Ctrl+C.
- Dos lanzadores simultáneos, PID reciclado, recibo alterado, supervisor muerto y proceso ajeno.
- Ruta no demo, raíz no marcada, symlink/junction anidado, demo activa y cancelación del reinicio.
- Actividad usada/retirada, sesión activa previa, consentimiento denegado/scopes parciales, texto libre en exportación.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST arrancar desde PowerShell con un comando, verificar dependencias/puertos/esquema/recursos, iniciar solo localhost y abrir navegador únicamente tras readiness real.
- **FR-002**: El sistema MUST rechazar puertos ocupados sin cambiar puertos ni detener procesos ajenos; comunicar causa y solución de fallos, incluyendo arranque parcial.
- **FR-003**: El sistema MUST solicitar credencial administrativa por entrada oculta o entorno de proceso; nunca escribir secretos en argumentos, URLs, archivos, frontend o logs; mantener autenticación normal.
- **FR-004**: El sistema MUST permitir parar solo procesos creados por el lanzador, comprobar su propiedad y limpiar arranques parciales; una parada no afecta procesos ajenos.
- **FR-005**: El sistema MUST aislar base, índice, archivos, configuración y logs de demo del entorno habitual; rechazar rutas/links que escapen del espacio de demo.
- **FR-006**: El sistema MUST preparar de forma idempotente curso/material breve/autoestudio/defensa ficticios, configuraciones activas y políticas de salida/retención válidas sin duplicar al arrancar.
- **FR-007**: El sistema MUST ofrecer reinicio explícito con ruta verificada y confirmación previa al borrado; rechazar demo activa, rutas no reconocidas y enlaces.
- **FR-008**: El sistema MUST no descargar modelos silenciosamente; comprobar recursos locales y ofrecer explícitamente texto sin fuentes si faltan embeddings, sin simular fuentes, voz o modelos reales.
- **FR-009**: El sistema MUST mostrar portada con accesos a participante y área docente, identificando IA, datos ficticios y funcionamiento determinista cuando corresponda; conservar rutas existentes.
- **FR-010**: El sistema MUST permitir abrir desde el área autenticada una actividad activa en su modo sin copiar identificadores; solo referencias no secretas viajan en navegación y el código seudónimo nunca autentica.
- **FR-011**: El sistema MUST ofrecer recorrido textual y de teclado con mensajes comprensibles, fuentes reales cuando disponibles, elección de scopes, cierre, revisión, exportación y eliminación verificable.
- **FR-012**: El sistema MUST permitir una alternativa efímera sin conservación; mantener T090/T150, permisos/propiedad, scopes/plazos/retención y aislamiento de sesiones.
- **FR-013**: El sistema MUST documentar guion aproximado de diez minutos, preparación/arranque/parada/reinicio/fallos y diferencia entre determinismo, modelos reales y validación humana pendiente.
- **FR-014**: El sistema MUST probar lanzador/aislamiento, recorrido real de portada a exportación/borrado y ensayo offline tras preparación, sin alterar base habitual ni procesos ajenos.
- **FR-015**: El sistema MUST preservar paquete006 original e integridad; registrar cambios de código del manifiesto y generar/reproducir evidencia actual con hashes medidos, nunca ajustarlos manualmente.
- **FR-016**: El sistema MUST completar regresión global, build/lint/Playwright, Black afectado y Ruff Counter contra baseline durable; migraciones limpias/upgrade si cambia esquema; entregar tabla de tareas, archivos y límites.

### Key Entities

- Entorno demo: raíz identificada, base/índice/material/config/logs propios, revisión de fixtures.
- Lanzamiento: identificador no secreto, procesos propios, creación, puertos, readiness y solicitud de parada.
- Fixture: curso/material/configuraciones publicadas y políticas versionadas; ninguna identidad real.
- Evidencia: guion, ensayos, hashes del paquete original006 y paquete reproducido con código actual.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Un comando inicia los dos servicios y anuncia sus URLs solo cuando están listos; los errores preparados son accionables y no provocan arranques ocultos.
- **SC-002**: Arranque repetido conserva exactamente una copia de cada fixture y parada/reinicio dejan intactos recursos habituales y procesos ajenos preparados.
- **SC-003**: Un recorrido real por teclado desde portada completa login, actividad, fuentes, conservación, cierre, revisión, exportación y borrado; alternativa efímera no es revisable.
- **SC-004**: El ensayo offline completa el recorrido preparado sin descargas ni conexiones externas; ausencia de recursos no se disfraza de funcionamiento real.
- **SC-005**: Todas las denegaciones de permisos/propiedad/confirmación/rutas/puertos preparadas fallan cerradas sin exponer secretos ni borrar contenido ajeno.
- **SC-006**: El paquete006 original conserva hashes; el paquete actual ejecuta/reproduce204celdas y las puertas globales pasan sin nuevas infracciones Ruff.

## Assumptions

- Única instalación local, una sesión interactiva activa; puertos demo propios y cambios solo explícitos.
- La credencial la introduce el presentador, no se distribuye una contraseña demo por defecto.
- Dependencias/embeddings se preparan antes del ensayo offline. Si falta embedding, opción textual sin fuentes explícita; sin descargas automáticas.
- El guion recomienda código ficticio fijo autorizado por la política; sigue siendo identificador, nunca credencial.
- Reinicio borra únicamente recursos demo identificados; nunca fuerza la terminación de procesos no reconocidos.
- No nuevos agentes/arquitectura/SSO/nube/LAN/piloto/voz real/rediseño ni sustitución general de JSON.

## Clarifications

### Session 2026-10-18

Cero preguntas: alcance/actores/datos/ciclo/UX/seguridad/fallos/dependencias/terminología
y cierre claros. Rutinas: localhost, una sesión, credencial oculta de presentador;
puertos demo explícitos8010/5180; prompt de reinicio BORRAR DEMO; opción TextOnly
explícita si faltan recursos. Ningún cambio constitucional. Checklist16/16 sin regresiones.
