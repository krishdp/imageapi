"""add users table

Revision ID: afd809d4acc1
Revises: f03afbd6ad4e
Create Date: 2022-01-28 10:43:53.427304

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afd809d4acc1'
down_revision = 'f03afbd6ad4e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users', sa.Column('id', sa.Integer(),nullable=False),
                            sa.Column('email', sa.String(), nullable=False),
                            sa.Column('username', sa.String(), nullable=False),
                            sa.Column('password', sa.String(), nullable=False),
                            sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()'), nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
