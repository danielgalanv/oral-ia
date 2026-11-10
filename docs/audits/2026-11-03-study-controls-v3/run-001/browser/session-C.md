# ORALIA — registro descriptivo de autoestudio

Sesión: 55eccb20-68c3-4fcf-bedc-bee0f76fba29

Generado: 2026-11-03T12:09:55.019681+00:00

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
La trazabilidad bidireccional de los requisitos implica vincular cada requerimiento tanto con las necesidades superiores (trazabilidad hacia atrás) como con elementos específicos del diseño o implementación (trazabilidad hacia adelante). Esto asegura que cada requerimiento esté justificado por una necesidad superior y que también pueda ser rastreado hasta un componente específico del sistema diseñado.

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe garantizar que los usuarios puedan realizar transacciones seguras y eficientes.

**Requerimiento:** El sistema debe validar la identidad del usuario mediante autenticación de dos factores antes de permitir cualquier transacción.

**Elemento de Diseño:** La aplicación móvil incluirá un módulo de autenticación que solicita tanto un código SMS como una huella digital del usuario antes de permitir acceso a la función de transacciones.

En este ejemplo:

- **Necesidad Superior**: Esta es una declaración general que define una funcionalidad crítica del sistema, en este caso, la seguridad y eficiencia en las transacciones.
  
- **Requerimiento**: Este es un requerimiento específico que deriva directamente de la necesidad superior. Específicamente, el requerimiento de autenticación de dos factores asegura que la transacción sea segura y eficiente, cumpliendo así con la necesidad superior.

- **Elemento de Diseño**: Este es un componente específico del sistema que implementa el requerimiento. En este caso, el módulo de autenticación en la aplicación móvil es el elemento que cumple con el requerimiento de autenticación de dos factores.

Este ejemplo demuestra cómo cada requerimiento puede ser rastreado desde una necesidad superior hasta un elemento de diseño específico, y viceversa, asegurando que todos los componentes del sistema estén alineados con los objetivos generales del proyecto.
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

1. **Completitud de los requisitos**: Implica que todos los elementos necesarios para satisfacer las necesidades del sistema están incluidos en el documento de requisitos. Esto significa que no falta ningún detalle importante que pueda afectar al funcionamiento del sistema. Por ejemplo, si se requiere que un sistema web permita a los usuarios realizar compras, los requisitos deben incluir detalles sobre cómo iniciar sesión, agregar productos al carrito, pagar y confirmar la compra. Un requisito incompleto podría omitir algún paso crucial, lo que llevaría a problemas durante la implementación.

2. **Consistencia de los requisitos**: Se refiere a la ausencia de conflictos o contradicciones entre los diferentes requisitos. Los requisitos deben ser coherentes entre sí, es decir, no deben existir requisitos que se contradigan o que no puedan cumplirse simultáneamente. Por ejemplo, si uno de los requisitos establece que el sistema debe ser seguro y otro requiere que sea fácil de usar, estos requisitos deben poder cumplirse sin contradecirse. Si se propone que el sistema debe ser seguro pero también debe permitir el acceso público sin restricciones, esto sería una inconsistencia.

Un ejemplo hipotético para ilustrar esta diferencia podría ser el siguiente:

**Necesidad Superior:** El sistema debe proporcionar un servicio de mensajería instantánea que sea seguro y fácil de usar.

**Requisitos:**
- El sistema debe cifrar todas las comunicaciones entre usuarios.
- El sistema debe permitir que los usuarios accedan sin necesidad de autenticación.
- El sistema debe mostrar una interfaz amigable y fácil de navegar.

En este caso:
- **Completitud**: El requisito de cifrado de comunicaciones cubre la necesidad de seguridad, pero falta un requisito que especifique cómo se manejarán las comunicaciones no cifradas, lo que podría considerarse una omisión.
- **Consistencia**: Existe una inconsistencia entre los requisitos de cifrar las comunicaciones y permitir acceso sin autenticación, ya que ambas características son difíciles de cumplir simultáneamente sin comprometer la seguridad.

Por lo tanto, la trazabilidad bidireccional de los requisitos permite rastrear cada requerimiento desde la necesidad superior hasta el diseño, asegurando que cada requerimiento esté completo y consistente con los demás, y que cumpla con los objetivos del sistema.
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
Dos requisitos pueden ser inconsistentes entre sí cuando uno excluye o contradice al otro, dificultando su cumplimiento simultáneo. Aquí tienes un ejemplo hipotético:

**Necesidad Superior:** El sistema debe proporcionar un servicio de mensajería instantánea que sea seguro y fácil de usar.

**Requisito 1:** El sistema debe cifrar todas las comunicaciones entre usuarios para garantizar la seguridad.

**Requisito 2:** El sistema debe permitir que los usuarios accedan sin necesidad de autenticación para facilitar su uso.

### Explicación del Conflicto

- **Requisito 1** enfatiza la seguridad al exigir que todas las comunicaciones entre usuarios estén cifradas. Esto implica que las comunicaciones no podrían ser interceptadas o leídas por terceros no autorizados, protegiendo la privacidad y la integridad de los datos.

- **Requisito 2**, por otro lado, busca mejorar la usabilidad al eliminar la necesidad de autenticación. Sin embargo, esto reduce significativamente la seguridad, ya que cualquier persona podría acceder al sistema sin verificar su identidad, lo que aumentaría el riesgo de intrusiones y mal uso.

Estos dos requisitos son inconsistentes porque:
- **Seguridad vs. Usabilidad**: La cifrado de comunicaciones (Requisito 1) incrementa la seguridad pero puede complicar el proceso de inicio de sesión, mientras que la eliminación de la autenticación (Requisito 2) simplifica el uso pero compromete la seguridad.
- **Contradicción Directa**: Si se cumple el Requisito 1, entonces las comunicaciones estarán cifradas, lo que implica que alguien que no ha sido autenticado no podrá acceder a ellas. Sin embargo, si se cumple el Requisito 2, cualquier persona podría acceder al sistema sin autenticación, lo que contradice la necesidad de cifrar las comunicaciones.

Este ejemplo ilustra cómo dos requisitos pueden ser inconsistentes debido a sus objetivos opuestos o contradictorios, lo que dificulta su implementación simultánea sin comprometer alguno de ellos.
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
