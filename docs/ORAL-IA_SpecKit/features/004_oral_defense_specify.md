# Feature 004 — Agencia de defensa oral y voz opcional

Añade a ORAL-IA un simulador de defensa oral construido sobre los mismos agentes, contratos, estado, materiales y verificadores utilizados por la agencia de autoestudio. La voz es una modalidad opcional de entrada y salida; todas las funciones esenciales deben estar disponibles por texto.

## Propósito

Permitir que un estudiante ensaye una exposición o defensa mediante preguntas iniciales y repreguntas relacionadas, revise la transcripción y obtenga un resumen descriptivo, sin recibir calificación ni evaluación automática.

## Configuración de la actividad

El profesor debe poder definir bloque de preguntas, temas, materiales autorizados, dificultad orientativa, número máximo de turnos, duración, idioma, entrada por texto o voz, salida por texto o voz, conocimiento general permitido, conservación de transcripción y agentes obligatorios u opcionales.

## Flujo de sesión

1. Mostrar propósito, limitaciones, tratamiento de audio y política de conservación.
2. Seleccionar actividad y pregunta inicial autorizada o generada desde los materiales.
3. Presentar la pregunta por texto y, si está activo, por síntesis de voz.
4. Recibir respuesta por texto o capturar audio.
5. Transcribir localmente y mostrar el texto al participante.
6. Permitir corregir segmentos dudosos antes de utilizarlos para el siguiente turno.
7. Conservar tanto la versión original de la transcripción como la corrección, sin conservar el audio por defecto.
8. Analizar conceptos mencionados como observaciones e hipótesis, no como evaluación.
9. Recuperar materiales relacionados.
10. Proponer una repregunta que pida justificación, ejemplo, comparación, decisión técnica, explicación de error o profundización.
11. Verificar alcance, coherencia y reglas constitucionales.
12. Decidir si profundizar, cambiar de tema, pedir aclaración o finalizar.
13. Repetir hasta el límite configurado o finalización voluntaria.
14. Permitir revisión final de la transcripción.
15. Generar un resumen descriptivo y aplicar la política de conservación.

## Agente de transcripción

Debe producir texto, marcas temporales cuando estén disponibles, confianza estimada y segmentos dudosos. Los errores o baja confianza deben ser visibles. El audio debe descartarse después de procesarse, salvo configuración excepcional expresamente fuera del MVP ordinario.

Si la transcripción falla o los recursos no son suficientes, el sistema debe ofrecer continuar por texto sin perder el estado de la sesión.

## Agente de síntesis de voz

Debe reproducir exactamente el contenido textual ya aprobado. No puede resumir, añadir, suavizar ni modificar la salida. Si falla, la respuesta textual sigue disponible.

## Agente de repreguntas

Debe basarse en la respuesta del participante, el objetivo, los conceptos tratados, los materiales y el historial. Debe evitar preguntas irrelevantes, repetidas, no fundamentadas o que impliquen una calificación encubierta.

## Escenarios prioritarios

### Escenario A — Defensa textual completa

El estudiante realiza una sesión completa solo por texto, recibe preguntas y repreguntas, revisa la transcripción textual y obtiene un resumen descriptivo.

### Escenario B — Defensa por voz

El estudiante activa voz, responde oralmente, revisa y corrige segmentos dudosos, y la versión corregida se utiliza en la siguiente repregunta. El audio es descartado.

### Escenario C — Fallo de transcripción

La captura o transcripción falla. El sistema informa con claridad, conserva el estado, cambia a texto y permite continuar.

### Escenario D — Respuesta ambigua

La respuesta transcrita es incompleta o tiene baja confianza en un término crítico. El sistema solicita confirmación o aclaración antes de generar una repregunta basada en una interpretación incierta.

### Escenario E — Intento de evaluación

Una propuesta contiene una nota, una clasificación de desempeño o una afirmación de que el estudiante ha aprobado. El control constitucional la bloquea y la sustituye por una formulación descriptiva permitida.

### Escenario F — Cierre y consentimiento

Al terminar, el estudiante revisa el texto y decide conservar o eliminar la sesión conforme a la configuración. El sistema ejecuta la decisión y registra únicamente lo permitido.

## Accesibilidad

La sesión debe controlarse mediante teclado, poder pausarse, repetir preguntas, ajustar el ritmo y mostrar mensajes claros. La interfaz no debe depender del audio, del color o de gestos no accesibles.

## Fuera de alcance

- análisis de prosodia, emociones o lenguaje corporal;
- evaluación automática de la calidad de la defensa;
- detección de fraude;
- audio almacenado por defecto;
- robot o avatar físico;
- videoconferencia;
- perfiles longitudinales.

## Criterios de éxito

- El mismo núcleo y agentes básicos soportan autoestudio y defensa oral sin duplicación arquitectónica.
- La modalidad textual cubre todo el flujo.
- La corrección de transcripción queda versionada y se usa en turnos posteriores.
- Un fallo de voz degrada a texto sin perder la sesión.
- Las repreguntas se relacionan con la respuesta y con materiales autorizados en el conjunto de pruebas.
- No se producen notas, decisiones académicas ni inferencias permanentes de nivel.
