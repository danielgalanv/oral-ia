# Feature Specification: Agencia de defensa oral y voz opcional

**Feature Branch**: `004-oral-defense-agency`

**Created**: 2026-09-02

**Status**: APTA PARA IMPLEMENTACIÓN

**Input**: User description: "Feature 004 — Agencia de defensa oral y voz opcional: añadir un simulador de defensa oral construido sobre los mismos agentes, contratos, estado, materiales y verificadores utilizados por la agencia de autoestudio (Feature 003). La voz es una modalidad opcional de entrada y salida; todas las funciones esenciales deben estar disponibles por texto. Formulación de preguntas, captura de respuesta por texto o voz, transcripción local cuando se use voz, revisión/corrección de la transcripción por el estudiante, análisis de la respuesta, generación de repreguntas contextuales, gestión del diálogo de defensa, síntesis de voz opcional, cierre y resumen descriptivo — sin evaluación académica, notas, inferencia de capacidad o nivel, arquitectura paralela a SelfStudyAgency, duplicación de agentes reutilizables, robot/embodiment, conservación de audio por defecto, ni servicios cloud obligatorios." (fuente: `docs/ORAL-IA_SpecKit/features/004_oral_defense_specify.md`, `.specify/memory/constitution.md`, `docs/ORAL-IA_SpecKit/13_definition_of_done.md`, `docs/ORAL-IA_SpecKit/14_domain_model.md`, Features 001–003 ya implementadas)

## Clarifications

### Session 2026-09-02

- Q: Cuando la transcripción de voz tiene confianza insuficiente o segmentos dudosos,
  ¿qué debe ofrecer el sistema al estudiante? → A: Corrección textual de los segmentos
  señalados, con la posibilidad de cambiar a responder por texto desde ese punto — MUST
  NOT ofrecerse repetir la grabación de audio.
- Q: ¿Cuándo debe el sistema pedir confirmación o corrección de una transcripción de
  voz, en vez de continuar directamente? → A: Únicamente cuando la propia transcripción
  señala un segmento de baja confianza o incompleto en un punto crítico; esta solicitud
  es una incidencia de la modalidad de voz, previa a cualquier procesamiento cognitivo
  de la respuesta — no constituye por sí misma una decisión de diálogo de la agencia de
  defensa (ver FR-022, FR-022a). Una respuesta de texto breve o poco desarrollada MUST
  NOT disparar por sí sola esta solicitud — se trata como una respuesta válida sobre la
  que generar una repregunta normal.
- Q: Si la transcripción de una grabación falla (error técnico, no baja confianza),
  ¿qué ocurre con ese audio antes de descartarlo? → A: Se descarta de inmediato, sin
  ningún reintento sobre el mismo audio; el sistema degrada a texto en el mismo turno.
- Q: ¿"Cambiar de tema" durante una defensa oral debe ser una acción de diálogo distinta
  y visible, o expresarse con las acciones ya existentes de la Feature 003? → A: Se
  reutiliza la acción `ask` ya existente tanto para profundizar en el mismo tema como
  para cambiar a un tema distinto — MUST NOT introducirse una acción `change_topic`
  nueva; la diferencia queda visible en la traza mediante los conceptos/materiales
  referenciados, no como un valor de acción distinto.
- Q: ¿Cuándo debe la agencia de defensa seleccionar la acción de diálogo de aclaración
  (`clarify`) sobre una respuesta ya confirmada como definitiva, y en qué se distingue
  de la solicitud de confirmación por baja confianza de transcripción? → A: MUST
  seleccionarse cuando la respuesta textual definitiva del participante no proporciona
  información suficiente o inequívoca para decidir con seguridad el siguiente paso del
  diálogo — por ejemplo, si no puede relacionarse razonablemente con la pregunta o los
  conceptos autorizados relevantes, si admite varias interpretaciones plausibles que
  llevarían a continuaciones distintas, o si contiene una aparente incompatibilidad
  interna que requiere saber qué quiso expresar el participante. Es una decisión
  cognitiva sobre una respuesta textual ya definitiva — MUST distinguirse por completo
  de la solicitud de confirmación/corrección por baja confianza de transcripción
  (incidencia de modalidad previa a la entrada cognitiva, FR-022); el umbral o
  algoritmo exacto de detección es una decisión de planificación técnica, no de esta
  especificación (ver FR-018b).
- Q: Si el mecanismo de generación de la pregunta inicial o de una repregunta falla o
  no está disponible, ¿debe perderse la sesión? → A: MUST NOT perderse la sesión por
  ese motivo; el sistema intenta las alternativas de generación autorizadas por la
  configuración y, si ninguna produce una continuación válida, selecciona una acción
  segura sin inventar contenido (reconocer la imposibilidad, pedir aclaración cuando
  proceda, cambiar de tema autorizado mediante `ask`, o finalizar de forma controlada)
  — mismo mecanismo de degradación controlada ya establecido en las Features 001 y 003
  (ver FR-037).

### Session 2026-10-16 — cierre W0 de arquitectura y seguridad

- Toda salida textual visible de la defensa, incluidas preguntas iniciales, repreguntas,
  aclaraciones, avisos por falta de evidencia, degradaciones y cierre, se somete a la
  puerta final estructurada de Feature 001 con una instantánea mínima y confiable de la
  política aplicable y una plantilla catalogada vinculada de forma verificable.
- Un bloqueo nunca publica el candidato. Solo puede intentarse una vez un mensaje
  operativo predefinido y ese intento se verifica de forma independiente; si tampoco se
  autoriza, el turno termina en seguro sin texto visible.
- El cierre de sesión usa una única transición ganadora. Resumen, consentimiento,
  retención o eliminación, eventos de cierre y liberación de recursos solo se ejecutan
  cuando esa transición gana.
- STT y TTS locales son operaciones bloqueantes ejecutadas fuera del bucle asíncrono con
  capacidad global acotada, espera cancelable y descarte de resultados tardíos.
