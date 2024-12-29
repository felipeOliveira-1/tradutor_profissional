"""update_models

Revision ID: 510fe3f120f2
Revises: eefa6da3aaf0
Create Date: 2024-12-29 16:09:17.493372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '510fe3f120f2'
down_revision: Union[str, None] = 'eefa6da3aaf0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('chapters', 'document_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('chapters', 'title',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('chapters', 'order',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('documents', 'filename',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('documents', 'mime_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('documents', 'file_path',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('documents', 'processed_path')
    op.alter_column('translations', 'domain_specific',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('translations', 'locale_specific',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('translations', 'has_been_edited',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(),
               existing_nullable=True)
    op.alter_column('translations', 'project_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.Integer(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('translations', 'project_id',
               existing_type=sa.Integer(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.alter_column('translations', 'has_been_edited',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('translations', 'locale_specific',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(length=20),
               existing_nullable=True)
    op.alter_column('translations', 'domain_specific',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
    op.add_column('documents', sa.Column('processed_path', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('documents', 'file_path',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('documents', 'mime_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('documents', 'filename',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('chapters', 'order',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('chapters', 'title',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('chapters', 'document_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
