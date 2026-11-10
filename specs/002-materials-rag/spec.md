# Feature Specification: Materiales autorizados y RAG trazable

**Feature Branch**: `002-materials-rag`

**Created**: 2026-07-21

**Status**: Draft

**Input**: User description: "Feature 002 — Materiales autorizados y RAG trazable: añadir a ORAL-IA la gestión de materiales docentes autorizados y un sistema local de recuperación documental que proporcione evidencias estructuradas a los agentes sin permitir acceso abierto a Internet. El sistema debe responder a consultas sobre una asignatura a partir de una base de conocimiento controlada por el profesorado, conservar la procedencia de cada fragmento y detectar cuándo la evidencia es insuficiente, está desactualizada o entra en conflicto." (fuente: `docs/ORAL-IA_SpecKit/features/002_materials_rag_specify.md`, `.specify/memory/constitution.md`, `docs/ORAL-IA_SpecKit/14_domain_model.md`, `docs/ORAL-IA_SpecKit/13_definition_of_done.md`)

## Clarifications

### Session 2026-07-21

- Q: ¿Qué debe ocurrir cuando un profesor carga un archivo cuyo hash coincide con el de
  un documento ya existente? → A: El sistema lo marca como probable duplicado y deja que
  el profesor elija: reutilizar/enlazar el documento existente con la actividad actual,
  o continuar de todos modos como una carga nueva y distinta. Ni el rechazo automático ni
  el enlace silencioso respetan igual de bien el control docente ya establecido
  (Constitución Principio VI).
- Q: ¿Un conflicto detectado entre dos materiales activos debe quedar visible de forma
  persistente para que el profesor lo revise, o es solo una señal efímera de esa
  consulta? → A: Queda registrado de forma persistente y visible para el profesor en su
  área de materiales, además de devolverse en la respuesta de la consulta que lo
  detectó. El propio texto de origen ("solicitar revisión docente") implica algo
  perdurable sobre lo que el profesor puede actuar, no solo un campo transitorio de la
  API.

### Session 2026-09-12

- Q: La definición de `GroundingVerificationResult` dice que "conflictiva" surge
  cuando "al menos una afirmación es contradicha por la evidencia recuperada o por
  otra fuente autorizada (Escenario D)". La anotación "(Escenario D)" es
  sintácticamente ambigua: ¿acota solo "por otra fuente autorizada", de modo que una
  propuesta contradicha por un único fragmento de evidencia (sin conflicto entre
  fuentes) también sería "conflictiva"; o acota todo el disyunto, de modo que
  "conflictiva" se reserva exclusivamente al conflicto pendiente y registrado entre
  dos o más fuentes autorizadas de la User Story 6 (`MaterialConflictRecord`), y una
  contradicción de un único fragmento se clasifica `no_fundamentada`? →
  A: "(Escenario D)" acota todo el disyunto — "conflictiva" se reserva
  exclusivamente al conflicto pendiente y registrado entre fuentes de la User Story
  6 (`MaterialConflictRecord` con `review_status = "pending_review"`, o el mecanismo
  contractual equivalente); tiene precedencia sobre los demás veredictos cuando ese
  conflicto existe. Una contradicción entre una propuesta y un único fragmento de
  evidencia NO constituye por sí sola un conflicto entre fuentes y NO debe crear un
  `MaterialConflictRecord` sintético — se clasifica `no_fundamentada` (si ninguna
  afirmación está soportada) o `parcialmente_fundamentada` (si coexiste con al menos
  una afirmación soportada). Consistente con `research.md §7` (la heurística de
  conflicto opera sobre fragmentos de **documentos distintos**) y con la
  implementación ya validada de `GroundingVerifierAgent._touches_unreviewed_conflict`
  (exige un `MaterialConflictRecord` pendiente, nunca se dispara por un único
  fragmento) — la clarificación formaliza el comportamiento ya construido y probado
  en T093-T096, no lo cambia.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Incorporar y activar un documento autorizado (Priority: P1)

Un profesor carga un documento (PDF textual, DOCX, PPTX, TXT o Markdown) en una
asignatura, el sistema lo valida, extrae su texto conservando la ubicación de origen, lo
segmenta, genera metadatos y embeddings locales, lo indexa, y ejecuta comprobaciones de
cobertura y errores. El profesor revisa el estado de procesamiento y activa el documento
para una actividad; hasta ese momento, el documento no puede usarse en sesiones.

**Why this priority**: Sin materiales incorporados y activos no hay nada que recuperar;
es el prerrequisito de valor para toda la feature.