- Cada audio de entrada se limita a 10 MiB y 300 segundos. Cualquier almacenamiento
  temporal creado por la recepción multipart se cierra y elimina de forma verificable
  antes de responder; nunca se incorpora a persistencia, trazas o referencias.
- La voz de salida se genera bajo demanda a partir del texto final aprobado y persistido.
  Repetir la reproducción vuelve a sintetizar ese mismo texto; no conserva audio.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Realizar una defensa completa por texto (Priority: P1) 🎯 MVP

Un estudiante inicia una sesión de defensa oral de una actividad autorizada, conoce su
propósito, sus límites y el tratamiento del audio antes de responder. Recibe una
pregunta inicial, responde por texto, el sistema analiza los conceptos mencionados,
recupera materiales relacionados, propone una repregunta fundamentada, y el ciclo se
repite hasta el límite configurado o hasta que el estudiante finaliza voluntariamente,
tras lo cual puede revisar la transcripción completa y recibe un resumen descriptivo.

**Why this priority**: Es el flujo extremo a extremo que demuestra el valor central de
la agencia de defensa oral (Escenario A del documento fuente) y constituye su MVP mínimo
demostrable — la modalidad textual MUST cubrir el 100% del flujo por sí sola, sin
depender de voz.

**Independent Test**: Puede probarse de forma independiente con una actividad de defensa
oral ya configurada (pregunta inicial y materiales autorizados), completando una sesión
íntegramente por texto y verificando que se reciben repreguntas fundamentadas y un
resumen descriptivo al cierre.

**Acceptance Scenarios**:

1. **Given** una actividad de defensa oral autorizada, **When** el estudiante la inicia,
   **Then** el sistema le informa de su propósito, sus límites y el tratamiento del
   audio antes de aceptar su primera respuesta.
2. **Given** la sesión iniciada, **When** el sistema presenta la pregunta inicial,
   **Then** la pregunta procede de un banco autorizado por el profesorado o se genera a
   partir de los materiales de la actividad.
3. **Given** una respuesta del estudiante por texto, **When** el sistema la procesa,
   **Then** analiza los conceptos mencionados como observaciones del estado de la
   sesión (nunca como evaluación), recupera materiales relacionados, y propone una
   repregunta que pide justificación, un ejemplo, una comparación, una decisión técnica,
   la explicación de un error o una profundización.
4. **Given** cualquier repregunta o afirmación generada, **When** se procesa, **Then**
   pasa por verificación de alcance (materiales autorizados de la actividad), coherencia
   conversacional y conformidad constitucional antes de mostrarse.
5. **Given** el ciclo de pregunta/respuesta en curso, **When** el sistema decide el
   siguiente paso, **Then** puede profundizar, cambiar de tema, pedir aclaración o
   finalizar, y esa decisión queda registrada de forma trazable.
6. **Given** el límite configurado de turnos o duración, o una finalización voluntaria,
   **When** se alcanza, **Then** el sistema avisa al estudiante, permite un cierre
   ordenado, permite revisar la transcripción completa, y entrega un resumen
   descriptivo.

---

### User Story 2 - Nunca recibir una evaluación académica (Priority: P1)

En cualquier momento de la sesión, si una propuesta generada contuviera una nota, una
clasificación de desempeño o una afirmación de que el estudiante ha aprobado o
suspendido, el sistema la bloquea antes de mostrarla y la sustituye por una formulación
descriptiva permitida.

**Why this priority**: Es la garantía constitucional central de esta feature (Escenario
E del documento fuente; Principio I) — tan crítica como el propio flujo de la User Story
1, porque una defensa oral sin esta garantía sería indistinguible de una evaluación
automática no autorizada.

**Independent Test**: Puede probarse de forma independiente forzando una propuesta de
prueba que contenga contenido evaluativo (nota, clasificación de desempeño, afirmación
de aprobado/suspenso) y verificando que se bloquea y se sustituye antes de llegar al
estudiante.

**Acceptance Scenarios**:

1. **Given** una propuesta de repregunta o de resumen que contiene una nota o
   clasificación de desempeño, **When** el control constitucional la evalúa, **Then** la
   bloquea y la sustituye por una formulación descriptiva permitida, sin interrumpir la
   sesión.
2. **Given** el resumen descriptivo de cierre, **When** se genera, **Then** describe
   incidencias como hechos observables del sistema (tipo, acción de recuperación), nunca
   como una caracterización de la comprensión, el esfuerzo o la capacidad del
   estudiante.

---

### User Story 3 - Responder por voz con transcripción local corregible (Priority: P2)

El estudiante activa la modalidad de voz en una actividad que la permite, responde
oralmente, el sistema transcribe localmente y muestra el texto resultante, y el
estudiante puede corregir segmentos dudosos antes de que se usen para generar la
siguiente repregunta. El audio se descarta tras procesarse.

**Why this priority**: Es la capacidad diferencial de esta feature frente al autoestudio
puramente textual (Feature 003); depende de que el flujo textual base (User Story 1) ya
funcione, ya que la voz es una modalidad opcional que se apoya en el mismo ciclo de
turno.

**Independent Test**: Puede probarse de forma independiente en una actividad con entrada
por voz habilitada, respondiendo oralmente, corrigiendo la transcripción mostrada, y
verificando que la repregunta siguiente refleja la versión corregida, no la original.

**Acceptance Scenarios**:

1. **Given** una actividad con entrada por voz habilitada, **When** el estudiante
   responde oralmente, **Then** el sistema transcribe localmente y muestra el texto
   resultante, con marcas temporales cuando estén disponibles, una confianza estimada, y
   los segmentos de baja confianza señalados visiblemente.
2. **Given** una transcripción mostrada, **When** el estudiante corrige uno o más
   segmentos, **Then** el sistema conserva tanto la versión original como la corregida
   (cuando la sesión se conserva), y usa la versión corregida para generar la siguiente
   repregunta.
