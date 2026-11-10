# Corrección localizada del autoestudio — 29 de octubre de 2026

## Cambio aplicado

Se modifica la selección comparativa optativa y el perfil de conversación que ya usa Qwen 14B. No se incorporan respuestas académicas predefinidas ni excepciones por identificador de documento o pregunta.

- `src/oralia/documentary/comparison_coverage.py`: una pregunta interrogativa explícita con contenido propio deja de heredar automáticamente las facetas de una comparación anterior. Para comparar conceptos, se priorizan encabezados centrados en el concepto y páginas que declaran su objetivo, frente a menciones incidentales, técnicas o listas especializadas. Se sigue seleccionando únicamente entre candidatas recuperadas, con los mismos límites; no se afirma suficiencia semántica por ranking.
- `src/oralia/course_dialogue/model_prompt_profiles.py`: el historial conserva referentes, pero no se convierte en autoridad académica. Se pide fundamentar comparaciones en la finalidad documentada, y contestar una pregunta práctica indicando una acción y un resultado observable, en vez de repetir cualidades de redacción. Se permiten premisas hipotéticas coherentes.
- `tests/unit/test_comparison_coverage.py`: dos regresiones nuevas, sobre conceptos distintos de los expuestos, fallaron antes del cambio y pasan después. Cubren prioridad del objetivo y no heredar comparaciones ante una nueva pregunta práctica.

## Comprobación CPU

68 pruebas aprobadas en la primera corrección y **69 en la versión final**, tras añadir la comparación sin «entre»: selección, representación, petición estructurada, perfil conversacional, proveedor, límites e historial/entrega. Black y Ruff correctos en los tres archivos modificados. Una advertencia de deprecación de Starlette, sin fallo. Los primeros intentos dentro del entorno restringido encontraron limitaciones de temporales/procesos; la ejecución válida se realizó fuera de ese entorno. Comandos y resultados iniciales en `cpu-validation.txt`.

La primera consulta real conserva como primeras páginas Procedimiento 10 y 12: ambas estaban en las veinte candidatas originales, pero antes se priorizaban Procedimiento 11 y Requisitos 74. Se mantienen intactos los textos y las fuentes. `retrieval-preflight.json` conserva las páginas completas y las omisiones.

## Ensayo real y revisión

Se ejecuta la composición `DiagnosticStudy` directamente con el recuperador real y Qwen2.5-14B NF4. El wrapper generativo usa el mismo `structured_request` y el mismo perfil que el proveedor docente; no se simulan respuestas. Se conservan pregunta exacta, petición, mensajes efectivos, fuentes, texto bruto, preview, resultado y tiempos en cada `turn-XX.json`.

Es una prueba de integración diagnóstica, **no una nueva prueba de navegador**. El ACK se realiza en el harness para reutilizar exactamente el texto recibido; no representa aceptación humana. El presupuesto independiente es de ocho llamadas: seis preguntas originales y dos variantes nuevas; el límite de seis llamadas del servidor público de diagnóstico no se modifica. No hay reintentos ni correcciones automáticas ocultas. Modelo, cuantización, semilla, decodificación greedy y presupuesto de 2048 tokens/180 segundos permanecen iguales al ensayo anterior.

La valoración considera si la respuesta contesta y es académicamente aceptable al nivel introductorio solicitado. Una lista repetida o una respuesta larga no son por sí mismas errores. No se exige un protocolo exhaustivo de pruebas para aceptar un ejemplo sencillo.

Revisión de los seis primeros turnos:

1. Correcta en la distinción principal: verificar calidad; validar correspondencia con necesidades reales y aprobación de clientes/usuarios. Desaparece la dicotomía individual/conjunto.
2. Ejemplo aceptable de citas médicas que aplica esa distinción. Sus escenarios y funcionalidades son hipótesis, no requisitos acreditados de un proyecto real.
3. Mantiene correctamente esa distinción y el referente. **Conserva un error localizado**: escribe «Complejidad» para describir que se cubren todos los aspectos necesarios; debería denominarlo completitud. No se cuenta como respuesta enteramente libre de errores ni se rechaza todo su contenido por ese término.
4. Mejora concreta: propone simular una reserva y observar una confirmación. Responde al nivel básico solicitado, aunque incluye mucha explicación general y no constituye un caso de prueba exhaustivo. No se exige que trate concurrencia, doble reserva o todas las excepciones para aceptar esa ilustración.
5. Distinción realizable/comprobable aceptable; ejemplo hipotético de transacciones. La referencia al producto final es una simplificación que no significa que nunca puedan diseñarse pruebas antes.
6. Ejemplo hipotético aceptable: experiencia de usuario «excepcionalmente fluida», difícil de comprobar sin concretar qué significa y cómo medirlo. No se rechazan las cifras inventadas de su propuesta de mejora por no aparecer literalmente en los documentos.

