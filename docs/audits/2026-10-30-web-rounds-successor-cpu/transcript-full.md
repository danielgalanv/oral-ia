# Rondas CPU: entradas, fuentes, críticas y versiones completas

Diagnóstico sin publicación. Ninguna respuesta fue reescrita manualmente.

## R01: Quiero que una aplicación de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propón un requisito hipotético comprobable de recuperación y explica si redactarlo demuestra que es realizable.

### Inicial real

````text
Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en métricas claras y medibles, y puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.
````

### Pase breve: critic_keeps_initial_unverified

#### review

````text
SOURCE: sustained
COURSE: compatible
ACTION: keep
ADVICE: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." (T22) Este requisito es realizable y verificable (T73).
````

### Contrarrevisión de premisas: challenge_keeps_unverified

#### review

````text
SOURCE: compatible  
COURSE: compatible  
ACTION: keep  
ADVICE: No substantive objections found.
````

### localized14-trace.json: critic_no_correction_unverified

````text
SOURCE: sustained
COURSE: compatible
ACTION: keep
CLAIM: NONE
ADVICE: Requisito claro y medible, verificable por pruebas. "Metrics for specifying nonfunctional requirements" (teacher/requisitos-p22).
````

### recover-advice-trace.json: budget_contract_or_deadline

Parcial no aplicado:

