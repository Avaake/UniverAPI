"""rename the study_year column to academic_year in the enrolment table

Revision ID: 05c075530557
Revises: 70791c0fbc0c
Create Date: 2025-01-26 16:04:10.518749

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "05c075530557"
down_revision: Union[str, None] = "70791c0fbc0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "enrollments", sa.Column("academic_year", sa.SmallInteger(), nullable=False)
    )
    op.drop_column("enrollments", "year_study")


def downgrade() -> None:
    op.add_column(
        "enrollments",
        sa.Column("year_study", sa.SMALLINT(), autoincrement=False, nullable=False),
    )
    op.drop_column("enrollments", "academic_year")
