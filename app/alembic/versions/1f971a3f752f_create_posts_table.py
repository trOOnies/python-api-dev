"""create posts table

Revision ID: 1f971a3f752f
Revises: 
Create Date: 2022-07-05 20:45:50.937091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f971a3f752f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("posts")
