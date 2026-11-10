# Feature Specification: Configuración docente, revisión, privacidad y exportación

**Feature Branch**: `005-teacher-governance` (workspace sin Git; sin commits)
**Created**: 2026-10-17
**Status**: Especificación validada
**Input**: `docs/ORAL-IA_SpecKit/features/005_teacher_review_privacy_specify.md` y autorización de completar el MVP en orden.

## Clarifications

### Session 2026-10-17

- Credencial local y roles: las decisiones aprobadas permiten una credencial administrativa de instalación; el código seudónimo identifica, pero no autentica. La propiedad de sesión necesita autorización secreta independiente.
- Conservación: consentimiento explícito y scopes independientes, plazo finito y eliminación al cierre; negar conservación no bloquea participación. No existe permiso implícito por ser docente.
- Versionado: los cambios crean versiones nuevas y preservan referencias históricas, incluidos materiales/modelos/agentes y política de retención.
- Exportación: revisión humana obligatoria antes de incluir texto libre; alias por lote sin prometer anonimización perfecta ni conservar archivos exportados en el servidor.
- Alcance: una instalación local, una sesión activa, red local deshabilitada por defecto, sin SSO, identidad real, perfiles ni experimentos de Feature 006.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Configurar y publicar versiones (Priority: P1)

Un docente crea una actividad, autoriza materiales y parámetros disponibles, duplica una versión usada, publica la nueva y retira la anterior.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US1.

**Independent Test**: Una sesión antigua conserva su versión y una nueva usa una versión activa; alterar la antigua falla.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US1, **Then** Una sesión antigua conserva su versión y una nueva usa una versión activa; alterar la antigua falla.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US1, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### User Story 2 - Aislar roles y sesiones locales (Priority: P1)

Docente inicia y cierra sesión administrativa; participante inicia su actividad y opera únicamente su sesión.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US2.

**Independent Test**: Credenciales inválidas y acceso a una sesión ajena se rechazan por todas las rutas sin revelar contenido.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US2, **Then** Credenciales inválidas y acceso a una sesión ajena se rechazan por todas las rutas sin revelar contenido.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US2, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### User Story 3 - Participar de forma efímera o consentida (Priority: P1)

Un participante lee el aviso, revisa/corrige su transcripción y elige los scopes antes del cierre voluntario o por límite.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US3.

**Independent Test**: Negativa permite completar y borra contenido; consentimiento conserva solo scopes autorizados durante el plazo configurado.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US3, **Then** Negativa permite completar y borra contenido; consentimiento conserva solo scopes autorizados durante el plazo configurado.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US3, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### User Story 4 - Revisar evidencia consentida (Priority: P1)

Docente abre una sesión consentida y distingue transcripción, revisiones y decisiones sin evaluar al participante.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US4.

**Independent Test**: Scopes resumen y transcripción producen vistas distintas; sesiones expiradas o eliminadas no se abren.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US4, **Then** Scopes resumen y transcripción producen vistas distintas; sesiones expiradas o eliminadas no se abren.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US4, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### User Story 5 - Exportar un lote permitido (Priority: P2)

Docente revisa texto libre y descarga datos abiertos de una o varias sesiones autorizadas con alias por lote.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US5.

**Independent Test**: Las dos representaciones contienen solo campos permitidos; incluir una sesión denegada bloquea el lote entero.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US5, **Then** Las dos representaciones contienen solo campos permitidos; incluir una sesión denegada bloquea el lote entero.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US5, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### User Story 6 - Eliminar y purgar con comprobación (Priority: P1)

Propietario o docente confirma eliminar contenido, recibe un recibo y comprueba su ausencia de revisión y exportación.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US6.

**Independent Test**: Segundo borrado es idempotente; purgar expirados no altera una sesión vigente ni materiales.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US6, **Then** Segundo borrado es idempotente; purgar expirados no altera una sesión vigente ni materiales.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US6, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### User Story 7 - Consultar el sistema y operar por teclado (Priority: P2)

Docente consulta métricas agregadas y estados técnicos; participantes mantienen su acceso textual completo.

**Why this priority**: Gobierno humano y privacidad exigidos por los principios VI/VII; US7.

**Independent Test**: Un recorrido real por teclado configura, revisa, exporta y elimina sin notas ni rankings.

**Acceptance Scenarios**:

1. **Given** una instalación local y datos ficticios autorizados, **When** se realiza el flujo US7, **Then** Un recorrido real por teclado configura, revisa, exporta y elimina sin notas ni rankings.
2. **Given** permisos ausentes, datos caducados o una operación fallida, **When** se intenta US7, **Then** no se revela contenido ni se comunica éxito sin efectos confirmados.

### Edge Cases

