import json
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException

from api.exceptions import FailToConnectTwelveLabs, IndexCreatingFail, FailToCreateTask
from api.schemas.base import StatusResponseModel
from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis
from api.schemas.models import VideoAnalysisResponseModel, AnalysisResult
from pydantic import ValidationError

video = APIRouter(prefix="/video", tags=["Video"])

@video.post("/index/create", response_model=StatusResponseModel)
async def create_index(index_name: str = None) -> StatusResponseModel:
    analyzer = VideoAnalysis()
    index = analyzer.create_index(index_name)
    return StatusResponseModel(
        status="success",
        message=f"Index created: {index.id}"
    )


@video.get("/list_indexes", response_model=StatusResponseModel)
async def list_indexes():
    analyzer = VideoAnalysis()
    indexes = analyzer.list_indexes()
    return StatusResponseModel(
        status="Success",
        message=f"Indexes listed: {str(indexes)}"
    )


@video.post("/upload_video", response_model=StatusResponseModel)
async def upload_video(video: UploadFile = File(...)):
    analyzer = VideoAnalysis()
    asset = analyzer.upload_asset(file=video)
    return StatusResponseModel(
        status="Success",
        message=f"Video uploaded: {asset.id}"
    )


@video.post("/index_video", response_model=StatusResponseModel)
async def index_video(asset_id: str, index_id: str):
    analyzer = VideoAnalysis()
    indexed_asset = analyzer.index_asset(index_id=index_id, asset_id=asset_id)
    return StatusResponseModel(
        status="Success",
        message=f"Video indexed: {indexed_asset.id}"
    )


@video.get("/list_indexed_assets", response_model=StatusResponseModel)
async def list_indexed_assets(index_id: str):
    analyzer = VideoAnalysis()
    indexed_assets = analyzer.list_indexed_assets(index_id=index_id)
    return StatusResponseModel(
        status="Success",
        message=f"Indexed assets listed: {str(indexed_assets)}"
    )


@video.post("/analyze", response_model=VideoAnalysisResponseModel)
async def analyze_video(indexed_asset_id: str = Form(...),question: str = Form(...)) -> VideoAnalysisResponseModel:
    analyzer = VideoAnalysis()

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

