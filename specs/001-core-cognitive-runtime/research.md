# Research: Núcleo cognitivo y ejecución local

**Input**: `spec.md`, `docs/ORAL-IA_SpecKit/11_plan_prompt.md`, `docs/ORAL-IA_SpecKit/14_domain_model.md`, `.specify/memory/constitution.md`

Este documento resuelve las incógnitas técnicas reales que quedaban abiertas después de la
especificación, acotadas al alcance de la Feature 001. No se investigan decisiones de
features posteriores (RAG, voz, evaluación).

## 1. Mecanismo de versionado y detección de conflictos del estado cognitivo

**Decision**: versionado optimista de dos capas: (a) un registro `CognitiveState` "actual"
por sesión con un contador de versión monotónico (`version: int`), y (b) un log
append-only `StatePatch` que registra cada intento de cambio (aplicado o rechazado) con su
`base_version` y `resulting_version`. Un patch solo se aplica si `base_version` coincide con
la versión vigente en el momento de la escritura (comparación y escritura atómica —
`UPDATE ... WHERE version = :base_version`); si no coincide, se persiste igualmente como
rechazado con la causa, sin sobrescribir el estado vigente.

**Rationale**: satisface a la vez FR-008/FR-019 (detección de conflicto sin sobrescritura
silenciosa) y FR-016/FR-020/SC-004 (reconstrucción completa), porque el log de patches ya
es el historial de trazabilidad — no hace falta un mecanismo distinto para reconstrucción y
otro para concurrencia. Coincide con la decisión ya fijada en
`10_clarification_decisions.md` ("versionado optimista o mecanismo equivalente").

**Alternatives considered**:
- Bloqueo pesimista por fila (`SELECT ... FOR UPDATE`): rechazado; añade contención
  innecesaria para el caso de uso real (una sola sesión interactiva activa, User Story 5
  cubre el caso raro de dos escrituras casi simultáneas dentro de esa sesión).
- Solo reconstrucción por reproducción de eventos, sin contador de versión: rechazado como
  único mecanismo porque complica la detección de conflicto en tiempo real (Principio XI:
  evitar complejidad no justificada); se conserva el log de eventos, pero se añade el
  contador para el chequeo optimista directo.

## 2. "Interpretación simulada o determinista" del turno (sin LLM real)

**Decision**: implementar un agente `Interpreter` con lógica determinista basada en reglas
(por ejemplo, heurística de palabras clave / patrón fijo de reconocimiento de intención),
detrás del mismo `AgentContract` que usará un intérprete real en features posteriores. No se
integra ningún modelo de lenguaje en esta feature.