````text
{"old":"\"El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo.\"","new":"\"El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99%
````

### Material docente entregado

teacher/requisitos-p22

````text
Metrics for specifying nonfunctional requirements
Robustness | Time to restart after failure Percentage of events causing failure Probability of data corruption on failure
````

teacher/requisitos-p73

````text
• Realism. Can the requirements be implemented given
available budget and technology
• Verifiability. Can the requirements be checked?
30/10/2014 Chapter 4 Requirements Engineering 73
````

### Información de Internet entregada

internet-archive/nasa-seh-p209

````text
Reliability
□ Are clearly defined, measurable, and verifiable
reliability requirements specified?
□ Are there error detection, reporting, handling,
and recovery requirements?
□ Are undesired events (e.g., single-event upset, data
loss or scrambling, operator error) considered and
their required responses specified?
□ 
````

El texto final permanece idéntico al inicial; no está aprobado para participante.

## R02: El apunte D interpreta MUST como opcional. ¿Qué afirma RFC 2119 sobre MUST? Explícalo con un ejemplo hipotético y contrástalo con ese mismo apunte, sin dar por resuelta una discrepancia.

### Inicial real

````text
RFC 2119 define que "MUST" significa un requisito completamente obligatorio, no opcional. Por ejemplo, si un protocolo requiere que "todas las conexiones deben ser seguras", esto sería un uso correcto de "MUST". Sin embargo, el apunte D interpreta este término como opcional, lo cual contradice la definición del RFC 2119.
````

### Pase breve: unchanged_stop

#### review

````text
SOURCE: unsupported  
COURSE: conflict  
ACTION: repair  
ADVICE: "RFC 2119 states, 'MUST means that the definition is an absolute requirement.' (R1)"
````

#### repair

````text
RFC 2119 define que "MUST" significa un requisito completamente obligatorio, no opcional. Por ejemplo, si un protocolo requiere que "todas las conexiones deben ser seguras", esto sería un uso correcto de "MUST". Sin embargo, el apunte D interpreta este término como opcional, lo cual contradice la definición del RFC 2119.
````

### Material docente entregado

teacher/experimental-rfc-note

````text
El apunte de esta actividad afirma sobre RFC 2119, sección 1: MUST significa un requisito completamente opcional, no una obligación absoluta.
````

### Información de Internet entregada

internet/rfc2119-1997

````text
1. MUST   This word, or the terms "REQUIRED" or "SHALL", mean that the
   definition is an absolute requirement of the specification.
````

El texto final permanece idéntico al inicial; no está aprobado para participante.

## R03: La diapositiva usa SHALL y RFC 2119 usa también MUST. ¿Eso los hace contradictorios? Explica brevemente el sentido relevante de ambos y da un ejemplo ficticio sencillo.

### Inicial real

````text
"SHALL" y "MUST" se usan para indicar requisitos obligatorios, aunque "SHALL" suele ser preferido en algunos contextos como una terminología más clara para lo que "MUST" expresa. Por ejemplo, en un protocolo de comunicación, si se dice "SHALL encrypt all data transmissions", esto significa que todas las transmisiones de datos deben ser encriptadas, igual que si se dijera "MUST encrypt all data transmissions". Ambas expresiones indican que el encriptado es un requisito indispensable del protocolo.
````

### Pase breve: critic_keeps_initial_unverified

#### review

````text
SOURCE: compatible  
COURSE: compatible  
ACTION: keep  
ADVICE: No son contradictorios. Ambas expresiones indican requisitos indispensables. Ej.: "SHALL encrypt all data transmissions" = "MUST encrypt all data transmissions".
````

### Contrarrevisión de premisas: challenge_keeps_unverified

#### review

````text
SOURCE: compatible  
COURSE: compatible  
ACTION: keep  
ADVICE: No hay contradicción; ambos términos indican requisitos indispensables.
````

### Material docente entregado

teacher/requisitos-p39

````text
• Use language in a consistent way. Use shall for
mandatory requirements, should for desirable
requirements.

````

### Información de Internet entregada

internet/rfc2119-1997

````text
1. MUST   This word, or the terms "REQUIRED" or "SHALL", mean that the
   definition is an absolute requirement of the specification.
````

El texto final permanece idéntico al inicial; no está aprobado para participante.

## R04: Si escribo MUST en el requisito de una copia de seguridad, ¿puedo asegurar que jamás perderá datos? Explica lo que permiten concluir estas fuentes sin presuponer pruebas del sistema.

### Inicial real

````text
Según la fuente "internet/rfc2119-1997", el uso de "MUST" en los requisitos implica que es una absoluta necesidad del especificación. Sin embargo, la fuente "teacher/requisitos-p73" enfatiza que la verificabilidad de los requisitos depende del presupuesto y la tecnología disponibles. Por lo tanto, aunque "MUST" indica una exigencia crítica, no garantiza que una copia de seguridad nunca pierda datos debido a limitaciones tecnológicas o presupuestarias.
````

### Pase breve: critic_keeps_initial_unverified

#### review

````text
SOURCE: supported  
COURSE: compatible  
ACTION: keep  
ADVICE: "MUST indica una exigencia crítica (internet/rfc2119-1997), pero no garantiza verificabilidad absoluta bajo todas las condiciones (teacher/requisitos-p73)."
````

### Contrarrevisión de premisas: unchanged_stop

#### review

````text
SOURCE: supported  
COURSE: conflict  
ACTION: repair  
ADVICE: "MUST" implies critical need, but verifiability depends on resources (T73). Thus, while "MUST" ensures importance, it doesn't guarantee zero data loss due to tech/pres constraints (R1).
````

#### repair

````text
Según la fuente "internet/rfc2119-1997", el uso de "MUST" en los requisitos implica que es una absoluta necesidad del especificación. Sin embargo, la fuente "teacher/requisitos-p73" enfatiza que la verificabilidad de los requisitos depende del presupuesto y la tecnología disponibles. Por lo tanto, aunque "MUST" indica una exigencia crítica, no garantiza que una copia de seguridad nunca pierda datos debido a limitaciones tecnológicas o presupuestarias.
````

### Material docente entregado

teacher/requisitos-p73

````text
• Realism. Can the requirements be implemented given
available budget and technology
• Verifiability. Can the requirements be checked?
30/10/2014 Chapter 4 Requirements Engineering 73
````

### Información de Internet entregada

internet/rfc2119-1997

````text
1. MUST   This word, or the terms "REQUIRED" or "SHALL", mean that the
   definition is an absolute requirement of the specification.
````

El texto final permanece idéntico al inicial; no está aprobado para participante.

## Procedencia legible

Material docente: 5 - Requisitos.pdf, páginas22,39,73, adaptación UPM/Sommerville, edición curso22-23. NotaD: control experimental aislado, no cita del profesor.

Información de Internet: RFC2119, S.Bradner/RFC Editor, marzo1997, sección1 (MUST/SHALL); captura pública exclusiva external-rfc2119.json del dossier previo. Enlace: https://www.rfc-editor.org/rfc/rfc2119.txt . NASA SEH, NASA/SP-2016-6105 Rev2, página física209, archivo autorizado adquirido anteriormente, no descarga nueva de esta fase. Autoría/captura/edición/hash completos en source-provenance.json y recibo previo.

NASA, enlace del original archivado: https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf . La captura usada es la anterior; no se afirma descarga nueva.
