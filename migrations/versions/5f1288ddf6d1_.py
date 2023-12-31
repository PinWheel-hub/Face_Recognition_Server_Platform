"""empty message

Revision ID: 5f1288ddf6d1
Revises: dc54049e39c9
Create Date: 2021-03-16 08:52:08.148471

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5f1288ddf6d1'
down_revision = 'dc54049e39c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('isSuccess', sa.Boolean(), nullable=False))
    op.drop_column('record', 'isSuceess')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('isSuceess', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False))
    op.drop_column('record', 'isSuccess')
    # ### end Alembic commands ###
