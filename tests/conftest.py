import pytest_asyncio
from app.main import app
from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from app.core import Base
from app.core import db_helper, Role, User, Course, Speciality, Group

from tests.utils import (
    client_manager,
    ClientManagerType,
    async_session_maker,
    engine_test,
)

metadata = Base.metadata


# Перевизначена залежність для тестування
async def override_transaction() -> AsyncSession:
    async with async_session_maker() as session:
        async with session.begin():
            yield session


app.dependency_overrides[db_helper.transaction] = override_transaction


async def insert_table():
    async with async_session_maker() as session:
        async with session.begin():
            role = Role(name="user")
            session.add(role)
            await session.commit()


@pytest_asyncio.fixture(scope="module", autouse=True)
async def engine():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await insert_table()

    yield engine_test

    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="module")
async def async_client() -> ClientManagerType:
    async with client_manager(app) as c:
        yield c
