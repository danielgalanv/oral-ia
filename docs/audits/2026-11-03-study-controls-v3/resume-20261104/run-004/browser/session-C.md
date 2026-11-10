# ORALIA — registro descriptivo de autoestudio

Sesión: 2908dc43-645b-4b6d-aeef-de8cb2a4383c

Generado: 2026-11-04T08:06:56.968998+00:00

Proveedor registrado (no es una acreditación de calidad):

```text
REAL_QWEN14B_QWEN3_THINKING_REVIEWED
```

Sin calificación, rúbrica, inferencia de aprendizaje o audio.

La copia descargada no se borra al finalizar la sesión.

```text
{
  "completed_attempts": 4,
  "shown_answers": 4,
  "shown_answers_with_internet": 0,
  "unshown_attempts": 0
}
```

## Intercambio 1

Pregunta

```text
¿Qué es la trazabilidad bidireccional de los requisitos? Pon un ejemplo inventado que relacione una necesidad, un requisito y un elemento de diseño.
```

Respuesta mostrada

```text
La trazabilidad bidireccional de los requisitos implica vincular cada requerimiento tanto con las necesidades superiores (trazabilidad hacia atrás) como con los elementos de diseño específicos (trazabilidad hacia adelante). Esto asegura que cada requerimiento esté justificado por una necesidad superior y que también tenga un impacto directo en el diseño del sistema.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe garantizar que los usuarios puedan realizar transacciones seguras y eficientes.

**Requerimiento:** El sistema debe validar la identidad del usuario mediante autenticación de dos factores antes de permitir cualquier transacción.

**Elemento de Diseño:** La aplicación móvil incluirá un módulo de autenticación que solicitará al usuario ingresar un código de seguridad enviado por SMS junto con su contraseña.

### Explicación

En este ejemplo:

- **Necesidad Superior**: Esta es una declaración general que define el objetivo principal del sistema. En este caso, se enfoca en la seguridad y eficiencia de las transacciones.

- **Requerimiento**: Este es un detalle específico que debe cumplirse para alcanzar la necesidad superior. Aquí, el requerimiento es la implementación de la autenticación de dos factores, que es una medida necesaria para garantizar la seguridad de las transacciones.

- **Elemento de Diseño**: Este es un componente específico del sistema que implementa el requerimiento. En este caso, el elemento de diseño es un módulo de autenticación en la aplicación móvil que cumple con el requerimiento de autenticación de dos factores.

Este ejemplo ilustra cómo cada requerimiento está vinculado tanto a una necesidad superior como a un elemento de diseño específico, proporcionando una trazabilidad bidireccional que asegura que cada parte del sistema cumpla con los objetivos definidos inicialmente.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "nasa-handbook.pdf",
      "page": 209,
      "original_url": "/api/v1/documentary/nasa-seh/original#page=209"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 13,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=13"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 4,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=4"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 39,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=39"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 37,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=37"
    }
  ],
  "internet": []
}
```

## Intercambio 2

Pregunta

```text
¿Tener esas relaciones de trazabilidad demuestra por sí solo que el diseño cumple correctamente el requisito?
```

Respuesta mostrada

