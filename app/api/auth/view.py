from fastapi import APIRouter, Depends, status, HTTPException
from app.api.auth.schemas import (
    AuthAddSchema,
    AuthLoginSchema,
    AuthRegistrationSchema,
    EmailSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import db_helper, settings
from typing import Annotated
from app.api.auth.dao import AuthDAO

router = APIRouter(prefix=settings.api_prefix.auth, tags=["Auth"])


@router.post("/register")
async def register_user(
    user_data: AuthRegistrationSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict:
    user = await AuthDAO.get_one_or_none(
        session=session,
        filters=EmailSchema(email=user_data.email),
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already registered",
        )
    user_data_dict = user_data.model_dump()
    del user_data_dict["confirm_password"]
    await AuthDAO.add(session=session, values=AuthAddSchema(**user_data_dict))
    return {"message": "You have been successfully registered!"}
