from typing import TypeVar, Generic
from app.core import Base
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model = None

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, filters: BaseModel):
        try:
            filter_dict = filters.model_dump(exclude_unset=True)
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def get_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except SQLAlchemyError as e:
            raise e

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        try:
            values_dict = values.model_dump(exclude_unset=True)
            new_instance = cls.model(**values_dict)
            session.add(new_instance)
            await session.commit()
            return new_instance
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
