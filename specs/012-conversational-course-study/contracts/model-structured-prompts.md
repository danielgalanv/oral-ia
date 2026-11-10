# Construcción por checkpoint y tarea — perfil optativo

Autoridad: orden humana28-10-2026 de implementar adaptación estructural y medirla.
No cambia defaults, protocolos históricos, gates o UI de participantes.

`StructuredGenerationRequest` extiende el límite optativo2048tokens/180000ms,
con `model_profile`, `prompt_task` generate/review/repair, pregunta, borrador,
observaciones falibles, obligaciones y evidencia como campos separados. La
solicitud se construye con `structured_request`; el constructor existente
`ReviewRepairGenerationAdapter.repair_request(..., model_profile=...)` lo reutiliza.
El adaptador usa `effective_messages`; el worker reconstruye y valida el frame
contra el MISMO renderer. Ninguna ruta nueva envuelve el JSON como pregunta_actual.

System es instrucción del host específica de tarea: generar; contrastar; o
confirmar observaciones con fuentes y sustituir/eliminar el error, ajustando
dependencias/coherencia y conservando contenido correcto. No dar autoridad a
críticas, no copiar una solución prefabricada ni mantener error y añadir negación.
Salida académica completa sin IDs/bibliografía, cuya procedencia muestra el host.
La tarea review existe para llamadas explícitas, no se invoca como sustituto
de revisión asistente ni se conecta automáticamente a process/autocrítica.

User contiene un objeto JSON completo con campos diferenciados, no una pregunta
escapada dentro de otra envoltura de pregunta. Escapes lossless de caracteres
`< > [ ]` dentro de strings impiden que delimitadores nativos adversarios entren
como tokens especiales de contenido. `json.loads` recupera cada texto exacto;
sin clipping ni eliminación de condiciones. Historial realmente mostrado conserva
roles user/assistant y contenido completo codificado como datos; roles system
inyectados rechazan. JSON no es universalmente mejor que otros formatos: este
contrato se comprueba por mensajes efectivos y tokenización real.

Registro cerrado `model_prompt_profiles.PROFILES`: Qwen2.5 Instruct1.5/7/14B,
Qwen3-8B non-thinking y Mistral Small24B2501. Identidad se liga al path exacto
del snapshot registrado, SHA256 de config.json y model_type, no a model_label.
Combinaciones desconocidas/incompatibles rechazan antes de cargar. Template
se obtiene del tokenizer local del snapshot; no ChatML ni tokens de control
fabricados. No se copia identidad, fechas o restricciones de ejemplos del fabricante.

Qwen2.5 usa roles nativos sin opción thinking. Qwen3 nuevo requiere
enable_thinking=False explícito y sampling registrado non-thinking; greedy de
este perfil nuevo rechaza (la vía histórica greedy sigue intacta). Mistral usa
su plantilla propia y system docente adaptado, con el parche regex local existente
registrado y comprobado en CPU. No se afirma limitación arquitectónica no medida.

Sampling optativo: greedy/v1 para Qwen2.5/Mistral; qwen25-sampling/v1,
qwen3-nonthinking-sampling/v1 y mistral-low-temperature/v1 con parámetros
explícitos/semilla validada. Son perfiles preparados; esta entrega NO mide
muestreo ni Qwen3/Mistral en GPU. Sin perfil registrado, defaults históricos
do_sampleFalse permanecen. La configuración efectiva se conserva por llamada
y el outcome no informa temperature0 para un perfil realmente muestreado.

`native_tokens` comprueba apply_chat_template(tokenize=True) frente a
render→tokenize(add_special_tokens=False), normalizando solo BatchEncoding/list.
La nueva ruta usa false explícito; la histórica queda intacta para reproducción.
CPU: equivalencia en los cinco checkpoints; ruta antigua equivalente en Qwen;
Mistral default actual duplica BOS (2 frente a1), corregido en la nueva ruta.
Esto no explica los errores del ensayo Qwen14. Qwen3 non-thinking es explícito;
thinking no se activa ni se expone con un presupuesto implícito.

Se conservan budgets, input7000tokens con rechazo explícito, output16000caracteres
sin recorte, bytes de pipe, trazas, vigencia de fuentes, consentimiento,
cancelación, cierre y OwnedWorkerTree. Stages de call deben coincidir con la
tarea tipada; no se convierte una revisión JSON o un stop en apoyo semántico.
Estados unverified/not_assessed, publicationfalse/participantnull. Sin cierre
E2/Feature012/G2/SC001 por infraestructura.
