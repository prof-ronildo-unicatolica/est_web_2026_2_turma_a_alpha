from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    email: str
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UsuarioCreateSchema(BaseModel):
    """Dados exigidos para cadastro de um novo usuario (POST /auth/register)."""

    nome: str
    email: str
    senha: str


class UsuarioPublic(BaseModel):
    """Perfil publico do usuario (nunca expoe senha/hash)."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    nome: str
    is_admin: bool