"""create course table

Revision ID: f3130297cb3c
Revises: 89c8a1d57b38
Create Date: 2024-12-30 23:29:12.180205

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3130297cb3c"
down_revision: Union[str, None] = "89c8a1d57b38"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "enrollments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("speciality_id", sa.Integer(), nullable=True),
        sa.Column("academic_year", sa.SmallInteger(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "academic_year BETWEEN 1 AND 7",
            name=op.f("ck_enrollments_chk_academic_year_range"),
        ),
        sa.ForeignKeyConstraint(
            ["group_id"], ["groups.id"], name=op.f("fk_enrollments_group_id_groups")
        ),
        sa.ForeignKeyConstraint(
            ["speciality_id"],
            ["specialities.id"],
            name=op.f("fk_enrollments_speciality_id_specialities"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_enrollments_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_enrollments")),
        sa.UniqueConstraint(
            "user_id",
            "group_id",
            "speciality_id",
            name="idx_unique_user_group_speciality",
        ),
    )


def downgrade() -> None:
    op.drop_table("enrollments")
