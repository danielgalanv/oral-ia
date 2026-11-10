# Quickstart007

Desde D:\Proyecto personal\ORALIA con dependencias/embeddings preparados:

```powershell
.\scripts\demo.ps1 -Action Check
.\scripts\demo.ps1
# Otra terminal para parada:
.\scripts\demo.ps1 -Action Stop
.\scripts\demo.ps1 -Action Reset
```

Primera preparación no descarga modelos. Si falta embedding: `-TextOnly` ofrece texto
sin fuentes, con aviso; no equivale al guion con recuperación. Credencial oculta elegida
por presentador, mínimo24 caracteres, no guardada. Código ficticio del guion: demo-007.
Puertos ocupados: liberar voluntariamente o elegir ambos puertos explícitos; no matar
procesos por nombre/puerto. Solo una sesión interactiva activa, cerrar antes de cambiar modo.

Guion de10min: portada/login(1), curso/material/actividad(2), abrir autoestudio sin copiar
ID(1), consulta/fuentes y elegir transcript+summary(2), cierre y revisión/exportación(2),
borrado verificado(1), alternativa efímera y límites(1). Detalle en docs/DEMO.md.
Resultados medidos y archivos en implementation-evidence.md al ejecutar; no se presupone éxito.
