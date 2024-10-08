"""empty message

Revision ID: 55d6ae76421b
Revises: e5a9b2b0cd73
Create Date: 2024-09-11 14:23:49.246292

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55d6ae76421b'
down_revision = 'e5a9b2b0cd73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=100), nullable=False))
        batch_op.drop_column('password_hash')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
        batch_op.drop_column('password')

    # ### end Alembic commands ###
