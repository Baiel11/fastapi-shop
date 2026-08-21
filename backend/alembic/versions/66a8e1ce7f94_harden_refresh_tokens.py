"""harden refresh tokens

Adds a DB-level default for `revoked` (so raw inserts can't leave the
NOT NULL column NULL) and an index on `expires_at` so the periodic
cleanup DELETE stays fast.

Revision ID: 66a8e1ce7f94
Revises: 3cea215db07d
Create Date: 2026-08-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '66a8e1ce7f94'
down_revision: Union[str, Sequence[str], None] = '3cea215db07d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'refresh_tokens', 'revoked',
        existing_type=sa.Boolean(),
        server_default=sa.text('false'),
        existing_nullable=False,
    )
    op.create_index('ix_refresh_tokens_expires_at', 'refresh_tokens', ['expires_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_refresh_tokens_expires_at', table_name='refresh_tokens')
    op.alter_column(
        'refresh_tokens', 'revoked',
        existing_type=sa.Boolean(),
        server_default=None,
        existing_nullable=False,
    )