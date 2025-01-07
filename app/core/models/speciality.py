from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR, TEXT

if TYPE_CHECKING:
    from app.core import Enrollment


class Speciality(Base):
    __tablename__ = "specialities"
    name: Mapped[str] = mapped_column(VARCHAR(length=100), nullable=False, unique=True)
    descriptions: Mapped[str] = mapped_column(TEXT, nullable=True)

    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="speciality")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
