# Ciclo iterativo asistido — transcripción íntegra

Se realizaron tres correcciones completas y revisión del asistente entre llamadas. Parada por dos iteraciones consecutivas sin reducción de defectos sustantivos. No hay respuesta final apta;003 se conserva como candidata de trabajo no aprobada. Dos grupos sustantivos pendientes y una ambigüedad; la certeza excesiva de una crítica del revisor se rectifica. unverified/not_assessed, participante null, publicación false.

## Pregunta congelada

¿Para qué sirve mantener trazabilidad entre necesidades, requisitos y pruebas? Explica cómo la usarías, con un ejemplo hipotético sencillo, para analizar qué revisar si cambia una necesidad del cliente, y qué no permite concluir por sí sola.

## Respuesta inicial COMPLETA — original intacto

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

## Revisión previa original del asistente

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


## Crítica original rechazada — conservada

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

## Crítica con testigo corregido en CPU

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
          "quote": "The requirements should be evaluated, independently if possible, to ensure that the requirements trace is correct"
        }
      ]
    }
  ]
}

## Reparación histórica768tokens — TODO el texto recibido, INCOMPLETO length

Mantener trazabilidad entre necesidades, requisitos y pruebas es crucial para asegurar que todos los elementos del desarrollo de un sistema estén alineados y coherentes. Esta trazabilidad permite rastrear cómo una necesidad del cliente se traduce en requisitos específicos y luego en pruebas que validan que esos requisitos se cumplen correctamente.

### ¿Cómo usaría la trazabilidad?

Supongamos un caso hipotético donde un cliente necesita que su sistema de gestión de pacientes permita buscar a un paciente en todas las clínicas. Este requerimiento sería una necesidad del cliente. La trazabilidad nos permitiría identificar:

1. **Necesidad del Cliente**: "El sistema debe permitir buscar a un paciente en todas las clínicas."
2. **Requisito Funcional**: "El sistema debe proporcionar una funcionalidad de búsqueda que permita encontrar a un paciente en cualquier clínica."
3. **Pruebas de Validación**: "Se debe realizar una prueba que demuestre que la búsqueda de un paciente funciona correctamente en todas las clínicas."

Si la necesidad del cliente cambia, por ejemplo, a "El sistema debe permitir buscar a un paciente en todas las clínicas y en sus citas médicas pasadas", la trazabilidad nos ayudaría a identificar qué requisitos y pruebas deben ser revisados y actualizados:

- **Revisar el Requisito Funcional**: El requisito funcional original podría necesitar ser modificado para incluir la búsqueda en citas médicas pasadas.
- **Revisar las Pruebas de Validación**: Se necesitarían nuevas pruebas para validar la nueva funcionalidad de búsqueda en citas médicas pasadas.

Además, la trazabilidad permite también el recorrido inverso, desde los requisitos hasta las necesidades del cliente, asegurando que cada requisito tenga un origen claro y que no haya requisitos redundantes o inconsistentes. Esto implica que cada requisito debe estar trazado hacia su necesidad de origen y que cada necesidad debe estar cubierta por uno o varios requisitos.

### ¿Qué no permite concluir por sí sola la trazabilidad?

La trazabilidad no permite determinar automáticamente si el cambio en la necesidad del cliente tiene implicaciones en otros aspectos del sistema que no sean directamente relacionados con la búsqueda de pacientes. Por ejemplo, si el cambio en la necesidad del cliente implica una mayor carga de datos, esto podría tener implicaciones en el rendimiento del sistema, en la capacidad de almacenamiento, en la seguridad de los datos, etc. Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas.

Además, la trazabilidad no garantiza que el trazado sea correcto ni que cubra íntegramente al requisito superior. Es necesario evaluar independientemente la consistencia y la precisión de cada requisito para asegurar que no existan ambigüedades o redundancias.

En resumen, la trazabilidad es una herramienta valiosa para asegurar que los cambios en las necesidades del cliente se reflejan adecuadamente en los requisitos y pruebas correspondientes, pero no reemplaza la necesidad de una evaluación integral de los impactos de estos cambios en el sistema completo.

### Fuentes consultadas:
- Fuente: nasa-handbook.pdf; página 142; NASA §6.2 Requirements Management
- Fuente: 6 - Procedimiento requisitos
[FIN EXACTO DEL TEXTO RECIBIDO: LENGTH]

## Revisión del asistente de la reparación histórica

# Contraste final por el asistente — reparación real incompleta

Autor: asistente actual. Se leyeron de nuevo la pregunta, la respuesta inicial
COMPLETA, los cinco pasajes COMPLETOS y TODO el texto que devolvió la única
llamada de reparación. No hay autocrítica ni post-review del14B. La salida nueva
terminó `length` a768tokens y48,078s: se cortó en «Fuente: 6 - Procedimiento
requisitos». No se inventa su continuación ni se declara una segunda versión
completa. El contraste siguiente evalúa solo el texto recibido; no acredita
una reparación completa.

## Avances observados, sin contar éxito de una versión completa

