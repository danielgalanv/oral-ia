# Revisión independiente del primer ensayo completo de chat A/B/C

24 de octubre de 2026. Revisión de sistema realizada por el asistente auditor; no es revisión docente, aceptación humana de diálogos ni validación de aprendizaje. La voz queda fuera del bloque actual.

## Rectificación de interpretación: GPU compartida

Después de la primera revisión, el usuario confirmó que está utilizando la GPU con ComfyUI y exigió comprobar su uso antes de inferir. ORALIA no tiene exclusividad de la GPU ni prioridad sobre ese trabajo. Debió evaluarse la disponibilidad antes del ensayo, no solo después de observar la ralentización.

Los deadlines conservados siguen describiendo lo ocurrido, pero **no puntúan como fallos del modelo, de la estrategia pedagógica o de la arquitectura** cuando hay contención detectada o no se acreditan condiciones comparables. Su clasificación de rendimiento es **no concluyente por recursos compartidos/no controlados**. Las salidas truncadas siguen sin ser respuestas autorizables; esa protección no implica un juicio negativo de capacidad. Las observaciones sobre el contenido de respuestas completas son una dimensión separada.

Los tiempos del diagnóstico posterior tampoco acreditan rendimiento exclusivo ni estable mientras la GPU esté compartida. Antes de nuevos ensayos se comprobarán procesos, actividad y memoria; se registrarán condiciones durante y después. Si no hay disponibilidad adecuada, se aplaza la inferencia y se continúa trabajo sin GPU. No se detiene ComfyUI, no se exige al usuario dejar de usarlo y no se amplía el timeout para maquillar resultados. Se preservan los paquetes originales y esta rectificación añade su interpretación, sin reescribirlos.

## Evidencia inspeccionada

Se leyeron íntegramente los ocho turnos de cada variante en `specs/012-conversational-course-study/evidence/chat-comparison-extended-first/`, incluyendo entradas reales, texto mostrado, candidatas brutas, errores, referencias y parámetros. También se inspeccionaron las páginas del corpus, protocolo, recibo del worker y copias de código del ensayo.

El protocolo corresponde a una conversación de desarrollo, una repetición por variante, con el mismo Qwen3-8B local/NF4 y `enable_thinking=false`. No es reserva ni acredita el requisito de tres ejecuciones por caso de G2. A usa además unidades authored; B/C usan generación directa sobre las páginas suministradas. Esa diferencia impide atribuir causalidad pura de arquitectura a cualquier mejora.

| Variante | Turnos | Candidatas mostradas sin error de contrato/terminación | Resultado |
|---|---:|---:|---|
| A, selector y renderer existentes | 8 | 8 | Varios fallos de pertinencia y continuidad; producir texto no equivale a contestar |
| B, documental | 8 | 6 | Mejora observable en corrección y cambio de foco; dos rechazos de contrato y problemas pedagógicos |
| C, pedagógica | 8 | 1 | Un rechazo de contrato y seis deadlines; muestra insuficiente para evaluar su conversación pedagógica |

Las cantidades anteriores describen integridad de salida, no tasas de éxito didáctico.

## A: problemas de contenido confirmados

- Turnos 1–2: la diferencia entre calidad documental y correspondencia con necesidades resulta útil, pero se repiten ejemplo y pregunta pese a la incomprensión.
- Turno 3: ante una duda explícita sobre validación/verificación devuelve una aclaración genérica sobre el concepto a tratar.
- Turno 5: no corrige directamente «validar equivale únicamente a pasar tests»; vuelve al bloque anterior.
- Turno 6: no responde a la rectificación y a cómo contrastar necesidades; pide otra aclaración genérica.
- Turnos 7–8: no define caso de prueba ni aclara la relación entrada/resultado; deriva a otro eje o pide aclaración genérica.

A no acredita SC001 en esta conversación, aunque haya generado ocho previews con fuentes.

## B: mejora parcial, con fallos concretos

- Turno 5: rechaza explícitamente que validar requisitos sea solo comprobar tests.
- Turno 6: aporta reuniones y prototipado para contrastar necesidades, operaciones presentes en el material.
- Turnos 7–8: responde al cambio de tema y ofrece una explicación de entradas, resultado esperado y comparación con el resultado obtenido. El ejemplo numérico es una derivación ilustrativa, no una cita de las diapositivas; la fundamentación detallada sigue pendiente.
- Turnos 2–3: el contrato rechaza listas de siete y ocho referencias frente al máximo de cuatro. Eso es un fallo de cumplimiento del formato, no una demostración de incapacidad conceptual.
- Turno 4: menciona supuestos de un sistema de biblioteca, pero no desarrolla el ejemplo concreto solicitado.
- El campo `question` reproduce entradas del alumno y alimenta el referente del siguiente paso; no es una buena pregunta de comprensión.
- `assumptions` presenta definiciones como supuestos. El aviso «No se incluyen referencias a pruebas de software…» persiste incluso al hablar de pruebas: el límite queda desactualizado.

B tampoco acredita conversación completa. La mejora localizada justifica estudiar esa ruta, pero no publicarla ni seleccionar todavía una ganadora.

## C: separar ejecución y pedagogía

El primer turno ofrece una distinción similar a B, con enumeración larga, supuestos que son definiciones y una pregunta que repite la entrada del usuario. El segundo se rechaza por exceso de referencias. Los seis restantes no producen candidatas completas antes del plazo.

En B se observaron 252–370 tokens de salida por turno, aproximadamente en 15–22 segundos. En C, desde el tercer turno, la salida cae a 138 y después 29–32 tokens en aproximadamente 30 segundos. El orden fue A, B y C con un worker; faltan observaciones suficientes de recursos por turno para explicar el cambio de rendimiento. No se puede concluir que la instrucción pedagógica cause la ralentización ni que C sea conceptualmente peor. Tampoco corresponde evaluar su raw truncado como enseñanza mostrada.

## Procedencia y operación

Se verificaron las 14 entradas de código incluidas en `source-before.zip` contra los hashes del manifiesto: ninguna discrepancia en esas copias. El archivo también contiene `protocol.json`. Esto verifica esas entradas, no que la lista cubra todas las dependencias transitivas del programa.

El recibo declara parada del árbol propio, tres identidades de proceso y código de salida 0. No se ha recertificado la integridad de todos los datos habituales desde esta revisión.

El piloto anterior, `chat-comparison-first`, queda separado. Sus B/C incluían `<think>` antes del JSON; esa configuración consumió tokens y provocó rechazos de formato. Esos fallos no prueban falta de capacidad docente y no se han reescrito como éxitos.

## Consecuencia para la implementación

Mantener la publicación cerrada y conservar los primeros resultados. Completar las correcciones de historial/contexto, probar los presupuestos y el contrato compacto y registrar su validación. Los siguientes ensayos deben congelar cambios nuevos, distinguir recuperación operativa de respuesta docente y conservar controles de límite documental. La integración en API/T090 exige un contrato de derivación autorizado: esta revisión no lo concede.

La conclusión es una mejora parcial observada en B, con fallos que siguen impidiendo una conversación aceptable; no una validación general del rediseño ni de los modelos locales.
