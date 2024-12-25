from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth.dependencies import get_current_admin_user
from app.api.roles.dao import RoleDAO
from app.api.roles.schemas import BaseRoleSchema, RoleSchemaRead
from fastapi import APIRouter, Depends, HTTPException, status
from app.core import settings, User, db_helper
from typing import Annotated, Union

router = APIRouter(prefix=settings.api_prefix.role, tags=["Role"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: BaseRoleSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, Union[str, RoleSchemaRead]]:
    role_info = await RoleDAO.get_one_or_none(session, filters=role_data)
    if role_info:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already exists",
        )

    role = await RoleDAO.add(session=session, values=role_data)
    return {"message": "Role created", "role": role}


@router.get("", status_code=status.HTTP_200_OK)
async def get_role(
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, list[RoleSchemaRead]]:
    roles = await RoleDAO.get_all(session=session)
    return {"roles": roles}


@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_role_by_id(
    role_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, RoleSchemaRead]:
    role = await RoleDAO.get_one_or_none_by_id(session=session, data_id=role_id)
    if role is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found",
        )
    return {"role": role}


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_role(
    role_id: int,
    role_data: BaseRoleSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    role = await RoleDAO.update(
        session=session, values=role_data, filters={"id": role_id}
    )
    if role:
        return {
            "message": "Role updated",
            "role": {"id": role_id, "name": role_data.name},
        }
    else:
        return {"message": "Role not found", "role_id": role_id}


@router.delete("/{id}")
async def delete_role(
    role_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    role = await RoleDAO.delete(session=session, filters={"id": role_id})
    if role:
        return {"message": "Role deleted"}
    else:
        return {"message": "Role not found"}
