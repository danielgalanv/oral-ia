# Pruebas CPU: preguntas, candidatas y revisiones completas

## development

### D01

**Pregunta**

Explica si una historia debe seguir siempre una plantilla literal. Da una historia ficticia para una biblioteca y un criterio de aceptación breve.

**Respuesta sintética sometida a revisión**

La guía permite otro formato si deja claros el actor, la necesidad y la finalidad. Ejemplo ficticio: una bibliotecaria necesita localizar los préstamos pendientes para reclamar devoluciones. Un criterio de aceptación podría ser que al consultar una ficha con un préstamo pendiente aparezca ese préstamo. No hace falta imponer una redacción literal única.

**Revisión bruta del modelo**

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

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-stories

Your user stories should include enough information for your product manager to decide how important the story is. They should always include: the person using the service (the actor) what the user needs the service for (the narrative) why the user needs it (the goal) The right format for user stories They’re usually written in the format: As a… [who is the user?] I need/want/expect to… [what does the user want to do?] So that… [why does the user want to do this?] Example: The Register to vote service’s user story is ‘as a UK resident, I want to get my details on the electoral register so that I can vote’. You can use a different format, but you should always briefly explain the actor, the narrative and the goal. Focus on the goal The most important part of a user story is the goal. This helps you: make sure you’re solving the right problem decide when the story is done and a user need is met If you’re struggling to write the goal then you should reconsider why you think you need that feature. Acceptance criteria You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need. They’re often written as a list that begins with ‘it’s done when…’. Example: The acceptance criteria for the Register to vote service are: ‘it’s done when the user knows how to register online’ ‘it’s done when the user knows how to download a form to register by post’ ‘it’s done when the user knows where to send the form’ Use the acceptance criteria to link to any evidence (for example, spreadsheets or diagrams) that support the story.

#### T-docente-agil-25

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

### D02

**Pregunta**

Explica si una historia debe seguir siempre una plantilla literal. Da una historia ficticia para una biblioteca y un criterio de aceptación breve.

**Respuesta sintética sometida a revisión**

GOV.UK obliga a que toda historia use literalmente la plantilla 'Como... quiero... para...'; prohíbe otros formatos aunque expresen actor, necesidad y finalidad. Ejemplo ficticio: como bibliotecaria quiero localizar préstamos para reclamar devoluciones. Un criterio sería que aparezca el préstamo pendiente al consultar la ficha.

**Revisión bruta del modelo**

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

Error de contrato: teacher contradiction needs an exact teacher witness. No publicada.

**Pasajes proporcionados al modelo**

#### E-stories

Your user stories should include enough information for your product manager to decide how important the story is. They should always include: the person using the service (the actor) what the user needs the service for (the narrative) why the user needs it (the goal) The right format for user stories They’re usually written in the format: As a… [who is the user?] I need/want/expect to… [what does the user want to do?] So that… [why does the user want to do this?] Example: The Register to vote service’s user story is ‘as a UK resident, I want to get my details on the electoral register so that I can vote’. You can use a different format, but you should always briefly explain the actor, the narrative and the goal. Focus on the goal The most important part of a user story is the goal. This helps you: make sure you’re solving the right problem decide when the story is done and a user need is met If you’re struggling to write the goal then you should reconsider why you think you need that feature. Acceptance criteria You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need. They’re often written as a list that begins with ‘it’s done when…’. Example: The acceptance criteria for the Register to vote service are: ‘it’s done when the user knows how to register online’ ‘it’s done when the user knows how to download a form to register by post’ ‘it’s done when the user knows where to send the form’ Use the acceptance criteria to link to any evidence (for example, spreadsheets or diagrams) that support the story.

#### T-docente-agil-25

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

### D03

**Pregunta**

¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta sintética sometida a revisión**

Permite recorrer las relaciones de un requisito hacia su origen y hacia los elementos derivados relacionados. En un ejemplo inventado, RS-17 procede de N-3 y se desarrolla en el diseño DS-8: desde RS-17 encontramos N-3 y DS-8, y desde esos elementos podemos volver a localizar RS-17. Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA.

**Revisión bruta del modelo**

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

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-trace

Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.

#### T-docente-procedimiento-13

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

### D04

**Pregunta**

¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta sintética sometida a revisión**

NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre. Los hijos y los elementos derivados no deben consultarse: el material docente excluye la trazabilidad hacia adelante. En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8.

