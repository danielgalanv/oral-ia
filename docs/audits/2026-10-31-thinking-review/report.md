# Qwen3-8B con razonamiento conectado y medido

Continuación completada el 1 de noviembre de 2026. El directorio conserva la fecha
del primer inicio de implementación; no cambia fechas ni resultados anteriores.

## Resultado

El perfil qwen3-8b-thinking está conectado al adaptador, al worker y al bucle de
revisión. Se ejecutaron cinco revisiones reales completas de las mismas cinco
respuestas generadas por Qwen2.5-14B en el ensayo anterior, sin alterarlas ni añadir
mis objeciones. Todas devolvieron no_issues_found, como el modo sin razonamiento.
**No se activó ninguna corrección y no hay mejora de calidad demostrada en esta muestra.**

La conclusión excesiva localizada de G04, señalada en el contraste técnico anterior,
continúa sin objeción automática. No se convierte esta observación en una tasa
universal ni en una invalidación de toda la respuesta: su núcleo sigue siendo
adecuado. Tampoco se suman controles negativos preparados como errores del generador.

[Preguntas, respuestas y dictámenes para móvil](transcript-mobile.html) ·
[Transcripción Markdown](transcript-final.md) · [Comparación y recibos](comparison.json).

## Configuración comprobada

Mismo checkpoint Qwen3-8B local fijado, modo nativo enable_thinking=True, NF4,
seed42 y muestreo específico 0,6/0,95/top_k20/min_p0, siguiendo la
[ficha oficial de Qwen](https://huggingface.co/Qwen/Qwen3-8B#best-practices).
Modo, muestreo y plantilla se confirman en los recibos; no se aplica greedy a las
revisiones. El calentamiento histórico genera un token greedy descartado, sin
historial ni semilla persistentes; su aviso de parámetros no describe el muestreo
de las revisiones reales, que se verifica por separado.

La plantilla real deja al modelo generar el bloque de razonamiento en modo True;
solo añade un bloque vacío cerrado cuando el modo es False. Una aserción CPU inicial
presuponía un prefijo abierto y falló antes de usar GPU. Se preservó el diagnóstico
y se corrigió la comprobación, sin cambiar el prompt académico. El primer script
se formateó mientras esperaba imports: sus números de línea de traceback corresponden
al formato previo. La repetición nativa pasa para las cinco preguntas en ambos modos,
con mensajes idénticos y tokenización directa/reconstruida coincidente.

Capacidad review-thinking/v1: hasta 8192 tokens totales, incluido razonamiento y
final, y 180 segundos por llamada; habilitación explícita del proveedor y petición
tipada solo de revisión. Generación/reparación conservan su máximo anterior de 2.048.
Un cierre ausente o final vacío no es un dictamen utilizable, aunque termine en EOS.
Las salidas con length/deadline siguen siendo incompletas. No se permite usar ese
presupuesto en generación, reparación ni decoder finito. El modo anterior y los
defaults históricos permanecen; la selección del nuevo modo es explícita, no una
activación de participantes o sustitución silenciosa de configuraciones anteriores.

El worker decodifica solo el canal final. Del tramo anterior se guardan recuentos y
SHA256 de los IDs de salida, nunca contenido interno en el dictamen ni en el
historial del alumno. La existencia de tokens de razonamiento no acredita verdad.

## Ensayo y comparación

| Caso | Sin razonamiento | Con razonamiento | Tokens anteriores al final, incluidos marcadores |
|---|---|---|---:|
| G01 definición/tipos | Sin objeciones | Sin objeciones | 295 |
| G02 rendimiento hipotético | Sin objeciones | Sin objeciones | 284 |
| G03 comprobable/realista | Sin objeciones | Sin objeciones | 318 |
| G04 trazabilidad | Sin objeciones | Sin objeciones | 304 |
| G05 control técnico W3C | Sin objeciones | Sin objeciones | 354 |

Cinco llamadas nuevas, cero generaciones iniciales nuevas, cero reparaciones.
1615 tokens de salida totales: 1.555 del tramo previo y 60 del dictamen final. Ninguna
llamada agotó tokens o tiempo. El runner terminó en 232,734 s, incluyendo 107,609 s de
preparación registrada del worker. No se usa este tiempo para ranking: hubo contextos
ajenos y variación de recursos; no se les atribuye el contenido de los dictámenes.
También cambia el sampler recomendado entre modos, por lo que no se aísla una causa
única. Las cinco respuestas son conocidas y no constituyen una reserva nueva.

Se conservan pregunta, evidencia y borrador generado exactos. El protocolo fijaba
máximo 35 llamadas / 2.400 s, dos correcciones y un recordatorio formal. El corrector 14B
se carga solo si hay una objeción: no se cargó, al no cumplirse esa condición. El
recorrido correctivo tiene pruebas CPU, pero no se acredita eficacia real de rondas.
No se incorporaron críticas del coordinador ni etiquetas esperadas a los mensajes.

## Código y validación

- model_prompt_profiles.py registra checkpoint/modo/sampler; qwen_thinking.py separa
  canales y valida confirmación; thinking_review_request.py tipa capacidad solo de revisión.
- generation_limits.py, cached_transformers.py y gpu_worker.py aplican el presupuesto
  y flags en ambos extremos, con versión/huella del renderer web confirmadas.
- review_repair.py y web_review_rounds.py construyen y revalidan la petición ampliada,
  dejando las reparaciones en el generador y sin autorizar publicación.
- 18 pruebas nuevas: modo y sampler, negativos de capacidad/tarea, marcador ausente,
  salida incompleta y confirmación alterada, además de conexión al bucle.
- Regresión final: **589 pruebas del módulo aprobadas**, un aviso previo de Starlette.
  La primera regresión y los focales se conservan por separado y no se suman como
  pruebas independientes. Black conforme; baseline Ruff en closeout.json.

## Estado y conservación

T184 completa conexión y comparación del perfil, no acredita al evaluador semántico.
T182 y los pendientes semánticos conservan su estado: no hubo reparación activada
ni publicación. Queda disponible Qwen3 con razonamiento como selección explícita
para los siguientes ensayos; no se declara mejor por haberlo activado.

Fuentes, reservas y expedientes históricos se verifican mediante hashes. No se descargaron modelos ni se modificaron bases habituales; no hubo Reset ni commits. El proceso ComfyUI encontrado
no se detuvo; se usó el margen disponible con preflight estable. El árbol del worker
propio quedó parado y la lectura final fue 0 % de utilización, 2.205 MiB usados y 29.983 MiB
libres. No se detienen procesos del escritorio para liberar esos contextos.


Durante el cierre se detectó un ID de tarea compartido con otro dossier ya existente.
Solo se renumeró la tarea nueva de este perfil, conservando la otra entrega y sus
estados. No se cambió código ni resultados del experimento por esa corrección.
