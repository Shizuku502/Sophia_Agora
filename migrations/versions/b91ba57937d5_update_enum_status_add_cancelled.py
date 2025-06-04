"""update enum status add cancelled

Revision ID: b91ba57937d5
Revises: 67c3e4a30f71
Create Date: 2025-06-05 01:56:33.110219

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b91ba57937d5'
down_revision = '67c3e4a30f71'
branch_labels = None
depends_on = None


def upgrade():
    # Postgres 專用 Enum 修改（安全做法）
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        # 1. 建立新 Enum 類型
        new_type = postgresql.ENUM('pending', 'accepted', 'rejected', 'cancelled', name='appointment_status')
        new_type.create(bind, checkfirst=False)

        # 2. 替換欄位類型（使用 CAST）
        op.execute("ALTER TABLE appointments ALTER COLUMN status TYPE appointment_status USING status::text::appointment_status")

        # 3. 刪除舊 Enum 類型（如果需要）
        op.execute('DROP TYPE appointment_status_old')

    elif bind.dialect.name == 'mysql':
        # MySQL 直接 ALTER
        op.execute("ALTER TABLE appointments MODIFY COLUMN status ENUM('pending', 'accepted', 'rejected', 'cancelled')")

    else:
        raise NotImplementedError("Unsupported DB dialect")


def downgrade():
    bind = op.get_bind()
    if bind.dialect.name == 'postgresql':
        # 1. 恢復舊 enum 類型
        old_type = postgresql.ENUM('pending', 'accepted', 'rejected', name='appointment_status_old')
        old_type.create(bind, checkfirst=False)

        # 2. 替換欄位類型
        op.execute("ALTER TABLE appointments ALTER COLUMN status TYPE appointment_status_old USING status::text::appointment_status_old")

        # 3. 刪除新的 enum 類型
        op.execute('DROP TYPE appointment_status')

        # 4. 重新命名回去
        op.execute('ALTER TYPE appointment_status_old RENAME TO appointment_status')

    elif bind.dialect.name == 'mysql':
        op.execute("ALTER TABLE appointments MODIFY COLUMN status ENUM('pending', 'accepted', 'rejected')")

    else:
        raise NotImplementedError("Unsupported DB dialect")

