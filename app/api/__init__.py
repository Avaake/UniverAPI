from fastapi import APIRouter
from app.core import settings

api_router = APIRouter(prefix=settings.api_prefix.api_v1, tags=["api_v1"])
