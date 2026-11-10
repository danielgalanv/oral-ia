# Comprobación CPU antes de GPU — T210

03-11-2026. **No se detectan bloqueos mecánicos en las rutas y entradas comprobadas después de la corrección.** Se preparó realmente la interfaz e índice y se revisaron recursos y peticiones con el runtime instalado del worker. No se ejecutó generación/revisión real ni se inicializó CUDA. Esta comprobación no puede garantizar carga NF4, kernels, memoria libre, tiempos o calidad de futuras respuestas en GPU; T191 sigue abierta.

## Qué se comprobó

| Área | Evidencia CPU | Resultado y límite |
|---|---|---|
| Arrancador real | `study-chat.ps1 -PrepareOnly -NoBrowser -WebPolicy ...v2.json`; [log final](preparation-final.log) y [reutilización](reuse.log) | Compila y prepara sin servidor ni LLM. Reutiliza el recibo después de consultar una copia del índice, sin reconstrucción. |
| Índice y preguntas | [Consulta real](retrieval-check.json), embeddings en CPU, sin respuestas generadas | **12/12** preguntas aprobadas recuperan pasajes (cinco por caso). **207 fragmentos**, máximo **128 tokens**, límite del encoder **128**. Presencia de pasajes no demuestra suficiencia. |
| Runtime de GPU instalado | [Sonda CPU](resources-worker/runtime-probe.json) | Python de `D:\ai-toolkit\venv`: Torch 2.13.0+cu130, Transformers 5.5.3, Accelerate 1.15.0, bitsandbytes 0.50.2, safetensors/tokenizers presentes. Operación de tensor en **CPU** correcta; `cuda_initialized=false`. No se comprobó disponibilidad del dispositivo. |
| Checkpoints locales | [Cabeceras, índices y frames](resources-worker/models-and-frames.json) | 14B: **8 shards y 579 tensores**; Qwen3: **5 shards y 399 tensores**. Identidad de configuración, nombres, shapes, offsets, tamaño de cada shard y total declarados coherentes. No se cargaron tensores del modelo ni se hizo checksum de todo su contenido. |
| Biblioteca NF4 | [Compatibilidad estática](compatibility.json) | Existe `libbitsandbytes_cuda130.dll`, correspondiente al build CUDA instalado. Se registra hash; no se cargó/ejecutó su kernel ni se reserva VRAM. |
| Tokenización efectiva | [Comparación](compatibility.json) y frames | **11 peticiones** del recorrido web, generación y revisión; tokenización nativa directa y por render coinciden. También coinciden los resultados del entorno del proyecto y del worker. Máximo medido **5.078 tokens de entrada**, por debajo del límite actual **7.000**. No demuestra que toda pregunta/historial arbitrario quepa. |
| Orquestación del proveedor real | `test_gpu_transition_cpu.py` | Se usa **RealStudyProvider**, sus métodos de preparación, binding, lifespan y cierre; solo se sustituyen GPU/worker. Perfiles 14B/Qwen3, NF4, razonamiento, muestreo y presupuestos correctos. Dos workers cerrados en orden. |
| Revisión y reparación | Misma composición real con salidas deterministas | Generación → crítica válida → reparación con 14B → post-revisión → entrega del final. No se interpreta como mejora académica real. |
| Fallos | Pruebas de recursos, arranque, transporte, cancelación/recuperación y retirada existentes | Recursos insuficientes no crean workers. Si falla el arranque del crítico se cierra el generador propio. Sin cierre de procesos ajenos ni clasificación de fallo académico. |

La advertencia del tokenizer sobre una secuencia de 146 tokens aparece mientras la partición mide candidatos. Se comprobó directamente que **los fragmentos finales usados no superan 128**; no se declara que ese candidato de medición haya entrado al encoder sin partirse.

## Defecto encontrado y corregido

`WebControlRequest.effective_messages()` usaba `json.dumps` sin el escape de marcadores nativos que ya empleaban otros perfiles. Cadenas de pregunta/evidencia podían contener separadores de roles sin escapar aunque estuvieran dentro de JSON. Se reutiliza ahora `data_json`: conserva el valor al decodificar y evita introducir esos separadores como tokens de control.

