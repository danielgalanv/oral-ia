# Diagnóstico CPU del prompt v2 — transcripción íntegra

Casos expuestos, sin publicación ni validación general. Las críticas automáticas son falibles. Los parciales no son revisiones completas.

## R01

### Pregunta

Quiero que una aplicación de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propón un requisito hipotético comprobable de recuperación y explica si redactarlo demuestra que es realizable.

### Borrador real conservado

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en métricas claras y medibles, y puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.

### Evidencia

**T22 — teacher/requisitos-p22**

```text
Metrics for specifying nonfunctional requirements
Robustness | Time to restart after failure Percentage of events causing failure Probability of data corruption on failure
```

**T73 — teacher/requisitos-p73**

```text
• Realism. Can the requirements be implemented given
available budget and technology
• Verifiability. Can the requirements be checked?
30/10/2014 Chapter 4 Requirements Engineering 73
```

**N209 — internet-archive/nasa-seh-p209**

```text
Reliability
□ Are clearly defined, measurable, and verifiable
reliability requirements specified?
□ Are there error detection, reporting, handling,
and recovery requirements?
□ Are undesired events (e.g., single-event upset, data
loss or scrambling, operator error) considered and
their required responses specified?
□ 
```

### Primera crítica automática

Terminación: deadline; 180.39 segundos.

```text
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "\"Este requisito es realizable ya que se basa en métricas claras y medibles\"",
      "explanation": "La fuente T22 menciona 'Time to restart after failure' como una métrica, pero no garantiza que sea fácilmente realizable. La realibilidad depende de factores como el presupuesto y la tecnología, como indica la fuente T73.",
      "evidence": [
        {"source_id": "T73", "quote": "Realism. Can the requirements be implemented given available budget and technology"}
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El requisito no aborda todos los aspectos de la recuperación mencionados en N209, como la dete
```

## R02

### Pregunta

El apunte D interpreta MUST como opcional. ¿Qué afirma RFC 2119 sobre MUST? Explícalo con un ejemplo hipotético y contrástalo con ese mismo apunte, sin dar por resuelta una discrepancia.

### Borrador real conservado

RFC 2119 define que "MUST" significa un requisito completamente obligatorio, no opcional. Por ejemplo, si un protocolo requiere que "todas las conexiones deben ser seguras", esto sería un uso correcto de "MUST". Sin embargo, el apunte D interpreta este término como opcional, lo cual contradice la definición del RFC 2119.

### Evidencia

**D — teacher/experimental-rfc-note**

```text
El apunte de esta actividad afirma sobre RFC 2119, sección 1: MUST significa un requisito completamente opcional, no una obligación absoluta.
```

**R1 — internet/rfc2119-1997**

```text
1. MUST   This word, or the terms "REQUIRED" or "SHALL", mean that the
   definition is an absolute requirement of the specification.
```

### Primera crítica automática

Terminación: deadline; 180.11 segundos.

```text
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "RFC 2119 define que 'MUST' significa un requisito completamente obligatorio, no opcional.",
      "explanation": "La cita del RFC 2119 afirma que 'MUST' es un 'requisito completamente obligatorio', mientras que el borrador afirma que es 'completamente opcional'. Esto es una contradicción clara. La corrección requerida es cambiar 'completamente opcional' a 'completamente obligatorio'.",
      "evidence": [
        {
          "source_id": "R1",
          "quote": "1. MUST   This word, or the terms \"REQUIRED\" or \"SHALL\", mean that the definition is an absolute requirement of the specification."
        }
      ]
    },
    {
      "kind": "ambigu
```

## R04

### Pregunta

Si escribo MUST en el requisito de una copia de seguridad, ¿puedo asegurar que jamás perderá datos? Explica lo que permiten concluir estas fuentes sin presuponer pruebas del sistema.

### Borrador real conservado

Según la fuente "internet/rfc2119-1997", el uso de "MUST" en los requisitos implica que es una absoluta necesidad del especificación. Sin embargo, la fuente "teacher/requisitos-p73" enfatiza que la verificabilidad de los requisitos depende del presupuesto y la tecnología disponibles. Por lo tanto, aunque "MUST" indica una exigencia crítica, no garantiza que una copia de seguridad nunca pierda datos debido a limitaciones tecnológicas o presupuestarias.

