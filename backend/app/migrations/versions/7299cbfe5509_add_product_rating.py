"""add_product_rating

Revision ID: 7299cbfe5509
Revises: 4921259ead2e
Create Date: 2025-10-19 16:23:24.281775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7299cbfe5509'
down_revision: Union[str, Sequence[str], None] = '4921259ead2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('rating', sa.Float(), nullable=True))
    op.execute("UPDATE products SET rating = 0.0 WHERE rating IS NULL")
    op.alter_column('products', 'rating', nullable=False, server_default='0.0')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('products', 'rating')
