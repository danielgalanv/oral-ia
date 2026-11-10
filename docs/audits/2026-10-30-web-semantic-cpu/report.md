# Decisión de contenido real en CPU y navegador — 30-10-2026

**Resultado: dos candidatos de revisión medidos, ninguno promovido. Navegador operativo completado. La ampliación autónoma con explicación académica sigue pendiente.** No se ha añadido una capa estructural que finja resolver la semántica ni instalado un veredicto de fixture en producción.

Se siguió la [auditoría independiente](../2026-10-30-web-fallback-independent-review.md): fuentes y criterios antes de evaluar, modelos reales CPU, oráculos fuera del proceso de inferencia y comparación explícita de resultados. El generador no se aprobó a sí mismo: los modelos actuaron como revisores de afirmaciones fijas, sin generar respuestas al alumno. Eso permite medir un candidato; no convierte su declaración en verdad.

## Ensayos congelados

Se auditaron los evaluadores existentes: `verification.py` y `claim_review.py` comprueban testigos/estructura y no entailment; `review_repair.py` es autocrítica diagnóstica con resultados previos no promovidos. No se reabrieron esas campañas. No había un evaluador semántico especializado validado que reutilizar. Se usaron Transformers y pesos ya instalados, sin dependencias ni descargas nuevas.

1. **Qwen2.5-1.5B-Instruct**, snapshot `989aa7980e4cf806f80c7fef2b1adb7bc71aa306`: CPU float32, 4 threads, cuatro llamadas greedy, 256 tokens y hasta 75 s por llamada, 600 s globales. Hipótesis limitada: comprobar si el recurso pequeño disponible distingue estas relaciones antes de integrarlo. No se asumía que ya fuese un buen verificador.
2. Tras el fallo del pequeño, **una única confirmación con Qwen2.5-7B-Instruct**, snapshot `a09a35458c702b33eeacc393d103063234e8bc28`: CPU float32, 4 threads, cuatro controles nuevos cercanos, misma instrucción y 256 tokens, 120 s por llamada/600 s globales. El mayor tamaño era una hipótesis de capacidad, no una garantía. Memoria libre inicial ~98 GiB frente a ~29 GiB de parámetros float32. No es una comparación controlada para ranking porque cambian los casos.

Ambos runtimes confirman `device=cpu`, `dtype=torch.float32` y `torch=2.13.0+cpu`. No hubo GPU, CUDA, modelos descargados o proveedor remoto. Cada candidato emitió cuatro salidas completas con EOS, sin reintentos de contenido ni cambios de prompt tras observarlas. Los tiempos generativos fueron 18,7–21,7 s en 1.5B y 65,7–93,8 s en 7B; carga/hash del 7B unos 26 s. No se ampliaron los plazos habituales de autoestudio para hacerlos caber.

Los archivos `inputs.json`, `oracle.json`, `protocol.json`, `instruction.txt` y sus SHA256 se fijaron antes de cada ensayo. El runner nunca lee el oráculo para inferir ni envía IDs de caso/etiquetas esperadas. La misma instrucción se conserva entre modelos. Los ocho casos no se habían ejecutado ni usado para ajustar esos candidatos; son controles pequeños construidos para este bloque, **no** la reserva histórica ni una validación de población independiente. Ahora quedan expuestos.

Fuentes: capturas originales NASA SEH ya autorizadas del paquete v2 —páginas físicas 208, 209 y 140— y páginas docentes Requisitos 20/73 y Procedimiento 10/12/13. No se simula que estas capturas se descargaron de Internet durante la evaluación: se fijaron desde el archivo existente. El ensayo de navegador adquiere una fuente pública distinta y se informa por separado.

Las situaciones son complemento compatible, contradicción, terminología compatible e incertidumbre. **C02 y D02 incluyen una variante docente contrafactual aislada**, que afirma lo opuesto a la condición examinada: implementación cómo/qué y factibilidad/imposibilidad, respectivamente. Se conserva únicamente en los datos experimentales; no es una cita del profesor ni modifica un documento activo. El modelo ve texto, no una etiqueta «contradicción». Esto prueba un control semántico claro, no una discrepancia real descubierta en el curso ni recuperación automática fuera del top-k.

## Resultados y decisión

| Medida, cuatro casos por candidato | 1.5B | 7B |
|---|---:|---:|
| Ambos ejes correctos con salida utilizable | 0/4 | 2/4 |
| Falsos permisos con parser estricto | 0 | 0 |
| Falsos rechazos de los positivos | 2 | 0 |
| Falsos conflictos | 0 | 1 |
| Conflictos esperados no identificados | 1 | 1 |
| Abstenciones, incluidas salidas inválidas | 4 | 2 |
| Salidas inválidas | 4 | 1 |

