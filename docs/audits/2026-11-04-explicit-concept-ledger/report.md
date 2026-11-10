# Registro explícito de conceptos: implementación y resultados

04-11-2026. Feature012 sigue abierta. T221/T222 son implementación y medición de laboratorio, no aceptación de T219, G2, SC001, participantes ni revisión docente.

## Resultado

El mecanismo combinado detectó y reparó el encabezado histórico **Complejidad → Completitud**, y detectó y reparó un control nuevo que atribuía la definición de trazabilidad a comprensibilidad. No contiene una tabla de sustitución de términos ni utilizó la guardia estrecha del piloto.

**No se promueve todavía:** el revisor de usos sigue produciendo críticas demasiado literales. En la pregunta sobre comprensibilidad, no ambigüedad y conjunto completo objetó injustificadamente «completo/completa» y «conjunto/especificación». Aunque el modelo aceptó su propia reparación posterior, no la cuento como mejora. La nueva vía también es costosa: unos 372 s para el caso largo, aun reutilizando su revisión de significado anterior.

[Preguntas, respuestas y correcciones íntegras](transcript-mobile.md) · [Versión móvil HTML](transcript-mobile.html) · [Métricas](metrics-final.json).

## Qué se implementó

- `concept_ledger.py`: catálogo literal de unidades de fuente con posiciones y hashes, contexto original completo, planificación de relevancia sin exponer el borrador y registro por unidades de respuesta. Los juicios se vinculan a referencias existentes y el host deriva el estado; la validez formal no demuestra verdad.
- `concept_review_loop.py`: planificación Qwen2.5-14B, revisión de significado Qwen3-8B con razonamiento, incidencias reales enviadas al reparador y revisión posterior de la versión producida. Preserva todas las unidades. Un fallo de cobertura en v4 reduce el lote; con una unidad, el host vincula el dictamen a esa única entrada, sin adivinar IDs omitidos.
- `concept_labels.py`: comparación aislada del **nombre usado** contra las definiciones originales. No recibe la descripción del autor ni el historial. Evita que una descripción correcta justifique por sí sola un nombre incorrecto. El 14B acepta, por ejemplo, trazabilidad frente a trazado y las variaciones gramaticales válidas. No constituye un evaluador humano ni independencia de checkpoint respecto del generador.
- `cached_transformers.py`, `review_repair.py`, `web_review_frame.py`: reconstrucción y validación de los contratos nativos; no se permite sustituirlos por instrucciones genéricas.
- `test_concept_ledger.py`: negativos de procedencia, referencias, cobertura, separación del borrador y recuperación de asignaciones; pruebas de estado derivado y conservación de incidencias.
- Spec, plan, tasks y [contrato](../../../specs/012-conversational-course-study/contracts/concept-ledger.md) actualizados. Se corrigió además una mención vigente desactualizada a generación v3: el piloto ya seleccionaba v4.

## Versiones conservadas

1. **run-001/v1:** el caso largo excedía el límite de entrada; otro control reparado fue rechazado por diferencia nominal y la ficción produjo abstención. Se conservan resultados y errores. El diagnóstico CPU contó 8.852 tokens frente a 7.000 permitidos: fue rechazo técnico, no fallo semántico del caso largo.
2. **run-002/v2:** representación compacta, fuentes e historial íntegros y criterios generales de equivalencia. Persistieron fallos de cobertura y de límite de referencias. También hubo una crítica errónea a un ejemplo ficticio; su cambio posterior no cuenta como mejora.
3. **run-003/v3:** se corrigieron esas trabas estructurales sin reinterpretar sus salidas. Se detectaron dos confusiones en controles derivados. El caso histórico, sin embargo, pasó incorrectamente: el revisor asociaba la descripción con Completeness e ignoraba el encabezado Complejidad. La candidata de generación real quedó conservada, pero el revisor omitió unidades.
4. **run-004/v4 + labels/v1:** separación explícita de nombre y significado, sin diccionario académico. Se reutilizan identificadamente tres revisiones v3 válidas estructuralmente; los otros dos controles reciben revisión nueva completa. No son cinco conversaciones inéditas ni transferencia ciega. Las objeciones que recibe el generador proceden de los modelos, no de mis correcciones manuales.

