# Chat de autoestudio: uso vigente

Actualizado 05-11-2026. Entrada `/estudio`, piloto docente local de requisitos de Ingeniería del Software. No puntúa ni aplica rúbricas. Voz y examen son fases posteriores. [Estado y siguiente trabajo](CONTINUAR.md) · [Instalación para desarrolladores](../CONTRIBUTING.md).

## Preparar sin GPU

Desde la raíz, con dependencias, paquete docente autorizado y encoder local disponibles:

```powershell
.\scripts\study-chat.ps1 -PrepareOnly -Offline -NoBrowser
```

Crea una carpeta propia bajo `.claude-scratch`: interfaz, índice de embeddings CPU y catálogo de conceptos candidatos. No carga modelos generativos, no descarga pesos ni inicia servidor. El recibo `oralia-study-preparation/v2` comprueba fuentes, código, entorno y artefactos. Preparaciones previas a v2 o alteradas deben prepararse de nuevo; no se reparan silenciosamente.

## Arrancar con GPU disponible

```powershell
.\scripts\study-chat.ps1
# Sin ampliación externa:
.\scripts\study-chat.ps1 -Offline
```

Por defecto (desde 06-11-2026): servicios llama.cpp locales — revisor Mistral-Small-24B :8089, generador Qwen2.5-14B :8090 — y servicio de ranking bge-m3 + reranker :8092; el lanzador los arranca con `scripts/llama-servers.ps1` (uno a uno; si el 24B arranca con la GPU llena pierde velocidad). La respuesta se muestra siempre con un aviso fijo si el revisor encuentra contradicción o concepto equivocado. Necesita ~30 GB de GPU libres. `-InProcess` conserva la ruta anterior: generador Qwen2.5-14B NF4 y revisor Qwen3-8B NF4 cargados en el proceso (configurar `ORALIA_CUDA_PYTHON` si el intérprete CUDA no está en la ruta histórica; el proveedor comprueba al menos 25.000 MiB libres). El lanzador no cierra aplicaciones ajenas; `scripts/llama-servers.ps1 stop` para los servicios propios. Ctrl+C detiene el servidor del chat, no los servicios llama.cpp.

El piloto selecciona alcance `web-control/v5`, generación `study-dialogue/v4` y revisión estable `web-review/v8`. `config/requirements-study-policy.json` habilita la ampliación externa de esta actividad; el runtime genérico no da permiso web por defecto. `-Offline` la desactiva conservando alcance. `-ActivityPolicy`/`-WebPolicy` permite una política explícita que incluya `activity_scope`.

La ampliación local primero/web restringida está conectada y se han medido recorridos reales, incluidas dos ampliaciones de unos 339 s. Eso no acredita fiabilidad académica universal y esos tiempos no son aceptables como objetivo de experiencia. Se muestran aviso y procedencia externa; no se usa todo Internet ni se deduce fuera de temario de la ausencia de pasajes.

## Reutilizar preparación

```powershell
.\scripts\study-chat.ps1 -PrepareOnly -NoBrowser -PreparedRun '<carpeta-creada>'
.\scripts\study-chat.ps1 -PreparedRun '<carpeta-creada>'
```

La primera orden valida sin cargar modelos; la segunda arranca. Cada lanzamiento usa una copia de trabajo nueva del índice para que Chroma no altere el template. Cambiar código, fuentes o entorno invalida preparaciones anteriores. No copiar una ruta de una evidencia antigua como si fuera un recurso compartido vigente.

## Funcionamiento y límites

- Preguntas libres, cambio de tema natural y palabras clave; no hay cupo académico de preguntas. `-ExperimentalLimits` sirve solo a ensayos acotados.
- El botón de envío confirma el turno; no reenviar automáticamente al recuperar conexión. El historial y los borradores tienen límites y expiración; no prometer memoria ilimitada ni recuperación después de caducar.
- El generador recibe las últimas tres interacciones. La vista puede mostrar más; no equivale a que el modelo las recuerde todas.
- Las fuentes autorizadas disponibles son nueve documentos y 117 pasajes. No representan toda la asignatura; tablas, gráficos y cuarentena mantienen limitaciones. INCOSE no se ha incorporado como corpus completo.
- Exportación JSON/Markdown al finalizar: registros descriptivos, no notas, rúbrica o prueba de aprendizaje. No se guarda audio. Las copias descargadas quedan bajo custodia del usuario.

- Revisor (06-11-2026): el chat usa el revisor compacto `concept-ledger/v5` en modo aviso (la respuesta se muestra siempre; un aviso fijo si hay contradicción, concepto confundido o atribución sin respaldo). Estado y mediciones en [CONTINUAR](CONTINUAR.md).
- Rechazos: «No he encontrado esa cuestión entre los temas…» (tema ajeno o no reconocido) y «El material… no trata esto» (primera pregunta sin pasajes relevantes: puntuación del reranker < 0,3).

## Evidencias y preparación del piloto

[Comparación del catálogo](audits/2026-11-04-prepared-concepts/report.md) · [ensayo integrado anterior](audits/2026-11-03-gpu-integrated/report.md) · [configuración y guion del piloto](STUDY-PILOT.md) · [registros descriptivos](piloto/README.md).

Las guías `MVP.md`, `DEMO.md` y las instaladoras 001–003 conservan demostradores históricos de otro alcance. No inferir de sus pruebas que la conversación generativa actual está aceptada para estudiantes. G2, SC001 y pendientes humanos de SpecKit no se cierran mediante esta guía.

## Registro de avisos y revisión docente

Con el arranque por defecto (llama.cpp), cada vez que el alumno ve un aviso (o la revisión falla y se muestra "no se ha podido revisar") se añade una línea a `registro-avisos/avisos.jsonl`: pregunta, respuesta, fuentes, tipo de aviso y lo que decía el revisor (unidad marcada y motivo, solo para el docente). Contiene las preguntas de los alumnos: queda en local. No se registran las respuestas sin aviso.

El docente evalúa los avisos en una página local, separada del chat de los alumnos (el registro tiene sus preguntas, por eso escucha solo en 127.0.0.1):

```powershell
.\.venv\Scripts\python.exe -m oralia.documentary.notice_review_app --port 8038
```

y abre `http://127.0.0.1:8038`: lista de pendientes con pregunta, respuesta, lo que señaló el revisor y las fuentes; botones Acierto / Falsa alarma / Dudoso y nota opcional; pestañas Pendientes / Evaluados / Todos y recuento arriba. También se puede por línea de comandos con `scripts/avisos_docente.py`:

```powershell
.\.venv\Scripts\python.exe scripts\avisos_docente.py pendientes
.\.venv\Scripts\python.exe scripts\avisos_docente.py ver <id>
.\.venv\Scripts\python.exe scripts\avisos_docente.py marcar <id> acierto|falsa_alarma|dudoso "nota opcional"
.\.venv\Scripts\python.exe scripts\avisos_docente.py resumen
```

`acierto` = el aviso estaba justificado; `falsa_alarma` = la respuesta era correcta; `dudoso` = no se puede decir. Las marcas van a `registro-avisos/etiquetas.jsonl`. Con ellas se mide cuántos avisos son falsas alarmas por tipo y se decide qué ajustar. La primera versión no registra las respuestas sin aviso, así que no mide errores no detectados.
