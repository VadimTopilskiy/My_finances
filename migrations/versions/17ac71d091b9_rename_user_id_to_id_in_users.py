"""Rename user_id to id in users

Revision ID: 17ac71d091b9
Revises: 27403b8f8581
Create Date: 2025-01-14 22:24:05.775439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '17ac71d091b9'
down_revision: Union[str, None] = '27403b8f8581'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('user_id', new_column_name='id', existing_type=sa.dialects.postgresql.UUID(as_uuid=True),
                              nullable=False)


def downgrade() -> None:
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id', new_column_name='user_id', existing_type=sa.dialects.postgresql.UUID(as_uuid=True),
                              nullable=False)