**Revisión bruta del modelo**

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

Error de contrato: teacher contradiction needs an exact teacher witness. No publicada.

**Pasajes proporcionados al modelo**

#### E-trace

Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.

#### T-docente-procedimiento-13

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

### D05

**Pregunta**

Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta sintética sometida a revisión**

Como requisito de ejemplo, proponemos un contraste mínimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, más exigente que el mínimo de 4,5:1 del criterio recibido. Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1; proponer ese valor no demuestra que una página ya lo cumpla.

**Revisión bruta del modelo**

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

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-contrast

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### T-docente-requisitos-20

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

### D06

**Pregunta**

Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta sintética sometida a revisión**

El criterio W3C recibido establece 3:1 como mínimo para texto normal de tamaño ordinario. Por tanto, para ese texto —sin ser grande, decorativo ni un logotipo— basta una relación de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

**Revisión bruta del modelo**

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

Error de contrato: 1 validation error for WebAdvisoryReview
issues.0.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='Large-scale text and ima...o contrast requirement.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long. No publicada.

**Pasajes proporcionados al modelo**

#### E-contrast

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### T-docente-requisitos-20

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

## calibration

**Intento inválido por copia con codificación equivocada. Se conserva para auditar la incidencia; no usar para comparar perfiles.**

### D02

**Pregunta**

Explica si una historia debe seguir siempre una plantilla literal. Da una historia ficticia para una biblioteca y un criterio de aceptaciÃ³n breve.

**Respuesta sintética sometida a revisión**

GOV.UK obliga a que toda historia use literalmente la plantilla 'Como... quiero... para...'; prohÃ­be otros formatos aunque expresen actor, necesidad y finalidad. Ejemplo ficticio: como bibliotecaria quiero localizar prÃ©stamos para reclamar devoluciones. Un criterio serÃ­a que aparezca el prÃ©stamo pendiente al consultar la ficha.

