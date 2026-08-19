"""fix created_at default

Revision ID: b1e7afd47003
Revises: 207c44d9cb30
Create Date: 2026-08-19 13:46:20.172501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1e7afd47003'
down_revision: Union[str, Sequence[str], None] = '207c44d9cb30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Backfill existing rows created before the DEFAULT existed (one-time repair)
    op.execute("UPDATE products SET created_at = now() WHERE created_at IS NULL")
    op.execute("UPDATE users SET created_at = now() WHERE created_at IS NULL")

    # Add a real DB-level default + NOT NULL so the server always fills created_at
    op.alter_column('products', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=True,
               nullable=False)
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=sa.text('now()'),
               existing_nullable=True,
               nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('products', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=None,
               existing_nullable=False,
               nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               server_default=None,
               existing_nullable=False,
               nullable=True)
