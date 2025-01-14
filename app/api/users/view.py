from app.api.users.dependencies import check_access_to_user, check_user_by_id
from fastapi import APIRouter, status, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import settings, User, db_helper
from app.api.auth.dependencies import (
    get_current_user_access_token,
    get_current_admin_user,
)
from app.api.users.dao import UserDAO
from app.api.users.schemas import (
    UserReadSchema,
    UserReadListSchema,
    UserUpdateSchema,
    UserRoleIDSchema,
)
from typing import Annotated, Union

router = APIRouter(prefix=settings.api_prefix.user, tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
    user_data: Annotated[UserReadSchema, Depends(get_current_user_access_token)]
) -> UserReadSchema:
    try:
        return UserReadSchema.model_validate(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    user_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_user: Annotated[User, Depends(check_user_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> UserReadSchema:
    try:
        return UserReadSchema(**check_user.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/roles/{role_name}")
async def get_users_by_role(
    role_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> UserReadListSchema:
    try:
        users = await UserDAO.get_all_users_by_role_name(
            session=session, role_name=role_name
        )
        return UserReadListSchema(users=users)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.put("/{user_id}/role", status_code=status.HTTP_200_OK)
async def update_user_role(
    user_id: Annotated[int, Path(ge=0)],
    role_data: UserRoleIDSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_user: Annotated[User, Depends(check_user_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, Union[str, UserReadSchema]]:
    try:
        new_user_role = await UserDAO.update(
            session=session, values=role_data, filters={"id": user_id}
        )
        if new_user_role:
            return {
                "message": "User role updated",
                "user": UserReadSchema.model_validate(new_user_role),
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: Annotated[int, Path(ge=0)],
    new_user_data: UserUpdateSchema,
    current_user: Annotated[User, Depends(check_access_to_user)],
    check_user: Annotated[User, Depends(check_user_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, Union[str, UserReadSchema]]:
    try:
        user = await UserDAO.update(
            session=session, values=new_user_data, filters={"id": user_id}
        )
        if user:
            return {
                "message": "User updated",
                "user": UserReadSchema.model_validate(user),
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(check_access_to_user)],
    check_user: Annotated[User, Depends(check_user_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    try:
        user_deleted = await UserDAO.delete(session=session, filters={"id": user_id})
        if user_deleted:
            return
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