**Revisión bruta del modelo**

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
      "explanation": "Esto contradice la documentación que permite otros formatos siempre que se incluyan el actor, la necesidad y la finalidad. La plantilla sugerida es solo un ejemplo.",
      "evidence": [
        {
          "source_id": "E-stories",
          "quote": "Theyâ€™re usually written in the format: As aâ€¦ [who is the user?] I need/want/expect toâ€¦ [what does the user want to do?] So thatâ€¦ [why does the user want to do this?]"
        },
        {
          "source_id": "T-docente-agil-25",
          "quote": "User requirements are expressed as user stories or scenarios. These are written on cards and the development team break them down into implementation tasks."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 283797 ms.

Error de contrato: claim not literally in candidate. No publicada.

**Pasajes proporcionados al modelo**

#### E-stories

Your user stories should include enough information for your product manager to decide how important the story is. They should always include: the person using the service (the actor) what the user needs the service for (the narrative) why the user needs it (the goal) The right format for user stories Theyâ€™re usually written in the format: As aâ€¦ [who is the user?] I need/want/expect toâ€¦ [what does the user want to do?] So thatâ€¦ [why does the user want to do this?] Example: The Register to vote serviceâ€™s user story is â€˜as a UK resident, I want to get my details on the electoral register so that I can voteâ€™. You can use a different format, but you should always briefly explain the actor, the narrative and the goal. Focus on the goal The most important part of a user story is the goal. This helps you: make sure youâ€™re solving the right problem decide when the story is done and a user need is met If youâ€™re struggling to write the goal then you should reconsider why you think you need that feature. Acceptance criteria You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need. Theyâ€™re often written as a list that begins with â€˜itâ€™s done whenâ€¦â€™. Example: The acceptance criteria for the Register to vote service are: â€˜itâ€™s done when the user knows how to register onlineâ€™ â€˜itâ€™s done when the user knows how to download a form to register by postâ€™ â€˜itâ€™s done when the user knows where to send the formâ€™ Use the acceptance criteria to link to any evidence (for example, spreadsheets or diagrams) that support the story.

#### T-docente-agil-25

User stories for requirements
â€¢ In XP, a customer or user is part of the XP team and
is responsible for making decisions on requirements.
â€¢ User requirements are expressed as user stories or
scenarios.
â€¢ These are written on cards and the development
team break them down into implementation tasks.
These tasks are the basis of schedule and cost
estimates.
â€¢ The customer chooses the stories for inclusion in the
next release based on their priorities and the
schedule estimates.
Chapter 4 Agile Software Development 25

### D05

**Pregunta**

PropÃ³n un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta sintética sometida a revisión**

Como requisito de ejemplo, proponemos un contraste mÃ­nimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, mÃ¡s exigente que el mÃ­nimo de 4,5:1 del criterio recibido. Se comprobarÃ­a calculando la relaciÃ³n de contraste de los colores del texto y del fondo y contrastÃ¡ndola con 5:1; proponer ese valor no demuestra que una pÃ¡gina ya lo cumpla.

**Revisión bruta del modelo**

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "limit",
  "issues": []
}
```

Final: stop; latencia: 66593 ms.

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-contrast

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### T-docente-requisitos-20

Goals and requirements
â€¢ Non-functional requirements may be very difficult to state
precisely and imprecise requirements may be difficult to
verify.
â€¢ Differentiate between goal:
â€¢ A general intention of the user such as ease of use.
â€¢ And verifiable non-functional requirement:
â€¢ A statement using some measure that can be objectively tested.
â€¢ Goals are helpful to developers as they convey the intentions
of the system users.
30/10/2014 Chapter 4 Requirements Engineering 20

### D06

**Pregunta**

PropÃ³n un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta sintética sometida a revisión**

El criterio W3C recibido establece 3:1 como mÃ­nimo para texto normal de tamaÃ±o ordinario. Por tanto, para ese texto â€”sin ser grande, decorativo ni un logotipoâ€” basta una relaciÃ³n de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

**Revisión bruta del modelo**

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "coverage",
      "claim": "El criterio W3C establece 3:1 como mínimo para texto normal de tamaño ordinario.",
      "explanation": "El fragmento W3C menciona excepciones para texto grande, decorativo y logotipos, pero el borrador no considera estas excepciones.",
      "evidence": [
        {
          "source_id": "E-contrast",
          "quote": "Large Text, Incidental Text, or images of text that are part of an inactive user interface component, that are pure decoration, that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 199483 ms.

Error de contrato: 1 validation error for WebAdvisoryReview
issues.0.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='Large Text, Incidental T...o contrast requirement.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long. No publicada.

**Pasajes proporcionados al modelo**

#### E-contrast

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### T-docente-requisitos-20

Goals and requirements
â€¢ Non-functional requirements may be very difficult to state
precisely and imprecise requirements may be difficult to
verify.
â€¢ Differentiate between goal:
â€¢ A general intention of the user such as ease of use.
â€¢ And verifiable non-functional requirement:
â€¢ A statement using some measure that can be objectively tested.
â€¢ Goals are helpful to developers as they convey the intentions
of the system users.
30/10/2014 Chapter 4 Requirements Engineering 20

### previous-C02

**Pregunta**

Quiero que una aplicaciÃ³n de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propÃ³n un requisito hipotÃ©tico comprobable de recuperaciÃ³n y explica si redactarlo demuestra que es realizable.

**Respuesta sintética sometida a revisión**

Un requisito hipotÃ©tico comprobable de recuperaciÃ³n podrÃ­a ser: "El tiempo para reiniciar la aplicaciÃ³n despuÃ©s de un fallo no debe exceder 5 segundos en mÃ¡s del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en mÃ©tricas claras y medibles, y puede ser verificado mediante pruebas de carga y anÃ¡lisis de rendimiento. Sin embargo, su realizabilidad tambiÃ©n dependerÃ­a del presupuesto y la tecnologÃ­a disponibles, lo cual se verifica segÃºn la guÃ­a de requisitos del profesor.

Sin resultado ejecutado registrado.

## calibration-utf8

### D02

**Pregunta**

Explica si una historia debe seguir siempre una plantilla literal. Da una historia ficticia para una biblioteca y un criterio de aceptación breve.

**Respuesta sintética sometida a revisión**

GOV.UK obliga a que toda historia use literalmente la plantilla 'Como... quiero... para...'; prohíbe otros formatos aunque expresen actor, necesidad y finalidad. Ejemplo ficticio: como bibliotecaria quiero localizar préstamos para reclamar devoluciones. Un criterio sería que aparezca el préstamo pendiente al consultar la ficha.

**Revisión bruta del modelo**

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
      "explanation": "Esto contradice la información de la fuente E-stories, que permite otros formatos siempre que se incluyan el actor, la narrativa y el objetivo. La fuente T-docente-agil-25 también apoya la flexibilidad en el formato.",
      "evidence": [
        {
          "source_id": "E-stories",
          "quote": "They’re usually written in the format: As a… [who is the user?] I need/want/expect to… [what does the user want to do?] So that… [why does the user want to do this?]"
        },
        {
          "source_id": "T-docente-agil-25",
          "quote": "User requirements are expressed as user stories or scenarios."
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 274906 ms.

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-stories

Your user stories should include enough information for your product manager to decide how important the story is. They should always include: the person using the service (the actor) what the user needs the service for (the narrative) why the user needs it (the goal) The right format for user stories They’re usually written in the format: As a… [who is the user?] I need/want/expect to… [what does the user want to do?] So that… [why does the user want to do this?] Example: The Register to vote service’s user story is ‘as a UK resident, I want to get my details on the electoral register so that I can vote’. You can use a different format, but you should always briefly explain the actor, the narrative and the goal. Focus on the goal The most important part of a user story is the goal. This helps you: make sure you’re solving the right problem decide when the story is done and a user need is met If you’re struggling to write the goal then you should reconsider why you think you need that feature. Acceptance criteria You can also include a few acceptance criteria for each story. Acceptance criteria are a list of outcomes that you use as a checklist to confirm that your service has done its job and is meeting that user need. They’re often written as a list that begins with ‘it’s done when…’. Example: The acceptance criteria for the Register to vote service are: ‘it’s done when the user knows how to register online’ ‘it’s done when the user knows how to download a form to register by post’ ‘it’s done when the user knows where to send the form’ Use the acceptance criteria to link to any evidence (for example, spreadsheets or diagrams) that support the story.

#### T-docente-agil-25

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

### D05

**Pregunta**

Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta sintética sometida a revisión**

Como requisito de ejemplo, proponemos un contraste mínimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, más exigente que el mínimo de 4,5:1 del criterio recibido. Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1; proponer ese valor no demuestra que una página ya lo cumpla.

**Revisión bruta del modelo**

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "coverage",
      "claim": "El requisito propuesto no incluye la excepción para el texto grande.",
      "explanation": "El requisito debe especificar que el contraste mínimo de 5:1 no aplica para el texto grande (mayor a 18 puntos o 14 puntos en dispositivos móviles).",
      "evidence": [
        {
          "source_id": "E-contrast",
          "quote": "Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 175907 ms.

Error de contrato: claim not literally in candidate. No publicada.

**Pasajes proporcionados al modelo**

#### E-contrast

The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.

#### T-docente-requisitos-20

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

### D06

**Pregunta**

Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta sintética sometida a revisión**

El criterio W3C recibido establece 3:1 como mínimo para texto normal de tamaño ordinario. Por tanto, para ese texto —sin ser grande, decorativo ni un logotipo— basta una relación de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

Sin resultado ejecutado registrado.

### previous-C02

**Pregunta**

Quiero que una aplicación de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propón un requisito hipotético comprobable de recuperación y explica si redactarlo demuestra que es realizable.

**Respuesta sintética sometida a revisión**

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en métricas claras y medibles, y puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.

Sin resultado ejecutado registrado.

## transfer-utf8

### H01

**Pregunta**

Para una aplicación ficticia de reserva de salas, distingue verificar el producto frente a su especificación y validarlo con sus usuarios. Da un ejemplo sencillo de cada uno.

**Respuesta sintética sometida a revisión**

Verificar aporta evidencia de conformidad con lo especificado: en el ejemplo, se prueba que la aplicación impide dos reservas simultáneas de la misma sala si eso exige el requisito. Validar comprueba si el producto satisface las expectativas de los usuarios en su uso previsto: por ejemplo, observar con usuarios si les permite organizar una reunión en las condiciones reales previstas. Probar la primera propiedad no demuestra por sí solo la segunda.

**Revisión bruta del modelo**

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

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-validation

The Product Validation Process is the second of the verification and validation processes conducted on an implemented or integrated end product. While verification proves whether “the product was done right,” validation proves whether “the right product was done.” In other words, verification provides objective evidence that every “shall” statement in the requirements document or specification was met, whereas validation is performed for the benefit of the customers and users to ensure that the system functions in the expected manner when placed in the intended environment. This is achieved by examining the products of the system at every level of the product structure and comparing them to the stakeholder expectations for that level. A well-structured validation process can save cost and schedule while meeting the stakeholder expectations. System validation confirms that the integrated realized end products conform to stakeholder expectations as captured in the MOEs, MOPs, and ConOps. Validation also ensures that any anomalies discovered are appropriately resolved prior to product delivery. This section discusses the process activities, methods of validation, inputs and outputs, and potential deficiencies. See Section 2.4 for a discussion about the distinctions between Product Verification and Product Validation.

#### T-docente-requisitos-73

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

### H02

**Pregunta**

Para una aplicación ficticia de reserva de salas, distingue verificar el producto frente a su especificación y validarlo con sus usuarios. Da un ejemplo sencillo de cada uno.

**Respuesta sintética sometida a revisión**

Según NASA, verificar consiste exclusivamente en comprobar las necesidades de los usuarios y no la especificación. Validar es lo contrario: solo hay que comprobar las cláusulas del documento de requisitos, sin considerar el uso previsto ni las expectativas de los usuarios. Por eso validar la aplicación de salas no requiere tener en cuenta para qué la necesitan.

**Revisión bruta del modelo**

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

Error de contrato: 2 validation errors for WebAdvisoryReview
issues.0.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='While verification prove...e intended environment.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long
issues.1.evidence.0.quote
  String should have at most 240 characters [type=string_too_long, input_value='In other words, verifica...e intended environment.', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/string_too_long. No publicada.

**Pasajes proporcionados al modelo**

#### E-validation

The Product Validation Process is the second of the verification and validation processes conducted on an implemented or integrated end product. While verification proves whether “the product was done right,” validation proves whether “the right product was done.” In other words, verification provides objective evidence that every “shall” statement in the requirements document or specification was met, whereas validation is performed for the benefit of the customers and users to ensure that the system functions in the expected manner when placed in the intended environment. This is achieved by examining the products of the system at every level of the product structure and comparing them to the stakeholder expectations for that level. A well-structured validation process can save cost and schedule while meeting the stakeholder expectations. System validation confirms that the integrated realized end products conform to stakeholder expectations as captured in the MOEs, MOPs, and ConOps. Validation also ensures that any anomalies discovered are appropriately resolved prior to product delivery. This section discusses the process activities, methods of validation, inputs and outputs, and potential deficiencies. See Section 2.4 for a discussion about the distinctions between Product Verification and Product Validation.

#### T-docente-requisitos-73

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

### H03

**Pregunta**

Quiero descubrir necesidades de reserva de salas mediante una entrevista abierta. Propón una pregunta inicial y una de seguimiento, y explica si inducen la respuesta.

**Respuesta sintética sometida a revisión**

Una pregunta inicial ficticia sería: 'Cuéntame cómo reservaste una sala la última vez'. Después podría preguntar: '¿Qué ocurrió a continuación?'. Son abiertas y neutrales: permiten describir la experiencia sin imponer que el sistema sea bueno o malo ni adelantar una respuesta esperada. No pretenden cubrir toda la entrevista.

**Revisión bruta del modelo**

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

Error de contrato: ninguno. No publicada.

**Pasajes proporcionados al modelo**

#### E-interviews

Think about your discussion guide and get participants talking with open, neutral questions like: how do you…? what are the different ways you…? what do you think about…? Encourage them to give more detail with simple follow-up questions like: you said… when/why/who was that? can you tell me more about…? in what way…?

#### T-docente-requisitos-60

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

### H04

**Pregunta**

Quiero descubrir necesidades de reserva de salas mediante una entrevista abierta. Propón una pregunta inicial y una de seguimiento, y explica si inducen la respuesta.

**Respuesta sintética sometida a revisión**

Una entrevista abierta debe inducir la respuesta que esperamos. '¿No crees que nuestro sistema es mucho mejor?' es una pregunta abierta y neutral precisamente porque ya sugiere una valoración positiva. Como seguimiento, '¿Verdad que te resulta perfecto?' evita influir en la persona. Así cumplimos la recomendación recibida de mantener preguntas neutrales.

**Revisión bruta del modelo**

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

Error de contrato: claim not literally in candidate. No publicada.

**Pasajes proporcionados al modelo**

#### E-interviews

Think about your discussion guide and get participants talking with open, neutral questions like: how do you…? what are the different ways you…? what do you think about…? Encourage them to give more detail with simple follow-up questions like: you said… when/why/who was that? can you tell me more about…? in what way…?

#### T-docente-requisitos-60

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
