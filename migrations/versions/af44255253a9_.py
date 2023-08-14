"""empty message

Revision ID: af44255253a9
Revises: 3c08e474d28b
Create Date: 2021-03-01 20:05:04.873493

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af44255253a9'
down_revision = '3c08e474d28b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('app_ibfk_1', 'app', type_='foreignkey')
    op.create_foreign_key(None, 'app', 'developer', ['Did'], ['Did'], ondelete='CASCADE')
    op.drop_constraint('face_ibfk_1', 'face', type_='foreignkey')
    op.create_foreign_key(None, 'face', 'app', ['Apid'], ['Apid'], ondelete='CASCADE')
    op.drop_constraint('record_ibfk_1', 'record', type_='foreignkey')
    op.create_foreign_key(None, 'record', 'app', ['Apid'], ['Apid'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'record', type_='foreignkey')
    op.create_foreign_key('record_ibfk_1', 'record', 'app', ['Apid'], ['Apid'])
    op.drop_constraint(None, 'face', type_='foreignkey')
    op.create_foreign_key('face_ibfk_1', 'face', 'app', ['Apid'], ['Apid'])
    op.drop_constraint(None, 'app', type_='foreignkey')
    op.create_foreign_key('app_ibfk_1', 'app', 'developer', ['Did'], ['Did'])
    # ### end Alembic commands ###
