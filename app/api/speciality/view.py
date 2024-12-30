from fastapi import APIRouter, HTTPException, Path, Depends, status
from app.api.speciality.schemas import (
    SpecialityReadSchema,
    SpecialityBaseSchema,
    SpecialityUpdateSchema,
)
from app.api.speciality.dao import SpecialityDAO
from typing import Annotated
from app.core import db_helper, settings, Speciality
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.speciality.dependencies import check_speciality_by_id

router = APIRouter(prefix=settings.api_prefix.specialities, tags=["Speciality"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_speciality(
    speciality_data: SpecialityBaseSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    check_speciality = await SpecialityDAO.get_one_or_none(
        session=session, filters={"name": speciality_data.name}
    )
    if check_speciality:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Group already exists",
        )
    speciality = await SpecialityDAO.add(session, values=speciality_data)
    return {"message": "Speciality created", "speciality": speciality}


@router.get("/{speciality_id}", status_code=status.HTTP_200_OK)
async def get_speciality_by_id(
    speciality_id: Annotated[int, Path(ge=0)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_speciality: Annotated[Speciality, Depends(check_speciality_by_id)],
):
    # return create_speciality
    return {"speciality": SpecialityReadSchema(**check_speciality.to_dict())}


@router.patch("{speciality_id}", status_code=status.HTTP_200_OK)
async def update_speciality(
    speciality_id: Annotated[int, Path(ge=0)],
    speciality_data: SpecialityUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_speciality: Annotated[Speciality, Depends(check_speciality_by_id)],
):
    speciality = await SpecialityDAO.update(
        session=session, values=speciality_data, filters={"id": speciality_id}
    )

    if speciality:
        return {
            "message": "Speciality updated",
            "speciality": SpecialityReadSchema(**speciality.to_dict()),
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update user role. Please try again later.",
    )


@router.delete("/{speciality_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speciality(
    speciality_id: Annotated[int, Path(ge=0)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_speciality: Annotated[Speciality, Depends(check_speciality_by_id)],
):
    speciality_deleted = await SpecialityDAO.delete(
        session=session, filters={"id": speciality_id}
    )
    if not speciality_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user. Please try again later.",
        )
    return
