<!--
Sync Impact Report — 2026-10-30
- Version change: 1.0.0 → 2.0.0 (MAJOR: narrow exception to the blanket session Internet exclusion).
- Human authorization: web fallback when course evidence is insufficient, visibly external,
  checked for validity and against the teacher's material. Development amendment, not a
  policy change by the product during a participant session.
- Modified principles: I (restricted fallback), V (external evidence and contradictions),
  VII (minimised external queries; inference stays local), and MVP exclusions.
- Added sections: none. Removed principles: none.
- ✅ Templates checked: plan-template.md updated; spec/tasks templates remain compatible.
- ✅ Feature012 spec/plan/tasks and RAG contract synchronised; restricted web contract added.
- ✅ README.md and docs/ORAL-IA_SpecKit/README.md synchronised; historical evidence preserved.
- ✅ Installed SpecKit skills checked; no operational blanket web exclusions found.
- Implementation remains off: no runtime network activation, model calls or migration.
- No deferred constitution placeholders. Implementation tasks T114–T118 remain pending.
-->

<!-- Historical ratification report, preserved below.
Sync Impact Report
- Version change: (unratified template) → 1.0.0
- Rationale: Initial ratification of the ORAL-IA constitution. Bump is MAJOR because this
  establishes the full governance baseline (11 core principles + scope + workflow +
  governance) where none previously existed.
