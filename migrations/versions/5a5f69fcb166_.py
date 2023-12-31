"""empty message

Revision ID: 5a5f69fcb166
Revises: 6ece5dbbc015
Create Date: 2021-04-07 21:21:49.573193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a5f69fcb166'
down_revision = '6ece5dbbc015'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('developer', sa.Column('Dbirth', sa.Date(), nullable=True))
    op.add_column('developer', sa.Column('Demail', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('developer', 'Demail')
    op.drop_column('developer', 'Dbirth')
    # ### end Alembic commands ###
