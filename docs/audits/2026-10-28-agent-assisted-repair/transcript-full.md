# Corrección con revisión aportada por el asistente: antes y después íntegros

Cuatro casos expuestos. El asistente aportó objeciones antes de la corrección; el14B local generó una única reparación por caso. El asistente revisó después el texto real. No es una prueba de verificación autónoma ni salida participante.

## A3

Pregunta: No entiendo si funcional/no funcional y usuario/sistema son la misma clasificación. Acláralo de otra forma.

### Antes, literal

Basándome en la evidencia proporcionada, los requisitos se pueden clasificar de diferentes maneras, pero no todas las clasificaciones son idénticas. Veamos cada uno de estos conceptos:

1. **Requisitos Funcionales vs. No Funcionales**:
   - **Funcionales**: Describen la funcionalidad o servicios del sistema. Por ejemplo, si el sistema debe permitir a los usuarios realizar transacciones, esto sería un requisito funcional.
   - **No Funcionales**: Impiden que el sistema cumpla ciertas características o limitan su operación. Por ejemplo, si el sistema debe ser capaz de manejar hasta 100 transacciones por segundo, esta sería una restricción no funcional.

2. **Requisitos de Usuario vs. Sistema**:
   - **Usuario**: Estos son requisitos escritos en lenguaje natural y diagramas que describen los servicios que el sistema proporcionará y sus restricciones operativas. Están destinados a clientes no técnicos.
   - **Sistema**: Son documentos estructurados que contienen descripciones detalladas de las funciones, servicios y restricciones operativas del sistema. Definen lo que debe implementarse y pueden formar parte de un contrato entre cliente y contratista. Están destinados a desarrolladores y clientes técnicos.

Por lo tanto, los requisitos funcionales y no funcionales son una clasificación basada en la naturaleza del requisito (si describe una funcionalidad específica o una característica general del sistema). Por otro lado, los requisitos de usuario y sistema son una clasificación basada en quién es el destinatario final del requisito (usuario final o equipo de desarrollo).

Estas son dos clasificaciones distintas y no son intercambiables.

### Objeciones del asistente, literales

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Impiden que el sistema cumpla ciertas características o limitan su operación.",
      "explanation": "Se ha invertido el significado de una restricción: los no funcionales establecen propiedades o límites que deben cumplirse, no impiden cumplir características. Corrige esa definición manteniendo los ejes de clasificación y el resto respaldado.",
      "evidence": [
        {
          "source_id": "docente-requisitos:86",
          "quote": "Non-functional requirements often constrain the system"
        }
      ]
    }
  ]
}

### Después, literal

Basándome en la evidencia proporcionada, los requisitos se pueden clasificar de diferentes maneras, pero no todas las clasificaciones son idénticas. Veamos cada uno de estos conceptos:

1. **Requisitos Funcionales vs. No Funcionales**:
   - **Funcionales**: Describen la funcionalidad o servicios del sistema. Por ejemplo, si el sistema debe permitir a los usuarios realizar transacciones, esto sería un requisito funcional.
   - **No Funcionales**: Establecen propiedades o límites que el sistema debe cumplir. Por ejemplo, si el sistema debe ser capaz de manejar hasta 100 transacciones por segundo, esta sería una restricción no funcional.

2. **Requisitos de Usuario vs. Sistema**:
   - **Usuario**: Estos son requisitos escritos en lenguaje natural y diagramas que describen los servicios que el sistema proporcionará y sus restricciones operativas. Están destinados a clientes no técnicos.
   - **Sistema**: Son documentos estructurados que contienen descripciones detalladas de las funciones, servicios y restricciones operativas del sistema. Definen lo que debe implementarse y pueden formar parte de un contrato entre cliente y contratista. Están destinados a desarrolladores y clientes técnicos.

Por lo tanto, los requisitos funcionales y no funcionales son una clasificación basada en la naturaleza del requisito (si describe una funcionalidad específica o una característica general del sistema). Por otro lado, los requisitos de usuario y sistema son una clasificación basada en quién es el destinatario final del requisito (usuario final o equipo de desarrollo).

Estas son dos clasificaciones distintas y no son intercambiables.

### Revisión posterior del asistente

{
  "target_status": "corrected",
  "observations": [
    "Elimina la inversión impiden cumplir y la sustituye por propiedades/límites que deben cumplirse.",
    "Conserva los dos ejes de clasificación y el ejemplo hipotético."
  ],
  "residual_findings": [
    "La síntesis final enfatiza destinatario más que nivel de detalle; las definiciones anteriores sí dan ese detalle. No se toma como validación exhaustiva."
  ]
}

## A4

Pregunta: Dame un ejemplo hipotético sencillo y explica cómo encaja en esas clasificaciones, sin presentarlo como garantía del sistema.

