from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decodificar_access_token, verificar_senha
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository

bearer_scheme = HTTPBearer(description="Use o token retornado por POST /auth/login")


def autenticar_credenciais(db: Session, email: str, senha: str) -> Usuario | None:
    """Confere e-mail/senha contra o banco, usando bcrypt."""
    usuario = UsuarioRepository(db).buscar_por_email(email)
    if usuario is None or not verificar_senha(senha, usuario.senha_hash):
        return None
    return usuario


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """Valida o JWT e retorna o usuario autenticado (a partir do banco)."""
    payload = decodificar_access_token(credentials.credentials)
    if payload is None or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario = UsuarioRepository(db).buscar_por_email(payload["sub"])
    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario nao encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return usuario


def get_current_admin(usuario: Usuario = Depends(get_current_user)) -> Usuario:
    """Autorizacao (RBAC): exige is_admin=True."""
    if not usuario.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return usuario