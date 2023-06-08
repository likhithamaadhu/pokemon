"""adding column defaults and nullable

Revision ID: 04d31b03f80c
Revises: 5002a9c13477
Create Date: 2023-06-08 13:24:10.630874

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04d31b03f80c'
down_revision = '5002a9c13477'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.alter_column('type_1',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('total',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('hp',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('attack',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('defense',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('sp_atk',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('sp_def',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('speed',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('generation',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('legendary',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pokemon', schema=None) as batch_op:
        batch_op.alter_column('legendary',
               existing_type=sa.BOOLEAN(),
               nullable=True)
        batch_op.alter_column('generation',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('speed',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('sp_def',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('sp_atk',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('defense',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('attack',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('hp',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('total',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('type_1',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###
