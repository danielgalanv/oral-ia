"""Registered opt-in study bounds; no authority or runtime renewal."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class StudyBudget:
    profile: str
    max_tokens: int
    deadline_seconds: int
    candidate_characters: int

    def public(self):
        return asdict(self)


HISTORICAL = StudyBudget("historical/v1", 768, 50, 4000)
EXPANDED = StudyBudget("study-expanded/v1", 2048, 180, 16000)
REVIEWED = StudyBudget("study-reviewed/v1", 2048, 180, 16000)


def study_budget(profile="historical/v1"):
    for budget in (HISTORICAL, EXPANDED, REVIEWED):
        if profile == budget.profile:
            return budget
    raise ValueError("Unknown study budget profile")
