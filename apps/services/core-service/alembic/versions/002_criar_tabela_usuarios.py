"""criar tabela usuarios

Revision ID: 002
Revises: 001
Create Date: 2026-08-20 18:00:00.000000

"""
import uuid
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from passlib.context import CryptContext

# Identificadores de revisão do Alembic
revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def upgrade() -> None:
    # 1. Criar tabela de usuários
    op.create_table(
        "usuarios",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("senha_hash", sa.String(length=255), nullable=False),
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=True)

    # 2. Seed do Admin inicial padrão (admin@hotel.com / admin123)
    admin_id = str(uuid.uuid4())
    senha_hash_admin = pwd_context.hash("admin123")
    
    op.execute(
        f"""
        INSERT INTO usuarios (id, nome, email, senha_hash, is_admin)
        VALUES ('{admin_id}', 'Administrador da Franquia', 'admin@hotel.com', '{senha_hash_admin}', true)
        """
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_table("usuarios")