1. La nueva frase «la trazabilidad permite también el recorrido inverso, desde
   los requisitos hasta las necesidades del cliente» añade una dirección que
   faltaba. Respaldo: NASA142, «Each requirement should be traced back to a
   parent/source requirement or expectation in a baselined document». Es un
   avance conceptual, aunque no muestra el recorrido inverso desde una prueba
   ni aplica ese recorrido al ejemplo completo. No basta añadir la palabra
   bidireccional: aquí sí explica una dirección antes ausente.
2. «la trazabilidad no garantiza que el trazado sea correcto ni que cubra
   íntegramente al requisito superior» expresa el límite omitido. NASA142
   requiere comprobar corrección y atención completa al requisito padre.
   La frase es un avance real; la oración siguiente describe de modo impreciso
   qué debe comprobarse, como se registra abajo.

No se cuentan como dos defectos totalmente resueltos: ambos avances pertenecen
a la única objeción original de cobertura y están en una salida incompleta.

## Persistencias y omisiones

- Se conserva el ejemplo hipotético coherente y el análisis de qué requisito
  y pruebas revisar. No se penalizan citas médicas pasadas como hechos inventados:
  son datos declarados de un ejemplo. Su principio está respaldado por NASA142;
  el alcance de búsqueda ilustra la ambigüedad de Requisitos13.
- La parte sobre impactos indirectos conserva «no se derivan directamente».
  Sigue faltando explicitar que es un límite de los enlaces representados,
  no una incapacidad universal de la trazabilidad para ayudar a descubrirlos.
  Se mantiene como matiz, no como contradicción demostrada.
- Las fuentes pasan de ausentes a una lista iniciada: NASA142 está identificada,
  pero la segunda referencia se corta. Procedencia visible aún incompleta.
- El recorrido inverso prueba→requisito no está explicado y no se demuestra
  cobertura completa del ejemplo. No se exige repetir toda la página NASA.

## Problemas nuevos en el texto recibido

1. **Sobreafirmación de garantía.** «asegurando que cada requisito tenga un
   origen claro y que no haya requisitos redundantes o inconsistentes» atribuye
   al recorrido inverso un aseguramiento que los enlaces no prueban. NASA142
   pide evaluar las trazas y resolver duplicaciones; Procedimiento10 distingue
   consistencia interna/externa como cualidades que deben comprobarse. La frase
   posterior que niega garantías no elimina esta tensión del texto completo.
2. **Condición de origen demasiado universal.** «cada requisito debe estar
   trazado hacia su necesidad de origen» no conserva la alternativa de NASA142:
   «or identified as self-derived and concurrence on it sought from the next
   higher level requirements sources». La fuente admite requisitos derivados
   de buenas prácticas o decisiones de diseño bajo esa condición. No se deben
   eliminar esas excepciones al resumir; la objeción original no pidió hacerlo.
3. **Comprobación independiente mal delimitada.** «Es necesario evaluar
   independientemente la consistencia y la precisión de cada requisito para
   asegurar que no existan ambigüedades o redundancias» transforma «independently
   if possible» de NASA142 en una necesidad incondicional y desplaza el objeto
   de comprobación de corrección/cobertura de la traza a calidad individual.
   Procedimiento10/11 sí respaldan comprobar calidad, pero no esa equivalencia
   ni esa garantía. Es un problema de condición y síntesis, con evidencia
   disponible; no una ausencia del ranking.

Los tres hallazgos nuevos no son tres errores del alumno ni una nota: describen
el texto generado. No son una tasa de calidad extrapolable. Se separan de las
persistencias y del truncamiento operativo.

## Balance y crítica del revisor

Una objeción original de cobertura con dos componentes: avances parciales en
ambos; cero reparaciones completas aceptables. Una omisión de procedencia
visible persiste por corte. Tres hallazgos nuevos localizados arriba. No se
observó eliminación del ejemplo ni del análisis de cambio: se conservaron,
pero se perdieron condiciones de la fuente en las adiciones. No hay crítica
semántica original demostrada como equivocada. El testigo original mal
transcrito sigue reconocido como error mecánico del asistente, corregido en
CPU antes de esta carga; no se reescribe su evidencia histórica.

El `outcome` exterior de repair.json es el INICIAL conservado por el adaptador,
no la salida nueva. La reparación recibida se encuentra en
`trace.calls[0].outcome` y en el recibo `*-result.json`; su `ok=false` y
`finish_reason=length` permanecen intactos. No contar texto inicial retornado
como prueba de que el modelo no cambió nada.

Resultado: se completó la invocación pendiente y su revisión asistida, con
resultado negativo de terminación y defectos nuevos. No hay revisión semántica
autónoma local resuelta, publicación ni tutor aprobado. No se hace otra llamada
para acortar o aprobar este mismo caso. E2/Feature012 y gates siguen como antes.


## Revisión renovada antes de001

# Revisión renovada antes de la corrección001

El asistente releyó íntegramente pregunta, respuesta inicial, TODO el resultado
length de recovery-001 y cinco fuentes de request.json. Los textos anteriores
se conservan. La entrada a regenerar será ese resultado parcial exacto, marcado
como incompleto; no se simula que fuera una respuesta completa.

Se confirman cuatro defectos sustantivos corregibles, agrupados en tres issues:
garantía indebida al recorrer enlaces, eliminación de excepción auto-derivada,
independencia incondicional/desplazamiento de comprobación de traza a calidad,
y límite demasiado categórico sobre impactos indirectos. NASA142 y
Procedimiento11 proporcionan los testigos. El cuarto antes se registró como
matiz: la frase completa ahora se precisa como sobreafirmación condicionada,
sin afirmar que la trazabilidad descubra todos los impactos.

