from app.api.auth.dependencies import get_current_user_access_token
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.users.dao import UserDAO
from app.core import User, db_helper
from typing import Annotated


async def check_access_to_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user_access_token)],
):
    if (current_user.id != user_id) and (current_user.role.name != "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the administrator or the user can change this data.",
        )
    return current_user


async def check_user_by_id(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> User:
    group = await UserDAO.get_one_or_none_by_id(session=session, data_id=user_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return group