3. **Given** una sesión con voz activada, **When** la sesión termina, **Then** el audio
   capturado ya ha sido descartado y no se conserva por defecto.
4. **Given** síntesis de voz activada, **When** el sistema presenta una pregunta o
   repregunta, **Then** la voz reproduce exactamente el texto ya verificado, sin
   resumirlo, ampliarlo ni suavizarlo.

---

### User Story 4 - Continuar por texto cuando falla la voz (Priority: P2)

La captura de audio o la transcripción fallan, o los recursos locales no son
suficientes. El sistema informa con claridad, conserva el estado alcanzado en la sesión,
y ofrece continuar por texto sin interrupción.

**Why this priority**: Es la aplicación directa, al contexto de la defensa oral, del
mecanismo de degradación controlada ya establecido en la Feature 001 (Principio IX);
depende de que exista ya una sesión de voz en curso (User Story 3).

**Independent Test**: Puede probarse de forma independiente forzando un fallo simulado
de captura o transcripción durante una sesión de voz y verificando que la sesión
continúa por texto sin perder el estado ya alcanzado.

**Acceptance Scenarios**:

1. **Given** una sesión con voz activada, **When** la captura o la transcripción fallan,
   **Then** el sistema informa al estudiante con un mensaje claro y ofrece continuar por
   texto.
2. **Given** la degradación a texto, **When** el estudiante continúa, **Then** el estado
   de la sesión (turnos ya completados, conceptos tratados, historial) permanece
   intacto.
3. **Given** la síntesis de voz activada, **When** falla al reproducir una salida,
   **Then** la respuesta en texto sigue disponible y el turno no se interrumpe.

---

### User Story 5 - Pedir aclaración ante una transcripción ambigua (Priority: P2)

La respuesta transcrita está incompleta o tiene baja confianza en un término crítico. En
vez de generar una repregunta basada en una interpretación incierta, el sistema solicita
confirmación o aclaración al estudiante.

**Why this priority**: Evita que una repregunta se construya sobre una base
malinterpretada, protegiendo la fiabilidad conversacional; depende de que exista ya
transcripción de voz (User Story 3).

**Independent Test**: Puede probarse de forma independiente con una transcripción de
prueba marcada con baja confianza en un término crítico y verificando que el sistema
pide aclaración antes de proponer una repregunta.

**Acceptance Scenarios**:

1. **Given** una transcripción incompleta o con baja confianza en un término crítico,
   **When** el sistema la procesa, **Then** solicita confirmación o aclaración al
   estudiante en vez de generar una repregunta basada en esa interpretación — el
   sistema MUST NOT ofrecer repetir la grabación de audio; MUST ofrecer corregir el
   texto señalado y, si el estudiante lo prefiere, continuar respondiendo por texto.
2. **Given** la aclaración proporcionada por el estudiante, **When** se recibe, **Then**
   el sistema continúa el ciclo normal de repregunta con la información confirmada.
3. **Given** una respuesta de texto breve o poco desarrollada sin ninguna transcripción
   de por medio, **When** el sistema la procesa, **Then** MUST NOT solicitar aclaración
   solo por su brevedad — la trata como una respuesta válida sobre la que generar una
   repregunta normal (la solicitud de aclaración de esta User Story se limita a una
   transcripción de voz señalada como incompleta o de baja confianza).

---

### User Story 6 - Repreguntas relevantes y no repetitivas (Priority: P2)

Cada repregunta generada se basa en la respuesta del estudiante, el objetivo de la
actividad, los conceptos ya tratados, los materiales autorizados y el historial de la
sesión actual — nunca en una pregunta genérica desconectada, repetida literalmente, sin
respaldo en materiales, o que implique una calificación encubierta.

**Why this priority**: Es lo que hace pedagógicamente útil el ciclo de repreguntas más
allá de una sola interacción; depende de que exista ya un primer intercambio
pregunta-respuesta (User Story 1).

**Independent Test**: Puede probarse de forma independiente completando varios turnos de
defensa sobre el mismo tema y verificando, mediante la traza, que cada repregunta
referencia la respuesta previa o un material autorizado, y que ninguna repite
literalmente una repregunta ya formulada en la misma sesión.

**Acceptance Scenarios**:

1. **Given** una respuesta del estudiante, **When** el sistema genera la siguiente
   repregunta, **Then** esa repregunta referencia de forma trazable la respuesta del
   estudiante, un concepto ya tratado, o un material autorizado.
2. **Given** el historial de repreguntas ya formuladas en la sesión, **When** se genera
   una nueva, **Then** el sistema evita repetirla literalmente o formular una pregunta
   sin relación con la respuesta o los materiales.

---

### User Story 7 - Cerrar la sesión con consentimiento sobre la conservación (Priority: P3)

Al finalizar la sesión (por límite alcanzado o decisión voluntaria), el estudiante
revisa la transcripción final y decide si conserva o elimina los datos de la sesión
conforme a la política de conservación configurada por la actividad; el sistema ejecuta
esa decisión y registra únicamente lo permitido.

**Why this priority**: Cierra el ciclo de privacidad de la sesión; es de baja frecuencia
frente a una sesión ya en curso y depende de que la sesión haya avanzado lo suficiente
para tener contenido que revisar (User Story 1).

**Independent Test**: Puede probarse de forma independiente configurando una actividad
que permita elegir conservar o eliminar la sesión al cierre, completando una sesión
corta, y verificando que la decisión del estudiante se ejecuta y se registra
correctamente.

**Acceptance Scenarios**:

1. **Given** el cierre de una sesión, **When** el estudiante revisa la transcripción
   final, **Then** puede decidir conservar o eliminar los datos de la sesión conforme a
   la política de conservación configurada.
2. **Given** la decisión del estudiante, **When** se registra, **Then** el sistema
   ejecuta exactamente esa decisión y solo conserva lo explícitamente permitido por la
   configuración y el consentimiento.

