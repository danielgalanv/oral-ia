# Variante de decisión única — transcripción íntegra

Mismos casos de desarrollo expuestos, sin etiquetas esperadas ni críticas humanas en el prompt. No es reserva nueva.

## D03

**Pregunta**: ¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta revisada**: Permite recorrer las relaciones de un requisito hacia su origen y hacia los elementos derivados relacionados. En un ejemplo inventado, RS-17 procede de N-3 y se desarrolla en el diseño DS-8: desde RS-17 encontramos N-3 y DS-8, y desde esos elementos podemos volver a localizar RS-17. Los códigos solo ilustran las relaciones; no son identificadores publicados por NASA.

**Salida original del revisor**:
```json
{"status":"no_issues_found","issues":[]}
```

**Derivación mecánica del host**:
```json
{
  "status": "no_issues_found",
  "external_support": "unknown",
  "teacher_compatibility": "unknown",
  "response_action": "explanation",
  "issues": []
}
```

**Contraste técnico**: Adecuada: acepta definición y códigos ficticios coherentes.

**Pasajes recibidos**:

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

## D04

**Pregunta**: ¿Qué significa trazabilidad bidireccional? Pon un ejemplo hipotético con identificadores inventados sin describir un proyecto completo.

**Respuesta revisada**: NASA define la trazabilidad bidireccional como seguir únicamente el enlace al requisito padre. Los hijos y los elementos derivados no deben consultarse: el material docente excluye la trazabilidad hacia adelante. En el ejemplo ficticio basta RS-17 hacia N-3, y queda prohibido relacionarlo con el diseño DS-8.

**Salida original del revisor**:
```json
{"status":"issues_found","issues":[{"kind":"contradiction","claim":"La definición de trazabilidad bidireccional según el borrador contradice la fuente académica.","explanation":"El borrador afirma que la trazabilidad bidireccional según NASA solo permite seguir el enlace al requisito padre, excluyendo la trazabilidad hacia adelante. Sin embargo, la fuente académica (E-trace) define la trazabilidad bidireccional como la capacidad de rastrear cualquier requisito hacia su padre y hacia sus hijos, lo que contradice la definición del borrador.","evidence":[{"source_id":"E-trace"}]}]}
```

**Derivación mecánica del host**:
```json
{
  "status": "issues_found",
  "external_support": "unknown",
  "teacher_compatibility": "unknown",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "La definición de trazabilidad bidireccional según el borrador contradice la fuente académica.",
      "explanation": "El borrador afirma que la trazabilidad bidireccional según NASA solo permite seguir el enlace al requisito padre, excluyendo la trazabilidad hacia adelante. Sin embargo, la fuente académica (E-trace) define la trazabilidad bidireccional como la capacidad de rastrear cualquier requisito hacia su padre y hacia sus hijos, lo que contradice la definición del borrador.",
      "evidence": [
        {
          "source_id": "E-trace"
        }
      ]
    }
  ]
}
```

**Contraste técnico**: Adecuada para el defecto principal: identifica que el borrador excluye hijos/trazabilidad hacia adelante. Ya no atribuye esa exclusión al profesor. Señala el pasaje externo pertinente.

**Pasajes recibidos**:

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

## D05

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta revisada**: Como requisito de ejemplo, proponemos un contraste mínimo de 5:1 entre el texto normal y su fondo. Es un umbral ficticio del proyecto, más exigente que el mínimo de 4,5:1 del criterio recibido. Se comprobaría calculando la relación de contraste de los colores del texto y del fondo y contrastándola con 5:1; proponer ese valor no demuestra que una página ya lo cumpla.

**Salida original del revisor**:
```json
{"status":"no_issues_found","issues":[]}
```

**Derivación mecánica del host**:
```json
{
  "status": "no_issues_found",
  "external_support": "unknown",
  "teacher_compatibility": "unknown",
  "response_action": "explanation",
  "issues": []
}
```

**Contraste técnico**: Adecuada: acepta el umbral hipotético más exigente, sin exigir que esté publicado.

**Pasajes recibidos**:

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

## D06

**Pregunta**: Propón un requisito no funcional comprobable de contraste para texto normal de una web, que no sea texto grande, decorativo ni un logotipo, usando el criterio W3C recibido.

**Respuesta revisada**: El criterio W3C recibido establece 3:1 como mínimo para texto normal de tamaño ordinario. Por tanto, para ese texto —sin ser grande, decorativo ni un logotipo— basta una relación de 3:1 para cumplir este criterio. Podemos comprobarla calculando el contraste entre texto y fondo.

**Salida original del revisor**:
```json
{"status":"no_issues_found","issues":[]}
```

**Derivación mecánica del host**:
```json
{
  "status": "no_issues_found",
  "external_support": "unknown",
  "teacher_compatibility": "unknown",
  "response_action": "explanation",
  "issues": []
}
```

**Contraste técnico**: Falso permiso: acepta la atribución de 3:1 a texto normal, aunque la fuente exige 4,5:1 y reserva 3:1 a texto grande. Es un error material, no una mejora opcional.

**Pasajes recibidos**:

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
