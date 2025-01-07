from fastapi import APIRouter, HTTPException, Depends, status
from app.api.course.dao import CourseDAO
from app.api.course.dependencies import check_course_by_id, verify_user_is_teacher
from app.api.course.schemas import (
    BaseCourseSchema,
    CourseReadSchema,
    CourseUpdateSchema,
)
from typing import Annotated
from app.core import db_helper, settings, User, Course
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix=settings.api_prefix.courses, tags=["courseS"])


@router.post("")
async def create_course(
    course_data: BaseCourseSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_teacher: Annotated[User, Depends(verify_user_is_teacher)],
):
    print(check_teacher)
    check_course = await CourseDAO.get_one_or_none(
        session=session, filters={"name": course_data.name}
    )
    if check_course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Course already exists",
        )
    course = await CourseDAO.add(session=session, values=course_data)
    return {"message": "Course created", "course": course}


@router.get("/{course_id}")
async def get_course_by_id(
    course_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_course: Annotated[Course, Depends(check_course_by_id)],
):
    return {"course": CourseReadSchema(**check_course.to_dict())}


@router.patch("/{course_id}")
async def update_course(
    course_id: int,
    course_data: CourseUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_course: Annotated[Course, Depends(check_course_by_id)],
    check_teacher: Annotated[User, Depends(verify_user_is_teacher)],
):
    print(check_teacher)
    course = await CourseDAO.update(
        session=session, values=course_data, filters={"id": course_id}
    )

    if course:
        return {
            "message": "Course updated",
            "course": CourseReadSchema(**course.to_dict()),
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to delete user. Please try again later.",
    )


@router.delete("/{course_id}")
async def delete_course(
    course_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
    check_course: Annotated[Course, Depends(check_course_by_id)],
):
    course_deleted = await CourseDAO.delete(session=session, filters={"id": course_id})
    if not course_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user. Please try again later.",
        )
    return
