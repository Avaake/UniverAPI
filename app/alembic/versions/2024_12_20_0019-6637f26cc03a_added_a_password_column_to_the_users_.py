"""added a password column to the users table

Revision ID: 6637f26cc03a
Revises: 6736abd101a0
Create Date: 2024-12-20 00:19:09.936795

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6637f26cc03a"
down_revision: Union[str, None] = "6736abd101a0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users", sa.Column("password", sa.VARCHAR(length=100), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("users", "password")
