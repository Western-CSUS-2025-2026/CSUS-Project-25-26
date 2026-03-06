import starlette.requests
from starlette.responses import JSONResponse

from api.exceptions import (
    AlreadyExists,
    AuthFailed,
    FailToConnectTwelveLabs,
    FailToCreateTask,
    FailToParseAnalysis,
    ForbiddenAction,
    IndexCreatingFail,
    ObjectNotFound,
    RegistrationIncomplete,
    TooManyEmailRequests,
    RateLimitExceeded,
    WebhookVerificationFailed,
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


@app.exception_handler(Exception)
async def http_error_handler(req: starlette.requests.Request, exc: Exception):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message="Internal server error").model_dump(),
        status_code=500,
    )


@app.exception_handler(FailToConnectTwelveLabs)
async def fail_to_connect_twelvelabs_handler(req: starlette.requests.Request, exc: FailToConnectTwelveLabs):
    return JSONResponse(content=StatusResponseModel(status="Error", message=exc.msg).model_dump(), status_code=503)


@app.exception_handler(IndexCreatingFail)
async def index_creating_fail_handler(req: starlette.requests.Request, exc: IndexCreatingFail):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=500,
    )


@app.exception_handler(FailToCreateTask)
async def fail_to_create_task_handler(req: starlette.requests.Request, exc: FailToCreateTask):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=500,
    )


@app.exception_handler(FailToCreateTask)
async def fail_to_parse_analysis_handler(req: starlette.requests.Request, exc: FailToParseAnalysis):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=500,
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(req: starlette.requests.Request, exc: RateLimitExceeded):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=429,
    )


@app.exception_handler(WebhookVerificationFailed)
async def webhook_verification_failed_handler(req: starlette.requests.Request, exc: WebhookVerificationFailed):
    return JSONResponse(
        content=StatusResponseModel(status="Error", message=exc.msg).model_dump(),
        status_code=400,
    )