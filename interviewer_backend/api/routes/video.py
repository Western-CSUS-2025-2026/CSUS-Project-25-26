import json

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi import Request
from fastapi_sqlalchemy import db


from api.exceptions import FailToCreateTask
from api.schemas.base import StatusResponseModel
from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis
from api.schemas.models import VideoAnalysisResponseModel, AnalysisResult, VideoUploadResponse
from api.models.db import SessionState, Session, UserSession
from pydantic import ValidationError


video = APIRouter(prefix="/video", tags=["Video"])
analyzer = VideoAnalysis()


########
@video.get("/list_indexes", response_model=StatusResponseModel)
async def list_indexes():
    analyzer = VideoAnalysis()
    indexes = analyzer.list_indexes()
    return StatusResponseModel( 
        status="Success",
        message=f"Indexes listed: {str(indexes)}"
    )


@video.get("/list_indexed_assets", response_model=StatusResponseModel)
async def list_indexed_assets(index_id: str):
    analyzer = VideoAnalysis()
    indexed_assets = analyzer.list_indexed_assets(index_id=index_id)
    return StatusResponseModel(
        status="Success",
        message=f"Indexed assets listed: {str(indexed_assets)}"
    )
##For development



@video.post("/upload_video", status_code=202)
async def upload_video(video: UploadFile = File(...), 
    user_session: UserSession = Depends(Auth()),
    question: str = Form(...)):
    
    index_id = analyzer.get_or_create_index(user_session.user_id, session=db.session)
    
    asset = analyzer.upload_asset(file=video)

    indexed_asset = analyzer.index_asset(index_id=index_id, asset_id=asset.id)

    session = Session.create(
        session=db.session,
        user_id=user_session.user_id,
        indexed_asset_id=indexed_asset.id,
        question=question,
        state=SessionState.PENDING,
        video_url=None #TODO
    )
    db.session.commit()
    
    return VideoUploadResponse(
        asset_id=asset.id,
        session_id=session.id
    )


@video.post("/webhook/twelvelabs")
async def twelvelabs_webhook(request: Request):

    data = await request.json()

    indexed_asset_id = data.get("indexed_asset_id")




@video.post("/analyze", response_model=VideoAnalysisResponseModel)
async def analyze_video(indexed_asset_id: str = Form(...),question: str = Form(...)) -> VideoAnalysisResponseModel:

    try:
        # Get raw analysis result from TwelveLabs
        result = analyzer.generate_interview_analysis(
            video_id=indexed_asset_id,
            question=question
        )

        data_string = result.data if hasattr(result, 'data') else result

        try:
            analysis_dict = json.loads(data_string)
        except json.JSONDecodeError as e:
            # Handle cases where the analysis service returns bad/empty data
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: Service returned invalid data. Details: {e}"
            )

        
        try:
            analysis_data = AnalysisResult(**analysis_dict)
        except ValidationError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: Data structure mismatch. Expected fields: confidence, clarity, speech_rate, eye_contact, body_language, voice_tone, relevant_to_question, imp_points, overall_summary, actionable_feedback. Details: {str(e)}"
            )

        return VideoAnalysisResponseModel(
            status="Success",
            analysis_data=analysis_data
        )
        
    except FailToCreateTask as e:
        # Handle specific errors from the TwelveLabs API wrapper
        raise HTTPException(status_code=500, detail=f"TwelveLabs API Error: {str(e)}")
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing video: {str(e)}"
        )
