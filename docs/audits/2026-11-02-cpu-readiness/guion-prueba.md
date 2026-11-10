# Guion de comprobación del chat

Objetivo: que el docente pruebe explicaciones sobre requisitos, seguimiento y cambio natural de tema. No se evalúa ni puntúa al alumno. Se aceptan ejemplos ficticios coherentes y valores ilustrativos identificados como tales. Las fuentes se presentan por documento/página o URL, sin exigir citas por frase.

## Preparación

La prueba real requiere GPU disponible y autorización vigente. No se inicia automáticamente al terminar las comprobaciones CPU. Desde la raíz de ORALIA:

```powershell
.\scripts\study-chat.ps1
```

Abrir `/estudio` en la URL local anunciada. No cerrar servicios ajenos ni ejecutar Reset. Si faltan recursos, registrar el bloqueo; un fallo de recursos no demuestra mala calidad académica.

Para preparar interfaz e índice sin inferencia, se conserva `-PrepareOnly -NoBrowser`. La preparación no sustituye el ensayo real.

## Conversación

Se reutilizan las doce preguntas ya aprobadas por el usuario el 1 de noviembre, sin cambiar su texto. El JSON histórico conserva su estado inicial; la confirmación posterior está en `approval.json`. No se modifica ninguno.

- [Preguntas completas](../2026-11-01-autostudy-approval/questions.md).
- [Confirmación conservada](../2026-11-01-autostudy-approval/approval.json).

1. Comenzar y hacer A1–A4: definición, funcional/no funcional y dos ejemplos. Comprobar que la aclaración atiende a la duda y conserva el contexto. Repetir una estructura o inventar un escenario no es, por sí mismo, un error.
2. Continuar con B1–B4: valor hipotético de 0,3 segundos, comprobación y realismo, revisión con el cliente. No confundir un dato de ejemplo con un estándar obligatorio.
3. Continuar con C1–C4: trazabilidad, límites de lo que demuestra, completitud/consistencia y ejemplo de conflicto. Enviar C3 como una pregunta normal: no usar bandera de cambio de tema.
4. Abrir Fuentes en una respuesta y contrastar el original. La presencia del documento no prueba que respalde toda la explicación: revisar las afirmaciones centrales, sin exigir exhaustividad enciclopédica.
5. Al agotar las doce preguntas, comprobar que el envío queda deshabilitado y Finalizar sigue disponible. Cerrar y reentrar no renueva la cuota del proceso.

Guardar el texto realmente mostrado, pregunta, fuentes y crítica/corrección interna en un dossier técnico separado de la vista del alumno. Registrar qué turnos no ocurrieron, sin inventar respuestas. Una conversación útil no exige que haya una reparación: si el borrador es adecuado, puede entregarse tras revisión.

## Operación y fallos

Cancelación durante generación, recarga de workers y recuperación con inferencia real se prueban en un arranque propio separado, porque consumen el mismo presupuesto y no deben impedir terminar el guion académico. Una pregunta cancelada que llegó al proveedor consume cuota. Cancelar no debe incorporar texto parcial al historial.

La recuperación de red no reenvía preguntas: conserva la sesión solo mientras sigue vigente. La reentrada tras cierre comienza sin mensajes anteriores; no es restauración persistente. Las pruebas CPU ya cubren pérdida de confirmación, pérdida de respuesta, pregunta no recibida y conservación de un borrador nuevo.

No exigir al docente provocar cortes de red durante su primera prueba. Conexión, cierre y caducidad se comprueban además en el ensayo técnico reproducible.

## Decisión

Considerar adecuada una respuesta si contesta la pregunta, es comprensible, conserva las condiciones importantes y no contradice materialmente la fuente ni atribuye como reales datos inventados. Separar errores académicos centrales, omisiones necesarias, mejoras opcionales de estilo y fallos operativos. No convertir una mejora opcional en rechazo.

Conservar cada versión si hay corrección y contar también errores nuevos o críticas equivocadas. Detener ante fuga de datos, fuente retirada, texto estructurado mostrado indebidamente o entrega parcial. Un límite seguro puede ser técnicamente correcto, pero no acredita una conversación útil.

T191 termina solo con evidencia integrada de modelos reales; los ensayos CPU no la cierran. La aceptación docente y el ensayo con estudiantes son decisiones posteriores y distintas.
