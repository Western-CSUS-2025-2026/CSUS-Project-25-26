from typing import List, Set, Tuple

from sqlalchemy.orm import joinedload, raiseload

from api.models.db import Session, SessionComponent
from api.schemas.models import (
    FeedbackGet,
    GradeGet,
    QuestionGet,
    SessionComponentGet,
    SessionGet,
    TemplateGet,
    VideoGet,
)


def parse_include(include: List[str] | None) -> Set[str]:
    if not include:
        return set()
    return {item.strip().lower() for item in include}


def get_session_options(requested: Set[str]) -> Tuple[list, Set[str]]:
    valid_fields = {"template", "components", "grades", "feedback", "videos", "questions"}
    valid_requested = requested & valid_fields

    options = []
    if "template" in valid_requested:
        options.append(joinedload(Session.template))
    else:
        options.append(raiseload(Session.template))

    relationships = {
        "questions": SessionComponent.question,
        "grades": SessionComponent.grade,
        "feedback": SessionComponent.feedback,
        "videos": SessionComponent.video,
    }

    component_keys = {"components", "grades", "feedback", "videos", "questions"}
    if valid_requested & component_keys:
        base = joinedload(Session.session_components)
        options.append(base.raiseload("*"))

        for key, relationship in relationships.items():
            if key in valid_requested:
                options.append(base.joinedload(relationship))
    else:
        options.append(raiseload(Session.session_components))

    return options, valid_requested


def serialize_session(s: Session, valid_requested: Set[str]) -> SessionGet:
    template = None
    if "template" in valid_requested and s.template is not None:
        template = TemplateGet(
            id=s.template.id,
            job_title=s.template.job_title,
            description=s.template.description,
            is_hidden=s.template.is_hidden,
        )

    components = None
    if "components" in valid_requested or any(
        k in valid_requested for k in {"grades", "feedback", "videos", "questions"}
    ):
        components = []
        for c in s.session_components:
            question = None
            grade = None
            feedback = None
            video = None

            if "questions" in valid_requested and c.question is not None:
                question = QuestionGet(
                    id=c.question.id,
                    question=c.question.question,
                    template_id=c.question.template_id,
                )
            if "grades" in valid_requested and c.grade is not None:
                grade = GradeGet(
                    id=c.grade.id,
                    body_language_score=c.grade.body_language_score,
                    speech_score=c.grade.speech_score,
                    material_score=c.grade.material_score,
                    brevity_score=c.grade.brevity_score,
                )
            if "feedback" in valid_requested and c.feedback is not None:
                feedback = FeedbackGet(
                    id=c.feedback.id,
                    point=c.feedback.point,
                    ways_to_improve=c.feedback.ways_to_improve,
                )
            if "videos" in valid_requested and c.video is not None:
                video = VideoGet(
                    id=c.video.id,
                    s3_key=c.video.s3_key,
                )

            components.append(
                SessionComponentGet(
                    id=c.id,
                    transcript=c.transcript,
                    state=c.state.value,
                    question_id=c.question_id,
                    question=question,
                    grade=grade,
                    feedback=feedback,
                    video=video,
                )
            )

    return SessionGet(
        id=s.id,
        user_id=s.user_id,
        overall_grade=s.overall_grade,
        create_ts=s.create_ts,
        template=template,
        session_components=components,
    )