Se corrige también una posible lectura demasiado exigente de nuestra crítica
previa: no todo requisito tiene que proceder directamente de una necesidad del
cliente y no toda explicación introductoria necesita repetir toda la gestión
NASA. La bidireccionalidad debe explicarse de forma útil para esta pregunta;
NASA aporta condiciones de su procedimiento, no obligaciones universales.
La crítica anterior no pidió eliminar excepciones; sí debemos evitar que el
corrector entienda su petición de cobertura como tal regla universal.

Preservar: principio respaldado, ejemplo hipotético coherente, análisis de qué
requisito/pruebas revisar y límite de que enlaces no prueban corrección/cobertura.
Cambiar: garantías, condiciones/excepciones y relación entre tipos de comprobación.
Puede reescribir concisamente para coherencia; no tiene que copiar todos los
párrafos y añadir otros. No se proporciona una respuesta académica completa.

Referencias internas deben apuntar a los IDs de los mismos pasajes. La lista
visible de fuentes la construirá el host desde su procedencia. No se exige al
modelo repetir una bibliografía que ya contiene el recibo.


## Crítica001 EXACTA antes de generar

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "overclaim",
      "claim": "asegurando que cada requisito tenga un origen claro y que no haya requisitos redundantes o inconsistentes. Esto implica que cada requisito debe estar trazado hacia su necesidad de origen y que cada necesidad debe estar cubierta por uno o varios requisitos.",
      "explanation": "El recorrido inverso no asegura por sí solo ausencia de redundancia o inconsistencia: hay que comprobarlas. Además, en el procedimiento NASA no todo requisito necesita una necesidad de cliente directa: admite auto-derivados con conformidad del nivel superior. Conserva esa excepción y su ámbito, sin imponer reglas NASA como universales. Preserva el ejemplo hipotético y explica el uso de enlaces hacia delante y hacia atrás entre necesidades, requisitos y pruebas, condicionado a los enlaces realmente registrados.",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "or identified as self-derived and concurrence on it sought from the next higher level requirements sources."
        },
        {
          "source_id": "nasa-seh:142",
          "quote": "Duplication between levels should be resolved."
        }
      ]
    },
    {
      "kind": "ambiguity",
      "claim": "Es necesario evaluar independientemente la consistencia y la precisión de cada requisito para asegurar que no existan ambigüedades o redundancias.",
      "explanation": "NASA recomienda evaluación independiente cuando sea posible y pide comprobar corrección/cobertura de la traza. La candidata convierte la independencia en necesidad incondicional y la sustituye por calidad individual del requisito. Separa ambas comprobaciones; evita garantizar ausencia de defectos por hacerlas. Conserva explícito que tener enlaces no acredita por sí solo corrección ni cobertura completa.",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "The requirements should be evaluated, independently if possible, to ensure that the requirements trace is correct"
        },
        {
          "source_id": "docente-procedimiento:11",
          "quote": "Modelo de calidad para cada requisito individualmente:"
        }
      ]
    },
    {
      "kind": "overclaim",
      "claim": "Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas.",
      "explanation": "Es correcto pedir análisis adicional; la limitación depende de qué relaciones estén representadas. No excluyas categóricamente que enlaces registrados a requisitos dependientes ayuden a descubrir efectos indirectos. Lo que no permiten por sí solos es descubrir todos los impactos ni probar su corrección. La fuente respalda dependencias entre requisitos; explica el límite del ejemplo sin inventar un análisis real de rendimiento o seguridad.",
      "evidence": [
        {
          "source_id": "docente-procedimiento:11",
          "quote": "Las dependencias del requisito están trazadas hacia otros requisitos o casos de uso."
        },
        {
          "source_id": "nasa-seh:142",
          "quote": "Maintain consistency between the require- ments, the ConOps, and the architecture/design,"
        }
      ]
    }
  ]
}

## Versión001 COMPLETA — stop

Mantener trazabilidad entre necesidades, requisitos y pruebas es crucial para asegurar que todos los elementos del desarrollo de un sistema estén alineados y coherentes. Esta trazabilidad permite rastrear cómo una necesidad del cliente se traduce en requisitos específicos y luego en pruebas que validan que esos requisitos se cumplen correctamente.

### ¿Cómo usaría la trazabilidad?

Supongamos un caso hipotético donde un cliente necesita que su sistema de gestión de pacientes permita buscar a un paciente en todas las clínicas. Este requerimiento sería una necesidad del cliente. La trazabilidad nos permitiría identificar:

1. **Necesidad del Cliente**: "El sistema debe permitir buscar a un paciente en todas las clínicas."
2. **Requisito Funcional**: "El sistema debe proporcionar una funcionalidad de búsqueda que permita encontrar a un paciente en cualquier clínica."
3. **Pruebas de Validación**: "Se debe realizar una prueba que demuestre que la búsqueda de un paciente funciona correctamente en todas las clínicas."

