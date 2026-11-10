# Rondas automáticas de revisión/corrección: resultado real CPU

**No se observó una mejora aplicada en los cuatro casos.** La propuesta se implementó y ensayó con modelos reales, sin críticas del asistente dentro del bucle. Los resultados no justifican activar la ampliación autónoma ni concluir que las rondas sean inútiles en general: sigue faltando un crítico fiable, y el último intento de reparación14B no terminó dentro del límite CPU.

## Base y método

La auditoría de `comparison-003` encontró reparaciones localizadas útiles en trazabilidad y una pregunta nueva, pero no en otra; las críticas eran del asistente, no automáticas. Los perfiles posteriores mejoraron recuperación/instrucciones y conservaron fallos localizados. Se reutilizaron sus renderers, `GenerationPort`, ejecutor, presupuestos y estrategia de conservar lo válido.

Se añadieron `src/oralia/course_dialogue/web_review_rounds.py` y pruebas. La composición experimental genera, revisa dos ejes, devuelve objeciones con evidencia, corrige y puede revisar después. Máximo dos correcciones, un reintento de formato y paradas por falta de cambio/progreso, contratos, retirada y tiempo. Los tests demuestran el recorrido y los límites; no validan semántica. No se instaló el candidato en la sesión docente ni en participantes.

El [ensayo predecesor](../2026-10-30-web-review-rounds-cpu/report.md) produjo cuatro iniciales reales con7B float32, pero sus críticas JSON no terminaron en180s. Se conservaron todos los intentos, incluido un fallo de configuración y una pérdida de texto parcial en la primera recuperación, declarada expresamente. El predecesor cerró su presupuesto con15llamadas/1531,437s. No se reabrió al recibir la continuación del usuario.

Este sucesor tiene presupuesto **nuevo y separado: máximo12llamadas y1800s**. Reutiliza aquellos cuatro borradores completos, mismas preguntas/fuentes/criterios y juicios externos sellados, que nunca se dan al modelo. Es desarrollo sobre casos expuestos, no reserva ni validación independiente. Las fases posteriores se fijaron prospectivamente; sus resultados no sustituyen los del primer pase.

Se aclaró en todos los prompts: comprobar primero si la fuente sostiene lo que se le atribuye y después comparar la proposición con una afirmación docente del mismo contexto. La atribución fiel «la fuente afirma X» puede estar sustentada aunque X discrepe del curso. Ausencia de respaldo y terminología diferente no demuestran contradicción. No se penaliza estilo, repetición, falta de exhaustividad o ficción coherente.

## Qué se ejecutó

| Fase | Ejecución real | Resultado |
|---|---|---|
| Crítica breve7B | Cuatro críticas y una corrección | Tres propuestas de conservar; enR02 pidió corregir una atribución correcta y el corrector devolvió el texto idéntico |
| Contrarrevisión de premisas7B | Tres críticas de los borradores conservados y una corrección | R01/R03 conservados; R04 recibió una objeción mal fundada y volvió idéntico |
| Capacidad14B | Una crítica del primer caso aún no corregido | Conservó el borrador, omitiendo el error de viabilidad |
| Recuperación de críticas14B | Un intento de parche localizado | Recibió todas las críticas automáticas anteriores, incluso la parcial, como datos falibles; llegó al límite180s sin terminar el parche; no se aplicó |

Total sucesor: **11 de12llamadas**, última salida a **1517,625s** del reloj original del sucesor. No hubo otra asignación, reintento final ni consumo de la llamada restante para simular convergencia. Una primera carga de la contrarrevisión salió con código1 sin diagnóstico ni llamada registrada; se conservó el log vacío y se recuperó una vez sin reiniciar reloj/cuota.

Modelos: Qwen2.5-7B y Qwen2.5-14B locales, snapshots `a09a35458c702b33eeacc393d103063234e8bc28` y `cf98f3b3bbb457ad9e2bb7baf9a0125b6b88caa8`, **CPU float32,8threads, Torch2.13.0+cpu**. El14B se eligió por la evidencia previa de corrección, no por suponer infalibilidad; no es la misma ejecución NF4/GPU de aquellos informes. No se usó GPU/CUDA ni se descargaron pesos.

Críticas128tokens, correcciones completas192tokens y parche96tokens,180s por llamada dentro del límite expandido registrado. El parche14B se detuvo tras69tokens/180,485s: no hay propuesta completa ni revisión posterior de ese texto. Las dos correcciones completas anteriores fueron idénticas a la inicial y activaron la parada. **No se ejecutó ninguna post-revisión real de una corrección completa distinta**, porque nunca se alcanzó esa precondición. Ese tramo está probado con dobles, no acreditado semánticamente por esta ejecución.

## Comparación sustantiva, sin convertir opiniones en verificación

| Caso | Lectura externa de inicial/final | Qué falló en el crítico |
|---|---|---|
| R01 recuperación hipotética | La medida5s/99% es una ilustración admisible. Pero afirmar que el requisito es realizable por ser medible no está demostrado; la salvedad posterior no justifica esa conclusión. Texto final idéntico | Los críticos7B y14B lo conservaron; relacionado con una métrica no equivale a demostrar viabilidad |
| R02 oposición concreta sobre RFC2119 | Inicial adecuada: atribuye obligatoriedad a RFC, reconoce la interpretación opuesta del apunteD y da un ejemplo coherente. Se conserva idéntica | Declaró SOURCE unsupported aunque su propia cita deRFC respalda la atribución. El corrector resistió esa mala objeción |
| R03 SHALL/MUST | Núcleo de equivalencia correcto. Queda una preferencia/mayor claridad deSHALL no acreditada en esas fuentes. Se registra como reserva lateral, no como falsedad demostrada ni fracaso entero por estilo | Conservó esa reserva; además utilizó compatible como etiqueta del ejeSOURCE |
| R04 garantía de no perder datos | Es correcto queMUST no garantiza el resultado. Pero atribuye a verificabilidad la dependencia presupuesto/tecnología queT73 trata como realizabilidad. Se conserva idéntica | Primero lo conservó; la contrarrevisión marcó conflicto sin una oposición concreta y repitió la confusión en lugar de identificarla |

