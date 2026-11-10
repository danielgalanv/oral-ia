# Feature Specification: 011 — Autoestudio de Ingeniería del Software real

**Created**: 2026-10-21
**Status**: Especificación aclarada; implementación autorizada, sin commits.
**Input**: Empezar autoestudio con las diapositivas reales proporcionadas, un formato por documento; solo PDF en esta experiencia. No material del alumno ni defensa. Preservar originales, entornos y puertas históricas.

## User Scenarios & Testing

### User Story 1 — Comprender requisitos con fuentes reales (P1)

Un participante consulta qué significa validar requisitos, distingue verificación de calidad y solicita aclaración con citas comprobables. Comienza por Procedimiento requisitos, páginas10–12. El sistema informa de sus límites cuando el documento no aporta un ejemplo o información suficiente.

**Independent Test**: conversación completa por API real, con actividad y almacenamiento propios y política explícita; cada salida contiene respuesta efectiva o límite honesto y fuentes de la versión activa, no respuestas sustituidas.

1. Dado el PDF autorizado, al preguntar qué significa validar requisitos responde sobre necesidades de clientes/usuarios y aprobación; nunca sobre aceptar cantidades.
2. Al comparar verificación y validación distingue calidad de especificación y correspondencia con necesidades, con páginas reales.
3. Ante petición de ejemplo no documentado o concepto no cubierto comunica límite; añade Requisitos/Testing solo cuando sea necesario, cada uno exclusivamente PDF y con procedencia propia.
4. Si una puerta bloquea, conserva primer resultado y causa observada; no declara éxito por HTTP200 ni simula turnos tras cierre.

### User Story 2 — Experiencia revisable y repetible (P1)

El usuario puede examinar la conversación real completa y probar una actividad aislada sin alterar la demo habitual.

**Independent Test**: preparación repetible explícita con identidad de entorno propio; registro de perfil, material, estados, verificaciones y cierre; instrucciones para un entorno local separado cuando esté técnicamente disponible.

1. La sesión admite varios turnos académicos y finaliza por un cierre autorizado; autenticación/consentimiento/retención existentes se conservan.
2. Un entorno de prueba no consulta ni activa material habitual, no mata procesos ajenos y no utiliza el código seudónimo como autenticación.
3. Una publicación técnica, extracción o prueba automática no se presenta como revisión docente ni validación humana.

### User Story 3 — Transferencia y fallos trazables (P2)

El diagnóstico diferencia preparación, perfil, composición, fundamentación y autorización; solo corrige causas demostradas.

**Independent Test**: caso rojo conservado y reproducción instrumentada del candidato/snapshot, seguida de negativos y regresiones que muestran que un texto sin fuente o permiso sigue bloqueado.

### Edge Cases

Referencia ambigua, saludo compuesto, pregunta no cubierta, ejemplo ausente, fuentes desactivadas/ajenas, permiso insuficiente, reformulación que modifica el candidato, error/cancelación y cierre seguro. No reconstruir el flujo de la página3 desde extracción vacía. Páginas13–14 tienen incidencias documentales y no sirven para decidir una respuesta de este piloto. No elegir rúbrica/plazos/evaluación histórica.

## Requirements

### Functional Requirements

- **FR-001**: Usar solo documentos docentes proporcionados, PDF único por documento, con hashes y originales intactos.
- **FR-002**: Iniciar aprendizaje en páginas10–12 del procedimiento; distinguir material disponible de foco activo y citar versión/página real sin atribuir una derivación al original.
- **FR-003**: Permitir conversación de autoestudio sobre validacion_requisitos y calidad_requisitos con significado propio, sin atajos de cantidades/agua/datos.
- **FR-004**: Emitir contenido autorizado pertinente o límite explícito; no afirmar ejemplos, hechos de proyecto o pruebas que no consten en la fuente.
- **FR-005**: Conservar y diagnosticar el primer intento fallido antes de modificar producción; demostrar causas con candidatos, referencias y decisiones efectivas.
- **FR-006**: Mantener T090/T150 y verificadores independientes; toda transformación de contenido conserva testigo de fuente exacto y autorización completa. Nunca eximir controles para publicar.
- **FR-007**: Preservar gates del perfil guiado; no fabricar cinco objetivos/repertorio para activarlo. Elegir perfil adecuado y describir sus límites.
- **FR-008**: Si se preparan unidades o documentos derivados, explicitar autoría, transformación y fuentes; publicación técnica no implica aprobación docente.
- **FR-009**: Separar BD/índice/archivos/credenciales/actividad del entorno habitual y preservar procesos/entornos originales; sin Reset, commits, modelos o descargas nuevos.
- **FR-010**: Entregar transcriptos completos reales con entradas, salidas, fuentes, estado, perfil y verificación; separar propuesta de respuesta ejecutada y captura de aceptación.
- **FR-011**: Preparación repetible y forma de probar el perfil/actividad aislada, sin activación habitual inferida, secretos en URL/logs o bypass de acceso/consentimiento.
- **FR-012**: Validar contratos, fallos, privacidad, regresiones y evidencia histórica; mantener T061/T067 y demás puertas humanas previas abiertas.

### Key Entities

Documento docente/version/página; actividad autoestudio aislada; fragmento y testigo literal; propuesta/snapshot/veredicto; sesión y preferencia; recibo/transcripto. Reusar contratos existentes; cualquier extensión se versiona y documenta.

## Success Criteria

- **SC-001**: Una experiencia académica completa de al menos seis turnos útiles sobre significado, comparación, aclaración y límites produce salidas efectivas con citas o aviso honesto; ninguna sesión se cierra por error ocultado.
- **SC-002**: Cada afirmación publicada se vincula a una fuente vigente; cero atribuciones al antiguo caso numérico y cero contenidos personales/administrativos incorporados.
- **SC-003**: Una variante de conversación distinta de desarrollo se congela antes de ajustar; se conserva su primera ejecución y se registra toda divergencia sin simular continuación.
- **SC-004**: El ensayo aislado finaliza y puede repetirse con recursos propios, con datos/procesos habituales y evidencias anteriores intactos; pruebas pertinentes y global si cambia código compartido.

## Clarifications — 2026-10-21

No preguntas necesarias: instrucción humana suficiente. Solo autoestudio, sin SRS ni defensa; un PDF por documento. El perfil extractivo es una opción válida si es operativo y sus límites son claros. El foco inicial es páginas10–12, no toda la asignatura. Materiales adicionales se añaden solo si el concepto los necesita. Revisión humana de utilidad y voz real pendientes; no son criterios automatizables ni autorizaciones inferidas. Pérdida histórica y D01 negativo no se borran.
