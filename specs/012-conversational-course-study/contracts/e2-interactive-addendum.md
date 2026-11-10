# E2: addendum prospectivo28-10-2026

Prevalece la política answer-evaluation-calibration-audit y readjudication:
aceptable con mejoras menores no exige reparación; error material, incertidumbre
y didáctica se registran separados. Se retira structured-prompts/T2 como bloqueo
semántico, sin alterar sus llamadas, parada o evidencia histórica.

Nuevo alcance E2: docente identificado, modelo local real optativo mediante
--real-provider, RAGv2 denso experimental y renderer nativo registrado. Se conserva
768/50s/4000caracteres por coherencia con UI/historial existentes, en lugar de
afirmar ampliación2048/180 no conectada. Plazo45min y seis llamadas previas máximo
desde primerpreflight, cargas/warmups dentro del reloj; no reset mecánico.
Defaults/fixture separados; sin permiso de participante ni revisión positiva ficticia.

Secuencia mínima congelada: definición de requisito; tipos; «No lo entiendo,
explícalo de otra manera»; ejemplo coherente del referente realmente mostrado;
cancelación y cierre/reentrada. Criterio: idea central pertinente, ejemplo
plausible y continuidad razonable; mejoras menores no bloquean. Solo lo mostrado
entra en historia. Consentimiento/lease/auth/retirada/cancelación permanecen.

Resultado actual: preparación y pruebas CPU; arranque real rechazado por GPU
sin holgura (21060/32607MiB asignados). No preguntas/respuestas reales en navegador.
T103/E2 NO completada ni disponible para usuario. Informe/evidencia en
docs/audits/2026-10-28-e2-interactive/. No reescritura de IDs/estados históricos.

## Recuperación autorizada posteriormente por el usuario

«Saca todo de la GPU y úsala tu» autorizó liberar las cargas locales y reanudar
la prueba. La recuperación conserva el intento anterior como historia y fija
un reloj nuevo explícito de900s/seis llamadas, sin renovarlo durante recarga,
reentrada o relevo técnico. Dossier: recovery-002 dentro de la auditoría E2.

Ahora sí se ejecutaron en navegador real las cuatro preguntas consecutivas,
sus fuentes, cancelación durante inferencia, cierre/reentrada vacía, recarga
explícita y una respuesta posterior. Seis llamadas, cinco candidatas completas,
tres cargas técnicas; transcripción móvil y capturas UI disponibles. Evaluación
proporcionada: aceptables con mejoras menores, sin error material bloqueante.
Contenido siempre unverified/not_assessed; participante cerrado.

La caducidad del runtime probado detuvo modelo y servidor, pero emitió
TimeoutError al cerrar el lifespan. Se corrigió el alcance del timeout para que
el watchdog solicite cierre antes del teardown; regresión CPU específica aprobada.
No se repitió GPU tras esa última corrección.46pruebas CPU y build web correctos.
La ejecución técnica de E2 queda acreditada; aceptación personal del usuario y
T103 formal pendientes. No se abren T090/T150/G2/SC001/Feature012.
