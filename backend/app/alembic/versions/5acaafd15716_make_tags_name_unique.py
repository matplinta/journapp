"""make tags name unique

Revision ID: 5acaafd15716
Revises: 07148db85539
Create Date: 2022-05-22 18:22:46.683374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5acaafd15716'
down_revision = '07148db85539'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_tag_name', table_name='tag')
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.create_index('ix_tag_name', 'tag', ['name'], unique=False)
    # ### end Alembic commands ###