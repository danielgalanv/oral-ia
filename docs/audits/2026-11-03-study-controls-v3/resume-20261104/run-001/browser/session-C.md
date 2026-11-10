# ORALIA — registro descriptivo de autoestudio

Sesión: 4f322aab-5079-4813-a552-69811190e5a3

Generado: 2026-11-04T06:49:43.369967+00:00

Proveedor registrado (no es una acreditación de calidad):

```text
REAL_QWEN14B_QWEN3_THINKING_REVIEWED
```

Sin calificación, rúbrica, inferencia de aprendizaje o audio.

La copia descargada no se borra al finalizar la sesión.

```text
{
  "completed_attempts": 4,
  "shown_answers": 3,
  "shown_answers_with_internet": 0,
  "unshown_attempts": 1
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

Sin respuesta confirmada como mostrada

```text

```

Fuentes consultadas

```text
{
  "locales": [],
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
La diferencia entre que los requisitos sean completos y que sean consistentes radica en dos aspectos fundamentales:

1. **Completitud de los requisitos**: Implica que todos los elementos necesarios para satisfacer las necesidades del sistema están incluidos en el conjunto de requisitos. Esto significa que no falta ningún detalle importante que sea necesario para el funcionamiento adecuado del sistema. Por ejemplo, si se requiere que un sistema web permita a los usuarios realizar compras online, la completitud implicaría que se describen todos los pasos necesarios para realizar una compra, desde la selección del producto hasta el pago y confirmación del pedido.

2. **Consistencia de los requisitos**: Se refiere a la ausencia de conflictos o contradicciones entre los diferentes requisitos. Esto significa que cada requerimiento debe ser coherente con los demás y no debe contradecir a otros requerimientos. Por ejemplo, si uno de los requisitos es que el sistema debe permitir a los usuarios realizar compras sin registrarse previamente, mientras que otro requisito es que el sistema debe almacenar información personal de los usuarios para futuras compras, estos dos requisitos podrían entrar en conflicto si no se especifica cómo manejar esta situación.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe permitir a los usuarios realizar compras online de manera segura y eficiente.

**Requisitos:**

1. **Requisito 1:** El sistema debe permitir a los usuarios realizar compras sin registrarse previamente.
2. **Requisito 2:** El sistema debe almacenar información personal de los usuarios para futuras compras.

**Elemento de Diseño:**

- **Diseño del Proceso de Compra:** El sistema implementará un proceso de compra que permitirá a los usuarios realizar compras sin registro, utilizando métodos de pago seguros. Además, el sistema almacenará la información de los usuarios que decidan registrarse para futuras compras.

### Explicación

- **Completitud:** El diseño del sistema incluye todos los detalles necesarios para permitir a los usuarios realizar compras sin registro y también para almacenar la información de los usuarios que deciden registrarse. Esto asegura que todas las necesidades del usuario están cubiertas.

- **Consistencia:** Los requisitos deben ser consistentes entre sí. En este caso, se ha resuelto la posible contradicción entre los requisitos 1 y 2 al especificar que el almacenamiento de información será opcional y estará disponible solo para aquellos usuarios que deciden registrarse. De esta manera, ambos requisitos pueden coexistir sin conflicto.

Este ejemplo muestra cómo la completitud y la consistencia de los requisitos son dos características importantes que deben mantenerse en un documento de requisitos para asegurar que el sistema cumpla con todas las necesidades del usuario de manera coherente y sin errores.
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
Dos requisitos inconsistentes entre sí son aquellos que no pueden coexistir debido a que uno excluye al otro o ambos no pueden ser verdaderos simultáneamente. Veamos un ejemplo inventado para ilustrar esto:

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe permitir a los usuarios realizar transacciones seguras y eficientes.

**Requisitos:**

1. **Requisito 1:** El sistema debe permitir a los usuarios iniciar sesión utilizando una contraseña única.
2. **Requisito 2:** El sistema debe prohibir el uso de contraseñas únicas y exigir que los usuarios utilicen un método de autenticación de dos factores.

### Explicación

- **Requisito 1:** Este requisito establece que los usuarios deben iniciar sesión utilizando una contraseña única. Esto implica que el sistema aceptará una sola forma de autenticación basada en una contraseña.

- **Requisito 2:** Este requisito, por otro lado, establece que el sistema debe prohibir el uso de contraseñas únicas y requerir que los usuarios utilicen un método de autenticación de dos factores. Esto implica que los usuarios no podrán iniciar sesión simplemente con una contraseña, sino que deben usar un segundo factor de autenticación adicional, como un token o un código de verificación.

### Conflicto

Estos dos requisitos entran en conflicto porque uno excluye al otro. Si se implementa el Requisito 1, los usuarios podrían iniciar sesión únicamente con una contraseña, lo cual contradice el Requisito 2 que prohíbe el uso de contraseñas únicas. Por otro lado, si se implementa el Requisito 2, los usuarios no podrían iniciar sesión con una sola contraseña, lo cual contradice el Requisito 1.

Para resolver este conflicto, sería necesario tomar una decisión sobre cuál de los dos requisitos se va a implementar. Por ejemplo, si se decide implementar el Requisito 2, entonces el Requisito 1 debería ser descartado o modificado para que coincida con el nuevo enfoque de autenticación.

Este ejemplo demuestra cómo la consistencia entre los requisitos es crucial para evitar situaciones donde los requisitos se contradigan entre sí, lo que puede llevar a problemas durante la implementación del sistema.
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
