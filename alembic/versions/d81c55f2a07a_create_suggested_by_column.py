"""Create suggested_by column

Revision ID: d81c55f2a07a
Revises: 5d5f8169d4f9
Create Date: 2025-05-20 13:12:57.467723

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd81c55f2a07a'
down_revision: Union[str, None] = '5d5f8169d4f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('movie_suggest',sa.Column('suggested_by', sa.String(), nullable = False))
    op.create_foreign_key('moie_user_fk', source_table="movie_suggest",
    referent_table="users",
    local_cols=['suggested_by'], remote_cols=['username'],ondelete="CASCADE"
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constarin('moie_user_fk', table_name='movie_suggest')
    op.drop_column('movie_suggest', 'suggested_by')
    
