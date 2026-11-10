# Hallazgos y criterios para resolverlos

P0 identifica una decisión o barrera previa a la publicación. P1 señala una corrección o incertidumbre de alto impacto. P2 corresponde a trabajo posterior. No son puntuaciones de vulnerabilidad. Las rutas se expresan desde la raíz del proyecto; las líneas corresponden al código leído y se acompañan de funciones para facilitar su localización.

## F01 — P1 — Defecto reproducido de identidad de embeddings

En `src/oralia/infrastructure/embeddings/sentence_transformer_adapter.py`, líneas 24–42, la caché `_model` es global y no está ligada a `model_name`. Dos instancias configuradas como A y B reciben ambas el modelo A. La [reproducción CPU](embedding-identity-results.json) usa un constructor falso: no carga pesos ni intenta conexiones. Esto puede invalidar cambios de encoder y comparaciones; no demuestra que afectara a los ensayos históricos.

Resolución verificable: caché por identidad completa o rechazo explícito de configuraciones incompatibles. Probar A→B→A y cargas concurrentes con dobles que registren identidad y número de cargas. Conservar el comportamiento del modelo por defecto.

## F02 — P1 — La garantía de modo offline es más fuerte que el código

En el mismo archivo, líneas 37–38, `setdefault` deja intactas las variables de entorno si ya valen `0`. La reproducción confirma esa diferencia con el docstring que afirma forzar ejecución offline. No se observó tráfico: el modelo era falso.

Resolución verificable: carga explícitamente local o rechazo antes de invocar el cargador cuando la configuración contradiga la política. Probar variables ausentes, `0`, `1` y caché ausente con transporte simulado. No depender únicamente de variables globales fijadas por un launcher.

## F03 — P1 — Falta una identidad suficiente del espacio vectorial

`src/oralia/infrastructure/vector_store/chroma_store.py` versiona colecciones y un puntero, pero la interfaz observada no liga cada índice a un fingerprint completo de encoder, revisión, normalización y estrategia de representación. F01 hace especialmente importante esta frontera: dos modelos pueden compartir dimensión y producir espacios incompatibles. No se abrió ni declaró corrupto ningún índice habitual.

Resolución verificable: guardar y comprobar ese fingerprint antes de consultar o añadir vectores; un desacuerdo bloquea y explica la reconstrucción necesaria. Ensayar encoders de igual dimensión pero distinta identidad. No reindexar datos existentes automáticamente.

## F04 — P1 — Presupuestos de salida recortados silenciosamente

`src/oralia/course_dialogue/cached_transformers.py`, líneas 128–130, aplica un máximo de 512 tokens a peticiones ordinarias y 768 a `LabGenerationRequest`. `generation/config.py` limita también Ollama a 512. La [evaluación aislada de la expresión](cpu-boundary-results.json) confirma que solicitar 2.048 no los hace efectivos. No es una ejecución del worker.

Resolución verificable: validar el presupuesto prospectivamente y registrar solicitado, efectivo y motivo. Rechazar una configuración incompatible o negociarla antes del ensayo. Cambiar únicamente el protocolo no basta; tampoco se deben reinterpretar los resultados truncados anteriores.

## F05 — P0 — Contrato pendiente para autorizar contenido generativo

`output_proposal_builder.py`, línea 39, y el contrato T090 aceptan composición desde plantillas y valores autorizados. Feature012 exige texto generado y revisión semántica. La reconstrucción literal preserva permisos, pero no proporciona por sí sola una autoridad que permita publicar ese texto libre. Esto es una incompatibilidad de integración pendiente, no un defecto que deba sortearse.

Resolución verificable: contrato sucesor versionado, con autoridad de revisión independiente del generador, vínculo al texto exacto y vigencia de fuentes. Requiere revisión humana del cambio. Probar que un permiso no sirve para otro texto, sesión o configuración. Una ranura llamada `trusted_text` no resuelve la frontera.

## F06 — P0 — No confundir aceptación empírica con garantía universal

El conceptual del MVP, párrafo P1971, pide detección de una parte significativa de salidas no fundamentadas. Los gates posteriores son más específicos y siguen vigentes. No se recuperó una instrucción humana que exija una demostración formal universal para toda paráfrasis libre. Tampoco hay permiso para rebajar las condiciones actuales.

Resolución verificable: especificar qué clases de error, cobertura y riesgo residual permiten avanzar; identificar qué es criterio finito de ensayo y qué es obligación de producto. Si se exige formalización completa, presentar su coste y el cambio de producto al usuario, sin imponerlo por interpretación del agente.

## F07 — P1 — El clasificador anterior a toda búsqueda puede ser un cuello artificial