---

### Edge Cases

- ¿Qué ocurre si el estudiante solicita activar voz en una actividad que solo permite
  texto? El sistema MUST mantener la sesión en modalidad textual y explicar que la voz
  no está disponible para esa actividad.
- ¿Qué ocurre si una actividad de defensa oral se configura sin ninguna pregunta inicial
  autorizada ni materiales desde los que generarla? El sistema MUST rechazar esa
  configuración antes de permitir iniciar cualquier sesión sobre ella.
- ¿Qué ocurre si la comprobación de no-evaluación (User Story 2) bloquea también la
  alternativa de reserva? El sistema MUST optar por una formulación mínima y
  genéricamente segura en vez de arriesgar una salida evaluativa, siguiendo el mismo
  principio de degradación segura ya aplicado en las Features 001 y 003.
- ¿Qué ocurre si un agente no esencial (por ejemplo, síntesis de voz) falla a mitad de
  turno mientras el resto de la agencia funciona con normalidad? El sistema MUST
  degradar ese componente sin interrumpir el resto de la sesión, siguiendo el mecanismo
  de degradación controlada ya establecido en la Feature 001.
- ¿Qué ocurre si el estudiante corrige la transcripción después de que ya se haya
  generado una repregunta sobre la versión original? La corrección MUST aplicarse a
  partir de ese punto en adelante; no reescribe retroactivamente una repregunta ya
  mostrada.
- ¿Qué ocurre si la transcripción de una grabación falla por un error técnico (no por
  baja confianza)? El sistema MUST descartar el audio de inmediato, sin reintentarlo
  sobre el mismo audio, y MUST degradar a texto en ese mismo turno (ver FR-011a,
  Clarifications).
- ¿Qué ocurre si el estudiante pide un tema fuera del alcance autorizado de la
  actividad? El sistema MUST rechazar o redirigir la petición, siguiendo el mismo
  aislamiento de autorización ya establecido en la Feature 002 y reutilizado en la
  Feature 003.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema MUST ofrecer un simulador de defensa oral construido
  reutilizando los mismos agentes, contratos, estado cognitivo, verificadores y
  mecanismos de trazabilidad ya utilizados por la agencia de autoestudio (Feature 003) —
  MUST NOT introducir una arquitectura paralela a `SelfStudyAgency`, ni duplicar un
  agente cuando el ya existente pueda reutilizarse.
- **FR-002**: Cada actividad de defensa oral MUST tener una configuración propia,
  versionada e inmutable una vez utilizada por una sesión, que defina como mínimo: banco
  de preguntas iniciales autorizadas y/o materiales desde los que generarlas, temas,
  materiales autorizados, dificultad orientativa, número máximo de turnos, duración
  máxima, idioma, si la entrada acepta texto y/o voz, si la salida ofrece texto y/o voz,
  si se permite conocimiento general, la política de conservación de la transcripción, y
  qué agentes son obligatorios u opcionales.
- **FR-002a**: Una configuración de actividad de defensa oral sin ninguna pregunta
  inicial autorizada ni materiales desde los que generarla MUST considerarse inválida y
  MUST rechazarse antes de permitir el inicio de cualquier sesión sobre esa actividad.
- **FR-003**: La modalidad textual (entrada y salida) MUST estar siempre disponible y
  MUST cubrir el 100% del flujo de la defensa oral, independientemente de si la voz está
  habilitada para la actividad.
- **FR-004**: El sistema MUST informar al estudiante del propósito de la sesión, sus
  límites, el tratamiento del audio y la política de conservación antes de aceptar su
  primera respuesta.
- **FR-005**: El sistema MUST presentar cada pregunta o repregunta por texto y, si la
  síntesis de voz está activa para la actividad, también mediante voz.
- **FR-006**: El sistema MUST aceptar la respuesta del participante por texto o, cuando
  la actividad lo permita, mediante captura de voz.
- **FR-007**: Cuando la respuesta se capture por voz, el sistema MUST transcribirla
  localmente y MUST mostrar el texto resultante al participante antes de continuar.
- **FR-008**: La transcripción MUST incluir el texto reconocido, marcas temporales
  cuando estén disponibles, una confianza estimada, y una señalización visible de los
  segmentos de baja confianza.
- **FR-009**: El participante MUST poder corregir segmentos de la transcripción antes de
  que esta se utilice para generar la siguiente repregunta.
- **FR-010**: Cuando la sesión se conserve, el sistema MUST conservar tanto la
  transcripción original como su corrección, sin que la corrección sustituya o elimine
  la original.
- **FR-011**: El audio capturado MUST ser efímero y MUST descartarse inmediatamente
  después de procesarse. Esta feature MUST NOT persistirlo, conservarlo, incluirlo en
  trazas ni crear referencias recuperables a él bajo ninguna configuración. Cualquier
  recurso temporal usado por el transporte de entrada MUST cerrarse y eliminarse antes
  de completar la respuesta.
- **FR-011a**: Si la transcripción de una grabación falla por un error técnico (no por
  baja confianza), el audio MUST descartarse de inmediato, sin ningún reintento sobre
  ese mismo audio; el sistema degrada a texto en el mismo turno (ver FR-021, ver
  Clarifications).
- **FR-012**: El sistema MUST analizar los conceptos mencionados en cada respuesta como
  observaciones e hipótesis del estado cognitivo de la sesión — MUST NOT tratarlos ni
  registrarlos como una evaluación o un juicio de calidad de la respuesta.
- **FR-013**: El sistema MUST recuperar materiales relacionados con la respuesta del
  participante, reutilizando el mecanismo de recuperación documental ya definido en la
  Feature 002 sin modificar su contrato.
- **FR-014**: El sistema MUST generar una repregunta que solicite, según corresponda,
  justificación, un ejemplo, una comparación, una decisión técnica, la explicación de un
  error, o una profundización sobre la respuesta del participante.
