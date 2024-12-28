from fastapi import Depends, status, HTTPException

from app.core import Group, db_helper
from typing import Annotated
from app.api.groups.dao import GroupDAO
from sqlalchemy.ext.asyncio import AsyncSession


async def check_group_by_id(
    group_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> Group:
    group = await GroupDAO.get_one_or_none_by_id(session=session, data_id=group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )
    return group
