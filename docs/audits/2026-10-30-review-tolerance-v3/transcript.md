# Revisor tolerante v3 — transcripción íntegra

Calibración de desarrollo, no revisión independiente ciega ni publicación.

## C01

### Pregunta

Quiero que una aplicación de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propón un requisito hipotético comprobable de recuperación y explica si redactarlo demuestra que es realizable.

### Respuesta examinada

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.

### Fuentes recibidas

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

### Veredicto automático bruto

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "explanation",
  "issues": []
}
```

Etiqueta esperada: no_issues_found; emitida: no_issues_found.

## C02

### Pregunta

Quiero que una aplicación de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propón un requisito hipotético comprobable de recuperación y explica si redactarlo demuestra que es realizable.

### Respuesta examinada

Un requisito hipotético comprobable de recuperación podría ser: "El tiempo para reiniciar la aplicación después de un fallo no debe exceder 5 segundos en más del 99% de los eventos de fallo." Este requisito es realizable ya que se basa en métricas claras y medibles, y puede ser verificado mediante pruebas de carga y análisis de rendimiento. Sin embargo, su realizabilidad también dependería del presupuesto y la tecnología disponibles, lo cual se verifica según la guía de requisitos del profesor.

### Fuentes recibidas

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

### Veredicto automático bruto

```json
{
  "status": "no_issues_found",
  "external_support": "supported",
  "teacher_compatibility": "compatible",
  "response_action": "explanation",
  "issues": []
}
```

Etiqueta esperada: issues_found; emitida: no_issues_found.

## C03

### Pregunta

Quiero que una aplicación de archivo vuelva a funcionar pronto tras un fallo. Con estas fuentes, propón un requisito hipotético comprobable de recuperación y explica si redactarlo demuestra que es realizable.

### Respuesta examinada

Un requisito hipotético es que la aplicación reinicie en cinco segundos. El material docente define la verificabilidad como que el requisito no se puede comprobar. Por ello, cuanto menos se pueda comprobar este requisito, más verificable es.

### Fuentes recibidas

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

### Veredicto automático bruto

```json
{
  "status": "issues_found",
  "external_support": "unknown",
  "teacher_compatibility": "conflict",
  "response_action": "repair",
  "issues": [
    {
      "kind": "contradiction",
      "claim": "El material docente define la verificabilidad como que el requisito no se puede comprobar.",
      "explanation": "Esta afirmación contradice la idea de que un requisito verificable debe poderse comprobar. La verificabilidad implica que se pueden realizar pruebas o mediciones para confirmar si el requisito se cumple. Se debe cambiar a: 'El material docente define la verificabilidad como que el requisito puede ser comprobado mediante pruebas o mediciones.'",
      "evidence": [
        {
          "source_id": "T73",
          "quote": "• Verifiability. Can the requirements be checked?"
        }
      ]
    },
    {
      "kind": "coverage",
      "claim": "",
      "explanation": "El borrador no incluye información sobre la realizabilidad del requisito, que es otro aspecto crucial mencionado en la fuente T73. Debe considerarse si la aplicación puede realmente implementar la capacidad de reiniciar en cinco segundos dadas las restricciones de presupuesto y tecnología.",
      "evidence": [
        {
          "source_id": "T73",
          "quote": "Realism. Can the requirements be implemented given available budget and technology"
        }
      ]
    }
  ]
}
```

Etiqueta esperada: issues_found; emitida: issues_found.
