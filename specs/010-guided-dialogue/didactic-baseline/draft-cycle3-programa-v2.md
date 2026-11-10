# Material docente ficticio — programa

## entrada

Objetivo: Separar recepción de datos y decisiones posteriores.

En el programa ficticio Registro Local, la entrada recibe un registro y lo entrega a validación. Recibir un dato no equivale a comprobarlo ni a guardarlo.

Ejemplo: La entrada recibe un registro de inventario ficticio con un campo cantidad y lo pasa a validación.

Contraste: La entrada recibe registros; la validación comprueba sus campos. Cada parte tiene una responsabilidad distinta.

## validacion

Objetivo: Justificar una comprobación antes del almacenamiento.

La validación comprueba los campos requeridos y el formato declarado del registro ficticio. Si falta un campo requerido, devuelve un error comprensible y no envía ese registro al almacenamiento.

Ejemplo: Si falta el campo cantidad requerido, validación rechaza el registro y explica el campo que falta.

Contraste: Validar comprueba requisitos; almacenar conserva registros que han superado esas comprobaciones.

## almacenamiento

Objetivo: Identificar el componente que conserva resultados.

El almacenamiento del programa ficticio conserva registros validados. No recibe como válidos los registros rechazados por validación. El material no describe conexión a servicios externos.

Ejemplo: Un registro aceptado por validación se conserva en el almacenamiento local ficticio.

Contraste: Conservar un registro y presentar su resultado son responsabilidades diferentes.

## salida

Objetivo: Distinguir presentación y conservación.

La salida presenta un resultado comprensible: confirmación de registro aceptado o aviso de validación. Presentar ese resultado no añade por sí mismo otra operación de almacenamiento.

Ejemplo: La salida muestra un aviso cuando falta un campo requerido, sin afirmar que el registro fue guardado.

Contraste: La salida comunica resultados; el almacenamiento conserva datos aceptados.

## responsabilidades

Objetivo: Explicar un recorrido con funciones acotadas.

El recorrido válido es entrada, validación, almacenamiento y salida. Un registro inválido pasa de validación a un aviso de salida sin conservarse como aceptado. Cada parte conserva su función declarada.

Ejemplo: Un registro válido se comprueba antes de guardarse y luego se presenta una confirmación.

Contraste: El recorrido válido incluye almacenamiento; el recorrido rechazado produce un aviso sin conservar el registro como aceptado.


# Ampliación didáctica ficticia v2

## validacion: definition

La comprobación se llama validación. En Registro Local, valida los campos de un registro antes de almacenarlo. Recibir datos, comprobarlos y mostrarlos son responsabilidades diferentes.

## validacion: process

Primero, la entrada recibe el registro ficticio y lo envía a validación. Después, validación comprueba sus campos, incluido que cantidad sea un entero igual o mayor que cero. Por último, si cumple las reglas, el registro pasa a almacenamiento; si falla, se muestra un aviso de rechazo. El almacenamiento recibe únicamente los registros aceptados. Cada etapa tiene una responsabilidad distinta.

## validacion: process/alternative

Primero, separa recibir de comprobar: entrada solo entrega los datos. Después, decide con las reglas de validación si el registro es aceptable. Por último, sigue una de dos salidas: guardar el registro válido o avisar del rechazo sin almacenarlo como aceptado. Por ejemplo, una cantidad negativa recorre la vía de rechazo en lugar de la de guardado.

## validacion: cause

Se valida antes de guardar para evitar conservar como aceptados registros que incumplen las reglas del programa. En Registro Local, una cantidad negativa incumple las reglas; detectarla antes del almacenamiento permite mostrar un aviso y conservar únicamente los registros aceptados.

## validacion: cause/alternative

Distingue un dato recibido de un dato aceptado. La entrada puede recibir una cantidad incorrecta; la validación detecta ese problema. Esa comprobación previa explica por qué el almacenamiento solo debe aceptar lo que supera las reglas.

## validacion: possibility

No: la validación previa es obligatoria. En el recorrido autorizado de Registro Local, solo se guarda como aceptado un registro tras superar la validación. Primero se comprueban sus campos; únicamente el registro válido pasa a almacenamiento. Un registro inválido produce un aviso de rechazo. Esta regla describe este programa ficticio; otros programas pueden tener diseños diferentes.

## validacion: possibility/alternative

No: la validación previa es obligatoria. Dentro del recorrido válido de este programa, recibir un registro es solo el primer paso. La validación decide si puede pasar a almacenamiento. Si falla, se rechaza y se emite un aviso; se guarda como aceptado únicamente lo que supera la comprobación. Otros diseños informáticos pueden aplicar reglas diferentes.

