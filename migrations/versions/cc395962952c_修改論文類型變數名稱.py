"""修改論文類型變數名稱

Revision ID: cc395962952c
Revises: 75bf9a2cb969
Create Date: 2025-06-03 13:31:06.768692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'cc395962952c'
down_revision = '75bf9a2cb969'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher_papers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('paper_type', sa.String(length=50), nullable=False))
        batch_op.drop_column('type')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teacher_papers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_column('paper_type')

    # ### end Alembic commands ###
