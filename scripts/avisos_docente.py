"""Revisión docente del registro de avisos por línea de comandos (hay también una página: ver docs/ESTUDIO.md).

    python scripts/avisos_docente.py pendientes            # avisos sin evaluar
    python scripts/avisos_docente.py ver <id>              # un aviso completo
    python scripts/avisos_docente.py marcar <id> acierto|falsa_alarma|dudoso [nota]
    python scripts/avisos_docente.py resumen               # recuento por veredicto y tipo de aviso
    python scripts/avisos_docente.py purgar <dias>|todo    # borra avisos y etiquetas con más de N días (o todo); ver docs/PROTECCION-DATOS.md

acierto = el aviso estaba justificado; falsa_alarma = la respuesta era correcta; dudoso = no se puede decir.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from oralia.documentary import notice_review as review  # noqa: E402


def mostrar(e, completo=False):
    print(f"[{e['id']}] {e['at']}  avisos: {', '.join(e['notice_kinds'])}")
    print(f"  Pregunta: {e['question']}")
    if completo:
        print(f"  Respuesta:\n{e['answer']}\n  Fuentes: {', '.join(e['sources'])}")
        for f in e["reviewer_findings"]:
            print(f"  Revisor ({f['kind']}, {f['use_id']}): {f['reason']}\n    Unidad: {f['unit_text'][:400]}")
        if e["mark"]:
            print(f"  Marca: {e['mark']['veredicto']} {e['mark']['nota']}")


def main(argv):
    orden = argv[0] if argv else "pendientes"
    avisos = review.notices()
    if orden == "pendientes":
        pendientes = [a for a in avisos if not a["mark"]]
        for a in pendientes:
            mostrar(a)
        print(f"{len(pendientes)} pendientes de {len(avisos)}")
    elif orden == "ver" and len(argv) == 2:
        for a in avisos:
            if a["id"] == argv[1]:
                mostrar(a, completo=True)
    elif orden == "marcar" and len(argv) >= 3 and argv[2] in review.VERDICTS:
        try:
            review.mark(argv[1], argv[2], " ".join(argv[3:]))
        except KeyError:
            sys.exit("id desconocido")
        print("anotado")
    elif orden == "resumen":
        r = review.summary()
        print(f"avisos: {r['total']}  evaluados: {r['evaluados']}  {r['por_veredicto']}")
        for fila in r["por_tipo"]:
            print(f"  {fila['tipo']:14} {fila['veredicto']:13} {fila['n']}")
    elif orden == "purgar" and len(argv) == 2 and (argv[1] == "todo" or argv[1].isdigit()):
        r = review.summary()
        print(f"antes: avisos {r['total']}, evaluados {r['evaluados']}  {r['por_veredicto']}  (copia estas cifras si las quieres conservar)")
        print(f"borrados: {review.purge(0 if argv[1] == 'todo' else int(argv[1]))}")
    else:
        print(__doc__)


main(sys.argv[1:])
