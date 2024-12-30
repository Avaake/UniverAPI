from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR, TEXT


class Speciality(Base):
    __tablename__ = "specialities"
    name: Mapped[str] = mapped_column(VARCHAR(length=100), nullable=False, unique=True)
    descriptions: Mapped[str] = mapped_column(TEXT, nullable=True)
