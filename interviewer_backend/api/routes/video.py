import json

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi_sqlalchemy import db


from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis
from api.schemas.models import VideoAnalysisStateResponse, VideoUploadResponse, TwelveLabsWebhookRequest, QuestionResponseModel, FeedbackModel
from api.schemas.base import StatusResponseModel
from api.schemas.models import SessionCreateResponse, SessionComponentCreateResponse, SessionComponentCreateRequest
from api.models.db import SessionState, Session, UserSession, Question, SessionComponent, Feedback, Grade, Template


video = APIRouter(prefix="/video", tags=["Video"])
analyzer = VideoAnalysis()


@video.post("/session", status_code=201, response_model=SessionCreateResponse)
async def create_session(
    user_session: UserSession = Depends(Auth())
) -> SessionCreateResponse:
    """Create a new interview session for the authenticated user."""
    
    session = Session.create(
        session=db.session,
        user_id=user_session.user_id,
        indexed_asset_id=None,
        state=SessionState.PENDING
    )
    db.session.commit()
    
    return SessionCreateResponse(
        session_id=session.id,
        state=session.state.value,
    )


@video.post("/session/{session_id}/component", status_code=201, response_model=SessionComponentCreateResponse)
async def add_session_component(
    session_id: int,
    component_data: SessionComponentCreateRequest,
    user_session: UserSession = Depends(Auth())
) -> SessionComponentCreateResponse:
    """Add a question/component to an existing session."""
    
    session = Session.get(session_id, session=db.session)
    
    if session.user_id != user_session.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    default_template = (
        Template.query(session=db.session)
        .filter(Template.job_title == f"{user_session.user_id} Questions")
        .one_or_none()
    )
    
    if not default_template:
        default_template = Template.create(
            session=db.session,
            job_title=f"{user_session.user_id} Questions",
            description=f"Questions submitted by {user_session.user_id} during video uploads"
        )
        db.session.flush()
    
    question_record = (
        Question.query(session=db.session)
        .filter(Question.question == component_data.question)
        .one_or_none()
    )
    
    if not question_record:
        question_record = Question.create(
            session=db.session,
            question=component_data.question,
            template_id=default_template.id
        )
        db.session.flush()
    
    session_component = SessionComponent.create(
        session=db.session,
        session_id=session_id,
        question_id=question_record.id,
        transcript=None
    )
    db.session.commit()

    return SessionComponentCreateResponse(
        session_component_id=session_component.id,
        session_id=session_id,
        question=question_record.question,
        question_id=question_record.id
    )


@video.post("/session/{session_id}/upload_video", status_code=202)
async def upload_video_to_session(
    session_id: int,
    session_component_id: int = Form(...),
    video: UploadFile = File(...),
    user_session: UserSession = Depends(Auth())
):
    """Upload video for a specific session component."""
    
    session = Session.get(session_id, session=db.session)
    
    if session.user_id != user_session.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    session_component = SessionComponent.get(session_component_id, session=db.session)
    
    if session_component.session_id != session_id:
        raise HTTPException(status_code=400, detail="Component does not belong to this session")
    
    index_id = analyzer.get_or_create_index(user_session.user_id, session=db.session)
    asset = analyzer.upload_asset(file=video)
    indexed_asset = analyzer.index_asset(index_id=index_id, asset_id=asset.id)
    
    if not session.indexed_asset_id:
        session.indexed_asset_id = indexed_asset.id
        session.state = SessionState.INDEXING
        db.session.commit()
    
    return VideoUploadResponse(
        asset_id=asset.id,
        indexed_asset_id=indexed_asset.id,
        session_id=session.id,
        session_component_id=session_component.id,
        question=session_component.question.question,
        state=session.state.value
    )


