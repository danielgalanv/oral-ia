# Revisión y reparación diagnósticas — no autorización de participante

Dos entradas explícitas sobre GenerationPort existente:

1. `ReviewRepairGenerationAdapter.generate`: candidata inicial, llamada separada al mismo14B como revisor, máximo una reparación si existen objeciones estructuralmente válidas, post-revisión. **Es autocrítica del mismo modelo, no la revisión del asistente que identificó los errores.** Resultado experimental negativo documentado; no se promueve como puerta semántica.
2. `repair_with_supplied_review`: una candidata y una crítica ya producida por un revisor externo al corrector, con procedencia explícita. En el control medido esa crítica fue redactada por el asistente técnico tras leer fuentes/originales; una llamada local de corrección y revisión posterior del asistente por separado. No es un revisor autónomo local ni se inventa un veredicto posterior.

Críticas con esquema `status`/`issues`; hasta3objeciones. Cada objeción incluye tipo, cita de candidata (salvo omisión), explicación y hasta2testigos source_id/quote de fuentes recibidas; quote≤240caracteres. Solo se normaliza whitespace, sin traducir, quitar palabras o viñetas. IDs/texto anclados al contexto, no a memoria del modelo. Es control de procedencia, no prueba de verdad. Un revisor puede señalar cosas falsas con citas literales o fallar por detalles de presentación; ambos se reportan.

`no_issues_found` nunca significa supported. Estado permanente unverified/not_assessed y publicación false. Los ejemplos hipotéticos coherentes se contrastan en su principio/conclusión, sin exigir sus cifras o nombres literales. No se ejecutan instrucciones/herramientas del candidato/crítica ni se evalúan estudiantes.

Cada llamada mantiene LabGenerationConstraints768tokens/50.000ms. El flujo completo optativo permite hasta200s por pregunta para4llamadas; default histórico50s intacto. Presupuesto de llamadas compartido y finito, no reiniciado por fases/sesiones. No hay rondas automáticas adicionales. Crítica inválida/incompleta o reparación incompleta conservan inicial diagnóstica; post-revisión incompleta/ inválida no autoriza la reparación. Brutos y motivos íntegros.

DiagnosticStudy crea una copia del workflow por inspección y liga su guard a permiso/corpus vigentes de esa sesión, compartiendo solo transporte y presupuesto. Revalida antes/después de cada etapa, invalida por cierre/cancelación/retirada y purga trazas. Una cancelación absorbida por proveedor no permite iniciar otra etapa. `timeout.expired()` evita aceptar el resultado tras señal de timeout temprano de Windows. Solo la candidata realmente mostrada y confirmada entra en ese historial; borradores/críticas nunca entran como mensajes académicos ocultos.

Materiales informa la duración por llamada y total, identifica autocrítica cuando ese camino se inyecta y muestra inicial/crítica/reparación como texto inerte dentro de inspección. No hay selector HTTP que conceda al participante esta capacidad o convierta una crítica suministrada por cliente en autoridad. El control con crítica del asistente fue offline/experimental; no se presenta como la UI real de E2 aceptada.

Resultado medido28-10: autocrítica14B0mejoras claras/8casos, dos errores prioritarios intactos; control asistido4expuestos,2objetivos corregidos/2mejoras parciales con defectos residuales. Evidencia y límites en `docs/audits/2026-10-28-review-repair/` y `docs/audits/2026-10-28-agent-assisted-repair/`. Mantener revisión crítica de estos resultados; no abrir T090/T150/G2/SC001 o participante.
