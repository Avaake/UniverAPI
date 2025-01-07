from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR

if TYPE_CHECKING:
    from app.core import Enrollment


class Group(Base):
    name: Mapped[str] = mapped_column(VARCHAR(length=50), unique=True, nullable=False)

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="group")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
