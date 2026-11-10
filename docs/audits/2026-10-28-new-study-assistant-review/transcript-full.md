# Candidata nueva y revisión del asistente — resultado parcial

Inspección docente offline; unverified / not_assessed. Participante: null; publicación: false. No sesión humana, no demo aceptada.

## Pregunta congelada

¿Para qué sirve mantener trazabilidad entre necesidades, requisitos y pruebas? Explica cómo la usarías, con un ejemplo hipotético sencillo, para analizar qué revisar si cambia una necesidad del cliente, y qué no permite concluir por sí sola.

## Antes — texto íntegro del modelo local

Mantener trazabilidad entre necesidades, requisitos y pruebas es crucial para asegurar que todos los elementos del desarrollo de un sistema estén alineados y coherentes. Esta trazabilidad permite rastrear cómo una necesidad del cliente se traduce en requisitos específicos y luego en pruebas que validan que esos requisitos se cumplen correctamente.

### ¿Cómo usaría la trazabilidad?

Supongamos un caso hipotético donde un cliente necesita que su sistema de gestión de pacientes permita buscar a un paciente en todas las clínicas. Este requerimiento sería una necesidad del cliente. La trazabilidad nos permitiría identificar:

1. **Necesidad del Cliente**: "El sistema debe permitir buscar a un paciente en todas las clínicas."
2. **Requisito Funcional**: "El sistema debe proporcionar una funcionalidad de búsqueda que permita encontrar a un paciente en cualquier clínica."
3. **Pruebas de Validación**: "Se debe realizar una prueba que demuestre que la búsqueda de un paciente funciona correctamente en todas las clínicas."

Si la necesidad del cliente cambia, por ejemplo, a "El sistema debe permitir buscar a un paciente en todas las clínicas y en sus citas médicas pasadas", la trazabilidad nos ayudaría a identificar qué requisitos y pruebas deben ser revisados y actualizados:

- **Revisar el Requisito Funcional**: El requisito funcional original podría necesitar ser modificado para incluir la búsqueda en citas médicas pasadas.
- **Revisar las Pruebas de Validación**: Se necesitarían nuevas pruebas para validar la nueva funcionalidad de búsqueda en citas médicas pasadas.

### ¿Qué no permite concluir por sí sola la trazabilidad?

La trazabilidad no permite determinar automáticamente si el cambio en la necesidad del cliente tiene implicaciones en otros aspectos del sistema que no sean directamente relacionados con la búsqueda de pacientes. Por ejemplo, si el cambio en la necesidad del cliente implica una mayor carga de datos, esto podría tener implicaciones en el rendimiento del sistema, en la capacidad de almacenamiento, en la seguridad de los datos, etc. Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas.

En resumen, la trazabilidad es una herramienta valiosa para asegurar que los cambios en las necesidades del cliente se reflejan adecuadamente en los requisitos y pruebas correspondientes, pero no reemplaza la necesidad de una evaluación integral de los impactos de estos cambios en el sistema completo.

## Revisión antes de entregar

# Revisión previa por el asistente

Autor: asistente actual, con conocimiento del proyecto; no revisión ciega estadística.
Entradas leídas completas: pregunta, cinco evidencias de request.json y texto íntegro
de initial.json. No se usaron tarjetas históricas, etiquetas de errores esperados,
respuesta modelo corregida ni una llamada de autocrítica del 14B.

La explicación y el ejemplo de búsqueda de pacientes responden al objetivo. Las
citas médicas pasadas son una hipótesis coherente, no un hecho que deba aparecer
literalmente en las fuentes. No se penaliza esa ficción. La distinción entre el
propósito de trazabilidad y una evaluación integral de impactos es útil.

Objeción fundada de cobertura: la cadena está presentada solo de necesidad a
requisito y prueba. Omite explicar el recorrido inverso y que tener enlaces no
demuestra que el trazado sea correcto o satisfaga por completo al requisito
superior. NASA142 exige mantener bidireccionalidad y evaluar corrección/cobertura
del trazado. Es relevante al explicar para qué sirve y qué no concluye por sí
sola, no una exigencia de repetir toda la página ni un cambio de vocabulario.
Testigos literales e IDs constan en assistant-review.json. La frase inicial
«asegurar ... alineados y coherentes» se interpreta aquí como propósito, no se
inventa una contradicción por ese verbo aislado.

La advertencia sobre efectos indirectos es razonable si no están representados
en los enlaces; su redacción no explica esa condición. Se conserva como matiz
de revisión, sin elevarla a una segunda objeción categórica. No corresponde
inferir que la trazabilidad nunca ayude a descubrir esos efectos.

Además no enumera fuentes consultadas, aunque la instrucción lo pide. Se
registra como defecto de presentación/procedencia, distinto del defecto
conceptual que motiva la única reparación. Los recibos contienen las fuentes
exactas; eso no equivale a que la respuesta las haya citado.

