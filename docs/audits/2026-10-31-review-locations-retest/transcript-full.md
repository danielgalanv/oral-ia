# Comparación íntegra: v3 con citas frente a v5 con localizaciones

## D01

### Pregunta

Explica si una historia debe seguir siempre una plantilla literal. Da una historia ficticia para una biblioteca y un criterio de aceptación breve.

### Respuesta de control

La guía permite otro formato si deja claros el actor, la necesidad y la finalidad. Ejemplo ficticio: una bibliotecaria necesita localizar los préstamos pendientes para reclamar devoluciones. Un criterio de aceptación podría ser que al consultar una ficha con un préstamo pendiente aparezca ese préstamo. No hace falta imponer una redacción literal única.

### Revisión v3

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "explanation",
  "issues": []
}
```

Final: stop; latencia: 58718 ms.

Contrato: válido. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "La guía permite otro formato si deja claros el actor, la necesidad y la finalidad.",
      "explanation": "El fragmento 'E-stories' especifica un formato específico para las historias de usuario y sugiere que se pueden usar otros formatos solo si se incluyen claramente el actor, la necesidad y la finalidad. La afirmación del borrador implica que cualquier formato es válido siempre y cuando se cumplan estos requisitos, lo cual contradice la idea de que hay un formato preferido.",
      "evidence": [
        {
          "source_id": "E-stories"
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Un criterio de aceptación podría ser que al consultar una ficha con un préstamo pendiente aparezca ese préstamo.",
      "explanation": "El fragmento 'E-stories' menciona que los criterios de aceptación deben ser una lista de resultados que se usan como una lista de comprobación para confirmar que el servicio ha hecho su trabajo. El ejemplo dado es demasiado genérico y no proporciona suficiente detalle sobre cómo se verificará la aceptación del criterio.",
      "evidence": [
        {
          "source_id": "E-stories"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 303422 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.gov.uk/service-manual/agile-delivery/writing-user-stories

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.gov.uk/service-manual/agile-delivery/writing-user-stories

Your user stories should include enough information for your product manager to decide how important the story is. They should always include: the person using the service (the actor) what the user needs the service for (the narrative) why the user needs it (the goal) The right format for user stories They’re usually written in the format: As a… [who is the user?] I need/want/expect to… [what does the user want to do?] So that… [why does the user want to do this?] Example: The Register to vote service’s user story is ‘as a UK resident, I want to get my details on the electoral register so that I can vote’. You can use a different format, but you should always briefly explain the actor, the narrative and the goal. Focus on the goal The most important part of a user story is the goal. This helps you: make sure you’re solving the right problem decide when the story is done and a user need is met If you’re struggling to write the goal then you should reconsider why you think you need that feature. Acceptance criteria You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need. They’re often written as a list that begins with ‘it’s done when…’. Example: The acceptance criteria for the Register to vote service are: ‘it’s done when the user knows how to register online’ ‘it’s done when the user knows how to download a form to register by post’ ‘it’s done when the user knows where to send the form’ Use the acceptance criteria to link to any evidence (for example, spreadsheets or diagrams) that support the story.

#### 4 - Agil.pdf, página 25

User stories for requirements
• In XP, a customer or user is part of the XP team and
is responsible for making decisions on requirements.
• User requirements are expressed as user stories or
scenarios.
• These are written on cards and the development
team break them down into implementation tasks.
These tasks are the basis of schedule and cost
estimates.
• The customer chooses the stories for inclusion in the
next release based on their priorities and the
schedule estimates.
Chapter 4 Agile Software Development 25

## D02

### Pregunta

Explica si una historia debe seguir siempre una plantilla literal. Da una historia ficticia para una biblioteca y un criterio de aceptación breve.

### Respuesta de control

GOV.UK obliga a que toda historia use literalmente la plantilla 'Como... quiero... para...'; prohíbe otros formatos aunque expresen actor, necesidad y finalidad. Ejemplo ficticio: como bibliotecaria quiero localizar préstamos para reclamar devoluciones. Un criterio sería que aparezca el préstamo pendiente al consultar la ficha.

### Revisión v3

```json
{
  "status": "issues_found",
  "external_support": "rejected",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "GOV.UK obliga a que toda historia use literalmente la plantilla 'Como... quiero... para...'; prohíbe otros formatos aunque expresen actor, necesidad y finalidad.",
      "explanation": "La fuente no menciona que GOV.UK prohíba otros formatos. En cambio, sugiere que se pueden usar diferentes formatos siempre que se incluyan el actor, la necesidad y el objetivo. La cita del documento dice: 'You can use a different format, but you should always briefly explain the actor, the narrative and the goal.'",
      "evidence": [
        {
          "source_id": "E-stories",
          "quote": "You can use a different format, but you should always briefly explain the actor, the narrative and the goal."
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El borrador omite mencionar la importancia del criterio de aceptación, que es un aspecto crucial según la fuente.",
      "evidence": [
        {
          "source_id": "E-stories",
          "quote": "You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 285093 ms.

Contrato: teacher contradiction needs an exact teacher witness. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "GOV.UK obliga a que toda historia use literalmente la plantilla 'Como... quiero... para...'; prohíbe otros formatos",
      "explanation": "El fragmento de texto de GOV.UK no menciona que se prohíba otros formatos. En cambio, sugiere que se pueden usar diferentes formatos siempre que se incluyan el actor, la necesidad y el objetivo.",
      "evidence": [
        {
          "source_id": "E-stories"
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Un criterio sería que aparezca el préstamo pendiente al consultar la ficha",
      "explanation": "El fragmento de texto de GOV.UK no proporciona ejemplos específicos de criterios de aceptación. El criterio propuesto no está respaldado por el texto original.",
      "evidence": []
    }
  ]
}
```

Final: stop; latencia: 236093 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.gov.uk/service-manual/agile-delivery/writing-user-stories

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.gov.uk/service-manual/agile-delivery/writing-user-stories

Your user stories should include enough information for your product manager to decide how important the story is. They should always include: the person using the service (the actor) what the user needs the service for (the narrative) why the user needs it (the goal) The right format for user stories They’re usually written in the format: As a… [who is the user?] I need/want/expect to… [what does the user want to do?] So that… [why does the user want to do this?] Example: The Register to vote service’s user story is ‘as a UK resident, I want to get my details on the electoral register so that I can vote’. You can use a different format, but you should always briefly explain the actor, the narrative and the goal. Focus on the goal The most important part of a user story is the goal. This helps you: make sure you’re solving the right problem decide when the story is done and a user need is met If you’re struggling to write the goal then you should reconsider why you think you need that feature. Acceptance criteria You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need. They’re often written as a list that begins with ‘it’s done when…’. Example: The acceptance criteria for the Register to vote service are: ‘it’s done when the user knows how to register online’ ‘it’s done when the user knows how to download a form to register by post’ ‘it’s done when the user knows where to send the form’ Use the acceptance criteria to link to any evidence (for example, spreadsheets or diagrams) that support the story.

#### 4 - Agil.pdf, página 25

User stories for requirements
• In XP, a customer or user is part of the XP team and
is responsible for making decisions on requirements.
• User requirements are expressed as user stories or
scenarios.
• These are written on cards and the development
team break them down into implementation tasks.
These tasks are the basis of schedule and cost
estimates.
• The customer chooses the stories for inclusion in the
next release based on their priorities and the
schedule estimates.
Chapter 4 Agile Software Development 25

## D03

### Pregunta

¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

### Respuesta de control

Permite recorrer las relaciones de un requisito hacia su origen y hacia los elementos derivados relacionados. En un ejemplo inventado, RS-17 procede de N-3 y se desarrolla en el diseño DS-8: desde RS-17 encontramos N-3 y DS-8, y desde esos elementos podemos volver a localizar RS-17. Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA.

### Revisión v3

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "limit",
  "issues": []
}
```

Final: stop; latencia: 52889 ms.

Contrato: válido. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "RS-17 procede de N-3 y se desarrolla en el diseño DS-8",
      "explanation": "El fragmento de texto no proporciona un ejemplo específico de cómo RS-17, N-3 y DS-8 están relacionados. Además, el ejemplo no refleja la trazabilidad bidireccional, ya que no se muestra cómo se puede seguir tanto hacia arriba como hacia abajo.",
      "evidence": [
        {"source_id": "E-trace"}
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA",
      "explanation": "La afirmación sobre que los códigos no son identificadores publicados por NASA no está respaldada por ninguna fuente. El fragmento de texto no menciona nada sobre la naturaleza de estos códigos ni su relación con la NASA.",
      "evidence": []
    }
  ]
}
```

Final: stop; latencia: 237687 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.nasa.gov/reference/6-0-crosscutting-technical-management/

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.nasa.gov/reference/6-0-crosscutting-technical-management/

Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.

#### 6 - Procedimiento requisitos.pdf, página 13

Registrar problemas en los requisitos
• Objetivo: asegurar que se registran las
dependencias establecidas entre cada requisito del
software y uno o más requisitos del usuario, u otras
fuentes (trazabilidad hacia atrás) o una o varias
partes del diseño o la implementación (trazabilidad
hacia adelante)
• Riesgos de no efectuar la actividad: Fracaso del
proyecto.
30/10/2014 Chapter 4 Requirements Engineering 13

## D04

### Pregunta

¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

### Respuesta de control

NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre. Los hijos y los elementos derivados no deben consultarse: el material docente excluye la trazabilidad hacia adelante. En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8.

### Revisión v3

```json
{
  "status": "issues_found",
  "external_support": "rejected",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre.",
      "explanation": "La definición de trazabilidad bidireccional en la fuente E-trace incluye la capacidad de trazar tanto hacia adelante como hacia atrás. La afirmación del borrador contradice esto.",
      "evidence": [
        {
          "source_id": "E-trace",
          "quote": "Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations."
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El borrador omite mencionar la trazabilidad hacia adelante, que es parte integral de la definición de trazabilidad bidireccional según la fuente E-trace.",
      "evidence": [
        {
          "source_id": "E-trace",
          "quote": "Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 246172 ms.

Contrato: teacher contradiction needs an exact teacher witness. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre.",
      "explanation": "La definición de trazabilidad bidireccional en la fuente externa incluye tanto la trazabilidad hacia adelante como hacia atrás. La afirmación del estudiante contradice esto.",
      "evidence": [{"source_id": "E-trace"}]
    },
    {
      "kind": "coverage",
      "claim": "Los hijos y los elementos derivados no deben consultarse: el material docente excluye la trazabilidad hacia adelante.",
      "explanation": "La fuente externa menciona explícitamente la trazabilidad hacia adelante. La afirmación del estudiante omite esta parte crucial de la definición.",
      "evidence": [{"source_id": "E-trace"}]
    }
  ]
}
```

Final: stop; latencia: 210952 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.nasa.gov/reference/6-0-crosscutting-technical-management/

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.nasa.gov/reference/6-0-crosscutting-technical-management/

Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.

#### 6 - Procedimiento requisitos.pdf, página 13

Registrar problemas en los requisitos
• Objetivo: asegurar que se registran las
dependencias establecidas entre cada requisito del
software y uno o más requisitos del usuario, u otras
fuentes (trazabilidad hacia atrás) o una o varias
partes del diseño o la implementación (trazabilidad
hacia adelante)
• Riesgos de no efectuar la actividad: Fracaso del
proyecto.
30/10/2014 Chapter 4 Requirements Engineering 13

## D05

### Pregunta

Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

### Respuesta de control

Como requisito de ejemplo, proponemos un contraste mínimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, más exigente que el mínimo de 4,5:1 del criterio recibido. Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1; proponer ese valor no demuestra que una página ya lo cumpla.

### Revisión v3

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "explanation",
  "issues": []
}
```

Final: stop; latencia: 52125 ms.

Contrato: válido. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "El requisito propuesto es más exigente que el mínimo de 4,5:1 del criterio recibido.",
      "explanation": "El criterio W3C establece que el contraste mínimo para el texto normal es 4,5:1, excepto en casos específicos. Proporcionar un requisito de 5:1 contradice este estándar.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "El requisito propuesto no es claro sobre cómo se debe calcular el contraste.",
      "explanation": "Aunque se menciona que se debe calcular la relación de contraste, no se especifican los detalles técnicos necesarios para hacerlo de manera precisa.",
      "evidence": []
    }
  ]
}
```

Final: stop; latencia: 212562 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### 5 - Requisitos.pdf, página 20

Goals and requirements
• Non-functional requirements may be very difficult to state
precisely and imprecise requirements may be difficult to
verify.
• Differentiate between goal:
• A general intention of the user such as ease of use.
• And verifiable non-functional requirement:
• A statement using some measure that can be objectively tested.
• Goals are helpful to developers as they convey the intentions
of the system users.
30/10/2014 Chapter 4 Requirements Engineering 20

## D06

### Pregunta

Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

### Respuesta de control

El criterio W3C recibido establece 3:1 como mínimo para texto normal de tamaño ordinario. Por tanto, para ese texto —sin ser grande, decorativo ni un logotipo— basta una relación de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

### Revisión v3

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "La respuesta omite mencionar que el texto debe ser parte de un componente de interfaz inactivo, puro decorativo, invisible para todos o parte de una imagen con contenido visual significativo. Esto es importante para cumplir con el criterio W3C.",
      "evidence": [
        {
          "source_id": "E-contrast",
          "quote": "Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component, that are pure decoration, that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 173108 ms.

Contrato: 1 validation error for WebAdvisoryReview
issues.0.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='Large-scale text and ima...o contrast requirement.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "El criterio W3C establece 3:1 como mínimo para texto normal de tamaño ordinario.",
      "explanation": "Según el fragmento de W3C, el criterio es de 4.5:1 para texto normal, a menos que cumpla con las excepciones mencionadas. El texto propuesto no se ajusta a estas excepciones.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Podemos comprobarla calculando el contraste entre texto y fondo.",
      "explanation": "La afirmación es correcta pero no proporciona detalles sobre cómo realizar la verificación. Debería incluir un método específico o una herramienta para calcular el contraste.",
      "evidence": []
    }
  ]
}
```

Final: stop; latencia: 210797 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### 5 - Requisitos.pdf, página 20

Goals and requirements
• Non-functional requirements may be very difficult to state
precisely and imprecise requirements may be difficult to
verify.
• Differentiate between goal:
• A general intention of the user such as ease of use.
• And verifiable non-functional requirement:
• A statement using some measure that can be objectively tested.
• Goals are helpful to developers as they convey the intentions
of the system users.
30/10/2014 Chapter 4 Requirements Engineering 20

## H01

### Pregunta

Para una aplicación ficticia de reserva de salas, distingue verificar el producto frente a su especificación y validarlo con sus usuarios. Da un ejemplo sencillo de cada uno.

### Respuesta de control

Verificar aporta evidencia de conformidad con lo especificado: en el ejemplo, se prueba que la aplicación impide dos reservas simultáneas de la misma sala si eso exige el requisito. Validar comprueba si el producto satisface las expectativas de los usuarios en su uso previsto: por ejemplo, observar con usuarios si les permite organizar una reunión en las condiciones reales previstas. Probar la primera propiedad no demuestra por sí solo la segunda.

### Revisión v3

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "explanation",
  "issues": []
}
```

Final: stop; latencia: 65608 ms.

Contrato: válido. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Probar la primera propiedad no demuestra por sí solo la segunda.",
      "explanation": "La verificación (prueba) y la validación son procesos distintos pero complementarios. La verificación verifica que el producto cumple con la especificación, mientras que la validación asegura que el producto cumple con las expectativas de los usuarios. El borrador sugiere que probar la primera propiedad (verificación) no garantiza la segunda (validación), lo cual contradice la definición proporcionada en la fuente externa.",
      "evidence": [
        {
          "source_id": "E-validation"
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Validar comprueba si el producto satisface las expectativas de los usuarios en su uso previsto: por ejemplo, observar con usuarios si les permite organizar una reunión en las condiciones reales previstas.",
      "explanation": "La descripción de la validación es demasiado genérica y podría ser interpretada de diferentes maneras. La validación no solo implica observar a los usuarios, sino que también incluye pruebas funcionales y análisis de usabilidad. La descripción podría ser más precisa y detallada.",
      "evidence": [
        {
          "source_id": "E-validation"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 296718 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.nasa.gov/reference/5-4-product-validation/

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.nasa.gov/reference/5-4-product-validation/

The Product Validation Process is the second of the verification and validation processes conducted on an implemented or integrated end product. While verification proves whether “the product was done right,” validation proves whether “the right product was done.” In other words, verification provides objective evidence that every “shall” statement in the requirements document or specification was met, whereas validation is performed for the benefit of the customers and users to ensure that the system functions in the expected manner when placed in the intended environment. This is achieved by examining the products of the system at every level of the product structure and comparing them to the stakeholder expectations for that level. A well-structured validation process can save cost and schedule while meeting the stakeholder expectations. System validation confirms that the integrated realized end products conform to stakeholder expectations as captured in the MOEs, MOPs, and ConOps. Validation also ensures that any anomalies discovered are appropriately resolved prior to product delivery. This section discusses the process activities, methods of validation, inputs and outputs, and potential deficiencies. See Section 2.4 for a discussion about the distinctions between Product Verification and Product Validation.

#### 5 - Requisitos.pdf, página 73

Requirements checking
• Validity. Does the system provide the functions which best
support the customer’s needs?
• Consistency. Are there any requirements conflicts?
• Completeness. Are all functions required by the customer
included?
• Realism. Can the requirements be implemented given
available budget and technology
• Verifiability. Can the requirements be checked?
30/10/2014 Chapter 4 Requirements Engineering 73

## H02

### Pregunta

Para una aplicación ficticia de reserva de salas, distingue verificar el producto frente a su especificación y validarlo con sus usuarios. Da un ejemplo sencillo de cada uno.

### Respuesta de control

Según NASA, verificar consiste exclusivamente en comprobar las necesidades de los usuarios y no la especificación. Validar es lo contrario: solo hay que comprobar las cláusulas del documento de requisitos, sin considerar el uso previsto ni las expectativas de los usuarios. Por eso validar la aplicación de salas no requiere tener en cuenta para qué la necesitan.

### Revisión v3

```json
{
  "status": "issues_found",
  "external_support": "rejected",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Según NASA, verificar consiste exclusivamente en comprobar las necesidades de los usuarios y no la especificación.",
      "explanation": "Esta afirmación contradice la definición de verificación y validación proporcionada en la fuente E-validation. La verificación no solo verifica las necesidades de los usuarios, sino que también comprueba si todas las declaraciones 'deberían' en el documento de especificaciones fueron cumplidas. La validación, por otro lado, se enfoca en asegurar que el sistema funcione según las expectativas de los usuarios en su entorno previsto.",
      "evidence": [
        {
          "source_id": "E-validation",
          "quote": "While verification proves whether “the product was done right,” validation proves whether “the right product was done.” Verification provides objective evidence that every “shall” statement in the requirements document or specification was met, whereas validation is performed for the benefit of the customers and users to ensure that the system functions in the expected manner when placed in the intended environment."
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El borrador omite mencionar que la verificación también incluye la verificación de la especificación, no solo las necesidades de los usuarios. Además, no se menciona que la validación también implica considerar el uso previsto y las expectativas de los usuarios.",
      "evidence": [
        {
          "source_id": "E-validation",
          "quote": "In other words, verification provides objective evidence that every “shall” statement in the requirements document or specification was met, whereas validation is performed for the benefit of the customers and users to ensure that the system functions in the expected manner when placed in the intended environment."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 379000 ms.

Contrato: 2 validation errors for WebAdvisoryReview
issues.0.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='While verification prove...e intended environment.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long
issues.1.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='In other words, verifica...e intended environment.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "rejected",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Verificar consiste exclusivamente en comprobar las necesidades de los usuarios y no la especificación.",
      "explanation": "Esta afirmación contradice la definición proporcionada por NASA, que indica que la verificación proporciona evidencia objetiva de que todas las cláusulas en el documento de especificaciones fueron cumplidas. La verificación no se limita a las necesidades de los usuarios sino que también incluye la especificación.",
      "evidence": [
        {
          "source_id": "E-validation"
        }
      ]
    },
    {
      "kind": "contradiction",
      "claim": "Validar es lo contrario: solo hay que comprobar las cláusulas del documento de requisitos, sin considerar el uso previsto ni las expectativas de los usuarios.",
      "explanation": "Esta afirmación contradice la definición proporcionada por NASA, que indica que la validación se realiza para asegurar que el sistema funcione según las expectativas de los usuarios en el entorno previsto. La validación no se limita a comprobar solo las cláusulas del documento de requisitos, sino que también considera el uso previsto y las expectativas de los usuarios.",
      "evidence": [
        {
          "source_id": "E-validation"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 288968 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.nasa.gov/reference/5-4-product-validation/

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.nasa.gov/reference/5-4-product-validation/

The Product Validation Process is the second of the verification and validation processes conducted on an implemented or integrated end product. While verification proves whether “the product was done right,” validation proves whether “the right product was done.” In other words, verification provides objective evidence that every “shall” statement in the requirements document or specification was met, whereas validation is performed for the benefit of the customers and users to ensure that the system functions in the expected manner when placed in the intended environment. This is achieved by examining the products of the system at every level of the product structure and comparing them to the stakeholder expectations for that level. A well-structured validation process can save cost and schedule while meeting the stakeholder expectations. System validation confirms that the integrated realized end products conform to stakeholder expectations as captured in the MOEs, MOPs, and ConOps. Validation also ensures that any anomalies discovered are appropriately resolved prior to product delivery. This section discusses the process activities, methods of validation, inputs and outputs, and potential deficiencies. See Section 2.4 for a discussion about the distinctions between Product Verification and Product Validation.

#### 5 - Requisitos.pdf, página 73

Requirements checking
• Validity. Does the system provide the functions which best
support the customer’s needs?
• Consistency. Are there any requirements conflicts?
• Completeness. Are all functions required by the customer
included?
• Realism. Can the requirements be implemented given
available budget and technology
• Verifiability. Can the requirements be checked?
30/10/2014 Chapter 4 Requirements Engineering 73

## H03

### Pregunta

Quiero descubrir necesidades de reserva de salas mediante una entrevista abierta. Propón una pregunta inicial y una de seguimiento, y explica si inducen la respuesta.

### Respuesta de control

Una pregunta inicial ficticia sería: 'Cuéntame cómo reservaste una sala la última vez'. Después podría preguntar: '¿Qué ocurrió a continuación?'. Son abiertas y neutrales: permiten describir la experiencia sin imponer que el sistema sea bueno o malo ni adelantar una respuesta esperada. No pretenden cubrir toda la entrevista.

### Revisión v3

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "limit",
  "issues": []
}
```

Final: stop; latencia: 53093 ms.

Contrato: válido. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "La pregunta inicial y la de seguimiento permiten describir la experiencia sin imponer que el sistema sea bueno o malo ni adelantar una respuesta esperada.",
      "explanation": "Las preguntas propuestas pueden inducir una respuesta más limitada que la intención original. La pregunta inicial 'Cuéntame cómo reservaste una sala la última vez' puede llevar a un relato más detallado sobre el proceso de reserva, pero la pregunta de seguimiento '¿Qué ocurrió a continuación?' puede sugerir una secuencia lineal de eventos que no necesariamente refleja las necesidades de reserva de salas. Se recomienda enfocarse más en obtener información sobre las necesidades y desafíos específicos.",
      "evidence": [
        {"source_id": "E-interviews"}
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Son abiertas y neutrales: permiten describir la experiencia sin imponer que el sistema sea bueno o malo ni adelantar una respuesta esperada.",
      "explanation": "Aunque las preguntas son abiertas, podrían ser interpretadas como orientadas hacia un proceso específico de reserva de salas. Para evitar esto, se sugiere formular preguntas que se centren en las necesidades y desafíos del usuario, como '¿Cuáles son los principales desafíos que enfrentas al reservar salas?', lo que permite una discusión más amplia y relevante.",
      "evidence": [
        {"source_id": "E-interviews"},
        {"source_id": "T-docente-requisitos-60"}
      ]
    }
  ]
}
```

Final: stop; latencia: 348437 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.gov.uk/service-manual/user-research/using-in-depth-interviews
- 5 - Requisitos.pdf, página 60

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.gov.uk/service-manual/user-research/using-in-depth-interviews

Think about your discussion guide and get participants talking with open, neutral questions like: how do you…? what are the different ways you…? what do you think about…? Encourage them to give more detail with simple follow-up questions like: you said… when/why/who was that? can you tell me more about…? in what way…?

#### 5 - Requisitos.pdf, página 60

Interviewing
• Formal or informal interviews with stakeholders are part
of most RE processes.
• Types of interview
• Closed interviews based on pre-determined list of questions
• Open interviews where various issues are explored with
stakeholders.
• Effective interviewing
• Be open-minded, avoid pre-conceived ideas about the
requirements and are willing to listen to stakeholders.
• Prompt the interviewee to get discussions going using a
springboard question, a requirements proposal, or by working
together on a prototype system.
30/10/2014 Chapter 4 Requirements Engineering 60

## H04

### Pregunta

Quiero descubrir necesidades de reserva de salas mediante una entrevista abierta. Propón una pregunta inicial y una de seguimiento, y explica si inducen la respuesta.

### Respuesta de control

Una entrevista abierta debe inducir la respuesta que esperamos. '¿No crees que nuestro sistema es mucho mejor?' es una pregunta abierta y neutral precisamente porque ya sugiere una valoración positiva. Como seguimiento, '¿Verdad que te resulta perfecto?' evita influir en la persona. Así cumplimos la recomendación recibida de mantener preguntas neutrales.

### Revisión v3

```json
{
  "status": "issues_found",
  "external_support": "rejected",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "'Una entrevista abierta debe inducir la respuesta que esperamos.'",
      "explanation": "Esta afirmación contradice la naturaleza de una entrevista abierta, que busca obtener información detallada y variada sin influir en la respuesta del entrevistado. Las preguntas abiertas deben ser neutrales y evitar sugerir respuestas específicas.",
      "evidence": [
        {
          "source_id": "E-interviews",
          "quote": "Think about your discussion guide and get participants talking with open, neutral questions like: how do you…? what are the different ways you…? what do you think about…?"
        }
      ]
    },
    {
      "kind": "unsupported",
      "claim": "'¿No crees que nuestro sistema es mucho mejor?' es una pregunta abierta y neutral precisamente porque ya sugiere una valoración positiva.",
      "explanation": "La pregunta propuesta no es neutral y sugiere una valoración positiva, lo cual no es apropiado para una entrevista abierta. La pregunta debe ser más general y no incluir juicios de valor.",
      "evidence": [
        {
          "source_id": "E-interviews",
          "quote": "Encourage them to give more detail with simple follow-up questions like: you said… when/why/who was that? can you tell me more about…? in what way…?"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El borrador omite mencionar cómo se pueden formular preguntas abiertas efectivas que no induzcan respuestas específicas. Se necesita una pregunta inicial más adecuada y un seguimiento que no sugiera respuestas.",
      "evidence": [
        {
          "source_id": "E-interviews",
          "quote": "how do you…? what are the different ways you…? what do you think about…?"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 407485 ms.

Contrato: claim not literally in candidate. Publicación: deshabilitada.

### Revisión v5

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Una entrevista abierta debe inducir la respuesta que esperamos.",
      "explanation": "La cita de la fuente indica que las preguntas deben ser neutrales y evitar influir en la persona, lo cual contradice la afirmación de que se debe inducir una respuesta específica.",
      "evidence": [{"source_id": "E-interviews"}]
    },
    {
      "kind": "unsupported",
      "claim": "'¿No crees que nuestro sistema es mucho mejor?' es una pregunta abierta y neutral precisamente porque ya sugiere una valoración positiva.",
      "explanation": "Esta afirmación no está respaldada por ninguna fuente y contradice la recomendación de mantener preguntas neutrales.",
      "evidence": []
    }
  ]
}
```

Final: stop; latencia: 195609 ms.

Contrato: teacher contradiction needs a teacher source reference. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.gov.uk/service-manual/user-research/using-in-depth-interviews

Localizaciones resueltas solo para inspección; el dictamen sigue siendo inválido.

### Pasajes suministrados

#### https://www.gov.uk/service-manual/user-research/using-in-depth-interviews

Think about your discussion guide and get participants talking with open, neutral questions like: how do you…? what are the different ways you…? what do you think about…? Encourage them to give more detail with simple follow-up questions like: you said… when/why/who was that? can you tell me more about…? in what way…?

#### 5 - Requisitos.pdf, página 60

Interviewing
• Formal or informal interviews with stakeholders are part
of most RE processes.
• Types of interview
• Closed interviews based on pre-determined list of questions
• Open interviews where various issues are explored with
stakeholders.
• Effective interviewing
• Be open-minded, avoid pre-conceived ideas about the
requirements and are willing to listen to stakeholders.
• Prompt the interviewee to get discussions going using a
springboard question, a requirements proposal, or by working
together on a prototype system.
30/10/2014 Chapter 4 Requirements Engineering 60
