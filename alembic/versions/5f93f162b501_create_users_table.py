"""Create users table

Revision ID: 5f93f162b501
Revises: 3d72aad495a8
Create Date: 2024-09-22 13:01:52.074423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '5f93f162b501'
down_revision: Union[str, None] = '3d72aad495a8'
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