Se autoriza exactamente una corrección local con pregunta, candidata, mismas
fuentes y esta crítica. No se proporciona una respuesta académica prefabricada.
Revisión posterior externa pendiente; salida unverified/not_assessed,
participant_display null, publication_allowed false.


## Crítica original enviada al método de reparación

```json
{
  "status": "issues_found",
  "issues": [
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "La explicación solo recorre necesidad→requisito→prueba. Omite explicar el recorrido inverso y que disponer de enlaces no permite concluir que el trazado sea correcto ni que cubra íntegramente al requisito superior: NASA pide comprobar ambas cosas. Es una omisión sustantiva para explicar la utilidad y los límites solicitados. Conserva el ejemplo hipotético coherente; no se objeta que sus datos no sean literales. Enumera también las fuentes consultadas, como pide la instrucción original.",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "As each requirement is documented, its bidirectional traceability should be recorded."
        },
        {
          "source_id": "nasa-seh:142",
          "quote": "The requirements should be evaluated, independently if possible, to ensure that the requirements trace is correct and that it fully addresses its parent requirements."
        }
      ]
    }
  ]
}
```

## Después

No existe candidata corregida. El validador rechazó un testigo no literal antes de llamar al modelo. Una sola candidata completa, cero reparaciones ejecutadas. No se recargó el modelo: ya se había consumido el único calentamiento autorizado.

## Contraste final

# Contraste final por el asistente

Se releyeron pregunta, candidata inicial completa y los cinco pasajes íntegros
de la misma solicitud congelada. No existe versión corregida: el rechazo del
testigo ocurrió antes de reservar o enviar una llamada de reparación. No se
presenta el texto inicial como un «después» ni se inventa un contraste entre
dos versiones. Resultado del mínimo con reparación: incompleto.

- Concepto y aplicación: la relación necesidad→requisito→prueba y el análisis
  del cambio están respaldados por NASA142 y Procedimiento11. El ejemplo toma
  el problema de alcance de búsqueda de Requisitos13 y añade explícitamente
  datos hipotéticos. No hay motivo para rechazar esos datos como invención
  factual. No dice que el cambio ya esté aprobado.
- Omisión persistente: falta el recorrido inverso y la obligación de comprobar
  corrección/cobertura de los enlaces. NASA142 contiene ambas. La necesidad de
  esa comprobación limita lo que puede concluirse por disponer de una cadena.
- Límites: advierte que hace falta evaluar impactos adicionales. La mención
  hipotética de rendimiento, almacenamiento y seguridad es ilustrativa, no un
  diagnóstico observado. «No se derivan directamente» debe entenderse como
  límite de las relaciones representadas en ese ejemplo; no acredita que la
  trazabilidad sea incapaz de ayudar a descubrir impactos indirectos. No se
  eleva este matiz a una contradicción inequívoca.
- Procedencia visible: faltan fuentes consultadas en la respuesta inicial,
  pese a ser una obligación de la instrucción. El contexto sí las conserva.
- Corregidos: ninguno acreditado. Persistentes: omisión conceptual y falta de
  fuentes enumeradas. Nuevos: no evaluables sin otra versión. Pérdida de
  información entre versiones: no evaluable. No hay críticas sustantivas
  demostradas como equivocadas; sí un testigo mal transcrito por el asistente.

La crítica original se conserva intacta. Su segundo testigo escribía
«parent requirements» donde el PDF extraído contiene «parent require-\nments».
El validador admite normalización de espacios, no eliminación de guiones.
La corrección mecánica CPU acorta ese testigo a una subcadena literalmente
presente; mantiene explicación, pregunta, candidata y contexto. Pasa
parse_review, como registra cpu-witness-check.log. Eso prueba procedencia del
testigo, no verdad semántica ni que se haya ejecutado el corrector.

La lectura final mantiene fundada la objeción de cobertura, con el pasaje
completo disponible. No se marca supported ni aceptación humana. Esta revisión
la hace el asistente, no un verificador autónomo local. E2 y Feature012 siguen
abiertos. La segunda candidata no aportaría una comprobación distinta del fallo
de transporte, por lo que no se inicia.

## Mismas fuentes exactas — contexto íntegro recibido

### docente-procedimiento:11

Fuente: 6 - Procedimiento requisitos.pdf; página 11; Verificar la calidad de los requisitos del sistema
SHA256 original: 27a7defe182ecdc4c209a56fd7c220f120ed02c997c2c898dc292bcb13e4e409
Verificar la calidad de los requisitos del sistema
• Modelo de calidad para cada requisito individualmente:
• Comprensible. Redactado de forma que es fácilmente
compresible.
• No ambiguo. Sólo puede interpretarse de una sola manera.
• Gramaticalmente correcto.
• Ortográficamente correcto.
• Realizable. Puede implementarse mediante tecnología
existente y con un coste asumible
• Comprobable. Se pueden definir una o más pruebas, de coste
y tiempo razonables.
• Trazado. Las dependencias del requisito están trazadas hacia
otros requisitos o casos de uso.
30/10/2014 Chapter 4 Requirements Engineering 11

