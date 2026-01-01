from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware

from api import __version__
from api.settings import Settings, get_settings

from .session import session as session_router
from .template import template as templates_router
from .question import question as questions_router
from .user import user as user_router


settings: Settings = get_settings()
app = FastAPI(
    title='WesternPrep',
    version=__version__,
    root_path=settings.ROOT_PATH if __version__ != 'dev' else '/',
    docs_url='/' if __version__ != 'dev' else '/docs',
    redoc_url=None,
)

app.add_middleware(
    DBSessionMiddleware,
    db_url=str(settings.DB_DSN),
    engine_args={"pool_pre_ping": True},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

app.include_router(user_router)
app.include_router(session_router)
app.include_router(templates_router)
app.include_router(questions_router)
