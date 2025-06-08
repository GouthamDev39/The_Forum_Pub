"""Create Movie_suggest Table

Revision ID: de396efb41d4
Revises: 
Create Date: 2025-05-20 12:40:39.155156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de396efb41d4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('movie_suggest', sa.Column('id',sa.Integer(), nullable=False, primary_key=True),
    sa.Column('name', sa.String, nullable=False),sa.Column('ott', sa.String, nullable=False),
    sa.Column('description', sa.String, nullable=False ),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('movie_suggest')
    pass
