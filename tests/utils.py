from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core import Base, Role, User, Course, Speciality, Group, Enrollment
from app.api.auth.utis import get_password_hash
from httpx import AsyncClient, ASGITransport
from contextlib import asynccontextmanager
from asgi_lifespan import LifespanManager
from typing import AsyncGenerator
from sqlalchemy import NullPool
import logging


def logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()
        ],  # Додайте цей handler для виведення на екран
    )
    return logging


ClientManagerType = AsyncGenerator[AsyncClient, None]
metadata = Base.metadata
DATABASE_URL = "postgresql+asyncpg://admin_test:admin_password_test@postgres_db_test:5433/postgres_univer_db_test"


engine_test = create_async_engine(
    DATABASE_URL,
    echo=False,
    poolclass=NullPool,
)
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


def test_data(session: AsyncSession):
    # Role
    default_role = Role(name="user")
    role_admin = Role(name="admin")
    role_teacher = Role(name="teacher")
    role_student = Role(name="student")
    session.add_all([default_role, role_admin, role_teacher, role_student])
    # User
    admin_user = User(
        first_name="admin",
        last_name="admin",
        email="admin@gmail.com",
        phone_number="+38099999999",
        password=get_password_hash("qwerty"),
        role=role_admin,
    )
    tomas_teacher_user = User(
        first_name="tomas",
        last_name="tamas",
        email="tamas@gmail.com",
        phone_number="+38088888888",
        password=get_password_hash("qwerty"),
        role=role_teacher,
    )
    john_student_user = User(
        first_name="john",
        last_name="johnson",
        email="john@gmail.com",
        phone_number="+38077777777",
        password=get_password_hash("qwerty"),
        role=role_student,
    )
    session.add(admin_user)
    session.add(tomas_teacher_user)
    session.add(john_student_user)
    first_group = Group(name="LL25/1")
    second_group = Group(name="SE25")
    session.add_all([first_group, second_group])
    # Speciality
    first_speciality = Speciality(
        name="International law",
        descriptions="International law",
    )
    second_speciality = Speciality(
        name="Software engineering",
        descriptions="Software engineering",
    )
    session.add_all([first_speciality, second_speciality])
    # Course
    sql_course = Course(
        name="SQL",
        description="Structured query language",
        credit_hours=21,
        user=tomas_teacher_user,
    )
    session.add(sql_course)
    # Enrollment
    first_enrollment = Enrollment(
        user=john_student_user,
        group=second_group,
        speciality=second_speciality,
        academic_year=1,
    )
    session.add(first_enrollment)


def delete_token(async_client: AsyncClient):
    async_client.cookies.delete("access_token")
    async_client.cookies.delete("refresh_token")
