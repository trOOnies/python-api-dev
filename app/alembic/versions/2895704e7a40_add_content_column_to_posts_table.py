"""add content column to posts table

Revision ID: 2895704e7a40
Revises: 1f971a3f752f
Create Date: 2022-07-05 20:57:21.489220

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2895704e7a40'
down_revision = '1f971a3f752f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("posts", "content")