### docente-requisitos:13

Fuente: 5 - Requisitos.pdf; página 13; Requirements imprecision
SHA256 original: 17cca5f0a12db7757216f32b15c3045dc12d4ed05ac3f3729d862f3c3301be99
Requirements imprecision
• Ambiguous requirements may be interpreted in different
ways by developers and users.
• Problems arise when functional requirements are not
precisely stated.
• Consider the term ‘search’ in requirement 1
• User intention – search for a patient name across all
appointments in all clinics;
• Developer interpretation – search for a patient name in an
individual clinic. User chooses clinic then search.
• Precisation is a process: don’t start from too precise
requirements to avoid closing design opportunities.
30/10/2014 Chapter 4 Requirements Engineering 13

### docente-procedimiento:10

Fuente: 6 - Procedimiento requisitos.pdf; página 10; Verificar la calidad de los requisitos del sistema
SHA256 original: 27a7defe182ecdc4c209a56fd7c220f120ed02c997c2c898dc292bcb13e4e409
Verificar la calidad de los requisitos del sistema
• Objetivo: verificar que la Especificación de Requisitos
del Sistema cumple el modelo de calidad de requisitos
propuesto.
• Riesgos de no efectuar la actividad: Sobrecostes.
• Modelo de calidad para la especificación de requisitos:
• Correcta. Acorde a la estructura y contenidos.
• Completa. Contempla todo lo que se conoce que debe hacer
el sistema software a desarrollar
• Consistente internamente. No contiene contradicciones
internas ni redundancias innecesarias
• Consistente externamente. No contiene requisitos u otra
información inconsistente con otros documentos del proyecto.
30/10/2014 Chapter 4 Requirements Engineering 10

### nasa-seh:142

Fuente: nasa-handbook.pdf; página 142; NASA §6.2 Requirements Management
SHA256 original: 8eeb4887a4dc57a23049da7dd2ed556833cf98e214b240468d987873164ff688
requirements database with the goal of verifying
and validating all requirements.
6.2.1.2 Process Activities
6.2.1.2.1 Prepare to Conduct Requirements
Management
Preparing to conduct requirements management
includes gathering the requirements that were defined
and baselined during the Requirements Definition
Process. Identification of the sources/owners of each
requirement should be checked for currency. The
organization (e.g., change board) and procedures to
perform requirements management are established.
6.2.1.2.2 Conduct Requirements Management
The Requirements Management Process involves
managing all changes to expectations and require-
ments baselines over the life of the product and main-
taining bidirectional traceability between stakeholder
expectations, customer requirements, technical prod-
uct requirements, product component requirements,
design documents, and test plans and procedures.
The successful management of requirements involves
several key activities:
• Establish a plan for executing requirements
management.
• Receive requirements from the system design pro-
cesses and organize them in a hierarchical tree
structure.
• Maintain bidirectional traceability between
requirements.
• Evaluate all change requests to the requirements
baseline over the life of the project and make
changes if approved by change board.
• Maintain consistency between the require-
ments, the ConOps, and the architecture/design,

and initiate corrective actions to eliminate
inconsistencies.
6.2.1.2.3 Conduct Expectations and Requirements
Traceability
As each requirement is documented, its bidirectional
traceability should be recorded. Each requirement
should be traced back to a parent/source requirement
or expectation in a baselined document or identified
as self-derived and concurrence on it sought from the
next higher level requirements sources. Examples of
self-derived requirements are requirements that are
locally adopted as good practices or are the result
of design decisions made while performing the
activities of the Logical Decomposition and Design
Solution Processes.
The requirements should be evaluated, independently
if possible, to ensure that the requirements trace is
correct and that it fully addresses its parent require-
ments. If it does not, some other requirement(s)
should complete fulfillment of the parent require-
ment and be included in the traceability matrix. In
addition, ensure that all top-level parent document
requirements have been allocated to the lower level
requirements. If there is no parent for a particular
requirement and it is not an acceptable self-derived
requirement, it should be assumed either that the
traceability process is flawed and should be redone
or that the requirement is “gold plating” and should
be eliminated. Duplication between levels should be
resolved. If a requirement is simply repeated at a lower
level and it is not an externally imposed constraint,
it may not belong at the higher level. Requirements
traceability is usually recorded in a requirements
matrix or through the use of a requirements model-
ing application.

### docente-requisitos:20

Fuente: 5 - Requisitos.pdf; página 20; Goals and requirements
SHA256 original: 17cca5f0a12db7757216f32b15c3045dc12d4ed05ac3f3729d862f3c3301be99
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

## Recibos

Solicitud: request.json. Recuperación y ranking: retrieval.json. Bruto y transporte: initial.json. Congelaciones: pre-generation-freeze.json e initial-freeze.json. Error: failure.json. Validación mecánica CPU: assistant-review-cpu-corrected.json y cpu-witness-check.log. Cierre: worker-cleanup.json. Métricas: metrics.json.
