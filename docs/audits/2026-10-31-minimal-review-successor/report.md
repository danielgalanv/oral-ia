# Contrato de decisión única: mejora parcial, sin promoción

## Resultado

La variante optativa web-review/v7 obtiene **cuatro salidas completas y formalmente
válidas; tres revisiones adecuadas de cuatro**. Acepta los dos ejemplos ficticios
coherentes y detecta el error de trazabilidad. Sigue dando un permiso falso a la
atribución de 3:1 para texto normal. No supera la selección preregistrada; no se
inicia transferencia nueva, reparación real ni publicación. T175/T180 siguen abiertas.

[Pregunta, respuesta, revisión y fuentes completas](transcript-full.md).

## Qué cambió

El modelo decide solo status/issues. El host deriva reparación si hay incidencias,
explicación si no encuentra objeciones y límite si declara insuficiencia. Esa
operación versionada no repara salidas erróneas ni cambia el status o las objeciones.
Respaldo externo y compatibilidad docente quedan explícitamente unknown; no se
infiere ninguno del hecho de que el modelo no encuentre errores.

Se conserva íntegro el criterio de tolerancia v3, el mismo para docente e Internet.
Se pide distinguir propuesta hipotética, atribución académica y conclusión con
premisas; distinguir también postura del borrador de postura del profesor y aplicar
mínimos/excepciones bajo sus condiciones. No se introducen el número esperado ni
las objeciones del coordinador. Las referencias siguen siendo source_id y el host
presenta documento/página o URL, sin citas literales.

Se mantienen v1–v6 y el default v1. El cambio es optativo y de laboratorio. No hay
nuevo evaluador semántico independiente ni clasificación acreditada de todos los
conflictos docente/web. Suprimir dos etiquetas no demuestra esos juicios; evita
pretender haberlos emitido.

## Ensayo

Qwen3-8B NF4 no pensante, mismo sampler registrado y seed42 que su ensayo anterior;
cuatro llamadas, máximo 768 tokens/180 segundos cada una y 1200 segundos totales.
Código, entradas y oráculo separados se congelaron antes de inferir. Todas las
llamadas terminaron; 48,859 segundos totales del runner. No hubo reparaciones de
formato, reintentos ni cambios durante la ejecución. Los casos son conocidos y
expuestos, no una reserva inédita.

| Caso | V6 con el mismo checkpoint | V7 |
|---|---|---|
| D03, ficción de trazabilidad válida | Acepta | Acepta |
| D04, atribución errónea solo hacia padre | Detecta parte, confunde profesor/borrador y contrato inválido | Detecta el defecto con referencia pertinente |
| D05, umbral hipotético válido más exigente | Rechaza falsamente | Acepta |
| D06, falsa atribución de 3:1 a texto normal | Acepta falsamente | Acepta falsamente |

Contrato: 2/4 a 4/4. Revisiones enteras utilizables: 1/4 a 3/4 en estos casos. Se
cambiaron esquema e instrucciones conjuntamente, por lo que no se atribuye la mejora
a una sola de esas causas. Una única pasada con muestreo tampoco acredita estabilidad.
El permiso falso restante es material: no lo suavizamos por tratarse de Internet ni
lo excusamos como ficción, pues el borrador atribuye el umbral a W3C y declara cumplirlo.

## Pruebas y conservación

18 pruebas nuevas pasaron antes de inferir; después se añadió una prueba del bucle
revisión/reparación/revisión, con cuatro llamadas simuladas, revalidación, referencias,
semántica desconocida y participante vacío. Las 19 focales pasan. La primera fixture
entregaba borrador a generate y fue rechazada correctamente: se corrigió la fixture,
no la protección de generación limpia. La copia del test congelada antes de inferir
contiene 18 pruebas; el test final contiene 19 y se conserva por separado.

La regresión del módulo suma **562 pruebas aprobadas** (antes de añadir la última prueba del bucle); las **19 focales finales** también pasan y se solapan con aquella suite. Black deja nueve archivos conformes. Ruff en src/tests/scripts conserva diez hallazgos previos y cero nuevos, comprobando multiplicidad. No se suman ambas suites como si fueran independientes. Los originales,
fuentes y reservas se conservan. Se detuvo el árbol GPU propio; modelos ajenos sin
cambios, sin descargas, Reset ni commits. El contexto residente ajeno impide usar los
tiempos como comparativa de rendimiento; no prueba que causara el falso permiso.

## Cierre del incremento

T181 completa implementación y medición, sin acreditar al revisor. Esta hipótesis
se detiene aquí según el protocolo, en lugar de reajustarla sobre D06 y presentar
ese mismo control como transferencia. El siguiente problema es de contraste de
condiciones y atribuciones, no de citas ni redundancia JSON. El objetivo de revisión
académica fiable y transferencia nueva continúa en T168/T169/T175; Feature012 no
converge. No se afirma que hayan desaparecido todas las mejoras posibles.


La comprobación final conserva los 308/140/22 hashes de referencia, las 50/51 copias
congeladas de ambos ensayos y los PID ajenos 40320/17672. GPU observada al finalizar:
0 % de utilización, 20.972 MiB ocupados y 11.216 MiB libres; esa memoria incluye los
modelos ajenos conservados. Los tres árboles propios de ambos incrementos constan
como detenidos. El falso permiso de un control externo no revoca por sí solo las
experiencias locales de chat previamente probadas ni acredita incapacidad universal.