`rag_lab.py`, líneas 228–286, devuelve un límite por alcance incierto antes de recuperar. FR-017 exige decidir antes de generar, no demuestra que sea necesario impedir una búsqueda previa sobre fuentes ya autorizadas. Los fallos de F01/C01 del clasificador muestran el coste de esa elección.

Prueba de refutación: comparar la condición actual con una variante que recupere primero en el catálogo autorizado y use esa evidencia como información auxiliar de alcance. Medir falsas exclusiones, inclusiones y preguntas mixtas. La política docente sigue siendo autoridad; un score o un resultado vacío nunca prueban exclusión.

## F08 — P1 — Reutilización parcial de recuperación

Feature002 dispone de recuperación densa multilingüe y Chroma en `material_retriever_agent.py`; Feature012 usa selección léxica de unidades en `document_evidence.py`. La segunda vía mejora procedencia y unidades, pero no hereda automáticamente la capacidad densa. No se ha demostrado que sea globalmente superior o inferior.

Resolución verificable: comparar ambas estrategias sobre las mismas unidades, consultas y filtros de autoridad. Reutilizar sus interfaces y controles después de corregir F01–F03. No sustituir una vía a ciegas ni adoptar un nuevo modelo antes de medir la capacidad ya disponible.

## F09 — P1 — Filtros previos pierden evidencia antes del reranking

`document_evidence.py`, líneas 284–295, filtra por coincidencias de conceptos y por un umbral relativo al mejor candidato. R04/R05 documentan omisiones por ranking sin agotar presupuesto; el historial extenso puede elevar el umbral. Añadir un reranker después no recupera lo que ya fue eliminado.

Resolución verificable: medir recall antes y después de cada filtro, peso total del historial y contexto entregado. Congelar positivos y distractores nuevos. No forzar una página por ID del caso ni ajustar repetidamente los seis controles expuestos.

## F10 — P1 — Extracción correcta no significa representación docente suficiente

`pdf_extractor.py`, línea 15, extrae texto; `pptx_extractor.py`, línea 44 en adelante, trata tablas nativas. No son representaciones equivalentes de diagramas, fórmulas y relaciones visuales. Las 26 páginas en cuarentena son una limitación de cobertura, no prueba de que los temas estén excluidos.

Resolución verificable: inspección por página o diapositiva y correspondencia con el original. Ensayar extracción estructural u OCR solo en huecos relevantes. Validar tablas y relaciones, no solo cantidad de caracteres; conservar los originales y las decisiones previas.

## F11 — P1 — La proyección técnica no es un saneador universal

`session_privacy_service.py`, líneas 59–105, filtra nombres de claves, pero conserva cadenas arbitrarias bajo claves permitidas como `reasons`, `model` o `scope`. El [contraejemplo con sentinel](cpu-boundary-results.json) demuestra ese límite del componente. No demuestra una ruta explotable desde el participante ni una fuga real en los datos existentes.

Resolución verificable: recorrer productores, tipar los payloads por evento y cerrar códigos o identificadores donde se prometen datos técnicos. Probar estructuras anidadas, conservación negativa y exportación. No declarar resuelto el flujo completo por un test de una función aislada.

## F12 — P1 — Recuperación tras caída y purga necesitan un contrato operativo

Los tokens de `LocalAccess` viven en memoria; una sesión persistida puede permanecer activa tras reiniciar y perder el acceso del propietario. Existe cierre docente confirmado. `purge_private_sessions`, línea 497 en adelante, considera sesiones terminadas, por lo que no resuelve por sí mismo todas las sesiones abandonadas activas.

Resolución verificable: ensayo de caída y reinicio con datos aislados, recuperación segura o cierre autorizado, y comprobación de purga posterior. No habilitar recuperación pública por código seudónimo ni borrar automáticamente una sesión que pudiera estar activa en otro proceso.

## F13 — P2 — Borrado lógico y eliminación forense son promesas distintas

`infrastructure/db/engine.py` activa WAL; `erase_content` redacta o elimina filas. No se comprobó si quedan residuos reales. La configuración observada no permite afirmar borrado forense completo de base, WAL, backups y exportaciones.

Resolución verificable: definir amenaza y alcance de la promesa, inventariar copias y probar una base sintética. No ejecutar VACUUM ni checkpoints sobre datos habituales como remedio automático. Una exigencia nueva de eliminación forense requiere decisión explícita y análisis de coste.

## F14 — P1 — Delimitar documentos no neutraliza toda inyección

`ollama_adapter.py:_build_user_content` y `cached_transformers.py`, líneas 118–122, incorporan texto en etiquetas. Los roles separados ayudan, pero las etiquetas no son una frontera de seguridad formal y admiten contenido que imita delimitadores. No se ejecutaron ataques contra servicios.

