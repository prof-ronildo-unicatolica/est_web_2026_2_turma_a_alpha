"""criar tabelas cidades e hoteis

Revision ID: 003
Revises: 002
Create Date: 2026-09-07 14:00:00.000000

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

# Identificadores de revisão do Alembic
revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Criar tabela de cidades
    op.create_table(
        "cidades",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # 2. Criar tabela de hoteis (com chave estrangeira cidade_id apontando para cidades.id)
    op.create_table(
        "hoteis",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("cidade_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["cidade_id"], ["cidades.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    # Ordem reversa: apaga hoteis primeiro (dependente), depois cidades
    op.drop_table("hoteis")
    op.drop_table("cidades")