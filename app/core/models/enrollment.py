from app.core import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UniqueConstraint, SmallInteger, CheckConstraint

if TYPE_CHECKING:
    from app.core import User, Group, Speciality


class Enrollment(Base):
    """
    User-Group-Speciality association
    """

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)
    speciality_id: Mapped[int] = mapped_column(
        ForeignKey("specialities.id"), nullable=True
    )
    academic_year: Mapped[int] = mapped_column(SmallInteger, nullable=True)

    user: Mapped["User"] = relationship(back_populates="enrollments")
    group: Mapped["Group"] = relationship(back_populates="enrollments")
    speciality: Mapped["Speciality"] = relationship(back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "group_id",
            "speciality_id",
            name="idx_unique_user_group_speciality",
        ),
        CheckConstraint(
            "academic_year BETWEEN 1 AND 7", name="chk_academic_year_range"
        ),
    )

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, user_id={self.user_id}, "
            f"group_id={self.group_id}, speciality_id={self.speciality_id})"
        )
