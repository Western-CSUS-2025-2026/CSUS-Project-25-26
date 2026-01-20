import starlette.requests
from starlette.responses import JSONResponse

from api.exceptions import (
    AlreadyExists,
    AnalysisFailed,
    AuthFailed,
    ForbiddenAction,
    ObjectNotFound,
    RegistrationIncomplete,
    TooManyEmailRequests,
    VideoProcessingFailed,
)
from api.schemas.base import StatusResponseModel

from .base import app


@app.exception_handler(ObjectNotFound)
async def not_found_handler(req: starlette.requests.Request, exc: ObjectNotFound):
    return JSONResponse(content=StatusResponseModel(status="Error", message=exc.msg).model_dump(), status_code=404)


@app.exception_handler(AlreadyExists)
async def already_exists_handler(req: starlette.requests.Request, exc: AlreadyExists):
    return JSONResponse(content=StatusResponseModel(status="Error", message=exc.msg).model_dump(), status_code=409)


@app.exception_handler(ForbiddenAction)
async def forbidden_action_handler(req: starlette.requests.Request, exc: ForbiddenAction):
    return JSONResponse(content=StatusResponseModel(status="Error", message=exc.msg).model_dump(), status_code=403)


@app.exception_handler(TooManyEmailRequests)
async def too_many_requests_handler(req: starlette.requests.Request, exc: TooManyEmailRequests):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=429,
    )


@app.exception_handler(AuthFailed)
async def auth_failed_handler(req: starlette.requests.Request, exc: AuthFailed):
    return JSONResponse(content=StatusResponseModel(status="Error", message=exc.msg).model_dump(), status_code=401)


@app.exception_handler(RegistrationIncomplete)
async def registration_incomplete_handler(req: starlette.requests.Request, exc: RegistrationIncomplete):
    return JSONResponse(
        StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=403,
    )


@app.exception_handler(VideoProcessingFailed)
async def video_processing_failed_handler(req: starlette.requests.Request, exc: VideoProcessingFailed):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=422,
    )


@app.exception_handler(AnalysisFailed)
async def analysis_failed_handler(req: starlette.requests.Request, exc: AnalysisFailed):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=422,
    )


@app.exception_handler(Exception)
async def http_error_handler(req: starlette.requests.Request, exc: Exception):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message="Internal server error").model_dump(),
        status_code=500,
    )