Si la necesidad del cliente cambia, por ejemplo, a "El sistema debe permitir buscar a un paciente en todas las clínicas y en sus citas médicas pasadas", la trazabilidad nos ayudaría a identificar qué requisitos y pruebas deben ser revisados y actualizados:

- **Revisar el Requisito Funcional**: El requisito funcional original podría necesitar ser modificado para incluir la búsqueda en citas médicas pasadas.
- **Revisar las Pruebas de Validación**: Se necesitarían nuevas pruebas para validar la nueva funcionalidad de búsqueda en citas médicas pasadas.

Además, la trazabilidad permite también el recorrido inverso, desde los requisitos hasta las necesidades del cliente, asegurando que cada requisito tenga un origen claro. Sin embargo, no garantiza que no haya requisitos redundantes o inconsistentes; es necesario evaluar independientemente la consistencia y la precisión de cada requisito para asegurar que no existan ambigüedades o redundancias.

### ¿Qué no permite concluir por sí sola la trazabilidad?

La trazabilidad no permite determinar automáticamente si el cambio en la necesidad del cliente tiene implicaciones en otros aspectos del sistema que no sean directamente relacionados con la búsqueda de pacientes. Por ejemplo, si el cambio en la necesidad del cliente implica una mayor carga de datos, esto podría tener implicaciones en el rendimiento del sistema, en la capacidad de almacenamiento, en la seguridad de los datos, etc. Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas.

En resumen, la trazabilidad es una herramienta valiosa para asegurar que los cambios en las necesidades del cliente se reflejan adecuadamente en los requisitos y pruebas correspondientes, pero no reemplaza la necesidad de una evaluación integral de los impactos de estos cambios en el sistema completo.

### Fuentes consultadas:
- Fuente: nasa-handbook.pdf; página 142; NASA §6.2 Requirements Management
- Fuente: 6 - Procedimiento requisitos

## Contraste del asistente después de001

# Revisión completa de versión001

El asistente leyó toda la salida `stop` (708tokens/44,594s), la pregunta y los
cinco pasajes íntegros. No es truncamiento operativo, aunque copia el final
bibliográfico incompleto de su entrada. No es apta aún.

Corregidos o retirados: niega explícitamente que los enlaces garanticen ausencia
de redundancias/inconsistencias; retira la exigencia literal de que cada requisito
deba estar trazado a una necesidad directa. Son dos mejoras respecto del parcial
anterior. La segunda no explica todavía la alternativa aceptada por NASA.

Tres grupos sustantivos pendientes:
1. «es necesario evaluar independientemente ... para asegurar que no existan
   ambigüedades o redundancias» mantiene independencia incondicional y garantía
   indebida. NASA142 dice «independently if possible»; calidad individual de
   Procedimiento11 no sustituye revisar enlaces/cobertura.
2. Se pierde la frase útil que negaba que trazar garantice corrección/cobertura.
   Falta la excepción auto-derivada con conformidad superior del procedimiento
   NASA. El recorrido inverso aparece requisito→necesidad, sin aclarar regreso
   prueba→requisito. Son omisiones de explicación/condiciones, no evidencia
   perdida en el ranking. Se agrupan en cobertura para no duplicar recuento.
3. Persiste «no se derivan directamente» para impactos adicionales, sin
   condicionarlo a los enlaces representados. Las dependencias sí pueden ayudar
   a localizarlos; no prueban que estén todos ni que sean correctos.

Procedencia: no usa referencias internas [fragment_id], aunque se pidió. Copia
una lista de fuentes innecesaria que termina en un nombre incompleto. El host
puede presentar correctamente fuentes consultadas, pero eso no subsana por sí
solo atribuciones internas ausentes. Se registra aparte como fallo de contrato
de presentación, sin convertirlo en un nuevo concepto falso.

Ejemplo hipotético y análisis del cambio conservados y coherentes; ninguna cifra
o detalle ficticio se penaliza por no aparecer literal. No detecto crítica
sustantiva anterior falsa. Sí matizo que retirar la exigencia directa ya elimina
parte del error de origen: ahora se pide expresar la excepción/ámbito relevante,
no reparar una frase literal que ya no existe.

Recuento comparativo: cuatro grupos iniciales → tres grupos pendientes; dos
afirmaciones mejoradas/retiradas y una omisión reintroducida (límite de corrección
y cobertura). Es seguimiento de defectos de esta respuesta, no nota del alumno
ni tasa de calidad. Hay progreso; procede otra corrección justificada, no parada
por dos iteraciones sin reducción. Mantener versión001 íntegra.


