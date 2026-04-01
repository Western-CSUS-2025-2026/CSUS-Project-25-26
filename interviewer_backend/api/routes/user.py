import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Request, Response
from fastapi_sqlalchemy import db

from api.exceptions import AlreadyExists, AuthFailed, ObjectNotFound, RegistrationIncomplete
from api.models.db import RefreshSession, User
from api.models.role import Role, UserRole
from api.schemas.base import StatusResponseModel
from api.schemas.models import (
    AuthLoginResponse,
    AuthRefreshResponse,
    LogoutRequest,
    MyUserGet,
    RefreshRequest,
    RegistrationInitiate,
    RegistrationVerify,
    RegistrationVerifyCode,
    UserLogin,
)
from api.settings import get_settings
from api.utils.enc import hash_password, validate_password
from api.utils.jwt_auth import (
    create_access_token,
    generate_refresh_token,
    get_access_token_expires_in,
    get_refresh_token_expire_date,
    get_refresh_token_expires_in,
    hash_refresh_token,
)
from api.utils.security import Auth, CsrfProtect, JwtAuthUser, generate_csrf_token
from api.utils.smtp import SendEmailMessage
from api.utils.token import random_int, random_string


settings = get_settings()

logger = logging.getLogger(__name__)
user = APIRouter(prefix="/user", tags=["User"])


def _issue_refresh_session(user_id: int, now: datetime) -> tuple[str, datetime]:
    refresh_token = generate_refresh_token()
    refresh_expires_at = get_refresh_token_expire_date(now)
    RefreshSession.create(
        session=db.session,
        user_id=user_id,
        token_hash=hash_refresh_token(refresh_token),
        expires_at=refresh_expires_at,
        create_ts=now,
    )
    return refresh_token, refresh_expires_at


def _set_auth_cookies(
    response: Response,
    *,
    access_token: str,
    refresh_token: str,
    refresh_expires_at: datetime,
) -> None:
    csrf_token = generate_csrf_token()
    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        max_age=get_access_token_expires_in(),
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        value=refresh_token,
        max_age=get_refresh_token_expires_in(),
        expires=refresh_expires_at,
        httponly=True,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path=settings.REFRESH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    response.set_cookie(
        key=settings.CSRF_COOKIE_NAME,
        value=csrf_token,
        max_age=get_refresh_token_expires_in(),
        expires=refresh_expires_at,
        httponly=False,
        secure=settings.AUTH_COOKIE_SECURE,
        samesite=settings.AUTH_COOKIE_SAMESITE,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )


def _clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        key=settings.ACCESS_TOKEN_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    response.delete_cookie(
        key=settings.REFRESH_TOKEN_COOKIE_NAME,
        path=settings.REFRESH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )
    if settings.REFRESH_COOKIE_PATH != settings.AUTH_COOKIE_PATH:
        response.delete_cookie(
            key=settings.REFRESH_TOKEN_COOKIE_NAME,
            path=settings.AUTH_COOKIE_PATH,
            domain=settings.AUTH_COOKIE_DOMAIN,
        )
    response.delete_cookie(
        key=settings.CSRF_COOKIE_NAME,
        path=settings.AUTH_COOKIE_PATH,
        domain=settings.AUTH_COOKIE_DOMAIN,
    )


