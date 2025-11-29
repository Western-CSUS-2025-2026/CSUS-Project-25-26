video.py

import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException

from api.exceptions import FailToConnectTwelveLabs, IndexCreatingFail, FailToCreateTask
from api.schemas.base import StatusResponseModel
from api.utils.security import Auth
from api.utils.twelveLabs import VideoAnalysis

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


@video.post("/analyze")
async def analyze_video(indexed_asset_id: str = None, question: str = None):
    analyzer = VideoAnalysis()

    try:
        result = analyzer.generate_interview_analysis(
            video_id=indexed_asset_id,
            question=question
        )
        return StatusResponseModel(
            status="Success",
            message=f"Video analyzed: {result.data if hasattr(result, 'data') else result}"
        )
        
    except FailToCreateTask as e:
        # Handle TwelveLabs API errors
        error_msg = str(e)
        if "video_file_broken" in error_msg or "Unable to process video file" in error_msg:
            raise HTTPException(
                status_code=400,
                detail="Video file is invalid or corrupted. Please check the file format and try again."
            )
        raise HTTPException(status_code=500, detail=f"Error processing video: {error_msg}")
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing video: {str(e)}"
        )

