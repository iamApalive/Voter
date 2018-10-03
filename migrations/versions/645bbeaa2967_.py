"""empty message

Revision ID: 645bbeaa2967
Revises: 6f77185c3c01
Create Date: 2018-10-02 22:24:41.555369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '645bbeaa2967'
down_revision = '6f77185c3c01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vote', sa.Column('vaoted_to', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vote', 'vaoted_to')
    # ### end Alembic commands ###