- Credencial no configurada, expirada o reutilizada tras logout; origen remoto, sesión ajena y rutas históricas alternativas.
- Ediciones/activaciones simultáneas, configuración ya usada, agente/modelo no disponible, fuente retirada y retención nula.
- Sesión activa, cierre repetido, conservación de solo resumen o solo transcripción, negativa y expiración durante revisión/exportación.
- Texto libre con posibles datos personales, contenido malicioso, lote mixto autorizado/denegado, fallo de escritura y eliminación repetida.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001** (US1): El sistema MUST cumplir: El docente puede crear, duplicar y versionar configuraciones; cada sucesor recibe identidad propia y conserva familia y procedencia, incluso si la versión anterior ya fue utilizada.
- **FR-002** (US1): El sistema MUST cumplir: Las sesiones referencian una configuración inmutable. Cambiar objetivo, límites, idioma, modos, preguntas, temas, conocimiento general, modelos, agentes o política genera una nueva versión sin alterar sesiones anteriores.
- **FR-003** (US1): El sistema MUST cumplir: El docente puede activar y retirar versiones; solo una versión por familia está activa para nuevos usos y una retirada no inicia nuevas sesiones ni elimina evidencia histórica.
- **FR-004** (US1): El sistema MUST cumplir: La selección de materiales identifica versiones autorizadas y valida asignatura, actividad, estado activo y vigencia. Una versión retirada no aparece en nuevas recuperaciones.
- **FR-005** (US1): El sistema MUST cumplir: El docente selecciona únicamente modelos y composiciones de agentes disponibles y compatibles; los controles constitucionales y de privacidad son obligatorios y los contratos no pueden editarse desde una actividad.
- **FR-006** (US1): El sistema MUST cumplir: El docente puede consultar estados técnicos de documentos, extracción e índice, sus errores y versiones sin ejecutar su contenido.
- **FR-007** (US2): El sistema MUST cumplir: El acceso docente requiere una credencial administrativa local configurada y una sesión de duración limitada; ausencia, invalidez, caducidad y cierre de sesión deniegan acceso.
- **FR-008** (US2): El sistema MUST cumplir: El participante solo puede acceder y modificar la sesión que ha iniciado mediante una autorización secreta de sesión. Conocer códigos seudónimos o identificadores de otra sesión no concede acceso.
- **FR-009** (US2): El sistema MUST cumplir: La autorización abarca todas las rutas históricas y nuevas de contenido, trazas, materiales administrativos, configuración, exportación, corrección, cierre y eliminación; no quedan rutas alternativas sin protección.
- **FR-010** (US2): El sistema MUST cumplir: Los intentos denegados se registran solo con tipo, resultado e instante, sin credenciales, contenido, parámetros sensibles ni identificadores personales.
- **FR-011** (US2): El sistema MUST cumplir: La aplicación escucha solo en el anfitrión por defecto; habilitar una red local requiere una configuración administrativa explícita. Las peticiones de otros orígenes no pueden ejecutar acciones autenticadas.
- **FR-012** (US3): El sistema MUST cumplir: El participante conoce finalidad, datos operativos, datos conservados, plazo y quién accede antes de participar. Rechazar conservación no impide completar la sesión efímera.
- **FR-013** (US3): El sistema MUST cumplir: La conservación posterior exige autorización de actividad, consentimiento explícito y plazo finito no negativo. Transcripción y resumen se eligen independientemente; audio nunca se conserva.
- **FR-014** (US3): El sistema MUST cumplir: Los cierres voluntarios, automáticos y seguros aplican la elección actual una sola vez mediante el cierre ganador. Sin consentimiento se eliminan las copias de contenido operativo y solo quedan metadatos técnicos mínimos justificados.
- **FR-015** (US3): El sistema MUST cumplir: Las transcripciones de voz son revisables y corregibles por su participante; conservar incluye original y revisiones diferenciadas, sin reescribir la salida ya entregada.
- **FR-016** (US3): El sistema MUST cumplir: La política de retención queda versionada e inmutable con la configuración usada; no se acepta conservación indefinida ni se introduce un plazo implícito.
- **FR-017** (US4): El sistema MUST cumplir: La revisión docente lista y abre únicamente sesiones cerradas, consentidas, no eliminadas y no expiradas. Una sesión no autorizada devuelve denegación sin contenido.
- **FR-018** (US4): El sistema MUST cumplir: La revisión distingue entradas, originales y correcciones, respuestas aprobadas, fuentes con versión/ubicación, agentes, verificaciones, bloqueos, incidencias y resumen, filtrando cada campo según su scope consentido.
- **FR-019** (US4): El sistema MUST cumplir: Los registros técnicos mínimos no permiten reconstruir texto eliminado ni perfiles longitudinales. No se exponen prompts internos completos, razonamiento privado, candidatos bloqueados ni secretos.
- **FR-020** (US5): El sistema MUST cumplir: El docente puede exportar una o varias sesiones autorizadas a un formato abierto estructurado y otro legible, incluyendo configuración/versiones, contenido permitido, resumen, fuentes y trazabilidad saneada.
- **FR-021** (US5): El sistema MUST cumplir: Cada exportación revalida autorización, consentimiento, scopes, caducidad y eliminación en el momento de construirla; una selección que contenga una sesión no autorizada falla sin exportación parcial.
- **FR-022** (US5): El sistema MUST cumplir: Las exportaciones para análisis sustituyen códigos e identidades de sesión por alias del lote y omiten identificadores directos. Texto libre requiere revisión explícita por posible información personal antes de descargarlo; no se afirma anonimización automática.
- **FR-023** (US5): El sistema MUST cumplir: La exportación usa proyecciones de campos permitidos, excluye siempre audio, credenciales, secretos, razonamiento privado y datos fuera del consentimiento; no crea archivos persistentes en el servidor.
- **FR-024** (US6): El sistema MUST cumplir: Docente o participante propietario pueden eliminar el contenido de una sesión cerrada; una sesión activa requiere finalizar primero y no puede borrarse por accidente mientras procesa un turno.
- **FR-025** (US6): El sistema MUST cumplir: La eliminación retira contenido y copias en turnos, transcripciones, correcciones, estado, mensajes, propuestas y trazas; conserva solo un recibo técnico mínimo sin contenido y excluye la sesión de revisión y exportación posteriores.
- **FR-026** (US6): El sistema MUST cumplir: La eliminación repetida es idempotente y la purga de expirados es manual, comprobable y limitada a las sesiones alcanzadas; sesiones vigentes y materiales docentes no se eliminan.
- **FR-027** (US6): El sistema MUST cumplir: Un fallo o rollback no comunica una eliminación o exportación exitosa; los efectos de contenido, recibo y consentimiento se confirman de forma coherente.
- **FR-028** (US7): El sistema MUST cumplir: El panel muestra métricas agregadas del sistema —sesiones, turnos, cierres, bloqueos, incidencias y latencias disponibles— sin desglose individual, notas, rankings ni inferencia académica; métricas ausentes se marcan como faltantes.
- **FR-029** (US7): El sistema MUST cumplir: La interfaz docente y las funciones de privacidad del participante son operables por texto y teclado, con etiquetas, estados de carga, confirmación de acciones destructivas y errores comprensibles.
- **FR-030** (US7): El sistema MUST cumplir: Las extensiones preservan T090, T150, recuperación autorizada y contratos públicos de Features 001–004. Los cambios de autorización históricos se documentan y prueban con credenciales explícitas, sin un bypass de producción para pruebas.
- **FR-031** (US7): El sistema MUST cumplir: El sistema no almacena una relación entre identidad real y código; no incluye SSO, nube, correo, expedientes, biometría, notas ni perfiles de estudiantes.
- **FR-032** (US7): El sistema MUST cumplir: La entrega incluye datos ficticios, migraciones limpia y de actualización, instalación local, ejemplos ejecutados, pruebas de autorización/consentimiento/borrado/exportación y evidencia de límites.

