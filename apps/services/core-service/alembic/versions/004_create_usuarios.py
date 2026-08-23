"""create usuarios table with seed (admin and cliente)

Revision ID: 004
Revises: 003
Create Date: 2026-08-23 00:00:00.000000

"""

import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from passlib.context import CryptContext

from alembic import op

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    # --- Seed: admin e cliente de demonstracao (mesmas credenciais do placeholder) ---
    admin_id = uuid.uuid4()
    cliente_id = uuid.uuid4()

    admin_hash = pwd_context.hash("admin123")
    cliente_hash = pwd_context.hash("cliente123")

    usuarios_table = sa.table(
        "usuarios",
        sa.column("id", sa.UUID()),
        sa.column("nome", sa.String()),
        sa.column("email", sa.String()),
        sa.column("senha_hash", sa.String()),
        sa.column("is_admin", sa.Boolean()),
    )

    op.bulk_insert(
        usuarios_table,
        [
            {
                "id": admin_id,
                "nome": "Administrador da Franquia",
                "email": "admin@hotel.com",
                "senha_hash": admin_hash,
                "is_admin": True,
            },
            {
                "id": cliente_id,
                "nome": "Cliente Demonstracao",
                "email": "cliente@hotel.com",
                "senha_hash": cliente_hash,
                "is_admin": False,
            },
        ],
    )


def downgrade() -> None:
    op.drop_table("usuarios")