- **FR-015**: Cada repregunta generada MUST derivarse de la respuesta del participante,
  el objetivo de la actividad, los conceptos ya tratados, los materiales autorizados y
  el historial de la sesión actual — MUST evitar preguntas irrelevantes, repetidas
  literalmente, sin respaldo en materiales o en la respuesta, o que impliquen una
  calificación encubierta.
- **FR-016**: Toda repregunta o afirmación generada MUST pasar por verificación de
  alcance (materiales autorizados de la actividad), coherencia conversacional y
  conformidad constitucional antes de mostrarse al participante, reutilizando los
  verificadores ya existentes en las Features 002 y 003 sin modificar sus contratos.
- **FR-017**: Los controles marcados como no omitibles (constitucional y de seguridad)
  MUST ejecutarse en todos los turnos de una sesión de defensa oral, independientemente
  de la modalidad de entrada/salida o del resultado de otros agentes.
- **FR-018**: Tras cada respuesta, el sistema MUST decidir si profundiza en el mismo
  tema, cambia a un tema distinto, pide aclaración o finaliza la sesión, y esa decisión
  MUST quedar registrada de forma trazable.
- **FR-018a**: Profundizar en el mismo tema y cambiar a un tema distinto MUST expresarse
  ambos mediante la misma acción de diálogo ya existente (presentar una nueva
  pregunta/repregunta) — esta feature MUST NOT introducir una acción de diálogo nueva
  y distinta para "cambiar de tema"; la diferencia entre ambos MUST seguir siendo
  observable en la traza a través de los conceptos y materiales referenciados por la
  repregunta (ver Clarifications).
- **FR-018b**: La agencia de defensa MUST seleccionar la acción de aclaración
  (`clarify`) cuando la respuesta textual definitiva del participante (ya confirmada,
  tras cualquier corrección de transcripción cuando proceda) no proporcione información
  suficiente o inequívoca para decidir con seguridad el siguiente paso del diálogo —
  por ejemplo, cuando no pueda relacionarse razonablemente con la pregunta o los
  conceptos autorizados relevantes, cuando admita varias interpretaciones plausibles
  que conducirían a continuaciones distintas, o cuando contenga una aparente
  incompatibilidad interna sobre la que sea necesario conocer qué interpretación
  pretendía expresar el participante. Esta decisión MUST tomarse exclusivamente sobre
  la respuesta textual ya definitiva — MUST NOT confundirse ni compartir mecanismo con
  la solicitud de confirmación/corrección por baja confianza de transcripción
  (FR-022), que es una incidencia de modalidad previa a cualquier procesamiento
  cognitivo. Al seleccionar `clarify`, el sistema MUST solicitar únicamente la
  información mínima necesaria para desambiguar, MUST NOT evaluar ni corregir
  académicamente al participante, MUST NOT interpretar la necesidad de aclaración como
  un error o una señal de bajo rendimiento, MUST registrar la decisión y su motivo
  estructurado de forma trazable, y tras recibir la aclaración MUST volver a decidir la
  acción de diálogo correspondiente con la información ya desambiguada.
- **FR-019**: El ciclo de pregunta/repregunta MUST repetirse hasta alcanzar el límite
  configurado de turnos o duración, o hasta la finalización voluntaria del participante.
- **FR-020**: El participante MUST poder revisar la transcripción completa de la sesión
  antes de su cierre.
- **FR-021**: Si la captura de audio o la transcripción fallan, o los recursos locales
  no son suficientes, el sistema MUST ofrecer continuar por texto sin perder el estado
  ya alcanzado en la sesión, siguiendo el mismo mecanismo de degradación controlada ya
  establecido en la Feature 001.
- **FR-022**: Si la respuesta transcrita está incompleta o tiene baja confianza en un
  término crítico, el sistema MUST solicitar confirmación o aclaración al participante
  antes de generar una repregunta basada en esa interpretación. Esta solicitud de
  aclaración MUST ofrecer corregir el texto de los segmentos señalados y, si el
  participante lo prefiere, continuar respondiendo por texto desde ese punto — MUST NOT
  ofrecer repetir la grabación de audio (ver Clarifications). Esta solicitud es una
  incidencia de modalidad, previa a cualquier procesamiento cognitivo de la respuesta, y
  MUST distinguirse por completo de la acción de diálogo de aclaración cognitiva sobre
  una respuesta ya definitiva (ver FR-018b).
- **FR-022a**: Una respuesta capturada directamente como texto (sin transcripción de por
  medio) MUST NOT disparar por sí sola, solo por ser breve o poco desarrollada, la
  solicitud de aclaración de FR-022 — se trata como una respuesta válida sobre la que
  generar una repregunta normal (ver Clarifications).
- **FR-023**: Cuando la síntesis de voz esté activa, MUST reproducir exactamente el
  contenido textual ya verificado — MUST NOT resumirlo, ampliarlo, suavizarlo ni
  modificarlo de ninguna forma.
- **FR-024**: Si la síntesis de voz falla, la respuesta en texto MUST seguir disponible
  y el turno MUST NOT interrumpirse por ese fallo.
- **FR-025**: El sistema MUST NOT producir ni mostrar, en ningún momento de la sesión,
  una nota, calificación, clasificación de desempeño, o una afirmación de que el
  participante ha aprobado o suspendido.
- **FR-026**: Toda propuesta generada que contenga contenido evaluativo (nota,
  clasificación de desempeño, afirmación de aprobado/suspenso) MUST ser bloqueada por el
  control constitucional antes de mostrarse y su causa MUST quedar registrada sin
  revelar el contenido prohibido. El sistema MAY intentar como máximo una respuesta
  operativa segura predefinida, que solo podrá mostrarse si supera una verificación final
  independiente. Si tampoco se autoriza, MUST finalizar de forma segura sin presentar
  contenido.