- Source: docs/ORAL-IA_SpecKit/00_constitution_prompt.md (principles I–XI, and governance
  rules originally drafted as "XII. Gobierno de la constitución", relocated here to the
  template's Governance section). Sections "Alcance por Fases y Features Acumulativas" and
  "Flujo de Trabajo Spec Kit" derived from docs/ORAL-IA_SpecKit/README.md operational rules.
- Modified principles: n/a (initial adoption)
- Added sections: Core Principles I–XI; Alcance por Fases y Features Acumulativas;
  Flujo de Trabajo Spec Kit; Governance
- Removed sections: none
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — Constitution Check gate is dynamic
    ("[Gates determined based on constitution file]"); no edit required, still compatible.
  - ✅ .specify/templates/spec-template.md — generic, no constitution-specific references
    to reconcile.
  - ✅ .specify/templates/tasks-template.md — generic, no constitution-specific references
    to reconcile.
  - ✅ .claude/skills/speckit-*/SKILL.md — reviewed, no outdated agent-specific naming
    found that requires generic-guidance correction.
  - ✅ docs/ORAL-IA_SpecKit/README.md — already describes the constitution-first,
    six-feature cumulative workflow reflected in this constitution; no edit required.
- Follow-up TODOs: none — no placeholders deferred.
-->

# ORAL-IA Constitution

## Core Principles

### I. Finalidad y límites institucionales

ORAL-IA es un asistente automático de apoyo docente. Debe identificarse siempre como
sistema de IA, reconocer que puede cometer errores y permanecer dentro de la actividad y de
los materiales autorizados. No puede presentarse como profesor, asignar notas, emitir
decisiones académicas, aplicar rúbricas de forma autónoma, inferir capacidad académica o
sustituir el criterio del profesorado.

La versión mínima funciona localmente en un ordenador y no incorpora robots, control de
dispositivos físicos, acceso abierto a Internet durante las sesiones, Moodle, expedientes
académicos, correo, calendario ni otros sistemas personales o institucionales.

Como excepción acotada, el autoestudio puede consultar documentación pública en Internet
cuando la evidencia local no baste y la política versionada de la actividad lo habilite.
No se permite navegación abierta ni búsqueda de temas confirmados fuera de la actividad.
El acceso externo se mantiene desactivado hasta implementar y validar los controles de
los Principios IV, V y VII; esta autorización no activa conexiones en perfiles existentes.

**Rationale**: ORAL-IA opera en un contexto educativo donde la confusión entre asistencia y
autoridad académica, o la ampliación no controlada de superficies de integración, generaría
riesgos éticos, legales y de seguridad desproporcionados para un MVP.

### II. Arquitectura modular basada en contratos

Toda capacidad cognitiva relevante debe pertenecer a un agente con responsabilidad única y
explícita. Cada agente debe declarar, mediante un contrato versionado: identificador,
versión, propósito, entradas, salidas estructuradas, precondiciones, postcondiciones,
fuentes y herramientas permitidas, permisos, tiempo máximo, consumo esperado, errores
posibles, confianza, criterios de éxito, terminación, cancelación y datos de trazabilidad.

Los agentes pueden ejecutarse dentro de un mismo proceso. La modularidad se demuestra
mediante límites de software, esquemas y pruebas, no mediante microservicios prematuros.
Ningún agente puede depender de detalles internos de otro agente ni intercambiar únicamente
texto libre cuando exista un esquema estructurado adecuado.

**Rationale**: los contratos versionados permiten razonar, probar y sustituir cada agente de
forma independiente sin exigir una infraestructura distribuida que la escala del MVP no
justifica.

### III. Estado cognitivo explícito y memoria diferenciada

El estado relevante de una sesión debe mantenerse fuera del contexto privado del modelo de
lenguaje, en una pizarra cognitiva estructurada, versionada y reconstruible. Toda
modificación debe identificar al agente responsable, la versión previa, la versión
resultante, el instante y la justificación.

El sistema debe distinguir como mínimo memoria de trabajo, memoria episódica de sesión,
memoria semántica de materiales, memoria procedimental de agentes y agencias, y memoria
metacognitiva de fallos y verificaciones. No debe crear durante el MVP perfiles psicológicos
o académicos longitudinales del estudiante.

**Rationale**: un estado externo y versionado es lo que hace posible la trazabilidad
(Principio VIII) y evita que decisiones críticas dependan de contexto oculto e
irreproducible dentro del modelo.

### IV. Separación entre recuperación, generación, decisión y verificación

Recuperar evidencias, generar una propuesta, decidir la siguiente acción conversacional y
autorizar la presentación son responsabilidades separadas. El agente generador nunca puede
aprobar por sí solo su salida.

Toda salida docente debe pasar, como mínimo, por controles de fundamentación y
constitucionales. Los verificadores deben poder aprobar, reformular, pedir aclaración,
marcar incertidumbre o bloquear. La reflexión verbal de un modelo no constituye por sí sola
una verificación; deben preferirse comprobaciones externas y observables.

**Rationale**: separar generación de verificación evita que un único agente sea juez y
parte, y sustituye la falsa seguridad de la "auto-reflexión" del modelo por controles
observables y auditables.

### V. Fundamentación en materiales autorizados

Las afirmaciones específicas de la asignatura deben sustentarse preferentemente en
materiales autorizados, activos y vigentes. El sistema debe conservar la procedencia de los
fragmentos usados y mostrarla al usuario cuando corresponda.

El conocimiento general del modelo está desactivado por defecto. Solo puede utilizarse si la
configuración versionada de la actividad lo permite y debe etiquetarse claramente como
conocimiento general no recuperado de los materiales. Cuando no haya evidencia suficiente,
el sistema debe reconocerlo en lugar de inventar una respuesta.

La ampliación web debe identificar explícitamente la información externa y sus enlaces,
separándola de los materiales del profesor. Antes de incorporarla a la explicación, debe
contrastar autoría, contexto y respaldo de sus afirmaciones, y su compatibilidad con el
material docente vigente pertinente. Una URL, un dominio conocido o varias copias del
mismo contenido no prueban validez. El generador no aprueba su propia salida.

Si encuentra una contradicción, debe señalar la discrepancia y sus fuentes sin sustituir
silenciosamente el material del profesor ni presentar la afirmación conflictiva como
contenido establecido de la asignatura. Si no puede resolver el respaldo o la comparación,
debe comunicar la incertidumbre y pedir aclaración o revisión docente cuando corresponda.
No encontrar contradicciones en una revisión limitada no garantiza su ausencia universal.

**Rationale**: en un contexto docente, una afirmación no trazable a una fuente autorizada
es indistinguible de una alucinación; la fundamentación explícita es la base de la confianza
pedagógica en el sistema.

### VI. Supervisión humana y gobernanza

El profesorado controla materiales, actividades, preguntas iniciales, límites, agentes
obligatorios u opcionales, modelos, conservación de sesiones y eliminación de datos. Las
reglas fundamentales no pueden ser modificadas por agentes durante una sesión. Toda
modificación de la constitución, políticas, contratos o configuraciones debe ser manual,
versionada y auditable.

Las K-lines o configuraciones cognitivas reutilizables pueden proponerse automáticamente,
pero no consolidarse ni activarse permanentemente sin revisión humana durante el MVP.

**Rationale**: el sistema es una herramienta de apoyo, no un agente autónomo con autoridad
sobre su propia gobernanza; el control humano final es un requisito, no una opción de
configuración.

### VII. Privacidad, minimización y accesibilidad

La ejecución, recuperación, inferencia y transcripción deben realizarse localmente. Los
participantes se representan mediante códigos seudónimos. El audio se procesa y descarta; no
se conserva por defecto. Las transcripciones solo se almacenan con consentimiento explícito,
son revisables y corregibles, tienen retención limitada y pueden eliminarse.

La única excepción de red es la consulta/descarga pública habilitada en el Principio I.
La extracción, generación y revisión permanecen locales. Las consultas externas deben
limitarse al concepto académico necesario, sin enviar transcripciones, documentos privados,
identificadores, audios, credenciales ni datos personales. Si no puede construirse una
consulta mínima segura, no se realiza la petición. La actividad debe informar del acceso
externo y sus condiciones antes de usarlo; habilitarlo no cambia consentimientos anteriores.

La modalidad textual debe permitir realizar todas las funciones esenciales. La interfaz debe
ser utilizable mediante teclado, ofrecer etiquetas accesibles, contraste adecuado, control
del ritmo, pausa, repetición, corrección de transcripción y mensajes de error comprensibles.
La voz es opcional y nunca un requisito de acceso.

**Rationale**: procesar datos de estudiantes localmente y minimizar su retención reduce el
riesgo de exposición; exigir una vía textual completa evita que la accesibilidad dependa de
una modalidad opcional.

### VIII. Trazabilidad y reproducibilidad

Toda respuesta o acción relevante debe poder relacionarse con la sesión, configuración,
versión del sistema, modelo y parámetros, agentes ejecutados, mensajes internos, cambios de
estado, fragmentos recuperados, verificaciones, decisiones, latencias, errores y consumo de
recursos.

La reproducción significa reconstruir el flujo, los datos y las decisiones a partir de
registros. No se debe prometer identidad byte a byte de salidas generativas salvo que se
hayan fijado modelo, versión, semilla y condiciones deterministas.

Los registros no deben almacenar datos personales que no sean necesarios ni cadenas de
razonamiento privadas del modelo. Deben registrar resultados estructurados y
justificaciones operativas observables.

**Rationale**: sin trazabilidad completa del flujo de decisión, ni el profesorado ni una
auditoría posterior pueden verificar por qué el sistema actuó de una forma determinada.

### IX. Degradación controlada y límites de recursos

Cada agente y sesión debe disponer de límites explícitos de tiempo, memoria, contexto,
iteraciones, recuperaciones, almacenamiento y llamadas al modelo. Los fallos deben
transformarse en estados conocidos y trazables, no en bloqueos silenciosos.

Cuando un componente no esté disponible, el sistema debe degradarse de forma explícita:
pasar de voz a texto, reducir contexto o recuperación, desactivar análisis secundarios,
usar un modelo alternativo autorizado, aplazar resúmenes o finalizar de forma segura. Los
controles constitucionales y de privacidad nunca pueden omitirse por ahorro de recursos.

**Rationale**: un sistema sin límites explícitos falla de forma impredecible; la
degradación controlada preserva la seguridad y la privacidad incluso cuando el rendimiento
se reduce.

### X. Calidad, pruebas y evidencia

Cada requisito funcional debe poseer criterios de aceptación observables. Cada agente debe
disponer de pruebas unitarias de contrato; cada agencia, pruebas de integración; cada flujo
prioritario, una prueba extremo a extremo. Deben existir pruebas de fallo, cancelación,
timeout, datos insuficientes, conflicto entre fuentes, degradación y bloqueo constitucional.

La arquitectura debe compararse con un baseline monolítico cuando proceda. Las métricas
evaluarán el sistema y su arquitectura, no la capacidad o personalidad del estudiante.

No se considera terminada una feature si no incluye código, pruebas, trazabilidad,
documentación mínima, migraciones o datos de ejemplo necesarios, manejo de errores,
comprobación de privacidad y evidencia de que satisface sus escenarios de aceptación.

**Rationale**: la hipótesis arquitectónica del proyecto (sociedad de agentes frente a un
monolito) solo es defendible si existe evidencia medible y comparable, no solo una
implementación funcional.

### XI. Simplicidad evolutiva

Debe implementarse la solución más sencilla que preserve los contratos y permita medir la
hipótesis arquitectónica. Se evitarán frameworks de agentes, colas, bases de datos o
servicios distribuidos que oculten el comportamiento o compliquen la reproducibilidad sin
aportar una necesidad demostrable.

Toda dependencia nueva debe justificar qué requisito satisface, qué alternativa más simple
se descartó y cómo se sustituiría mediante un adaptador. Los componentes de inferencia,
embeddings, vectorización, transcripción y síntesis deben quedar detrás de interfaces
reemplazables.

**Rationale**: la complejidad de infraestructura no demostrada por una necesidad concreta
compromete la reproducibilidad (Principio VIII) y dificulta medir si la arquitectura
multiagente aporta valor real frente a un baseline monolítico (Principio X).

## Alcance por Fases y Features Acumulativas

El sistema se construye como una constitución común y seis features acumulativas, en este
orden:

1. Núcleo cognitivo y ejecución local
2. Materiales autorizados y RAG trazable
3. Agencia de autoestudio
4. Agencia de defensa oral y voz opcional
5. Configuración docente, revisión, privacidad y exportación
6. Validación arquitectónica y comparación con baseline monolítico

Cada feature MUST quedar integrada, probada y revisada antes de iniciar la siguiente. Las
features posteriores pueden depender de las anteriores, pero no deben reescribir sus
contratos sin una decisión arquitectónica explícita, documentada y versionada conforme al
Principio II.

Quedan fuera del alcance del MVP: robots y dispositivos físicos; integración con Moodle y
sistemas institucionales; expedientes y calificaciones oficiales; evaluación automática,
notas o aplicación autónoma de rúbricas; acceso abierto a Internet durante sesiones, salvo
la ampliación documental restringida de autoestudio definida en los Principios I/V/VII; creación
autónoma de código o agentes; memoria académica o psicológica longitudinal; herramientas
personales como correo o calendario; y microservicios distribuidos salvo necesidad
demostrada. Estas exclusiones desarrollan operativamente los límites ya fijados en los
Principios I, III y XI, y solo pueden ampliarse mediante enmienda constitucional.

## Flujo de Trabajo Spec Kit

La constitución se establece una única vez con `/speckit-constitution` y gobierna todas las
features. Para cada feature, en orden estricto: `/speckit-specify` → `/speckit-clarify` →
`/speckit-plan` → `/speckit-checklist` → `/speckit-tasks` → `/speckit-analyze` →
`/speckit-implement` → `/speckit-converge`.

La implementación (`/speckit-implement`) MUST NOT comenzar mientras `/speckit-analyze`
reporte errores críticos, requisitos sin cobertura o contradicciones entre la constitución,
la especificación, el plan y las tareas. `/speckit-converge` se repite hasta satisfacer los
criterios de terminación de la feature (definition of done) antes de iniciar la siguiente
feature de la lista de la sección anterior.

## Governance

La constitución prevalece sobre decisiones locales de una feature. Las excepciones
requieren una enmienda explícita con motivación, impacto, alternativa considerada y plan de
migración. Los cambios incompatibles en contratos, estado cognitivo, políticas o esquemas
persistidos requieren versionado y pruebas de compatibilidad o migración.

**Procedimiento de enmienda**: cualquier cambio a este documento debe proponerse por
escrito, indicar el principio o sección afectada, la motivación, el impacto en features en
curso y, si aplica, el plan de migración. El cambio se incorpora manualmente al archivo
`.specify/memory/constitution.md`, nunca por un agente durante una sesión (Principio VI).

**Política de versionado**: esta constitución usa versionado semántico MAJOR.MINOR.PATCH.
MAJOR indica eliminación o redefinición incompatible de un principio o regla de gobernanza;
MINOR indica la adición de un principio o una ampliación material de una guía existente;
PATCH indica aclaraciones o correcciones de redacción sin cambio de norma.

**Expectativas de cumplimiento**: en cada revisión (incluyendo `/speckit-analyze` y
`/speckit-converge`) se debe comprobar conformidad con la constitución, cobertura de
requisitos, límites de alcance, privacidad, trazabilidad, pruebas, recursos, degradación y
documentación, conforme al Principio X. Un hallazgo que viole un principio marcado como
obligatorio (MUST) se trata como severidad crítica y bloquea el avance de la feature hasta
su resolución o hasta que se apruebe una enmienda explícita.

**Version**: 2.0.0 | **Ratified**: 2026-07-21 | **Last Amended**: 2026-10-30
