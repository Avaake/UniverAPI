"""create speciality table

Revision ID: 419f2544abea
Revises: 37d8494c0657
Create Date: 2025-01-30 16:43:17.049492

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "419f2544abea"
down_revision: Union[str, None] = "37d8494c0657"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "specialities",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(length=100), nullable=False),
        sa.Column("descriptions", sa.TEXT(), nullable=True),
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
        sa.PrimaryKeyConstraint("id", name=op.f("pk_specialities")),
        sa.UniqueConstraint("name", name=op.f("uq_specialities_name")),
    )


def downgrade() -> None:
    op.drop_table("specialities")
