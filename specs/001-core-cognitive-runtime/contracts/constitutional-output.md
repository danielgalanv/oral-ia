# Contrato interno propuesto: autorización de salida T090 (2026-10-13)

**Estado**: diseño, no implementado. Especializa `agent-contract.md` para FR-014/FR-015 y deja intactas las reglas H02. Todos los campos descritos son conceptuales; la implementación tipada se hará durante T090.

## Autoridad

`OutputAuthorizationPolicy` se almacena como valor de la versión concreta de `ActivityConfiguration`: `policy_id`, `policy_version`, `schema_version`, destinatarios permitidos, triples autorizados `(category, provenance, recipient)`, conjuntos de `topic_ref`, `purpose_ref` y `action_ref`, `general_knowledge_allowed`, y conjunto de `operational_message_id` permitidos. Su identidad efectiva incluye `activity_configuration_id` + versión, `policy_id` + versión y versión de esquema. Permisos ausentes son denegaciones, no comodines. Una política mal formada o de versión no compatible se bloquea. `general_knowledge_allowed` también exige permitir tema, propósito y acción; no autoriza datos particulares.

`AuthorizationSnapshot` la construye el orquestador desde la configuración y fuentes identificadas para el turno. Contiene la identidad efectiva de la política, `recipient` real de la sesión, reglas filtradas y un mapa mínimo de referencias confiables usadas en la propuesta. Cada referencia indica ID opaco, categoría, procedencia y referencias de alcance asignadas por un constructor confiable; **solo las referencias autorizadas** aportan el valor exacto o huella con medio de comparación necesarios para verificar el texto. Puede describir una referencia denegada para explicar `unauthorized_data`, sin concederle permiso ni incorporar su valor a un fallback o una traza. No hay acceso del control a la base de datos. Ni el generador ni una etiqueta escrita por él pueden crear o cambiar esta instantánea.

## Propuesta y comprobación

`OutputProposal` contiene `text` (los bytes/caracteres exactos destinados al participante), `message_type` (`normal` u `operational`), `template_id` + versión, y una secuencia de `segments`. Cada segmento lleva `start`, `end` en índices de caracteres Unicode (intervalo semiabierto `[start,end)`), texto/valor esperado, `data_ref` opcional, y referencias `topic_ref`, `purpose_ref`, `action_ref`. Las partes fijas de la plantilla también tienen cobertura y procedencia de catálogo confiable. Las ranuras de datos nunca reciben autoridad solo porque un generador las nombre.

Validación determinista, en orden: (1) validar versiones, configuración, destinatario y forma cerrada de instantánea/propuesta; (2) validar intervalos y cobertura total de **todos** los caracteres mediante segmentos fijos de plantilla o ranuras; (3) reconstruir el texto desde plantilla exacta y ranuras ya presentes en la propuesta del constructor confiable, comparando igualdad de texto final sin consultar otras fuentes; (4) resolver los identificadores de referencia y comprobar tipo/categoría/procedencia/destinatario **antes** de obtener valores externos; (5) solo para referencias autorizadas, comprobar valor/huella y vínculo con texto; (6) comprobar temas, propósitos y acciones contra la política y su vínculo con plantilla/referencia confiable; (7) aplicar H02 al texto final sin cambiar sus reglas. Rechazar una referencia inventada, ausente, de tipo incompatible, huérfana o que reclame un valor distinto. Si no puede reconstruirse o autorizarse un segmento, `unverified_binding`; si existe una referencia válida pero el triple no está permitido, `unauthorized_data`; si el alcance no está permitido, `out_of_scope`.

Para el MVP, una salida de LLM en texto libre no es autorizable por simples etiquetas ni por coincidencia léxica; debe transformarse en composición comprobable mediante constructor confiable o bloquearse. El constructor no puede tomar libremente un texto prohibido y declararlo «plantilla». El catálogo de plantillas es controlado por el proyecto/administración, versionado y separado de contenido generado. La autorización estructural no reemplaza grounding ni la admisión de materiales de Feature 002; esos verificadores mantienen sus propias entradas y veredictos.

## Veredicto y recuperación

