# ORALIA — registro descriptivo de autoestudio

Sesión: ca1d34ff-e633-434a-a868-30126660ccad

Generado: 2026-11-03T09:57:44.076279+00:00

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
En una aplicación de reservas propongo que la búsqueda responda en menos de 0,3 segundos. Es un valor inventado para el ejemplo. ¿Qué tipo de requisito es y por qué?
```

Respuesta mostrada

```text
La propuesta de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos es un requisito no funcional. Este tipo de requisitos se refiere a las características del sistema que no describen directamente lo que el sistema debe hacer, sino cómo debe hacerlo. En este caso, el requisito se relaciona con la propiedad de velocidad, específicamente con el tiempo de respuesta del usuario o evento, que es una medida de la capacidad del sistema para procesar transacciones o responder a eventos en un tiempo determinado.

Según la tabla de métricas para especificar requisitos no funcionales presentada en la fuente, la propiedad de velocidad puede ser medida por el tiempo de respuesta del usuario o evento. En tu ejemplo, estás estableciendo un límite temporal para la respuesta de la aplicación, lo cual es una forma común de especificar un requisito no funcional de velocidad.

Este requisito no funcional de velocidad asegura que la aplicación sea rápida y eficiente en la respuesta a las solicitudes de los usuarios, mejorando así la experiencia del usuario y la eficacia general del sistema.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "5 - Requisitos.pdf",
      "page": 22,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=22"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 41,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=41"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 83,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=83"
    },
    {
      "filename": "4 - Agil.pdf",
      "page": 25,
      "original_url": "/api/v1/documentary/docente-agil/original#page=25"
    },
    {
      "filename": "7 - Modelos.pdf",
      "page": 35,
      "original_url": "/api/v1/documentary/docente-modelos/original#page=35"
    }
  ],
  "internet": []
}
```

## Intercambio 2

Pregunta

```text
¿Cómo comprobaríamos que se cumple ese requisito? Explícame qué haríamos y qué observaríamos.
```

Respuesta mostrada

```text
Para comprobar que la aplicación de reservas cumple el requisito de responder a las búsquedas en menos de 0,3 segundos, se deben seguir estos pasos:

1. **Definir la prueba**: Diseñar una prueba que simule una búsqueda típica en la aplicación. Esta prueba debería incluir todas las operaciones necesarias para realizar una búsqueda, desde la entrada de los parámetros hasta la obtención de resultados.

2. **Configurar el entorno de prueba**: Preparar un ambiente de prueba que sea representativo del entorno real donde se utilizará la aplicación. Esto incluye tener un servidor adecuadamente configurado, una base de datos con datos de prueba similares a los que se encontrarían en producción, y un cliente que pueda simular las condiciones de uso del usuario final.

3. **Ejecutar la prueba**: Ejecutar la prueba varias veces para obtener una media de tiempos de respuesta. Es importante realizar múltiples pruebas para asegurarse de que el resultado no es una anomalía y para poder calcular una media que refleje el rendimiento promedio de la aplicación.

4. **Medir el tiempo de respuesta**: Durante cada prueba, medir el tiempo que tarda la aplicación en responder a la solicitud de búsqueda. Esto se puede hacer utilizando herramientas de medición de rendimiento, como herramientas de profiling o monitoreo de aplicaciones web.

5. **Análisis de resultados**: Comparar el tiempo de respuesta medio obtenido con el umbral de 0,3 segundos. Si el tiempo medio de respuesta es menor que 0,3 segundos, entonces el requisito se considera cumplido. Si no es así, se debe investigar por qué el tiempo de respuesta es mayor y tomar medidas correctivas.

Estos pasos permiten asegurar que el requisito de velocidad se cumple de manera consistente y que la aplicación proporciona respuestas rápidas a las solicitudes de los usuarios, mejorando así la experiencia del usuario y la eficacia del sistema.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 11,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=11"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 12,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=12"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 22,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=22"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 10,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=10"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 41,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=41"
    }
  ],
  "internet": []
}
```

## Intercambio 3

Pregunta

```text
Entonces, si podemos medirlo, ¿ya sabemos que es un requisito realista?
```

Respuesta mostrada

```text
La capacidad de medir un requisito no garantiza automáticamente que sea realista. La medición permite verificar si el requisito se cumple, pero no asegura que sea factible o adecuado desde una perspectiva práctica. Según las fuentes proporcionadas, un requisito debe cumplir varios criterios para considerarse realista y válido:

1. **Verificabilidad**: Debe ser posible definir pruebas que demuestren si el requisito se cumple o no. En tu caso, podrías realizar pruebas de rendimiento para medir el tiempo de respuesta de la aplicación durante las búsquedas. Sin embargo, esto no asegura que el requisito sea realista.

2. **Realizabilidad**: Un requisito debe ser técnicamente factible y económicamente viable. Por ejemplo, aunque puedas medir que la aplicación responde en menos de 0,3 segundos, debes considerar si es técnicamente posible implementar esta velocidad de respuesta con los recursos disponibles y si el costo de implementación es razonable.

3. **Compreensibilidad**: El requisito debe ser claro y fácil de entender. Si el requisito de que la aplicación responda en menos de 0,3 segundos es bien entendido por todos los involucrados, eso es un paso importante, pero aún no garantiza su realizabilidad.

4. **Trazabilidad**: Debe existir una relación clara entre el requisito y los objetivos del sistema. Si el requisito de velocidad está alineado con los objetivos del sistema y es necesario para cumplir con ellos, entonces es más probable que sea realista.

Por lo tanto, aunque puedas medir que la aplicación cumple con el requisito de responder en menos de 0,3 segundos, también debes considerar si es técnicamente factible y si el costo de implementarlo es razonable. Además, debes asegurarte de que el requisito esté bien comprendido y alineado con los objetivos del sistema. Estos son aspectos adicionales que deben evaluarse para determinar si el requisito es realista.
```

Fuentes consultadas

```text
{
  "locales": [
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 11,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=11"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 76,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=76"
    },
    {
      "filename": "Ch4 Req Eng.pptx",
      "page": 76,
      "original_url": "/api/v1/documentary/sommerville/original"
    },
    {
      "filename": "nasa-handbook.pdf",
      "page": 209,
      "original_url": "/api/v1/documentary/nasa-seh/original#page=209"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 14,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=14"
    }
  ],
  "internet": []
}
```

## Intercambio 4

Pregunta

```text
¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?
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
