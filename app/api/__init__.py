from fastapi import APIRouter
from app.core import settings
from app.api.auth.view import router as auth_router
from app.api.roles.view import router as roles_router
from app.api.users.view import router as users_router
from app.api.groups.view import router as groups_router
from app.api.speciality.view import router as speciality_router

api_router = APIRouter(prefix=settings.api_prefix.api_v1)
api_router.include_router(auth_router)
api_router.include_router(roles_router)
api_router.include_router(users_router)
api_router.include_router(groups_router)

api_router.include_router(speciality_router)
