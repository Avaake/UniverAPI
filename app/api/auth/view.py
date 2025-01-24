from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import db_helper, settings, User
from app.api.auth.dao import AuthDAO
from typing import Annotated
from app.api.auth.schemas import (
    AuthAddSchema,
    AuthLoginSchema,
    AuthRegistrationSchema,
    EmailSchema,
)
from app.api.auth.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)
from app.api.auth.dependencies import (
    get_current_user_refresh_token,
    get_current_user_access_token,
)

from app.core import get_or_409

router = APIRouter(prefix=settings.api_prefix.auth, tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: AuthRegistrationSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict:
    await get_or_409(
        session=session,
        dao=AuthDAO,
        filters=EmailSchema(email=user_data.email),
        detail="User already registered",
    )
    user_data_dict = user_data.model_dump()
    del user_data_dict["confirm_password"]
    await AuthDAO.add(session=session, values=AuthAddSchema(**user_data_dict))
    return {"message": "You have been successfully registered!"}


@router.post("/login")
async def login(
    response: Response,
    user_data: AuthLoginSchema,
    session: Annotated[AsyncSession, Depends(db_helper.transaction)],
) -> dict:
    try:
        user = await authenticate_user(
            email=user_data.email, password=user_data.password, session=session
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        payload_dict = {"sub": str(user.id)}

        access_token = create_access_token(payload_dict)
        refresh_token = create_refresh_token(payload_dict)

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {
            "message": "You have been logged in!",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/refresh")
async def refresh(
    response: Response,
    user_data: Annotated[User, Depends(get_current_user_refresh_token)],
):
    try:
        payload_dict = {"sub": str(user_data.id)}

        access_token = create_access_token(payload_dict)
        refresh_token = create_refresh_token(payload_dict)

        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/logout")
async def logout(response: Response) -> dict:
    try:
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return {"message": "The user has successfully logged out"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )


@router.get("/protected")
async def protected(
    current_user: Annotated[User, Depends(get_current_user_access_token)],
) -> dict:
    try:
        return {"message": "You are authorized"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user. Please try again later.",
        )
