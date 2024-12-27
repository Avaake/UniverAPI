from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.core import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def get_all_users_by_role_name(cls, role_name: str, session: AsyncSession):
        try:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.role))
                .filter(cls.model.role.has(name=role_name))
            )
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise e
