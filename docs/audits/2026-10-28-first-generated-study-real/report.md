# E1 real: ocho turnos completos, con errores de contenido conservados

28 de octubre de2026. **Ejecutadas8/8 preguntas reales y1 calentamiento** con Qwen2.5-14B-Instruct NF4 local, recuperación densa real v2.1 y encoder CPU. Todas terminaron `stop`, se mostraron completas en consola diagnóstica y entraron en el historial de esa superficie. No hubo truncamientos ni preguntas repetidas. **Esto acredita el recorrido técnico, no la corrección del tutor:** A3 contiene una inversión de significado y B1 mezcla validez con estructura/calidad. E2 no se anuncia lista como demo correcta.

[Transcripción íntegra](transcript-full.md) · [Versión móvil estática](transcript-mobile.html) · [Contexto/historial íntegros](context-and-history-full.md) · [Revisión por turno contra originales](review-by-turn.md) · [Guion docente y E2 pendiente](teacher-review-guide.md) · [Métricas](metrics.json).

## Autorización, presupuesto y primer fallo

La nueva orden humana autorizó GPU/LLM real para este objetivo. [Recibo de autorización](authorization.json). El [protocolo50s congelado](../2026-10-27-generated-study-cpu/protocol-v2-50s.json) conserva su texto/estado histórico de preparación CPU; la autorización del28-10 permite ejecutarlo sin reescribir retroactivamente ese archivo. Una candidata,8preguntas+1calentamiento,768tokens nuevos,50.000ms por petición y20min globales. Sin nueva campaña, fallback, prompt ajustado tras ver resultados o reserva histórica.

Primer intento exclusivo `capture-001-37a6c2`: comprobación vigente503/32607MiB,0 %. Falló **mecánicamente** el límite de preparación90s del proveedor. El encoder CPU había cargado y el worker llegó a cargar pesos locales, pero no emitió disponibilidad. No se alcanzó el marcador `weights_loaded`, que precede al calentamiento en el worker;0preguntas/0calentamientos. [Consola y traceback](capture-001-console.log), [contador](capture-001-37a6c2/count.json), [stderr](capture-001-37a6c2/worker-stderr.log), [limpieza](capture-001-37a6c2/worker-cleanup.json). No se toma como fracaso semántico.

Corrección mínima y prospectiva: parámetro explícito `preparation_seconds` en `cached_provider`, default90 intacto, techo180; solo la recuperación mecánica pide180. No cambia50s de generación,768tokens, fuente, modelo o prompt. El runner solo admite recuperar este caso si no hubo preguntas, no hay `worker.json`, no se alcanzó el marcador previo al warmup y el árbol propio está detenido. Usa el **monotonic original**, no reinicia20min. [Congelación de recuperación](mechanical-recovery-freeze.json), [presupuesto efectivo](capture-002-8b31f4/preparation-budget.json), [39 pruebas CPU iniciales](preparation-tests.log).

Segundo intento exclusivo `capture-002-8b31f4`: preflight nuevo517MiB/0 %, worker listo en40,062s, calentamiento interno de1token y8preguntas. No se repitió ninguna pregunta del primer intento porque no se había enviado ninguna. Tiempo desde primer muestreo hasta último, **incluyendo fallo, corrección/pruebas y recuperación:473,813s (7min53,813s)**, inferior a20min. Recuperación228,907s. Presupuesto total consumido:8peticiones académicas y1calentamiento, sin ampliación de cupo. Tras agotarlo no se inició ensayo interactivo, pregunta extra o modelo nuevo.

## Configuración y evidencia efectiva

El flujo ejecutado es el preparado en CPU: `Retrieval(build=False)` del paquete v2→rama densa experimental→pasajes completos registrados→`LabGenerationRequest`→`CachedTransformersGenerationAdapter`/GenerationPort→worker propio por pipes→bruto/finish_reason→inspección de consola unverified→confirmación→historial. La captura es experimento offline, **no sesión humana realizada ni prueba de navegación del usuario**.

