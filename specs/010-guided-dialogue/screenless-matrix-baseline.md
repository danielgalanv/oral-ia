# Matriz de equivalencia sin pantalla — baseline

Auditoría técnica IA de24 conversaciones actuales; no es aprobación humana ni audio real. Los textos y fallos anteriores permanecen intactos. Los pasos se refieren al JSON original y no se sustituyen por selectores visuales.

| Caso | Pasos con navegación incompleta | Correcciones transversales pendientes |
|---|---|---|
| D01 | 0:orientation, 1:clarify | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D02 | 5:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D03 | 3:limited, 4:recovery | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D04 | 1:limited, 5:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D05 | 2:clarify | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D06 | 0:orientation, 1:clarify, 5:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D07 | 7:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D08 | 5:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D09 | 1:confirm_topic, 2:limited, 5:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D10 | 7:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D11 | 1:confirm_topic, 2:limited, 4:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| D12 | 2:confirm_topic, 6:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H01 | 0:orientation | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H02 | Sin aviso de navegación en este fragmento; recorrido esencial no completo | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H03 | 6:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H04 | 4:limited, 7:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H05 | Sin aviso de navegación en este fragmento; recorrido esencial no completo | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H06 | 3:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H07 | 7:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H08 | 1:confirm_topic, 6:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H09 | 1:confirm_topic, 6:limited | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H10 | 5:limited, 7:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H11 | 1:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |
| W-H12 | 6:limited, 7:confirm_topic | fuente, consentimiento/cierre, revisión/borrado por conversación; humano No evaluado |

| Acción | Equivalente conversacional requerido | Evidencia baseline |
|---|---|---|
| Tema/opciones | Enunciar hasta3, más/repetir opciones, elijo/confirmo | Listas solo en metadatos/UI no bastan |
| Ayuda/repetición/reformulación | Pedido verbal sobre objetivo/pregunta vigente | Control de contenido ya existente; referencias y límites requieren navegación verbal |
| Fuentes | Identificar material/sección legibles y ampliar a petición | Panel de fuentes no satisface petición hablada |
| Modos | Enumerar modos habilitados y cómo elegirlos | Selector visual insuficiente |
| Conservación/cierre | Alcance/plazo y confirmación inequívoca, cancelar | Checkboxes y botón no equivalentes a diálogo |
| Revisión/borrado | Comando propio con scope/caducidad/confirmación | Operaciones API existen, falta recorrido conversacional |
| Interrupciones/silencios/STT/TTS | Gate G4 con audio local real | No validado; no inferirlo de texto |
