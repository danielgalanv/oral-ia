"""Immutable, versioned catalog of trusted output templates."""

import hashlib
from collections.abc import Iterable
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    model_validator,
)

from oralia.domain.agents.fallback_agent import SAFE_FALLBACK_TEXT
from oralia.domain.dialogue.navigation_catalog import NAVIGATION_TEXTS


def _reject_blank_string(value: str) -> str:
    if not value.strip():
        raise ValueError("string must contain at least one non-whitespace character")
    return value


NonBlankString = Annotated[
    str,
    StringConstraints(strict=True, min_length=1),
    AfterValidator(_reject_blank_string),
]
PositiveStrictInt = Annotated[int, Field(strict=True, gt=0)]
Sha256Hex = Annotated[
    str,
    StringConstraints(strict=True, min_length=64, max_length=64, pattern=r"^[0-9a-f]+$"),
]
MessageType = Literal["normal", "operational"]


def output_text_sha256(text: str) -> str:
    """Hash the exact UTF-8 bytes of output text without transforming it."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class OutputTemplateEntry(BaseModel):
    """One immutable normal or operational output template version."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    template_id: NonBlankString
    version: PositiveStrictInt
    message_type: MessageType
    text: NonBlankString
    sha256: Sha256Hex
    topic_ref: NonBlankString
    purpose_ref: NonBlankString
    action_ref: NonBlankString

    @model_validator(mode="after")
    def validate_text_hash(self) -> Self:
        if self.sha256 != output_text_sha256(self.text):
            raise ValueError("sha256 must match the exact UTF-8 bytes of text")
        return self

    @classmethod
    def from_text(
        cls,
        *,
        template_id: str,
        version: int,
        message_type: MessageType,
        text: str,
        topic_ref: str,
        purpose_ref: str,
        action_ref: str,
    ) -> Self:
        """Build a validated entry and derive its exact-text SHA-256."""

        return cls(
            template_id=template_id,
            version=version,
            message_type=message_type,
            text=text,
            sha256=output_text_sha256(text),
            topic_ref=topic_ref,
            purpose_ref=purpose_ref,
            action_ref=action_ref,
        )

    @property
    def identity(self) -> tuple[str, int, str]:
        """Return the complete identity required for catalog resolution."""

        return (self.template_id, self.version, self.sha256)