`AuthorizationVerdict`: `verdict` (`approved`/`block`), `reason_codes` (lista cerrada), identidad efectiva de configuración/política, `template_id` y `fallback_attempt` (0 o 1). Códigos mínimos: `unauthorized_data`, `out_of_scope`, `missing_policy`, `invalid_context`, `unverified_binding`, `unsafe_fallback`; los códigos H02 existentes permanecen. `invalid_context` incluye destinatario, configuración o versión incongruentes; `missing_policy` distingue política ausente; `unsafe_fallback` registra rechazo de la única alternativa. No registrar texto de la propuesta bloqueada, valores de ranuras, instantánea completa ni trazas del razonamiento privado.

Si se bloquea la primera propuesta, el orquestador registra la causa y elige **una** entrada predeterminada `operational_message_id` de un catálogo interno confiable; su elección no implica permiso. Su texto exacto, versión, tema/propósito/acción y cobertura de plantilla se reconstruyen y verifican con el mismo control, incluida su autorización explícita por la política. Se descarta íntegramente la propuesta rechazada. Si falta política/contexto o falla esta verificación, la respuesta visible tiene `output_text = null`, `blocked = true` y acción de cierre seguro; no hay tercer intento. El catálogo no concede permisos por sí mismo.

## Corrección de diseño T090 — cobertura, persistencia y precedencia (2026-10-13)

Esta sección precisa la adenda precedente y prevalece sobre sus formulaciones abreviadas; no altera el contrato histórico. Los índices `[start,end)` se miden en **puntos de código Unicode de `str` en Python**, no en bytes UTF-8 ni unidades UTF-16. Para texto no vacío: `segments[0].start = 0`, cada `segments[i].end = segments[i+1].start`, y `segments[-1].end = len(text)`; cada intervalo cumple `start < end`. Segmentos ordenados y contiguos cubren **todos** los caracteres: letras, espacios, separadores, puntuación, prefijos y sufijos. Un hueco de un carácter bloquea. El texto fijo también ocupa segmentos de una plantilla versionada y participa en la reconstrucción exacta. Texto vacío no es una propuesta visible autorizable. La comparación es igualdad exacta de cadenas Python con `text[start:end]`, sin `strip`, casefold ni normalización Unicode silenciosa; si entrada y plantilla usan formas distintas, se rechaza la vinculación.

`AuthorizationVerdict` es un **valor efímero interno**, no una nueva tabla. El control constitucional final emite solo `approved` o `block`, que se escriben sin traducción semántica en el `VerificationResult.verdict` existente; `reformulate` y `clarify` permanecen en el contrato general para otros verificadores. Se persiste **una fila final** `VerificationResult` por turno, asociada a la propuesta final considerada: `reasons: list[str]` contiene los códigos finales ordenados y sin duplicados; `approved` lleva `[]`. Una nueva columna nullable `VerificationResult.authorization_context` de tipo SQLAlchemy `JSON` (SQLite JSON almacenado como TEXT) conserva `activity_configuration_id`, `activity_version`, `policy_id`, `policy_version`, `schema_version`, huella canónica de política, `template_id`, `template_version`, huella de plantilla, `attempt` (0 propuesta inicial, 1 alternativa) y `message_type`. Es metadato, no otra fuente de veredicto. `TraceEvent.payload` registra un evento por intento con `turn_id`, `attempt`, `verdict`, `reason_codes` ordenados e identidades/versiones/huellas no sensibles; el intento 0 bloqueado queda trazado aunque el 1 se apruebe. La traza del intento final puede referenciar `VerificationResult.id`. Se excluyen propuesta bloqueada, valores de ranura, referencias de datos potencialmente personales, política completa y razonamiento privado. `GeneratedProposal.content` de un intento rechazado no conserva texto bruto: solo metadatos saneados; la propuesta final aprobada puede guardar el texto visible conforme a la retención ordinaria. Grounding y coherencia siguen en sus resultados separados; no cambian `VerificationResult.verdict` del control constitucional.

