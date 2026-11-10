# Prueba docente breve de recuperación v2.1

Desde `D:\Proyecto personal\ORALIA`, con un puerto propio libre (ejemplo8029):

```powershell
.venv\Scripts\python.exe -X utf8 -m oralia.documentary --package v2 --retrieval --port 8029 --no-browser
```

Abra [Materiales locales](http://127.0.0.1:8029/tecnica?documental=1) y pulse «Entrar en consulta documental». La raíz fija es `materiales/docente/piloto-requisitos/recuperacion-v2.1`; no use `--build --measure` para probar la interfaz: ese banco ya está expuesto y el runner rechaza repetirlo.

1. Escriba «¿Qué medidas permiten expresar rendimiento y portabilidad?» y pulse «Recuperar pasajes». En esta entrega aparece Requisitos22 (tabla Property/Measure) entre otros resultados; abra su original y contraste la página. Las filas del resultado mantienen texto/encabezado, no una respuesta redactada.
2. Pruebe una pregunta propia de otro subtema. Puede escribir un referente visible para un seguimiento y marcar «Cambio de tema» para descartarlo. Esa casilla es explícita; no existe resolución generativa de pronombres.
3. «Cerrar consulta» retira resultados y permiso. Al volver a entrar los campos quedan vacíos. Ctrl+C detiene exclusivamente el servidor que acaba de iniciar.

Límites ya conocidos: el baseline léxico falla preguntas naturales como «¿Qué es un requisito?» y «¿Qué tipos de requisitos hay?» en español; no necesita descubrir esos fallos. Denso y RRF recuperan mejores candidatos en media, pero ambos pierden la tabla22 en el contexto final de su control, por lo que no se adoptaron. Preguntar por Kubernetes o una prescripción INCOSE puede devolver pasajes poco pertinentes: **no se ha establecido suficiencia para responder** y no habrá respuesta generada. Los scores no expresan verdad ni exclusión del temario. Esto sirve para inspeccionar fuentes, no para afirmar que el tutor ya conversa correctamente.

Para volver a la consulta documental anterior, cierre su servidor y ejecute:

```powershell
.venv\Scripts\python.exe -m oralia.documentary --port 8031 --no-browser
```

v1.1 sigue por defecto. Para documental v2 sin recuperación añada `--package v2`, sin `--retrieval`. El launcher existente también conserva `scripts/demo.ps1 -Documentary` y su selector de paquete. No pare ni reutilice un servidor ajeno en8022. En el sandbox de esta tarea el arranque sin modelos necesitó ejecución local autorizada porque asyncio quedó bloqueado creando socketpair; fuera del sandbox se comprobó correctamente.

La [entrega](report.md) contiene métricas, negativos, hashes y lo que falta antes de conectar un generador. No se pide aceptación académica ni validación de defectos ya conocidos.
