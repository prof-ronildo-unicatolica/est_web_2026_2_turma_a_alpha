from datetime import datetime, timedelta, timezone
from typing import Any
from jwt import PyJWTError, decode, encode
from passlib.context import CryptContext

from app.core.config import settings

# Configuração do contexto de criptografia de senha com Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Transforma a senha limpa digitada pelo usuário em um hash indecifrável."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara se a senha digitada no login é compatível com o hash salvo no banco."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: timedelta | None = None) -> str:
    """Cria e assina um Token JWT seguro contendo o ID do usuário e data de expiração."""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """Decodifica e valida um Token JWT recebido no cabeçalho das requisições."""
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        return None