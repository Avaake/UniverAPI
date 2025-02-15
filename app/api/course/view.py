from fastapi import APIRouter, HTTPException, Depends, status
from app.api.auth.dependencies import get_current_admin_user
from app.api.course.dao import CourseDAO
from app.api.course.dependencies import check_course_by_id, verify_user_is_teacher
from app.api.course.schemas import (
    BaseCourseSchema,
    CourseReadSchema,
    CourseUpdateSchema,
)
from typing import Annotated
from app.core import db_helper, settings, User, Course, configurate_logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import get_or_409

log = configurate_logger(level="WARNING")
router = APIRouter(prefix=settings.api_prefix.courses, tags=["Courses"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: BaseCourseSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_teacher: Annotated[User, Depends(verify_user_is_teacher)],
):
    try:
        await get_or_409(
            session=session,
            dao=CourseDAO,
            filters=course_data,
            detail="Course already exists",
        )
        course = await CourseDAO.add(session=session, values=course_data)

        log.info("Created course {}", course.id)
        return {"message": "Course created", "course": course}
    except HTTPException as err:
        log.warning("HTTP error occurred: {}", str(err))
        raise err
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/{course_id}", status_code=status.HTTP_200_OK)
async def get_course_by_id(
    course_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_course: Annotated[Course, Depends(check_course_by_id)],
):
    try:
        return {"course": CourseReadSchema(**check_course.to_dict())}
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.patch("/{course_id}", status_code=status.HTTP_200_OK)
async def update_course(
    course_id: int,
    course_data: CourseUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_course: Annotated[Course, Depends(check_course_by_id)],
    check_teacher: Annotated[User, Depends(verify_user_is_teacher)],
):
    try:
        course = await CourseDAO.update(
            session=session, values=course_data, filters={"id": course_id}
        )

        if course:
            log.info("Updated course {}", course_id)
            return {
                "message": "Course updated",
                "course": CourseReadSchema(**course.to_dict()),
            }
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    check_course: Annotated[Course, Depends(check_course_by_id)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> None:
    try:
        course_deleted = await CourseDAO.delete(
            session=session, filters={"id": course_id}
        )
        if course_deleted:
            log.info("Deleted course {}", course_id)
            return
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
