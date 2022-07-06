"""add foreign key to posts table

Revision ID: eca143f998d9
Revises: 2f6ed760871c
Create Date: 2022-07-05 21:13:05.743998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eca143f998d9'
down_revision = '2f6ed760871c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        "posts_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
    )


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
