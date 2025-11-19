import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi_sqlalchemy import db

from api.exceptions import AlreadyExists, AuthFailed, ObjectNotFound, RegistrationIncomplete
from api.models.db import User, UserSession
from api.schemas.base import StatusResponseModel
from api.schemas.models import (
    MyUserGet,
    RegistrationInitiate,
    RegistrationVerify,
    RegistrationVerifyCode,
    UserLogin,
    UserSessionGet,
    UserSessionsGet,
)
from api.settings import get_settings
from api.utils.enc import hash_password, validate_password
from api.utils.security import Auth
from api.utils.smtp import SendEmailMessage
from api.utils.token import random_int, random_string


settings = get_settings()

logger = logging.getLogger(__name__)
user = APIRouter(prefix="/user", tags=["User"])


@user.post("/registration/initiate", response_model=StatusResponseModel)
async def registration_initiate(
    request: Request, user_data: RegistrationInitiate, background_tasks: BackgroundTasks
) -> StatusResponseModel:
    verification_token: int = random_int()
    async with User.lock(db.session) as txn:
        user: User | None = User.query(session=txn).filter(User.email == user_data.email).one_or_none()
        if user:
            if user.password_hash:
                raise AlreadyExists(User, user_data.email)
            else:
                user.verification_token = verification_token
        else:
            user = User.create(session=txn, email=user_data.email, verification_token=verification_token)
        if settings.EMAIL:
            SendEmailMessage.send(
                user_data.email,
                request.client.host,
                "EmailRegConfirm.html",
                "Email Verification | WesternPrep",
                txn,
                background_tasks,
                token=verification_token,
                token_TTL=settings.VERIFICATION_TOKEN_TTL,
            )
            return StatusResponseModel(status="Success", message="Email verification token sent")
        else:
            return StatusResponseModel(status="Success", message=f"Email verification token: {verification_token}")


@user.get("/registration/code-verify", response_model=StatusResponseModel)
async def registration_verify_code(verification_token: int, email: str) -> StatusResponseModel:
    RegistrationVerifyCode(email=email, verification_token=verification_token)
    user: User | None = User.query(session=db.session).filter(User.email == email).one_or_none()
    if not user:
        raise AuthFailed("Incorrect or expired verification token")
    if (
        user.create_ts < datetime.now(tz=timezone.utc) - timedelta(minutes=settings.VERIFICATION_TOKEN_TTL)
        or user.verification_token != verification_token
    ):
        raise AuthFailed("Incorrect or expired verification token")

    return StatusResponseModel(status="Success", message="Email verified")


@user.put("/registration/verify", response_model=StatusResponseModel)
async def registration_verify(user_data: RegistrationVerify) -> StatusResponseModel:
    user: User = User.query(session=db.session).filter(User.email == user_data.email).one_or_none()
    if not user:
        raise ObjectNotFound(User, user_data.email)
    if user.password_hash:
        raise AlreadyExists(User, user.id)
    if (
        user.create_ts < datetime.now(tz=timezone.utc) - timedelta(minutes=settings.VERIFICATION_TOKEN_TTL)
        or user.verification_token != user_data.verification_token
    ):
        raise AuthFailed("Incorrect or expired verification token")
    salt = random_string()

    user.password_hash = hash_password(user_data.password, salt)
    user.salt = salt
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name

    db.session.commit()
    return StatusResponseModel(status="Success", message="Registration complete")


@user.post("/login", response_model=UserSessionGet)
async def login(user_data: UserLogin) -> UserSessionGet:
    user: User | None = User.query(session=db.session).filter(User.email == user_data.email).one_or_none()
    if user is None:
        raise AuthFailed("Incorrect login or password")
    if not user.password_hash:
        raise RegistrationIncomplete()
    if not validate_password(user_data.password, user.password_hash, user.salt):
        raise AuthFailed("Incorrect login or password")
    user_session = UserSession.create(session=db.session, user_id=user.id, token=random_string(settings.TOKEN_LENGTH))
    db.session.commit()
    return UserSessionGet(
        user_id=user_session.user_id,
        expires=user_session.expires,
        token=user_session.token,
    )


@user.get("", response_model=MyUserGet)
async def me(user_session: UserSession = Depends(Auth())) -> MyUserGet:
    return MyUserGet(
        id=user_session.user_id,
        email=user_session.user.email,
        first_name=user_session.user.first_name,
        last_name=user_session.user.last_name,
    )


@user.get("/sessions", response_model=UserSessionsGet)
async def get_sessions(user_session: UserSession = Depends(Auth())) -> UserSessionsGet:
    response = UserSessionsGet(sessions=[])
    for session in user_session.user.sessions:
        response.sessions.append(
            UserSessionGet(
                user_id=session.user_id,
                expires=session.expires,
                token=session.token,
            )
        )
    return UserSessionsGet.model_validate(response)


@user.delete("", response_model=StatusResponseModel)
async def delete_user(user_session: UserSession = Depends(Auth())) -> StatusResponseModel:
    User.delete(session=db.session, id=user_session.user_id)
    db.session.commit()
    return StatusResponseModel(status="Success", message="User deleted")
