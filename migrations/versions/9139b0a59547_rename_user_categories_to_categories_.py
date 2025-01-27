"""rename user_categories to categories and rename name_cat to name_categories

Revision ID: 9139b0a59547
Revises: 7dccdf45c155
Create Date: 2025-01-25 12:33:32.897159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9139b0a59547'
down_revision: Union[str, None] = '7dccdf45c155'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Переименовываем таблицу user_categories в categories
    op.rename_table('user_categories', 'categories')

    # Переименовываем столбец name_cat в name_categories
    op.alter_column('categories', 'name_cat', new_column_name='name_categories')


def downgrade():
    # В случае отката переименовываем обратно
    op.alter_column('categories', 'name_categories', new_column_name='name_cat')
    op.rename_table('categories', 'user_categories')