### Antes, literal

Claro, aquí tienes un ejemplo hipotético sencillo para ilustrar las diferentes clasificaciones de requisitos:

Supongamos que estamos desarrollando una aplicación móvil para un banco que permite a los clientes consultar su saldo bancario.

### Ejemplo Hipotético

#### Requisitos Funcionales
- **Consultar Saldo**: El sistema debe permitir a los usuarios consultar su saldo bancario ingresando su número de cuenta y contraseña.
- **Restricción de Acceso**: El sistema no debe permitir que un usuario acceda al saldo de otra persona.

#### Requisitos No Funcionales
- **Tiempo de Respuesta**: El sistema debe responder a una consulta de saldo en menos de 2 segundos.
- **Capacidad de Tráfico**: El sistema debe manejar hasta 1000 consultas simultáneas durante horas pico.

#### Requisitos de Usuario
- **Consultar Saldo**: En lenguaje natural, el usuario debe poder ver su saldo bancario ingresando su número de cuenta y contraseña.
- **Tiempo de Respuesta**: El sistema debe responder rápidamente a las consultas de saldo para evitar frustración del usuario.

#### Requisitos de Sistema
- **Consultar Saldo**: Se debe implementar una función que permita a los usuarios ingresar su número de cuenta y contraseña para consultar su saldo.
- **Tiempo de Respuesta**: El sistema debe estar diseñado para responder a una consulta de saldo en menos de 2 segundos.

### Explicación

- **Requisitos Funcionales**: Estos describen lo que el sistema debe hacer, como permitir a los usuarios consultar su saldo y restringir el acceso a otros saldos.
  
- **Requisitos No Funcionales**: Estos imponen restricciones sobre el rendimiento del sistema, como el tiempo de respuesta y la capacidad de tráfico.

- **Requisitos de Usuario**: Estos están escritos en lenguaje natural y describen lo que el usuario espera del sistema, como la facilidad de uso y el tiempo de respuesta.

- **Requisitos de Sistema**: Estos son documentos estructurados que detallan cómo se implementará la funcionalidad y las restricciones operativas, como la implementación de la función de consulta de saldo y el cumplimiento del tiempo de respuesta.

Este ejemplo ilustra cómo los diferentes tipos de requisitos se relacionan y complementan entre sí para definir completamente el sistema.

### Objeciones del asistente, literales

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "ambiguity",
      "claim": "Estos son documentos estructurados que detallan cómo se implementará la funcionalidad y las restricciones operativas",
      "explanation": "Confunde especificación detallada de qué debe cumplir el sistema con cómo diseñarlo/implementarlo. Corrige ese principio; conserva el escenario y las cifras explícitamente hipotéticas, que no son un error por no estar literales en RAG.",
      "evidence": [
        {
          "source_id": "docente-requisitos:7",
          "quote": "Defines what should be implemented"
        },
        {
          "source_id": "docente-requisitos:37",
          "quote": "requirements should state what the system should do,\nand the design should describe how it does this."
        }
      ]
    }
  ]
}

### Después, literal

Claro, aquí tienes un ejemplo hipotético sencillo para ilustrar las diferentes clasificaciones de requisitos:

Supongamos que estamos desarrollando una aplicación móvil para un banco que permite a los clientes consultar su saldo bancario.

### Ejemplo Hipotético

#### Requisitos Funcionales
- **Consultar Saldo**: El sistema debe permitir a los usuarios consultar su saldo bancario ingresando su número de cuenta y contraseña.
- **Restricción de Acceso**: El sistema no debe permitir que un usuario acceda al saldo de otra persona.

#### Requisitos No Funcionales
- **Tiempo de Respuesta**: El sistema debe responder a una consulta de saldo en menos de 2 segundos.
- **Capacidad de Tráfico**: El sistema debe manejar hasta 1000 consultas simultáneas durante horas pico.

#### Requisitos de Usuario
- **Consultar Saldo**: En lenguaje natural, el usuario debe poder ver su saldo bancario ingresando su número de cuenta y contraseña.
- **Tiempo de Respuesta**: El sistema debe responder rápidamente a las consultas de saldo para evitar frustración del usuario.

#### Requisitos de Sistema
- **Consultar Saldo**: Se debe implementar una función que permita a los usuarios ingresar su número de cuenta y contraseña para consultar su saldo.
- **Tiempo de Respuesta**: El sistema debe estar diseñado para responder a una consulta de saldo en menos de 2 segundos.

### Explicación

- **Requisitos Funcionales**: Estos describen lo que el sistema debe hacer, como permitir a los usuarios consultar su saldo y restringir el acceso a otros saldos.

- **Requisitos No Funcionales**: Estos imponen restricciones sobre el rendimiento del sistema, como el tiempo de respuesta y la capacidad de tráfico.

