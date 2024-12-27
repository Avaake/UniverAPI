from fastapi import Depends, status, HTTPException

from app.api.auth.dependencies import get_current_user_access_token
from app.core import User
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
