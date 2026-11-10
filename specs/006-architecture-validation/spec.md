# Feature Specification: Validación arquitectónica reproducible



**Feature Branch**: `006-architecture-validation` (sin Git, sin commits)

**Created**: 2026-10-17

**Status**: Especificación validada

**Input**: docs/ORAL-IA_SpecKit/features/006_validation_specify.md; completar MVP en orden tras cierre005.



## User Scenarios & Testing *(mandatory)*



### User Story 1 - Comparar baseline y agencia (Priority: P1)



El mantenedor necesita: Ejecutar el mismo catálogo y leer mediciones por condición, incluidas diferencias de fuentes, decisión y coste.



**Why this priority**: Evidencia verificable de la hipótesis arquitectónica, principio X.

**Independent Test**: Ejecutar el mismo catálogo y leer mediciones por condición, incluidas diferencias de fuentes, decisión y coste.



**Acceptance Scenarios**:



1. **Given** catálogo sintético autorizado, **When** se ejecuta el recorrido, **Then** se obtiene el resultado observable descrito y su procedencia.

2. **Given** datos o condiciones incompatibles, **When** se intenta el recorrido, **Then** se rechaza o declara no comparable sin inventar resultados ni exponer datos.



### User Story 2 - Ablacionar con aislamiento (Priority: P1)



El mantenedor necesita: Autorizar protocolo sintético y comparar ambas verificaciones; una petición con datos no sintéticos se rechaza.



**Why this priority**: Evidencia verificable de la hipótesis arquitectónica, principio X.

**Independent Test**: Autorizar protocolo sintético y comparar ambas verificaciones; una petición con datos no sintéticos se rechaza.



**Acceptance Scenarios**:



1. **Given** catálogo sintético autorizado, **When** se ejecuta el recorrido, **Then** se obtiene el resultado observable descrito y su procedencia.

2. **Given** datos o condiciones incompatibles, **When** se intenta el recorrido, **Then** se rechaza o declara no comparable sin inventar resultados ni exponer datos.



### User Story 3 - Medir recuperación (Priority: P1)



El mantenedor necesita: Inyectar cada fallo y comprobar resultado, traza y estado antes/después.



**Why this priority**: Evidencia verificable de la hipótesis arquitectónica, principio X.

**Independent Test**: Inyectar cada fallo y comprobar resultado, traza y estado antes/después.



**Acceptance Scenarios**:



1. **Given** catálogo sintético autorizado, **When** se ejecuta el recorrido, **Then** se obtiene el resultado observable descrito y su procedencia.

2. **Given** datos o condiciones incompatibles, **When** se intenta el recorrido, **Then** se rechaza o declara no comparable sin inventar resultados ni exponer datos.



### User Story 4 - Reproducir el paquete (Priority: P1)



El mantenedor necesita: Reejecutar entradas registradas y comparar decisiones estructurales; un paquete manipulado se rechaza.



**Why this priority**: Evidencia verificable de la hipótesis arquitectónica, principio X.

**Independent Test**: Reejecutar entradas registradas y comparar decisiones estructurales; un paquete manipulado se rechaza.



**Acceptance Scenarios**:



1. **Given** catálogo sintético autorizado, **When** se ejecuta el recorrido, **Then** se obtiene el resultado observable descrito y su procedencia.

2. **Given** datos o condiciones incompatibles, **When** se intenta el recorrido, **Then** se rechaza o declara no comparable sin inventar resultados ni exponer datos.



### User Story 5 - Interpretar evidencia prudente (Priority: P2)



El mantenedor necesita: Leer informe y distinguir observaciones sintéticas, costes, resultados negativos y utilidad humana no medida.



**Why this priority**: Evidencia verificable de la hipótesis arquitectónica, principio X.

**Independent Test**: Leer informe y distinguir observaciones sintéticas, costes, resultados negativos y utilidad humana no medida.



**Acceptance Scenarios**:



1. **Given** catálogo sintético autorizado, **When** se ejecuta el recorrido, **Then** se obtiene el resultado observable descrito y su procedencia.

2. **Given** datos o condiciones incompatibles, **When** se intenta el recorrido, **Then** se rechaza o declara no comparable sin inventar resultados ni exponer datos.



### Edge Cases



- Paquete alterado, código distinto, campo desconocido, tamaño excesivo o protocolo no autorizado.

- Fallos obligatorios/opcionales, timeout, actualización concurrente, presupuesto agotado, ausencia de GPU/modelo/voz.

- Conjunto etiquetado vacío, denominador cero, errores/no recuperación, muestras pequeñas y ninguna observación humana.

- Eliminación y retención sintética; ningún dato de instalación normal en artefactos.



## Requirements *(mandatory)*



### Functional Requirements



- **FR-001**: El sistema MUST ejecutar el mismo catálogo sintético con baseline directo y agencia completa, registrando condiciones comunes y diferencias.

- **FR-002**: El sistema MUST permitir ablaciones de fundamentación y coherencia únicamente en un proceso experimental aislado con datos sintéticos y autorización de protocolo; nunca entregar sus resultados a participantes.

- **FR-003**: El sistema MUST mantener controles constitucionales y de privacidad; no añadir rutas de producción que omitan verificadores.

- **FR-004**: El sistema MUST comparar estrategias de recuperación y composiciones de agentes existentes con parámetros registrados y evidencia etiquetada.