**Independent Test**: Puede probarse por completo cargando un documento de prueba,
verificando su estado de procesamiento y activándolo, sin que exista todavía ninguna
consulta de recuperación.

**Acceptance Scenarios**:

1. **Given** un archivo en un formato admitido (PDF textual, DOCX, PPTX, TXT o
   Markdown), **When** el profesor lo carga en una asignatura, **Then** el sistema
   valida formato, tamaño e integridad y calcula un identificador de contenido antes de
   procesarlo.
2. **Given** un documento cargado, **When** el sistema lo procesa, **Then** extrae el
   texto conservando referencias de página, diapositiva, sección o párrafo cuando el
   formato lo permite, lo segmenta de forma reproducible, genera metadatos y embeddings
   locales, y lo indexa localmente.
3. **Given** un documento procesado, **When** el profesor revisa su estado, **Then**
   puede ver si quedó pendiente, procesado, en error o activo, y el documento MUST
   permanecer inutilizable en sesiones hasta que el profesor lo active manualmente.
4. **Given** un documento escaneado sin texto extraíble, **When** el sistema lo procesa,
   **Then** lo identifica explícitamente como no procesable en vez de indexarlo de forma
   incompleta y silenciosa.

---

### User Story 2 - Recuperar fragmentos autorizados con procedencia (Priority: P1) 🎯 MVP

Un agente de recuperación recibe una consulta limitada a una sesión, asignatura,
actividad y conjunto de materiales autorizados, junto con un número máximo de
fragmentos y un presupuesto temporal, y devuelve fragmentos relevantes con su
procedencia (documento, versión, ubicación), metadatos, versión del índice utilizada,
advertencias y posibles conflictos.

**Why this priority**: Es el flujo extremo a extremo que demuestra el valor central de
la feature (Escenario A) y constituye su MVP mínimo demostrable, apoyado en la
incorporación de materiales de la User Story 1.

**Independent Test**: Puede probarse de forma independiente con al menos un documento ya
activo (User Story 1), enviando una consulta y verificando que los fragmentos devueltos
incluyen procedencia completa y trazable.

**Acceptance Scenarios**:

1. **Given** un documento activo y asignado a una actividad, **When** un agente consulta
   sobre esa actividad, **Then** recibe fragmentos correctos con referencia a su
   documento, versión y ubicación de origen.
2. **Given** una consulta con número máximo de fragmentos y presupuesto temporal,
   **When** se ejecuta la recuperación, **Then** el resultado respeta ambos límites y
   MUST NOT tardar indefinidamente.
3. **Given** la misma consulta, configuración y versión de índice, **When** se repite la
   recuperación, **Then** el resultado MUST ser el mismo.
4. **Given** un participante que consulta un tema, **When** el sistema presenta una
   respuesta, **Then** las fuentes utilizadas se muestran de forma comprensible sin
   exponer fragmentos no autorizados para su actividad.

---

### User Story 3 - Detectar evidencia insuficiente y clasificar la fundamentación (Priority: P2)

Un verificador de fundamentación evalúa una propuesta de salida frente a los fragmentos
recuperados y la clasifica como fundamentada, parcialmente fundamentada, no
fundamentada, conflictiva o no verificable, indicando qué afirmaciones tienen soporte y
cuáles no. Cuando una consulta no tiene cobertura suficiente, el sistema lo reconoce en
vez de presentar una respuesta como si estuviera fundamentada.

**Why this priority**: Protege la fiabilidad pedagógica del sistema (Principio V de la
constitución); depende de que exista un flujo de recuperación (User Story 2) sobre el
que evaluar la fundamentación.

**Independent Test**: Puede probarse de forma independiente enviando una consulta sin
cobertura en los materiales autorizados y verificando que el sistema señala la
limitación en vez de inventar una respuesta.

**Acceptance Scenarios**:

1. **Given** una propuesta de salida y los fragmentos que la respaldan, **When** el
   verificador de fundamentación la evalúa, **Then** la clasifica en una de las cinco
   categorías y explica qué afirmaciones tienen soporte.
2. **Given** una consulta sin cobertura en los materiales permitidos, **When** el
   recuperador la procesa, **Then** el sistema lo indica explícitamente y evita generar
   una respuesta específica presentada como fundamentada.
3. **Given** una actividad con conocimiento general desactivado, **When** no hay
   evidencia suficiente, **Then** el sistema reconoce la limitación o solicita
   aclaración en vez de responder como hecho de la asignatura.