### Evidencia

**T73 — teacher/requisitos-p73**

```text
• Realism. Can the requirements be implemented given
available budget and technology
• Verifiability. Can the requirements be checked?
30/10/2014 Chapter 4 Requirements Engineering 73
```

**R1 — internet/rfc2119-1997**

```text
1. MUST   This word, or the terms "REQUIRED" or "SHALL", mean that the
   definition is an absolute requirement of the specification.
```

### Primera crítica automática

Terminación: deadline; 180.30 segundos.

```text
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "Sin embargo, la fuente 'teacher/requisitos-p73' enfatiza que la verificabilidad de los requisitos depende del presupuesto y la tecnología disponibles.",
      "explanation": "Esta afirmación contradice la fuente 'internet/rfc2119-1997', que define 'MUST' como una necesidad absoluta. La verificabilidad de 'MUST' no depende del presupuesto o la tecnología, sino de la implementación de la especificación. Se debe corregir para evitar esta contradicción.",
      "evidence": [
        {"source_id": "T73", "quote": "Verifiability. Can the requirements be checked?"}
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
     
```

## Recuperación de R01: más tiempo CPU, mismo prompt

El texto completo del crítico se transmite como observación falible, incluso si su contrato literal falla. No se transforma en evidencia validada.

### 01-review-output

Terminación: stop

```text
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "\"Este requisito es realizable ya que se basa en métricas claras y medibles\"",
      "explanation": "La fuente T22 menciona 'Time to restart after failure' como una métrica, pero no garantiza que sea fácilmente realizable. La realibilidad depende de factores como el presupuesto y la tecnología, como indica la fuente T73.",
      "evidence": [
        {"source_id": "T73", "quote": "Realism. Can the requirements be implemented given available budget and technology"}
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El requisito no aborda todos los aspectos de la recuperación mencionados en N209, como la detección de errores, el informe, el manejo y la recuperación. Se recomienda incluir estos elementos para una definición completa.",
      "evidence": [
        {"source_id": "N209", "quote": "Are there error detection, reporting, handling, and recovery requirements?"}
      ]
    }
  ]
}
```

### 02-repair-output

Terminación: stop

```text
Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en métricas claras y medibles, y puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.

Para mejorar este requisito, se deben incluir aspectos adicionales de recuperación, como la detección de errores, el informe, el manejo y la recuperación, tal como sugiere la fuente N209. Un requisito más completo podría ser:

"El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo, y se deben implementar mecanismos de detección de errores, informe, manejo y recuperación para todos los tipos de eventos de fallo, asegurando que el sistema no experimente corrupción de datos."

Este requisito completo aborda tanto la verificabilidad como la realibilidad, y considera los aspectos mencionados en la fuente N209.
```

### 03-review-output

Terminación: stop

```text
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "limit",
  "issues": []
}
```

## Parche localizado — objetivo real

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en métricas claras y medibles, y puede ser verificado mediante pruebas de carga y análisis de rendimiento.

### Reemplazo bruto

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito puede ser verificado mediante pruebas de carga y análisis de rendimiento.

### Respuesta ensamblada

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.

### Post-revisión automática falible

```json
{
  "status": "issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "\"El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo\"",
      "explanation": "La fuente T22 menciona 'Time to restart after failure' pero no especifica un tiempo específico. La fuente N209 sugiere que los requisitos de recuperación deben ser verificables, pero no establece un umbral específico. La frase del borrador contradice esto al establecer un tiempo específico.",
      "evidence": [
        {"source_id": "T22", "quote": "Time to restart after failure"},
        {"source_id": "N209", "quote": "Are clearly defined, measurable, and verifiable reliability requirements specified?"}
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El requisito propuesto no aborda todos los aspectos de la recuperación mencionados en la fuente N209, como la detección de errores, el informe, el manejo y la recuperación. Además, no considera eventos no deseados como la pérdida de datos o el error operativo.",
      "evidence": [
        {"source_id": "N209", "quote": "Are there error detection, reporting, handling, and recovery requirements?\nAre undesired events (e.g., single-event upset, data loss or scrambling, operator error) considered and their required responses specified?"}
      ]
    }
  ]
}
```
