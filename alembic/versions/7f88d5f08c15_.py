"""empty message

Revision ID: 7f88d5f08c15
Revises: 
Create Date: 2023-06-14 15:35:28.745336

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f88d5f08c15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('id_olx', sa.Float(), nullable=True),
    sa.Column('id_otodom', sa.Float(), nullable=True),
    sa.Column('rooms', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('district', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_olx'),
    sa.UniqueConstraint('id_otodom')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('records')
    # ### end Alembic commands ###
