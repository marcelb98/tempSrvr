"""init

Revision ID: e9a2fea799f6
Revises: 
Create Date: 2018-12-30 01:36:54.974640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9a2fea799f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('sensor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=True),
    sa.Column('api_key', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('passwort', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('value',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('temp', sa.Float(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('sensor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('view_permission',
    sa.Column('sensor_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['sensor_id'], ['sensor.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('sensor_id', 'user_id')
    )


def downgrade():
    op.drop_table('view_permission')
    op.drop_table('value')
    op.drop_table('user')
    op.drop_table('sensor')
