"""add content column to posts table

Revision ID: 8a33c1201619
Revises: 86d42f033b57
Create Date: 2023-05-02 15:20:22.030853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a33c1201619'
down_revision = '86d42f033b57'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
