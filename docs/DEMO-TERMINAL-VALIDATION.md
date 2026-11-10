# Corrección de arranque desde una terminal normal

18 de octubre de 2026. El PATH del agente incluía el runtime Node de Codex; el de
Windows PowerShell del usuario no. Vite estaba instalado. La validación previa del
agente no cubría esa diferencia. Además, Windows PowerShell 5.1 interpretaba el script
UTF-8 sin BOM como otra codificación.

Cambio en scripts/demo.ps1: resolver un Node ya instalado desde PATH o rutas locales
conocidas (incluido el runtime Codex presente), añadirlo únicamente al PATH del proceso
durante la invocación y restaurar PATH en finally. Sin descargas ni instalación ni
modificaciones permanentes del sistema. Guardado UTF-8 con BOM.

Verificación independiente: ejecutar Windows PowerShell 5.1 -NoProfile con PATH
reconstruido exclusivamente desde los valores Machine/User de Windows, sin el PATH
ampliado del agente. Check: exit 0, recursos/esquema válidos. Start -NoBrowser con
credencial ficticia aleatoria solo en entorno: API8010 y web5180 respondieron; Stop
confirmó parada y conservó datos. Mensajes españoles legibles y BOM verificado.

No se alteraron fuentes Python, políticas, datos demo, base habitual ni paquetes
experimentales. Demo detenida tras el ensayo. No se ejecutó de nuevo la suite global.