Resolución verificable: pruebas directas e indirectas con documentos ficticios, controles de salida y ausencia de capacidades de red o escritura concedidas al LLM. Escapar delimitadores elimina una ambigüedad formal, pero no prueba resistencia semántica ni sustituye autorización del host.

## F15 — P1 — Revalidar varias veces no demuestra atomicidad total de entrega

`conversation_lab.py:prepare_display/acknowledge_display` y la caché de `rag_lab.py` tienen controles útiles. Quedan supuestos sobre mutabilidad de recibos/catálogos y la ventana entre verificación, envío y confirmación. Esta revisión no reprodujo una entrega no autorizada.

Prueba de refutación: definir el punto de commit, una instantánea inmutable o copia defensiva, y qué ocurre si se retira una fuente entre fases. Ensayar intercalaciones concretas. El sistema no puede retractar bytes ya vistos; debe declarar y controlar esa frontera, sin prometer atomicidad imposible con la pantalla.

## F16 — P1 — Locks de proceso y transacciones de base tienen alcances diferentes

`app.py`, línea 34, crea un lock asíncrono por proceso; `end_session.py`, líneas 39–43, usa una transición condicional en la base. El segundo protege al ganador en su alcance; el primero no coordina otros procesos por sí solo.

Resolución verificable: dos conexiones o procesos aislados, reintentos con el mismo identificador y caída después del commit. Comprobar cierre, resumen y liberación únicos; cancelación o resultado tardío no publican ni duplican efectos.

## F17 — P1 — Verificación semántica todavía insuficiente

El juez que pasó 7/7 controles breves aceptó después salidas largas con defectos centrales. H1 verifica un plan sin cubrir toda su realización libre. La comparación pedagógica falla con evidencia presente. Son límites medidos de candidatos y métodos concretos, no incapacidad universal del RAG local.

Prueba de refutación: señal independiente calibrada sobre español, negación, modalidad y conclusiones de ejemplos; medir omisiones del extractor, falsos permisos, falsos rechazos y cobertura. No reemplazar esa evaluación por acuerdo entre dos modelos o presencia de citas.

## F18 — P1 — Las paradas tempranas preservan evidencia, pero limitan el diagnóstico

Parar al primer fallo evita contaminar continuidad o gastar presupuesto, pero deja familias sin medir. No se debe puntuar como fallidos los turnos no ejecutados. Tampoco una salida que falla formato prueba automáticamente incapacidad conceptual.

Resolución verificable: separar controles independientes del diagnóstico offline y el flujo conversacional que solo continúa desde lo mostrado. Se pueden analizar candidatos rechazados como bruto; no incorporarlos al historial ni usarlos para declarar una conversación completa.

## F19 — P1 — Falta evidencia de utilidad de estudio

La prueba de usuario del 18 de octubre y los criterios P1976–P1983 muestran que completar APIs o citar no basta. La reformulación debe ayudar a superar una dificultad y los ejemplos deben permitir aplicar el principio. No hay todavía aceptación docente suficiente del tutor generativo.

Prueba de refutación: episodio completo con objetivo puntual, adaptación y transferencia, revisado por docentes; medir además carga de revisión y claridad. No convertir sus resultados en una nota del alumno ni guardar un perfil de capacidad.

## F20 — P2 — La ruta de inspección no es la experiencia de estudio final

`scripts/course-dialogue.ps1`, línea 4, bloquea el perfil no aprobado y ofrece inspección. Ese límite es honesto, pero no satisface la experiencia final. Los perfiles extractivos previos no se transforman en tutor por compartir launcher o interfaz.

Aceptación: recorrido docente→actividad→participante→fuentes→cierre, con capacidades visibles, teclado y errores accionables. Mantener la publicación cerrada mientras falten los gates; no invertir primero en otra interfaz de laboratorio.

## F21 — P2 — La superioridad arquitectónica sigue siendo una hipótesis

Las 204 celdas son sintéticas; A/B/C difieren también en contenido. No aíslan el valor de los agentes. Eso no invalida la modularidad, pero impide atribuirle mejoras pedagógicas o de rendimiento.

Prueba de refutación: ablación pareada con mismas fuentes, modelo y presupuestos, midiendo calidad, bloqueos, coste y latencia. No generar otro paquete de 204 celdas como sustituto de esa comparación.

F01–F04 tienen reproducción o evaluación estática directa. F11 prueba el límite de una función. F12–F16 identifican fronteras que necesitan pruebas, no vulnerabilidades explotadas. T090 y T150 son contratos valiosos que deben comprobarse, no sellos generales de seguridad.