R02 usa una nota experimental aislada que afirma sobre la **misma sección y término RFC** lo contrario del original. No se inventa un error del profesor real ni se reemplaza su material activo. Las otras fuentes docentes son originales inalterados. La medición no acredita descubrir una contradicción natural en todo el corpus o ampliar automáticamente más allá del top-k.

Balance de los cuatro textos: **0mejoras claras,0errores nuevos aplicados,0finales distintos,2correcciones completas idénticas y1parche incompleto**. Hubo **2críticas completas equivocadas o mal fundadas** (R02 y contrarrevisiónR04). En el primer pase se conservaron **2errores sustantivos** (R01/R04) y **1reserva lateral de procedencia** (R03). El recuento estricto de procedencia del baseline es3; no se infla eso como tres respuestas centralmente falsas ni se convierte corregir estilo en una mejora. Los juicios originales y esta distinción quedan en `external-assessment.json`.

Las críticas repetidas no son muestras independientes. Los modelos comparten familia y varios roles usan el mismo checkpoint. `ACTION: keep`, una fuente citada, una salida completa o acuerdo entre críticos **no** probaron validez. Las falsas conservaciones son opiniones equivocadas del candidato, no publicaciones: `publication_allowed=false` y `participant_display=null` siempre.

## Evidencia y reproducción

- [Transcripción legible completa](transcript-full.md): iniciales, críticas, intentos, fuentes y versiones. Ningún texto académico fue corregido manualmente.
- [Mensajes efectivos y salidas exactas](effective-messages-full.md), archivos `*-call-*-request/result.json` y `raw-port-*`: incluyen los parciales no aplicados. `recover-advice-input.json` permite comprobar que solo entraron críticas automáticas, no los baseline/criterios del asistente.
- `protocol.json`, `challenge-protocol.json`, `localized14-protocol.json`, `recover-advice-protocol.json`: límites y versiones. `trial-clock.json` es el único reloj del sucesor; las fases lo conservan.
- Material docente: Requisitos22/39/73, UPM/adaptaciónSommerville, curso22-23. **Información de Internet:** [RFC2119](https://www.rfc-editor.org/rfc/rfc2119.txt), S.Bradner, marzo1997; captura nueva del predecesor,4723bytes/unGET. NASA SEH209, [original archivado](https://www.nasa.gov/wp-content/uploads/2018/09/nasa_systems_engineering_handbook_0.pdf), NASA/SP-2016-6105Rev2; no se descargó de nuevo. Autoría, edición, hashes y fragmentos están en los recibos y `source-provenance.json`. No se dedujo validez de HTTP/dominio.

Para repetir diagnóstico, usar una carpeta NUEVA bajo `docs/audits/`, copiar `run_successor.py`, `cases.json`, `criteria.json`, `protocol.json` y `frozen-sha256.json`, y ejecutar desde el workspace:

```powershell
.venv/Scripts/python.exe <carpeta-nueva>/run_successor.py
```

Necesita los snapshots locales registrados y el transporte CPU del predecesor que importa el script. El proceso rechaza sobrescribir el reloj. Consumirá un presupuesto nuevo explícito; no se ejecuta por abrir este informe. Las fases de desarrollo adicionales son scripts separados y conservan el reloj de su carpeta, no deben lanzarse como una manera de reiniciar cuota. Repetir estos casos ya expuestos no acreditará generalización.

El ensayo mínimo ya está ejecutado, no solo propuesto: cuatro borradores, crítica automática, dos intentos de corrección que no cambiaron nada y un parche14B incompleto. Faltan dos cosas precisas: **obtener objeciones correctas sin nuestra intervención y completar una corrección útil dentro del presupuesto**, para después medir la post-revisión y una muestra nueva. No se concluye queGPU arreglaría el significado; solo que el parcheCPU concreto no terminó en180s. No se inicia otro modelo/campaña ni GPU sin la autorización correspondiente.

## Integridad y SpecKit

Pasan **137pruebas Python**, incluidas nueve nuevas del orquestador: conservación, fuente docente testigo, ejeexterno sustentado con conflicto, reintento limitado, dos correcciones, repetición, cancelación, retirada, presupuesto y plazos. Son controles de implementación; las afirmaciones sustantivas anteriores provienen del ensayo real y su revisión externa. Black correcto y Ruff sin nuevos diagnósticos frente al baseline estructural con multiplicidad. UI no cambió; no se atribuye un navegador nuevo a esta fase.

Se preservan originales, reservas y expedientes de ensayo anteriores. Sin SQL/migraciones, commits, Reset, perfiles habituales, índices nuevos o procesos ajenos detenidos. Los procesos propios terminaron; no queda servicio propio. Ver `final-checks.json`.

Spec/plan/tasks conservan su historia y añaden el resultado. T159/T160 registran orquestación técnica y medición del experimento, **no** validación de contraste web. Analyze/converge mantienen los pendientes semánticos, de integración real y de muestra nueva; T116–T118/T151–T153 y los gates históricos siguen abiertos. Feature012 no se cierra ni se atribuye aceptación docente, eficacia humana, calificación o capacidad al alumno.
