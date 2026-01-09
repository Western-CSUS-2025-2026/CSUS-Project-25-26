import json
import traceback

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi import Request
from fastapi_sqlalchemy import db


from api.exceptions import FailToCreateTask
from api.schemas.base import StatusResponseModel
from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis
from api.schemas.models import VideoAnalysisStateResponse, AnalysisResult, VideoUploadResponse, TwelveLabsWebhookRequest
from api.schemas.models import TwelveLabsAnalysisModel
from api.models.db import SessionState, Session, UserSession, Question, SessionComponent, Feedback, Grade, Template
from pydantic import ValidationError


video = APIRouter(prefix="/video", tags=["Video"])
analyzer = VideoAnalysis()


@video.post("/upload_video", status_code=202)
async def upload_video(video: UploadFile = File(...), 
    user_session: UserSession = Depends(Auth()),
    question: str = Form(...)):
    
    index_id = analyzer.get_or_create_index(user_session.user_id, session=db.session)
    
    asset = analyzer.upload_asset(file=video)

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
        .filter(Question.question == question)
        .one_or_none()
    )

    if not question_record:
        question_record = Question.create(
            session=db.session,
            question=question,
            template_id=default_template.id
        )
        db.session.flush()

    session = Session.create(
        session=db.session,
        user_id=user_session.user_id,
        indexed_asset_id=None,
        question=question,
        state=SessionState.PENDING
    )
    db.session.flush()

    indexed_asset = analyzer.index_asset(index_id=index_id, asset_id=asset.id)
    session.indexed_asset_id = indexed_asset.id
    session.state = SessionState.INDEXING
    db.session.commit()
    
    return VideoUploadResponse(
        asset_id=asset.id,
        indexed_asset_id=indexed_asset.id,
        session_id=session.id,
        question=question,
        state=session.state.value
    )


@video.post("/webhook/twelvelabs")
async def twelvelabs_webhook(payload: TwelveLabsWebhookRequest):
    indexed_asset_id = payload.indexed_asset_id or payload.id
    state = (payload.state or payload.status or "").lower()

    # always return 200 even if malformed, but log server-side
    if not indexed_asset_id:
        print(f"[webhook] ERROR: Missing indexed_asset_id in payload: {payload}")
        return {"ok": True, "message": "missing id", "received_payload": payload.dict()}

    session = (
        Session.query(session=db.session)
        .filter(Session.indexed_asset_id == indexed_asset_id)
        .one_or_none()
    )

    if not session:
        return {"ok": True, "message": "no session", "indexed_asset_id": indexed_asset_id}

    # idempotency
    if session.state in (SessionState.ANALYZING, SessionState.COMPLETED):
        return {"ok": True, "message": "already handled", "session_id": session.id, "current_state": session.state.value}

    if state in ("error", "failed"):
        session.state = SessionState.ERROR
        db.session.commit()
        return {"ok": True, "message": "error state handled", "session_id": session.id, "state": "error"}

    if state not in ("completed", "ready"):
        return {"ok": True, "message": "still processing", "state": state, "session_id": session.id}

    session.state = SessionState.ANALYZING
    db.session.flush()

    try:
        result = analyzer.generate_interview_analysis(
            video_id=indexed_asset_id,            
            questions=[session.question]     
        )

        data_string = result.data if hasattr(result, "data") else str(result)
        analysis_dict = json.loads(data_string)

        # Store raw JSON
        session.analysis_data = json.dumps(analysis_dict)

        print(f"[webhook] SUCCESS: Analysis completed for session_id: {session.id}")

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


                # Get or create Question record
                question_text = qr.get("question", "")
                question = (
                    Question.query(session=db.session)
                    .filter(Question.question == question_text)
                    .one_or_none()
                )

                if not question:
                    question = Question.create(
                        session=db.session,
                        question=question_text,
                        template_id=default_template.id
                    )
                    db.session.flush()
                    print(f"[webhook] Created question: {question.id}")

                # Create SessionComponent
                session_component = SessionComponent.create(
                    session=db.session,
                    session_id=session.id,
                    question_id=question.id,
                    transcript=None
                )
                db.session.flush()

                Grade.create(
                    session=db.session,
                    session_component_id=session_component.id,
                    body_language_score=qr.get("body_language_score", 0),
                    speech_score=qr.get("speech_score", 0),
                    brevity_score=qr.get("brevity_score", 0)
                )

                # Create Feedback
                # Note: DB has point (singular string) and ways_to_improve (string)
                # TwelveLabs returns points (array) and ways_to_improve (array)
                feedback_data = qr.get("feedback", {})
                points_list = feedback_data.get("points", [])
                ways_list = feedback_data.get("ways_to_improve", [])
                
                # Join arrays into strings (adjust separator as needed)
                point_str = "\n".join(points_list) if points_list else ""
                ways_str = "\n".join(ways_list) if ways_list else None

                Feedback.create(
                    session=db.session,
                    session_component_id=session_component.id,
                    point=point_str,
                    ways_to_improve=ways_str
                )
                db.session.flush()

        session.state = SessionState.COMPLETED
        db.session.commit()

        return {
            "message": "analysis completed",
            "session_id": session.id,
            "state": "completed",
            "analysis_keys": list(analysis_dict.keys()) if isinstance(analysis_dict, dict) else None
        }

    except Exception as e:
        session.state = SessionState.ERROR
        db.session.commit()
        return {"message": "error occurred", "error": str(e), "session_id": session.id}


@video.get("/analysis/{session_id}", response_model=VideoAnalysisStateResponse)
async def get_video_analysis(
    session_id: int,
    user_session: UserSession = Depends(Auth())
):
    """Get video analysis state and results if ready."""
    
    session = Session.get(session_id, session=db.session)
    
    # Verify ownership
    if session.user_id != user_session.user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Parse analysis data if available
    analysis_data = None
    if session.analysis_data:
        try:
            analysis_dict = json.loads(session.analysis_data)
            # Check if it's new format (question_responses) or old format
            if "question_responses" in analysis_dict:
                filtered_responses = []
                for response in analysis_dict["question_responses"]:
                    filtered_response = {
                        "question": response.get("question"),
                        "body_language_score": response.get("body_language_score"),
                        "speech_score": response.get("speech_score"),
                        "brevity_score": response.get("brevity_score"),
                        "feedback": {
                            "points": response.get("feedback", {}).get("points", []),
                            "ways_to_improve": response.get("feedback", {}).get("ways_to_improve", [])
                        },
                        "improved_answer": {  # Add this
                            "version": response.get("improved_answer", {}).get("version", "")
                        }
                    }
                    filtered_responses.append(filtered_response)
                
                filtered_dict = {"question_responses": filtered_responses}
                analysis_data = TwelveLabsAnalysisModel(**filtered_dict)
            else:
                # Old format - try to parse as AnalysisResult
                analysis_data = AnalysisResult(**analysis_dict)
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"[get_video_analysis] Error parsing analysis data: {e}")
            analysis_data = None
    
    # Determine status message
    status = "success" if session.state == SessionState.COMPLETED else "processing"
    if session.state == SessionState.ERROR:
        status = "error"
    
    return VideoAnalysisStateResponse(
        status=status,
        session_id=session.id,
        analysis_data=analysis_data,
        error=None if session.state != SessionState.ERROR else "Analysis failed"
    )