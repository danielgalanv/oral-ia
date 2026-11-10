"""Does the retrieved material hold what the student asked? One word from the reviewer (24B), used for a soft notice.

Two one-word judgements, NO if either says so (probe_cobertura2.py, 11 questions the material does not develop and the
teacher's 59 valid ones): 8 of 11 detected, 4 of 59 valid flagged. It never rejects: it only adds a fixed notice.
"""

MIN_WORDS = 6  # "ponme otro ejemplo" or "¿y eso?" carry their topic in the history, not in the words
PROMPT = (
    "Eres un revisor estricto de cobertura. Recibes una pregunta de un alumno y unos pasajes del material de la "
    "asignatura. Decide si los pasajes contienen la información ESPECÍFICA que pide la pregunta. "
    "SI: los pasajes desarrollan lo que se pregunta (aunque sea con otras palabras o a modo de principios generales). "
    "PARCIAL: tratan el tema general y permiten una respuesta útil pero no el detalle exacto pedido. "
    "NO: los pasajes solo mencionan de pasada la herramienta, técnica o método preguntado, o tratan otro tema, y "
    "responder exigiría conocimiento que no está en ellos. Responde con una sola palabra: SI, PARCIAL o NO."
)


PROMPT_CENTRAL = (
    "Recibes una pregunta de un alumno y unos pasajes del material. Contesta SOLO con una palabra. "
    "Primero identifica el elemento central que la pregunta quiere conocer (concepto, técnica, herramienta, norma, modelo "
    "o método). ¿Lo desarrollan los pasajes (lo definen, lo explican o dan pautas sobre él)? "
    "Responde DESARROLLA si lo desarrollan o si es un concepto general de requisitos que los pasajes tratan; "
    "responde AUSENTE si el elemento central es una herramienta, técnica, norma o modelo concreto que los pasajes no "
    "describen (aunque tratan temas cercanos o lo nombran de pasada)."
)


def worth_checking(question):
    return len(question.split()) >= MIN_WORDS


def messages(question, texts, prompt=PROMPT):
    context = "\n\n".join(f"[{i + 1}] {text[:1500]}" for i, text in enumerate(texts))
    return [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Pregunta: {question}\n\nPasajes:\n{context}\n\nRespuesta:"},
    ]


def parse(text):
    word = text.strip().upper()
    return "NO" if word.startswith("NO") else "PARCIAL" if word.startswith("PARCIAL") else "SI" if word.startswith("SI") else None


def absent(text):
    return text.strip().upper().startswith("AUSENTE")
