# Reducción de falsas alarmas del revisor 24B (07-11-2026)

Mistral-Small-24B, sin razonamiento, esquema JSON, T=0,15; casos etiquetados v1 (49+4) y réplica v2. `compare.py` compara por mayoría de semillas.

## Diagnóstico
- Las falsas alarmas del 24B (0,17) son deterministas: 4 de 8 casos "correctos según el docente" se marcan en 18/18 semillas. Son intercambios de conceptos vecinos o de títulos de lista (criterios docentes 5, 6, 12), que el modelo clasificaba como `wrong_concept`.
- Votos 2 de 3: sin efecto (falsas alarmas 0,211 frente a 0,210 por pasada, simulado con las 18 semillas). El error es sistemático, no aleatorio.
- Segunda opinión del 14B (aviso solo si ambos coinciden): baja la detección a la del 14B (0,40) sin mejorar sobre la política aclarada.
- Verificación de cita: no implementada; las alarmas restantes citan fuentes reales, así que no las quitaría.

## Cambio adoptado (general, sin reglas por tema)
En `COMPACT_POLICY`: `wrong_concept` = atribuir a un concepto las características de otro de naturaleza distinta; `related_concept` = intercambiar o mezclar conceptos hermanos (misma lista, clasificación o categoría de las fuentes), con desempate hacia `related_concept`; `label` = etiqueta inexacta con contenido correcto. `related_concept` y `label` no avisan (el servidor decide).

## Resultado (mayoría de 9 semillas en v1; 3 en v2)
| | detecta | falsas alarmas | v2: avisos en respuestas desconocidas | v2: detecta inyectadas |
|---|---|---|---|---|
| antes | 0,733 | 0,167 (0,203 por pasada) | 0,019 | 0,64 |
| política aclarada | 0,733 | 0,125 (0,144 por pasada) | 0,014 | 0,53 (12 casos; ≈1 caso) |

Quedan sistemáticos: `INJ_concept_N_GOOD` (3/3) e `INJ_title_REG_FIXED` (2/3). Sin cambio en tiempos (~5–6 s/caso). La política se ajustó mirando estos mismos casos: confirmar con casos nuevos del docente.

## Lote de etiquetado v3 (docente, 24 casos; 2 excluidos)
Etiquetas en `labeling-batch/etiquetas-docente.json`; clave del revisor en `clave-revisor.json` (24B, política actual, semilla 11). Excluidos por el docente: caso 7 (error inyectado mal construido) y caso 23 (pregunta no relacionada con la asignatura). El docente corrigió el caso 17 a M. Sobre los 22 válidos (4 M, 18 P):

| | avisa | no avisa |
|---|---|---|
| docente M (4: casos 1, 2, 17, 24) | 4 | 0 |
| docente P (18) | 5 (casos 10, 14, 15, 18, 21) | 13 |

- Cobertura 4/4; falsas alarmas 5/18. El lote está sesgado: 10 de los 24 casos se eligieron por haber sido marcados a menudo por el revisor, así que la tasa real es menor (~2 % en las 215 respuestas de la réplica).
- Los 4 casos M son antónimos inyectados por el generador de casos de prueba ("excluye", "idénticas", "roles idénticos"), no errores espontáneos del chat. El docente valora el nivel de las respuestas reales como muy bueno: el problema práctico son las falsas alarmas.
- Las 5 alarmas sobre P son sistemáticas (marcadas en 6–18 de 18 semillas antiguas), casi todas en preguntas "diferencia entre X e Y": razonamiento confuso o autocontradictorio ("lo cual es correcto, pero…", caso 15) o papel mal atribuido a un concepto (10, 14, 18, 21).

## Segundo pase de verificación sobre las unidades marcadas (`verify_pass.py`)
Cada unidad que el primer pase marca con aviso se revisa aparte (fuentes + unidad, salida cerrada `confirmed`/`not_confirmed`); solo avisa si se confirma. Sobre las 22 etiquetas (4 M, 18 P):

| verificador | variante | detecta M | falsas alarmas P |
|---|---|---|---|
| sin segundo pase | – | 4/4 | 5/18 |
| Mistral-24B | a ciegas | 1/4 | 0/18 |
| Mistral-24B | con el motivo del primer pase | 2/4 (1, 24) | 0/18 |
| Qwen2.5-14B | a ciegas | 2/4 | 0/18 |
| Qwen2.5-14B | con el motivo del primer pase | 3/4 | 3/18 |

- El segundo pase elimina las falsas alarmas, pero también deja de avisar de los antónimos inyectados (casos 2 y 17 se pierden casi siempre): la unidad entera, sin el resto de la respuesta, no basta para ver la inversión.
- Ninguna variante da 4/4 con 0 falsas alarmas. Ajustado sobre las mismas 22 etiquetas; los M son antónimos artificiales, no errores espontáneos. Coste ~1–2 s por unidad marcada. No integrado en el chat.

## Controles web de apoyo y compatibilidad (`judge_web.py`)
Prueba sintética (decisión finita `web-control/v5`): apoyo = 29 preguntas con su página NASA (debe ser `supported`) y con otra página NASA no relacionada (no debe serlo); compatibilidad = una página docente como "web" frente a sí misma (`compatible`) y con sus afirmaciones invertidas (`conflict`), 10 pares.

| juez | apoyo correcto | rechazo sin apoyo | compatibles | conflictos |
|---|---|---|---|---|
| Qwen2.5-14B (el que usa el chat ahora) | 26/29 | 27/29 | 10/10 | 9/10 |
| Mistral-24B | 27/29 | 25/29 | 10/10 | 9/10 |
| Qwen3-8B con razonamiento (juez anterior) | 28/29 | 20/29 | 10/10 | 6/10 |

El 14B es al menos tan bueno como el juez anterior (más estricto con páginas no relacionadas y mejor detectando conflictos). Es una comprobación sintética, no mide la calidad de páginas web reales.
