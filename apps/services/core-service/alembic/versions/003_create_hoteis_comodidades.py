"""create hoteis, comodidades and hotel_comodidade tables

Revision ID: 003
Revises: 002
Create Date: 2026-08-23 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Criar tabela de Comodidades
    op.create_table(
        "comodidades",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nome"),
    )

    # 2. Criar tabela de Hoteis (FK para Cidade)
    op.create_table(
        "hoteis",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=150), nullable=False),
        sa.Column("categoria_estrelas", sa.Integer(), nullable=False),
        sa.Column("cidade_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cidade_id"], ["cidades.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # 3. Criar tabela associativa Hotel <-> Comodidade (N:M)
    op.create_table(
        "hotel_comodidade",
        sa.Column("hotel_id", sa.UUID(), nullable=False),
        sa.Column("comodidade_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"], ["hoteis.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["comodidade_id"], ["comodidades.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("hotel_id", "comodidade_id"),
    )


def downgrade() -> None:
    op.drop_table("hotel_comodidade")
    op.drop_table("hoteis")
    op.drop_table("comodidades")