def _fetch_user_role_names(user_id: int) -> list[str]:
    rows = (
        db.session.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return [row.name for row in rows]


def _get_refresh_token(payload: RefreshRequest | LogoutRequest | None, request: Request) -> str | None:
    if payload and payload.refresh_token:
        return payload.refresh_token
    token = request.cookies.get(settings.REFRESH_TOKEN_COOKIE_NAME)
    if token:
        return token
    return None


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
            client_ip = request.client.host
            SendEmailMessage.send(
                user_data.email,
                client_ip,
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
        db.session.rollback()
        raise AuthFailed("Incorrect or expired verification token")
    if (
        user.create_ts < datetime.now(tz=timezone.utc) - timedelta(minutes=settings.VERIFICATION_TOKEN_TTL)
        or user.verification_token != verification_token
    ):
        db.session.rollback()
        raise AuthFailed("Incorrect or expired verification token")

    response = StatusResponseModel(status="Success", message="Email verified")
    db.session.rollback()
    return response


@user.put("/registration/verify", response_model=StatusResponseModel)
async def registration_verify(user_data: RegistrationVerify) -> StatusResponseModel:
    salt = random_string()
    password_hash = hash_password(user_data.password, salt)

    user: User = User.query(session=db.session).filter(User.email == user_data.email).one_or_none()
    if not user:
        db.session.rollback()
        raise ObjectNotFound(User, user_data.email)
    if user.password_hash:
        db.session.rollback()
        raise AlreadyExists(User, user.id)
    if (
        user.create_ts < datetime.now(tz=timezone.utc) - timedelta(minutes=settings.VERIFICATION_TOKEN_TTL)
        or user.verification_token != user_data.verification_token
    ):
        db.session.rollback()
        raise AuthFailed("Incorrect or expired verification token")

    user.password_hash = password_hash
    user.salt = salt
    user.first_name = user_data.first_name
    user.last_name = user_data.last_name

    db.session.commit()
    return StatusResponseModel(status="Success", message="Registration complete")


@user.post("/login", response_model=AuthLoginResponse)
async def login(user_data: UserLogin, response: Response) -> AuthLoginResponse:
    user: User | None = User.query(session=db.session).filter(User.email == user_data.email).one_or_none()
    if user is None:
        db.session.rollback()
        raise AuthFailed("Incorrect login or password")

    user_id = user.id
    password_hash = user.password_hash
    salt = user.salt

    # Close the read transaction before expensive password verification.
    db.session.rollback()

    if not password_hash:
        raise RegistrationIncomplete()
    if not validate_password(user_data.password, password_hash, salt):
        raise AuthFailed("Incorrect login or password")

    now = datetime.now(tz=timezone.utc)
    role_names = _fetch_user_role_names(user_id)
    access_token = create_access_token(user_id, now=now, roles=role_names)
    refresh_token, refresh_expires_at = _issue_refresh_session(user_id, now)
    _set_auth_cookies(
        response,
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
    )
    db.session.commit()
    return AuthLoginResponse(
        user_id=user_id,
        access_token=access_token,
        token_type="Bearer",
        expires_in=get_access_token_expires_in(),
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
    )


@user.post("/refresh", response_model=AuthRefreshResponse)
async def refresh(
    request: Request,
    response: Response,
    payload: RefreshRequest | None = Body(default=None),
    _: None = Depends(CsrfProtect()),
) -> AuthRefreshResponse:
    refresh_token_raw = _get_refresh_token(payload, request)
    if not refresh_token_raw:
        raise AuthFailed("Not authorized")

    now = datetime.now(tz=timezone.utc)
    token_hash = hash_refresh_token(refresh_token_raw)
    refresh_session: RefreshSession | None = (
        RefreshSession.query(session=db.session)
        .filter(RefreshSession.token_hash == token_hash)
        .with_for_update()
        .one_or_none()
    )
    if not refresh_session or refresh_session.revoked_at is not None or refresh_session.expires_at <= now:
        db.session.rollback()
        raise AuthFailed("Not authorized")

    refresh_session.revoked_at = now
    role_names = _fetch_user_role_names(refresh_session.user_id)
    access_token = create_access_token(refresh_session.user_id, now=now, roles=role_names)
    refresh_token, refresh_expires_at = _issue_refresh_session(refresh_session.user_id, now)
    _set_auth_cookies(
        response,
        access_token=access_token,
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
    )
    db.session.commit()

    return AuthRefreshResponse(
        access_token=access_token,
        token_type="Bearer",
        expires_in=get_access_token_expires_in(),
        refresh_token=refresh_token,
        refresh_expires_at=refresh_expires_at,
    )


@user.post("/logout", response_model=StatusResponseModel)
async def logout(
    request: Request,
    response: Response,
    payload: LogoutRequest | None = Body(default=None),
    _: None = Depends(CsrfProtect()),
) -> StatusResponseModel:
    now = datetime.now(tz=timezone.utc)
    refresh_token_raw = _get_refresh_token(payload, request)
    if refresh_token_raw:
        token_hash = hash_refresh_token(refresh_token_raw)
        refresh_session: RefreshSession | None = (
            RefreshSession.query(session=db.session).filter(RefreshSession.token_hash == token_hash).one_or_none()
        )
        if refresh_session and refresh_session.revoked_at is None:
            refresh_session.revoked_at = now
            db.session.commit()
        else:
            db.session.rollback()
    else:
        db.session.rollback()
    _clear_auth_cookies(response)
    return StatusResponseModel(status="Success", message="Logged out")


@user.get("", response_model=MyUserGet)
async def me(current_user: JwtAuthUser = Depends(Auth())) -> MyUserGet:
    user_obj: User | None = User.query(session=db.session).filter(User.id == current_user.user_id).one_or_none()
    if not user_obj:
        db.session.rollback()
        raise AuthFailed("Not authorized")
    response = MyUserGet(
        id=user_obj.id,
        email=user_obj.email,
        first_name=user_obj.first_name,
        last_name=user_obj.last_name,
    )
    db.session.rollback()
    return response


@user.delete("", response_model=StatusResponseModel)
async def delete_user(
    _: None = Depends(CsrfProtect()),
    current_user: JwtAuthUser = Depends(Auth()),
) -> StatusResponseModel:
    User.delete(session=db.session, id=current_user.user_id)
    db.session.commit()
    return StatusResponseModel(status="Success", message="User deleted")
