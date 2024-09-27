"""Create users table

Revision ID: b7bb00c82a08
Revises: 3fdb482d6c4b
Create Date: 2024-09-22 13:03:45.604765

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7bb00c82a08'
down_revision: Union[str, None] = '3fdb482d6c4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
    )


def downgrade():
    op.drop_table('users')