El criterio previo era 4/4 en ambos ejes y ningún permiso/conflicto falso. **Ninguno lo cumple.** Los ceros de permisos no acreditan validación: el 1.5B bloquea todo por esquema; en el 7B el esquema bloquea precisamente el caso de contradicción y el caso incierto tiene apoyo `unknown`.

Fallos de significado observados, separados del formato:

- **C04, 1.5B:** escribe `supported: true` para una garantía de reducir costes a la mitad; su propia razón reconoce que la fuente no trata esa afirmación. No se reinterpreta el booleano como permiso válido.
- **D02, 7B:** llama compatibles a exigir factibilidad técnica y prohibir requisitos factibles. Lo justifica como «diferentes perspectivas». Además mezcla el enum de apoyo con el de compatibilidad. Reparar el JSON no resolvería el error de significado.
- **D04, 7B:** reconoce que no hay respaldo para garantizar plazos, pero declara `conflict` frente a material que no afirma lo contrario. Confunde falta de respaldo con contradicción.
- D01/D03 obtienen los dos veredictos esperados en el 7B, pero sus razones son breves y no documentan una comparación exhaustiva del catálogo. Dos positivos no compensan los controles negativos fallidos ni acreditan autoría/edición/independencia de fuentes.

El scorer no corrige campos, enums o JSON ilegible. Se conserva la revisión v1 del scorer: solo contaba falsos conflictos cuando el oráculo decía compatible. La v2 incluye también conflictos emitidos ante un oráculo incierto, y compara solo los dos ejes, dejando fuera metadatos del oráculo. Este cambio de contabilidad está versionado; no modifica entradas, criterios semánticos, salidas ni modelos. Ambos resultados del 1.5B se conservan; la decisión de no promoción no cambia.

Salidas y entradas completas legibles: [1.5B](cpu-recovery-002/review-transcript-full.md), [7B](seven-b-confirmation/review-transcript-full.md). Resultados máquina: `score-v2.json` en cada carpeta. No hay transcripción de una explicación académica nueva porque no se ejecutó el generador de respuestas ni se autorizó una salida a participante.

Dos fallos mecánicos se preservan antes de la ejecución efectiva: `device_map` requería Accelerate ausente; se cargó explícitamente a CPU sin instalarlo. Después, la versión de Transformers devolvía un contenedor de tokens distinto; se pasó el diccionario explícito a `generate`. No habían producido texto. Se conservaron scripts/logs de ambos arranques y `runtime.json`; la recuperación `cpu-recovery-002` mantiene el reloj original de 600 s mediante `trial-clock.json`. No se gastaron/reiniciaron presupuestos históricos.

## Navegador real, separado de la semántica

Se probó la interfaz existente en una pestaña real del navegador integrado, puerto propio 8041, recuperación densa real en CPU, índice nuevo exclusivamente en este dossier y proveedor **FIXTURE_CPU_NO_LLM**. No hay nuevas respuestas académicas. El build es el ya verificado de la entrega anterior, sin sobrescribirlo. El índice se aisló para no abrir/modificar el histórico; su identidad confirma CPU.

Recorrido observado:

1. Entrar en consulta e inspección temporal. Ver el proveedor fixture y el aviso previo de Internet.
2. Preguntar «¿Qué es un requisito verificable?». La salida fixture, visible como texto inerte, registra cinco pasajes y cero mensajes previos. Cuota generativa 1.
3. Seleccionar el concepto configurado y registrar una decisión docente diagnóstica explícita. El navegador muestra que ranking/cero pasajes no bastan. Esto **no** es una decisión autónoma de insuficiencia.
4. Consultar la fuente pública original. Un GET real a RFC Editor, 4.723 bytes, sin error/reintento. Se muestran «Información de Internet», enlace, entidad, edición y `acquired_unreviewed`, con respaldo/compatibilidad inciertos. No se entrega ese texto al modelo. El recibo registra 117 páginas del catálogo para el contrato estructural, no comprensión semántica de las 117.
5. Preguntar «¿Y cómo puedo comprobar ese requisito?». La salida fixture conserva dos mensajes de historial local; cuota 2. El contenido RFC no aparece en el contexto. No hubo una llamada generativa adicional por descargar.
6. El plazo web de 60 s vence: se oculta la evidencia externa y aparece offline, manteniendo ambos turnos locales. Cerrar y reabrir no renueva la cuota ni ese plazo; cerrar finalmente descarta el contenido temporal.