Las ocho respuestas de esta fase terminaron con `stop`, sin truncamiento. La variante 8, guardar una factura, propone introducirla, guardarla, comprobar datos y volver a consultarla: respuesta práctica aceptable. La variante 7 volvió a presentar la dicotomía individual/conjunto. La inspección mostró un fallo concreto de reconocimiento: «¿En qué se diferencian…?» no activaba la selección comparativa, que reconocía «entre». Se conserva íntegro ese primer fallo; no se cuenta como transferencia superada.

## Segunda corrección y regresión acotada

Se reconoce de forma general «se diferencian A y B» y se añade una regresión con alfa/beta, sin contenidos del curso ni IDs documentales. Se refuerza además la conservación de los nombres de atributos de las fuentes, sin proporcionar definiciones académicas preparadas.

`recheck/` conserva tres regresiones expuestas, no una reserva nueva. La primera vuelve a preguntar la variante 7 desde contexto vacío; la segunda repite la aclaración 3 con las dos respuestas reales previas; la tercera repite la pregunta práctica 4 con las tres respuestas previas. El historial se reconstruye explícitamente de recibos reales: no se presenta como una segunda conversación continua completa ni como uso de navegador.

La comparación 7 recibe ahora Procedimiento 10 y 12 y explica correctamente calidad de la especificación frente a correspondencia con necesidades de clientes/usuarios. Se corrige el fallo observado en la primera variante. La aclaración 3 conserva esa diferencia, pero **vuelve a denominar «Complejidad» a la cobertura de funcionalidades**: la instrucción general sobre denominaciones no ha corregido ese error localizado. No se declara resuelto ni se vuelve a generar indefinidamente.

La repetición 4 ofrece ahora una prueba concreta: seleccionar fecha/hora disponibles, introducir datos, confirmar y observar la cita en el calendario del paciente y en el sistema de la clínica. Es una respuesta práctica aceptable para el ejemplo hipotético. No se exige que resuelva todas las variantes de una aplicación real para considerarla útil.

**Resultado final:** 11 llamadas académicas completas (ocho iniciales y tres regresiones expuestas), todas con fin `stop`; 69 pruebas CPU aprobadas. Los dos fallos principales observados —distinción individual/conjunto y falta de comprobación concreta— quedan corregidos en los casos reejecutados. Sigue abierto el error de denominación de la aclaración. No se presenta un 11/11 de corrección semántica ni se afirma que las ocho preguntas se hayan vuelto a pasar bajo los bytes finales.

Las transcripciones mantienen separadas ambas fases: [primeras ocho respuestas](transcript-mobile.html) y [tres regresiones finales](recheck/transcript-mobile.html). No se construye una conversación artificial combinando respuestas de ejecuciones distintas.

Las conclusiones se limitan a la muestra observada. No se presenta como validez general del tutor ni como aceptación docente.

## Procedencia y conservación

Los originales del paquete v2 y los recibos/transcriptos del ensayo anterior se comparan mediante hashes antes y después. Se reutiliza el índice aislado del ensayo anterior porque no cambia la representación, los documentos ni `retrieval.py`; no se reescribe su identidad ni se reconstruye. Esta consulta no acredita el arranque con el índice histórico anterior, cuya discrepancia de identidad ya estaba documentada.

Durante la primera ejecución, Black envolvió una línea del módulo de comparación que el proceso ya había importado. `comparison-executed.py` reconstruye los bytes importados y coincide con el hash previo; `comparison-first-formatted.py` y `format-accounting.json` verifican igualdad del AST con el archivo reformateado de esa fase. La corrección posterior del parser es distinta y sus archivos exactos están copiados en `recheck/`. No se atribuye una nueva ejecución a bytes distintos sin documentarlo.

No hay servidor público en este ensayo, cambios de datos habituales, Reset, commits, descargas ni apertura a participantes. El worker se cierra al terminar y conserva su recibo de propiedad y limpieza. La revisión de estas respuestas es técnica, no una evaluación de estudiantes.

La comparación de preservación confirmó **318 archivos sin cambios** (paquete v2 y recibos/documentos seleccionados del ensayo anterior). Las ocho respuestas de la primera fase también conservaron sus hashes tras la segunda. Ambos árboles propios terminaron con código 0 y recibo `owned_tree_stopped: true`. Medición final: 1323 MiB y 0 % de uso de GPU. No se detuvieron servicios ajenos.
