# Transporte corregido y comparación GPU de revisores

## Resultado

Se corrigió un defecto de transporte real. Ninguno de los dos candidatos supera la
calibración de desarrollo; no se promueve revisor ni se abre publicación. No se
consume una reserva nueva ni se ejecuta T180 sin satisfacer su condición previa.

El adaptador antes enviaba mensajes registrados de WebRoundRequest, mientras el
worker reconstruía solo el renderer estructurado genérico. Se reproducen nueve
fallos antes de corregirlo. Ahora ambos validan la misma versión/política,
metadatos de fuentes e historial; el recibo confirma versión, recordatorio y SHA256
de los mensajes. Se rechazan confirmaciones ausentes, alteradas o con hash ajeno.
No se acepta un fallback a instrucciones genéricas.

## Cambios

- src/oralia/course_dialogue/web_review_frame.py: reconstrucción tipada, sin iniciar
  aplicación, servicios, bases de datos, red ni otro modelo.
- model_prompt_profiles.py, cached_transformers.py y gpu_worker.py: transporte y
  confirmación del renderer; las rutas genéricas históricas conservan su contrato.
- tests/course_dialogue/test_web_review_gpu_frames.py: positivos generate/review/
  repair y negativos de versión, hash, fuente, historial y recordatorio.

La comprobación standalone del Python CUDA valida veinte frames sin importar torch
ni iniciar servicios. La llamada GPU real confirma además el perfil y la huella.
Esto acredita transporte, no implicación semántica ni calidad del revisor.

## Medición real

Protocolo, código, entradas, localizaciones y oráculo se congelaron separados antes
de inferir. El modelo no recibe las etiquetas esperadas. Ocho llamadas, cuatro por
candidato, todas completas; 290,844 segundos desde el inicio del runner. No hubo
reintentos ni reajustes durante el ensayo. Máximo 768 tokens y 180 segundos por
llamada, total permitido ocho llamadas/2400 segundos.

| Candidato | Contrato válido | Ejemplos válidos aceptados | Errores centrales detectados | Revisiones enteras utilizables |
|---|---:|---:|---:|---:|
| Qwen2.5-7B NF4, greedy | 2/4 | 0/2 | 1/2 | 0/4 |
| Qwen3-8B NF4, nonthinking | 2/4 | 1/2 | 1/2 | 1/4 |

El 7B rechaza ambos ejemplos ficticios y, en D06, pide detalles de medición en vez
de detectar la atribución falsa de 3:1 a texto normal. No se cuenta como acierto por
emitir issues_found. El 8B acepta D03, pero rechaza también el umbral ficticio 5:1 y
acepta D06. En D04 detecta parte del error, pero confunde la postura del borrador
con la fuente docente. Fuentes docente y externa no discrepan en ese caso.

La mejora parcial de un caso no supera la selección preregistrada; T180 no se
inicia. Las explicaciones falsas siguen siendo fallos aunque su JSON sea válido;
los errores de contrato no convierten automáticamente toda observación en falsa.
[Preguntas, respuestas, salidas y pasajes completos](transcript-full.md).

Qwen3 usa enable_thinking=False y el sampler registrado 0,7/0,8/top_k20/min_p0,
con seed42, siguiendo la [ficha oficial](https://huggingface.co/Qwen/Qwen3-8B#best-practices).
No se comparan tiempos con los ensayos CPU previos: cambian checkpoint/perfil,
cuantización y entorno, y hay modelos ajenos residentes. La muestra es pequeña,
expuesta y no ciega; no prueba que ningún modelo o estrategia pueda funcionar.

## Recursos y ejecución

La GPU mostraba unos 21 GiB ocupados y 11 GiB libres, con baja utilización antes de
cada carga. Se conservaron Dolphin y ComfyUI. Solo se cargó un modelo propio por
vez. Los recibos worker-cleanup.json acreditan la parada de ambos árboles propios;
la memoria volvió aproximadamente a su estado inicial. Recursos y rendimiento se
clasifican resource-inconclusive por contexto ajeno residente, sin atribuirle los
fallos académicos. No hubo descarga de modelos, red nueva, Reset ni commits.

Los primeros lanzamientos restringidos no llegaron a crear el marcador ni a llamar
al modelo; se interrumpieron y se ejecutó el mismo código por la vía autorizada.
La búsqueda inicial de test_structured_requests.py usó un nombre inexistente; no
es una prueba pasada. Se corrigió a los archivos reales.

## Verificación

- 15 pruebas nuevas de frames; la regresión focal compartida suma 88 aprobadas.
- Módulo course_dialogue completo: 544 aprobadas, un aviso previo de Starlette.
- Black: seis archivos conformes. Ruff src/tests/scripts: diez hallazgos previos,
  cero nuevos, comparación de ruta/código/mensaje con multiplicidad. Una pasada
  ruff sobre todo el árbol incluye copias históricas y no es el baseline habitual;
  se conserva separada y no se presenta como chequeo de producción limpio.
- Coinciden 308 hashes durables, 140 de expedientes anteriores y 22 de fuentes/banco.
- Ejecutables y prompts congelados se conservan en executed-code y manifest.

## Decisión y pendientes

T178 completa corrección y verificación de transporte. T179 completa esta
comparación y decide no promover. T180, T168/T169/T175 siguen abiertos: no hay
revisión/corrección automática fiable ni transferencia nueva satisfactoria. Los
candidatos no dan permiso para publicar y no se sustituye al tutor por respuestas
académicas predefinidas.

Se detiene esta línea de cambiar solo checkpoint/sampler con v6. Antes de otro
ensayo procede una hipótesis distinta y comprobable: reducir decisiones redundantes
que hoy permiten status/issues/action contradictorios, y separar en el análisis la
propuesta hipotética de una atribución documental y la postura del profesor de la
del borrador. El host puede derivar una acción mecánica de un veredicto consistente;
no puede inferir verdad académica de esa derivación. Cualquier sucesor requiere
contrato optativo, negativos CPU, congelado y casos nuevos; no reajustar estos cuatro
para declararlos una transferencia. No se afirma que se hayan agotado todas las
mejoras posibles ni que Feature012 esté terminada.


Continuación separada: la hipótesis de veredicto único se implementó y midió después,
con su propio congelado y presupuesto. [Resultado v7](../2026-10-31-minimal-review-successor/report.md): mejora parcial 3/4, sin promoción. No reescribe los resultados v6 de este expediente.