## Crítica002 EXACTA antes de generar

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "overclaim",
      "claim": "es necesario evaluar independientemente la consistencia y la precisión de cada requisito para asegurar que no existan ambigüedades o redundancias.",
      "explanation": "Persiste la independencia incondicional y una garantía indebida. En NASA la evaluación independiente es cuando sea posible y se comprueba corrección/cobertura de la traza, que no equivale a calidad individual del requisito. Distingue estas comprobaciones, sin prometer que una revisión elimine todos los defectos. Se puede reescribir con concisión, sin copiar párrafos y añadir una salvedad contradictoria.",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "The requirements should be evaluated, independently if possible, to ensure that the requirements trace is correct"
        },
        {
          "source_id": "docente-procedimiento:11",
          "quote": "Modelo de calidad para cada requisito individualmente:"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "Se perdió el límite útil: tener enlaces no prueba corrección ni cobertura total de la traza. Falta conservar la alternativa NASA de auto-derivados aceptados con conformidad superior, sin imponerla universalmente. Explica también retorno prueba→requisito dentro de los enlaces registrados. Usa referencias internas [fragment_id] reales para principios y condiciones: el host presenta la lista de fuentes, no copies la lista bibliográfica rota de la candidata. Preserva el ejemplo coherente sin confundir sus datos con hechos.",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "or identified as self-derived and concurrence on it sought from the next higher level requirements sources."
        },
        {
          "source_id": "nasa-seh:142",
          "quote": "The requirements should be evaluated, independently if possible, to ensure that the requirements trace is correct"
        }
      ]
    },
    {
      "kind": "overclaim",
      "claim": "Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas.",
      "explanation": "Condiciona el límite a lo que está registrado: las dependencias trazadas pueden ayudar a detectar efectos indirectos, aunque no descubran todos los impactos ni acrediten corrección por sí solas. No excluyas categóricamente su utilidad para esos efectos. No diagnostiques impactos reales del ejemplo ficticio sin premisas. Reescribe para mantener consistencia con la explicación de bidireccionalidad y con el análisis adicional necesario.",
      "evidence": [
        {
          "source_id": "docente-procedimiento:11",
          "quote": "Las dependencias del requisito están trazadas hacia otros requisitos o casos de uso."
        }
      ]
    }
  ]
}

## Versión002 COMPLETA — stop

Mantener trazabilidad entre necesidades, requisitos y pruebas es crucial para asegurar que todos los elementos del desarrollo de un sistema estén alineados y coherentes. Esta trazabilidad permite rastrear cómo una necesidad del cliente se traduce en requisitos específicos y luego en pruebas que validan que esos requisitos se cumplen correctamente.

### ¿Cómo usaría la trazabilidad?

Supongamos un caso hipotético donde un cliente necesita que su sistema de gestión de pacientes permita buscar a un paciente en todas las clínicas. Este requerimiento sería una necesidad del cliente. La trazabilidad nos permitiría identificar:

1. **Necesidad del Cliente**: "El sistema debe permitir buscar a un paciente en todas las clínicas."
2. **Requisito Funcional**: "El sistema debe proporcionar una funcionalidad de búsqueda que permita encontrar a un paciente en cualquier clínica."
3. **Pruebas de Validación**: "Se debe realizar una prueba que demuestre que la búsqueda de un paciente funciona correctamente en todas las clínicas."

Si la necesidad del cliente cambia, por ejemplo, a "El sistema debe permitir buscar a un paciente en todas las clínicas y en sus citas médicas pasadas", la trazabilidad nos ayudaría a identificar qué requisitos y pruebas deben ser revisados y actualizados:

- **Revisar el Requisito Funcional**: El requisito funcional original podría necesitar ser modificado para incluir la búsqueda en citas médicas pasadas.
- **Revisar las Pruebas de Validación**: Se necesitarían nuevas pruebas para validar la nueva funcionalidad de búsqueda en citas médicas pasadas.

Además, la trazabilidad permite también el recorrido inverso, desde los requisitos hasta las necesidades del cliente, asegurando que cada requisito tenga un origen claro. Sin embargo, no garantiza que no haya requisitos redundantes o inconsistentes; es necesario evaluar independientemente la consistencia y la precisión de cada requisito para asegurar que no existan ambigüedades o redundancias [fragment_id].

### ¿Qué no permite concluir por sí sola la trazabilidad?

La trazabilidad no permite determinar automáticamente si el cambio en la necesidad del cliente tiene implicaciones en otros aspectos del sistema que no sean directamente relacionados con la búsqueda de pacientes. Por ejemplo, si el cambio en la necesidad del cliente implica una mayor carga de datos, esto podría tener implicaciones en el rendimiento del sistema, en la capacidad de almacenamiento, en la seguridad de los datos, etc. Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas [fragment_id].

En resumen, la trazabilidad es una herramienta valiosa para asegurar que los cambios en las necesidades del cliente se reflejan adecuadamente en los requisitos y pruebas correspondientes, pero no reemplaza la necesidad de una evaluación integral de los impactos de estos cambios en el sistema completo.

[fragment_id]: La evaluación independiente de la consistencia y precisión de cada requisito es necesaria para evitar ambigüedades o redundancias, aunque no garantiza la eliminación de todos los defectos. [fragment_id]: Las dependencias trazadas pueden ayudar a detectar efectos indirectos, aunque no descubren todos los impactos ni acreditan la corrección por sí solas.

## Contraste del asistente después de002

# Revisión completa de versión002

Lectura íntegra del asistente: pregunta, versión002 `stop` (761tokens/48,969s),
versión001 y los cinco pasajes. Se ha retirado la lista bibliográfica copiada,
pero no se han resuelto los tres grupos sustantivos pendientes.

Persiste la necesidad incondicional de evaluación independiente; el texto
añadido vuelve a llamarla «necesaria». NASA dice independiente si es posible y
se centra en traza/cobertura, no solo precisión individual. Persiste la omisión
de la excepción auto-derivada y del límite corrección/cobertura de enlaces.
Persiste la frase categórica sobre efectos indirectos. Una nota final sí dice
que dependencias trazadas pueden ayudar a detectarlos: es un matiz correcto,
pero queda en tensión con el cuerpo que conserva la exclusión categórica.
No basta añadir al final la salvedad sin integrar su significado.

