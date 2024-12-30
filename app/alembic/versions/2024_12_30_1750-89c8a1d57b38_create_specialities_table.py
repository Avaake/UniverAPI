"""create specialities table

Revision ID: 89c8a1d57b38
Revises: de0e73e848bc
Create Date: 2024-12-30 17:50:23.729072

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "89c8a1d57b38"
down_revision: Union[str, None] = "de0e73e848bc"
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
