from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core import User


class Role(Base):
    name: Mapped[str] = mapped_column(unique=True)
    users: Mapped[list["User"]] = relationship(
        back_populates="role", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name})"
