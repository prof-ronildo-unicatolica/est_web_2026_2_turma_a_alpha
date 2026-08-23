from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Confere se a senha em texto puro corresponde ao hash armazenado."""
    return pwd_context.verify(senha_plana, senha_hash)


def gerar_hash_senha(senha_plana: str) -> str:
    """Gera o hash bcrypt de uma senha em texto puro."""
    return pwd_context.hash(senha_plana)


def criar_access_token(dados: dict) -> str:
    """Gera um JWT assinado, com expiracao, a partir dos dados informados."""
    to_encode = dados.copy()
    expira_em = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expira_em})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decodificar_access_token(token: str) -> dict | None:
    """Valida e decodifica um JWT. Retorna None se invalido ou expirado."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None