Problema nuevo de procedencia: usa literalmente [fragment_id] como referencia
y crea dos notas con esa misma etiqueta. No identifica ningún pasaje real.
No se cuenta como cuatro referencias correctas ni como prueba de respaldo.
Los IDs reales sí están en las críticas/testigos; no se habían enumerado todos
los IDs junto al texto de cada evidencia en la serialización académica histórica.
Esto puede contribuir a la ambigüedad de formato, sin demostrar que explique
los errores conceptuales: las condiciones y citas pertinentes estaban presentes.
La siguiente crítica dará los IDs reales de referencia de forma explícita,
sin añadir contenido académico ni otra fuente.

Conservados: ejemplo hipotético, análisis del cambio y retirada previa de la
garantía de ausencia de inconsistencia. No se inventa un nuevo error por estilo.
No detecto críticas anteriores semánticamente falsas; sí una consigna de IDs
insuficientemente concreta en este transporte, que se precisa a continuación.

Balance: cero grupos sustantivos resueltos de los tres; un matiz correcto añadido
sin integrarlo y un fallo nuevo de referencia. Primera iteración consecutiva
sin reducción desde versión001. Se permite una corrección más; si tampoco
reduce, corresponde la parada autorizada por dos consecutivas sin reducción.


## Crítica003 EXACTA antes de generar

{
  "status": "issues_found",
  "issues": [
    {
      "kind": "overclaim",
      "claim": "es necesario evaluar independientemente la consistencia y la precisión de cada requisito para asegurar que no existan ambigüedades o redundancias [fragment_id].",
      "explanation": "La modalidad sigue siendo incorrecta: NASA dice independencia cuando sea posible. Debe comprobarse corrección/cobertura de la traza, distinta de la calidad individual, sin prometer ausencia de defectos. No basta añadir al final una nota que mantenga 'necesaria'. Reescribe el cuerpo para resolver la afirmación. Referencias reales disponibles: [nasa-seh:142] y [docente-procedimiento:11]; [fragment_id] es un marcador inválido y no debe aparecer como cita literal.",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "The requirements should be evaluated, independently if possible, to ensure that the requirements trace is correct"
        },
        {
          "source_id": "docente-procedimiento:11",
          "quote": "Modelo de calidad para cada requisito individualmente:"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "Siguen omitidos: tener enlaces no prueba corrección/cobertura; alternativa de auto-derivados aceptados con conformidad del nivel superior en el procedimiento NASA; retorno prueba→requisito en el ejemplo. Integra esas condiciones en una explicación coherente y breve, sin imponer NASA universalmente. Puedes rehacer la estructura y acortar repeticiones: no copies toda la candidata y agregues notas. Conserva las premisas del ejemplo ficticio. Usa IDs reales como [nasa-seh:142], no una bibliografía o notas [fragment_id].",
      "evidence": [
        {
          "source_id": "nasa-seh:142",
          "quote": "or identified as self-derived and concurrence on it sought from the next higher level requirements sources."
        },
        {
          "source_id": "nasa-seh:142",
          "quote": "Maintain bidirectional traceability between requirements."
        }
      ]
    },
    {
      "kind": "overclaim",
      "claim": "Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas [fragment_id].",
      "explanation": "El cuerpo excluye de forma categórica los efectos indirectos, pero tu nota final reconoce que dependencias trazadas pueden ayudar a detectarlos. Integra esa condición y elimina la tensión en el cuerpo: el alcance depende de las relaciones realmente registradas; no permite acreditar todos los impactos. Respaldo de dependencias: [docente-procedimiento:11]. No añadas una tercera nota al final. Devuelve una respuesta académica reescrita y coherente, con referencias reales internas y sin lista de fuentes del modelo.",
      "evidence": [
        {
          "source_id": "docente-procedimiento:11",
          "quote": "Las dependencias del requisito están trazadas hacia otros requisitos o casos de uso."
        }
      ]
    }
  ]
}

## Versión003 COMPLETA — stop

Mantener trazabilidad entre necesidades, requisitos y pruebas es crucial para asegurar que todos los elementos del desarrollo de un sistema estén alineados y coherentes. Esta trazabilidad permite rastrear cómo una necesidad del cliente se traduce en requisitos específicos y luego en pruebas que validan que esos requisitos se cumplen correctamente.

### ¿Cómo usaría la trazabilidad?

Supongamos un caso hipotético donde un cliente necesita que su sistema de gestión de pacientes permita buscar a un paciente en todas las clínicas. Este requerimiento sería una necesidad del cliente. La trazabilidad nos permitiría identificar:

1. **Necesidad del Cliente**: "El sistema debe permitir buscar a un paciente en todas las clínicas."
2. **Requisito Funcional**: "El sistema debe proporcionar una funcionalidad de búsqueda que permita encontrar a un paciente en cualquier clínica."
3. **Pruebas de Validación**: "Se debe realizar una prueba que demuestre que la búsqueda de un paciente funciona correctamente en todas las clínicas."

