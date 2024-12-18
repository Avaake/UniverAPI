from fastapi import APIRouter
from app.core import settings
from app.api.auth.view import router as auth_router

api_router = APIRouter(prefix=settings.api_prefix.api_v1)
api_router.include_router(auth_router)
