# ORALIA — registro descriptivo de autoestudio

Sesión: 087a0227-0c08-4991-a842-10a12b43663b

Generado: 2026-11-03T12:05:49.954557+00:00

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
¿Qué tendríamos que revisar con el cliente antes de aceptar ese requisito?
```

Respuesta mostrada

```text
Antes de aceptar el requisito de que la aplicación de reservas responda a las búsquedas en menos de 0,3 segundos, sería necesario revisar varios aspectos con el cliente para garantizar que el requisito es adecuado y factible. Aquí están algunos puntos clave a considerar:

1. **Necesidad del Cliente**: Comprobar que el cliente realmente necesita que la aplicación responda tan rápidamente. Esto implica entender el contexto de uso y las expectativas del cliente. Por ejemplo, si el cliente opera en un entorno donde la rapidez de respuesta es crítica, como en un servicio de atención al cliente en tiempo real, entonces este requisito podría ser muy apropiado.

2. **Impacto en el Diseño y Desarrollo**: Evaluar si el requisito es factible desde el punto de vista técnico. Esto incluye considerar si el equipo tiene la capacidad técnica para implementar tal velocidad de respuesta, y si el sistema actual o futuro puede manejar esta carga de trabajo. Por ejemplo, si el sistema actual no tiene la capacidad de procesar solicitudes tan rápidamente, podría requerir inversiones significativas en hardware o software.

3. **Costo y Beneficio**: Analizar el costo asociado con cumplir con este requisito frente a los beneficios que proporcionará. Un requisito de velocidad tan estricto podría aumentar el costo del desarrollo debido a la necesidad de optimización adicional o la adquisición de recursos adicionales. El cliente debe estar dispuesto a asumir este costo.

4. **Prioridades del Cliente**: Determinar si este requisito es una prioridad para el cliente en relación con otros requisitos. Si hay otros requisitos que son igualmente importantes o más críticos, el cliente podría preferir enfocarse en ellos primero.

5. **Flexibilidad y Adaptabilidad**: Considerar si el requisito permite cierta flexibilidad en caso de cambios futuros. Un requisito demasiado específico o rígido podría dificultar la adaptación del sistema a nuevas necesidades o tecnologías en el futuro.

6. **Medición y Monitoreo**: Establecer cómo se medirá y verificará el cumplimiento del requisito una vez implementado. Esto incluye definir las herramientas y métodos de medición, así como los procedimientos para monitorear el rendimiento continuamente.

7. **Impacto en la Experiencia del Usuario**: Evaluar cómo este requisito afectará la experiencia del usuario. Una aplicación que responde rápidamente puede mejorar la satisfacción del usuario, pero también es importante considerar otros aspectos de la experiencia, como la facilidad de uso y la funcionalidad.

Estas revisiones ayudarán a asegurar que el requisito de velocidad es adecuado, factible y beneficioso para el cliente y el usuario final.
```

Fuentes consultadas

```text
{
  "locales": [
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
    }
  ],
  "internet": []
}
```
