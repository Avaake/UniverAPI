from app.api.groups.schemas import GroupBaseSchema, GroupUpdateSchema, GroupReadSchema
from fastapi import APIRouter, HTTPException, status, Depends, Path
from app.api.auth.dependencies import get_current_admin_user
from app.api.groups.dependencies import check_group_by_id
from app.core import settings, db_helper, Group, User
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.groups.dao import GroupDAO
from typing import Annotated

router = APIRouter(prefix=settings.api_prefix.group, tags=["Groups"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_group(
    group_data: GroupBaseSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, GroupReadSchema]:
    check_group = await GroupDAO.get_one_or_none(session=session, filters=group_data)
    if check_group:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Group already exists",
        )
    group = await GroupDAO.add(session=session, values=group_data)
    return {"message": "Group created", "group": group}


@router.get("/{group_id}", status_code=status.HTTP_200_OK)
async def get_group_by_id(
    group_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_group: Annotated[Group, Depends(check_group_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, GroupReadSchema]:
    return {"group": GroupReadSchema(**check_group.to_dict())}


@router.put("/{group_id}", status_code=status.HTTP_200_OK)
async def update_group(
    group_id: Annotated[int, Path(ge=0)],
    data: GroupUpdateSchema,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_group: Annotated[Group, Depends(check_group_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict[str, GroupReadSchema]:
    group = await GroupDAO.update(
        session=session, values=data, filters={"id": group_id}
    )
    if group:
        return {
            "message": "Group updated",
            "group": GroupReadSchema(**check_group.to_dict()),
        }
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Failed to update user role. Please try again later.",
    )


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: Annotated[int, Path(ge=0)],
    current_user: Annotated[User, Depends(get_current_admin_user)],
    check_group: Annotated[Group, Depends(check_group_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> None:
    user_deleted = await GroupDAO.delete(session=session, filters={"id": group_id})
    if not user_deleted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete user. Please try again later.",
        )
    return