[Prueba con el tokenizer real del worker](native-boundary-check.json): el serializador anterior reproducido sobre el mismo payload introduce **dos separadores extra**; el corregido introduce **cero**, conservando pregunta y evidencia. No es una garantía general frente a persuasión/inyección semántica; prueba específicamente el límite de datos y delimitadores de chat.

La preparación anterior a este cambio se conserva. Se creó una **nueva** después de la corrección y del formato final; no se repararon sus hashes ni se reutilizó un recibo obsoleto silenciosamente.

## Pruebas y transparencia

- [Suite de transición](pipeline-release.log): **90 aprobadas**, una optativa omitida y una advertencia existente Starlette/httpx. Incluye perfiles, adaptador/frames, razonamiento, API web/exportación, preparación y recuperación. La prueba optativa de preparación real no se habilitó en pytest; los comandos reales de preparación/reuso se ejecutaron por separado y están registrados.
- [Últimas dirigidas](last-tests.log): cinco casos aprobados después de limpiar imports; su ámbito se superpone con la suite anterior, no sumar como casos únicos.
- [Checks finales](final-checks-final.json): Ruff **10 existentes y 0 nuevos**, comparación estructural con multiplicidad. **308/140/22** archivos históricos conservan hashes, sin sumarlos como únicos. Black conforme; sin servicios propios nuevos activos. El puerto habitual estaba libre cuando se comprobó; no se reserva para un futuro arranque.
- [Fuentes finales](release-manifest-final.json) en `release-source-final`. El archivo inicial se conserva por separado; incluía dos imports de pruebas sin uso, eliminados antes de la comprobación final.

El primer test de delimitadores tenía un montaje incompleto de EvidenceItem; fue corregido. El primer doble del runtime usaba un nombre de adaptador no permitido, y la primera crítica simulada pedía cobertura sin el testigo exigido por ese contrato: activaba reintento de formato en vez de reparación. Se corrigieron los dobles sin debilitar validadores de producción. Sus logs se conservan; no se cuentan como fallos del modelo o como reparaciones académicas. La comparación nativa del serializador anterior/corregido reproduce directamente el defecto de delimitadores.

Los valores GPU de las pruebas de orquestación son **simulados**, no telemetría. La sonda del runtime hace únicamente una suma de tensor CPU y comprueba ausencia de inicialización CUDA. Los únicos pesos cargados fueron los del encoder de recuperación en CPU; no se cargó el generador o revisor en ningún dispositivo. No se hicieron descargas nuevas, migraciones, Reset o commits, y no se tocaron procesos ajenos. No se repitió navegador: la UI no cambió; la compilación actual es real y la evidencia de navegador del incremento anterior se conserva.

## Arranque preparado y guion vigente

La carpeta actual preparada y comprobada está en `prepared_run` de [retrieval-check.json](retrieval-check.json). Su `launch.json` selecciona `--study-chat --reviewed-provider`, política web v2, índice propio y modo sin cupo educativo. No inicia un runtime durante PrepareOnly. La consulta de las doce preguntas usa historial placeholder explícito: no contiene respuestas falsas ni se presenta como conversación generada.

El [guion vigente](guion-gpu.md) reutiliza las preguntas aprobadas y corrige una instrucción operativa obsoleta: **no debe bloquearse el envío al terminar las doce preguntas en el modo normal**. Los experimentos expresamente limitados son otro modo. El guion anterior y su aprobación se conservan sin reescribirlos.

Cuando se autorice GPU, usar esa preparación con `-PreparedRun` y el catálogo v2. Si vuelve a cambiar el código, la validación rechazará la preparación antigua y habrá que preparar otra. Antes de cargar, el runtime vuelve a comprobar recursos reales; estas comprobaciones CPU no los reservan.

**Conclusión:** hay preparación reutilizable y evidencia favorable de cableado, formatos, recursos locales, recuperación y limpieza. Lo que queda por confirmar exige ejecutar realmente la GPU: carga y generación NF4, comportamiento/latencia del revisor, continuidad con respuestas efectivas y calidad académica. No se aprueban por esta auditoría G2, SC001, aceptación docente, eficacia con estudiantes o publicación.
