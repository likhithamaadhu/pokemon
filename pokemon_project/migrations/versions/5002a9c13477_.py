"""empty message

Revision ID: 5002a9c13477
Revises: 
Create Date: 2023-05-27 11:14:03.020311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5002a9c13477'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pokemon',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('type_1', sa.Text(), nullable=True),
    sa.Column('type_2', sa.Text(), nullable=True),
    sa.Column('total', sa.Integer(), nullable=True),
    sa.Column('hp', sa.Integer(), nullable=True),
    sa.Column('attack', sa.Integer(), nullable=True),
    sa.Column('defense', sa.Integer(), nullable=True),
    sa.Column('sp_atk', sa.Integer(), nullable=True),
    sa.Column('sp_def', sa.Integer(), nullable=True),
    sa.Column('speed', sa.Integer(), nullable=True),
    sa.Column('generation', sa.Integer(), nullable=True),
    sa.Column('legendary', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon')
    # ### end Alembic commands ###