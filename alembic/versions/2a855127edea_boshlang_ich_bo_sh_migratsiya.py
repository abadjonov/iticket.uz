"""boshlang'ich bo'sh migratsiya

Revision ID: 2a855127edea
Revises:
Create Date: 2026-08-11 21:47:45.726168

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "2a855127edea"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
