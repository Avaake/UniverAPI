from app.api.course.schemas import CourseUpdateSchema
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import Course, db_helper, User
from app.api.course.dao import CourseDAO
from app.api.auth.dao import AuthDAO
from typing import Annotated


async def check_course_by_id(
    course_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> Course:
    course = await CourseDAO.get_one_or_none_by_id(session=session, data_id=course_id)
    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    return course


async def verify_user_is_teacher(
    course_data: CourseUpdateSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> User | None:
    if course_data.user_id is None:
        return None

    user = await AuthDAO.get_one_or_none_by_id(
        session=session, data_id=course_data.user_id
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.role.name == "teacher":
        return user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is not a teacher",
    )
