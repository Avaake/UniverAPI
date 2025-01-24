from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel


async def get_or_404(
    dao,
    session: AsyncSession,
    data_id: int,
    detail: str,
):
    obj = await dao.get_one_or_none_by_id(session=session, data_id=data_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
    return obj


async def get_or_409(
    dao,
    session: AsyncSession,
    filters: dict | BaseModel,
    detail: str,
):
    obj = await dao.get_one_or_none(session=session, filters=filters)
    if obj:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )
    return obj