```text
La trazabilidad bidireccional de los requisitos asegura que cada requerimiento esté vinculado tanto a una necesidad superior como a un elemento de diseño específico. Sin embargo, tener estas relaciones de trazabilidad por sí sola no demuestra que el diseño cumpla correctamente el requisito. La trazabilidad es una herramienta importante para gestionar y controlar los requisitos, pero no garantiza automáticamente la satisfacción de estos.

Para asegurar que el diseño cumple correctamente con el requisito, es necesario realizar una serie de actividades adicionales:

1. **Verificación de la calidad del requisito**: Debe ser comprensible, no ambiguo, gramaticalmente correcto, ortográficamente correcto, realizable y comprobable. Esto significa que el requisito debe ser claro y preciso, y debe poder implementarse con tecnología existente y dentro de un costo razonable.

2. **Evaluación de la trazabilidad**: Asegurarse de que cada requerimiento esté correctamente trazado hacia atrás a una necesidad superior y hacia adelante a un elemento de diseño. Esto implica verificar que cada requerimiento tiene una fuente clara y que está vinculado adecuadamente a los elementos de diseño relevantes.

3. **Consistencia interna y externa**: Los requisitos deben ser consistentes entre sí y con otros documentos del proyecto. Esto implica evitar contradicciones internas y redundancias innecesarias, así como asegurar que los requisitos no sean inconsistentes con otros documentos del proyecto.

4. **Pruebas y validación**: Se deben definir y realizar pruebas para verificar que el diseño cumple con el requisito. Estas pruebas deben ser realizables y proporcionar resultados claros que permitan determinar si el requisito se ha cumplido correctamente.

Por ejemplo, consideremos nuevamente el ejemplo anterior:

- **Necesidad Superior:** El sistema debe garantizar que los usuarios puedan realizar transacciones seguras y eficientes.
- **Requerimiento:** El sistema debe validar la identidad del usuario mediante autenticación de dos factores antes de permitir cualquier transacción.
- **Elemento de Diseño:** La aplicación móvil incluirá un módulo de autenticación que solicitará al usuario ingresar un código de seguridad enviado por SMS junto con su contraseña.

Para asegurar que el diseño cumple correctamente con el requisito, se deben realizar las siguientes acciones:

- **Verificación de la calidad del requisito**: El requisito de autenticación de dos factores debe ser claro y preciso, y debe ser posible implementarlo con tecnología existente y dentro de un costo razonable.
- **Evaluación de la trazabilidad**: Se debe verificar que el requisito de autenticación de dos factores está correctamente trazado hacia atrás a la necesidad superior de seguridad y eficiencia en las transacciones, y hacia adelante al módulo de autenticación en la aplicación móvil.
- **Consistencia interna y externa**: El requisito de autenticación de dos factores debe ser consistente con otros requisitos y documentos del proyecto, evitando contradicciones y redundancias innecesarias.
- **Pruebas y validación**: Se deben definir y realizar pruebas para verificar que el módulo de autenticación cumple con el requisito de autenticación de dos factores. Por ejemplo, se podría realizar una prueba donde se simula la entrada de un usuario con una contraseña y un código de seguridad válido, y se verifica que el sistema permita la transacción.

Estas acciones aseguran que el diseño cumple correctamente con el requisito, y no solo que existe una relación de trazabilidad entre ellos.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "nasa-handbook.pdf",
      "page": 142,
      "original_url": "/api/v1/documentary/nasa-seh/original#page=142"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 11,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=11"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 10,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=10"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 13,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=13"
    },
    {
      "filename": "Ch4 Req Eng.pptx",
      "page": 76,
      "original_url": "/api/v1/documentary/sommerville/original"
    }
  ],
  "internet": []
}
```

## Intercambio 3

Pregunta

```text
Cambiemos de tema: ¿qué diferencia hay entre que los requisitos sean completos y que sean consistentes?
```

Respuesta mostrada

