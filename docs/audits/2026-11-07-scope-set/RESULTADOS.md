# Conjunto de alcance del docente: 60 preguntas (07-11-2026)

60 preguntas de estudio redactadas por el docente (6 grupos de 10: conceptos, tipos, obtención y análisis, especificación y calidad, modelado/trazabilidad/gestión, verificación/validación y situaciones reales). Todas están dentro del alcance. Pasadas una a una por el chat real (paquete v3, 4 huecos) con `run_set.py`; resultados en `resultados-final.json`.

## Resultado del filtro (versión final)
- **Respondidas 59 de 60**; la única rechazada es la 46 (MoSCoW), que el docente confirmó como rechazo correcto («el material no lo trata»).
- **Rechazos de alcance indebidos: 0 de 60** (el filtro de alcance no rechazó ninguna pregunta válida).
- **Dos fallos encontrados con estas preguntas y corregidos:**
  1. Puerta de relevancia demasiado estricta: con el umbral 0,3 rechazó 4 preguntas como «el material no trata esto»; el docente dijo que 3 (#16 requisitos legales, #23 entrevista individual o conjunta, #45 priorizar con poco presupuesto) debían responderse. Umbral bajado a 0,1 (la 46 puntúa 0,04; las ajenas y ambiguas, menos de 0,07).
  2. Detector de referencias (`chat_context.referential`): «…¿cómo clasificaríamos **ese** requisito?» (#19) se tomó por un seguimiento y pidió aclaración. Ahora «ese requisito/ese ejemplo…» solo cuenta si la pregunta es corta (≤ 10 palabras).
- **Aviso falso del revisor** en la #14: el ejemplo hipotético «AES 256» se tomó por una norma sin respaldo. La regla de atribución ahora exige que el designador lo emita un organismo de normalización (ISO, IEC, IEEE, ANSI, RFC, NIST, UNE, EN, DO, ITU, CMMI, PMBOK, SWEBOK).

## Calidad de las respuestas (etiquetas del docente sobre las dos dudosas)
- #16 (legales, protección de datos): respuesta aceptable pese a que el material no trata el tema (menciona «Ley GDPR» y dice «según la fuente» cuando no hay fuente sobre requisitos legales): **mostrar tal cual**.
- #19 (Windows y Linux): clasificación incoherente (no funcional «y de integración», luego «de dominio»): **debía llevar aviso**; el revisor no avisó. Es un fallo real de cobertura del revisor, sin resolver.
- Avisos del revisor en las 60 respuestas finales: 1 (falso, el de la #14, ya corregido).

## Incidencia de infraestructura
La primera pasada tuvo 10 y la segunda 8 respuestas caducadas (límite de 180 s), todas distintas: el servidor del 14B arrancó degradado (13 tok/s en vez de 120, parte de las capas fuera de la GPU) sin avisar. Con servidores sanos y 2 a la vez, las 15 afectadas se respondieron. `scripts/llama-servers.ps1` mide ahora la velocidad al arrancar y avisa si baja de 40 tok/s (resultado correcto hoy: revisor 85, generador 120). Aun con servidores sanos, 2–3 sesiones a la vez dieron 49 s por turno de media (primer texto a 12 s) frente a ~10 s de un alumno solo: la GPU se comparte con otros procesos del equipo.

## Conjunto de 30 (grupos 1-6, borrador validado por el docente; paquete v2, servidores sanos 87/120 tok/s)
Script `run_alcance.py` (con latido de conexión: sin él el servidor cierra la sesión a los 15 s y salen falsos «permiso caducado»); resultados en `resultados-alcance.json`.
- Grupo 1 (directas) 5/5, grupo 2 (seguimientos) 5/5, grupo 3 (comprobar comprensión) 5/5, grupo 5 (fuera de alcance, incluida la inyección de instrucciones) 5/5.
- Grupo 6 (límite) 4/5: la pregunta compuesta «¿Qué es un requisito? y de paso recomiéndame novelas» se rechazó entera (esperaba responder la parte de la asignatura).
- Grupo 4 (tema de la asignatura que el material no trata) 1/5: Kano y QFD se rechazan como «fuera de los temas» (no con «el material no lo trata»); Volere sí da «el material no trata esto»; **DOORS y puntos de función reciben una respuesta genérica del modelo, no del material** (DOORS aparece una vez como ejemplo de herramienta en NASA SWE-055; puntos de función no aparece). Hallazgo de contenido: cuando la pregunta toca un concepto cercano al alcance, la puerta de relevancia (0,1) no la frena y el generador responde con conocimiento propio. Una regla por nombres propios ausentes del material no lo arreglaría (DOORS sí está) y daría falsas alarmas (Linux en la 19). Pendiente de decidir si hace falta un freno en el generador/revisor.
- Un aviso (comprobar comprensión «requisito no funcional = lo que hace el sistema»): `wrong_concept`; la respuesta corrige al alumno y el aviso es discutible. Para evaluar con la página de avisos.

## Intento de cerrar el fallo del grupo 4 (no integrado)
1. **Instrucción en el prompt del generador** («si las fuentes no desarrollan lo pedido, di que el material no lo cubre»): sin efecto. El 14B sigue respondiendo DOORS y puntos de función con conocimiento propio (grupo 4: 1/5, igual que antes).
2. **Control `gap` (14B, GBNF, ya registrado) en la primera pregunta de la sesión**: grupo 4 sube a 4/5 (DOORS, puntos de función, Volere detectados; Kano sigue como rechazo de alcance) pero **rechaza 11 de las 59 preguntas válidas del docente** (≈19 %: #6, 7, 15, 16, 18, 19, 22, 23, 38, 42, 57; la 46, MoSCoW, era el rechazo correcto) y 2 del conjunto de 30. Descartado: peor que el fallo que corrige. Código y cambio de prompt revertidos.
Siguientes ideas, sin probar: que lo decida el revisor 24B con los pasajes (más caro y con riesgo similar) o un aviso del revisor cuando la mayoría de las afirmaciones no tengan respaldo en los pasajes; pedir al docente las preguntas de este tipo que más le preocupen antes de invertir más.
Nota operativa: con `-Slots 4` el generador arrancó degradado (12 tok/s) en 4 de 6 intentos tras reinicios; con `-Slots 3` arrancó bien las dos veces. Conviene `-Slots 3` como valor por defecto si se repite.

## Pregunta compuesta y ranking propio (07-11-2026)
- `StudyWebFlow.admit_local`: si el juez de alcance da `outside` y la pregunta tiene varias partes (separadas por `?`, «y de paso», «además», «por cierto»), cada parte se juzga por separado; se responde solo la parte dentro del alcance y la respuesta empieza con «Solo he respondido a la parte de tu mensaje que trata de la asignatura.». Conjunto de 30: grupo 6 pasa de 4/5 a 5/5 y el grupo 5 (fuera de alcance, inyección) se mantiene en 5/5.
- Ranking: `scripts/llama-servers.ps1` usa `.venv-ranker` (torch 2.13.0+cu130, transformers 5.22.2; ignorado por git) y solo cae a `D:\ai-toolkit` si no existe. Arranca y el conjunto de 30 da los mismos resultados.

## Segunda vía para el grupo 4: el revisor 24B decide la cobertura (sonda, no integrada)
`probe_cobertura.py`: se pasan pregunta + pasajes recuperados al 24B (temperatura 0, una palabra: SI / PARCIAL / NO).
- Grupo 4: NO en Puntos de función, Volere, Kano y QFD; **DOORS sale PARCIAL** (el material lo menciona como ejemplo de herramienta), así que 4 de 5.
- Las 60 preguntas del docente: NO en 7 (#6, 17, 18, 23, 32, 40 y la 46, que era el rechazo correcto) → **6 falsas alarmas de 59 (≈10 %)**, la mitad que el control 14B (19 %) pero aún demasiado para usarlo como rechazo.
- La relevancia numérica del recuperador no separa: puntos de función sale 0,59 y varias preguntas válidas del docente 0,13-0,29.

## Aviso suave de cobertura (implementado, sin medir en vivo)
Decisión del docente (07-11-2026): en vez de rechazar, la respuesta sale igual con el aviso fijo «Esta respuesta puede incluir contenido que el material de la asignatura no desarrolla.» cuando el revisor 24B dice NO sobre pregunta + pasajes (`coverage_check.py`, `LlamaStudyProvider.coverage`, `build_notice(trace, extra)`). Solo preguntas de 6 o más palabras (las cortas dependen del historial); si el revisor no responde, no hay aviso; queda en el registro de avisos para que el docente lo evalúe. Probado con tests unitarios (616 pasan); **falta medirlo con el chat completo** (esperado: aviso en ~4 de 5 del grupo 4 y en ~10 % de las 60 válidas).
Hallazgo operativo: en la última sesión la GPU tenía 20 GB ocupados por procesos ajenos al proyecto (ComfyUI y otro llama-server de `D:\ComfyUIModels`), por eso el generador arrancó degradado (12 tok/s) en 5 de 8 arranques; sin esos 20 GB el sistema no cabe. Para la clase hace falta GPU libre (ya anotado como B1).

### Medición en vivo del aviso de cobertura (GPU libre, v3, 4 huecos, servidores 89/118 tok/s)
- Grupo 4: aviso `coverage` en QFD (#17) y puntos de función (#20); Volere (#19) sigue dando «el material no trata esto» y Kano (#16) rechazo de alcance; **DOORS (#18) sigue sin aviso** (el material lo menciona). Es decir, 4 de 5 con algún freno, en la misma línea que la sonda.
- Las 60 válidas: 59 respondidas y 1 «material no cubierto» (la 46, correcta); **aviso `coverage` en 8 de 59 (≈14 %)**: #6, 19, 20, 23, 32, 35, 40, 42 (la sonda daba 6; el aviso va junto a una respuesta que se muestra igual). Ningún otro aviso en las 60.
- Conjunto de 30: grupos 1, 2, 3, 5 y 6 sin rechazos indebidos; un aviso `coverage` en un seguimiento («no lo entiendo, ¿puedes explicarlo más fácil?», #9) → ajustado: solo se comprueba la cobertura en la primera pregunta de la sesión (los seguimientos llevan su tema en el historial). Un `wrong_concept` en la #12 (comprobación de comprensión), a evaluar en la página de avisos.

### Ajuste del aviso de cobertura (variantes sobre pasajes en caché)
`probe_cobertura2.py` (11 negativos: 5 del docente + 6 del asistente sobre Jira, ISO 29148, UML, CMMI, puntos de caso de uso, COCOMO; 59 positivos del docente):
| variante | negativos detectados | falsas alarmas |
|---|---|---|
| A: una palabra SI/PARCIAL/NO (la anterior) | 7/11 | 4/59 |
| B: citar la frase que responde (NINGUNA) | 10/11 | **33/59** (descartada) |
| C: elemento central DESARROLLA/AUSENTE | 4/11 | 0/59 |
| **A o C** (adoptada) | **8/11** | 4/59 |
Las falsas alarmas de A son casos defendibles (p. ej. el material no trae un ejemplo desarrollado de casos de uso frente a estados, ni una comparación rendimiento/disponibilidad/fiabilidad).
En vivo (GPU libre): las 60 válidas dan aviso `coverage` en 5/59 (#19, 23, 32, 40, 42; antes 8); grupo 4: QFD y Kano rechazo de alcance, Volere «no trata esto», puntos de función con aviso, DOORS sin freno (el material lo menciona). Conjunto de 30 sin rechazos indebidos. Aparecen además `wrong_concept` en #24 y #33 de las 60 y en #11 y #12 del conjunto de 30: a evaluar en la página de avisos.

## Etiquetas del docente sobre los 4 avisos `wrong_concept` (07-11-2026)
| caso | pregunta | etiqueta |
|---|---|---|
| 60 #24 | requisitos contradictorios de dos usuarios | dudoso |
| 60 #33 | requisito mal redactado y reescrito | falsa alarma |
| 30 #11 | «requisito no funcional = lo que hace el sistema» (comprobar comprensión) | falsa alarma |
| 30 #12 | «validar = comprobar que está bien programado» (comprobar comprensión) | falsa alarma |
0 aciertos de 4. En los dos casos de comprobación de comprensión la respuesta corrige al alumno y repite su error para refutarlo; hipótesis: el revisor toma esa repetición por una afirmación de la respuesta.

### Intentos de reducir los falsos `wrong_concept`
Motivos del revisor en #11 y #12 (leídos del registro): dice que la respuesta «atribuye a los no funcionales la definición de los funcionales» y que «confunde la validación con la verificación», cuando la respuesta afirma justo lo contrario: **cita la idea del alumno para refutarla y el 24B la toma por afirmación de la respuesta**.
1. Regla en la política del revisor («si la respuesta cita una idea para negarla no la atribuye»): sin efecto sobre #11 y #12.
2. Segunda lectura del 24B del hallazgo (`probe_confirmacion.py`): separa las dos falsas alarmas (NIEGA) pero también descarta 2 de 3 errores reales construidos a mano: descartada.
3. **Regla determinista adoptada** (`review_notice.drop_corrections`): si la pregunta es una comprobación de comprensión («creo que…», «entiendo que…», «¿voy bien?», «¿es correcto?», «¿es así?»…) y el hallazgo de concepto/contradicción cae en una unidad con marcas de corrección («no se limita», «sino», «confundiendo», «no es»…), no se muestra como aviso (sí queda en el registro). Efecto en vivo: #11 y #12 del conjunto de 30 dejan de avisar.
Persiste ruido: en la última pasada salió `wrong_concept` en #33 (etiquetada falsa alarma) y en el seguimiento #9 del conjunto de 30; el revisor da 1-3 `wrong_concept` por cada 90 respuestas y cambian de una pasada a otra. **Con 4 etiquetas del docente: 0 aciertos, 3 falsas alarmas, 1 dudoso.**

## Conversaciones encadenadas (60 preguntas del docente en 6 sesiones de 10, 6 alumnos a la vez, GPU libre)
`run_conversacion.py`. Cada pregunta ve las anteriores de su sesión.
| historial que reciben generador y revisor | respuestas | fallos | segundos por turno (media / p95) |
|---|---|---|---|
| últimas 3 parejas pregunta-respuesta (antes) | 40/60 | **20 `transport_error`** | 51,3 / 79,2 |
| **solo la pareja anterior** (nuevo valor por defecto, `ORALIA_HISTORY_TURNS=1`) | **60/60** | 0 | **40,9 / 64,9** |
Causa de los fallos: el servidor del revisor (24B) se queda sin caché KV («failed to find a memory slot for batch») cuando coinciden varias peticiones largas (historial de 3 respuestas de ~700 tokens + pasajes + borrador); afecta a las posiciones 5-10 de cada conversación. Es un fallo que no se veía con preguntas sueltas.
Avisos con historial de 1: `wrong_concept` en #25 y #26; los motivos del revisor son absurdos («atribuye a la elicitación la definición de "estudio ético"», «a "sanidad"…», «a los requisitos de usuario características de los de sistema»): confunde tarjetas de su propio catálogo de conceptos. Pendiente de etiquetar; probable falsa alarma (con las 4 anteriores: 0 aciertos).
Limitación vista: en conversación la puerta de relevancia y el aviso de cobertura no actúan (solo en la primera pregunta), por eso la 46 (MoSCoW, que el material no trata) se respondió en vez de rechazarse.

## Puerta de relevancia y aviso de cobertura en toda la conversación (07-11-2026)
Cambio: `study_lab.self_contained`: la relevancia (umbral 0,1) y la comprobación de cobertura se aplican a la primera pregunta y a cualquier pregunta posterior que se recupere por sí sola (modo `current_question`) y tenga 8 o más palabras; los seguimientos y las preguntas cortas siguen exentos. `reviewed_study` usa la presencia de `retrieval_relevance` como condición de ambas.
Medición (6 conversaciones de 10 con las 60 del docente, historial de 1 pareja): 59 respondidas y la 46 (MoSCoW) rechazada con «el material no trata esto» (antes se respondía); **0 rechazos indebidos**; 5 avisos `coverage` (#19, 23, 32, 40, 42, los mismos de antes), 1 `wrong_concept` (#12) y 1 `attribution` (#58, sin evaluar). 48,7 s de media por turno (p95 77 s). Conjunto de 30: sin cambios (grupo 2, seguimientos, 5/5; grupos 1, 3, 5 y 6 sin rechazos indebidos; grupo 4 como antes).

## Etiquetas del docente en conversación (07-11-2026)
| caso | aviso | etiqueta |
|---|---|---|
| 60 #12 (robot en 30 s: ¿funcional, rendimiento o ambos?) | wrong_concept | **acierto** |
| 60 #58 (requisitos verificables en una IA no determinista; cita «normas ISO 27001») | attribution | **acierto** |
Acumulado `wrong_concept` etiquetado: 1 acierto, 3 falsas alarmas, 1 dudoso (5 casos). `attribution`: 1 acierto de 1. Primeros aciertos reales del revisor; la lectura del asistente de la #12 («respuesta correcta») era errónea, lo que apoya no desactivar el aviso hasta tener más datos.
