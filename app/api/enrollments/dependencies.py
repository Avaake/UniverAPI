from app.api.enrollments.schemas import EnrollmentUpdateSchema
from app.core import db_helper, Enrollment, get_or_404
from fastapi import Depends, status, HTTPException
from app.api.enrollments.dao import EnrollmentDAO
from app.api.speciality.dao import SpecialityDAO
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.groups.dao import GroupDAO
from app.api.auth.dao import AuthDAO
from typing import Annotated


async def check_enrollment_by_id(
    enrollment_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> Enrollment:
    enrollment = await get_or_404(
        dao=EnrollmentDAO,
        session=session,
        data_id=enrollment_id,
        detail="Enrollment not found",
    )
    return enrollment


async def check_the_availability_of_group_student_and_speciality(
    enrollment_data: EnrollmentUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    if enrollment_data.user_id is not None:
        user = await get_or_404(
            dao=AuthDAO,
            session=session,
            data_id=enrollment_data.user_id,
            detail="User not found",
        )

        if user.role.name != "student":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User is not a student",
            )

    if enrollment_data.group_id is not None:
        await get_or_404(
            dao=GroupDAO(),
            session=session,
            data_id=enrollment_data.group_id,
            detail="Group not found",
        )

    if enrollment_data.speciality_id is not None:
        await get_or_404(
            dao=SpecialityDAO(),
            session=session,
            data_id=enrollment_data.speciality_id,
            detail="Speciality not found",
        )

    return True