class OutputTemplateCatalog(BaseModel):
    """Immutable catalog that retains every registered template version."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    entries: tuple[OutputTemplateEntry, ...]

    @model_validator(mode="after")
    def reject_duplicate_versions(self) -> Self:
        identities = [(entry.template_id, entry.version) for entry in self.entries]
        if len(identities) != len(set(identities)):
            raise ValueError("template_id and version pairs must be unique")
        return self

    def resolve(self, template_id: str, version: int, sha256: str) -> OutputTemplateEntry:
        """Resolve only an exact ID, version, and content-hash identity."""

        if not isinstance(template_id, str) or not template_id.strip():
            raise ValueError("template_id must be a non-blank string")
        if type(version) is not int or version <= 0:
            raise ValueError("version must be a positive integer")
        if (
            not isinstance(sha256, str)
            or len(sha256) != 64
            or any(character not in "0123456789abcdef" for character in sha256)
        ):
            raise ValueError("sha256 must be exactly 64 lowercase hexadecimal characters")

        for entry in self.entries:
            if entry.identity == (template_id, version, sha256):
                return entry
        raise KeyError("no output template matches the complete identity")

    def extended(self, entries: Iterable[OutputTemplateEntry]) -> Self:
        """Return a new catalog with additional versions and preserve this catalog."""

        return type(self)(entries=(*self.entries, *tuple(entries)))


SC007_ACKNOWLEDGEMENT_TEXT = "He recibido tu mensaje. Continuemos con la actividad."

SC007_ACKNOWLEDGEMENT = OutputTemplateEntry.from_text(
    template_id="sc007-acknowledgement",
    version=1,
    message_type="normal",
    text=SC007_ACKNOWLEDGEMENT_TEXT,
    topic_ref="activity",
    purpose_ref="acknowledge_turn",
    action_ref="continue",
)

SAFE_TECHNICAL_FALLBACK = OutputTemplateEntry.from_text(
    template_id="safe-technical-fallback",
    version=1,
    message_type="operational",
    text=SAFE_FALLBACK_TEXT,
    topic_ref="activity",
    purpose_ref="technical_recovery",
    action_ref="clarify",
)

MATERIAL_FRAGMENT_RESPONSE = OutputTemplateEntry.from_text(
    template_id="material-fragment-response",
    version=1,
    message_type="normal",
    text="{content}",
    topic_ref="activity",
    purpose_ref="material_response",
    action_ref="respond",
)

GREETED_REVIEWED_RESPONSE = OutputTemplateEntry.from_text(
    template_id="greeted-reviewed-response",
    version=1,
    message_type="normal",
    text="Hola. {content}",
    topic_ref="activity",
    purpose_ref="material_response",
    action_ref="respond",
)

MATERIAL_FRAGMENT_RESPONSE_2 = OutputTemplateEntry.from_text(
    template_id="material-fragment-response-2",
    version=1,
    message_type="normal",
    text="{content_0} {content_1}",
    topic_ref="activity",
    purpose_ref="material_response",
    action_ref="respond",
)

MATERIAL_FRAGMENT_RESPONSE_3 = OutputTemplateEntry.from_text(
    template_id="material-fragment-response-3",
    version=1,
    message_type="normal",
    text="{content_0} {content_1} {content_2}",
    topic_ref="activity",
    purpose_ref="material_response",
    action_ref="respond",
)

SELF_STUDY_MISSING_INFO = OutputTemplateEntry.from_text(
    template_id="self-study-missing-info",
    version=1,
    message_type="normal",
    text=(
        "No he encontrado información suficiente en los materiales de la actividad para "
        "responder con precisión a esto. ¿Puedes reformular tu pregunta o consultarlo con "
        "el profesorado?"
    ),
    topic_ref="activity",
    purpose_ref="missing_information",
    action_ref="acknowledge_missing_info",
)

SELF_STUDY_CONFLICT = OutputTemplateEntry.from_text(
    template_id="self-study-material-conflict",
    version=1,
    message_type="normal",
    text=(
        "Los materiales de la actividad contienen información que parece contradictoria "
        "sobre esto. Te recomiendo consultarlo con el profesorado."
    ),
    topic_ref="activity",
    purpose_ref="material_conflict",
    action_ref="clarify",
)

SELF_STUDY_INCOHERENCE = OutputTemplateEntry.from_text(
    template_id="self-study-incoherence",
    version=1,
    message_type="normal",
    text=(
        "Antes de continuar, creo que conviene revisar el hilo de la conversación: puede "
        "que ya hayamos tratado esto o que convenga reformularlo. ¿Quieres que lo retomemos "
        "de otra forma?"
    ),
    topic_ref="activity",
    purpose_ref="conversation_recovery",
    action_ref="clarify",
)

SELF_STUDY_GENERAL_KNOWLEDGE_NOTICE = OutputTemplateEntry.from_text(
    template_id="self-study-general-knowledge-notice",
    version=1,
    message_type="normal",
    text=(
        "No encuentro esto en los materiales de la actividad; se trata de conocimiento "
        "general, no verificado frente a los materiales."
    ),
    topic_ref="activity",
    purpose_ref="general_knowledge",
    action_ref="respond",
)

SELF_STUDY_DEFAULT_PRACTICE_QUESTION = OutputTemplateEntry.from_text(
    template_id="self-study-default-practice-question",
    version=1,
    message_type="normal",
    text="Explica con tus propias palabras qué sabes sobre: el tema tratado.",
    topic_ref="activity",
    purpose_ref="practice_question",
    action_ref="ask",
)

DEFENSE_DYNAMIC_OUTPUT = OutputTemplateEntry.from_text(
    template_id="defense-dynamic-output",
    version=1,
    message_type="normal",
    text="{content}",
    topic_ref="activity",
    purpose_ref="oral_defense",
    action_ref="ask",
)

DEFENSE_MISSING_INFORMATION = OutputTemplateEntry.from_text(
    template_id="defense-missing-information",
    version=1,
    message_type="normal",
    text=(
        "No dispongo de información suficiente en los materiales autorizados para "
        "formular otra pregunta sobre este tema."
    ),
    topic_ref="activity",
    purpose_ref="missing_information",
    action_ref="acknowledge_missing_info",
)

DEFENSE_CLARIFICATION = OutputTemplateEntry.from_text(
    template_id="defense-clarification",
    version=1,
    message_type="normal",
    text="¿Puedes aclarar qué quisiste expresar para que podamos continuar?",
    topic_ref="activity",
    purpose_ref="clarify_response",
    action_ref="clarify",
)

DEFENSE_INITIAL_QUESTION = OutputTemplateEntry.from_text(
    template_id="defense-initial-question",
    version=1,
    message_type="normal",
    text="{content}",
    topic_ref="activity",
    purpose_ref="oral_defense",
    action_ref="ask",
)

DEFENSE_LIMIT_CLOSE = OutputTemplateEntry.from_text(
    template_id="defense-limit-close",
    version=1,
    message_type="normal",
    text="La defensa ha finalizado al alcanzar el límite configurado.",
    topic_ref="activity",
    purpose_ref="oral_defense_close",
    action_ref="finish",
)

DEFENSE_VOLUNTARY_CLOSE = OutputTemplateEntry.from_text(
    template_id="defense-voluntary-close",
    version=1,
    message_type="normal",
    text="La defensa ha finalizado a petición del participante.",
    topic_ref="activity",
    purpose_ref="oral_defense_close",
    action_ref="finish",
)

DEFENSE_SUMMARY = OutputTemplateEntry.from_text(
    template_id="defense-summary",
    version=1,
    message_type="normal",
    text="{content}",
    topic_ref="activity",
    purpose_ref="oral_defense_summary",
    action_ref="respond",
)

_GUIDED_TEXT = {
    "unavailable_repeat": (
        "El contenido sigue sin estar disponible. Puedes terminar la sesión "
        "y pedir al docente que revise la actividad."
    ),
    "recovery": (
        "Elige explícitamente otro objetivo publicado, pide una pregunta de práctica "
        "o termina y solicita revisión docente. El contenido que no se ha verificado no se mostrará."
    ),
    "verification_failed": (
        "No se ha podido verificar una respuesta para este turno. Puedes pedir otra "
        "pregunta, elegir otro tema o terminar."
    ),
    "orientation": (
        "Podemos trabajar los objetivos publicados de esta actividad. Elige un tema "
        "disponible o pide una pregunta de práctica."
    ),
    "clarify": (
        "¿A qué objetivo te refieres? Elige un tema disponible, pide repetir la "
        "pregunta pendiente o termina la sesión."
    ),
    "limited": (
        "El material vigente no incluye ese apoyo para este objetivo. Puedes elegir "
        "otro tema disponible, pedir una pregunta o terminar."
    ),
    "confirm_topic": (
        "Confirma el nuevo tema para cambiar de objetivo o pide continuar con la " "pregunta pendiente."
    ),
    "disabled_mode": (
        "Ese modo no está habilitado en esta actividad. Elige uno de los modos "
        "disponibles o continúa con el actual."
    ),
    "unavailable": (
        "No hay contenido autorizado vigente para esta actividad. Puedes terminar y "
        "solicitar revisión docente."
    ),
    "finish": (
        "La sesión ha terminado. La conservación se aplica únicamente conforme a tu "
        "elección y la política de esta actividad."
    ),
}
GUIDED_NOTICES = {
    name: OutputTemplateEntry.from_text(
        template_id=f"guided-{name.replace('_','-')}",
        version=1,
        message_type="normal",
        text=text,
        topic_ref="activity",
        purpose_ref="guided_control",
        action_ref="respond",
    )
    for name, text in _GUIDED_TEXT.items()
}

# Additive navigation versions; historical entries and identities remain unchanged.

NAVIGATION_TEMPLATES = {
    name: OutputTemplateEntry.from_text(
        template_id=f"screenless-{name.replace('_', '-')}",
        version=1,
        message_type="normal",
        text=text,
        topic_ref="activity",
        purpose_ref="guided_control",
        action_ref="respond",
    )
    for name, text in NAVIGATION_TEXTS.items()
}

PEDAGOGIC_NAVIGATION_TEMPLATES = {
    name: OutputTemplateEntry.from_text(
        template_id=f"didactic-{name}",
        version=1,
        message_type="normal",
        text=text,
        topic_ref="activity",
        purpose_ref="guided_control",
        action_ref="respond",
    )
    for name, text in {
        "greeting": (
            "Hola. Soy ORALIA, un asistente automático de apoyo al estudio. Podemos"
            " trabajar estos temas publicados: {options}. Puedes preguntar por uno,"
            " pedir más opciones o elegir un tema y confirmar el cambio."
        ),
        "overview": (
            "Podemos estudiar el material de esta actividad; no es una explicación "
            "completa de toda la asignatura. Estos temas publicados permiten empeza"
            "r: {options}. Puedes preguntar qué significa uno, cómo ocurre, por qué"
            " ocurre o pedir más opciones. Si falta una explicación autorizada, te "
            "indicaré ese límite."
        ),
    }.items()
}

PACKAGE_NAVIGATION_TEMPLATES = {
    name: OutputTemplateEntry.from_text(
        template_id=f"package-{name}",
        version=1,
        message_type="normal",
        text=text,
        topic_ref="activity",
        purpose_ref="guided_control",
        action_ref="respond",
    )
    for name, text in {
        "package_welcome": (
            "Hola. Soy ORALIA, un asistente automático de apoyo al estudio. Ma"
            "ntendremos como objetivo {topic}. Puedes preguntar qué significa,"
            " por qué ocurre, cómo se desarrolla o pedir ayuda. Otros temas pu"
            "blicados: {options}."
        ),
        "package_topic_confirmed": (
            "Hemos confirmado el cambio al objetivo {topic}. Puedes preguntar "
            "qué significa, por qué ocurre o cómo se desarrolla. El objetivo a"
            "nterior ya no se usa para responder."
        ),
        "outside_source": (
            "No encuentro una respuesta respaldada para esa petición en las fu"
            "entes de esta actividad. No voy a inventarla. Puedes concretar un"
            "a duda sobre estos temas publicados: {options}, pedir fuentes o t"
            "erminar la sesión."
        ),
    }.items()
}

CONTINUITY_NAVIGATION_TEMPLATES = {
    "followups_exhausted": OutputTemplateEntry.from_text(
        template_id="continuity-followups-exhausted",
        version=1,
        message_type="normal",
        text=(
            "Hemos agotado las repreguntas publicadas para esta pregunta. Esto"
            " no valora tu respuesta. Puedes pedir una pista disponible, repet"
            "ir la pregunta o terminar la sesión."
        ),
        topic_ref="activity",
        purpose_ref="guided_control",
        action_ref="respond",
    ),
}

DEFAULT_OUTPUT_TEMPLATE_CATALOG = OutputTemplateCatalog(
    entries=(
        SC007_ACKNOWLEDGEMENT,
        SAFE_TECHNICAL_FALLBACK,
        MATERIAL_FRAGMENT_RESPONSE,
        GREETED_REVIEWED_RESPONSE,
        MATERIAL_FRAGMENT_RESPONSE_2,
        MATERIAL_FRAGMENT_RESPONSE_3,
        SELF_STUDY_MISSING_INFO,
        SELF_STUDY_CONFLICT,
        SELF_STUDY_INCOHERENCE,
        SELF_STUDY_GENERAL_KNOWLEDGE_NOTICE,
        SELF_STUDY_DEFAULT_PRACTICE_QUESTION,
        DEFENSE_DYNAMIC_OUTPUT,
        DEFENSE_MISSING_INFORMATION,
        DEFENSE_CLARIFICATION,
        DEFENSE_INITIAL_QUESTION,
        DEFENSE_LIMIT_CLOSE,
        DEFENSE_VOLUNTARY_CLOSE,
        DEFENSE_SUMMARY,
        *GUIDED_NOTICES.values(),
        *NAVIGATION_TEMPLATES.values(),
        *PEDAGOGIC_NAVIGATION_TEMPLATES.values(),
        *PACKAGE_NAVIGATION_TEMPLATES.values(),
        *CONTINUITY_NAVIGATION_TEMPLATES.values(),
    ),
)


__all__ = [
    "DEFAULT_OUTPUT_TEMPLATE_CATALOG",
    "DEFENSE_CLARIFICATION",
    "DEFENSE_DYNAMIC_OUTPUT",
    "DEFENSE_INITIAL_QUESTION",
    "DEFENSE_LIMIT_CLOSE",
    "DEFENSE_MISSING_INFORMATION",
    "DEFENSE_SUMMARY",
    "DEFENSE_VOLUNTARY_CLOSE",
    "MATERIAL_FRAGMENT_RESPONSE",
    "MATERIAL_FRAGMENT_RESPONSE_2",
    "MATERIAL_FRAGMENT_RESPONSE_3",
    "OutputTemplateCatalog",
    "OutputTemplateEntry",
    "SAFE_TECHNICAL_FALLBACK",
    "SELF_STUDY_CONFLICT",
    "SELF_STUDY_DEFAULT_PRACTICE_QUESTION",
    "SELF_STUDY_GENERAL_KNOWLEDGE_NOTICE",
    "SELF_STUDY_INCOHERENCE",
    "SELF_STUDY_MISSING_INFO",
    "SC007_ACKNOWLEDGEMENT",
    "SC007_ACKNOWLEDGEMENT_TEXT",
    "output_text_sha256",
]
