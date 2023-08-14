"""empty message

Revision ID: c7c8ced99a84
Revises: d667a12885a7
Create Date: 2021-02-11 00:42:16.641561

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c7c8ced99a84'
down_revision = 'd667a12885a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('appkey')
    op.add_column('app', sa.Column('Kdate', sa.Date(), nullable=False))
    op.add_column('app', sa.Column('Kvalue', sa.String(length=50), nullable=False))
    op.add_column('developer', sa.Column('isDelete', sa.Boolean(), nullable=True))
    op.add_column('record', sa.Column('Apid', sa.Integer(), nullable=False))
    op.add_column('record', sa.Column('isSuceess', sa.Boolean(), nullable=False))
    op.create_foreign_key(None, 'record', 'app', ['Apid'], ['Apid'])
    op.drop_column('record', 'Rtype')
    op.drop_column('record', 'Ritemid')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('record', sa.Column('Ritemid', mysql.VARCHAR(length=10), nullable=False))
    op.add_column('record', sa.Column('Rtype', mysql.VARCHAR(length=10), nullable=False))
    op.drop_constraint(None, 'record', type_='foreignkey')
    op.drop_column('record', 'isSuceess')
    op.drop_column('record', 'Apid')
    op.drop_column('developer', 'isDelete')
    op.drop_column('app', 'Kvalue')
    op.drop_column('app', 'Kdate')
    op.create_table('appkey',
    sa.Column('Kid', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Did', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('Kvalue', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('Kdate', sa.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['Did'], ['developer.Did'], name='appkey_ibfk_1'),
    sa.PrimaryKeyConstraint('Kid'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