### Key Entities

- ActivityConfiguration/RetentionPolicy: versión concreta, límites, permisos, contenido, duración y acceso; inmutable una vez usada.
- Ciclo de publicación: borrador, activa, retirada; familia y procedencia del duplicado.
- Autorización local: rol administrativo o participante propietario, secreto de sesión y caducidad; sin identidad real.
- ConsentRecord: scopes y decisión explícita sobre conservación, separado de datos operativos.
- Recibo de eliminación: instante, resultado y conteos, sin texto eliminado.
- Exportación: proyección autorizada con alias y revisión humana de texto libre; efímera.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: En las pruebas de versionado, el 100% de las sesiones antiguas conserva configuración y política originales tras crear y activar un sucesor.
- **SC-002**: El 100% de intentos preparados de rol no autorizado o sesión ajena se deniega sin datos sensibles.
- **SC-003**: Todas las combinaciones de consentimiento y scopes preparadas completan la sesión y conservan exactamente lo permitido; la negativa no impide el flujo.
- **SC-004**: El 100% de revisiones y lotes de exportación excluye sesiones no consentidas, expiradas o eliminadas y campos no autorizados.
- **SC-005**: Las exportaciones estructurada y legible son utilizables sin servicios externos y no contienen ninguno de los secretos, audio o razonamiento privado sembrados en pruebas.
- **SC-006**: Todas las eliminaciones y purgas de prueba son verificables, idempotentes y aíslan sesiones vigentes y materiales.
- **SC-007**: Un docente completa por teclado el recorrido de configuración, revisión, exportación y eliminación; el participante revisa/corrige y decide privacidad por texto.
- **SC-008**: Las métricas agregadas describen funcionamiento, faltantes y limitaciones sin notas, rankings ni inferencias académicas.

## Assumptions

- Una instalación local, una sesión interactiva activa; no hay SSO ni almacén de identidades reales. Credencial local según decisiones aprobadas.
- Solo se revisan datos cuya conservación ya está autorizada; tener un rol docente no sustituye consentimiento.
- Disponibilidad de modelos es local y explícita; no hay descargas silenciosas. La voz real sigue siendo opcional.
- Las extensiones de integración se documentan y conservan regresiones; ningún modo de producción desactiva autorización para facilitar pruebas.
- Feature 006, experimentos y comparación arquitectónica no forman parte de esta implementación.
