"""empty message

Revision ID: 443370cd4904
Revises: None
Create Date: 2016-04-24 18:25:15.301062

"""

# revision identifiers, used by Alembic.
revision = '443370cd4904'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trabalhos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('startdate', sa.DateTime(), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('em_aberto', sa.Boolean(), nullable=False),
    sa.CheckConstraint('deadline >= startdate', name='deadline_maior_igual_que_startdate'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=54), nullable=True),
    sa.Column('superuser', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('register_date', sa.DateTime(), nullable=True),
    sa.Column('last_login', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('username')
    )
    op.create_table('trabalho_entregue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trabalho_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('path', sa.String(), nullable=True),
    sa.Column('entrega', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['trabalho_id'], ['trabalhos.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path'),
    sa.UniqueConstraint('user_id', 'trabalho_id', name='user_id_trabalho_id_par_unico')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('trabalho_entregue')
    op.drop_table('user')
    op.drop_table('trabalhos')
    ### end Alembic commands ###
