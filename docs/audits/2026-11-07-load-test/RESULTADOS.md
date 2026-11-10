# Prueba de carga del chat de autoestudio (07-11-2026)

`scripts/load_test_chat.py`: N alumnos con sesión propia (entran, mantienen la conexión y preguntan como el navegador). Política web por defecto, GPU compartida con otros procesos del equipo. Un alumno solo tarda ~10 s por respuesta.

| configuración | prueba | respuestas/min | latencia media | p95 | fallos |
|---|---|---|---|---|---|
| 1 hueco (antes), cerrojo global | 10 alumnos a la vez × 2 preguntas | 5,8 | 84 s | 107 s | 0 |
| 4 huecos, sin turnos de GPU | misma | 2,7–6,4 (inestable) | 75–142 s | 136–333 s | 0 |
| 4 huecos + turnos de GPU | misma | 10,1 | 49 s | 72 s | 0 |
| 4 huecos + turnos, caché 16 384 | 10 alumnos, 4 preguntas, pausa 25 s | 7,7 | 46 s | 74 s | 8/40 (caché del 14B agotada) |
| 4 huecos + turnos, caché 24 576 | misma | 6,9 | 55 s | 85 s | 0/40 |
| misma | 10 alumnos, 3 preguntas, pausa 90 s | 3,0 | 60 s (mediana 34 s) | 147 s | 0/30 |

## Qué se encontró
- El cuello de botella no era solo el cerrojo global: dos servidores llama.cpp (14B y 24B) decodificando a la vez en la misma GPU se frenan unas 14 veces entre sí (4 peticiones en paralelo: 350 y 290 tok/s por separado, 25 tok/s cada uno a la vez). Solución: `documentary/gpu_turns.py` hace que se turnen por grupos (generador y controles / revisor): muchas peticiones del mismo grupo a la vez, el otro grupo espera.
- Memoria: con ~32 GB ocupados la GPU pasa a usar memoria del sistema y todo se frena 10–50 veces. Hecho: caché de contexto cuantizada (q8) y unificada entre huecos, `empty_cache` en el servicio de ranking, 4 huecos.
- Caché demasiado pequeña (16 384) falla con 4 turnos a la vez (turnos con error de transporte); con 24 576 en cada servidor, 0 fallos. El proveedor reintenta una vez ante 5xx.
- La ráfaga de la segunda pregunta en la prueba de pausa 90 s tuvo respuestas de 2 min: en esos momentos el 14B procesaba el prompt a 77 tok/s (normal: miles) con mis otros servicios parados, es decir, la GPU estaba ocupada por otro proceso del equipo (no demostrado del todo). Si hay otras cargas de GPU, la capacidad cae a minutos por respuesta.

## Capacidad estimada
Con la GPU dedicada: ~10 respuestas/min como máximo (un alumno solo: 10 s). Diez alumnos preguntando cada 1,5–2 min dan ~5–7 respuestas/min: espera típica de 20–40 s, con picos de 1–1,5 min si coinciden. Dos turnos de 10 alumnos caben, con la GPU sin otros usos durante la clase. No medido: más de 10 alumnos, sesiones largas, ni el efecto del túnel de Cloudflare.

## Prueba final con 4 alumnos (paquete v3, 4 huecos, servidores sanos: revisor 86 tok/s, generador 120 tok/s)
4 alumnos a la vez, 3 turnos cada uno, pausa 5 s: 12/12 respondidos, 0 errores, latencia media 29,2 s (p95 31,4 s, máx. 31,6 s), 6,9 turnos/min.
Con 4 simultáneos cada alumno espera ~30 s por turno (leyendo ya desde ~2 s por streaming). Con 10 no se ha medido: por extrapolación, ~10 turnos/min implica 60-75 s por turno en ráfaga. Recomendación: grupos de 4-5 o turnos.

## Prueba con 10 alumnos a la vez (paquete v3, 4 huecos, GPU libre, servidores 87/120 tok/s)
10 alumnos × 3 preguntas, todos arrancan a la vez, pausa de 5 s: 30/30 respondidas, 0 errores, 9,4 turnos/min; latencia media 49,6 s (p50 48,1; p95 72,9; máx. 73,3). Con streaming el primer texto llega a los pocos segundos. Es el peor caso (10 preguntas en el mismo instante): una clase real, con pausas de lectura, irá mejor. Con 4 a la vez eran ~29 s. Condición: GPU dedicada.
Nota: las pruebas escriben avisos en `registro-avisos/`; se vació (140 entradas de prueba) con `avisos_docente.py purgar todo` antes de usarlo con alumnos.
