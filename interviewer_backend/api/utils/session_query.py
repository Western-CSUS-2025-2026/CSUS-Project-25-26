from sqlalchemy.orm import joinedload

from typing import List, Set
from api.models.db import Session, SessionComponent


def parse_include(include: List[str] | None) -> Set[str]:
    """Helper to normalize the include list into a set of lowercase strings."""
    if not include:
        return set()
    requested = set()
    for item in include:
        for sub_item in item.split(","):
            requested.add(sub_item.strip().lower())
    return requested


def get_session_options(requested: Set[str]):
    """Helper to convert a set of strings into SQLAlchemy joinedload options."""
    options = []
    component_triggers = {"components", "grades", "feedback", "videos"}

    if any(item in requested for item in component_triggers):
        base_load = joinedload(Session.session_components)
        if "grades" in requested:
            options.append(base_load.joinedload(SessionComponent.grade))
        if "feedback" in requested:
            options.append(base_load.joinedload(SessionComponent.feedback))
        if "videos" in requested:
            options.append(base_load.joinedload(SessionComponent.video))

        if not options:
            options.append(base_load)
    return options


def build_serialization_filter(requested: Set[str]) -> dict:
    """
    Builds a Pydantic 'include' mask.
    Only fields set to True or a sub-dict will be included in the final JSON.
    """

    session_mask = {
        "id": True,
        "user_id": True,
        "state": True,
        "overall_grade": True,
        "create_ts": True,
    }

    if "components" in requested or any(x in requested for x in ["grades", "feedback", "videos"]):
        component_mask = {"id": True, "transcript": True, "question_id": True}

        if "grades" in requested:
            component_mask["grade"] = True
        if "feedback" in requested:
            component_mask["feedback"] = True
        if "videos" in requested:
            component_mask["video"] = True

        session_mask["session_components"] = {"__all__": component_mask}

    return session_mask