**Precedencia y cortocircuitos**: orden único de códigos: `missing_policy`, `invalid_context`, `invalid_proposal`, `unverified_binding`, `unauthorized_data`, `out_of_scope`, los códigos H02 existentes en su orden histórico, `unsafe_fallback`. Se deduplican y ordenan siempre así. Política ausente detiene la inspección con `missing_policy`; identidad/esquema/contexto inválidos detienen con `invalid_context`; forma estructural inválida (segmentos fuera de rango, huecos, solapamientos, Unicode incorrecto) detiene con `invalid_proposal`; reconstrucción o referencia no verificable detiene con `unverified_binding`. Tras superar esas puertas, se pueden acumular `unauthorized_data`, `out_of_scope` y H02 mediante metadatos confiables y texto ya presente en memoria, **sin leer valores de referencias denegadas** ni acceder a nuevas fuentes. Un intento 1 bloqueado añade `unsafe_fallback` al final, incluso si la causa primaria fue `missing_policy` o `invalid_context`. Cualquier excepción o timeout se traduce a `invalid_context`/`unsafe_fallback` y bloqueo, nunca aprobación. Códigos de otros verificadores no se mezclan con estos.

**Estados visibles**: intento 0 aprobado → `VerificationResult.approved`, `Turn.status=completed`, texto autorizado visible; intento 0 bloqueado e intento 1 aprobado → `VerificationResult.approved` para la alternativa, `Turn.status=degraded`, `blocked=true` en API para informar el rechazo inicial, texto operativo visible y evento de intento 0 con su causa; intento 1 bloqueado → `VerificationResult.block`, `Turn.status=blocked`, `Turn.output_text=NULL`, `blocked=true`, acción `finish` y `Session.status=closed_error_safe` tras persistir el turno. Así `VerificationResult` sigue siendo la única verdad del veredicto constitucional **final**, mientras los eventos conservan la historia de intentos. Nunca se publica el texto inicial rechazado.

Un fallback iniciado por fallo/timeout de otro agente **ya consume** el único intento operativo de esa incidencia (`attempt=1`); si el control lo bloquea, se cierra sin evaluar otra alternativa. Si no llegó a existir propuesta inicial, la traza registra el fallo upstream y solo el intento 1 constitucional. Una respuesta normal rechazada registra intentos 0 y 1. `blocked=true` expresa que se rechazó una salida candidata o que el fallback no pudo autorizarse, sin cambiar el significado del veredicto final persistido.

**Catálogo**: identidad completa `(template_id, template_version, sha256_del_contenido_canónico)` para plantillas normales y operativas. Una versión publicada es inmutable; no se reutiliza el mismo par ID/versión con otro contenido. Política y trazas guardan versión y huella; el registro local conserva versiones antiguas mientras una configuración, sesión o verificación pueda referenciarlas, incluso tras actualizar el código. Una versión ausente o huella discordante provoca `invalid_context`, no sustitución por la versión nueva. Los permisos operativos de la política se expresan como pares `(operational_message_id, version)` y los normales como pares `(template_id, version)`.

## Estado de implementación validado — T146 (2026-10-16)

La cabecera histórica de este documento registra su estado cuando se propuso el
contrato. T092–T143 y las convergencias T148–T150 implementan y validan actualmente la
adenda T090: política y catálogo inmutables/versionados, migración equivalente entre
Alembic y `create_all`, instantánea mínima ligada a sesión/configuración/destinatario,
propuesta estructurada, cobertura Unicode exacta, autorización por referencia y
alcance, H02 sin cambios, puerta 0/1, persistencia final saneada y cierre seguro
transaccional.

La validación focal final fue **263 passed, 1 warning** y la suite exacta sin las dos
reproducciones deliberadamente rojas de Feature 002 fue **581 passed, 3 deselected,
1 warning**. La privacidad se verifica en propuesta, transporte, eventos,
`authorization_context`, API y errores: un rechazo no conserva texto bruto ni valores
denegados; el texto aprobado conserva solo la salida visible conforme a retención. El
cierre concurrente usa el resultado real del `UPDATE active -> terminal`; únicamente el
ganador genera resúmenes/evento/liberación y una excepción previa al commit exterior
revierte todo el cierre.

Ruff 0.15.22 conserva 17 hallazgos heredados frente a 49 del manifiesto T092: 12 sin
mover, 5 desplazados, 32 eliminados y **0 nuevos** por identidad estable. El manifiesto
permanece intacto con SHA-256
`3cae09803a082a5e5dc7bcc31b387d3823d2eaae3c8a9d677a07e1bc0a541b30`.

Las reproducciones A/B de la carrera de reconstrucción del índice siguen fallando de
forma deliberada y pertenecen a T087/T092 de Feature 002; este contrato no declara esa
carrera resuelta.
