# Perfil optativo offline de reparación asistida — 28-10-2026

Autoridad prospectiva: orden humana de iterar generación/revisión del asistente/
corrección local hasta respuesta adecuada o parada real. Este contrato amplía
solo el perfil `repair-expanded/v1`; no reescribe los protocolos históricos ni
la vía de autocrítica descrita en advisory-review-repair.md.

`RepairGenerationRequest`/`RepairGenerationConstraints`: hasta2048tokens nuevos,
180000ms; defaults de este tipo2048/180000. `LabGenerationRequest` conserva
768/50000 y solicitud ordinaria sus límites históricos. El proveedor CUDA debe
optar explícitamente por `repair_profile_enabled=True`. Worker anuncia esa
capacidad, valida budget_profile con el mismo validador puro del host y confirma
el perfil en la respuesta. Ausencia de opt-in, perfil desconocido, valores fuera
de capacidad o alternativas finitas rechazan sin clipping. Formatos finitos
históricos no se amplían.

Tipo de mensaje exclusivo de reparación hasta16000caracteres; GenerationMessage
ordinario sigue4000. Salida/recibo expandido hasta16000caracteres, sin recorte:
worker, adaptador y guard de llamada rechazan exceso. Pipe del proceso admite
262144bytes para serializar UTF8+auditoría sin el techo implícito de64KiB. El
contexto de entrada del worker sigue7000tokens, con rechazo explícito si excede,
nunca truncamiento silencioso. No se confunden tokens con caracteres.

Timeout de transporte deriva del deadline de solicitud (180s+2s de tolerancia
de lectura); guard exterior de call aplica180s exactos o el tiempo global restante,
revalida y rechaza resultados tardíos incluso si el proveedor absorbe cancelación.
Parada/cancelación actúan solo sobre árbol propio. Presupuesto compartido se
reserva antes de cada llamada y no se reinicia por iteración. Reloj global
persistido antes del primer preflight y propagado por cualquier recuperación.

Solo etapas de reparación con crítica del asistente. `generate/process` y
`review_request` rechazan este tipo expandido para impedir usarlo accidentalmente
como autocrítica o workflow histórico de200s. `repair_with_supplied_review` sigue
siendo una sola corrección con revisión externa; bucle acotado offline invoca
call(repair) tras validar cada crítica/candidata e inspecciona cada resultado
antes de otra llamada. Un candidato incompleto puede ser dato de diagnóstico,
marcado como tal, no un texto completo ni historia mostrada ficticia.

La instrucción expandida permite reescribir concisamente y exige IDs reales
internos. El host entrega source_index de procedencia, sin cambiar los textos
fuente, y construye la lista visible de fuentes consultadas. Un ID presente no
demuestra que la afirmación esté respaldada; revisión sustantiva del asistente
por separado. El índice explícito fue una mejora CPU posterior a las tres
llamadas medidas y no se le atribuyen resultados GPU retrospectivos.

El consumidor efectivo de este perfil es el circuito offline autorizado y su
transcripción inerte sin recorte. NO se enruta a DiagnosticStudy.turn ni a la
UI de Materiales: sus768/50s,4000caracteres, historial y lease siguen intactos.
No ampliar esos límites o leases de participante por extender el tipo offline.
Fuentes/candidata/crítica/historial tratados como datos no confiables; escape y
CSP en artefactos, cero ejecución de contenido. No servidor nuevo.

Este caso:30min desde primerpreflight, máximo6correcciones (no obligatorias),
cargas/warmups aparte dentro del mismo reloj. Parar ante evidencia esencial
ausente, dos iteraciones consecutivas sin reducción sustantiva o bloqueo real
de capacidad. No completar length/deadline a mano ni declarar supported por
JSON. Mantener inicial/versiones/críticas/contabilidad históricas intactas.

Estados siempre unverified/not_assessed, publicaciónfalse/participantnull.
No cierre E2/Feature012 ni automatización del juicio del asistente.
