from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, VARCHAR, TEXT, INTEGER

if TYPE_CHECKING:
    from app.core import User


class Course(Base):
    name: Mapped[str] = mapped_column(VARCHAR(length=70), unique=True)
    description: Mapped[str] = mapped_column(TEXT)
    credit_hours: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="courses")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id}, {self.user_id})"
