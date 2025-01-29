from fastapi import APIRouter, HTTPException, status, Depends, Path
from app.api.auth.dependencies import get_current_admin_user
from app.core import Enrollment, db_helper, settings, User, configurate_logger
from typing import Annotated, Union
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.enrollments.dao import EnrollmentDAO
from app.api.enrollments.schemas import BaseEnrollmentSchema, EnrollmentUpdateSchema
from app.api.enrollments.dependencies import (
    check_the_availability_of_group_student_and_speciality,
    check_enrollment_by_id,
)
from app.core import get_or_409

log = configurate_logger(level="WARNING")

router = APIRouter(prefix=settings.api_prefix.enrollments, tags=["Enrollments"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment_data: BaseEnrollmentSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    verify_enrollment: Annotated[
        bool, Depends(check_the_availability_of_group_student_and_speciality)
    ],
):
    try:
        await get_or_409(
            dao=EnrollmentDAO,
            session=session,
            filters={
                "user_id": enrollment_data.user_id,
                "group_id": enrollment_data.group_id,
                "speciality_id": enrollment_data.speciality_id,
            },
            detail="Enrollment already exists",
        )
        enrollment = await EnrollmentDAO.add(session=session, values=enrollment_data)

        log.info("Created enrollment {}", enrollment.id)
        return {
            "message": "Enrollment created",
            "enrollment": enrollment,
        }
    except HTTPException as err:
        log.warning("HTTP error occurred: {}", err)
        raise err
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/{enrollment_id}", status_code=status.HTTP_200_OK)
async def get_enrollment_by_id(
    enrollment_id: Annotated[int, Path(ge=0)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_enrollment: Annotated[Enrollment, Depends(check_enrollment_by_id)],
):
    try:
        return {"course": BaseEnrollmentSchema(**check_enrollment.to_dict())}
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.patch("/{enrollment_id}", status_code=status.HTTP_200_OK)
async def update_enrollment(
    enrollment_id: Annotated[int, Path(ge=0)],
    enrollment_data: EnrollmentUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_enrollment: Annotated[Enrollment, Depends(check_enrollment_by_id)],
):
    try:
        enrollment = await EnrollmentDAO.update(
            session=session, values=enrollment_data, filters={"id": enrollment_id}
        )

        log.info("Updated enrollment {}", enrollment_id)
        return {
            "message": "Enrollment updated",
            "enrollment": BaseEnrollmentSchema(**enrollment.to_dict()),
        }
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    enrollment_id: Annotated[int, Path(ge=0)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_enrollment: Annotated[Enrollment, Depends(check_enrollment_by_id)],
):
    try:
        enrollment_deleted = await EnrollmentDAO.delete(
            session=session,
            filters={"id": enrollment_id},
        )
        if enrollment_deleted:
            log.info("Deleted enrollment {}", enrollment_id)
            return
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
