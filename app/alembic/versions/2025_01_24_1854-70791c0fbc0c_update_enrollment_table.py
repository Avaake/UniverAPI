"""update enrollment table

Revision ID: 70791c0fbc0c
Revises: 159e3235bf03
Create Date: 2025-01-24 18:54:26.535672

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "70791c0fbc0c"
down_revision: Union[str, None] = "159e3235bf03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint("fk_courses_user_id_users", "courses", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_courses_user_id_users"),
        "courses",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.add_column(
        "enrollments", sa.Column("study_year", sa.SmallInteger(), nullable=False)
    )
    op.alter_column(
        "enrollments", "user_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "enrollments", "group_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.alter_column(
        "enrollments", "speciality_id", existing_type=sa.INTEGER(), nullable=False
    )
    op.drop_constraint(
        "fk_enrollments_user_id_users", "enrollments", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_enrollments_group_id_groups", "enrollments", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_enrollments_speciality_id_specialities", "enrollments", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_enrollments_group_id_groups"),
        "enrollments",
        "groups",
        ["group_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_enrollments_speciality_id_specialities"),
        "enrollments",
        "specialities",
        ["speciality_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_enrollments_user_id_users"),
        "enrollments",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_column("enrollments", "academic_year")


def downgrade() -> None:
    op.add_column(
        "enrollments",
        sa.Column("academic_year", sa.SMALLINT(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(
        op.f("fk_enrollments_user_id_users"), "enrollments", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_enrollments_speciality_id_specialities"),
        "enrollments",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_enrollments_group_id_groups"), "enrollments", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_enrollments_speciality_id_specialities",
        "enrollments",
        "specialities",
        ["speciality_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_enrollments_group_id_groups", "enrollments", "groups", ["group_id"], ["id"]
    )
    op.create_foreign_key(
        "fk_enrollments_user_id_users", "enrollments", "users", ["user_id"], ["id"]
    )
    op.alter_column(
        "enrollments", "speciality_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column(
        "enrollments", "group_id", existing_type=sa.INTEGER(), nullable=True
    )
    op.alter_column("enrollments", "user_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_column("enrollments", "study_year")
    op.drop_constraint(op.f("fk_courses_user_id_users"), "courses", type_="foreignkey")
    op.create_foreign_key(
        "fk_courses_user_id_users", "courses", "users", ["user_id"], ["id"]
    )
