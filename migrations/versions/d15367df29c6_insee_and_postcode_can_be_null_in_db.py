"""insee and postcode can be null in db

Revision ID: d15367df29c6
Revises: 7516c29f2ce4
Create Date: 2025-03-10 14:29:12.199220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd15367df29c6'
down_revision = '7516c29f2ce4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("network_providers_coverage") as batch_op:
        batch_op.alter_column("insee_code", existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column("post_code", existing_type=sa.Integer(), nullable=True)


def downgrade():
    with op.batch_alter_table("network_providers_coverage") as batch_op:
        batch_op.alter_column("insee_code", existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column("post_code", existing_type=sa.Integer(), nullable=False)