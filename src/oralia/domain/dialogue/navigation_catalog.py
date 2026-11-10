"""Authored navigation templates, additive to the historical catalog and policies."""

NAVIGATION_TEXTS = {
    "orientation": (
        "Podemos estudiar estos temas publicados: {options}. "
        "Di elijo y el nombre del tema; después di confirmo. "
        "Puedes pedir más opciones, repetir opciones o terminar la sesión."
    ),
    "clarify": (
        "No puedo resolver esa referencia con seguridad. Temas disponibles: {options}. "
        "Di elijo y el nombre del tema, repetir opciones o terminar la sesión."
    ),
    "clarify_question": (
        "La pregunta actual se mantiene. Puedes decir repite la pregunta, ayuda, "
        "otra forma o cambiar de tema. Para elegir un tema di qué temas hay."
    ),
    "confirm_topic": (
        "Se propone el tema {topic}. Di confirmo para cambiar o cancelar cambio para mantener el actual."
    ),
    "limited": (
        "Ese apoyo no está disponible o permitido para este objetivo. "
        "Puedes pedir ayuda, qué temas hay, qué modos hay o terminar la sesión."
    ),
    "recovery": (
        "Vamos a elegir otra acción. Di qué temas hay para oír alternativas, "
        "ayuda para un apoyo autorizado o terminar la sesión."
    ),
    "modes": "Modos habilitados: {modes}. Para elegir uno di quiero y su nombre.",
    "defense_controls": (
        "Esta actividad es una defensa; no ofrece modos de autoestudio. Puedes decir "
        "repite la pregunta, ayuda, otra forma o qué temas hay."
    ),
    "unknown_topic": (
        "No puedo seleccionar ese tema con seguridad. Temas vigentes: {options}. Di "
        "elijo y un nombre inequívoco, o más opciones."
    ),
    "controls": (
        "Puedes decir qué temas hay, elijo y el nombre de un tema, confirmo, "
        "repite opciones, ayuda, otra forma, de dónde sale eso, "
        "qué conservarás o terminar la sesión."
    ),
    "sources": (
        "La procedencia vigente es {source}. Identifico la procedencia, no leo fragmentos de la fuente. "
        "Para ampliar di más sobre la fuente; para seguir di ayuda o continúa."
    ),
    "sources_more": (
        "Referencia ampliada: {source}. No leo fragmentos no autorizados. Para " "seguir di ayuda o continúa."
    ),
    "no_sources": (
        "No hay una fuente vigente que pueda identificar para la última respuesta. "
        "Puedes pedir qué temas hay o ayuda. No leeré contenido retirado o no autorizado."
    ),
    "privacy": (
        "Al cerrar se conservará {choice}. Plazo autorizado: {days}. "
        "El audio no se conserva. Opciones autorizadas: {privacy_options}. "
        "Te pediré confirmar la elección exacta; puedes participar sin conservar."
    ),
    "privacy_closed": (
        "Estado actual del registro: {choice}. Plazo configurado: {days}. Puedes "
        "decir revisar intervención uno o eliminar mi contenido."
    ),
    "privacy_pending": (
        "Propones conservar {choice}. Plazo autorizado: {days}. "
        "Para aceptarlo di {confirmation}. Para descartarlo di cancelar conservación. "
        "Un sí aislado no confirma esta decisión. El audio no se conserva."
    ),
    "privacy_confirmed": (
        "Elección confirmada: al cerrar se conservará {choice}. "
        "El audio no se conserva. Puedes cambiar la elección antes de cerrar o terminar la sesión."
    ),
    "privacy_forbidden": (
        "Esa conservación no está autorizada por la actividad. No he cambiado tu elección. "
        "Puedes decir qué conservarás o no conservar nada."
    ),
    "cancelled": "Solicitud cancelada. La sesión sigue activa. Puedes decir ayuda o qué temas hay.",
    "close_confirm": (
        "¿Quieres cerrar esta sesión? Se conservará {choice}. "
        "Di confirmo cerrar para finalizar o continuar sesión para seguir. "
        "Para cambiar la conservación di qué conservarás antes de confirmar el cierre."
    ),
    "finish": (
        "La sesión ha terminado. Se aplica la elección confirmada: {choice}. "
        "Puedes decir revisar intervención uno, estado de conservación o eliminar mi contenido."
    ),
    "closed": (
        "La sesión está cerrada. Puedes decir revisar intervención uno, "
        "estado de conservación o eliminar mi contenido. No se inicia otra sesión."
    ),
    "review": (
        "Registro histórico propio, intervención {index}. Participante dijo: "
        "{input}. Sistema dijo: {output}. Esto es una lectura del registro, no una "
        "nueva respuesta docente. Para otra intervención di revisar intervención y "
        "su número; también puedes decir eliminar mi contenido."
    ),
    "no_record": (
        "No hay una transcripción propia conservada y accesible para esa intervención. "
        "Puede no haberse conservado, haber caducado o estar eliminada. No reconstruiré su contenido. "
        "Puedes pedir estado de conservación."
    ),
    "delete_prompt": (
        "Eliminar borra el contenido conservado de esta sesión y no se puede deshacer. "
        "Si quieres hacerlo di confirmo eliminar el contenido de esta sesión. "
        "Un sí aislado no autoriza la eliminación."
    ),
    "deleted": "El contenido de esta sesión está eliminado. Solo queda un recibo técnico sin texto.",
    "verification_failed": (
        "No he podido verificar la respuesta. Puedes decir qué temas hay, ayuda o " "terminar la sesión."
    ),
    "disabled_mode": (
        "Ese modo no está habilitado. Di qué modos hay para oír los permitidos o " "ayuda para continuar."
    ),
    "empty": "No hay temas autorizados vigentes. Puedes terminar la sesión y solicitar revisión docente.",
}