- **FR-027**: Esta feature MUST NOT inferir ni almacenar un perfil de capacidad, nivel o
  desempeño del participante a partir de sus respuestas, correcciones de transcripción,
  o historial de la sesión. Esta prohibición incluye usar como señales académicas la
  duración, confianza STT, número de aclaraciones/repreguntas o incidencias técnicas;
  esos datos solo pueden describir hechos operativos de la sesión.
- **FR-028**: Al alcanzarse el límite de turnos o duración, o ante una finalización
  voluntaria, el sistema MUST avisar al participante y MUST permitir un cierre
  ordenado.
- **FR-029**: Al cerrar la sesión, el sistema MUST generar un resumen descriptivo,
  limitado exclusivamente a hechos observables y datos estructurados registrados
  durante la propia sesión — puede incluir preguntas formuladas, repreguntas,
  aclaraciones solicitadas, temas/conceptos tratados, materiales o fuentes consultados,
  incidencias técnicas, duración, número de turnos, y causa de cierre. El resumen MUST
  NOT incluir notas, calificaciones, puntuaciones, diagnóstico de nivel, personalidad,
  capacidad, rendimiento, competencia, dominio, ni recomendaciones académicas
  automatizadas, y MUST NOT introducir ninguna inferencia nueva sobre el participante
  más allá de esos hechos ya registrados durante la sesión. El resumen MUST ser
  reproducible mediante construcción determinista a partir de los datos estructurados de
  la sesión ya disponibles y MUST NOT invocar un generador de texto libre.
- **FR-029a**: Las incidencias, aclaraciones y repreguntas incluidas en el resumen de
  cierre MUST describirse como hechos observables del sistema y su desarrollo (tipo de
  incidencia o aclaración, acción de recuperación aplicada, tema o concepto al que se
  refiere la repregunta) — MUST NOT redactarse ni interpretarse como una caracterización
  de la comprensión, el esfuerzo, el rendimiento o la capacidad del participante, mismo
  estándar ya exigido en la Feature 003.
- **FR-030**: Al cierre, el participante MUST poder decidir si conserva o elimina los
  datos de la sesión conforme a la política de conservación configurada por la
  actividad; el sistema MUST ejecutar esa decisión y MUST registrar únicamente lo
  explícitamente permitido. La persistencia operativa durante una sesión MUST NOT
  interpretarse como consentimiento de conservación ni la decisión de conservación como
  condición para participar o completar la defensa. Cuando la actividad autoriza
  conservar, el participante puede elegir de forma independiente transcripción y resumen;
  el audio nunca forma parte de esa elección.
- **FR-031**: La conservación de transcripción, corrección o resumen más allá del cierre
  MUST sujetarse a la misma política de retención y consentimiento ya definida por el
  sistema (`RetentionPolicy`, Feature 001), con un periodo de retención finito y
  configurable como parte de esa configuración — esta feature MUST NOT introducir un
  sistema de retención paralelo ni fijar un número de días por defecto no definido ya en
  la constitución o en los requisitos existentes. La eliminación elegida o exigida por
  falta de autorización MUST aplicarse en el cierre; la purga diferida MUST limitarse a
  datos expirados propios de esta feature y MUST NOT afectar las Features 001–003.
- **FR-032**: El sistema MUST NOT agregar, correlacionar ni construir un perfil a partir
  de información de defensa oral (respuestas, transcripciones, repreguntas, incidencias,
  resúmenes) entre distintas sesiones del mismo `participant_code` — toda esa
  información MUST permanecer acotada a la sesión que la generó, mismo principio ya
  aplicado en la Feature 003.
- **FR-033**: Esta feature MUST preservar el comportamiento ya validado de las
  Features 001 (núcleo cognitivo, contratos de agente, ciclo de sesión/turno, control
  constitucional, versionado del estado cognitivo), 002 (materiales, recuperación,
  fundamentación) ni 003 (agencia de autoestudio, generación, verificadores de
  coherencia y no-revelación). MUST integrar sus contratos públicos estables y MAY
  realizar extensiones aditivas necesarias para registrar la nueva agencia, rutas,
  propósitos, plantillas y clientes, siempre que las pruebas de regresión demuestren que
  no se debilita ningún comportamiento anterior.
- **FR-034**: Esta feature MUST NOT incluir análisis de prosodia, emociones o lenguaje
  corporal, evaluación automática de la calidad de la defensa, detección de fraude,
  robot o avatar físico, videoconferencia, ni memoria longitudinal entre sesiones.
- **FR-035**: La interfaz esencial de la sesión MUST ser operable mediante teclado, MUST
  permitir pausar la sesión, repetir la pregunta actual, ajustar el ritmo, y MUST
  mostrar mensajes de error comprensibles — sin depender del audio, del color, ni de
  gestos no accesibles.
- **FR-036**: Esta feature MUST NOT requerir un servicio en la nube para su
  funcionamiento esencial — la transcripción local y la síntesis de voz, cuando se
  utilicen, MUST ejecutarse localmente, consistente con la ejecución local ya exigida en
  la Feature 001.
- **FR-037**: Si el mecanismo de generación de la pregunta inicial o de una repregunta
  falla o no está disponible, ese fallo MUST NOT provocar por sí solo la pérdida de la
  sesión. El sistema MUST intentar las alternativas de generación autorizadas por la
  configuración de la actividad; cuando exista una pregunta autorizada/preconfigurada o
  una alternativa determinista válida, MUST poder utilizarla. Si, tras agotar esas
  alternativas, no puede obtenerse una pregunta, repregunta o salida válida, el sistema
  MUST seleccionar una acción segura que no invente contenido — reconocer la
  imposibilidad de continuar sobre el tema actual, solicitar aclaración cuando proceda,
  pasar mediante la acción `ask` a otro tema autorizado, o finalizar la sesión de forma
  controlada — MUST NOT fabricar una repregunta sin evidencia o contexto suficiente
  únicamente para mantener la conversación. El fallo detectado y la acción de
  recuperación seleccionada MUST quedar registrados de forma trazable. Este requisito
  cubre tanto la pregunta inicial como las repreguntas, reutilizando el mismo mecanismo
  de degradación controlada ya establecido en la Feature 001 y aplicado en la
  Feature 003, sin introducir un mecanismo de reserva adicional.
