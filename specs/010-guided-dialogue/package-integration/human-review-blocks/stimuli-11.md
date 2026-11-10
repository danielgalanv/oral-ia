# Estímulos expuestos, bloque 11

Solo desarrollo expuesto; revisión didáctica humana pendiente. No llamar reserva.

## programa-docx / DEV-programa-almacenamiento-cause

Participante: ¿Por qué es así en confirmación del guardado?

ORALIA: Una escritura puede fallar por una ruta no disponible o falta de permisos. Informar éxito antes de terminar confunde una intención con un resultado y puede inducir al usuario a creer que sus datos están a salvo.

Propósito esperado: cause. Unidad esperada: programa-almacenamiento-cause.

[Cita, versión y resultado completo](../stimuli-v3-final/programa-docx-DEV-programa-almacenamiento-cause.json).

Revisión humana de pertinencia/suficiencia y hechos: pendiente.

## programa-docx / DEV-programa-almacenamiento-definition

Participante: ¿Qué significa confirmación del guardado?

ORALIA: Almacenar significa conservar el registro aceptado para poder recuperarlo después. En Registro Local se usa un archivo local. Que un dato sea válido no demuestra que el guardado haya terminado.

Propósito esperado: definition. Unidad esperada: programa-almacenamiento-definition.

[Cita, versión y resultado completo](../stimuli-v3-final/programa-docx-DEV-programa-almacenamiento-definition.json).

Revisión humana de pertinencia/suficiencia y hechos: pendiente.

## programa-docx / DEV-programa-almacenamiento-possibility

Participante: ¿Qué es posible y qué no en confirmación del guardado?

ORALIA: Sí, un registro válido puede no guardarse. Tras un fallo no se debe reintentar indefinidamente ni afirmar que no hubo ningún efecto si el resultado es desconocido.

Propósito esperado: possibility. Unidad esperada: programa-almacenamiento-possibility.

[Cita, versión y resultado completo](../stimuli-v3-final/programa-docx-DEV-programa-almacenamiento-possibility.json).

Revisión humana de pertinencia/suficiencia y hechos: pendiente.

## programa-docx / DEV-programa-almacenamiento-process

Participante: Explícame paso a paso confirmación del guardado.

ORALIA: Primero, recibe el registro validado. Después, intenta la escritura mediante la función de almacenamiento. Solo cuando esa operación termina sin error, devuelve confirmación al flujo principal. Si aparece un error de escritura, informa que no se ha confirmado el guardado y conserva el control para decidir el siguiente paso.

Propósito esperado: process. Unidad esperada: programa-almacenamiento-process.

[Cita, versión y resultado completo](../stimuli-v3-final/programa-docx-DEV-programa-almacenamiento-process.json).

Revisión humana de pertinencia/suficiencia y hechos: pendiente.
