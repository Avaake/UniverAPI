from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.roles.dao import RoleDAO
from app.core import Role, db_helper
from typing import Annotated


async def check_role_by_id(
    role_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> Role:
    group = await RoleDAO.get_one_or_none_by_id(session=session, data_id=role_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return group
