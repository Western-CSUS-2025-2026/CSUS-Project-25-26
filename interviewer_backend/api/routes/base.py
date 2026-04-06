from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from api import __version__
from api.settings import Settings, get_settings

from .question import question as question_router
from .roles import router as roles_router
from .session import session as session_router
from .template import template as template_router
from .user import user as user_router
from .video import video as video_router


settings: Settings = get_settings()
app = FastAPI(
    title='Jobless.live',
    version=__version__,
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '/',
    docs_url='/' if __version__ != 'dev' else '/docs',
    redoc_url=None,
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={
        "pool_pre_ping": True,
        "pool_size": settings.DB_POOL_SIZE,
        "max_overflow": settings.DB_POOL_MAX_OVERFLOW,
        "pool_timeout": settings.DB_POOL_TIMEOUT_SECONDS,
        "pool_recycle": settings.DB_POOL_RECYCLE_SECONDS,
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_origin_regex=settings.CORS_ALLOW_ORIGIN_REGEX,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(user_router)
app.include_router(roles_router)
app.include_router(video_router)
app.include_router(session_router)
app.include_router(template_router)
app.include_router(question_router)

if settings.METRICS_ENABLED:
    Instrumentator(excluded_handlers=['/metrics']).instrument(app).expose(
        app,
        endpoint='/metrics',
        include_in_schema=False,
    )
