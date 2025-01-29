from fastapi import APIRouter, Depends, HTTPException, status, Path
from app.api.roles.schemas import BaseRoleSchema, RoleSchemaRead
from app.api.auth.dependencies import get_current_admin_user
from app.api.roles.dependencies import check_role_by_id
from app.core import settings, User, db_helper, Role, configurate_logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.roles.dao import RoleDAO
from typing import Annotated, Union
from app.core import get_or_409

log = configurate_logger(level="WARNING")
router = APIRouter(prefix=settings.api_prefix.role, tags=["Role"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: BaseRoleSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, Union[str, RoleSchemaRead]]:
    try:
        await get_or_409(
            session=session,
            dao=RoleDAO,
            filters=role_data,
            detail="Role already exists",
        )

        role = await RoleDAO.add(session=session, values=role_data)

        log.info("Created new role: {}", role.id)
        return {"message": "Role created", "role": role}
    except HTTPException as err:
        log.warning("HTTP error occurred: {}", err)
        raise err
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("", status_code=status.HTTP_200_OK)
async def get_roles(
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, list[RoleSchemaRead]]:
    try:
        roles = await RoleDAO.get_all(session=session)
        return {"roles": roles}
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/{role_id}", status_code=status.HTTP_200_OK)
async def get_role_by_id(
    role_id: Annotated[int, Path(ge=0)],
    check_role: Annotated[Role, Depends(check_role_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, RoleSchemaRead]:
    try:
        return {"role": RoleSchemaRead(**check_role.to_dict())}
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.put("/{role_id}", status_code=status.HTTP_200_OK)
async def update_role(
    role_id: Annotated[int, Path(ge=0)],
    role_data: BaseRoleSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_role: Annotated[Role, Depends(check_role_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    try:

        role = await RoleDAO.update(
            session=session, values=role_data, filters={"id": role_id}
        )
        if role:
            log.info("Updated role: {}", role_id)
            return {
                "message": "Role updated",
                "role": role,
            }
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_role: Annotated[Role, Depends(check_role_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
):
    try:
        role = await RoleDAO.delete(session=session, filters={"id": role_id})
        if role:
            log.info("Deleted role: {}", role_id)
            return
    except Exception as err:
        log.warning("Error occurred: {}", str(err), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
