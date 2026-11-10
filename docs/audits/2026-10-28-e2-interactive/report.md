# E2: cableado optativo preparado; prueba real bloqueada por capacidad GPU

28-10-2026. Se incorporó la adjudicación proporcionada: structured-prompts/new
sobre «buscar» es aceptable con mejora opcional. Se retira su rechazo semántico
como bloqueo de E2; no se reparó otra vez ni se reescribieron recibos históricos.

Implementación: `real_study_provider.py` une el lifespan docente a cached_provider,
OwnedWorkerTree y renderer structured Qwen2.5-14B NF4 registrado/greedy.
`__main__.py --real-provider` es opt-in, incompatible con fixture y exige directorio
técnico exclusivo. `study_lab_api.py` comparte presupuesto real de seis llamadas;
TrialBudget conserva defaults históricos y admite el plazo explícito. Proveedor
bound revalida permiso/fuentes antes/después y conserva frame efectivo temporal.
768tokens/50s/4000caracteres y UI histórica intactos: NO se simulan2048/180s.
Cookie/origin/consent/lease15s/cancelación/cierre existentes siguen vigentes.
El lifespan tiene plazo finito; no se deja un modelo indefinido.

Pruebas CPU de fuente/permiso/historial mostrado/cancelación/tardíos/retirada/
idempotencia originales más binding real→structured y bloqueo por retirada:
[tests-final.log](tests-final.log). Son pruebas técnicas con dobles, NO contenido
real de modelo. Sin cambios de defaults, UI, índices, corpus o participantes.

Intento REAL de arranque en8027, con RAG denso de corpusv2 e índice build=False.
La interfaz se abrió mediante navegador integrado hacia la URL real, pero recibió
ERR_CONNECTION_RESET porque el lifespan rechazó cargar antes de iniciar HTTP.
[Consola íntegra](server-001.log), [capacidad medida](runtime-001/gpu-before.json).
GPU actual21060/32607MiB asignados,0%uso: quedan11547MiB, por debajo de la
estimación mínima NF4 del worker para estos shards (~14GB). Memoria reservada
no demuestra actividad ajena, pero sí falta holgura para esta carga. No se
provocó OOM, no se detuvo ComfyUI/otros procesos ni se cambió de modelo.

Cero cargas de pesos/calentamientos/peticiones académicas. No hay primera
pregunta/respuesta mostrada ni transcripción de contenido. No se ejecutaron
seguimiento, ejemplo o cancelación real; no presentar fixture/offline como
navegación real. Servidor propio terminó;8027 sin listener al comprobar cierre.

Reloj original:17:46:05 Europe/Madrid,45min hasta18:31:05; se preservó incluso
al llegar «Continúa» y no se reinició. Parte sustancial transcurrió antes del
seguimiento operativo. No se extiende el plazo para un arranque sin memoria.
Primer intento y GPU se conservan intactos; no procesos GPU propios iniciados.

Comando de reinicio preparado (requiere GPU con capacidad libre; arranque real
NO acreditado como correcto): desde D:\Proyecto personal\ORALIA,

```powershell
.venv\Scripts\python.exe -m oralia.documentary --package v2 --retrieval --study-lab --real-provider --runtime-output docs/audits/2026-10-28-e2-interactive/runtime-002 --runtime-seconds 900 --port 8027 --no-browser
```

Directorio nuevo obligatorio cada vez;15min finitos/seis llamadas máximo. Abrir
http://127.0.0.1:8027/tecnica?documental=1 solo tras startup completo, entrar como
docente y consentir inspección temporal. Desde móvil/chat el coordinador puede
manejar esa misma interfaz y compartir texto; no se abre LAN. No se afirma que
este comando esté probado de extremo a extremo: el primer arranque equivalente
fue rechazado por capacidad. No mantener servidor/modelo preparado a escondidas.

Estado: cableado implementado y CPU verificado; navegador/modelo real NO
verificados juntos, NO disponible como E2 operativo ni probado por el usuario.
T103 continúa pendiente; Feature012/G2/SC001/T090/T150/participante sin apertura.
`unverified/not_assessed`, publicationfalse/participantnull. No revisión humana
obligatoria por turno ni supported ficticio. Siguiente paso concreto: disponer
de holgura GPU y ejecutar ese arranque y guion de cuatro preguntas en navegador;
no otra comparación de prompts, auditoría general o fase automática.

## Recuperación posterior con autorización humana

El usuario autorizó liberar la GPU y usarla. El estado bloqueado anterior se
conserva como historia; el resultado posterior está en
[recovery-002/report.md](recovery-002/report.md). Se verificaron en navegador real
las cuatro preguntas, fuentes, cancelación, cierre/reentrada vacía y respuesta
tras recarga. Seis llamadas en total, cinco candidatas completas, ninguna salida
de participante. La transcripción móvil está en
[recovery-002/transcript-mobile.md](recovery-002/transcript-mobile.md).
Modelo y servidor detenidos; GPU final1963/32607MiB,0%.46pruebas CPU, build web
y Ruff correctos. La ejecución técnica E2 ya existe; aceptación del usuario
pendiente. La corrección final de caducidad se probó en CPU sin repetir GPU.
