# ORALIA — registro descriptivo de autoestudio

Sesión: 572fb533-6970-4f65-9b5c-ea1dd11b4b65

Generado: 2026-11-04T08:02:02.878974+00:00

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
En una aplicación de reservas propongo que la búsqueda responda en menos de 0,3 segundos. Es un valor inventado para el ejemplo. ¿Qué tipo de requisito es y por qué?
```

Respuesta mostrada

```text
La propuesta de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos es un requisito no funcional. Este tipo de requisito se refiere a las características del sistema que no describen directamente lo que el sistema debe hacer, sino cómo debe hacerlo o cómo debe comportarse. Según la tabla de métricas para especificar requisitos no funcionales en la fuente proporcionada, la velocidad es uno de los aspectos que se pueden medir para especificar estos requisitos. La velocidad puede incluir el tiempo de respuesta del usuario o el tiempo de respuesta a eventos, que en este caso sería el tiempo que tarda el sistema en procesar una solicitud de búsqueda y devolver una respuesta.

Este requisito específico de velocidad se relaciona con la propiedad de "Speed" (Velocidad) en la tabla de métricas, donde se menciona el "User/event response time" (Tiempo de respuesta del usuario/a evento). Por lo tanto, el requisito de que la búsqueda responda en menos de 0,3 segundos es un requisito no funcional que especifica un límite de tiempo para la respuesta del sistema a una solicitud de búsqueda, asegurando que sea rápida y eficiente desde la perspectiva del usuario.
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
Para comprobar que la búsqueda en una aplicación de reservas responde en menos de 0,3 segundos, se deben seguir los siguientes pasos:

1. **Preparación**: Configurar un entorno de prueba adecuado que simule las condiciones de uso real. Esto incluye tener una base de datos con datos representativos de los que se encontrarían en producción, así como un servidor y una red configurados para reflejar las condiciones típicas de uso.

2. **Ejecución de pruebas**: Realizar múltiples búsquedas en la aplicación de reservas utilizando diferentes términos de búsqueda y en diferentes momentos de carga del sistema. Esto ayuda a garantizar que la aplicación cumple con el requisito en una variedad de situaciones.

3. **Medición del tiempo de respuesta**: Utilizar herramientas de medición de rendimiento para registrar el tiempo que tarda la aplicación en responder a cada solicitud de búsqueda. Estas herramientas pueden ser integradas en la aplicación o utilizarse desde fuera, como navegadores web con extensiones de medición de tiempo de respuesta, o herramientas de pruebas automatizadas.

4. **Análisis de resultados**: Analizar los tiempos de respuesta registrados para determinar si cumplen con el requisito de ser menores a 0,3 segundos. Si todos los tiempos de respuesta cumplen con este requisito, entonces se puede considerar que el requisito se ha cumplido.

5. **Replicabilidad**: Repetir las pruebas varias veces para asegurar que los resultados no son producto de condiciones atípicas o fluctuaciones temporales. Esto implica realizar pruebas durante diferentes momentos del día y bajo diferentes cargas de trabajo.

6. **Documentación**: Registrar todos los detalles de las pruebas, incluyendo el entorno de prueba, los términos de búsqueda utilizados, los tiempos de respuesta medidos y cualquier otra información relevante. Esta documentación será útil para la auditoría y para futuras revisiones del requisito.

Estos pasos aseguran que el requisito de velocidad se cumple de manera consistente y que se puede demostrar de manera objetiva que la aplicación de reservas responde a las solicitudes de búsqueda en menos de 0,3 segundos.
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
La capacidad de medir si una aplicación de reservas responde a las solicitudes de búsqueda en menos de 0,3 segundos no garantiza automáticamente que el requisito sea realista. La medición es una parte importante del proceso de validación, pero hay otros factores que también deben considerarse para determinar la realidad del requisito.

Según las fuentes proporcionadas, un requisito debe ser no sólo medible, sino también:

1. **Comprensible**: Debe estar redactado de manera que sea fácilmente comprensible.
2. **No ambiguo**: Debe poder interpretarse de una sola manera.
3. **Gramaticalmente y ortográficamente correcto**.
4. **Realizable**: Debe ser posible implementarlo con tecnología existente y dentro de un costo asumible.
5. **Comprobable**: Debe ser posible definir pruebas que sean razonables en términos de coste y tiempo.
6. **Trazable**: Debe haber una clara trazabilidad hacia otros requisitos o casos de uso.

