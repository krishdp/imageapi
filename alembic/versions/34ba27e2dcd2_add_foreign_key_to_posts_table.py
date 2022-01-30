"""add foreign-key to posts table

Revision ID: 34ba27e2dcd2
Revises: afd809d4acc1
Create Date: 2022-01-28 10:58:26.061229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34ba27e2dcd2'
down_revision = 'afd809d4acc1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
