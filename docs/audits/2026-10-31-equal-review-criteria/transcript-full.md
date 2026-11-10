# Comparación íntegra: v5 frente a v6 con criterio común

## D03

### Pregunta

¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

### Respuesta de control

Permite recorrer las relaciones de un requisito hacia su origen y hacia los elementos derivados relacionados. En un ejemplo inventado, RS-17 procede de N-3 y se desarrolla en el diseño DS-8: desde RS-17 encontramos N-3 y DS-8, y desde esos elementos podemos volver a localizar RS-17. Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA.

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

### Revisión v6

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "none",
  "issues": []
}
```

Final: stop; latencia: 66077 ms.

Contrato: 1 validation error for ReferenceReview
response_action
  Input should be 'explanation', 'limit' or 'repair' [type=literal_error, input_value='none', input_type=str]
    For further information visit https://errors.pydantic.dev/2.13/v/literal_error. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):


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

### Revisión v6

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
      "explanation": "La definición de trazabilidad bidireccional en la fuente E-trace incluye tanto la trazabilidad hacia adelante como hacia atrás. La afirmación del borrador contradice esto.",
      "evidence": [
        {
          "source_id": "E-trace"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8.",
      "explanation": "La definición de trazabilidad bidireccional en la fuente E-trace implica que se pueden trazar tanto hacia adelante como hacia atrás. Por lo tanto, el ejemplo debe incluir tanto la trazabilidad hacia adelante como hacia atrás.",
      "evidence": [
        {
          "source_id": "E-trace"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 258016 ms.

Contrato: teacher conflict needs a teacher source reference. Publicación: deshabilitada.

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

### Revisión v6

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "limit",
  "issues": [
    {
      "kind": "coverage",
      "claim": "El requisito propuesto es un umbral ficticio más exigente que el mínimo de 4,5:1 del criterio recibido.",
      "explanation": "El requisito propuesto no se ajusta al criterio W3C, que establece un mínimo de 4,5:1 para el contraste de texto normal. Proporcionar un umbral más exigente puede no ser apropiado si se desea cumplir con el estándar W3C.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    },
    {
      "kind": "contradiction",
      "claim": "Se propone un contraste mínimo de 5:1 entre el texto normal y su fondo, sin mencionar excepciones.",
      "explanation": "Según el criterio W3C, hay excepciones para el contraste de texto, como el texto grande y los elementos decorativos. No mencionar estas excepciones puede llevar a una interpretación incorrecta del requisito.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 262202 ms.

Contrato: 1 validation error for ReferenceReview
  Value error, repair action and issues must agree [type=value_error, input_value={'status': 'issues_found'...e_id': 'E-contrast'}]}]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.13/v/value_error. Publicación: deshabilitada.

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

### Revisión v6

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "coverage",
      "claim": "El requisito propuesto es 3:1 para texto normal de tamaño ordinario.",
      "explanation": "La fuente W3C indica que el mínimo requerido es 4.5:1 para texto normal, a menos que cumpla con otras excepciones. La propuesta omite esta información crucial.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    },
    {
      "kind": "contradiction",
      "claim": "Basta una relación de 3:1 para cumplir el criterio W3C.",
      "explanation": "Según la fuente W3C, el mínimo requerido es 4.5:1 para el contraste de texto normal, a menos que cumpla con las excepciones mencionadas. La afirmación de que 3:1 es suficiente contradice la normativa W3C.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    }
  ]
}
```

Final: stop; latencia: 226014 ms.

Contrato: válido. Publicación: deshabilitada.

Referencias señaladas por el revisor (no acreditan por sí mismas su juicio):

- https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html

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
