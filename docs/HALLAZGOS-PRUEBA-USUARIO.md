# Hallazgos de la prueba de usuario

## Autoestudio — 18 de octubre de 2026

Estado: pendiente. Registrar y esperar la prueba de defensa oral antes de agrupar
el trabajo correctivo. No iniciar cambios por este registro.

Evidencia: revisión de solo lectura de la sesión demo
`3e3ae9e1-921f-432d-88ec-6874ffb172ee`, siete turnos. No se duplica aquí toda la
transcripción ni se convierte esta observación en una evaluación del participante.

| Entrada observada | Comportamiento | Brecha |
|---|---|---|
| Saludo | Respuesta de información insuficiente | Falta orientación para comenzar |
| Pregunta general pertinente sobre el agua | Información insuficiente | Recuperación/interpretación insuficiente para esa formulación |
| Pregunta precisa de temperatura de ebullición | Dos frases extractivas con evidencia | Responde, pero no desarrolla explicación |
| Preguntas sobre transformación a vapor | Aviso repetido de revisar el hilo | Bucle de recuperación/repetición sin avance |
| Referencia breve al turno anterior | Información insuficiente | Falta resolución contextual de la referencia |

La traza de las preguntas sobre vapor registra grounding `fundamentada` y coherencia
`reformulate`, seguida de plantilla `self-study-incoherence`. El sistema encuentra
evidencia, pero la repetición del resultado extractivo conduce al aviso en vez de a
una ampliación útil. Esto no es prueba de un error o falta de progreso del usuario.

El material de la actividad demo contiene solo dos frases. La generación determinista
extrae texto; los gates técnicos aprobados no acreditan calidad conversacional ni
utilidad educativa. La afirmación previa de estar lista debe entenderse limitada a
los recorridos funcionales verificados, no como validación de un tutor útil.

Trabajo a valorar después de la prueba de defensa:

1. Orientación inicial y respuesta a preguntas generales dentro del tema autorizado.
2. Continuidad contextual para referencias breves al turno anterior.
3. Diferenciar repetición improductiva de ampliación legítima de un tema y ofrecer
   una salida útil, sin rebajar autorización ni verificadores.
4. Material docente suficientemente desarrollado y estrategia de generación que
   permita explicar y profundizar; no disimular las limitaciones extractivas.
5. Aceptación basada en diálogos completos y variadas formulaciones, incluyendo
   bucles y recuperación, además de pruebas de mecanismos técnicos.

## Defensa oral

Revisión de solo lectura del 18 de octubre de 2026, sesión
`fa16861a-1680-48c1-b45c-95763f8df3f1`, seis turnos. Sin cambios de comportamiento.

Pregunta inicial: temperatura de ebullición. Ante una respuesta de 99 grados, el
sistema pregunta cómo justificar una afirmación de 100 grados y añade el paso a vapor:
no explicita la discrepancia entre respuesta y material y mezcla dos asuntos.
Esto no implica evaluar académicamente al participante; la discrepancia factual
podría abordarse con una pregunta neutral respaldada en fuente.

Después de expresar que no sabe justificarlo y pedir continuación, repetición y otra
formulación, devuelve cuatro veces la misma plantilla de información insuficiente.
Las trazas registran evidencia vacía y acknowledge_missing_info; no recupera el tema
de la pregunta previa para esas peticiones conversacionales. La memoria de conceptos
registra tokens como no, puedes y ahora como destinos, señal de extracción superficial,
no de una decisión pedagógica útil. T090 aprueba esas plantillas: el problema observado
es calidad/control del diálogo, no un bloqueo de autorización.

Pendiente: distinguir respuesta temática de solicitudes de repetir, reformular,
recibir orientación o cambiar de pregunta; conservar pregunta/tema para recuperación;
tratar discrepancias factuales sin notas; evitar fallback idéntico indefinido y ofrecer
salida explícita. Añadir aceptación con la secuencia completa observada y variantes,
sin sustituirla por preguntas exactas favorables. Revisar junto a autoestudio antes
de implementar. La defensa actual no demuestra una práctica educativa útil sostenida.