4. **Given** una actividad con conocimiento general permitido, **When** el sistema
   recurre a él, **Then** lo etiqueta explícitamente como conocimiento general no
   recuperado de los materiales, distinguiéndolo del contenido fundamentado.
5. **Given** una propuesta en la que solo una parte de sus afirmaciones tiene soporte en
   la evidencia recuperada, **When** el verificador la evalúa, **Then** la clasifica
   como parcialmente fundamentada, indicando qué afirmaciones concretas carecen de
   soporte.
6. **Given** una propuesta con una afirmación soportada por la evidencia y otra
   contradicha por un único fragmento de evidencia (sin que exista un conflicto
   pendiente entre fuentes distintas), **When** el verificador la evalúa, **Then** la
   clasifica como parcialmente fundamentada — una contradicción con una sola fuente no
   convierte por sí sola la propuesta en conflictiva (Session 2026-09-12, ver
   Clarifications).
7. **Given** una propuesta en la que ninguna afirmación tiene soporte y al menos una es
   contradicha por un único fragmento de evidencia (sin conflicto pendiente entre
   fuentes), **When** el verificador la evalúa, **Then** la clasifica como no
   fundamentada, no como conflictiva.

---

### User Story 4 - Aislar materiales por asignatura, actividad y sesión (Priority: P2)

Una consulta de una actividad no puede recuperar fragmentos de otra actividad o
asignatura, ni de materiales inactivos o de versiones retiradas. Un intento de acceso
fuera del alcance autorizado queda bloqueado y registrado de forma trazable.

**Why this priority**: Es un límite de seguridad y privacidad no negociable (Constitución
Principio I y VII); depende de que existan materiales de más de una asignatura o
actividad para poder demostrarse (User Story 1).

**Independent Test**: Puede probarse de forma independiente creando materiales en dos
actividades distintas y verificando que una consulta de una de ellas nunca recupera
fragmentos de la otra.

**Acceptance Scenarios**:

1. **Given** materiales activos en dos actividades distintas, **When** una consulta se
   ejecuta para la actividad A, **Then** el sistema MUST NOT devolver fragmentos
   pertenecientes a la actividad B.
2. **Given** una consulta que solicita materiales fuera del alcance autorizado de la
   sesión, **When** se procesa, **Then** el sistema bloquea la recuperación y registra
   el intento de forma trazable.
3. **Given** un material inactivo o una versión retirada, **When** cualquier consulta lo
   referencia, **Then** el sistema MUST NOT incluirlo en los resultados.

---

### User Story 5 - Sustituir y retirar versiones de materiales (Priority: P2)

Un profesor sustituye un documento por una nueva versión o lo desactiva. Las sesiones
nuevas dejan de recuperar fragmentos de la versión retirada, el registro indica la
versión activa vigente, y las sesiones antiguas conservan la referencia histórica
necesaria para ser auditadas.

**Why this priority**: Evita que el sistema presente contenido obsoleto como vigente,
protegiendo la fiabilidad de los materiales (Principio V); depende de que exista al
menos un documento ya incorporado (User Story 1).

**Independent Test**: Puede probarse de forma independiente sustituyendo la versión de
un documento de prueba y verificando que una sesión nueva solo recupera la versión
activa mientras una sesión histórica conserva su referencia original.

**Acceptance Scenarios**:

1. **Given** un documento con una nueva versión disponible, **When** el profesor la
   sustituye, **Then** la versión anterior queda retirada sin eliminarse del registro
   histórico.
2. **Given** una versión retirada, **When** se inicia una sesión nueva, **Then** ninguna
   consulta recupera fragmentos de esa versión.
3. **Given** una sesión que ya utilizó una versión ahora retirada, **When** un
   investigador la audita, **Then** puede consultar la referencia histórica completa de
   los fragmentos usados en su momento.

---

### User Story 6 - Señalar conflictos entre fuentes activas (Priority: P3)

Dos materiales activos y autorizados contienen afirmaciones incompatibles sobre la misma
consulta. La recuperación devuelve ambas evidencias y marca el conflicto para que el
diálogo lo comunique, y el conflicto queda además registrado de forma persistente y
visible en el área de materiales del profesor para su revisión, en vez de elegir una
fuente de forma arbitraria y perderse tras la consulta.

**Why this priority**: Es una condición de borde importante para la fiabilidad
pedagógica, pero de menor frecuencia esperada que los flujos anteriores; refuerza la
fundamentación ya cubierta por la User Story 3.

