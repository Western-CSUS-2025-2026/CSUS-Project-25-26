from typing import List, Set
from sqlalchemy.orm import joinedload, noload
from api.models.db import Session, SessionComponent


def parse_include(include: List[str] | None) -> Set[str]:
    if not include:
        return set()
    return {item.strip().lower() for item in include}


def get_session_options(requested: Set[str]):
    if not requested or not any(
        item in {"components", "grades", "feedback", "videos", "questions"} for item in requested
    ):
        return [noload(Session.session_components)]

    base = joinedload(Session.session_components)
    options = [base]

    relationships = {
        "questions": SessionComponent.question,
        "grades": SessionComponent.grade,
        "feedback": SessionComponent.feedback,
        "videos": SessionComponent.video,
    }

    for key, relationship in relationships.items():
        if key in requested:
            options.append(base.joinedload(relationship))
        else:
            options.append(base.noload(relationship))

    return options
