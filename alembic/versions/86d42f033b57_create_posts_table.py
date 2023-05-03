"""create posts table

Revision ID: 86d42f033b57
Revises: 
Create Date: 2023-05-02 13:41:15.350749

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '86d42f033b57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
    pass
