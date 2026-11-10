# Preparación e integración de rondas CPU — 30-10-2026

Se auditó `comparison-003`, revisión/reparación y corrección localizada posterior. La mejora observada con críticas del asistente justifica ensayar rondas, pero no se presentó como crítico autónomo existente. Se implementó `web_review_rounds.py` sobre `StructuredGenerationRequest`, `ReviewRepairGenerationAdapter.call`, `CallBudget`, `Issue` y `parse_review`, sin nuevo framework ni activación de sesiones.

La composición separa respaldo externo y compatibilidad docente, conserva todas las propuestas, confirma testigos estructurales, permite hasta dos correcciones y un reintento de formato, y se detiene por respuesta idéntica, repetición/no disminución de incidencias, límite, retirada o cancelación. Esas paradas son heurísticas de recursos, no demostración semántica. Que el crítico no encuentre objeciones nunca concede publicación. Se admite que una atribución fiel a Internet sea sustentada aunque su contenido discrepe del material docente.

## Ensayo y recuperaciones conservadas

Se congelaron cuatro preguntas, fuentes y criterios en `cases.json`, `criteria.json`, `protocol.json`, `rules.json` y `frozen-sha256.json`, antes de cargar modelos. El crítico/corrector no recibió juicios del asistente ni criterios esperados. Fuentes: material docente real 22/39/73, NASA SEH209 archivado y RFC2119 adquirido públicamente en este bloque (un GET, 4723bytes). R02 añade un apunte experimental aislado sobre el significado de MUST en la misma sección RFC; es una oposición lógica concreta, **no una cita ni un error real del profesor**.

Presupuesto propio: 1800s desde `trial-clock.json`, máximo28 llamadas, sin modificar cuotas históricas. Todo CPU, pesos locales, sin instalaciones/descargas de modelos.

- Primera variante: Qwen1.5B inicial y Qwen7B crítico, dynamic-int8/oneDNN en memoria. Cuatro iniciales incoherentes/truncadas; no llegaron a revisión. No se atribuye este resultado como prueba de que las rondas no funcionen ni como una comparación causal aislada de cuantización.
- Recuperación float32 con7B: conservó reloj/cuota; el inicial seguía teniendo90s asignados al modelo pequeño. Dos timeouts y una tercera petición interrumpida. Solo se detuvieron sus dos PID propios verificados, 43112/57252. La excepción del adaptador descartó texto parcial de esta versión; **esa pérdida queda documentada**, no se reconstruyó ni se contó como respuesta. `recovery-stop-accounting.json` registra siete intentos acumulados.
- `compact-fp32`: mismos temas/preguntas/criterios, pasajes pertinentes recortados explícitamente con offsets y originales conservados; 7B float32/8threads, plazo180s para el inicial grande. Las cuatro iniciales terminaron conEOS; las cuatro críticas JSON excedieron180s. El puerto guardó cada salida antes de entregar, incluidos parciales, corrigiendo la pérdida de observabilidad para este runner. No cambió el adaptador habitual.

El último perfil terminó con **15 llamadas acumuladas** y **1531,437s**, dentro del techo original; no se reinició el reloj en sus recuperaciones. Los cuatro borradores reales y sus críticas parciales están en `compact-fp32/`. Una crítica parcial señalaba la afirmación de viabilidad, pero también exigía cobertura no necesaria del ejemplo; no es una crítica completa validada.

## Continuación expresa posterior

Cuando el usuario pidió «Continúa», el proceso ya había terminado y el reloj original llevaba horas vencido. Se mantuvo cerrado. La continuación usa un sucesor independiente con techo12 llamadas/1800s; no arrastra ni devuelve la cuota no utilizada de este ensayo. [Resultado, comparaciones y transcripciones](../2026-10-30-web-rounds-successor-cpu/report.md).

No se modificaron los ensayos C/D anteriores ni se los reinterpretó para hacerlos pasar. Tampoco se modificaron fuentes originales, SQL, políticas de sesiones, modelos o índices. La variante int8 se basó en la API instalada y [documentación primaria de PyTorch](https://docs.pytorch.org/docs/main/generated/torch.ao.quantization.quantize_dynamic.html); no se adoptó como perfil de producto. Toda salida sigue diagnóstica, sin participante/publicación, sin calificaciones ni inferencia de capacidad del alumno.