Se guardaron once recibos HTTP exclusivos (`browser-001.json`–`011.json`), tres capturas, estados completos y [transcripción fixture](browser-transcript.md). [Aviso previo](browser-notice.png), [fuente atribuida](browser-internet.png), [continuación](browser-continuation.png). La selección Playwright no encontró el control en esta superficie; se completó con las acciones accesibles nativas. No se inyectó JavaScript ni se invocó un endpoint directamente desde el navegador para sustituir la prueba de interfaz.

Servidor propio PID 57284 terminado con código 0 y `Application shutdown complete`; pestaña propia cerrada. Los dos procesos de inferencia terminaron normalmente. No se detuvo ningún proceso ajeno.

## Qué sigue faltando y cómo reproducir

**No se ha conectado la cadena autónoma completa**: alcance e insuficiencia tras ampliación local → adquisición → respaldo y compatibilidad → generación → revisión independiente → explicación atribuida. Los modelos medidos no satisfacen el contraste. Tampoco se ha producido la explicación útil positiva pedida dentro de esa cadena. No se presenta una fixture o revisión manual como sustituto. Lo que sí se ha ejecutado es la decisión de contenido real de dos candidatos y el recorrido operativo del producto; ambos límites son observables y conservados.

Los protocolos ejecutados ya concretan modelo, pesos, fuentes, presupuesto y criterio; no es una propuesta sin ensayar. Para un próximo candidato hace falta superar los controles de contradicción e incertidumbre con **casos nuevos** y comprobar autoría/contexto/vigencia e independencia externa, además de la suficiencia local. Reutilizar C/D serviría para diagnóstico expuesto, no para acreditar generalización. La latencia CPU medida debe entrar en el diseño antes de intentar varias revisiones dentro de un turno de 50/180 s; no se promete que aumentar tamaño arregle significado o presupuesto.

Reproducción del navegador, sin modelos generativos: usar una carpeta NUEVA, copiar `serve_browser.py` y `browser-policy.json`, sin `stop-request` ni recibos/índice anteriores, y ejecutar desde el workspace:

```powershell
.venv/Scripts/python.exe <carpeta-nueva>/serve_browser.py --package v2 --retrieval --study-lab --test-provider --port 8041 --no-browser
```

El runner busca el workspace por su ubicación `docs/audits/<carpeta>` y usa el build aislado anterior. Entrar en `http://127.0.0.1:8041/tecnica?documental=1` y seguir los seis pasos. Crear `stop-request` únicamente en esa carpeta detiene su servidor propio. Los runners y recibos de este dossier no deben reutilizarse para sobrescribir evidencia.

Reproducción de inferencia: copiar a otra carpeta las entradas/protocolo/instrucción/hash de `seven-b-confirmation` y su `run_review.py`, conservar el snapshot local indicado y ejecutar ese script con `.venv/Scripts/python.exe`. Son cuatro llamadas CPU nuevas y hasta 600 s; no se ejecutan por abrir el informe. El runner rechaza reutilizar una carpeta con resultados/runtime. No se repitió el ensayo tras observar fallos.

Comprobaciones actuales: **76 pruebas Python y 14 UI pasan**; Ruff global mantiene diez diagnósticos previos, cero nuevos, comparados con Counter de ruta/código/mensaje y multiplicidad. No se atribuyen otra vez las 123 regresiones de la entrega anterior. Scripts nuevos comprobados con Black/Ruff; producción permanece byte a byte igual a la entrega auditada. Los 308 archivos históricos del manifiesto previo siguen iguales. Evidencia contable en `final-checks.json`.

## SpecKit y estados

Se actualizaron spec/plan/tasks por adendas, sin regeneración ni pérdida de historia. Analyze final acotado: ocho FR, SC-008/009 y tareas del incremento trazadas, sin requisitos sin tarea, duplicidades de requisitos ni contradicciones constitucionales bloqueantes. Checklists previos completos; no hay `extensions.yml`/hooks. Converge deja tres hallazgos altos parciales —evaluador, cadena y validación nueva— trazados como T156–T158. T154/T155 registran únicamente ensayo diagnóstico negativo y navegador operativo terminado.

**T116–T118 y T151–T153 permanecen abiertos.** T114/T115 conservan su estado operativo anterior. No se cambia FR-014, T090/T150, G2/G3/G4, consentimiento, reserva, políticas habituales, acceso de alumnos ni aceptación docente. Sin commits, Reset, migraciones o cierre de Feature012. Los únicos archivos fuera del dossier modificados en este bloque son spec/plan/tasks; no se ha introducido un evaluador no acreditado en producción.
