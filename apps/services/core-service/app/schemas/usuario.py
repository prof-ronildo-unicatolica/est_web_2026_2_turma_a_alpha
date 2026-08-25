import uuid
from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    """Dados enviados pelo usuário na hora do login."""
    email: str
    senha: str


class Token(BaseModel):
    """Formato do Token JWT retornado após o login bem-sucedido."""
    access_token: str
    token_type: str = "bearer"


class UsuarioCreate(BaseModel):
    """Dados enviados pelo cliente no formulário de cadastro."""
    nome: str
    email: str
    senha: str


class UsuarioPublic(BaseModel):
    """Perfil público do usuário retornado nas APIs (nunca expõe a senha)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    nome: str
    email: str
    is_admin: bool