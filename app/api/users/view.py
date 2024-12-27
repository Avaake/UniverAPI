from app.api.users.schemas import (
    UserReadSchema,
    UserReadListSchema,
    UserUpdateSchema,
)
from fastapi import APIRouter, status, HTTPException, Depends, Path
from app.api.users.dependencies import check_access_to_user
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import settings, User, db_helper
from app.api.auth.dependencies import (
    get_current_user_access_token,
    get_current_admin_user,
)
from app.api.roles.dao import RoleDAO
from app.api.users.dao import UserDAO
from typing import Annotated


router = APIRouter(prefix=settings.api_prefix.user, tags=["Users"])


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(
    user_data: Annotated[UserReadSchema, Depends(get_current_user_access_token)]
) -> UserReadSchema:
    return UserReadSchema.model_validate(user_data)


@router.get("{user_id}", status_code=status.HTTP_200_OK)
async def get_user(
    user_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> UserReadSchema:
    user = await UserDAO.get_one_or_none_by_id(session=session, data_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return UserReadSchema.model_validate(user)


@router.get("/roles/{role_name}")
async def get_users_by_role(
    role_name: str,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> UserReadListSchema:
    users = await UserDAO.get_all_users_by_role_name(
        session=session, role_name=role_name
    )
    return UserReadListSchema(users=users)


@router.patch("/{user_id}/role/{role_id}", status_code=status.HTTP_200_OK)
async def update_user_role(
    user_id: Annotated[int, Path(ge=0)],
    role_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_user_access_token)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    role = await RoleDAO.get_one_or_none_by_id(session=session, data_id=role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    user = await UserDAO.get_one_or_none_by_id(session=session, data_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    new_user_role = await UserDAO.update(
        session=session, values={"role_id": role_id}, filters={"id": user_id}
    )
    if new_user_role:
        return {"message": "User role updated"}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user role. Please try again later.",
        )


@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: Annotated[int, Path(ge=0)],
    new_user_data: UserUpdateSchema,
    current_user: Annotated[User, Depends(check_access_to_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    user = await UserDAO.update(
        session=session, values=new_user_data, filters={"id": user_id}
    )
    if user:
        return {
            "message": "User updated",
            "user": UserReadSchema.model_validate(user),
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update user. Please try again later.",
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(check_access_to_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    check_user = await UserDAO.get_one_or_none_by_id(session=session, data_id=user_id)
    if check_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    user_deleted = await UserDAO.delete(session=session, filters={"id": user_id})
    if not user_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user. Please try again later.",
        )
    return
