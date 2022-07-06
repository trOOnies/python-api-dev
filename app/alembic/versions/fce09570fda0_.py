"""empty message

Revision ID: fce09570fda0
Revises: eca143f998d9
Create Date: 2022-07-05 21:18:05.072288

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fce09570fda0'
down_revision = 'eca143f998d9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column(
            "published",
            sa.Boolean(),
            nullable=False,
            server_default="TRUE"
        )
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()")
        )
    )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
