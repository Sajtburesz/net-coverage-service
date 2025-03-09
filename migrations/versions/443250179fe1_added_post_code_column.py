"""Added post_code column

Revision ID: 443250179fe1
Revises: cb89a5ad55b5
Create Date: 2025-03-09 13:08:48.215299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '443250179fe1'
down_revision = 'cb89a5ad55b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('network_providers_coverage', sa.Column('post_code', sa.Integer(), nullable=False),)


def downgrade():
    op.drop_column('network_providers_coverage', 'post_code')
