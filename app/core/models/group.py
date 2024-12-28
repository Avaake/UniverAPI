from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR


class Group(Base):
    name: Mapped[str] = mapped_column(VARCHAR(length=50), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