**Independent Test**: Puede probarse de forma independiente activando dos documentos de
prueba con afirmaciones contradictorias y verificando que una consulta relacionada
devuelve ambas evidencias marcadas como conflictivas.

**Acceptance Scenarios**:

1. **Given** dos materiales activos con afirmaciones incompatibles sobre el mismo tema,
   **When** una consulta relacionada se ejecuta, **Then** la recuperación devuelve ambas
   evidencias y marca el conflicto de forma explícita.
2. **Given** un conflicto detectado, **When** el verificador de fundamentación evalúa la
   propuesta relacionada, **Then** la clasifica como conflictiva en vez de fundamentada,
   parcialmente fundamentada, no fundamentada o no verificable — conflictiva tiene
   precedencia sobre los demás veredictos mientras el conflicto siga pendiente de
   revisión, incluso si alguna afirmación aislada de la propuesta parecería tener
   soporte (Session 2026-09-12, ver Clarifications).
3. **Given** un conflicto detectado durante una consulta, **When** el profesor revisa su
   área de materiales, **Then** puede ver el conflicto registrado (materiales
   implicados, afirmaciones incompatibles) de forma persistente, no solo como un campo
   efímero de esa consulta.
4. **Given** un conflicto ya revisado por el profesor (`review_status` distinto de
   pendiente), **When** una consulta posterior recupera los mismos materiales
   implicados, **Then** el verificador de fundamentación MUST NOT clasificar la
   propuesta como conflictiva por ese conflicto ya revisado — evalúa la propuesta según
   las demás categorías, conforme al contrato ya vigente (FR-022b acota "pendiente de
   revisión", no "revisado alguna vez").

---

### User Story 7 - Degradar de forma controlada ante un fallo de indexación (Priority: P3)

Un archivo no se puede extraer o indexar. El profesor recibe un error accionable, el
documento no se activa, y el índice ya existente sigue siendo utilizable sin
interrupción.

**Why this priority**: Sin esta garantía, un fallo de indexación podría dejar el sistema
sin materiales disponibles; es una condición de borde de baja frecuencia esperada que
refuerza la degradación controlada ya establecida en la Feature 001 (Principio IX).

**Independent Test**: Puede probarse de forma independiente forzando el fallo de
extracción de un archivo de prueba y verificando que el índice existente sigue
respondiendo consultas con normalidad.

**Acceptance Scenarios**:

1. **Given** un archivo que no puede extraerse o indexarse, **When** el sistema lo
   procesa, **Then** el profesor recibe un error accionable y el documento no se activa.
2. **Given** un fallo de indexación de un documento nuevo, **When** se consulta el
   índice existente, **Then** sigue siendo utilizable sin degradación ni corrupción.

---

### Edge Cases

- ¿Qué ocurre si se carga un documento con el mismo identificador de contenido (hash)
  que uno ya existente? El sistema MUST marcarlo como probable duplicado y MUST dejar
  que el profesor elija entre reutilizar/enlazar el documento existente con la actividad
  actual o continuar como una carga nueva y distinta (ver Clarifications); MUST NOT
  rechazarlo automáticamente ni enlazarlo sin que el profesor lo confirme.
- ¿Qué ocurre si el presupuesto temporal de una consulta se agota antes de completar la
  recuperación? El sistema MUST devolver los resultados parciales obtenidos hasta ese
  momento junto con una advertencia explícita, en vez de fallar sin explicación. Esto es
  un resultado parcial válido, distinto de un fallo o timeout del propio agente de
  recuperación (que se trataría como degradación de agente, no como resultado parcial).
- ¿Qué ocurre si un profesor intenta activar un documento cuyo procesamiento no ha
  finalizado o terminó en error? El sistema MUST rechazar la activación con un mensaje
  comprensible.
- ¿Qué ocurre si dos operaciones de reconstrucción del índice se solicitan de forma
  simultánea? El sistema MUST evitar corromper el índice, aplicando una de ellas de
  forma consistente y tratando la otra de forma explícita (rechazo o encolado), en la
  línea del control de conflictos ya establecido para el estado cognitivo en la Feature
  001.
- ¿Qué ocurre si el texto extraído de un documento contiene instrucciones dirigidas a un
  agente (por ejemplo, "ignora las reglas anteriores")? El sistema MUST tratar ese texto
  como contenido a recuperar, nunca como una instrucción ejecutable.
- ¿Qué ocurre si se ejecuta una consulta de recuperación mientras el índice se está
  reconstruyendo? El sistema MUST servir la consulta contra la última versión de índice
  completamente construida, nunca contra un índice a medio reconstruir.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST permitir a un profesor incorporar documentos dentro de una
  asignatura ya existente (entidad `Course`, definida en la Feature 001).
- **FR-002**: El sistema MUST aceptar como formatos iniciales PDF textual, DOCX, PPTX,
  TXT y Markdown.
- **FR-003**: El sistema MUST identificar los documentos no procesables (por ejemplo,
  escaneados sin texto extraíble) como tales, en vez de indexarlos de forma incompleta y
  silenciosa.
- **FR-004**: El sistema MUST validar formato, tamaño e integridad de cada archivo
  recibido antes de procesarlo, rechazando los archivos inválidos con un mensaje
  accionable.
- **FR-005**: El sistema MUST calcular un identificador de contenido (hash) por
  documento para evitar duplicados accidentales.
- **FR-005a**: Cuando el hash de un archivo cargado coincida con el de un documento ya
  existente, el sistema MUST marcarlo como probable duplicado y MUST ofrecer al
  profesor la elección entre reutilizar/enlazar el documento existente con la actividad
  actual o continuar como una carga nueva y distinta; el sistema MUST NOT decidir esto
  de forma automática (ver Clarifications; Constitución Principio VI — toda modificación
  de materiales debe ser una decisión manual y auditable). Si el profesor elige
  reutilizar/enlazar, el sistema MUST asociar el documento existente a la actividad
  actual sin alterar su estado de activación vigente ni requerir un nuevo ciclo de
  procesamiento.
- **FR-006**: El sistema MUST extraer el texto de cada documento conservando
  referencias de ubicación (página, diapositiva, sección o párrafo) cuando el formato lo
  permita.
- **FR-007**: El sistema MUST segmentar el texto extraído de forma configurable y
  reproducible: la misma configuración sobre el mismo documento MUST producir los mismos
  fragmentos.
- **FR-008**: El sistema MUST generar, para cada documento y fragmento, como mínimo los
  metadatos: identificador, documento de origen, versión, hash, ubicación
  (página/diapositiva/sección), tipo de contenido, asignatura, actividad, fecha de
  incorporación, estado de autorización, vigencia, prioridad, idioma y estado de
  indexación. El campo "prioridad" MUST utilizarse únicamente para influir en el orden
  de relevancia de la recuperación (FR-018); MUST NOT interpretarse ni utilizarse como
  una medida de dificultad atribuida a ningún participante.
- **FR-009**: El sistema MUST generar embeddings y construir el índice de recuperación
  de forma local, sin depender de servicios externos.
- **FR-010**: El sistema MUST ejecutar comprobaciones de cobertura (proporción de
  páginas, diapositivas, secciones o párrafos de los que se extrajo texto utilizable
  respecto del total del documento) y errores tras indexar un documento, y reportarlas
  al profesor.
- **FR-011**: Un documento MUST permanecer inutilizable en sesiones hasta que su
  procesamiento se complete y un profesor lo active manualmente.
- **FR-012**: El sistema MUST permitir a un profesor consultar el estado de
  procesamiento de cada documento (pendiente, procesado, en error, activo o inactivo).
- **FR-013**: El sistema MUST permitir a un profesor activar o desactivar materiales y
  asignarlos a actividades específicas. Un material desactivado (a diferencia de uno
  retirado, FR-015) MUST poder reactivarse posteriormente por el profesor.
- **FR-013a**: El sistema MUST rechazar la asignación de una versión retirada o
  inactiva de un documento a una nueva actividad; solo la versión activa vigente de un
  documento MUST poder asignarse.
- **FR-014**: El sistema MUST permitir a un profesor sustituir un documento por una
  nueva versión sin eliminar la versión anterior del registro histórico. La nueva
  versión MAY estar en un formato admitido (FR-002) distinto al de la versión anterior.
- **FR-015**: Cuando una versión de un documento se sustituye o desactiva, el sistema
  MUST impedir que sesiones nuevas recuperen fragmentos de esa versión, y MUST conservar
  la referencia histórica necesaria para auditar las sesiones que ya la utilizaron —como
  mínimo, el documento, la versión, el contenido de los fragmentos usados y su ubicación
  en el momento en que la sesión los utilizó. A diferencia de un material desactivado
  (FR-013), una versión retirada MUST NOT poder reactivarse; para volver a usar su
  contenido, el profesor MUST crear una nueva versión.
- **FR-016**: El sistema MUST permitir a un profesor reconstruir el índice de materiales
  sin perder la relación entre documentos, fragmentos y versiones.
- **FR-016a**: La reconstrucción del índice MUST preservar los identificadores
  existentes de cada fragmento o, si se regeneran, MUST actualizar las referencias ya
  existentes en `Evidence`, `GroundingVerificationResult` y `MaterialConflictRecord`, de
  modo que ningún registro previamente creado quede huérfano tras una reconstrucción.
- **FR-017**: El agente de recuperación MUST aceptar una consulta junto con filtros de
  autorización (sesión, asignatura, actividad, materiales permitidos), un número máximo
  de fragmentos y un presupuesto temporal.
- **FR-018**: El agente de recuperación MUST devolver, por cada resultado: los
  fragmentos, su procedencia (documento, versión, ubicación), relevancia, metadatos, la
  versión del índice utilizada, advertencias y los conflictos detectados.
- **FR-019**: El agente de recuperación MUST NOT devolver fragmentos de una asignatura,
  actividad, versión retirada o material inactivo distintos de los autorizados para la
  sesión en curso.
- **FR-019a**: El agente de recuperación MUST excluir de sus resultados los fragmentos
  cuyo material haya superado su vigencia configurada (FR-008), tratándolos como si
  estuvieran retirados.
- **FR-020**: Una recuperación MUST ser repetible: la misma consulta, configuración y
  versión de índice MUST producir el mismo resultado, en el mismo orden.
- **FR-021**: Cuando una consulta no tenga cobertura suficiente en los materiales
  autorizados, el sistema MUST señalarlo explícitamente en vez de generar una respuesta
  presentada como fundamentada.
- **FR-022**: Cuando dos o más materiales activos autorizados contengan afirmaciones
  incompatibles relevantes para la misma consulta, la recuperación MUST devolver ambas
  evidencias y marcar el conflicto de forma explícita.
- **FR-022a**: Todo conflicto detectado entre materiales MUST quedar registrado de forma
  persistente y visible en el área de materiales del profesor (documentos y afirmaciones
  implicadas), no únicamente como un campo transitorio de la respuesta de la consulta
  que lo detectó (ver Clarifications; Constitución Principio VI).
- **FR-022b**: Un conflicto registrado que siga pendiente de revisión MUST seguir
  devolviéndose como conflictivo en cualquier consulta posterior que recupere los mismos
  materiales implicados, hasta que el profesor lo revise (FR-022a).
- **FR-023**: Un verificador de fundamentación MUST clasificar cada propuesta de salida
  como fundamentada, parcialmente fundamentada, no fundamentada, conflictiva o no
  verificable, indicando qué afirmaciones tienen soporte y cuáles no. Este veredicto
  MUST evaluar exclusivamente la propuesta y su respaldo documental; MUST NOT
  interpretarse ni utilizarse como una medida de la capacidad o el desempeño del
  participante.
- **FR-023a**: El sistema MUST NOT agregar ni acumular los veredictos de fundamentación
  de un participante a lo largo de una o varias sesiones como una señal de su capacidad
  o progreso.
- **FR-024**: Cuando el conocimiento general esté desactivado para la actividad
  (`ActivityConfiguration.general_knowledge_allowed = false`, Feature 001) y no exista
  evidencia suficiente, el sistema MUST reconocer la limitación o solicitar aclaración
  en vez de responder como hecho de la asignatura.
- **FR-025**: Cuando el conocimiento general esté permitido para la actividad, el
  sistema MUST etiquetar explícitamente el contenido no recuperado de los materiales
  como conocimiento general, distinguiéndolo del contenido fundamentado.
- **FR-026**: Un intento de recuperación que solicite materiales fuera del alcance
  autorizado de la sesión (otra asignatura o actividad) MUST ser bloqueado y MUST quedar
  registrado de forma trazable.
- **FR-027**: Un fallo de extracción o indexación de un documento MUST producir un error
  accionable para el profesor, MUST NOT activar el documento, y MUST NOT afectar la
  disponibilidad del índice ya existente.
- **FR-028**: El sistema MUST tratar el texto extraído de los documentos como datos,
  nunca como instrucciones ejecutables para los agentes, incluso si su contenido imita
  instrucciones del sistema.
- **FR-029**: El sistema MUST conservar la trazabilidad de cada fragmento devuelto hasta
  su documento, versión y ubicación de origen.
- **FR-030**: Esta feature MUST NOT modificar el comportamiento ya validado del núcleo
  cognitivo de la Feature 001 (contratos de agente, ciclo de sesión/turno, control
  constitucional, versionado del estado cognitivo); únicamente añade materiales,
  recuperación y verificación de fundamentación como capacidades nuevas. El veredicto de
  fundamentación de esta feature y el veredicto constitucional de la Feature 001 MUST
  evaluarse y registrarse de forma independiente; ninguno de los dos MUST sustituir,
  ocultar o sobrescribir al otro.
- **FR-031**: Los endpoints de gestión de materiales de esta feature MUST heredar el
  mismo vínculo exclusivo a la máquina local (`127.0.0.1`) ya establecido en la Feature
  001 (FR-022); esta feature MUST NOT introducir un nuevo punto de exposición de red.
- **FR-032**: Las pantallas nuevas del área técnica introducidas por esta feature (carga,
  activación, revisión de conflictos, resolución de duplicados) MUST cumplir el mismo
  estándar de accesibilidad ya exigido en la Feature 001 (FR-025): operables
  íntegramente por teclado, con etiquetas accesibles, contraste suficiente, y mensajes
  de error comprensibles que no dependan únicamente del color para transmitir su
  significado.

### Key Entities

- **MaterialDocument**: archivo docente versionado, procesado y autorizado; pertenece a
  un `Course` (Feature 001) y opcionalmente a una o más `ActivityConfiguration`.
- **MaterialFragment**: unidad recuperable de un `MaterialDocument`, con texto,
  ubicación, metadatos, embedding y autorización heredada de su documento de origen.
- **Evidence**: fragmento o resultado verificable que respalda (o contradice) una
  afirmación o decisión, incluida su procedencia completa.
- **GroundingVerificationResult**: clasificación observable de fundamentación de una
  propuesta de salida frente a la evidencia recuperada, en uno de cinco valores
  (aclarado en Session 2026-09-12; ver Clarifications — la redacción anterior de este
  párrafo dejaba ambiguo el alcance de "conflictiva" y se sustituye por completo):
  - **fundamentada**: todas las afirmaciones de la propuesta están soportadas por la
    evidencia recuperada.
  - **parcialmente fundamentada**: al menos una afirmación está soportada y al menos
    una no lo está (por falta de respaldo o por contradicción con una fuente
    individual) — siempre que la evidencia utilizada no esté afectada por un
    conflicto pendiente entre fuentes (si lo está, ver "conflictiva", que tiene
    precedencia).
  - **no fundamentada**: ninguna afirmación está soportada, y al menos una carece de
    respaldo en la evidencia o contradice una fuente individual.
  - **no verificable**: ninguna afirmación está soportada, y el mecanismo no puede
    determinar de forma fiable si hay respaldo o contradicción (p. ej. evidencia
    vacía con conocimiento general permitido, o una expresión de la propuesta que el
    analizador no puede interpretar con seguridad y que no coincide literalmente con
    la evidencia).
  - **conflictiva**: la evidencia utilizada toca un conflicto **pendiente y
    registrado** entre dos o más fuentes autorizadas (Escenario D, User Story 6 —
    `MaterialConflictRecord` con revisión docente pendiente, o el mecanismo
    contractual equivalente). Tiene **precedencia** sobre los otros cuatro valores
    cuando ese conflicto existe. Una contradicción entre la propuesta y un **único**
    fragmento de evidencia (sin que exista un conflicto de esa naturaleza entre
    fuentes) NO constituye por sí sola un conflicto y NO debe generar un
    `MaterialConflictRecord` sintético — se clasifica como "no fundamentada" o
    "parcialmente fundamentada" según corresponda arriba.

  Es una entidad distinta del `VerificationResult` constitucional de la Feature 001
  (cuyo veredicto cerrado de cuatro valores —aprobado/reformular/aclarar/bloquear— no
  se modifica): esta feature añade fundamentación como un control adicional,
  independiente del control constitucional ya existente (Constitución Principio IV:
  "controles de fundamentación y constitucionales").
- **MaterialConflictRecord**: registro persistente de un conflicto detectado entre dos o
  más materiales activos (documentos y fragmentos implicados, afirmaciones
  incompatibles, consulta que lo detectó, estado de revisión docente), visible en el
  área de materiales del profesor hasta que se revise (ver Clarifications).

*(Course, ActivityConfiguration, Session, Turn, AgentContract e InternalMessage se
reutilizan tal como quedaron definidos en la Feature 001, sin cambios.)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El 100% de los fragmentos recuperados en las pruebas pueden atribuirse a
  su documento, versión y ubicación de origen.
- **SC-002**: El 0% de los resultados de recuperación en sesiones de prueba incluye
  material inactivo o una versión retirada.
- **SC-003**: Tras sustituir la versión de un documento, el 100% de las sesiones nuevas
  de prueba obtienen únicamente fragmentos de la versión activa.
- **SC-004**: El 100% de las consultas de prueba sin evidencia suficiente generan una
  señal explícita y trazable en vez de una respuesta presentada como fundamentada.
- **SC-005**: El verificador de fundamentación detecta el 100% de las referencias que no
  respaldan la afirmación atribuida en el conjunto de pruebas preparado para esta
  feature.
- **SC-006**: El índice puede reconstruirse por completo sin pérdida de la relación
  entre documentos, fragmentos y versiones, verificable comparando el índice
  reconstruido con el original.
- **SC-007**: Un profesor puede cargar, procesar y activar un documento de prueba en un
  único flujo sin intervención técnica externa.
- **SC-008**: El 100% de los intentos de recuperación fuera del alcance autorizado
  (otra asignatura o actividad) de las pruebas quedan bloqueados y registrados.

## Assumptions

- El comportamiento ya validado de la Feature 001 (núcleo cognitivo, contratos de
  agente, ciclo de sesión/turno, control constitucional, versionado del estado
  cognitivo) permanece sin cambios; esta feature es puramente aditiva. Cómo se integra
  el nuevo agente de recuperación en el flujo de turno existente es una decisión de
  `/speckit-plan`, no de esta especificación.
- El agente de recuperación y el verificador de fundamentación de esta feature
  implementan el mismo protocolo de agente (`AgentContract`, entradas/salidas
  estructuradas, tiempo máximo, cancelación) ya definido en la Feature 001; esta feature
  no introduce una forma de contrato de agente distinta.
- Los documentos cargados por el profesorado se asumen libres de datos personales de
  terceros no autorizados; esta feature no implementa detección ni redacción automática
  de datos personales dentro del contenido de los documentos — es responsabilidad del
  profesorado al seleccionar los materiales que carga.
- El límite exacto de tamaño de archivo admitido es una decisión de planificación
  (según el perfil de hardware, igual que los límites de tiempo/recursos ya
  establecidos en la Feature 001), pero se espera que corresponda a documentos docentes
  individuales (apuntes, diapositivas, guiones), no a archivos multimedia de gran
  tamaño.
- La eliminación definitiva (borrado físico) de un `MaterialDocument` queda fuera de
  alcance de esta feature; solo se admite desactivación (reversible) o retirada por
  sustitución de versión (irreversible, FR-013/FR-015). El borrado definitivo se
  abordará, si procede, en la Feature 005 (configuración docente, revisión, privacidad y
  exportación).
- El criterio exacto para detectar que dos fragmentos contienen "afirmaciones
  incompatibles" (FR-022) es una decisión técnica de planificación (ver `research.md`),
  no de esta especificación; el requisito funcional es que el conflicto se detecte, se
  devuelva junto a ambas evidencias y se registre para revisión docente.
- La "colección de una asignatura" mencionada en la fuente se representa mediante la
  entidad `Course` ya existente (Feature 001), no como una entidad nueva.
- El campo `ActivityConfiguration.general_knowledge_allowed` (Feature 001) sigue siendo
  la única fuente de verdad sobre si el conocimiento general está permitido; esta
  feature no introduce un mecanismo paralelo.
- Los parámetros exactos de segmentación (tamaño de fragmento, solapamiento) y el
  modelo de embeddings son decisiones técnicas de planificación, no de esta
  especificación; el requisito funcional es que la segmentación sea configurable y
  reproducible.
- OCR avanzado de documentos escaneados, acceso web, generación automática de material
  docente, modificación de documentos originales, evaluación de la calidad académica del
  participante y recomendación longitudinal personalizada quedan fuera de alcance,
  conforme a `docs/ORAL-IA_SpecKit/features/002_materials_rag_specify.md`.
- Un intento de recuperación fuera del alcance autorizado (User Story 4) se comunica al
  participante como ausencia de evidencia suficiente (mismo tratamiento que la User
  Story 3), sin revelar la existencia de materiales de otras asignaturas o actividades;
  el detalle completo del intento bloqueado queda visible solo en el área técnica o de
  investigador, siguiendo el mismo patrón de separación ya establecido en la Feature 001
  (FR-012b).