## Último ensayo

| Caso | Observación | Llamadas nuevas | Segundos |
|---|---|---:|---:|
| REG_H_BAD | Nombre incorrecto detectado; reparación y revisión posterior sin incidencias del modelo. | 10 | 371.64 |
| REG_FIXED | Control válido trazabilidad/trazado aceptado. | 1 | 6.45 |
| REG_FICTION | Revisión v3 conservada; sin llamada nueva ni rechazo de cifras inventadas. | 0 | 0.00 |
| FRESH_LABEL_BAD | Control derivado comprensibilidad/trazabilidad detectado y reparado. | 5 | 61.62 |
| LIVE_GENERATED | Dos falsas objeciones literales; reformulación innecesaria, no mejora acreditada. | 11 | 342.91 |

27 intentos nuevos de llamada, todos con salida completa en este último ensayo; presupuesto propio máximo 48. Cero generaciones iniciales nuevas en v4: se reutilizan candidatas explícitas de v3. El control derivado se preparó antes de inferir; el oráculo se guardó por separado y no se envió al proveedor. Una reparación máxima por caso, 180 s por etapa, 600 s por caso, 7.000 tokens de entrada sin recorte silencioso. No se consumió la reserva ni presupuestos históricos. Los primeros fallos de preparación UTF-8 y de invocación de pruebas quedan registrados; ocurrieron antes de inferencia o ejecución de pruebas, respectivamente.

## Validación y preservación

- **688 pruebas del módulo aprobadas** (`cpu-final.log`); 79 dirigidas también pasan y están incluidas en esas 688, no se suman como pruebas distintas.
- Black conforme en los módulos afectados. Ruff en `src tests scripts`: 10 diagnósticos previos, 0 nuevos, comparados con multiplicidad por archivo/código/mensaje. El barrido inicial desde la raíz también incluyó copias documentales de código; se conserva aparte y no se compara falsamente con el baseline ejecutable.
- **467 archivos históricos distintos**, contenidos en 470 entradas de tres mapas, mantienen hashes; originales docentes revalidados antes/después de llamadas. Código fuente ejecutado congelado en cada paquete.
- Modelos propios cerrados tras los cinco casos. GPU: aproximadamente 2,1 GiB del escritorio y 30 GiB libres al comprobar. T permanece pausado; no se reinicia. Sin descargas, red, Reset, commits, migraciones ni datos docentes modificados.

## Límites y siguiente trabajo concreto

El extractor identifica definiciones en viñetas y conserva la página completa como contexto; no demuestra extracción semántica exhaustiva de todo documento. La comprobación aislada actúa sobre encabezados que la revisión vinculó a definiciones con nombre, no sobre todas las menciones o todas las palabras clave. Las traducciones propuestas por el modelo son tentativas. La presencia y correspondencia literal de fuentes prueba trazabilidad estructural, no respaldo semántico.

T219 sigue parcial: faltan controlar las falsas objeciones materiales antes de reparar, medir cobertura de conceptos sin encabezado y acotar el coste del recorrido completo sin las revisiones v3 reutilizadas. Queda T223 para evaluar la validez/materialidad de las objeciones con controles nuevos. No se conecta esta candidata al chat normal: continúa generación v4 con palabras clave y revisión estable v8; la guardia estrecha anterior no se modificó y no intervino en estos ensayos. El resultado demuestra mitigación del error concreto, no solución universal.

Comprobación final: 272 archivos fuente coinciden con la versión ejecutada; IDs de tareas sin duplicados. El primer Black restringido quedó esperando: se cerró exclusivamente su árbol de procesos y se repitió fuera de ese bloqueo, con caché del proyecto; siete archivos sin cambios (`black-final.log`, `sandbox-format-cleanup.json`). Se liberó la petición temporal de evitar suspensión al terminar.