**Rationale**: el alcance de la Feature 001 excluye explícitamente materiales docentes
reales y RAG; el contrato estable permite sustituir este agente por uno real sin tocar el
orquestador ni las agencias (Principio II, Principio XI — "componentes de inferencia deben
quedar detrás de interfaces reemplazables").

**Alternatives considered**:
- Conectar un LLM local (Ollama) desde ya: rechazado; añade una dependencia no justificada
  para esta feature y se sale del alcance declarado en `spec.md` ("Fuera de alcance").

## 3. Aplicación de la regla "una sesión interactiva activa por instancia"

**Decision**: un marcador persistido en SQLite (`active_session` con restricción de unicidad
a nivel de tabla, o una fila única con `session_id` referenciado) que se crea al iniciar una
sesión y se libera al cerrarla. El intento de iniciar una segunda sesión mientras el
marcador existe se rechaza a nivel de servicio de aplicación antes de tocar el dominio.

**Rationale**: persistir el marcador (en vez de mantenerlo solo en memoria) sobrevive a
reinicios del proceso dentro de la misma ejecución y es trivialmente extensible a "N
marcadores" si se amplía la concurrencia más adelante, sin rediseñar el mecanismo
(decisión ya fijada: "el diseño no debe impedir ampliar la concurrencia después").

**Alternatives considered**:
- Solo un `asyncio.Lock` en memoria: rechazado como mecanismo único porque no deja rastro
  trazable del rechazo (Principio VIII) y se pierde ante un reinicio a mitad de sesión.

## 4. Alcance del cliente web (frontend) para esta feature

**Decision**: una única aplicación React + TypeScript + Vite con dos áreas de rutas
(`/participante`, `/tecnica`), sin lógica cognitiva en el cliente; toda decisión pasa por la
API. El área técnica no queda protegida por credencial en esta feature (FR-021a: punto de
extensión presente pero deshabilitado).

**Rationale**: un único cliente simple es suficiente para ejercitar FR-021 y evita duplicar
infraestructura de frontend antes de que exista una necesidad demostrada (Principio XI).

**Alternatives considered**:
- Dos aplicaciones frontend separadas (participante / docente): rechazado por complejidad
  innecesaria en el MVP de esta feature.

## 5. Empaquetado del proyecto Python

**Decision**: un único proyecto Python 3.12 gestionado con `uv` en la raíz del repositorio
(`pyproject.toml`), paquete de dominio en `src/oralia/`, con `apps/api` como punto de entrada
fino (uvicorn) que importa `src/oralia`. Migraciones con Alembic apuntando a los modelos de
`infrastructure/db`.

**Rationale**: coincide con la pila propuesta en `11_plan_prompt.md` y evita la sobrecarga
de un monorepo multi-paquete que esta feature no necesita todavía.

## 6. Componentes de la pila propuesta que NO se adoptan en esta feature

**Decision**: se difieren explícitamente — ChromaDB / `VectorStore`, adaptadores de
embeddings, extracción documental (PDF/DOCX/PPTX), adaptadores de inferencia LLM
(Ollama/vLLM), Faster-Whisper y Piper (voz), Docker Compose. Ninguno de estos componentes
es necesario para satisfacer los requisitos funcionales de `spec.md`.

**Rationale**: Principio XI exige justificar toda dependencia nueva frente a la necesidad
real de la feature; estos componentes pertenecen a las Features 002 (materiales/RAG) y 004
(voz) del roadmap de la constitución. Añadirlos ahora violaría también la instrucción del
prompt de planificación de no implementar funcionalidades de features posteriores.

**Alternatives considered**: instalar las dependencias "por adelantado" sin usarlas —
rechazado; aumenta la superficie de mantenimiento y contradice Principio XI sin beneficio
medible en esta feature.

## 7. Pruebas frente a un LLM real ("no usar exclusivamente mocks del LLM")

**Decision**: esta directiva del prompt de planificación no aplica todavía a la Feature 001,
porque no existe ningún agente respaldado por un LLM real en su alcance (ver punto 2). Se
documenta la aplicabilidad diferida a partir de la Feature 002/003, cuando aparezcan
agentes de interpretación o generación reales.

**Rationale**: evita declarar cobertura de pruebas ficticia sobre un componente que no
existe todavía en esta feature; transparencia sobre el alcance real de las pruebas
(Principio X).

## 8. Refuerzo del control constitucional de bloqueo (FR-014) — implementado en la ronda de estabilización 3 (2026-09-11)

**Hallazgo de partida (auditoría previa, H02)**: `constitutional_control.py` clasifica
como `approved` frases como *"Tu nota es 9 sobre 10."* y *"Te otorgo un sobresaliente."*
porque su patrón `assigns_grade` exige que "nota"/"calificación"/"puntuación" preceda a un
dígito con solo espacio/`:`/`=` de por medio (ninguna palabra intermedia como "es"), y
ningún patrón cubre el vocabulario de calificación cualitativa ("sobresaliente",
"notable", "aprobado", "suspenso", "matrícula de honor", "apto/no apto") ni verbos de
otorgamiento ("otorgar", "conceder", "asignar") sin un dígito adyacente.

**Decision — tres reglas deterministas independientes, sin dependencias nuevas**
(Principio XI: sin LLM adicional, sin servicio externo, sin infraestructura nueva):

1. **Regla A — `assigns_grade`, anclada en el sustantivo de calificación**:
   `(nota|calificación|puntuación)` seguido, con hasta 4 palabras de relleno acotadas
   de por medio (nunca "cualquier distancia" — ver el porqué en L2/L3 más abajo), de un
   verbo copulativo (`es`/`será`/`queda en`) y un **valor**: un dígito, una palabra
   numeral cardinal simple (cero–diez, con o sin artículo "un/una" delante — cubre
   "Tu nota es un nueve."), una de las palabras de calificación cualitativa
   ("sobresaliente", "notable", "aprobado"/"aprobada", "suspenso"/"suspensa",
   "matrícula de honor", "apto"/"no apto", "excelente"), o una fracción "N/10". También
   cubre, sin cambios, la forma inmediata ya existente ("nota: 9", nota +
   `:`/`=` + dígito sin verbo intermedio).
2. **Regla B — `assigns_grade`, anclada en el verbo de otorgamiento**: un verbo de
   otorgamiento (`otorgo`/`otorga`/`concedo`/`concede`/`asigno`/`asigna`) seguido, con
   hasta 3 palabras de relleno, del mismo conjunto de valores que la Regla A — cubre
   *"Te otorgo un sobresaliente."* (P2), que no contiene "nota"/"calificación"/
   "puntuación" en absoluto y por tanto la Regla A no alcanza.
3. **Regla C — `assigns_score_fraction`, contextual, no un bloqueo incondicional de
   "N/10"**: una fracción "N/10" **únicamente** cuando aparece, con hasta 4 palabras de
   por medio en cualquiera de los dos sentidos, junto a un sustantivo de ítem evaluado
   ("práctica", "examen", "trabajo", "ejercicio", "tarea", "prueba") — cubre *"9/10 en
   la práctica 2."* (V2), que no contiene ningún disparador de las Reglas A/B. **Esta
   regla NO bloquea "N/10" por sí sola** (corrección respecto a un diseño intermedio
   descartado antes de implementarse: bloquear cualquier fracción "N/10" sin contexto
   habría bloqueado también "La probabilidad de este suceso es 9/10." y "La fracción
   9/10 equivale a 0,9." — ver matriz L6/L7 — que no son calificaciones).

**Por qué el acotamiento de palabras de relleno es necesario y suficiente**: permitir
"cualquier distancia" entre el disparador y el verbo copulativo convertiría el detector
en un bloqueo casi universal de la palabra "nota" en cualquier texto que, más adelante,
contuviera en cualquier punto posterior un verbo "es" seguido de un valor — exactamente
lo que la matriz (L1–L4) exige evitar. Acotar a un número fijo y pequeño de palabras
(4 para la Regla A/C, 3 para la Regla B) permite alcanzar construcciones reales con
preposiciones intermedias ("puntuación **en la práctica** es 9/10") sin degenerar en
ese bloqueo universal — verificado caso por caso en la matriz siguiente, no solo
argumentado.

**Tratamiento conservador ante verificación no concluyente**: este control sigue siendo,
por construcción, un detector de patrones conocidos (lista positiva de disparadores), no
un clasificador semántico. Su comportamiento ante un texto que no coincide con ninguna
regla sigue siendo `approved` — no se introduce un tercer veredicto ni un modo
"bloquear todo lo que mencione una nota".

**Matriz de aceptación (casos de control — no es una garantía semántica universal;
todos los casos se ejecutan contra el código real, `tests/contract/
test_verification_block.py`, no una copia de las expresiones regulares)**:

| # | Texto | Esperado | Motivo |
|---|---|---|---|
| P1 | "Tu nota es 9 sobre 10." | `block` (`assigns_grade`, Regla A) | caso original H02 — nota + verbo copulativo + dígito |
| P2 | "Te otorgo un sobresaliente." | `block` (`assigns_grade`, Regla B) | verbo de otorgamiento + cualitativo, sin "nota"/"calificación"/"puntuación" |
| P3 | "Has aprobado." | `block` (`academic_decision`, sin cambios) | decisión académica explícita, patrón preexistente |
| P4 | "Tu calificación queda en notable." | `block` (`assigns_grade`, Regla A) | verbo intermedio + cualitativo |
| P5 (nuevo, punto 3 de esta ronda) | "Tu puntuación en la práctica es 9/10." | `block` (`assigns_grade`, Regla A — fracción como valor) | "en la práctica" son 3 palabras de relleno, dentro del límite de 4; el valor es la fracción, no un dígito suelto |
| P6 (nuevo, = V2 de la ronda anterior, ya no "reportado" sino implementado) | "9/10 en la práctica 2." | `block` (`assigns_score_fraction`, Regla C) | fracción sin disparador de calificación, contexto de ítem evaluado ("práctica") |
| P7 (nuevo, punto 3 de esta ronda) | "Tu nota es un nueve." | `block` (`assigns_grade`, Regla A — numeral cardinal) | valor expresado en palabras, no en dígitos |
| L1 | "La nota de corte de esta asignatura el año pasado fue 7, según la guía docente." | `approved` | "fue" no es uno de los verbos copulativos reconocidos (`es`/`será`/`queda en`) — referencia histórica, no una declaración presente de calificación |
| L2 | "Toma nota de que el examen es la semana que viene." | `approved` | dentro de las 4 palabras de relleno tras "nota" aparece "es", pero el valor que le sigue ("la semana...") no es un dígito/numeral/cualitativo/fracción — la Regla A exige ambas partes |
| L3 | "En la puntuación de esta rúbrica, el criterio 3 vale 2 puntos." | `approved` | ningún verbo copulativo aparece en las 4 palabras siguientes a "puntuación" |
| L4 | "El aprobado de esta asignatura requiere entregar las tres prácticas." | `approved` | "aprobado" solo cuenta como valor cualitativo si aparece tras un disparador de calificación (Regla A) o de otorgamiento (Regla B) precedente — aquí no hay ninguno de los dos |
| L5 | "2/3 de los estudiantes aprobaron el examen." | `approved` | la Regla C exige denominador "10" exactamente — "2/3" no coincide, con independencia de que "examen" esté presente |
| L6 (nuevo, punto 3 de esta ronda) | "La probabilidad de este suceso es 9/10." | `approved` | ninguna de las tres reglas se activa: no hay "nota/calificación/puntuación" (Regla A), no hay verbo de otorgamiento (Regla B), y "suceso" no es un sustantivo de ítem evaluado (Regla C) — la fracción por sí sola nunca basta |
| L7 (nuevo, punto 3 de esta ronda) | "La fracción 9/10 equivale a 0,9." | `approved` | mismo motivo que L6 — "fracción"/"equivale" no son disparadores de ninguna regla |
| L8 (nuevo, punto 3 de esta ronda) | "No puedo asignarte una nota." | `approved` | contiene "asigno"-como-familia-léxica y "nota", pero ninguna de las dos reglas se completa: la Regla B exige un valor concreto tras el verbo (aquí sigue "una nota", que no es un valor); la Regla A exige un verbo copulativo tras "nota" (aquí no hay ninguno) — es, además, una negación/rechazo explícito de calificar |
| V1 | "Sacarás buena nota si sigues así." | `approved` | aliento genérico sin cifra ni veredicto concreto — fuera del alcance literal de FR-014 |

**Consumidores**: este agente (`ConstitutionalControl`) es reutilizado sin cambios por la
Feature 003 (control no omitible en cada turno de autoestudio, incluida la ruta
degradada/fallback de `turn_orchestrator.py`, que importa la misma función `evaluate`) y
está previsto que lo reutilice también la Feature 004 (defensa oral, `plan.md` de esa
feature, `specs/004-oral-defense-agency/plan.md:101`) — el refuerzo aquí descrito
beneficia a ambas sin que ninguna de las dos toque este archivo (Principio II).

**Límite documentado (no resuelto por este refuerzo)**: sigue sin haber negación
interpretada semánticamente (L8 queda a salvo por la estructura de las reglas, no
porque el control entienda "no puedo"), sinónimos no listados, ni ofuscación deliberada
(espaciado irregular, mayúsculas intercaladas). Superar la matriz anterior acredita
cobertura de los casos listados, **no** una garantía semántica general de que "ninguna
frase que asigne una nota pase nunca".

**Implementación**: `src/oralia/domain/policies/constitutional_control.py` —
`_PROHIBITED_PATTERNS` gana dos entradas nuevas bajo el nombre `assigns_grade` (Reglas
A y B combinadas en una única expresión con alternancia, mismo nombre de razón que ya
existía) y una entrada nueva `assigns_score_fraction` (Regla C). Pruebas en
`tests/contract/test_verification_block.py` (matriz completa, 001/T089/T088).

### 8.1 Seguimiento de H02 — tres falsos positivos corregidos (ronda de estabilización 4, 2026-09-11)

Una revisión independiente ejecutó `evaluate()` sobre el código de la ronda anterior y
encontró tres falsos positivos reales — se registran aquí con su causa exacta, no solo
el síntoma:

- **FP1** — *"Asigna un valor a la variable x."* → bloqueaba (`assigns_grade`, Regla B).
  **Causa**: `_NUMBER_WORDS` incluía `un`/`una` como numerales independientes (no solo
  como artículo delante de otro numeral) — "un" coincidía directamente como valor tras
  el verbo de otorgamiento "Asigna", confundiendo el artículo indefinido con una
  calificación.
- **FP2** — *"La nota es una observación sobre el experimento."* → bloqueaba
  (`assigns_grade`, Regla A). **Misma causa que FP1**: "una" coincidía como valor
  numeral independiente tras la cópula "es".
- **FP3** — *"En este ejercicio la probabilidad es 9/10."* → bloqueaba
  (`assigns_score_fraction`, Regla C). **Causa distinta**: la Regla C solo exigía que
  la fracción "N/10" apareciera a una distancia acotada (≤4 palabras) de un sustantivo
  de ítem evaluado, en cualquier dirección — sin exigir ninguna conexión gramatical
  directa entre ambos. "Ejercicio" aparece en la oración, pero la fracción describe una
  *probabilidad*, no una nota del ejercicio; la mera cercanía no demuestra evaluación
  académica (aparece igual en explicaciones matemáticas/estadísticas).

**Corrección (sin excepciones literales para las tres frases — verificado con
contrastes nuevos, no solo con las frases originales)**:

1. **`_NUMBER_WORDS` deja de incluir `un`/`una`** como numerales independientes —
   quedan únicamente como prefijo opcional de artículo delante de un numeral real
   (`cero`, `uno`, `dos`, ..., `diez`). "un"/"una" nunca vuelven a contar como valor por
   sí solos; solo lo hacen si preceden inmediatamente a uno de esos numerales (p. ej.
   "un nueve").
2. **La Regla B dejó de aceptar un dígito suelto como valor** (nuevo conjunto
   `_VALUE_GRANT`, sin la alternativa `\d+` que sí conserva la Regla A) — "asignar"/
   "otorgar" están muy solapados con el sentido genérico de "asignar un valor a una
   variable" (programación/matemáticas); un dígito suelto junto a esos verbos no
   demuestra por sí solo que se esté asignando una calificación. Solo una palabra de
   calificación cualitativa, un numeral cardinal deletreado, o una fracción "N/10"
   siguen siendo válidos como valor de la Regla B.
3. **La Regla C exige ahora una conexión preposicional directa** ("en"/"de" + artículo
   opcional) entre la fracción y el sustantivo de ítem evaluado, no solo cercanía
   dentro de una ventana de palabras — "9/10 en la práctica 2." tiene esa conexión
   directa; "en este ejercicio la probabilidad es 9/10." no la tiene (la fracción se
   conecta a "probabilidad" mediante "es", no a "ejercicio" mediante "en"/"de").

**Contrastes verificados (no solo las tres frases corregidas)**: "Te asigno un nueve
por tu trabajo." → sigue bloqueando (Regla B, artículo+numeral deletreado, sin cambios);
"Concede una prórroga para entregar la práctica." → aprobado (verbo de otorgamiento +
sustantivo genérico, nunca fue ni es un valor); "Asigna un 9 a la variable x." →
aprobado (dígito suelto ya no basta para la Regla B); "9/10 en el examen." → sigue
bloqueando (Regla C, conexión directa con otro sustantivo de ítem evaluado); "La
probabilidad de aprobar el ejercicio es 9/10." → aprobado (mismo patrón que FP3 con
otra redacción).

**Todos los casos previamente establecidos siguen bloqueando/aprobando exactamente
igual** — P1–P7, L1–L8, V1 sin cambios de resultado esperado (verificado, no asumido:
misma aserción, mismo archivo de prueba).

**Tarea de seguimiento**: `tasks.md` → Phase 15, **T091** (implementada y validada en
esta ronda).

## 9. Decisiones de diseño de T090 (2026-10-13)

Estas decisiones resuelven las cinco aclaraciones de FR-014/FR-015 sin reabrir H02. Son planificación, no evidencia de implementación.

### Autoridad y alcance

**Decisión**: política explícita `OutputAuthorizationPolicy` embebida en cada versión de `ActivityConfiguration`, identificada por `policy_id` y `policy_version`, con destinatarios, reglas de categoría × procedencia × destinatario, temas, propósitos, acciones, bandera de conocimiento general y una lista cerrada de IDs de mensajes operativos autorizados. Un identificador de política sin versión o una versión de esquema desconocida es inválido. La versión de configuración y la política efectivamente utilizada se registran en cada verificación.

**Razón**: `ActivityConfiguration` ya se versiona y se inmoviliza al iniciar una sesión. Una tabla de políticas separada introduciría sincronización y cambios en caliente innecesarios para el MVP. La política se copia/valida como valor de la configuración, y su modificación exige otra versión de actividad; no basta el objetivo docente en texto libre ni `general_knowledge_allowed=true` para ampliar temas/acciones. Los permisos de mensajes operativos son explícitos. **Alternativas descartadas**: reglas globales, inferencia desde `objective`, allow-all de legado y consulta directa del control a la base de datos.

**Política mínima histórica**: migrar filas existentes con política nula. Para una actividad existente que deba seguir usándose, un docente/administrador debe crear una nueva versión con permisos explícitos mínimos acordes a su propósito, destinatario y fuentes reales; ninguna autorización de datos privados se infiere. Si no hay política válida, la propuesta se bloquea. El fallback solo se muestra si una autorización independiente válida existe; de lo contrario no hay contenido. Datos y referencias heredados no se consideran autorizados por la migración.

### Prueba de vinculación, límites del MVP y recuperación

**Decisión**: la salida autorizable se compone a partir de un catálogo de plantillas confiables, ranuras tipadas y valores de referencias presentes en la instantánea de confianza. El constructor registra los intervalos exactos del texto resultante y el identificador de cada fragmento fuente. El verificador reconstruye el texto desde plantilla/ranuras, exige igualdad exacta y cobertura total de contenido no puramente estructural, valida rango, orden y no solapamiento de intervalos y contrasta cada referencia de dato/tema/propósito/acción con la instantánea. Rechaza referencias inventadas, huérfanas, incorrectas, o valores que no corresponden al texto. Una etiqueta suministrada por el generador no prueba tema ni propósito. Texto arbitrario de LLM, paráfrasis no reconstruibles y clasificación semántica libre quedan **fuera de T090** y se bloquean hasta disponer de otro mecanismo de verificación independiente; no se solucionan con patrones literales.

**Razón**: la igualdad estructural y la procedencia del constructor son observables y reproducibles. La mera coincidencia de texto con un valor autorizado es insuficiente si el valor puede proceder de otra fuente; el constructor confiable registra identificador + valor y el orquestador entrega referencias mínimas confiables, con solo metadatos para las denegadas. El texto del participante, instrucciones de LLM y metadatos de material por sí solos no son fuentes de autoridad. **Alternativas descartadas**: confiar en etiquetas del generador, escáneres de palabras clave y prueba semántica por otro LLM.

**Recuperación**: catálogo interno inmutable de entradas operativas con ID estable, plantilla exacta, propósito/acción y versión. Seleccionar una única entrada predeterminada, sin asumir que está autorizada ni interpolar texto rechazado o datos de sesión. Su comprobación usa la misma función constitucional y exige permiso explícito de política; si falla, registrar `unsafe_fallback` y cerrar sin texto. `missing_policy` e `invalid_context` no pueden transformarse en aprobación usando un mensaje presumiblemente seguro. La traza conserva códigos, versión de política, IDs de plantilla y conteo de intentos, nunca el texto bloqueado, valores de ranuras o la instantánea completa.

### Compatibilidad y riesgos

**Decisión**: `evaluate(str)` subsiste únicamente como clasificador H02 para llamadas heredadas y su matriz; la autorización final estructurada recibe un contrato nuevo y falla en cerrado ante una llamada solo textual. Los compositores de Feature 003 y las rutas de degradación se migran a esa única puerta, sin tocar la lógica de grounding Feature 002. El catálogo de fallbacks convierte `SAFE_FALLBACK_TEXT`, `_ACKNOWLEDGE_MISSING_INFO_TEXT` y `SAFE_BLOCKED_MESSAGE` en entradas autorizables solo si su contenido coincide exactamente con la versión catalogada; ninguna constante se publica de forma directa.

**Riesgos reales**: (1) el eco libre del participante en la ruta principal, el texto producido por adaptadores de generación y las preguntas de práctica pueden carecer de vinculación estructural; antes de activar el bloqueo se necesita composición verificable o cierre sin contenido, nunca una exención. (2) La persistencia actual de `InternalMessage`/`GeneratedProposal` puede incluir propuesta rechazada; diseñar saneamiento de trazas y retención evitando fugas, preservando solo metadatos de bloqueo. (3) La API pública histórica declara `output_text: string`; la finalización sin contenido requiere compatibilidad `string | null` y revisión de clientes. (4) Al principio muchas actividades antiguas quedarán sin salida; es una consecuencia deliberada del cierre en seguro y exige versionado docente explícito. (5) Cualquier salida que se transforme después de verificada debe pasar otra vez por la puerta final.

## 10. Revisión correctiva de decisiones T090 (2026-10-13)

**Política física — decisión**: guardar el documento validado como JSON canónico en columna SQLAlchemy `Text`/SQLite `TEXT` nullable más SHA-256 en `String(64)` nullable, no como un `dict` mutable en columna `JSON`. Validar con modelo Pydantic v2 congelado, colecciones inmutables y esquema cerrado; serializar con orden estable y comprobar hash al leer. `NULL` en legado bloquea. Alembic agrega esas dos columnas y `VerificationResult.authorization_context` nullable. **Razón**: elimina la mutación silenciosa en memoria, permite comparar/hash/versionar el valor exacto y reutiliza `ActivityConfiguration`/`VerificationResult`; trigger de SQLite y guardia de aplicación protegen la política tras primer uso. **Alternativa**: `JSON`/`MutableDict` en configuración exigiría copia profunda y vigilancia de mutaciones anidadas, con más superficies de error. El cambio de política de una actividad ya usada necesita una operación de sucesión explícita porque `create_activity(family_id=...)` hoy rechaza familias cuya última versión es inmutable; esa operación crea una fila nueva, nunca edita la antigua.

**Veredicto — decisión**: `AuthorizationVerdict` solo existe como valor temporal. Se persiste el resultado final en una fila `VerificationResult` existente; `reasons` contiene códigos ordenados, la columna nueva conserva identidad/versiones/huellas y `TraceEvent` conserva cada intento. Los cuatro valores históricos permanecen. **Razón**: una tabla nueva produciría dos fuentes de verdad y consultas más complejas. El bloque inicial seguido de fallback aprobado deja traza del bloque y `VerificationResult.approved` de la salida finalmente visible; `Turn.status=degraded`, no `blocked`. Si ambos fallan, el veredicto final es `block` y `Turn.output_text=NULL`, que ya está permitido por el modelo. **Alternativa**: dos filas `VerificationResult` por turno contradicen la relación histórica 1:1; por ello se descarta.

**Camino positivo — decisión**: la primera salida normal de Feature 001 usa una plantilla confiable sin eco de entrada, por ejemplo `He recibido tu mensaje. Continuemos con la actividad.` con política explícita de tema/propósito/acción y segmento fijo completo. **Razón**: prueba SC-007 de inicio→turno visible→cierre sin confiar en texto libre del participante ni apagar FR-014. **Alternativa**: mantener el eco libre exigiría tratar entrada no confiable como dato autorizable y podría publicar contenido fuera de alcance; queda fuera del recorrido mínimo. Algunas pruebas de integración del eco deberán actualizar su expectativa legítimamente; no se modifican las pruebas H02 ni su clasificador.

**Catálogo — decisión**: identificador `(id, version, sha256)` inmutable y conservación de versiones referenciadas por configuraciones/sesiones/trazas, también tras despliegues. **Razón**: un ID solo no permite reconstruir la decisión histórica. **Alternativa**: sobrescribir plantillas por ID, descartada. La eliminación de una versión requiere comprobar ausencia de referencias o una migración/archivo verificable; la falta de versión en ejecución cierra en seguro.

**Riesgos que permanecen**: composición verificable de las salidas de Feature 003 sin cambiar sus verificadores de grounding; saneamiento de `InternalMessage` y `GeneratedProposal`; actualización simultánea de tipos API/web; adopción explícita de política en todas las factories/seeds y configuración histórica. No son dudas sobre la política ni motivo para una exención de seguridad.