- **Requisitos de Usuario**: Estos están escritos en lenguaje natural y describen lo que el usuario espera del sistema, como la facilidad de uso y el tiempo de respuesta.

- **Requisitos de Sistema**: Estos son documentos estructurados que definen lo que debe implementarse, como la función de consulta de saldo y el cumplimiento del tiempo de respuesta.

Este ejemplo ilustra cómo los diferentes tipos de requisitos se relacionan y complementan entre sí para definir completamente el sistema.

### Revisión posterior del asistente

{
  "target_status": "corrected",
  "observations": [
    "Sustituye cómo se implementará por definen lo que debe implementarse.",
    "Conserva el escenario y2s/1000consultas como datos explícitamente hipotéticos, sin convertirlos en estándar."
  ],
  "residual_findings": [
    "El requisito de sistema del ejemplo es poco más detallado que el de usuario; es una ilustración simplificada, no una especificación completa."
  ]
}

## B1

Pregunta: ¿Qué significa validar requisitos y qué se comprueba al revisarlos?

### Antes, literal

Validar requisitos es el proceso de verificar que cumplen con ciertos criterios de calidad. Según las evidencias proporcionadas, al revisar los requisitos se comprueba:

1. **Válidos**: Que los requisitos sean válidos, es decir, que estén correctamente estructurados y contengan el contenido adecuado.
2. **Consistentes**: Que no contengan contradicciones internas ni redundancias innecesarias.
3. **Completos**: Que abarquen todos los aspectos conocidos que el sistema software debe realizar.
4. **Realistas**: Que puedan ser implementados con tecnología existente y dentro de un costo asumible.
5. **Verificables**: Que se puedan definir pruebas razonables para comprobar su cumplimiento.
6. **Comprensibles**: Que estén redactados de manera clara y sin ambigüedad.
7. **Trazables**: Que las dependencias de los requisitos estén correctamente vinculadas con otros requisitos o casos de uso.

Estas comprobaciones aseguran que los requisitos estén bien definidos, comprensibles, realistas y verificables, y que no contengan errores o ambigüedades que puedan llevar a problemas durante el desarrollo del sistema.

### Objeciones del asistente, literales

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Que los requisitos sean válidos, es decir, que estén correctamente estructurados y contengan el contenido adecuado.",
      "explanation": "Fusiona el atributo de calidad estructural Correcta de la especificación con validez. Distingue calidad de la SRS y ajuste de requisitos a las necesidades de interesados; conserva los controles respaldados sin inventar garantía de ausencia de errores.",
      "evidence": [
        {
          "source_id": "docente-procedimiento:10",
          "quote": "Correcta. Acorde a la estructura y contenidos."
        },
        {
          "source_id": "nasa-seh:71",
          "quote": "requirements and MOEs are consistent\nwith stakeholder needs;"
        }
      ]
    }
  ]
}

### Después, literal

Validar requisitos es el proceso de verificar que cumplen con ciertos criterios de calidad. Según las evidencias proporcionadas, al revisar los requisitos se comprueba:

1. **Correcta**: Que estén correctamente estructurados y contengan el contenido adecuado.
2. **Consistente internamente**: Que no contengan contradicciones internas ni redundancias innecesarias.
3. **Completa**: Que abarquen todos los aspectos conocidos que el sistema software debe realizar.
4. **Realista**: Que puedan ser implementados con tecnología existente y dentro de un costo asumible.
5. **Verificable**: Que se puedan definir pruebas razonables para comprobar su cumplimiento.
6. **Comprensible**: Que estén redactados de manera clara y sin ambigüedad.
7. **Trazable**: Que las dependencias de los requisitos estén correctamente vinculadas con otros requisitos o casos de uso.

Estas comprobaciones aseguran que los requisitos estén bien definidos, comprensibles, realistas y verificables, y que no contengan errores o ambigüedades que puedan llevar a problemas durante el desarrollo del sistema. Además, deben estar consistentes con las necesidades de los interesados.

### Revisión posterior del asistente

{
  "target_status": "partial",
  "observations": [
    "Ya no llama válidos a la estructura: cambia a Correcta.",
    "Añade consistencia con necesidades de interesados."
  ],
  "residual_findings": [
    "La primera frase sigue reduciendo validar a comprobar criterios de calidad. La separación conceptual no queda plenamente explicada.",
    "Mantiene Estas comprobaciones aseguran... que no contengan errores: garantía excesiva no eliminada.",
    "Mezcla propiedades de SRS y de requisitos individuales sin explicar el cambio de nivel."
  ]
}

## B2

Pregunta: ¿Por qué hace falta esa revisión? Explícamelo con otras palabras.

### Antes, literal

