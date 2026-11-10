# Comparación completa de revisores GPU — 31-10-2026

Casos de desarrollo ya expuestos; no son reserva ni evaluación humana. Los ejemplos D03 y D05 son adecuados. No se modifican sus datos para satisfacer al revisor.

## qwen25-7b

### D03

**Pregunta**: ¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta revisada**: Permite recorrer las relaciones de un requisito hacia su origen y hacia los elementos derivados relacionados. En un ejemplo inventado, RS-17 procede de N-3 y se desarrolla en el diseño DS-8: desde RS-17 encontramos N-3 y DS-8, y desde esos elementos podemos volver a localizar RS-17. Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA.

**Salida íntegra del revisor**:
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
      "explanation": "La trazabilidad bidireccional permite seguir tanto hacia arriba como hacia abajo, pero no especifica que un requisito derive directamente de otro o se desarrolle en un diseño específico. La afirmación sobre el origen y desarrollo de RS-17 no está respaldada por la fuente.",
      "evidence": [
        {
          "source_id": "E-trace"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA",
      "explanation": "El fragmento de la fuente no menciona que los códigos no sean identificadores publicados por NASA. Esto podría ser un error en la interpretación del borrador.",
      "evidence": []
    }
  ]
}
```

**Contrato**: source reference required.

**Contraste técnico**: Rechazo falso: exige respaldo para códigos y relaciones expresamente ficticios; además critica la declaración de ficción.

**Fuentes recibidas**:

- E-trace: Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.
- T-docente-procedimiento-13: Registrar problemas en los requisitos
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

**Pregunta**: ¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta revisada**: NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre. Los hijos y los elementos derivados no deben consultarse: el material docente excluye la trazabilidad hacia adelante. En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8.

**Salida íntegra del revisor**:
```json
{
  "status": "issues_found",
  "external_support": "rejected",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "NASA defines bidirectional traceability as following only the link to the parent requirement. Children and derived elements should not be consulted: the material docent excludes forward traceability.",
      "explanation": "The provided definition from NASA actually supports bidirectional traceability, which allows tracing both to parent and child requirements. The statement is contradictory to the given definition.",
      "evidence": [
        {
          "source_id": "E-trace"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "In the example, it is enough to have RS-17 towards N-3, and it is forbidden to relate it with the design DS-8.",
      "explanation": "The example does not cover the full scope of bidirectional traceability, which involves tracing both to parent and child requirements. The statement is too limited and does not reflect the complete concept of bidirectional traceability.",
      "evidence": []
    }
  ]
}
```

**Contrato**: source reference required.

**Contraste técnico**: Identifica la reducción falsa a padres, pero añade coverage sin referencia; declara conflicto docente sin citarlo. No es una revisión utilizable completa.

**Fuentes recibidas**:

- E-trace: Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.
- T-docente-procedimiento-13: Registrar problemas en los requisitos
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

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta revisada**: Como requisito de ejemplo, proponemos un contraste mínimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, más exigente que el mínimo de 4,5:1 del criterio recibido. Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1; proponer ese valor no demuestra que una página ya lo cumpla.

**Salida íntegra del revisor**:
```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "coverage",
      "claim": "El requisito propuesto es un umbral ficticio más exigente que el mínimo de 4,5:1 del criterio recibido.",
      "explanation": "El requisito propuesto no se ajusta al criterio W3C, que establece un mínimo de 4,5:1 para el contraste de texto y no-texto, y 3:1 para el texto grande. Proporcionar un umbral más exigente no es adecuado para un requisito no funcional comprobable.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    },
    {
      "kind": "contradiction",
      "claim": "Se propone un contraste mínimo de 5:1 entre el texto normal y su fondo como un requisito no funcional comprobable.",
      "explanation": "El criterio W3C establece un mínimo de 4,5:1 para el contraste de texto y no-texto, y 3:1 para el texto grande. Proporcionar un umbral más exigente contradice el criterio W3C.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    }
  ]
}
```

**Contrato**: Válido.

**Contraste técnico**: Rechazo falso: afirma que un umbral hipotético más exigente contradice un mínimo; confunde mínimo y valor exacto.

**Fuentes recibidas**:

- E-contrast: The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.
- T-docente-requisitos-20: Goals and requirements
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

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta revisada**: El criterio W3C recibido establece 3:1 como mínimo para texto normal de tamaño ordinario. Por tanto, para ese texto —sin ser grande, decorativo ni un logotipo— basta una relación de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

**Salida íntegra del revisor**:
```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "coverage",
      "claim": "El requisito no funcional propuesto solo menciona la relación de contraste mínima de 3:1, pero no especifica cómo se debe calcular o medir.",
      "explanation": "El requisito no funcional debe ser comprobable y medible. Debe incluir una descripción clara de cómo se debe calcular el contraste entre el texto y el fondo.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "La frase 'Podemos comprobarla calculando el contraste entre texto y fondo' es ambigua y no es suficiente para garantizar que el requisito sea comprobable.",
      "explanation": "Se debe proporcionar una descripción clara y detallada de cómo se debe realizar la prueba de contraste, incluyendo el método de cálculo y las herramientas que se pueden usar.",
      "evidence": [
        {
          "source_id": "E-contrast"
        }
      ]
    }
  ]
}
```

**Contrato**: Válido.

**Contraste técnico**: No detecta la atribución falsa de 3:1 a texto normal. Pide procedimiento y herramientas opcionales; no cuenta como detección correcta por emitir issues_found.

**Fuentes recibidas**:

- E-contrast: The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.
- T-docente-requisitos-20: Goals and requirements
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

## qwen3-8b-nonthinking

### D03

**Pregunta**: ¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta revisada**: Permite recorrer las relaciones de un requisito hacia su origen y hacia los elementos derivados relacionados. En un ejemplo inventado, RS-17 procede de N-3 y se desarrolla en el diseño DS-8: desde RS-17 encontramos N-3 y DS-8, y desde esos elementos podemos volver a localizar RS-17. Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA.

**Salida íntegra del revisor**:
```json
{"status":"no_issues_found","external_support":"supported","teacher_compatibility":"compatible","response_action":"explanation","issues":[]}
```

**Contrato**: Válido.

**Contraste técnico**: Aceptación adecuada de la definición y del ejemplo hipotético.

**Fuentes recibidas**:

- E-trace: Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.
- T-docente-procedimiento-13: Registrar problemas en los requisitos
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

**Pregunta**: ¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta revisada**: NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre. Los hijos y los elementos derivados no deben consultarse: el material docente excluye la trazabilidad hacia adelante. En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8.

**Salida íntegra del revisor**:
```json
{"status":"issues_found","external_support":"rejected","teacher_compatibility":"conflict","response_action":"explanation","issues":[{"kind":"contradiction","claim":"La trazabilidad bidireccional se limita a seguir únicamente el enlace al requisito padre","explanation":"La fuente externa define la trazabilidad bidireccional como la capacidad de rastrear un requisito hacia su padre y hacia sus hijos, mientras que el material docente afirma lo contrario. Esto crea una contradicción académica.","evidence":[{"source_id":"E-trace"},{"source_id":"T-docente-procedimiento-13"}]},{"kind":"overclaim","claim":"En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8","explanation":"La afirmación de que no se debe relacionar con el diseño es una suposición no respaldada por la fuente docente, que menciona trazabilidad hacia adelante (diseño). Por lo tanto, se excede del marco definido.","evidence":[{"source_id":"T-docente-procedimiento-13"}]}]}
```

**Contrato**: 1 validation error for ReferenceReview
  Value error, repair action and issues must agree [type=value_error, input_value={'status': 'issues_found'...e-procedimiento-13'}]}]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/value_error.

**Contraste técnico**: Detecta la limitación falsa a padres, pero atribuye al profesor una exclusión que solo estaba en el borrador. Las dos fuentes son compatibles. También emite explanation con issues_found, fuera de contrato.

**Fuentes recibidas**:

- E-trace: Requirements management activities apply to the management of all stakeholder expectations, customer requirements, and technical product requirements down to the lowest level product component requirements (hereafter referred to as expectations and requirements). This includes physical functional and operational requirements, including those that result from interfaces between the systems in question and other external entities and environments. The Requirements Management Process is used to: Identify, control, decompose, and allocate requirements across all levels of the WBS. Provide bidirectional traceability. Manage the changes to established requirement baselines over the life cycle of the system products. Definitions Traceability: A discernible association between two or more logical entities such as requirements, system elements, verifications, or tasks. Bidirectional traceability: The ability to trace any given requirement/expectation to its parent requirement/expectation and to its allocated children requirements/expectations.
- T-docente-procedimiento-13: Registrar problemas en los requisitos
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

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta revisada**: Como requisito de ejemplo, proponemos un contraste mínimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, más exigente que el mínimo de 4,5:1 del criterio recibido. Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1; proponer ese valor no demuestra que una página ya lo cumpla.

**Salida íntegra del revisor**:
```json
{"status":"issues_found","external_support":"rejected","teacher_compatibility":"conflict","response_action":"explanation","issues":[{"kind":"overclaim","claim":"Propone un contraste mínimo de 5:1 entre el texto normal y su fondo","explanation":"La afirmación de que se propone un umbral ficticio del proyecto (5:1) no está respaldada por la fuente externa W3C, que establece un mínimo de 4.5:1 para texto normal. La propuesta de un valor más exigente no puede considerarse un requisito comprobable sin evidencia de su adopción o justificación.","evidence":[{"source_id":"E-contrast"}]},{"kind":"unsupported","claim":"Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1","explanation":"Esta afirmación no está respaldada por la fuente externa, que no menciona el cálculo de contraste como requisito verificable para texto normal. La fuente W3C no establece un método de verificación para umbrales no oficiales.","evidence":[{"source_id":"E-contrast"}]}]}
```

**Contrato**: 1 validation error for ReferenceReview
  Value error, repair action and issues must agree [type=value_error, input_value={'status': 'issues_found'...e_id': 'E-contrast'}]}]}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.14/v/value_error.

**Contraste técnico**: Rechazo falso del umbral hipotético 5:1. Exige adopción documental de una ficción coherente y declara conflicto docente sin apoyo. También incumple la acción de reparación.

**Fuentes recibidas**:

- E-contrast: The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.
- T-docente-requisitos-20: Goals and requirements
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

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta revisada**: El criterio W3C recibido establece 3:1 como mínimo para texto normal de tamaño ordinario. Por tanto, para ese texto —sin ser grande, decorativo ni un logotipo— basta una relación de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

**Salida íntegra del revisor**:
```json
{"status":"no_issues_found","external_support":"supported","teacher_compatibility":"compatible","response_action":"explanation","issues":[]}
```

**Contrato**: Válido.

**Contraste técnico**: Aceptación falsa: el texto normal no tiene mínimo 3:1 en el pasaje; corresponde 4,5:1. No se está juzgando aquí la excepción de texto grande.

**Fuentes recibidas**:

- E-contrast: The visual presentation of text and images of text has a contrast ratio of at least 4.5:1, except for the following: Large Text Large-scale text and images of large-scale text have a contrast ratio of at least 3:1; Incidental Text or images of text that are part of an inactive user interface component , that are pure decoration , that are not visible to anyone, or that are part of a picture that contains significant other visual content, have no contrast requirement. Logotypes Text that is part of a logo or brand name has no contrast requirement.
- T-docente-requisitos-20: Goals and requirements
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
