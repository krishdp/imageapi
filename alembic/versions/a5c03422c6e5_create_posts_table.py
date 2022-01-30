"""create posts Table

Revision ID: a5c03422c6e5
Revises: 
Create Date: 2022-01-28 10:32:31.260864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5c03422c6e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                            sa.Column('image_url', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
