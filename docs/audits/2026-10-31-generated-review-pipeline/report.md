# Medición real: generación y revisión, no errores inyectados

## Resultado principal

Se generaron cinco respuestas reales: cuatro sobre requisitos de la asignatura y
un control W3C separado. Qwen2.5-14B NF4 produjo todas; Qwen3-8B NF4 revisó el texto
exacto recibido. Después Qwen2.5-14B revisó las mismas cinco sin recibir mis objeciones.
**Todos emitieron no_issues_found, así que no se activó ninguna corrección.**

El contraste técnico encuentra cuatro respuestas sin error académico material
observado y una con una conclusión excesiva localizada (G04). Las cinco contestan
el núcleo de la pregunta. No se presenta el resto de la explicación G04 como inútil:
la definición y su ejemplo son adecuados; el cierre afirma una garantía injustificada.

[Preguntas y respuestas completas para móvil](transcript-mobile.html) ·
[Transcripción Markdown](transcript-full.md) · [Adjudicación y métricas](technical-adjudication.json).

## Qué mide y qué no

Los borradores negativos de los ensayos anteriores fueron escritos para calibrar
revisores. Sus errores no se pueden contar como errores del generador. Esta medición
no usa esos borradores ni las etiquetas de sus oráculos. G05 reutiliza la pregunta
W3C, pero el generador produce ahora su respuesta: usa correctamente 4,5:1, no 3:1.
Por tanto, el fallo previo no demuestra que el generador inventara ese dato.

El banco actual tiene cinco preguntas dirigidas, con fuentes reales seleccionadas
y congeladas, no recuperación dinámica ni interfaz. No es una tasa representativa
del curso ni una reserva independiente. Los modelos no reciben respuestas docentes
predefinidas, etiquetas esperadas ni críticas del coordinador. La revisión técnica
posterior es explícita, no ciega ni aceptación docente.

## Resultados por respuesta

| Caso | Contenido | Contraste técnico | Revisor 8B / revisión 14B |
|---|---|---|---|
| G01 | Definición y tipos | Adecuado; ejemplo de sistema mejorable, sin penalización por perfeccionismo | Ambos sin objeciones |
| G02 | Rendimiento hipotético <0,3 s | Ejemplo correcto; nombres de herramientas fuera de los pasajes | Ambos sin objeciones |
| G03 | Comprobable frente a realista | Distinción y ejemplo condicional adecuados | Ambos sin objeciones |
| G04 | Trazabilidad bidireccional | Núcleo correcto; garantía final no justificada | Ambos omiten esa conclusión |
| G05 | Control técnico W3C, fuera del bloque docente | Genera correctamente 4,5:1 para texto normal | Ambos sin objeciones |

G04 termina literalmente:

> Esto garantiza que cada parte del diseño cumple con los requisitos originales y que todos los requisitos están respaldados por elementos específicos en el diseño.

Una relación documental rastreable no prueba que el elemento cumpla correctamente
el requisito. Tampoco mostrar una relación demuestra que todo el diseño esté cubierto.
La ficción del ejemplo es admisible; el defecto es convertirla en esa garantía.
Se cuenta una respuesta con una afirmación material excesiva, no toda una respuesta
académicamente falsa ni dos errores por haberla revisado dos modelos.

