# ORALIA — registro descriptivo de autoestudio

Sesión: 981fb3ac-963f-44c4-adbb-7c3ba733f4fb

Generado: 2026-11-03T01:23:46.777334+00:00

Proveedor registrado (no es una acreditación de calidad):

```text
REAL_QWEN14B_QWEN3_THINKING_REVIEWED
```

Sin calificación, rúbrica, inferencia de aprendizaje o audio.

La copia descargada no se borra al finalizar la sesión.

```text
{
  "completed_attempts": 4,
  "shown_answers": 2,
  "shown_answers_with_internet": 0,
  "unshown_attempts": 2
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

## Intercambio 4

Pregunta

```text
Pon un ejemplo inventado de dos requisitos que sean inconsistentes entre sí y explica el conflicto.
```

Respuesta mostrada

```text
Dos requisitos pueden ser inconsistentes entre sí cuando ambos no pueden cumplirse simultáneamente debido a restricciones técnicas, económicas o de tiempo. Aquí hay un ejemplo inventado que ilustra este concepto:

### Ejemplo Inventado

**Necesidad Superior:** El sistema debe proporcionar una alta disponibilidad y una alta seguridad.

**Requisito 1:** El sistema debe estar disponible al menos el 99.99% del tiempo.

**Requisito 2:** El sistema debe realizar una verificación de identidad triple factor (por ejemplo, token físico, biometría y pregunta secreta) antes de permitir el acceso a cualquier recurso sensible.

### Explicación del Conflicto

- **Requisito 1 (Alta Disponibilidad):** Este requisito busca garantizar que el sistema esté operativo casi siempre, minimizando el tiempo de inactividad. Para lograr esto, se deben implementar mecanismos de redundancia y recuperación rápida, como múltiples servidores en diferentes ubicaciones geográficas y sistemas de respaldo automatizados.

- **Requisito 2 (Alta Seguridad):** Este requisito busca asegurar que solo los usuarios autorizados puedan acceder a recursos sensibles. La verificación de identidad triple factor aumenta significativamente la seguridad, pero también introduce un mayor tiempo de espera y posibles fallas en el proceso de autenticación.

### Conflicto entre los Requisitos

El problema surge cuando intentamos cumplir ambos requisitos simultáneamente:

- **Tiempo de Inicio:** La verificación de identidad triple factor puede llevar varios minutos, incluso si todo funciona correctamente. Esto podría interrumpir la disponibilidad del sistema durante períodos de alta carga, ya que los usuarios tendrían que esperar para iniciar sesión.

- **Fallos en la Autenticación:** Si alguno de los métodos de autenticación falla (por ejemplo, el token físico se pierde o la biometría no funciona), el sistema podría quedarse bloqueado hasta que se resuelva el problema. Esto podría causar períodos prolongados de inactividad, afectando la disponibilidad del sistema.

- **Recuperación Rápida:** Para mantener la alta disponibilidad, el sistema necesita recuperarse rápidamente de cualquier fallo. Sin embargo, la implementación de un sistema de autenticación triple factor puede complicar la recuperación rápida, ya que requiere un proceso más complejo y detallado para restaurar el acceso.

### Solución Potencial

Para resolver este conflicto, se podrían considerar alternativas como:

- Implementar un sistema de autenticación de dos factores para la mayoría de los usuarios y reservar la verificación triple factor solo para accesos críticos.
- Utilizar un sistema de autenticación adaptativa que ajuste el nivel de seguridad según el riesgo percibido, permitiendo un acceso rápido en situaciones seguras y un proceso más riguroso en casos de alto riesgo.

Este ejemplo muestra cómo dos requisitos pueden entrar en conflicto debido a restricciones técnicas y operativas, y cómo es necesario encontrar soluciones equilibradas para satisfacer ambas necesidades de manera efectiva.
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