- **FR-005**: El sistema MUST incluir los quince escenarios del catálogo fuente: evidencia clara/ausente/conflictiva, fuera de alcance, afirmación sin respaldo, contradicción, repetición, timeout, modelo/índice/STT no disponibles, conflicto de estado, límites, eliminación y nota académica.

- **FR-006**: El sistema MUST inyectar fallos en las interfaces reales de agente/modelo/índice/STT/recursos y observar recuperación o terminación segura, sin contaminar el estado interactivo.

- **FR-007**: El sistema MUST calcular agentes por turno/sesión, composiciones, bloqueos/reformulaciones, salidas sin fuentes, precisión/cobertura etiquetadas, conflictos y fallos de coordinación.

- **FR-008**: El sistema MUST medir latencia total y por agente, CPU, memoria, GPU y contexto; informar unidades, alcance del muestreo y faltantes con motivo, sin fabricar ceros.

- **FR-009**: El sistema MUST calcular timeouts, recuperaciones, porcentaje de turnos trazables, reconstrucción, reutilización entre agencias y efectos de corrección de transcripción.

- **FR-010**: El sistema MUST registrar completadas/abandonos/duración/revisabilidad y observaciones voluntarias de utilidad/facilidad/preguntas/preparación/tiempo docente; distinguir observaciones humanas ausentes de ejecución sintética.

- **FR-011**: El sistema MUST fijar código, configuración, modelo/parámetros, índice/documentos, escenario, semilla, componentes/orden, límites y hardware para cada ejecución.

- **FR-012**: El sistema MUST generar resultados estructurados y resumen legible por escenario/configuración y comparación baseline/agencia, con conteos y variabilidad.

- **FR-013**: El sistema MUST distinguir métricas, observaciones, inferencias y limitaciones; declarar muestras pequeñas, condiciones no comparables y resultados negativos sin afirmar superioridad injustificada.

- **FR-014**: El sistema MUST reproducir paquetes comprobando integridad de entradas/código y secuencias/decisiones estructurales; excluir tiempo/identificadores aleatorios de la igualdad.

- **FR-015**: El sistema MUST operar localmente por texto mediante herramienta de mantenedor, usando solo fixtures sintéticas incorporadas; no importar bases de participantes ni publicar datos.

- **FR-016**: El sistema MUST conservar contratos y regresiones 001–005; documentar instalación, ejemplos ejecutados, límites, pruebas negativas y propuesta de evolución sin notas ni perfiles.



### Key Entities



- Protocolo versionado: catálogo sintético, condiciones, orden/semilla, límites y autorización de ablaciones.

- Escenario: consulta, materiales y etiquetas esperadas, historia y fallo inyectable.

- Ejecución/turno: condición, componentes reales, mediciones, decisiones, fuentes y estado.

- Paquete: manifest de integridad, entradas, resultados abiertos y resumen legible.

- Observación humana: opcional, separada de sesiones y nunca una calificación; faltante por defecto.



## Success Criteria *(mandatory)*



### Measurable Outcomes



- **SC-001**: Baseline, agencia y ambas ablaciones completan el catálogo mínimo de quince escenarios con resultados o fallos explícitos para cada celda.

- **SC-002**: El 100% de resultados declara procedencia de métricas y motivos de valores ausentes; nunca se presenta falta de medida como cero.

- **SC-003**: Un paquete determinista repetido conserva el 100% de secuencias y decisiones estructurales comparables; manipular entradas o código se detecta.

- **SC-004**: Las inyecciones previstas dejan resultado trazable y evidencia de recuperación o cierre; ninguna altera sesiones de la instalación normal.

- **SC-005**: Los informes muestran tamaño de muestra, variabilidad, no comparabilidad y límites, incluidos resultados negativos y ausencia de valoración humana.

- **SC-006**: Las pruebas demuestran que las ablaciones no están disponibles para datos de usuario ni por rutas de producción y que no asignan notas.



## Assumptions



- Un ordenador, ejecución secuencial y únicamente fixtures sintéticas incorporadas; sin publicar ni usar bases reales.

- Modelo determinista local disponible por defecto; sus mediciones no prueban calidad ni rendimiento de un LLM. Ollama/voz/hardware no disponibles se declaran faltantes, sin descargar modelos.

- Baseline directo comparte entrada/evidencia/modelo cuando corresponde, pero carece de coordinación; las diferencias se registran y limitan las conclusiones.

- La prueba controlada no necesita participantes humanos ni inventa sus opiniones. No se exige identidad textual generativa.

- Se reutilizan agentes y controles existentes; ninguna configuración experimental entra en catálogos de producción.



## Clarifications



### Session 2026-10-17



Cero preguntas: alcance, actores, entidades, interfaz textual, privacidad, límites,

fallos, dependencias, terminología y señales de cierre claros. Decisiones aprobadas

en 10_clarification_decisions.md: sintético/local, sin evaluar personas, modelo

determinista disponible, resultados humanos faltantes; reproducción estructural.

Checklist requisitos 16/16 antes y después. Sin hooks configurados.


## Clarifications

### Session 2026-10-17

Cero preguntas; categorías claras mediante decisiones aprobadas: local, sintético,
sin notas, sin usuarios en ablaciones, reproducción estructural. Modelo determinista
disponible y utilidad humana faltante. Checklist16/16 antes/después; sin hooks.

Aclaración de alcance de FR-010: las observaciones humanas se representan como faltantes
con motivo mientras no exista piloto consentido; este alcance sintético no recopila
opiniones. Se ejecutan 17 casos, incluidos los 15 obligatorios y dos sondas adicionales.