G02 añade JMeter y LoadRunner sin estar en los pasajes suministrados. Sus usos para
pruebas de carga/rendimiento se comprobaron después con [Apache JMeter](https://jmeter.apache.org/)
y [OpenText](https://www.opentext.com/products/enterprise-performance-engineering).
La mención no se clasifica como falsedad académica, pero sigue siendo una ampliación
factual no trazada por el RAG del ensayo. La verificación posterior no se pasó al
modelo ni demuestra fallback web automático. Ese defecto de procedencia se registra
separado de corrección del contenido.

## Rondas y coste

- Cinco generaciones iniciales completas y cinco revisiones 8B completas: diez llamadas.
- Segunda pasada de las mismas cinco por 14B: cinco llamadas, cero generaciones iniciales nuevas.
- Total: quince invocaciones completas, diez decisiones de revisión, cinco respuestas únicas.
- Cero objeciones automáticas, cero reparaciones, cero errores eliminados por rondas.
- No se acredita eficacia de corrección real: no se ejecutó porque ningún revisor la solicitó.
- Segunda revisión 14B usa el mismo checkpoint que el generador: no es independencia de modelo
  ni equivale a una revisión humana o a dos señales estadísticamente independientes.

El primer arranque de la prueba se conserva con cero llamadas: la muestra inicial
de preparación del revisor coincidió con el calentamiento del generador (36 % y
cuatro muestras posteriores de 0 %). La recuperación exige cinco muestras bajas
y estables en una ventana acotada; preserva todas las observaciones sin relajar
umbrales de utilización/memoria. No fue un error de respuesta ni un deadline de generación.

Tiempos registrados: primer arranque 46,984 s, recuperación generación/revisión
182,766 s, segunda revisión 34,359 s. No se presentan como ranking de modelos.
Los presupuestos están en los protocolos de cada expediente, sin reiniciar los
anteriores ni ocultar intentos. Máximo dos correcciones por caso y un recordatorio
formal; no hubo necesidad de emplearlos. Las respuestas y recibos no se retocaron.

## Cambios de código y pruebas

WebReviewRounds admite perfiles optativos distintos de generador/revisor, capacidades
por etapa y repair_with_generator=True. Defaults, perfiles antiguos y capacidad
máxima 2048 tokens permanecen. En este ensayo se registraron 1536/1024/2048 tokens
y 180 s para generar/revisar/corregir. No se reparte una respuesta entre prompts
artificiales ni se introduce crítica manual antes de medir.

Las pruebas comprueban que la salida exacta del generador llega al revisor y que la
corrección, si existe, vuelve al generador; la segunda revisión recibe esa corrección.
La prueba CPU con dobles acredita ese cableado, no la eficacia semántica de las rondas.

- 91 pruebas focales aprobadas.
- 571 pruebas del módulo aprobadas; un aviso previo de Starlette.
- Black conforme; baseline Ruff y conservación se registran en closeout.json.
- chain-integrity.json comprueba las cinco cadenas reales: sin borrador u objeción
  inicial, misma pregunta/evidencia, salida exacta y confirmación del perfil GPU.

Código activo modificado: src/oralia/course_dialogue/web_review_rounds.py;
pruebas nuevas: tests/course_dialogue/test_generated_review_profiles.py.
SpecKit registra T182. No se cambia política de publicación, contratos históricos,
material docente o datos de sesiones. No hubo Reset ni commits.

## GPU y conservación

Por orden expresa del usuario se descargaron los modelos ComfyUI mediante su API
(cola vacía) y se detuvo el servidor Dolphin identificado. No se borraron modelos,
archivos ni trabajos. La interfaz ComfyUI quedó disponible sin pesos cargados.
Tras las pruebas se cerraron todos los árboles GPU propios. La lectura final fue
0 % y 30.083 MiB libres; los aproximadamente 2,1 GiB restantes corresponden al
entorno gráfico/contextos del sistema, no a nuestros modelos cargados.

## Estado

T182 permanece parcial: están completados el cableado y esta medición de generación/revisión; falta acreditar una reparación real seguida de revisión. No cierra T169/T175/T180 ni acredita
un revisor autónomo fiable. Los controles negativos antiguos conservan su utilidad
como calibración, separados de las respuestas generadas. El pendiente observado ya
es concreto: detectar conclusiones no respaldadas sin rechazar ejemplos coherentes,
y mantener la procedencia de ampliaciones factuales. No se interpreta el permiso
de ambos modelos como prueba de verdad. La funcionalidad de chat local previamente
probada no se invalida por un control aislado, ni se declara aquí validado todo el piloto.
