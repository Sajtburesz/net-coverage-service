"""relationship between tables

Revision ID: 7516c29f2ce4
Revises: e60be818fbe4
Create Date: 2025-03-09 19:53:41.215806

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7516c29f2ce4'
down_revision = 'e60be818fbe4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(
        'fk_network_coverage_operator',
        'network_providers_coverage',
        'network_providers',
        ['operator'],
        ['operator'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('fk_network_coverage_operator', 'network_providers_coverage', type_='foreignkey')
