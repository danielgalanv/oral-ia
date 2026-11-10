# Riesgos y complicaciones previstas

Diseño preventivo; riesgo no equivale a incidencia nueva comprobada.

| ID | Riesgo / evidencia | Mitigación y prueba | Bloqueo |
|---|---|---|---|
| R01 | Confundir tests técnicos con valor; falló el diálogo real | G0/G1 separados; corpus completo y reservado, T045–T047 | no declarar listo sin G1 |
| R02 | Reglas ajustadas a agua/frases conocidas | segundo dominio, variantes y holdout renovado tras exposición | G1 |
| R03 | Memoria sustituida por última orden | contexto tipado y referente inequívoco; negativos A04–A06 | G1 |
| R04 | Exención repetir evita verificadores | exención solo coherencia por repetición intencional; revalidar todas las fuentes | G0 |
| R05 | Fluidez libre no autorizada por binder actual | renderer controlado; G2 independiente; ningún hash autoriza texto | G0/G2 |
| R06 | Pistas/fuentes revelan respuesta | matriz de todas las superficies y política docente | G0 |
| R07 | 99/100 tratado como error absoluto | unidades/condiciones/atribución explícita sin nota | G1 |
| R08 | Ejemplo revisado pierde alcance al reutilizarse | unidades versionadas, prerequisitos, destinatario y evidencia revalidados | G0 |
| R09 | Contexto crea retención oculta | scopes, purga, exportación, expiración y referencias acotadas | G0 |
| R10 | Recuperar sesión permite apropiación | autorización existente; código no autentica; cierre admin confirmado | G0 |
| R11 | Reconexión duplica turno o salida tardía revive datos | recibo atómico, reconciliación, versión de estado y cierre ganador | G0 |
| R12 | Controles consumen recursos sin límite | mismos presupuestos T090/T150; recuperación acotada | G0 |
| R13 | Máquina del agente oculta dependencias | PowerShell normal, offline, PATH temporal y modelos ausentes | G0 |
| R14 | Migraciones o edición reescriben evidencia | aditivas, snapshots legacy, rollback respaldado, hashes paquetes previos | G0 |
| R15 | Reserva extractiva se presenta como LLM | proveedor efectivo visible y evidencia por perfil | G1/G2 |
| R16 | Corpus reservado contaminado por ajuste | primera ejecución publicada, casos expuestos a regresión y reserva nueva | G1 |
| R17 | UX textual aparenta voz averiada | modalidad explícita y campo/fuentes accesibles; voz futura separada | G1 |
| R18 | Mayor contenido aumenta revisión docente | paquetes pequeños versionados y editables; medir esfuerzo de autoría en piloto | G3 |
| R19 | Texto generado plausiblemente incorrecto supera coincidencia léxica | no usar similitud como autorización; estudio G2 puede concluir no viable | G2 |
| R20 | Nuevos modelos/versiones degradan calidad o latencia | ejecutar aceptación por versión y recursos antes de habilitar | G2 |
| R21 | Exportar logs reales expone conversaciones | corpus sintético mínimo, sin IDs personales; consentimiento separado | G0 |

## Evolución posterior sin ampliar esta implementación

Después de G1: piloto consentido pequeño con protocolo docente, observación de si la orientación ayuda, registro de confusiones y esfuerzo de preparar material. No medir al participante ni inferir capacidad.

Después, si hay necesidad y viabilidad demostrada: generación local con verificación suficiente; voz con disponibilidad, permisos, transcripción revisable y matriz de fallos; más dominios con revisión. Accesibilidad de audio nunca sustituye texto funcional. Nube/SSO/concurrencia requieren feature y revisión constitucional propias; no se introducen como reparación rápida.


R22 — Una conversación sintética puede parecer correcta mientras llama una operación indebida o simula éxito. Mitigación: oráculos de operación/argumentos/estado y respuesta, negativos del runner T058, observación de servicios reales, roles y datos aislados; bloqueo G0/G1.