Además, según la guía de la NASA, un requisito debe ser técnicamente factible y sus especificaciones de rendimiento deben ser realistas. Esto significa que aunque podamos medir si el sistema cumple con el requisito de velocidad, también debemos considerar si es técnicamente posible implementar tal velocidad con los recursos disponibles y si el requisito tiene sentido en el contexto del proyecto.

Por lo tanto, aunque la medición es crucial, también es necesario evaluar la viabilidad técnica y la factibilidad económica del requisito. Si bien podemos verificar que el sistema cumple con el requisito de velocidad, también debemos asegurarnos de que sea factible implementarlo y mantenerlo en términos de recursos y costos.
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

Respuesta mostrada

```text
Antes de aceptar el requisito de que la búsqueda en una aplicación de reservas responda en menos de 0,3 segundos, es necesario revisar varios aspectos con el cliente para asegurar que el requisito cumpla con los estándares de calidad y sea realista. Aquí están los puntos clave que deberías abordar:

1. **Comprensibilidad y Claridad**:
   - Asegúrate de que el requisito esté redactado de manera que sea fácilmente comprensible para el cliente. Esto implica que el cliente entienda exactamente lo que se espera de la aplicación en términos de velocidad de respuesta.

2. **No Ambigüedad**:
   - Verifica que el requisito no tenga ambigüedades y que pueda interpretarse de una sola manera. Esto evitará malentendidos futuros sobre lo que se espera del sistema.

3. **Realizabilidad**:
   - Evalúa si es técnicamente posible implementar este requisito con la tecnología disponible y dentro del presupuesto acordado. Esto implica discutir con el equipo técnico si es viable alcanzar una velocidad de respuesta tan rápida.

4. **Comprobabilidad**:
   - Determina si es posible definir pruebas que sean razonables en términos de coste y tiempo para verificar que el sistema cumple con el requisito. Esto incluye la posibilidad de medir y probar la velocidad de respuesta de manera consistente y precisa.

5. **Trazabilidad**:
   - Asegúrate de que el requisito esté trazado hacia otros requisitos o casos de uso relevantes. Esto facilitará la gestión y seguimiento del requisito a lo largo del desarrollo del sistema.

6. **Feasibilidad**:
   - Discute con el cliente si el requisito es técnicamente factible y si puede ser implementado dado el presupuesto y la tecnología disponibles. Esto implica evaluar si el requisito tiene sentido en el contexto del proyecto y si es posible mantenerlo a largo plazo.

7. **Validación de Necesidades**:
   - Verifica que el sistema proporcionará las funciones que mejor satisfacen las necesidades del cliente. Esto implica asegurarte de que el requisito de velocidad de búsqueda responde a una necesidad real del cliente y no es simplemente una exigencia abstracta.

8. **Consistencia**:
   - Evalúa si hay conflictos con otros requisitos ya establecidos. Esto implica asegurarse de que el nuevo requisito no entra en conflicto con otros requisitos previamente acordados.

9. **Complejidad**:
   - Asegúrate de que todas las funciones requeridas por el cliente estén incluidas. Esto implica revisar si el requisito de velocidad de búsqueda cubre todas las necesidades del cliente y no deja ninguna funcionalidad pendiente.

10. **Verificabilidad**:
    - Determina si el requisito puede ser verificado después de que el producto final esté implementado. Esto implica asegurarse de que el requisito esté formulado de manera que pueda ser probado y comprobado de manera efectiva.

Revisar estos puntos con el cliente ayudará a garantizar que el requisito de velocidad de búsqueda sea claro, comprensible, técnicamente factible, y que satisfaga las necesidades del cliente.
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
      "page": 73,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=73"
    },
    {
      "filename": "6 - Procedimiento requisitos.pdf",
      "page": 12,
      "original_url": "/api/v1/documentary/docente-procedimiento/original#page=12"
    },
    {
      "filename": "nasa-handbook.pdf",
      "page": 70,
      "original_url": "/api/v1/documentary/nasa-seh/original#page=70"
    },
    {
      "filename": "5 - Requisitos.pdf",
      "page": 76,
      "original_url": "/api/v1/documentary/docente-requisitos/original#page=76"
    }
  ],
  "internet": []
}
```
