"""empty message

Revision ID: 600773643c2f
Revises: 
Create Date: 2018-10-01 20:21:04.173207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '600773643c2f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('poll',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('voters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('username', sa.String(length=60), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('poll_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_voters_email'), 'voters', ['email'], unique=True)
    op.create_index(op.f('ix_voters_first_name'), 'voters', ['first_name'], unique=False)
    op.create_index(op.f('ix_voters_last_name'), 'voters', ['last_name'], unique=False)
    op.create_index(op.f('ix_voters_username'), 'voters', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_voters_username'), table_name='voters')
    op.drop_index(op.f('ix_voters_last_name'), table_name='voters')
    op.drop_index(op.f('ix_voters_first_name'), table_name='voters')
    op.drop_index(op.f('ix_voters_email'), table_name='voters')
    op.drop_table('voters')
    op.drop_table('roles')
    op.drop_table('poll')
    # ### end Alembic commands ###