- Modelo/snapshot efectivo: Qwen2.5-14B-Instruct `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`;29.540.134.000bytes de shards originales. Runtime ya instalado `D:\ai-toolkit\venv\Scripts\python.exe`; torch2.13.0+cu130, transformers5.5.3; GPU RTX5090.
- Cuantización efectiva registrada: bitsandbytes4bit NF4, double quant, cómputo bfloat16; `is_quantized=true`, parámetro representativo en `cuda:0`. Huella modelo9.721.981.440bytes, distinta de la memoria GPU total medida. [Identidad/plantilla/configuración](capture-002-8b31f4/worker.json). Hash de plantilla aplicada `2e2d2512cfe46af53dc1eed45368ecaab26ac4461c480e6b69fe571cf0ceaa75`.
- Worker usa `do_sample=False` explícito. La advertencia sobre temperature/top_p/top_k del generation_config original se conserva; el campo informativo `temperature=0` del adaptador no prueba una reescritura de ese config. No se ajustó muestreo ni prompt entre turnos.
- Recuperación v2.1 CPU:117 unidades disponibles,207 fragmentos acreditados; fingerprint `c2756d3c78fd3dd9237b5a6aaa5fe63513a38747bf8894635bdb9e44143cf51a`, índice2 existente. Denso solo candidata experimental, baseline léxico y decisión negativa histórica intactos.20fragmentos candidatos, hasta5páginas completas y6000caracteres, sin páginas seleccionadas manualmente por pregunta.
- Cada JSON de [captura2](capture-002-8b31f4/) conserva consulta, escenario, referentes/historial, candidatos, pasajes/omisiones, petición al puerto, bruto, intercambio del adaptador, tokens/latencia/terminación, candidata mostrada y reconocimiento de historial. La consola completa está en [capture-002-console.log](capture-002-console.log). Las salidas no se corrigieron para el transcripto.

## Resultados por turno

| Turno | Tokens entrada/salida | Generación | Historial previo | Revisión técnica de contenido |
|---|---:|---:|---:|---|
| A1 definición |1467/267|17,594s|0mensajes|Núcleo servicios/restricciones correcto; apertura estrecha y proceso adicional innecesario. |
| A2 tipos |1679/185|12,250s|2|Parcial: funcional/no funcional; omite integración/dominio ya recibidos. Otro eje solo aparece mencionado en el contexto, sin definición. |
| A3 aclaración |1908/381|24,906s|4|Error sustantivo al decir que no funcionales «impiden» cumplir características; distingue en buena parte los dos ejes. |
| A4 ejemplo |2330/516|32,516s|6|Hipótesis coherente y útil; valores2s/1000consultas permitidos como ficción. Desliz al hablar de sistema como «cómo se implementará». |
| B1 validación |2156/278|18,531s|0|Lista mayormente trazable, pero fusiona validez con estructura/calidad y omite alineación con necesidades pese a recibirla. |
| B2 aclaración |2159/405|25,750s|2|Continúa desde B1, con repetición y error «Trasladables» por trazabilidad; formulación demasiado categórica de garantía. |
| B3 cambio |1776/635|39,016s|0|Cambia correctamente de tema. Núcleo trazable; primer rótulo puede adelantar indebidamente decisión, aunque después la sitúa tras análisis. Ámbito NASA identificado. |
| B4 ausencia |1965/68|4,750s|0|No inventa contraseña ni excluye tema del curso; reconoce que no está en fuentes suministradas. |

8/8`stop`,8/8mostrados completos,0`length`,0`deadline`.2735tokens nuevos totales. Media21,914s, mediana21,719s, rango4,750–39,016s; suma175,313s. Son latencias observadas de esta muestra y entorno, **no SLA, comparación de modelos o tasa de calidad**. No se calcula porcentaje general de acierto con estos ocho casos.

## Contexto, continuidad y causas

[Comprobación de recibos](receipt-consistency.json): todas las cadenas de historia coinciden exactamente con texto previamente mostrado; A1→A2→A3→A4 con0/2/4/6mensajes. B1nuevo episodio; B2incluye B1; B3cambio explícito sin historia; B4control independiente sin historia. Sin continuidad inventada, entrega tardía o salida completa fabricada a partir de un truncamiento. La continuidad técnica no evita que el modelo herede/reitere contenido defectuoso.

Primer fallo académico parcial: A2cobertura. Primera afirmación claramente falsa: A3. Requisitos86 estaba en su contexto y el original dice restricciones sobre sistema/proceso; la inversión no se explica por pérdida de recuperación, tabla o GPU. B1 recibió Procedimiento10 y NASA71: la fusión de «Correcta/estructura» con validez es un problema de interpretación/síntesis con distinción de ámbitos disponible, aunque la documentación del curso ya conserva diferencias terminológicas. B2 conserva esa limitación y añade el rótulo incorrecto.

Pérdidas registradas: B1omite NASA208 por empaquetado de página completa; B2omite NASA70. B3entrega3páginas/5715caracteres y registra14eventos de omisión para11IDs únicos; no14páginas diferentes. Ni estas omisiones ni las ausencias del ranking se atribuyen a formato tabular. A3recibió la definición que altera; B1recibió necesidades de stakeholders aun sin NASA208. Tablas/figuras siguen limitación aceptada; no se declara fiable toda la información estructurada ni se ocultan errores textuales bajo ese aviso.

La revisión leyó los pasajes efectivos y contrastó los originales locales mediante renders, incluidos Requisitos7/11/15/76/83/86/89, Procedimiento6/10/11 y NASA71/143/145/208, con páginaPDF frente a impresa diferenciadas. La [revisión por turno](review-by-turn.md) conserva afirmación, apoyo y matiz. Ejemplos ficticios no se penalizan por no ser literales: se revisa principio/conclusión, no cada cifra inventada.

