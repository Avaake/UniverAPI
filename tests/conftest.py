from sqlalchemy.ext.asyncio import AsyncSession
from app.core import db_helper
from tests.utils import (
    client_manager,
    ClientManagerType,
    async_session_maker,
    engine_test,
    metadata,
    test_data,
)
from app.main import app
import pytest_asyncio


async def override_transaction() -> AsyncSession:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


app.dependency_overrides[db_helper.transaction] = override_transaction


async def insert_into_tables() -> None:
    async with async_session_maker() as session:
        async with session.begin():
            test_data(session=session)
            await session.commit()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def engine():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)

    await insert_into_tables()

    yield engine_test

    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def token_admin(async_client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "qwerty1",
    }
    response = await async_client.post("/api/v1/auth/login", json=user_data)
    data = response.json()

    yield data["access_token"], data["refresh_token"]


@pytest_asyncio.fixture(scope="module")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c
