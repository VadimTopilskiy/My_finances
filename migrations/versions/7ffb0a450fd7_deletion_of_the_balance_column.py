"""deletion of the “balance” column

Revision ID: 7ffb0a450fd7
Revises: 9139b0a59547
Create Date: 2025-01-26 16:52:30.471398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ffb0a450fd7'
down_revision: Union[str, None] = '9139b0a59547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('finances', 'balance')


def downgrade() -> None:
    op.add_column(
        'finances',
        sa.Column('balance', sa.String(length=255), nullable=True)
    )
