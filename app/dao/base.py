from typing import TypeVar, Generic
from app.core import Base, configurate_logger
from fastapi import status, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, update, delete

log = configurate_logger(level="WARNING")

T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model = None

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, filters: BaseModel | dict):
        try:
            filters_dict = (
                filters.model_dump(exclude_unset=True)
                if isinstance(filters, BaseModel)
                else filters.copy()
            )

            query = select(cls.model).filter_by(**filters_dict)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except ConnectionRefusedError as e:
            log.error("Database connection error occurred: {}", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user. Please try again later.",
            )
        except SQLAlchemyError as e:
            log.warning("Database error occurred: {}", str(e), exc_info=True)
            raise e

    @classmethod
    async def get_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            return record
        except ConnectionRefusedError as e:
            log.error("Database connection error occurred: {}", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user. Please try again later.",
            )
        except SQLAlchemyError as e:
            log.warning("Database error occurred: {}", str(e), exc_info=True)
            raise e

    @classmethod
    async def add(cls, session: AsyncSession, values: BaseModel):
        try:
            values_dict = values.model_dump(exclude_unset=True)
            new_instance = cls.model(**values_dict)
            session.add(new_instance)
            await session.commit()
            return new_instance
        except ConnectionRefusedError as e:
            log.error("Database connection error occurred: {}", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user. Please try again later.",
            )
        except SQLAlchemyError as e:
            await session.rollback()
            log.warning("Database error occurred: {}", str(e), exc_info=True)
            raise e

    @classmethod
    async def get_all(cls, session: AsyncSession, filters: BaseModel | dict = None):
        if isinstance(filters, BaseModel):
            filters_dict = filters.model_dump(exclude_unset=True)
        elif filters is None:
            filters_dict = {}
        else:
            filters_dict = filters.copy()
        try:
            query = select(cls.model).filter_by(**filters_dict)
            result = await session.execute(query)
            record = result.scalars().all()
            return record
        except SQLAlchemyError as e:
            log.warning("Database error occurred: {}", str(e), exc_info=True)
            raise e

    @classmethod
    async def update(
        cls, session: AsyncSession, values: BaseModel | dict, filters: BaseModel | dict
    ):
        try:
            filters_dict = (
                filters.model_dump(exclude_unset=True)
                if isinstance(filters, BaseModel)
                else filters.copy()
            )

            values_dict = (
                values.model_dump(exclude_unset=True)
                if isinstance(values, BaseModel)
                else values.copy()
            )

            query = (
                update(cls.model)
                .where(*[getattr(cls.model, k) == v for k, v in filters_dict.items()])
                .values(**values_dict)
                .execution_options(synchronize_session="fetch")
            )
            await session.execute(query)

            update_record = await cls.get_one_or_none(session, filters=filters_dict)

            await session.commit()
            if update_record is None:
                return None
            return update_record
        except ConnectionRefusedError as e:
            log.error("Database connection error occurred: {}", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user. Please try again later.",
            )
        except SQLAlchemyError as e:
            await session.rollback()
            log.warning("Database error occurred: {}", str(e), exc_info=True)
            raise e

    @classmethod
    async def delete(cls, session: AsyncSession, filters: BaseModel | dict):
        try:
            if isinstance(filters, BaseModel):
                filters_dict = filters.model_dump(exclude_unset=True)
            else:
                filters_dict = filters.copy()
            query = delete(cls.model).filter_by(**filters_dict)
            record = await session.execute(query)
            await session.commit()
            return record.rowcount
        except ConnectionRefusedError as e:
            log.error("Database connection error occurred: {}", str(e), exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update user. Please try again later.",
            )
        except SQLAlchemyError as e:
            await session.rollback()
            log.warning("Database error occurred: {}", str(e), exc_info=True)
            raise e
