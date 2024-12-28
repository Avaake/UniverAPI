from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.api.roles.schemas import BaseRoleSchema, RoleSchemaRead
from app.api.auth.dependencies import get_current_admin_user
from app.api.roles.dependencies import check_role_by_id
from app.core import settings, User, db_helper, Role
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.roles.dao import RoleDAO
from typing import Annotated, Union


router = APIRouter(prefix=settings.api_prefix.role, tags=["Role"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: BaseRoleSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, RoleSchemaRead]:
    role_info = await RoleDAO.get_one_or_none(session, filters=role_data)
    if role_info:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already exists",
        )

    role = await RoleDAO.add(session=session, values=role_data)
    return {"message": "Role created", "role": role}


@router.get("", status_code=status.HTTP_200_OK)
async def get_roles(
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, list[RoleSchemaRead]]:
    roles = await RoleDAO.get_all(session=session)
    return {"roles": roles}


@router.get("/{role_id}", status_code=status.HTTP_200_OK)
async def get_role_by_id(
    role_id: Annotated[int, Path(ge=0)],
    check_role: Annotated[Role, Depends(check_role_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, RoleSchemaRead]:
    return {"role": RoleSchemaRead(**check_role.to_dict())}


@router.put("/{role_id}", status_code=status.HTTP_200_OK)
async def update_role(
    role_id: Annotated[int, Path(ge=0)],
    role_data: BaseRoleSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_role: Annotated[Role, Depends(check_role_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    role = await RoleDAO.update(
        session=session, values=role_data, filters={"id": role_id}
    )
    if role:
        return {
            "message": "Role updated",
            "role": role,
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update user. Please try again later.",
    )


@router.delete("/{role_id}")
async def delete_role(
    role_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_role: Annotated[Role, Depends(check_role_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    role = await RoleDAO.delete(session=session, filters={"id": role_id})
    if role:
        return
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to delete user. Please try again later.",
    )
