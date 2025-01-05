from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import VARCHAR, ForeignKey, text

if TYPE_CHECKING:
    from app.core import Role, Enrollment, Course


class User(Base):
    first_name: Mapped[str] = mapped_column(VARCHAR(50))
    last_name: Mapped[str] = mapped_column(VARCHAR(50))
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True)
    phone_number: Mapped[str] = mapped_column(VARCHAR(20), unique=True)
    password: Mapped[str] = mapped_column(VARCHAR(100))
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id", ondelete="CASCADE"), default=1, server_default=text("1")
    )
    role: Mapped["Role"] = relationship(back_populates="users")
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="user")
    courses: Mapped[list["Course"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
