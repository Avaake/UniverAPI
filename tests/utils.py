from contextlib import asynccontextmanager
from typing import AsyncGenerator

from asgi_lifespan import LifespanManager
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import NullPool

ClientManagerType = AsyncGenerator[AsyncClient, None]

DATABASE_URL = (
    "postgresql+asyncpg://admin:admin_password@localhost:5432/postgres_univer_db"
)
engine_test = create_async_engine(DATABASE_URL, echo=False, poolclass=NullPool)
async_session_maker = async_sessionmaker(
    bind=engine_test,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def client_manager(app, base_url="http://test", **kw) -> ClientManagerType:
    app.state.testing = True
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url=base_url, **kw) as c:
            yield c
