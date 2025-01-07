"""update course table

Revision ID: 159e3235bf03
Revises: 3cc569db49f0
Create Date: 2025-01-06 18:21:38.129685

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "159e3235bf03"
down_revision: Union[str, None] = "3cc569db49f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("courses", sa.Column("credit_hours", sa.Integer(), nullable=False))
    op.drop_column("courses", "course_hours")


def downgrade() -> None:
    op.add_column(
        "courses",
        sa.Column(
            "course_hours",
            sa.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("courses", "credit_hours")
