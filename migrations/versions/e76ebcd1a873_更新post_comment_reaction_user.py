"""更新POST, Comment, Reaction, User

Revision ID: e76ebcd1a873
Revises: 4e033e305d9f
Create Date: 2025-05-27 18:25:52.527334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e76ebcd1a873'
down_revision = '4e033e305d9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar_filename', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('avatar_filename')

    # ### end Alembic commands ###