Si la necesidad del cliente cambia, por ejemplo, a "El sistema debe permitir buscar a un paciente en todas las clínicas y en sus citas médicas pasadas", la trazabilidad nos ayudaría a identificar qué requisitos y pruebas deben ser revisados y actualizados:

- **Revisar el Requisito Funcional**: El requisito funcional original podría necesitar ser modificado para incluir la búsqueda en citas médicas pasadas.
- **Revisar las Pruebas de Validación**: Se necesitarían nuevas pruebas para validar la nueva funcionalidad de búsqueda en citas médicas pasadas.

Además, la trazabilidad permite también el recorrido inverso, desde los requisitos hasta las necesidades del cliente, asegurando que cada requisito tenga un origen claro. Sin embargo, no garantiza que no haya requisitos redundantes o inconsistentes; es necesario evaluar independientemente la consistencia y la precisión de cada requisito para evitar ambigüedades o redundancias [nasa-seh:142].

### ¿Qué no permite concluir por sí sola la trazabilidad?

La trazabilidad no permite determinar automáticamente si el cambio en la necesidad del cliente tiene implicaciones en otros aspectos del sistema que no sean directamente relacionados con la búsqueda de pacientes. Por ejemplo, si el cambio en la necesidad del cliente implica una mayor carga de datos, esto podría tener implicaciones en el rendimiento del sistema, en la capacidad de almacenamiento, en la seguridad de los datos, etc. Estas implicaciones adicionales deben ser evaluadas por separado y no se derivan directamente de la trazabilidad entre necesidades, requisitos y pruebas [docente-procedimiento:11].

En resumen, la trazabilidad es una herramienta valiosa para asegurar que los cambios en las necesidades del cliente se reflejan adecuadamente en los requisitos y pruebas correspondientes, pero no reemplaza la necesidad de una evaluación integral de los impactos de estos cambios en el sistema completo.

## Contraste del asistente después de003

# Revisión completa de versión003 y parada

El asistente leyó toda la salida `stop` (679tokens/43,343s), pregunta y los cinco
pasajes íntegros, comparándola con001/002 y el texto inicial. Esta tercera salida
es completa; no falla por longitud o deadline. No es apta para revisión docente
como respuesta sin defectos sustantivos detectados.

Mejora de presentación: elimina las notas duplicadas [fragment_id], usa los IDs
reales proporcionados explícitamente en la crítica y no repite bibliografía.
Es procedencia estructural, no respaldo semántico: la frase «es necesario
evaluar independientemente» ahora cita NASA142, que mantiene «independently
if possible». El ID correcto no transforma una condición mal resumida en verdad.

Persisten los tres grupos:
1. Independencia incondicional y confusión de comprobar trazado/cobertura con
   calidad individual. Cambia «asegurar» por «evitar», pero mantiene la necesidad
   sin condición. No se acredita corrección por ese cambio de verbo.
2. Sigue ausente la excepción NASA de auto-derivados aceptados/conformidad del
   nivel superior y el límite explícito de que enlaces no prueban corrección/
   cobertura completa. El retorno prueba→requisito sigue sin explicación. No
   son datos faltantes: estaban en el mismo contexto completo.
3. Persiste la exclusión categórica de derivar impactos adicionales de las
   dependencias trazadas, ahora citando Procedimiento11. Esa página respalda
   registrar dependencias; no esa exclusión. Se ha retirado además la salvedad
   correcta que había añadido002. Se registra pérdida de información útil.

No detecto un cuarto concepto falso nuevo. Las atribuciones ahora visibles
exponen los mismos problemas semánticos, no los resuelven. No hay crítica
sustantiva demostrada como equivocada en esta iteración. La corrección de la
consigna de IDs sí tuvo efecto de formato, sin mejora académica correspondiente.

El ejemplo de búsqueda y la aplicación del cambio siguen siendo hipotéticos,
coherentes y útiles. No se consideran inventados como hechos. Se conserva
la negación de garantía de ausencia de inconsistencias que mejoró001.

Balance: tres grupos sustantivos pendientes en001→tres en002→tres en003.
Son dos iteraciones consecutivas SIN reducción sustantiva, pese a variaciones
de formato. Se activa la condición prospectiva autorizada de parada. No se
ejecutan las tres llamadas restantes para gastar el cupo o forzar aprobación.

Se conserva003 como candidata de trabajo completa con mejor presentación entre
las regeneradas, con estos tres grupos señalados, sin declararla respuesta final
apta. La inicial y todas las críticas/versiones permanecen intactas. No se
entrega una respuesta académica reescrita por el asistente como si fuera local.
No se afirma que esta elección sea una superioridad académica global sobre001.

La revisión final completa contra los textos originales del contexto confirma
la parada y ausencia de candidata que cumpla el criterio de este caso. Los
originales fuente se revalidan/hashan al cierre. E2/Feature012 y participantes
siguen sin aprobación; el revisor semántico sigue siendo el asistente.


## Lectura final y rectificación del revisor

# Lectura final completa y rectificación de certeza del revisor

