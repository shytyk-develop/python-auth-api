"""Initial schema with users table

Revision ID: 6bf85164ab1d
Revises: 
Create Date: 2026-02-04 02:03:52.244503

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '6bf85164ab1d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('users',
    sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('email', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('is_subscribed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('users_pkey'))
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
