"""add other Column in posts Table

Revision ID: f03afbd6ad4e
Revises: a5c03422c6e5
Create Date: 2022-01-28 10:39:37.925480

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f03afbd6ad4e'
down_revision = 'a5c03422c6e5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('image_url_type', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','image_url_type')
    pass
