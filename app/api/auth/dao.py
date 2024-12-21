from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from app.dao.base import BaseDAO
from sqlalchemy import select
from app.core import User


class AuthDAO(BaseDAO):
    model = User

    @classmethod
    async def get_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        try:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.role))
                .filter_by(id=data_id)
            )
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e
