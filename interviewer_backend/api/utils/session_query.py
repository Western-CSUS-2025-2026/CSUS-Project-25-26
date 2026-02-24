from typing import List, Set, Tuple
from sqlalchemy.orm import joinedload, raiseload
from api.models.db import Session, SessionComponent
from api.schemas.models import SessionComponentGet, SessionGet


def parse_include(include: List[str] | None) -> Set[str]:
    if not include:
        return set()
    return {item.strip().lower() for item in include}


def get_session_options(requested: Set[str]) -> Tuple[list, Set[str]]:
    valid_fields = {"components", "grades", "feedback", "videos", "questions"}
    valid_requested = requested & valid_fields

    if not valid_requested:
        return [raiseload(Session.session_components)], set()

    base = joinedload(Session.session_components)
    options = [base.raiseload("*")]

    relationships = {
        "questions": SessionComponent.question,
        "grades": SessionComponent.grade,
        "feedback": SessionComponent.feedback,
        "videos": SessionComponent.video,
    }

    for key, relationship in relationships.items():
        if key in valid_requested:
            options.append(base.joinedload(relationship))

    return options, valid_requested


def serialize_session(s: Session, valid_requested: Set[str]) -> SessionGet:
    components = None
    if "components" in valid_requested or any(
        k in valid_requested for k in {"grades", "feedback", "videos", "questions"}
    ):
        components = [
            SessionComponentGet(
                id=c.id,
                transcript=c.transcript,
                question_id=c.question_id,
                question=c.question if "questions" in valid_requested else None,
                grade=c.grade if "grades" in valid_requested else None,
                feedback=c.feedback if "feedback" in valid_requested else None,
                video=c.video if "videos" in valid_requested else None,
            )
            for c in s.session_components
        ]

    return SessionGet(
        id=s.id,
        user_id=s.user_id,
        state=s.state,
        overall_grade=s.overall_grade,
        create_ts=s.create_ts,
        session_components=components,
    )
