"""empty message

Revision ID: e5a9b2b0cd73
Revises: 
Create Date: 2024-09-09 12:59:22.841531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a9b2b0cd73'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Users',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('Posts',
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('content_', sa.Text(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['uid'], ['Users.uid'], ),
    sa.PrimaryKeyConstraint('pid')
    )
    op.create_table('Comments',
    sa.Column('cid', sa.Integer(), nullable=False),
    sa.Column('content_', sa.Text(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['pid'], ['Posts.pid'], ),
    sa.ForeignKeyConstraint(['uid'], ['Users.uid'], ),
    sa.PrimaryKeyConstraint('cid')
    )
    op.create_table('Likes',
    sa.Column('lid', sa.Integer(), nullable=False),
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('pid', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pid'], ['Posts.pid'], ),
    sa.ForeignKeyConstraint(['uid'], ['Users.uid'], ),
    sa.PrimaryKeyConstraint('lid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Likes')
    op.drop_table('Comments')
    op.drop_table('Posts')
    op.drop_table('Users')
    # ### end Alembic commands ###