```text
La diferencia entre que los requisitos sean completos y que sean consistentes radica en los aspectos que cada uno aborda:

### Completitud de los requisitos:
Los requisitos deben ser completos en el sentido de que deben describir todas las características y funcionalidades necesarias para satisfacer las necesidades del usuario y del negocio. Esto significa que deben cubrir todos los aspectos del sistema que son relevantes y necesarios para su funcionamiento adecuado. Un requisito completo debe incluir detalles suficientes para que los desarrolladores comprendan completamente lo que se espera del sistema. Por ejemplo, si se requiere que el sistema permita la búsqueda de pacientes, el requisito completo debería especificar cómo se realizará esta búsqueda, en qué contexto, qué datos se utilizarán y cuáles serán los resultados esperados.

### Consistencia de los requisitos:
Los requisitos deben ser consistentes, lo que significa que no deben haber contradicciones entre ellos. Esto implica que los requisitos no deben ser mutuamente excluyentes ni entrar en conflicto entre sí. Por ejemplo, si se requiere que el sistema permita la búsqueda de pacientes en tiempo real, no puede haber otro requisito que especifique que la búsqueda debe ser lenta y detallada. La consistencia también implica que los requisitos deben ser coherentes con los objetivos del sistema y con otras partes del documento de requisitos.

### Ejemplo Hipotético:
Supongamos que estamos diseñando un sistema de gestión de pacientes en un hospital.

- **Completitud**:
    - **Requisito Completo**: "El sistema debe permitir la búsqueda de pacientes por nombre, apellido y número de seguro médico. La búsqueda debe devolver todos los registros médicos asociados al paciente."
    - Este requisito es completo porque describe claramente qué debe hacer el sistema y qué información se necesita para realizar la búsqueda.

- **Consistencia**:
    - **Requisito Consistente**: "El sistema debe permitir la búsqueda de pacientes por nombre, apellido y número de seguro médico. La búsqueda debe devolver todos los registros médicos asociados al paciente."
    - Este requisito es consistente con otros requisitos que pueden existir, como "El sistema debe almacenar todos los registros médicos de los pacientes de manera organizada y accesible".
    - Sin embargo, si hubiera otro requisito que dijera "El sistema debe buscar pacientes por nombre y apellido, pero no por número de seguro médico", esto sería inconsistente ya que entra en conflicto con el primer requisito.

### Conclusión:
La completitud se refiere a la exhaustividad de los requisitos, asegurando que todos los aspectos necesarios estén cubiertos. La consistencia se refiere a la ausencia de contradicciones entre los requisitos, asegurando que todos los requisitos sean coherentes entre sí y con los objetivos del sistema. Ambos son fundamentales para garantizar que el sistema final cumpla con las expectativas y funcione correctamente.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "5 - Requisitos.pdf",
      "page": 14,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=14"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 83,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=83"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 89,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=89"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 13,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=13"
    },
    {
      "filename": "nasa-handbook.pdf",
      "page": 142,
      "original_url": "/api/v1/documentary/nasa-seh/original#page=142"
    }
  ],
  "internet": []
}
```

## Intercambio 4

Pregunta

```text
Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.
```

Respuesta mostrada

```text
Dos requisitos inconsistentes entre sí son aquellos que contienen elementos que entran en conflicto o que no pueden cumplirse simultáneamente. Aquí tienes un ejemplo hipotético de dos requisitos que son inconsistentes:

### Ejemplo Hipotético

**Requisito 1:** "El sistema debe permitir que los usuarios ingresen y modifiquen sus datos personales en tiempo real."

**Requisito 2:** "El sistema debe bloquear cualquier intento de modificación de datos personales durante las horas pico de uso, que se definen como entre las 10:00 y las 14:00 horas."

### Explicación del Conflicto

- **Requisito 1** establece que los usuarios deben poder modificar sus datos personales en cualquier momento, incluidas las horas pico.
- **Requisito 2**, por otro lado, especifica que durante las horas pico (entre las 10:00 y las 14:00), el sistema debe bloquear cualquier intento de modificación de datos personales.

Estos dos requisitos son inconsistentes porque:
- **Requisito 1** permite modificaciones en tiempo real, lo cual implica que los usuarios pueden cambiar sus datos en cualquier momento.
- **Requisito 2** impide modificaciones durante un período específico (horas pico), lo cual entra en conflicto con la posibilidad de modificaciones en tiempo real.

### Conclusión

Este ejemplo ilustra cómo dos requisitos pueden ser inconsistentes debido a restricciones temporales que limitan la funcionalidad que otro requisito exige. La resolución de este conflicto podría implicar revisar y ajustar los requisitos para encontrar una solución que equilibre ambas necesidades, tal como permitir modificaciones fuera de las horas pico o establecer mecanismos alternativos para manejar las modificaciones durante las horas pico.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "5 - Requisitos.pdf",
      "page": 53,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=53"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 80,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=80"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 10,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=10"
    },
    {
      "filename": "nasa-handbook.pdf",
      "page": 144,
      "original_url": "/api/v1/documentary/nasa-seh/original#page=144"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 13,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=13"
    }
  ],
  "internet": []
}
```
