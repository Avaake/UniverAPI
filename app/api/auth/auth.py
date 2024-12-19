from jose import jwt
from datetime import datetime, timedelta, timezone
from app.api.auth.utis import verify_password, get_password_hash
from app.core import settings
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.dao import AuthDAO
from app.api.auth.schemas import EmailSchema
from pydantic import EmailStr


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.auth_jwt.secret_key, algorithm=settings.auth_jwt.algorithm
    )
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str, session: AsyncSession):
    user = await AuthDAO.get_one_or_none(
        session=session, filters=EmailSchema(email=email)
    )
    if (
        not user
        or not verify_password(
            plain_password=password,
            hashed_password=get_password_hash(password=password),
        )
        is False
    ):
        return None
    return user
