from fastapi import Request, status, HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.auth.dao import AuthDAO
from app.core import db_helper, settings, User
from typing import Annotated


def get_token(request: Request):
    token = request.headers.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return token


async def get_current_user(
    token: Annotated[str, Depends(get_token)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    try:
        payload = jwt.decode(
            token,
            settings.auth_jwt.secret_key,
            algorithms=[settings.auth_jwt.algorithm],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token not found",
        )

    expire = payload.get("exp")
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is expired",
        )

    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid",
        )

    user = await AuthDAO.get_one_or_none_by_id(data_id=int(user_id), session=session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User does not exist",
        )
    return user


async def get_current_admin_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.role.name in ["admin", "super_admin"]:
        return current_user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You do not have permission to perform this action",
    )
