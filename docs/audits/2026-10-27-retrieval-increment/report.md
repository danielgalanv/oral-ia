# Incremento de recuperación v2.1 — entrega y resultado negativo de promoción

27-10-2026. Se implementó la recuperación optativa sobre las **117 unidades habilitadas del corpus v2**, con **207 fragmentos de búsqueda** ajustados al tokenizer. La interfaz existente acepta una pregunta natural y muestra pasajes, documento, página/sección, procedencia y original consultable. No genera respuestas ni evalúa al alumno. **Ninguna variante nueva supera todos los criterios prospectivos; se conserva el baseline léxico.** No se inicia otro modelo ni una segunda pasada.

[Guion docente](teacher-guide.md) · [Métricas por pregunta/subtema](metrics.md) · [Decisión](decision.json) · [Banco/oráculo](bank-v1.json) · [Protocolo](protocol-v1.json) · [Congelación](freeze.json) · [Identidad efectiva](../../../materiales/docente/piloto-requisitos/recuperacion-v2.1/identity.json).

## Implementación y fronteras

- `src/oralia/documentary/retrieval.py`: composición única de encoder/tokenizer local CPU, fingerprint, fragmentación, construcción explícita e idempotente, reapertura y consulta del índice nuevo. Reutiliza `SentenceTransformerEmbeddingAdapter`, `ChromaVectorStore` y `query_excerpt.terms`. La referencia léxica conserva el conteo ponderado por coincidencias sobre la **misma representación nueva**; no es una reproducción del ranking histórico por páginas enteras ni del selector de contexto con diversidad/vecinos de `document_evidence.retrieve_units`. No se afirma equivalencia de esas dos rutas.
- Adaptador existente: opciones explícitas `device='cpu'` y normalización L2; el dispositivo forma parte de la clave de caché. Defaults históricos conservados. No carga GPU, generador ni otro checkpoint.
- `src/oralia/documentary/__main__.py`: opción explícita `--package v2 --retrieval`; por defecto sigue documental v1.1 sin importar modelos/Chroma. Endpoint docente local `/api/v1/retrieval`, mismo acceso Host/Origin/cookie, cierre y revalidación del permiso tras la espera. La estrategia final es léxica. El servidor activo no cambia de paquete/perfil.
- `apps/web/src/routes/Tecnica.tsx`: sección «Pasajes recuperados» dentro de Materiales, solo si el servidor declara la capacidad. Referente opcional visible y cambio explícito que lo descarta; no historial oculto o de examen. Cierre desmonta la sección e ignora resultados tardíos. No selector técnico para el docente.
- Scripts propios `scripts/run_retrieval_increment.py` y `scripts/verify_retrieval_increment.py`; pruebas nuevas `tests/unit/test_retrieval_increment.py`. Sin SQL, migración, reindexación habitual, commits o Reset.

Derivados en `materiales/docente/piloto-requisitos/recuperacion-v2.1/`, fuera de los paquetes anteriores: Chroma generación2, representación `fragments.json`, recibo `identity.json`. La construcción inicial es explícita; reapertura con `build=True` sobre identidad coincidente no vuelve a indexar. Raíz desconocida o recibo incompatible rechazan antes de crear/escribir Chroma. No existe operación de migración automática.

T077 queda **parcial**: se integran construcción/consulta/reapertura de este perfil. Siguen sin esta composición efectiva los defaults de `application/commands/ingest_material.py`, `application/commands/rebuild_material_index.py`, `domain/agents/material_retriever_agent.py`, `course_dialogue/corpus.py` y los warmups de `course_study/__main__.py` / `demo/resources.py`. Ningún índice histórico queda acreditado por compartir dimensión.

## Identidades, representación e integridad