- **FR-038**: Antes de persistir o presentar cualquier texto generado por esta feature,
  el sistema MUST autorizar el candidato final mediante la puerta estructurada ya
  establecida en la Feature 001. La autorización MUST usar una instantánea mínima,
  confiable y filtrada de la política aplicable, la identidad exacta de una plantilla o
  mensaje operativo catalogado y una vinculación verificable que cubra el contenido
  completo. Esta regla MUST aplicarse a la ruta normal y a todas las rutas de
  degradación, aclaración, falta de evidencia y cierre.
- **FR-039**: Cuando la autorización final bloquea un candidato, el sistema MUST
  persistir el turno como bloqueado con `output_text` ausente, MUST NOT transportar ni
  publicar el candidato y MUST NOT sintetizarlo. Solo se permite el intento operativo
  único descrito en FR-026; si ese intento se bloquea, la sesión MUST cerrarse en estado
  seguro y sin una tercera salida.
- **FR-040**: La síntesis de voz MUST ejecutarse únicamente sobre el texto final aprobado
  y ya persistido del turno. La reproducción y su repetición MUST obtener audio bajo
  demanda para esa misma identidad de turno y texto; el sistema MUST NOT persistir los
  bytes de audio ni sintetizar propuestas previas, bloqueadas o con texto ausente.
- **FR-041**: Todo cierre de defensa MUST usar la transición atómica de cierre ya
  establecida por la Feature 001. Solo la ejecución que gana esa transición MUST generar
  y entregar el resumen, registrar consentimiento, aplicar conservación o eliminación,
  emitir eventos de cierre y liberar recursos. Las ejecuciones concurrentes o repetidas
  MUST devolver el estado persistido sin repetir esos efectos.
- **FR-042**: La transcripción y la síntesis locales MUST ejecutarse con capacidad global
  explícitamente acotada, admisión con backpressure, plazo y cancelación. Un trabajo que
  termina después de cancelarse o expirar MUST descartarse y MUST NOT escribir datos,
  trazas ni respuestas tardías.
- **FR-043**: Cada audio de entrada MUST rechazarse antes de transcribir si supera 10 MiB
  y MUST rechazarse tras inspección si supera 300 segundos, si su duración no puede
  determinarse o si su formato no es admitido. La recepción MUST contabilizar bytes de
  forma acotada y garantizar el cierre y eliminación de cualquier recurso temporal del
  transporte multipart tanto en éxito como en error, timeout o cancelación.
- **FR-044**: La interfaz MUST distinguir de forma observable una salida textual
  aprobada de un turno bloqueado sin texto. Solo el primer caso MAY ofrecer reproducción
  de voz; un fallo de síntesis MUST dejar disponible el texto aprobado y permitir un
  nuevo intento explícito de reproducción sin repetir el turno cognitivo.

### Key Entities

- **DefenseActivityConfig**: configuración propia de una actividad de defensa oral
  (banco de preguntas/materiales de origen, temas, dificultad orientativa, límites de
  turnos/duración, idioma, modalidades de entrada/salida, conocimiento general
  permitido, política de conservación de transcripción, agentes obligatorios/opcionales)
  — versionada e inmutable una vez utilizada, mismo patrón que `SelfStudyActivityConfig`
  (Feature 003).
- **Transcript**: texto producido por la transcripción local de una respuesta de voz,
  con segmentos, confianza estimada y marcas temporales opcionales (ya anticipado en
  `docs/ORAL-IA_SpecKit/14_domain_model.md`).
- **TranscriptCorrection**: versión de un `Transcript` corregida por el participante; no
  elimina el original cuando la sesión se conserva (ya anticipado en
  `14_domain_model.md`).
- **Repregunta** (registro de pregunta de seguimiento): pregunta generada a partir de la
  respuesta del participante, el objetivo, los conceptos tratados, los materiales y el
  historial de la sesión actual — con su tipo (justificación, ejemplo, comparación,
  decisión técnica, explicación de error, profundización) y su referencia trazable a la
  respuesta o material que la motivó.
- **DefenseSessionSummary**: resumen descriptivo de una sesión de defensa oral (temas,
  preguntas y repreguntas, conceptos mencionados, materiales consultados, incidencias),
  visible para el propio estudiante cuando la actividad lo autoriza — mismo patrón que
  `StudySessionSummary` (Feature 003), distinto del resumen técnico interno de la
  Feature 001.
- **ConsentRecord**: decisión versionada del participante, al cierre de la sesión, sobre
  conservar o eliminar sus datos conforme a la política de conservación configurada (ya
  anticipado en `14_domain_model.md`).

*(Session, Turn, CognitiveState, Agent, Agency, AgentContract, StatePatch y TraceEvent se
reutilizan tal como quedaron definidos en la Feature 001. MaterialDocument,
MaterialFragment, Evidence y el agente de recuperación se reutilizan tal como quedaron
definidos en la Feature 002. `GenerationPort` (y sus dos adaptadores),
`GroundingVerifierAgent`, `CoherenceVerifierAgent`, `ConstitutionalControl` y el
mecanismo de degradación controlada se reutilizan tal como quedaron definidos en la
Feature 003. Sus contratos públicos se preservan; las extensiones aditivas documentadas y probadas se rigen por FR-033 — ver Assumptions.)*

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El mismo núcleo cognitivo y el mismo conjunto mínimo de agentes básicos
  soportan autoestudio (Feature 003) y defensa oral en las pruebas preparadas para esta
  feature, sin que se detecte una arquitectura o una implementación de agentes
  duplicada — verificado mediante las decisiones estructuradas de la agencia y la traza
  registrada, nunca mediante comparación literal de texto generado.
