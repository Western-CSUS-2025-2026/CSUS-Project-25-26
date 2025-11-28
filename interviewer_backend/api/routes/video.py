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


@video.post("/upload_url", response_model=StatusResponseModel)
async def upload_video(
    video_url: str,
    index_id: str = None,
    user_session = Depends(Auth())
) -> StatusResponseModel:
    """Upload and index a video"""
    analyzer = VideoAnalysis()
    task = analyzer.create_task(video_url=video_url, index_id=index_id)
    
    # Wait for task to complete
    completed_task = analyzer.wait_for_task(task_id=task.id)
    
    return StatusResponseModel(
        status="Success",
        message=f"Video uploaded and indexed. Video ID: {completed_task.video_id}"
    )


@video.post("/analyze")
async def analyze_video(video: UploadFile = File(...), question: str = Form(...), index_id: str = None):
    analyzer = VideoAnalysis()
    video_path = None

    try:
        os.makedirs("uploads", exist_ok=True)
        video_path = os.path.join("uploads", video.filename)

        with open(video_path, "wb") as f:
            content = await video.read()
            f.write(content)

        if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
            raise HTTPException(
                status_code=400,
                detail="Failed to save video file or file is empty"
            )

        with open(video_path, 'rb') as video_file:
            task = analyzer.client.tasks.create(
                index_id=index_id or analyzer.index_id,
                file=video_file
            )
            
        completed_task = analyzer.wait_for_task(task, sleep_interval=5)

        result = analyzer.generate_interview_analysis(
            video_id=completed_task.video_id,
            question=question
        )

        return {
            "video_id": completed_task.video_id,
            "analysis": result.data if hasattr(result, 'data') else result
        }
        
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
    finally:
        # Clean up temp file
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
            except:
                pass