Encoder instalado `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, snapshot local `e8f8c211226b894fcb81acc59f3b34ba3efd5f42`. Hashes de todos sus archivos en el recibo, no revisión inferida del nombre. Dimensión384, pooling medio, L2, CPU, límite128 **incluidos tokens especiales**. Versiones: sentence-transformers5.6.0, transformers5.14.1, tokenizers0.22.2, torch2.13.0, Chroma1.5.9. El fingerprint incluye fuentes, configuración efectiva, tokenizer por hashes, código de representación/adaptador y protocolo.

Fingerprint efectivo: `c2756d3c78fd3dd9237b5a6aaa5fe63513a38747bf8894635bdb9e44143cf51a`.
Manifiesto v2: `c0fb550ffa92efda47c932bb684ddc5bdf6cab4db199d73c5f0a259d8add935e`.
Banco: `a1e2f5d40740d0047b0d60ecd64f794fcc0f13fb8f97948eb8e1f9cd20880348`.
Protocolo: `751586c96f625421fe17614f2c1076c3305d03f7c6b15da3d68a9e0a4d6025fc`.

Cada fragmento tiene ID de página + offsets de caracteres exactos sobre `text` revisado. Todos los caracteres, incluidos finales y continuaciones literales, quedan representados; no se trunca durante embeddings. Se favorecen cortes por línea y se divide una línea larga si excede capacidad. Las relaciones completas de tablas y encabezados se entregan mediante la página revisada íntegra, nunca mediante una traducción o reconstrucción nueva. Contexto máximo6000 caracteres y5 páginas únicas; una página que no cabe queda omitida con motivo explícito. No se amplían automáticamente páginas contiguas: los originales y su aviso de continuidad siguen consultables, y esto limita suficiencia de secciones partidas.

El recibo enlaza texto revisado, `raw_text` por hash, derivación y original. Revalidación de originales/extracciones/manifiesto antes y después de recuperar; retirada, cambio o ruta ajena bloquean. Solo `status=disponible` se fragmenta. No se levanta cuarentena ni se reconstruyen figuras. Se deduplican fragmentos de la misma página en contexto. Equivalencias docente/Sommerville se conservan como candidatos históricos, **no se colapsan automáticamente por equivalencia semántica** ni se cuentan como corroboración independiente; el ranking puede gastar contexto en ellas. No se adquirió INCOSE ni se cambió el corpus.

Offline: `local_files_only=True`, ruta de snapshot concreta, flags HF/Transformers offline, telemetría desactivada, GPU oculta y CPU confirmada. Verificación independiente con `socket.connect` rechazando conexiones externas: cero intentos observados. Sin descargas, instalación, fallback remoto o llamadas LLM. El banco no se etiquetó mediante LLM.

## Medición congelada y decisión

30 escenarios nuevos: dos por cada uno de12 subtemas (24), cuatro controles positivos bilingües/referente/cambio y dos de ausencia/distractor. Doce escenarios de desarrollo y doce distintos de evaluación, más los controles; sin ajuste tras observar resultados. Las dos preguntas del demostrador son regresiones expuestas separadas. Oráculo con pasajes exactos, hashes y motivo seleccionados de las fuentes antes de ranking; propuesta técnica auditable, no revisión docente ni catálogo exhaustivo de todas las alternativas válidas. Fuentes equivalentes no son evidencia independiente.

Tres estrategias, una pasada de30 consultas cada una, todas finalizadas. Candidatos20 fragmentos, RRF60, empates por ID, contexto6000/5. RRF combina posiciones. No había `rank_bm25` ni `bm25s` instalados; no se instalaron. Se mantuvo la rama léxica descrita. No reranker ni ampliaciones iterativas.

Sobre16 positivos de evaluación (12 escenarios +4 controles):

| Estrategia | Recall candidatos | Recall final | MRR final | nDCG binario | Consulta media |
|---|---:|---:|---:|---:|---:|
| Léxico |0.750|0.625|0.422|0.446|0.043s|
| Denso CPU |0.813|0.813|0.698|0.687|0.117s|
| RRF |0.969|0.750|0.643|0.636|0.047s|

Carga/construcción inicial19.281s en esta ejecución. La primera carga exploratoria de recursos tuvo43.875s; condiciones de caché distintas, no benchmark comparativo. Los tiempos no tienen orden aleatorizado ni prueban capacidad concurrente. Volumen medio final3097/4530/3824 caracteres, respectivamente. Los JSON incluyen tiempo y volumen por caso y subtema, recall complementario y omisiones. `irrelevant_context_chars` se interpreta como caracteres fuera del oráculo, no como irrelevancia semántica demostrada.

El criterio prospectivo exige además mejora MRR≥0.05, recall no inferior y ninguna pérdida por subtema>0.25. Se aplica conservadoramente al contexto final, no solo a candidatos. **Q06 (medidas de rendimiento/portabilidad) pasa de1.0 a0.0 de recall final con denso y RRF**. Por eso ninguna se promueve, aunque mejoren medias. La interpretación inicial de candidatos sugería RRF; la comprobación final de contexto impidió adoptarlo. No se modificó el criterio ni se repitió el banco para aprobar.

C05/C06 devuelven vecinos sin respaldo para la pregunta en las tres ramas. La interfaz declara suficiencia no evaluada; no diagnostica fuera de temario ni inventa una respuesta. El baseline también falla definiciones/tipos naturales en español en el guion expuesto: no se ofrece como recuperador semántico satisfactorio. La entrega es infraestructura y evidencia negativa acotada, no éxito pedagógico.

## Pruebas y navegador

- [36 pruebas iniciales](tests-first.log): fragmentación/offsets/tablas, carga CPU/caché/offline, Chroma real con vectores sintéticos para identidad/rebuild, regresiones documentales v1.1/v2.
- [26 pruebas de entrega](tests-delivery.log), con nuevas negativas: fragmento ajeno con metadatos plausibles, retirada después de espera, consulta demasiado larga antes de encode y cierre durante recuperación que impide entrega tardía. No se suman las ejecuciones solapadas como62 casos distintos.
- [Contratos CPU reales finales](real-contracts-final.json), [log](real-contracts-final.log):117 páginas/207 fragmentos reconstruidos, todos los offsets/capacidades, CPU real, idempotencia sin avance de generación y rechazos de dimensión/pooling/límite/normalización/representación/fuentes/versiones antes de crear otro Chroma. No segunda pasada del banco; solo definición expuesta para verificar reapertura.
- [Black](black-final.log), [Ruff](ruff-final.log): seis archivos Python conformes. TypeScript y Vite build correctos; ESLint de Tecnica correcto. No instalaciones ni relajación de reglas.
- Navegador real IAB: definición, tipos, etnografía, original PDF4, ausencia/distractor, referente de prototipado y cambio a entrevistas, cierre/reentrada. Primero RRF durante la evaluación de promoción; después baseline final en8029, incluyendo Q06→Requisitos22. Evidencias `browser-*.txt`, [captura final](browser-final.png), [original](browser-original.png). Los rankings malos quedan registrados; no se encargó al usuario descubrirlos. Regreso a documental v1.1 comprobado en8031 sin sección de recuperación nueva.
- [385 archivos preservados](preservation.json), cero cambios/ausencias en paquetes v1/v2. Reserva, originales, cuarentena y presupuestos históricos intactos.

Errores conservados: Ruff inicial de líneas largas corregido antes del índice; primer arranque falló por concatenación del mensaje, corregida sin repetir ranking. Aviso tokenizer146>128 surge al contar candidatos de corte sin truncar; las207 entradas efectivamente codificadas se comprobaron≤128. Aviso Starlette/httpx previo permanece. Primer recibo de verificación comparaba todos los bytes Chroma y dio falso para esa igualdad; no probaba modificación lógica de identidad. El seguimiento verificó solo recibos/representación/puntero y generación constante. **El helper reutilizó por error el nombre del JSON inicial y lo sobrescribió**: se declara la pérdida; [primera observación reconstruida del output capturado](real-contracts-first-observation.json), logs separados y recibo final conservados. No se presenta como original íntegro. Banco/resultados no se sobrescribieron.

El arranque documental dentro del sandbox quedó bloqueado en `socket._fallback_socketpair`/`asyncio._make_self_pipe`, reproducido por faulthandler; no era fallo del corpus ni se resolvió cargando modelos. Arranque autorizado fuera del sandbox en8031 y navegador correctos. Una pestaña con error de timeout bloqueó su propia navegación a data:; se usó una pestaña limpia, sin eludir advertencias. Primer intento de parada propia falló al parsear fecha ya convertida por PowerShell; no detuvo nada ajeno. La comprobación final de propiedad/creación y parada figura en `cleanup.json`.

## Qué falta antes de conversar con el modelo

No se acredita evidencia suficiente para un ensayo generativo general. Faltan selección final que conserve referencias complementarias sin esta pérdida por subtema, tratamiento de equivalencias/continuidades y criterio independiente de suficiencia/ausencia/conflicto. Los candidatos RRF muestran que Q06 llega al conjunto pero se pierde al entregar contexto; eso identifica la carencia sin autorizar otra pasada. Para una conversación futura acotada, se podrá elegir un escenario con contexto fijo revisado y registrar el experimento, con autorización nueva; aquí no se conecta GenerationPort ni se sigue optimizando.

T077 global, T071/T072/T073/T074 y gates humanos conservan estado. T090/T150/G2/SC001, participantes, examen, voz y web durante sesiones no se abren. Autoestudio continúa antes que examen. Servicios propios detenidos al entregar, puerto8022 no intervenido. No continuación automática al generador.

## Reporte al coordinador bloqueado

El único intento de mensaje al chat01a14951-9510-70d0-85e5-25d51ab1b6ec, host local, fue rechazado por revisión automática: considera insuficientemente acreditada la autorización para compartir el informe con ese destinatario. No se envió el mensaje ni se eludió la decisión; se pidió confirmación humana expresa. T100 queda pendiente solo de ese reporte. Los artefactos locales y la parada de recursos están completados.

Actualización posterior: el usuario confirmó expresamente el envío. El resumen final con enlaces se entregó correctamente al coordinador indicado; T100 completada. El rechazo inicial queda registrado, sin elusión ni envío a otros chats. No se inicia trabajo generativo.