- **SC-002**: El 100% del flujo esencial (pregunta, respuesta, repregunta, revisión de
  transcripción, cierre y resumen) es completable únicamente por texto en el conjunto de
  pruebas preparado para esta feature.
- **SC-003**: El 100% de las correcciones de transcripción en las pruebas quedan
  conservadas junto con la versión original, y la repregunta generada tras una
  corrección se basa verificablemente en la versión corregida.
- **SC-004**: El 100% de los fallos de captura o transcripción de voz simulados en las
  pruebas degradan la sesión a modalidad textual sin pérdida del estado ya alcanzado.
- **SC-005**: El 100% de las repreguntas generadas en el conjunto de pruebas referencian
  de forma trazable la respuesta del participante, un concepto ya tratado o un material
  autorizado — ninguna repregunta de prueba resulta genérica, desconectada, o repetida
  literalmente dentro de la misma sesión.
- **SC-006**: El 100% de las propuestas de prueba que contienen contenido evaluativo
  (nota, clasificación de desempeño, afirmación de aprobado/suspenso) quedan bloqueadas
  antes de mostrarse al estudiante.
- **SC-007**: El 100% de las sesiones de prueba que alcanzan su límite de turnos o
  duración, o que finalizan voluntariamente, terminan de forma controlada, generan un
  resumen descriptivo, y producen una traza completa reconstruible.
- **SC-008**: En la matriz de salidas visibles, el 100% de los candidatos aprobados
  conserva propuesta y verificación vinculadas, y el 100% de los bloqueados persiste
  `output_text` ausente sin filtrar el candidato por API, transporte, traza o TTS.
- **SC-009**: Las pruebas de concurrencia de cierre demuestran un único ganador y una
  única ejecución de resumen, consentimiento, retención/eliminación, evento de cierre y
  liberación de recursos.
- **SC-010**: Las pruebas de audio fuerzan límites de bytes, duración, timeout,
  cancelación y rollover multipart, y verifican que no queda ningún archivo temporal ni
  escritura tardía después de responder.
- **SC-011**: Para un mismo texto definitivo y la misma configuración, las pruebas por
  entrada textual y por voz confirmada producen la misma estructura de acción de diálogo
  y conceptos referenciados, con independencia de la modalidad de origen.

## Assumptions

- El comportamiento ya validado de las Features 001 (núcleo cognitivo), 002 (materiales
  y RAG) y 003 (agencia de autoestudio) permanece compatible; esta feature compone sus
  contratos estables y añade únicamente integración explícita. Las extensiones aditivas
  se validan con las regresiones históricas (FR-033).
- **Capacidades de las Features 001–003 que esta feature MUST reutilizar sin debilitar**:
  ciclo de sesión/turno, `CognitiveState`/`StatePatch` versionado, `ConstitutionalControl`,
  `SafeFallbackAgent`, `execute_agency`/`run_with_deadline` y el resto del mecanismo de
  degradación controlada, `RetentionPolicy`, `TraceEvent`/trazabilidad (Feature 001);
  `MaterialRetrieverAgent` y el aislamiento de autorización documental
  (Feature 002); `GenerationPort` con sus dos adaptadores (`OllamaGenerationAdapter` /
  `DeterministicGenerationAdapter`), `GroundingVerifierAgent`, `CoherenceVerifierAgent`,
  el patrón de interpretación de intención con hipótesis y confianza, y el conjunto de
  acciones de `DialogueAction` ya existente (`ask`/`clarify`/`acknowledge_missing_info`/
  `finish`, entre otras) — esta feature MUST NOT añadir una acción nueva para "cambiar
  de tema" cuando `ask` ya expresa correctamente ese comportamiento (ver Clarifications,
  FR-018a) (Feature 003).
- **Capacidades genuinamente nuevas de esta feature**: un adaptador de transcripción
  local (voz → texto) y uno de síntesis de voz (texto → voz), cada uno tratado como
  sujeto a la misma degradación controlada ya exigida para la generación de texto; un
  agente de repreguntas (puede reutilizar el generador de respuestas existente con un
  propósito nuevo, o requerir un agente propio — decisión de planificación técnica, no
  de esta especificación); persistencia de `Transcript`/`TranscriptCorrection`;
  `DefenseActivityConfig`; `DefenseSessionSummary`; y el registro de consentimiento de
  cierre.
- La revisión de la transcripción por el estudiante (User Story 3) se implementa como un
  paso de confirmación explícito antes de continuar (el estudiante ve el texto y puede
  editarlo antes de avanzar), no como una edición forzada de cada segmento; el detalle
  exacto de la interacción es una decisión de planificación técnica.
- La pregunta inicial de una sesión puede proceder de un banco definido por el
  profesorado o generarse a partir de los materiales autorizados de la actividad; ambos
  mecanismos son válidos y pueden coexistir en la misma configuración.
- Igual que en la Feature 003, por defecto los datos derivados de una sesión de defensa
  oral no se conservan de forma permanente; si una actividad autoriza conservarlos, esa
  persistencia se sujeta a la misma `RetentionPolicy` ya definida en la Feature 001, sin
  un número de días por defecto no definido ya en la constitución o los requisitos
  existentes.
- Preparación de una exposición y revisión de conceptos (modos de la Feature 003) no
  forman parte de esta feature — la defensa oral es un flujo propio con su propia
  configuración de actividad, aunque comparta agentes con el autoestudio.
- El "resumen de sesión" de esta feature (`DefenseSessionSummary`) es distinto y visible
  para el estudiante, siguiendo exactamente el mismo patrón ya establecido por
  `StudySessionSummary` en la Feature 003 (visualización única y efímera, entregada en
  la misma respuesta que cierra la sesión, sin vía de consulta posterior).