## GPU, propiedad y limpieza

Antes del primer intento503/32607MiB,0 %; después de su limpieza517MiB,0 %. Preflight del segundo517MiB,0 %.77muestras del primero y112del segundo, aproximadamente cada2s, más medidas explícitas; registros en `gpu-before.json`/`gpu-samples.json` de cada carpeta. Pico de la recuperación15.620MiB y99 %; final517MiB/0 %. [Propiedad durante trabajo](worker-during.json), [limpieza1](capture-001-37a6c2/worker-cleanup.json), [limpieza2](capture-002-8b31f4/worker-cleanup.json).

Worker1 árbol54872/43172/54712: detenido por timeout, con identidades/create_time registradas. Worker2árbol90012/89740/67800: salida0 y todo el árbol propio detenido. No se detuvo ComfyUI, documental8022 ni otro proceso ajeno. No hubo servidor propio en esta ejecución; pipes sin listener. Las muestras agregadas no demuestran ausencia absoluta de toda concurrencia WDDM, pero no se observó una nueva presión ajena que explique los errores; no se les atribuye causa GPU. No se consumió GPU después de la captura para otra hipótesis/campaña.

## Cambios y pruebas

Únicos cambios de ejecución: `cached_transformers.py` añade límite de preparación explícito90por defecto/180máximo; `run_prepared_study_trial.py` añade recuperación mecánica segura con reloj global preservado. No cambia `gpu_worker.py`, `study_lab.py`, GenerationPort, prompt, corpus, ranking o parámetros académicos. Test de credenciales prepara90/180con proceso doble; nuevo `test_study_preparation_recovery.py` prueba cero cupo renovado, rechazo ante uso académico/warmup incierto/árbol vivo y límites inválidos antes de abrir runtime. Copias anteriores en `before/`.

[69 pruebas CPU finales](tests-final.log) correctas en6,65s; incluyen recuperación, adaptador/presupuesto, composición y entrega, observabilidad y propiedad worker. Ruff/Black correctos. Una advertencia Starlette/httpx preexistente y warnings de tokenizer/flags del modelo conservados, sin instalar nada para silenciarlos. Sin cambios frontend: no se repite build/UIfixture como si validara la calidad real ni se usa fixture para acreditar estas respuestas. [Preservación](preservation.json): solo cambian los dos archivos mecánicos indicados; protocolo, worker, composición, manifiesto v2, identidad, fragmentos y versión de índice intactos. Los originales siguen validados por sus hashes.

## Estado y siguiente decisión

**Implementado:** cableado previo y corrección mínima de preparación. **Verificado:** captura real de8turnos, recuperación/historial/terminación y revisión técnica contra fuentes. **Disponible:** evidencia íntegra para revisión docente desde móvil. **No probado por usuario / no aceptado:** contenido, navegación E2 y eficacia. E1completo como medición con resultados negativos/localizados; no tutor aprobado ni feature cerrada.

No anunciar E2lista: el mínimo incluye el fallo sustantivo A3. El [guion](teacher-review-guide.md) permite revisar la captura sin LLM ni localhost móvil y documenta una futura prueba con la superficie autorizada de inspección. Esa UI se probó anteriormente con fixture; esta ejecución real fue consola. No se confunden ambas pruebas con un recorrido real E2. No hay generador/servidor activo para que el usuario envíe consultas ahora; las8llamadas están consumidas.

Siguiente cambio propuesto, sin ejecutar: obligaciones de conservar el sentido de restricciones y separar clasificación/destinatario/nivel y validez/calidad, con contraste de significado/cobertura frente a fuentes antes de ofrecer contenido como tutor. No se afirma que una instrucción extra resuelva el problema ni se inicia otro verificador/modelo. El docente/coordinador puede revisar primero estos errores y decidir una corrección acotada y presupuesto nuevo; no se ajusta este ensayo hasta hacerlo aprobar.

T090/T150/G2/SC001/participante permanecen cerrados; T077global no completado. `unverified` no pasa a `supported`, suficiencia `not_assessed`, publicationfalse en los ocho recibos. Sin examen, voz, notas, rúbricas, participantes, nuevas instalaciones/checkpoints, nube, reindexación habitual, commits/Reset/migraciones o reserva. Tras el único reporte final autorizado al coordinador termina este alcance.

Reporte único de esta continuación enviado correctamente al coordinador `01a14951-9510-70d0-85e5-25d51ab1b6ec`, host local. [Estado final](final-status.json): cero procesos de ensayo propios restantes, ambos árboles detenidos y ningún servidor iniciado. No se envían otros mensajes ni se ejecutan más inferencias.
