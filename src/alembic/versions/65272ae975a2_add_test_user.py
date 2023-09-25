"""add_test_user

Revision ID: 65272ae975a2
Revises: fa5378814a19
Create Date: 2023-09-19 14:17:16.495358

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "65272ae975a2"
down_revision: Union[str, None] = "fa5378814a19"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    users_table = sa.table(
        "users", sa.column("username", sa.String), sa.column("api_key", sa.String)
    )

    op.bulk_insert(
        users_table,
        [
            {"username": "testuser1", "api_key": "test"},
            {"username": "testuser2", "api_key": "test2"},
            {"username": "testuser3", "api_key": "test3"},
        ],
    )

    users_to_users_table = sa.table(
        "user_to_user",
        sa.column("follower_id", sa.Integer),
        sa.column("following_id", sa.Integer),
    )

    op.bulk_insert(
        users_to_users_table,
        [
            {"follower_id": 1, "following_id": 3},
            {"follower_id": 3, "following_id": 1},
        ],
    )


def downgrade() -> None:
    users_table = sa.table(
        "users", sa.column("username", sa.String), sa.column("api_key", sa.String)
    )
    op.execute(
        users_table.delete().where(
            users_table.c.username.in_(["testuser1", "testuser2", "testuser3"])
        )
    )

    users_to_users_table = sa.table(
        "user_to_user",
        sa.column("follower_id", sa.Integer),
        sa.column("following_id", sa.Integer),
    )
    op.execute(
        users_to_users_table.delete().where(
            users_to_users_table.c.follower_id.in_([1, 3])
        )
    )
