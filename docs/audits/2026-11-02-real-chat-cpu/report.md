# Chat integrado con modelos reales en CPU

Se ejecutó un ensayo real sin GPU: documentos autorizados, índice aislado, navegador `/estudio`, Qwen2.5-14B y Qwen3-8B-thinking locales. **No se obtuvo una respuesta completa dentro del plazo actual.** No se presenta como prueba aprobada ni como fallo académico.

## Qué se ejecutó

- PyTorch `2.13.0+cpu`, sin build CUDA, con `CUDA_VISIBLE_DEVICES` vacío; sin descargas ni proveedor remoto.
- Snapshots ya instalados: 14B `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8` y Qwen3 `b968826d9c46dd6066d109eabc6255188de91218`. Se conservan perfiles de prompt, plantillas nativas, muestreo y semilla.
- Un derivado de laboratorio del worker usa CPU float32 y SDPA, sin NF4; no modifica el proveedor de producción. **No equivale numéricamente al despliegue GPU NF4.** La [derivación](derivation.json), [scripts congelados](frozen-sha256.json) y copias de los scripts exactos en `trial-frozen-source` conservan los cambios.
- Los dos modelos cargaron y completaron su calentamiento de un token: [generador](run-1793648114273368900/generator/ready.json), 27,81 s y unos 59,08 GB de parámetros/buffers; [revisor](run-1793648114273368900/reviewer/ready.json), 15,61 s y unos 32,76 GB. Ambos confirman dispositivo CPU, float32 y cuatro hilos de PyTorch.
- Recuperación real sobre un índice nuevo en la carpeta de ejecución, con el perfil comparativo ya existente. No se usaron respuestas ni evaluadores simulados.
- Dos preguntas del banco aprobado como máximo; parada ante la primera no entregada. [Protocolo](run-1793648114273368900/protocol.json).

## Resultado observado

Pregunta A1:

> ¿Qué es un requisito de software y cuáles son sus principales tipos? Explícamelo con un ejemplo sencillo.

El navegador inició la petición. Al alcanzar el límite de **180 segundos por etapa**, la llamada fue cancelada sin recibirse una salida completa del worker. La interfaz resolvió la espera en 181,78 s mostrando:

> No he podido completar una respuesta revisada. Puedes precisar la pregunta o intentarlo más tarde.

No hubo texto académico entregado, dictamen del revisor ni reparación. A2 quedó sin ejecutar. La cuota registra una pregunta y una llamada académica iniciada; los dos calentamientos se registran aparte y no son respuestas a preguntas. No se conoce el número de tokens que el generador pudo calcular antes de cancelarse: no se recibió un frame final.

La [conversación](run-1793648114273368900/conversation.json), [captura móvil](run-1793648114273368900/A1.png), [petición íntegra con fuentes](run-1793648114273368900/generator/request-01.json), [transporte cancelado](run-1793648114273368900/generator/transport-01.json) y [log](execution.log) conservan lo observado. No hubo errores JavaScript ni peticiones externas del navegador.

El checkpoint de revisión de sesión quedó vacío al cerrarse la sesión; no se inventa una traza de revisión. Las peticiones y el transporte del adaptador se guardaron antes del cierre. Un intento de leer telemetría desde el sandbox no pudo ver los procesos; la lectura posterior fuera de esa restricción confirmó CPU y memoria de los workers propios.

## Qué implica y qué falta

El resultado demuestra que estos checkpoints **se pueden cargar en CPU** y que el recorrido integrado llega al generador real. No demuestra que el generador sea incapaz de responder correctamente, que CPU sea inviable con otros presupuestos, ni que el revisor falle: no llegó a ejecutarse.

El límite actual de 180 segundos se valida en `RepairGenerationConstraints`, `validate_budget_frame` y `WebReviewRounds`, además de la sesión integrada y el adaptador. No existe un perfil temporal CPU ampliado registrado. El ensayo no eliminó ni parcheó esas barreras para aparentar que cumplía el contrato normal. Antes de repetir para completar la respuesta en CPU haría falta un perfil optativo con plazo mayor, pruebas de propagación y cancelación y límites globales explícitos. Tampoco basta aumentar tokens: aquí el obstáculo observado es temporal.

T198 completa el ensayo acotado, **no la validación conversacional**. T191 y Feature 012 permanecen abiertas. Los modelos y los controles de calidad del chat normal no se sustituyen por otros más pequeños ni por fixtures.

## Preservación y cierre

No cambió producción, corpus, prompts de producto, modelos, gates o datos habituales. Los grupos históricos de 308, 140 y 22 archivos conservan sus hashes, y el worker original GPU mantiene su hash.

El [cierre](run-1793648114273368900/closed.json), la [limpieza del generador](run-1793648114273368900/generator/cleanup.json), la [limpieza del revisor](run-1793648114273368900/reviewer/cleanup.json) y las [comprobaciones finales](final-checks.json) registran procesos propios detenidos y puerto 8053 libre. No se detuvieron procesos ajenos, no se consultó ni usó la GPU y no hubo Reset ni commits.

Sintaxis Python/JavaScript comprobada antes de ejecutar. Los scripts finales pasan Black y Ruff; los cambios posteriores fueron de estilo/imports y una variable de memoria no utilizada. Los scripts exactos ejecutados siguen preservados y no se repitió la inferencia tras observar el resultado.