Tras la parada se releyeron pregunta, inicial, las tres salidas completas y
todos los textos fuente. También se inspeccionaron las cinco imágenes de página
ya existentes y acreditadas por hash: requisitos13/20, procedimiento10/11 y
NASA142 (página impresa132). No se recuperaron otras páginas ni se añadió
contexto al modelo. La columna derecha de NASA confirma auto-derivados con
conformidad superior e independencia «if possible»; Procedimiento11 distingue
calidad individual y dependencias trazadas. No se atribuyen fallos a tablas.

Dos grupos de defectos sustantivos/omisiones permanecen inequívocos en la
mejor candidata de trabajo003:

1. Independencia obligatoria sin conservar «cuando sea posible», y desplazamiento
   de comprobar corrección/cobertura de la traza a calidad individual. El cambio
   de «asegurar» a «evitar» no subsana la modalidad ni la distinción.
2. Pérdida del límite explícito de que enlaces no prueban corrección/cobertura;
   omisión de la excepción auto-derivada aceptada en el ámbito NASA y del
   recorrido inverso desde pruebas que haría útil la explicación solicitada.
   La frase que exigía toda necesidad directa ya se había retirado: no se sigue
   acusando a003 de contener aquella afirmación literal.

Rectificación del revisor: la crítica a impactos indirectos se formuló demasiado
categóricamente en los issues de esta continuación. El párrafo completo comienza
con «no permite determinar automáticamente» y termina pidiendo evaluación
adicional. Es posible leer «no se derivan directamente» como ausencia de
deducción automática, no como prohibición de usar dependencias para descubrirlos.
Procedimiento11 respalda registrar dependencias, pero no basta para demostrar
que esa lectura contextualizada sea falsa. La sugerencia de explicitar el
alcance de los enlaces es útil, pero se rebaja a AMBIGÜEDAD, no tercer defecto
sustantivo indiscutible. La nota correcta de002 se perdió en003; esa pérdida se
registra sin inventar una contradicción probada.

Los recibos de críticas y decisiones provisionales no se reescriben. Allí se
contaron cuatro grupos iniciales y tres pendientes; la recalibración final,
excluyendo la objeción ambigua, da tres grupos de partida y dos pendientes
en001, dos en002 y dos en003. La condición de parada sigue cumplida:
001→002 y002→003 son dos comparaciones consecutivas sin reducción de los
dos grupos inequívocos. No se usa una crítica débil para forzar una reparación.

Críticas equivocadas/excesivas: una sobreafirmación de certeza del revisor
rectificada aquí; no se presenta como hecho falso definitivamente demostrado
del modelo. Además, la consigna de referencias se precisó tras ver [fragment_id]
literal en002; es una limitación de transporte/consigna, distinta del juicio
semántico. El nuevo índice explícito de fuentes del perfil se comprueba en CPU
al cerrar, sin ejecutar otra llamada ni atribuirle resultados GPU retrospectivos.

Balance final: mejoras parciales, dos grupos relevantes sin resolver y una
ambigüedad. No hay candidata que cumpla el criterio autorizado.003 se conserva
como trabajo completo con mejor presentación, SIN aprobación. No hay una respuesta
final adecuada redactada por el modelo que pueda entregarse como tal.


## Métricas y presupuesto

{
  "first_preflight": {
    "utc": "2026-10-28T13:43:55.6299885Z",
    "started_monotonic": 1177007.7743074,
    "maximum_seconds": 1800,
    "maximum_corrections": 6,
    "gpu": "name, memory.used [MiB], memory.total [MiB], utilization.gpu [%]\r\nNVIDIA GeForce RTX 5090, 1558 MiB, 32607 MiB, 0 %\r\n"
  },
  "gpu_lifecycle_seconds": 797.1316925999708,
  "elapsed_through_delivery_build": 1120.2876925999299,
  "maximum_seconds": 1800,
  "correction_calls": 3,
  "maximum_calls": 6,
  "loads": 1,
  "warmups": 1,
  "cumulative_academic_calls": 5,
  "cumulative_warmups": 3,
  "new_initial_candidates": 0,
  "iterations": [
    {
      "number": 1,
      "finish_reason": "stop",
      "input_tokens": 3825,
      "output_tokens": 708,
      "latency_ms": 44594
    },
    {
      "number": 2,
      "finish_reason": "stop",
      "input_tokens": 3681,
      "output_tokens": 761,
      "latency_ms": 48969
    },
    {
      "number": 3,
      "finish_reason": "stop",
      "input_tokens": 3788,
      "output_tokens": 679,
      "latency_ms": 43343
    }
  ],
  "gpu_before": {
    "monotonic": 1177380.906,
    "used_mib": 1567,
    "total_mib": 32607,
    "utilization_percent": 0
  },
  "gpu_final": {
    "monotonic": 1177804.906,
    "used_mib": 1558,
    "total_mib": 32607,
    "utilization_percent": 4
  },
  "gpu_samples": 206,
  "gpu_peak_mib": 18482,
  "gpu_peak_utilization": 100,
  "status": "two_consecutive_iterations_without_substantive_reduction",
  "adequate_for_teacher_review": false,
  "publication_allowed": false,
  "participant_display": null
}

## Fuentes consultadas — lista íntegra construida por el host

docente-procedimiento:11
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

docente-requisitos:13
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

docente-procedimiento:10
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

nasa-seh:142
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

docente-requisitos:20
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