Es necesario realizar una revisión exhaustiva de los requisitos para garantizar que estos cumplan con ciertos estándares de calidad y coherencia. Esta revisión es crucial porque:

1. **Válidos y Claros**: Los requisitos deben estar correctamente estructurados y redactados de manera clara y sin ambigüedades. Esto asegura que todos los involucrados entiendan exactamente lo que se espera del sistema.

2. **Completos**: Deben abarcar todos los aspectos conocidos que el sistema debe realizar. Si algo importante se omite, puede resultar en un sistema incompleto o inservible.

3. **Consistentes**: No deben contener contradicciones internas ni redundancias innecesarias. Esto ayuda a evitar confusiones y malentendidos durante el desarrollo.

4. **Realistas**: Los requisitos deben ser factibles de implementar con la tecnología disponible y dentro de un costo razonable. Si no son realistas, pueden llevar a proyectos costosos e imposibles de completar.

5. **Verificables**: Deben poder definirse pruebas para comprobar si se cumplen o no. Esto permite asegurar que el sistema final satisfaga realmente las necesidades establecidas.

6. **Trasladables**: La procedencia de cada requerimiento debe estar claramente establecida. Esto facilita rastrear y gestionar cambios en los requisitos.

7. **Adaptables**: Los requisitos deben poder modificarse sin causar grandes impactos en otros requisitos. Esto permite adaptarse a cambios inevitables en el proyecto.

En resumen, esta revisión asegura que los requisitos estén bien definidos, comprensibles, realistas y verificables, y que no contengan errores o ambigüedades que puedan llevar a problemas durante el desarrollo del sistema.

### Objeciones del asistente, literales

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "ambiguity",
      "claim": "Trasladables",
      "explanation": "La propiedad que describes como procedencia es trazabilidad, no trasladabilidad. Corrige el nombre sin convertirlo en otra propiedad ni añadir contenido ajeno.",
      "evidence": [
        {
          "source_id": "docente-requisitos:76",
          "quote": "Traceability"
        }
      ]
    },
    {
      "kind": "overclaim",
      "claim": "esta revisión asegura",
      "explanation": "Presenta la revisión como garantía de requisitos sin errores. Los controles revisan propiedades; no acreditan que la revisión concreta haya eliminado todo error. Expresa finalidad o contribución en vez de garantía absoluta.",
      "evidence": [
        {
          "source_id": "docente-requisitos:76",
          "quote": "Is the requirement realistically testable?"
        }
      ]
    }
  ]
}

### Después, literal

Es necesario realizar una revisión exhaustiva de los requisitos para garantizar que estos cumplan con ciertos estándares de calidad y coherencia. Esta revisión es crucial porque:

1. **Válidos y Claros**: Los requisitos deben estar correctamente estructurados y redactados de manera clara y sin ambigüedades. Esto asegura que todos los involucrados entiendan exactamente lo que se espera del sistema.

2. **Completos**: Deben abarcar todos los aspectos conocidos que el sistema debe realizar. Si algo importante se omite, puede resultar en un sistema incompleto o inservible.

3. **Consistentes**: No deben contener contradicciones internas ni redundancias innecesarias. Esto ayuda a evitar confusiones y malentendidos durante el desarrollo.

4. **Realistas**: Los requisitos deben ser factibles de implementar con la tecnología disponible y dentro de un costo razonable. Si no son realistas, pueden llevar a proyectos costosos e imposibles de completar.

5. **Verificables**: Deben poder definirse pruebas para comprobar si se cumplen o no. Esto permite asegurar que el sistema final satisfaga realmente las necesidades establecidas.

6. **Trazables**: La procedencia de cada requerimiento debe estar claramente establecida. Esto facilita rastrear y gestionar cambios en los requisitos.

7. **Adaptables**: Los requisitos deben poder modificarse sin causar grandes impactos en otros requisitos. Esto permite adaptarse a cambios inevitables en el proyecto.

En resumen, esta revisión contribuye a asegurar que los requisitos estén bien definidos, comprensibles, realistas y verificables, y que no contengan errores o ambigüedades que puedan llevar a problemas durante el desarrollo del sistema.

### Revisión posterior del asistente

{
  "target_status": "partial",
  "observations": [
    "Trasladables pasa a Trazables.",
    "El cierre pasa de asegura a contribuye a asegurar, reduciendo su carácter absoluto."
  ],
  "residual_findings": [
    "Mantiene la equivalencia inicial de Válidos y Claros con estar correctamente estructurados.",
    "Permite asegurar que el sistema final satisfaga realmente las necesidades a partir de verificabilidad sigue confundiendo prueba/verificación y validación.",
    "La revisión sigue siendo redundante; no se declara una respuesta sin defectos."
  ]
}
