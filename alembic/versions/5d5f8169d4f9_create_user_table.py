"""Create User Table

Revision ID: 5d5f8169d4f9
Revises: de396efb41d4
Create Date: 2025-05-20 12:55:14.744170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d5f8169d4f9'
down_revision: Union[str, None] = 'de396efb41d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('users', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
    sa.Column('username', sa.String, nullable=False, unique = True),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
