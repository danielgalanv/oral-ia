"""Fictional publication fixture for wiring tests, never real course review evidence."""

import json

from oralia.domain.dialogue.semantic_templates import semantic_guided_policy
from oralia.infrastructure.db import models
from tests.dialogue.api_fixture import checked, prepare_guided


def prepare_semantic_activity(client, *, start=True):
    policy = semantic_guided_policy("synthetic-010").model_dump(mode="json")

    def transform(value):
        value.clear()
        value.update(policy)

    prepared = prepare_guided(client, domain="programa", start=False, policy_transform=transform)
    activity_id = prepared["activity"]["id"]
    with client.__db_sessionmaker__() as db:
        rows = {key: db.get(models.TeachingUnit, value) for key, value in prepared["units"].items()}
        goals = []
        for key, root in rows.items():
            if not key.endswith("-explanation"):
                continue
            prefix = key.removesuffix("-explanation")
            question = rows[prefix + "-question"]
            goals.append(
                {
                    "goal": root.subgoal_ref,
                    "topic": root.topic_ref,
                    "root_text": root.reviewed_content,
                    "source_refs": root.source_refs,
                    "course_id": root.course_id,
                    "example": rows[prefix + "-example"].id,
                    "comparison": rows[prefix + "-comparison"].id,
                    "question_text": question.reviewed_content,
                    "hints": question.relations["hints"],
                }
            )
    bindings = {}
    for goal in goals:

        def create(kind, text, relations=None, *, goal=goal):
            created = checked(
                client.post(
                    "/api/v1/governance/teaching-units",
                    json={
                        "course_id": goal["course_id"],
                        "kind": kind,
                        "topic_ref": goal["topic"],
                        "subgoal_ref": goal["goal"],
                        "reviewed_content": text,
                        "source_refs": goal["source_refs"],
                        "activity_refs": [activity_id],
                        "reveal_policy": "question" if kind == "question" else "study_only",
                        "relations": relations or {},
                    },
                ),
                201,
            )
            # Explicit simulation on fictional material only. This cannot approve
            # any of the real83units or demonstrate review by a human teacher.
            checked(
                client.post(
                    f"/api/v1/governance/teaching-units/{created['id']}/publish", json={"reviewed": True}
                )
            )
            return created["id"]

        cause = create(
            "explanation",
            f"En el curso ficticio, {goal['topic']} tiene una función diferenciada dentro del sistema.",
        )
        process = create(
            "explanation",
            f"Para recorrer {goal['topic']} en el ejemplo ficticio, "
            "identifica su función y sigue sus operaciones.",
        )
        rephrase = create(
            "explanation",
            f"Otra mirada a {goal['topic']}: separa qué recibe, "
            "qué transforma y qué entrega este ejemplo ficticio.",
        )
        question = create(
            "question", goal["question_text"], {"hints": goal["hints"], "comparisons": [goal["comparison"]]}
        )
        root = create(
            "explanation",
            goal["root_text"],
            {
                "didactic_cause": [cause],
                "didactic_process": [process],
                "rephrases": [rephrase],
                "examples": [goal["example"]],
                "comparisons": [goal["comparison"]],
                "next": [question],
            },
        )
        bindings[goal["goal"]] = {
            "root": root,
            "cause": cause,
            "process": process,
            "rephrase": rephrase,
            "example": goal["example"],
            "comparison": goal["comparison"],
            "question": question,
        }
    prepared["bindings"] = bindings
    prepared["session"] = (
        checked(
            client.post(
                "/api/v1/sessions",
                json={"participant_code": "synthetic-010", "activity_configuration_id": activity_id},
            ),
            201,
        )
        if start
        else None
    )
    return prepared


class SyntheticIntentPort:
    def __init__(self, answers):
        self.answers = iter(answers)
        self.requests = []

    async def generate(self, request):
        from oralia.infrastructure.generation.generation_port import GenerationOutcome

        self.requests.append(request)
        return GenerationOutcome(
            ok=True, text=json.dumps(next(self.answers)), adapter="deterministic", finish_reason="stop"
        )