@video.post("/webhook/twelvelabs")
async def twelvelabs_webhook(payload: TwelveLabsWebhookRequest):
    indexed_asset_id = payload.indexed_asset_id or payload.id
    state = (payload.state or payload.status or "").lower()

    # always return 200 even if malformed, but log server-side
    if not indexed_asset_id:
        return StatusResponseModel(status="error", message="Missing indexed_asset_id")

    session = (
        Session.query(session=db.session)
        .filter(Session.indexed_asset_id == indexed_asset_id)
        .one_or_none()
    )

    if not session:
        return StatusResponseModel(status="error", message="Session not found")

    if session.state in (SessionState.ANALYZING, SessionState.COMPLETED):
        return StatusResponseModel(status="success", message="Webhook already processed")

    if state in ("error", "failed"):
        session.state = SessionState.ERROR
        db.session.commit()
        return StatusResponseModel(status="error", message="Analysis failed")

    if state not in ("completed", "ready"):
        return StatusResponseModel(status="processing", message="Analysis still in progress")

    session.state = SessionState.ANALYZING
    db.session.flush()

    try:
        # Get question from SessionComponent
        question_text = session.session_components[0].question.question if session.session_components else None
        
        if not question_text:
            raise ValueError("No question found in session components")
        
        result = analyzer.generate_interview_analysis(
            video_id=indexed_asset_id,            
            question=question_text
        )

        data_string = result.data if hasattr(result, "data") else str(result)
        analysis_dict = json.loads(data_string)

        if "question_responses" in analysis_dict:
            for qr in analysis_dict["question_responses"]:

                default_template = (
                    Template.query(session=db.session)
                    .filter(Template.job_title == f"{session.user_id} Questions")
                    .one_or_none()
                )

                if not default_template:
                    default_template = Template.create(
                        session=db.session,
                        job_title=f"{session.user_id} Questions",
                        description=f"Questions submitted by {session.user_id} during video uploads"
                    )
                    db.session.flush()


                # Get question text from response
                response_question_text = qr.get("question", "")
                
                # Find matching SessionComponent by question text
                session_component = None
                for sc in session.session_components:
                    if sc.question.question == response_question_text:
                        session_component = sc
                        break
                
                # Skip if no matching component found
                if not session_component:
                    continue

                # Get or create Question record
                question = (
                    Question.query(session=db.session)
                    .filter(Question.question == response_question_text)
                    .one_or_none()
                )

                if not question:
                    question = Question.create(
                        session=db.session,
                        question=response_question_text,
                        template_id=default_template.id
                    )
                    db.session.flush()

                Grade.create(
                    session=db.session,
                    session_component_id=session_component.id,
                    body_language_score=qr.get("body_language_score", 0),
                    speech_score=qr.get("speech_score", 0),
                    brevity_score=qr.get("brevity_score", 0),
                    material_score=0
                )

                # Create Feedback
                # Note: DB has point (singular string) and ways_to_improve (string)
                # TwelveLabs returns points (array) and ways_to_improve (array)
                feedback_data = qr.get("feedback", {})
                points_list = feedback_data.get("points", [])
                ways_list = feedback_data.get("ways_to_improve", [])
                
                point_str = "\n".join(points_list) if points_list else ""
                ways_str = "\n".join(ways_list) if ways_list else None

                Feedback.create(
                    session=db.session,
                    session_component_id=session_component.id,
                    point=point_str,
                    ways_to_improve=ways_str
                )
                db.session.flush()

                index_id = analyzer.get_or_create_index(session.user_id, session=db.session)
                transcript_text = analyzer.get_video_transcript(
                    index_id=index_id,
                    video_id=indexed_asset_id
                )

                if transcript_text:
                    session_component.transcript = transcript_text
                    db.session.flush()

        session.state = SessionState.COMPLETED
        db.session.commit()

        return StatusResponseModel(status="success", message="Analysis completed successfully")

    except Exception as e:
        session.state = SessionState.ERROR
        db.session.commit()
        return StatusResponseModel(status="error", message="Analysis processing failed")


@video.get("/analysis/{session_id}")
async def get_video_analysis(
    session_id: int,
    user_session: UserSession = Depends(Auth())
):
    """Get video analysis state and results if ready."""
    
    session = Session.get(session_id, session=db.session)
    
    # Verify ownership
    if session.user_id != user_session.user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    question_response = None

    if session.session_components:
        session_component = session.session_components[0]

        if session_component.grade and session_component.feedback:
            # Parse feedback strings back to arrays
            points_list = session_component.feedback.point.split("\n") if session_component.feedback.point else []
            ways_list = session_component.feedback.ways_to_improve.split("\n") if session_component.feedback.ways_to_improve else []

            question_response = QuestionResponseModel(
                question=session_component.question.question,
                body_language_score=session_component.grade.body_language_score,
                speech_score=session_component.grade.speech_score,
                brevity_score=session_component.grade.brevity_score,
                feedback=FeedbackModel(
                    points=points_list,
                    ways_to_improve=ways_list
                )
            )

    if question_response is None or session.state != SessionState.COMPLETED:
        return StatusResponseModel(
            status=session.state.value,
            message=f"Analysis {session.state.value}. Data not yet available."
        )
    
    return VideoAnalysisStateResponse(
        status=session.state.value,
        session_id=session.id,
        analysis_data=question_response,
        error=None if session.state != SessionState.ERROR else "Analysis failed"
    )