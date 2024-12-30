from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.core import db_helper, Speciality
from app.api.speciality.dao import SpecialityDAO


async def check_speciality_by_id(
    speciality_id: int, session: Annotated[AsyncSession, Depends(db_helper.transaction)]
) -> Speciality:
    speciality = await SpecialityDAO.get_one_or_none_by_id(
        session=session, data_id=speciality_id
    )
    if speciality is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Speciality not found"
        )
    return speciality
