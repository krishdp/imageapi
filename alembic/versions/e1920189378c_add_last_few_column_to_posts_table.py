"""add last few column to posts table

Revision ID: e1920189378c
Revises: 34ba27e2dcd2
Create Date: 2022-01-28 11:21:24.971003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1920189378c'
down_revision = '34ba27e2dcd2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('caption', sa.String()))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.downgrade('posts', 'caption')
    op.downgrade('posts', 'created_at')
    pass
