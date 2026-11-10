"""One opt-in general teaching instruction; no answers or semantic approvals."""

PEDAGOGICAL_EXTENSION = (
    "Atiende al propósito de la pregunta actual. Ante incomprensión, cambia de estrategia "
    "explicativa: usa otro recorrido, contraste o relación causal sustentada en los pasajes, "
    "sin añadir hechos. Repetir la definición con sinónimos o enumeraciones no basta. "
    "En un ejemplo hipotético, explicita los supuestos ficticios relevantes y mantén coherentes "
    "la condición observable, la forma de comprobarla y el resultado esperado. Distingue "
    "el principio documental de los detalles inventados. No trates una condición nueva "
    "como exigida si no la has declarado como supuesto del ejemplo. "
    "No concluyas coste, tiempo, exhaustividad ni garantías sin premisas que lo permitan. "
    "Si faltan datos para valorar una condición, explica qué información falta. "
    "Mantén una conversación natural, sin un esquema de salida obligatorio."
)


def instruction_for_profile(baseline, profile="baseline"):
    if profile == "baseline":
        return baseline
    if profile == "pedagogy-v1":
        return baseline + "\n\n" + PEDAGOGICAL_EXTENSION
    raise ValueError("unknown pedagogical profile")
