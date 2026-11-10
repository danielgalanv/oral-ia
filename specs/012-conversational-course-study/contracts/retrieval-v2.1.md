# Contrato de recuperación docente v2.1

Entrada: pregunta no vacía≤2000 caracteres y≤128 tokens con especiales; estrategia cerrada lexical/dense/rrf, referente visible opcional (dos últimas entradas como máximo en laboratorio), cambio explícito descarta referente. Interfaz docente fija baseline léxico tras la comparación negativa.

Precondiciones: paquete v2 técnico local y permiso docente local vigentes, encoder/tokenizer ya instalados con hashes/versiones concretos, CPU explícita, snapshot local-only, índice aislado con identidad coincidente. Este perfil no sustituye autorización SQL de participante.

Salida: candidatos con offsets sobre texto revisado; hasta5 páginas/contextos íntegros≤6000 caracteres, documento/página/sección/procedencia/derivación/original y hashes, omisiones por presupuesto. `sufficiency=not_assessed`: ranking no es verdad, suficiencia o decisión académica. No respuesta generada, notas, rúbrica, perfil del alumno ni publicación participante.

Fallo cerrado ante identidad desconocida/incompatible, unidad ajena, integridad/retirada o cambio antes/después de espera, consulta demasiado larga, permiso revocado durante recuperación. No reindexar datos históricos ni fallback remoto. Recursos ausentes bloquean carga local. Cierre explícito revoca permiso y desmonta resultados visibles; respuesta tardía se ignora. No se conservan consultas de uso ordinario; banco sintético autorizado conserva resultados por separado.

El laboratorio tiene un presupuesto de evaluación de30 consultas por cada una de3 estrategias, una sola pasada. Fuera del banco no hay bucle autónomo ni reintento al generador. CPU sin deadline pedagógico inventado: tiempos medidos en recibos, falta prueba de carga concurrente. Detener el servidor propio es la terminación operativa. T090/T150/G2/SC001 y T077 global conservan sus fronteras.
