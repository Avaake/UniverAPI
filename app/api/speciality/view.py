from fastapi import APIRouter, HTTPException, Path, Depends, status
from app.api.speciality.schemas import (
    SpecialityReadSchema,
    SpecialityBaseSchema,
    SpecialityUpdateSchema,
)
from app.api.speciality.dao import SpecialityDAO
from typing import Annotated
from app.core import db_helper, settings, Speciality, User
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.speciality.dependencies import check_speciality_by_id
from app.api.auth.dependencies import get_current_admin_user

router = APIRouter(prefix=settings.api_prefix.specialities, tags=["Speciality"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_speciality(
    speciality_data: SpecialityBaseSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    try:
        check_speciality = await SpecialityDAO.get_one_or_none(
            session=session, filters={"name": speciality_data.name}
        )
        if check_speciality:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Speciality already exists",
            )
        speciality = await SpecialityDAO.add(session, values=speciality_data)
        return {"message": "Speciality created", "speciality": speciality}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/{speciality_id}", status_code=status.HTTP_200_OK)
async def get_speciality_by_id(
    speciality_id: Annotated[int, Path(ge=0)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_speciality: Annotated[Speciality, Depends(check_speciality_by_id)],
):
    try:
        return {"speciality": SpecialityReadSchema(**check_speciality.to_dict())}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.patch("/{speciality_id}", status_code=status.HTTP_200_OK)
async def update_speciality(
    speciality_id: Annotated[int, Path(ge=0)],
    speciality_data: SpecialityUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_speciality: Annotated[Speciality, Depends(check_speciality_by_id)],
):
    try:
        speciality = await SpecialityDAO.update(
            session=session, values=speciality_data, filters={"id": speciality_id}
        )

        if speciality:
            return {
                "message": "Speciality updated",
                "speciality": SpecialityReadSchema(**speciality.to_dict()),
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.delete("/{speciality_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_speciality(
    speciality_id: Annotated[int, Path(ge=0)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_speciality: Annotated[Speciality, Depends(check_speciality_by_id)],
):
    try:
        speciality_deleted = await SpecialityDAO.delete(
            session=session, filters={"id": speciality_id}
        )
        if speciality_deleted:
            return
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
