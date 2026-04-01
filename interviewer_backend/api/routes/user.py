import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi_sqlalchemy import db

from api.exceptions import AlreadyExists, AuthFailed, ObjectNotFound, RegistrationIncomplete
from api.models.db import User, UserSession
from api.models.role import Role, UserRole
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
from api.utils.security import JwtAuthUser, mint_access_token
from api.utils.smtp import SendEmailMessage
from api.utils.token import random_int, random_string
from api.dependencies.auth import require_roles


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
                if user.create_ts > datetime.now(tz=timezone.utc) - timedelta(minutes=settings.VERIFICATION_TOKEN_TTL):
                    raise AlreadyExists(User, user_data.email)
                user.verification_token = verification_token
                user.create_ts = datetime.now(tz=timezone.utc)
        else:
            user = User.create(
                session=txn,
                email=user_data.email,
                verification_token=verification_token,
                create_ts=datetime.now(tz=timezone.utc),
            )
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
    role_rows = (
        db.session.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user.id)
        .all()
    )
    role_names = [row.name for row in role_rows]
    token, expires = mint_access_token(user.id, role_names)
    return UserSessionGet(
        user_id=user.id,
        expires=expires,
        token=token,
    )


@user.get("", response_model=MyUserGet)
async def me(auth_user: JwtAuthUser = Depends(require_roles(["admin", "interviewer"]))) -> MyUserGet:
    db_user: User | None = User.query(session=db.session).filter(User.id == auth_user.user_id).one_or_none()
    if not db_user:
        raise ObjectNotFound(User, auth_user.user_id)
    return MyUserGet(
        id=db_user.id,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
    )


@user.get("/sessions", response_model=UserSessionsGet)
async def get_sessions(auth_user: JwtAuthUser = Depends(require_roles(["admin", "interviewer"]))) -> UserSessionsGet:
    db_user: User | None = User.query(session=db.session).filter(User.id == auth_user.user_id).one_or_none()
    if not db_user:
        raise ObjectNotFound(User, auth_user.user_id)
    response = UserSessionsGet(sessions=[])
    for legacy_session in db_user.user_sessions:
        response.sessions.append(
            UserSessionGet(
                user_id=legacy_session.user_id,
                expires=legacy_session.expires,
                token=legacy_session.token,
            )
        )
    return UserSessionsGet.model_validate(response)


@user.delete("", response_model=StatusResponseModel)
async def delete_user(
    auth_user: JwtAuthUser = Depends(require_roles(["admin", "interviewer"]))
) -> StatusResponseModel:
    User.delete(session=db.session, id=auth_user.user_id)
    db.session.commit()
    return StatusResponseModel(status="Success", message="User deleted")
