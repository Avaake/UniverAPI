from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.utis import verify_password
from app.api.auth.schemas import EmailSchema
from app.api.auth.dao import AuthDAO
from app.core import settings
from pydantic import EmailStr
from jose import jwt
import uuid


def create_jwt(token_type: str, token_data: dict, expires_delta: timedelta):
    to_encode = token_data.copy()
    now = datetime.now(timezone.utc)
    expire = now + expires_delta

    to_encode.update(
        token=token_type,
        exp=expire,
        iat=now,
        jwi=str(uuid.uuid4()),
    )
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.auth_jwt.secret_key,
        algorithm=settings.auth_jwt.algorithm,
    )
    return encoded_jwt


def create_access_token(data: dict) -> str:
    jwt_payload = data.copy()
    return create_jwt(
        token_type="access",
        token_data=jwt_payload,
        expires_delta=timedelta(days=settings.auth_jwt.access_token_expire_day),
    )


def create_refresh_token(data: dict) -> str:
    jwt_payload = data.copy()
    return create_jwt(
        token_type="refresh",
        token_data=jwt_payload,
        expires_delta=timedelta(days=settings.auth_jwt.refresh_token_expire_day),
    )


async def authenticate_user(email: EmailStr, password: str, session: AsyncSession):
    user = await AuthDAO.get_one_or_none(
        session=session, filters=EmailSchema(email=email)
    )
    if (
        not user
        or verify_password(plain_password=password, hashed_password=user.password)
        is False
    ):
        return None
    return user
