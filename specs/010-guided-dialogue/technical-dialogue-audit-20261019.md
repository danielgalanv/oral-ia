# Auditoría técnica de IA — 24 diálogos

AI technical audit of actual synthetic outputs; no human utility, human approval or real voice validation

Los informes originales y sus propiedades aprobadas se conservan. Esta lectura detecta defectos semánticos adicionales; no sustituye T067 ni acredita utilidad humana.

| Caso | Resultado de lectura técnica | Hallazgo / decisión humana pendiente |
|---|---|---|
| D01 | review_scope | Aclaración de consulta amplia y selección de tema; no se afirma ausencia de material. La utilidad de la orientación debe revisarla una persona. |
| D02 | correction | La comparación con evaporación cambió el objetivo desde condensación. T069 conserva el objetivo y usa su contraste docente. |
| D03 | correction | Las solicitudes de ejemplo protegido y solución se sustituían por pregunta/aviso genérico. T070 da un límite autorizado sin revelar respuesta. |
| D04 | correction_and_scope | Petición de organización de exposición provocaba repetición rechazada. T070 limita composición idéntica; la cobertura docente de un guion de exposición sigue siendo juicio de revisión humana. |
| D05 | correction | En revisión conceptual, un ejemplo solicitado se sustituía por pregunta. T070 usa ejemplo revisado cuando los permisos lo permiten y conserva la pregunta pendiente. |
| D06 | correction | Confirmación de salida bloqueada por negación sobre otro predicado. T069 distingue predicados finitos conocidos; mantiene contradicciones reales y T090. |
| D07 | review_scope | Pregunta y tres pistas permanecen ancladas; agotamiento exige una opción explícita. Revisar claridad del siguiente paso, sin inferir aprendizaje. |
| D08 | correction | Ejemplo protegido no disponible provocaba verification_failed. T070 limita ese formato en vez de fingir otro ejemplo o mostrar solución. |
| D09 | correction | Respuesta sobre evaporación originaba repregunta genérica de temperatura. T069 solicita confirmar un tema ajeno al objetivo, sin cambiar la pregunta ni juzgar la respuesta. |
| D10 | correction | «¿Puedes ayudarme?» no activaba ayuda. T068 cubre formas de ayuda; repetir pregunta mantiene su referente. |
| D11 | correction | Respuesta de almacenamiento sobre otra pregunta y reformulación ya utilizada daban seguimiento no pertinente o fallo genérico. T069/T070 aclaran transición y limitan alternativa agotada. |
| D12 | review_scope | Validación es parte del objetivo recepción/validación; no debe confundirse con cambio de tema. El paso a salida requiere confirmación. |
| V-H01 | review_scope | Consulta de dos temas requiere elección explícita; la comparación/repetición se deben juzgar según el material seleccionado. |
| V-H02 | correction | «Repite la pregunta» reproducía un contraste cuando no existía pregunta pendiente. T068 orienta sin atribuir categoría de pregunta a una explicación. |
| V-H03 | review_scope | Composición de tres unidades revisadas y apoyos concretos. Revisión humana de suficiencia; no se acredita generación libre o un guion nuevo. |
| V-H04 | no_additional_technical_defect | Pregunta, tres pistas, repetición y reformulación protegidas; sin respuesta ni fuente revelada en el recorrido observado. |
| V-H05 | no_additional_technical_defect | Revisión conceptual conserva pregunta a través de pistas y exige transición confirmada; sin evaluación del participante. |
| V-H06 | correction | «Repite la comparación» se clasificaba como dos órdenes. T068 reconoce el objeto y reconstruye la unidad vigente, sin saltar verificadores. |
| V-H07 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |
| V-H08 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |
| V-H09 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |
| V-H10 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |
| V-H11 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |
| V-H12 | review_scope | Secuencia protegida con afirmación distinta: no se afirma corrección/contradicción ni se revela solución. Patrón de ayuda similar a otros casos; revisar pertinencia y variedad, no contar como validación humana independiente. |

Correcciones T068–T070 y validación T071 en curso. Las nuevas salidas se guardan en directorios separados. El primer paquete de revisión humana permanece como evidencia del código anterior; se preparará un paquete actualizado tras verificar los cambios.
