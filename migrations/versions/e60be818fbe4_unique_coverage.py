"""Unique coverage

Revision ID: e60be818fbe4
Revises: 443250179fe1
Create Date: 2025-03-09 17:00:20.937089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e60be818fbe4'
down_revision = '443250179fe1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(
        'unique_coverage_data',
        'network_providers_coverage',
        ['operator', 'insee_code', 'post_code','type_2g','type_3g','type_4g']
    )


def downgrade():
    op.drop_constraint(
        'unique_coverage_data',
        'network_providers_coverage'
    )
